"""Text summarization service."""

import logging
import re
from typing import List, Literal, Tuple

import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

MODE_RATIOS = {
    "brief": (0.15, 0.25),
    "standard": (0.30, 0.40),
    "detailed": (0.50, 0.60),
}

POSITION_BOOST_INTRO = 0.15
POSITION_BOOST_CONCLUSION = 0.10

MIN_SENTENCE_LENGTH = 15


def split_into_sentences(text: str) -> List[str]:
    if not text or not text.strip():
        return []
    
    sentence_pattern = r'[^.!?؟¿¡\n]+[.!?؟]+(?=\s|$|\n)'
    
    matches = re.finditer(sentence_pattern, text)
    sentences = []
    
    for match in matches:
        sentence = match.group(0).strip()
        if sentence and len(sentence) >= MIN_SENTENCE_LENGTH:
            sentences.append(sentence)
    
    if '\n' in text and not sentences:
        lines = text.split('\n')
        sentences = [line.strip() for line in lines if line.strip() and len(line.strip()) >= MIN_SENTENCE_LENGTH]
    
    if not sentences:
        return [text.strip()] if text.strip() else []
    
    return sentences


def split_into_paragraphs(text: str) -> List[str]:
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]


def build_similarity_matrix(sentences: List[str]) -> np.ndarray:
    if len(sentences) == 0:
        return np.array([])
    
    if len(sentences) == 1:
        return np.array([[1.0]])
    
    try:
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            stop_words=None,
            token_pattern=r'\S+',
            max_features=1000
        )
        tfidf_matrix = vectorizer.fit_transform(sentences)
        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    except Exception as e:
        logger.warning(f"TF-IDF vectorization failed: {e}. Using word overlap fallback.")
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        for i, sent_i in enumerate(sentences):
            for j, sent_j in enumerate(sentences):
                words_i = set(sent_i.lower().split())
                words_j = set(sent_j.lower().split())
                if words_i and words_j:
                    similarity_matrix[i][j] = len(words_i & words_j) / len(words_i | words_j)
                else:
                    similarity_matrix[i][j] = 0.0
        np.fill_diagonal(similarity_matrix, 1.0)
    
    return similarity_matrix


def calculate_position_score(index: int, total: int) -> float:
    if total <= 1:
        return 1.0
    
    relative_position = index / total
    
    if relative_position <= 0.20:
        return 1.0 + POSITION_BOOST_INTRO
    
    if relative_position >= 0.90:
        return 1.0 + POSITION_BOOST_CONCLUSION
    
    return 1.0


def normalize_sentence_length_score(sentence: str, avg_length: float) -> float:
    length = len(sentence)
    
    if avg_length == 0:
        return 1.0
    
    ratio = length / avg_length
    
    if ratio < 0.5:
        return 0.85
    
    if ratio > 2.0:
        return 0.90
    
    return 1.0


def intelligent_sentence_selection(
    sentences: List[str],
    pagerank_scores: dict,
    mode: Literal["brief", "standard", "detailed"]
) -> List[Tuple[str, int]]:
    if not sentences:
        return []
    
    total_sentences = len(sentences)
    avg_length = sum(len(s) for s in sentences) / total_sentences
    
    min_ratio, max_ratio = MODE_RATIOS[mode]
    target_count = int(total_sentences * ((min_ratio + max_ratio) / 2))
    target_count = max(2, min(target_count, total_sentences))
    
    sentence_data = []
    for i, sentence in enumerate(sentences):
        pagerank_score = pagerank_scores.get(i, 0.0)
        position_boost = calculate_position_score(i, total_sentences)
        length_norm = normalize_sentence_length_score(sentence, avg_length)
        
        final_score = pagerank_score * position_boost * length_norm
        
        sentence_data.append({
            'sentence': sentence,
            'index': i,
            'score': final_score,
            'pagerank': pagerank_score,
            'position': i / total_sentences if total_sentences > 1 else 0.5
        })
    
    sentence_data.sort(key=lambda x: x['score'], reverse=True)
    
    selected = []
    selected_positions = []
    
    for data in sentence_data:
        if len(selected) >= target_count:
            break
        
        position = data['position']
        too_clustered = False
        
        for sel_pos in selected_positions:
            if abs(position - sel_pos) < 0.15:
                nearby = sum(1 for p in selected_positions if abs(p - position) < 0.15)
                if nearby >= 2:
                    too_clustered = True
                    break
        
        if not too_clustered or len(selected) < 2:
            selected.append((data['sentence'], data['index']))
            selected_positions.append(position)
    
    if len(selected) < 2 and len(sentence_data) >= 2:
        for data in sentence_data:
            if (data['sentence'], data['index']) not in selected:
                selected.append((data['sentence'], data['index']))
                if len(selected) >= 2:
                    break
    
    selected.sort(key=lambda x: x[1])
    
    return selected


def textrank_summarize(
    text: str,
    mode: Literal["brief", "standard", "detailed"] = "standard",
    preserve_structure: bool = False
) -> str:
    if not text or not text.strip():
        return ""
    
    text = text.strip()
    
    sentences = split_into_sentences(text)
    
    if not sentences:
        return text
    
    if len(sentences) == 1:
        return sentences[0]
    
    if len(sentences) <= 3:
        return " ".join(sentences)
    
    similarity_matrix = build_similarity_matrix(sentences)
    
    graph = nx.Graph()
    graph.add_nodes_from(range(len(sentences)))
    
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            similarity = similarity_matrix[i][j]
            if similarity > 0:
                graph.add_edge(i, j, weight=similarity)
    
    try:
        pagerank_scores = nx.pagerank(graph, max_iter=100, tol=1e-6)
    except Exception as e:
        logger.warning(f"PageRank computation failed: {e}. Using uniform scores.")
        pagerank_scores = {i: 1.0 / len(sentences) for i in range(len(sentences))}
    
    selected_sentences = intelligent_sentence_selection(
        sentences,
        pagerank_scores,
        mode
    )
    
    if not selected_sentences:
        return sentences[0]
    
    if preserve_structure:
        paragraphs = split_into_paragraphs(text)
        if len(paragraphs) > 1:
            summary_parts = []
            for para in paragraphs:
                para_sentences = split_into_sentences(para)
                para_summary = [
                    sent for sent, _ in selected_sentences
                    if sent in para_sentences
                ]
                if para_summary:
                    summary_parts.append(" ".join(para_summary))
            
            return "\n\n".join(summary_parts) if summary_parts else " ".join(sent for sent, _ in selected_sentences)
    
    summary = " ".join(sent for sent, _ in selected_sentences)
    
    return summary


def summarize_text(
    text: str,
    mode: Literal["brief", "standard", "detailed"] = "standard",
    preserve_structure: bool = False
) -> str:
    """Summarize text."""
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    logger.info(
        f"Summarizing text: length={len(text)}, mode={mode}, preserve_structure={preserve_structure}"
    )
    
    try:
        summary = textrank_summarize(text, mode, preserve_structure)
        logger.info(f"Summarization complete: summary_length={len(summary)}")
        return summary
    except Exception as e:
        logger.error(f"Error during summarization: {e}", exc_info=True)
        raise

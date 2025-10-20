import re
from typing import List

def summarize_text(text: str, max_length: int = 100) -> str:
    """
    Summarize text by extracting key sentences and limiting length.
    
    Args:
        text: Input text to summarize
        max_length: Maximum length of the summary
    
    Returns:
        Summarized text
    """
    if not text or not text.strip():
        return ""
    
    # Clean the text
    text = text.strip()
    
    # Split into sentences
    sentences = split_into_sentences(text)
    
    if not sentences:
        return text[:max_length]
    
    # If text is already short enough, return as is
    if len(text) <= max_length:
        return text
    
    # Simple summarization: take first few sentences that fit within max_length
    summary_sentences = []
    current_length = 0
    
    for sentence in sentences:
        # Add space between sentences (except for the first one)
        space_needed = 1 if summary_sentences else 0
        if current_length + len(sentence) + space_needed <= max_length:
            summary_sentences.append(sentence)
            current_length += len(sentence) + space_needed
        else:
            break
    
    # If no sentences fit, truncate the first sentence
    if not summary_sentences:
        if len(sentences[0]) > max_length:
            return sentences[0][:max_length-3] + "..."
        else:
            return sentences[0]
    
    summary = " ".join(summary_sentences)
    
    # Only add ellipsis if we actually truncated content
    # and we're at or near the max_length limit
    if len(summary) < len(text) and len(summary) >= max_length * 0.9:
        summary = summary.rstrip() + "..."
    
    return summary

def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences using simple regex.
    
    Args:
        text: Input text
    
    Returns:
        List of sentences
    """
    # Simple sentence splitting regex
    sentence_endings = r'[.!?]+'
    sentences = re.split(sentence_endings, text)
    
    # Clean up and filter empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences

def extract_keywords(text: str, num_keywords: int = 5) -> List[str]:
    """
    Extract keywords from text (simple implementation).
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
    
    Returns:
        List of keywords
    """
    # Simple keyword extraction based on word frequency
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
    
    # Count word frequencies
    word_freq = {}
    for word in words:
        if word not in stop_words and len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:num_keywords]]

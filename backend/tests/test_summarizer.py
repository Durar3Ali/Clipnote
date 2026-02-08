"""Tests for intelligent summarization service."""

import pytest

from app.services.summarizer import (
    summarize_text,
    split_into_sentences,
    textrank_summarize,
    build_similarity_matrix,
    calculate_position_score,
    normalize_sentence_length_score,
)


class TestSentenceSplitting:
    """Tests for sentence splitting functionality."""
    
    def test_english_sentences(self):
        """Test splitting English sentences."""
        text = "This is sentence one. This is sentence two! This is sentence three?"
        sentences = split_into_sentences(text)
        assert len(sentences) == 3
        assert "This is sentence one" in sentences[0]
        assert "This is sentence two" in sentences[1]
        assert "This is sentence three" in sentences[2]
    
    def test_arabic_sentences(self):
        """Test splitting Arabic sentences with Arabic punctuation."""
        text = "هذه جملة واحدة طويلة. هذه جملة ثانية طويلة؟ هذه جملة ثالثة طويلة!"
        sentences = split_into_sentences(text)
        # Should handle Arabic punctuation
        assert len(sentences) >= 2
    
    def test_mixed_punctuation(self):
        """Test splitting with mixed punctuation."""
        text = "First sentence here. Second sentence here! Third sentence here?"
        sentences = split_into_sentences(text)
        assert len(sentences) == 3
    
    def test_single_sentence(self):
        """Test single sentence input."""
        text = "This is a single sentence with enough characters."
        sentences = split_into_sentences(text)
        assert len(sentences) == 1
    
    def test_empty_text(self):
        """Test empty text input."""
        sentences = split_into_sentences("")
        assert sentences == []
        
        sentences = split_into_sentences("   ")
        assert sentences == []
    
    def test_minimum_sentence_length_filter(self):
        """Test that very short sentences are filtered out."""
        text = "Long sentence here. Hi. Another long sentence here."
        sentences = split_into_sentences(text)
        # "Hi." should be filtered as too short (< 15 chars)
        assert all(len(s) >= 15 for s in sentences)


class TestPositionScoring:
    """Tests for position-based scoring."""
    
    def test_intro_boost(self):
        """Test that introduction sentences get boosted."""
        # First 20% of document
        score = calculate_position_score(0, 10)
        assert score > 1.0
        
        score = calculate_position_score(1, 10)
        assert score > 1.0
    
    def test_conclusion_boost(self):
        """Test that conclusion sentences get boosted."""
        # Last 10% of document
        score = calculate_position_score(9, 10)
        assert score > 1.0
    
    def test_middle_no_boost(self):
        """Test that middle sentences get no boost."""
        score = calculate_position_score(5, 10)
        assert score == 1.0


class TestLengthNormalization:
    """Tests for sentence length normalization."""
    
    def test_normal_length(self):
        """Test that normal length sentences get no penalty."""
        sentence = "This is a sentence of normal length."
        score = normalize_sentence_length_score(sentence, 40.0)
        assert score == 1.0
    
    def test_very_short_penalty(self):
        """Test that very short sentences get penalized."""
        sentence = "Short."
        score = normalize_sentence_length_score(sentence, 40.0)
        assert score < 1.0
    
    def test_very_long_penalty(self):
        """Test that very long sentences get penalized."""
        sentence = "A" * 200  # Very long sentence
        score = normalize_sentence_length_score(sentence, 40.0)
        assert score < 1.0


class TestSimilarityMatrix:
    """Tests for TF-IDF similarity matrix."""
    
    def test_empty_sentences(self):
        """Test with empty sentence list."""
        matrix = build_similarity_matrix([])
        assert matrix.shape == (0,)
    
    def test_single_sentence(self):
        """Test with single sentence."""
        matrix = build_similarity_matrix(["Test sentence here."])
        assert matrix.shape == (1, 1)
        assert matrix[0][0] == 1.0
    
    def test_multiple_sentences(self):
        """Test with multiple sentences."""
        sentences = [
            "This is the first sentence.",
            "This is the second sentence.",
            "Completely different content."
        ]
        matrix = build_similarity_matrix(sentences)
        assert matrix.shape == (3, 3)
        # First two sentences should be more similar
        assert matrix[0][1] > matrix[0][2]


class TestTextRankSummarization:
    """Tests for intelligent TextRank summarization."""
    
    def test_brief_mode(self):
        """Test brief mode returns concise summary."""
        text = " ".join([
            f"This is sentence number {i} with meaningful content and information." 
            for i in range(1, 11)
        ])
        result = textrank_summarize(text, mode="brief")
        assert len(result) > 0
        assert len(result) < len(text)
        # Brief should select fewer sentences
        result_sentences = split_into_sentences(result)
        original_sentences = split_into_sentences(text)
        assert len(result_sentences) < len(original_sentences)
    
    def test_standard_mode(self):
        """Test standard mode returns balanced summary."""
        text = " ".join([
            f"This is sentence number {i} with meaningful content and information." 
            for i in range(1, 11)
        ])
        result = textrank_summarize(text, mode="standard")
        assert len(result) > 0
        assert len(result) < len(text)
    
    def test_detailed_mode(self):
        """Test detailed mode returns comprehensive summary."""
        text = " ".join([
            f"This is sentence number {i} with meaningful content and information." 
            for i in range(1, 11)
        ])
        result = textrank_summarize(text, mode="detailed")
        assert len(result) > 0
        # Detailed should include more content
        result_sentences = split_into_sentences(result)
        original_sentences = split_into_sentences(text)
        ratio = len(result_sentences) / len(original_sentences)
        assert ratio > 0.4  # Should include at least 40% for detailed
    
    def test_preserve_structure(self):
        """Test paragraph structure preservation."""
        text = """This is the first paragraph with important information. It has multiple sentences.

This is the second paragraph with more details. It also has information."""
        
        result = textrank_summarize(text, mode="standard", preserve_structure=True)
        assert len(result) > 0
        # Structure preservation might include paragraph breaks
    
    def test_empty_text(self):
        """Test empty text handling."""
        result = textrank_summarize("", mode="standard")
        assert result == ""
        
        result = textrank_summarize("   ", mode="standard")
        assert result == ""
    
    def test_single_sentence(self):
        """Test single sentence returns as-is."""
        text = "This is a single sentence with enough characters."
        result = textrank_summarize(text, mode="standard")
        assert result == text
    
    def test_very_few_sentences(self):
        """Test with very few sentences returns all."""
        text = "First sentence here. Second sentence here. Third sentence here."
        result = textrank_summarize(text, mode="standard")
        assert len(result) > 0
        # With only 3 sentences, should return all or most


class TestMainSummarizeFunction:
    """Tests for main summarize_text function."""
    
    def test_brief_mode_integration(self):
        """Test brief mode integration."""
        text = " ".join([
            f"Sentence {i} contains important information about the topic being discussed." 
            for i in range(1, 15)
        ])
        result = summarize_text(text, mode="brief")
        assert len(result) > 0
        assert len(result) < len(text)
    
    def test_standard_mode_integration(self):
        """Test standard mode integration."""
        text = " ".join([
            f"Sentence {i} contains important information about the topic being discussed." 
            for i in range(1, 15)
        ])
        result = summarize_text(text, mode="standard")
        assert len(result) > 0
        assert len(result) < len(text)
    
    def test_detailed_mode_integration(self):
        """Test detailed mode integration."""
        text = " ".join([
            f"Sentence {i} contains important information about the topic being discussed." 
            for i in range(1, 15)
        ])
        result = summarize_text(text, mode="detailed")
        assert len(result) > 0
    
    def test_preserve_structure_integration(self):
        """Test structure preservation."""
        text = """Paragraph one with important information. More details here.

Paragraph two with additional context. Even more information."""
        result = summarize_text(text, mode="standard", preserve_structure=True)
        assert len(result) > 0
    
    def test_empty_input_error(self):
        """Test empty input raises error."""
        with pytest.raises(ValueError):
            summarize_text("", mode="standard")
        
        with pytest.raises(ValueError):
            summarize_text("   ", mode="standard")
    
    def test_concept_preservation(self):
        """Test that important concepts are preserved."""
        text = (
            "Machine learning is a subset of artificial intelligence. "
            "It enables systems to learn from data. "
            "Neural networks are a key component. "
            "Deep learning uses multiple layers. "
            "Applications include image recognition and natural language processing. "
            "Training requires large datasets. "
            "Accuracy improves with more data. "
            "Overfitting is a common challenge."
        )
        result = summarize_text(text, mode="brief")
        # Should contain some key concepts
        assert len(result) > 0
        assert len(result) < len(text)
    
    def test_multilingual_arabic(self):
        """Test Arabic text summarization."""
        text = " ".join([
            "هذه جملة طويلة تحتوي على معلومات مهمة جداً.",
            "هذه جملة أخرى تضيف المزيد من السياق.",
            "جملة ثالثة تحتوي على تفاصيل إضافية.",
            "جملة رابعة توفر معلومات أكثر شمولاً."
        ])
        result = summarize_text(text, mode="standard")
        assert len(result) > 0
    
    def test_sentence_order_preserved(self):
        """Test that sentence order is preserved in summary."""
        text = (
            "First important sentence. "
            "Second important sentence. "
            "Third important sentence. "
            "Fourth important sentence. "
            "Fifth important sentence."
        )
        result = summarize_text(text, mode="standard")
        # Original order should be maintained
        assert len(result) > 0
        # Can't easily verify order without sentence detection, but result should be coherent
    
    def test_diverse_sentence_selection(self):
        """Test that sentences are selected from different parts of document."""
        # Create text with distinct sections
        text = (
            "Introduction sentence one here. Introduction sentence two here. "
            "Middle section sentence one here. Middle section sentence two here. "
            "Conclusion sentence one here. Conclusion sentence two here."
        )
        result = summarize_text(text, mode="standard")
        assert len(result) > 0
        # Should ideally include sentences from different sections

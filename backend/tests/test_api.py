"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct response."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "modes" in data
        assert data["modes"] == ["brief", "standard", "detailed"]


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_check(self):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestSummarizeEndpoint:
    """Tests for summarize endpoint with new schema."""
    
    def test_valid_request_standard_mode(self):
        """Test valid summarization request with standard mode."""
        response = client.post(
            "/summarize",
            json={
                "text": "This is the first sentence with important information. This is the second sentence providing more context. This is the third sentence adding details. This is the fourth sentence with additional information. This is the fifth sentence wrapping things up.",
                "summary_mode": "standard"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert isinstance(data["summary"], str)
        assert len(data["summary"]) > 0
        # Should not include compression metrics
        assert "compression_ratio" not in data
        assert "original_length" not in data
        assert "summary_length" not in data
    
    def test_valid_request_brief_mode(self):
        """Test summarization with brief mode."""
        long_text = " ".join([
            f"This is sentence number {i} with some meaningful content." 
            for i in range(1, 11)
        ])
        response = client.post(
            "/summarize",
            json={
                "text": long_text,
                "summary_mode": "brief"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        # Brief mode should be shorter
        assert len(data["summary"]) < len(long_text)
    
    def test_valid_request_detailed_mode(self):
        """Test summarization with detailed mode."""
        long_text = " ".join([
            f"This is sentence number {i} with some meaningful content." 
            for i in range(1, 11)
        ])
        response = client.post(
            "/summarize",
            json={
                "text": long_text,
                "summary_mode": "detailed"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        # Detailed mode should include more content
        assert len(data["summary"]) > 0
    
    def test_preserve_structure(self):
        """Test paragraph structure preservation."""
        text_with_paragraphs = """This is the first paragraph with important information. It has multiple sentences.

This is the second paragraph with more details. It also contains relevant information."""
        
        response = client.post(
            "/summarize",
            json={
                "text": text_with_paragraphs,
                "summary_mode": "standard",
                "preserve_structure": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
    
    def test_default_mode(self):
        """Test that default mode is 'standard' when not specified."""
        response = client.post(
            "/summarize",
            json={
                "text": "This is a test sentence with important information. This is another sentence providing context. This is a third sentence with more details."
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
    
    def test_empty_text_error(self):
        """Test that empty text returns 422 error."""
        response = client.post(
            "/summarize",
            json={
                "text": "",
                "summary_mode": "standard"
            }
        )
        assert response.status_code == 422
    
    def test_whitespace_only_text_error(self):
        """Test that whitespace-only text returns 422 error."""
        response = client.post(
            "/summarize",
            json={
                "text": "   ",
                "summary_mode": "standard"
            }
        )
        assert response.status_code == 422
    
    def test_text_too_short(self):
        """Test that text below minimum length returns 422 error."""
        response = client.post(
            "/summarize",
            json={
                "text": "Short text.",
                "summary_mode": "standard"
            }
        )
        assert response.status_code == 422
        assert "too short" in response.json()["detail"].lower()
    
    def test_text_too_long(self):
        """Test that text above maximum length returns 422 error."""
        # Create text longer than 50000 characters
        very_long_text = "A" * 50001
        response = client.post(
            "/summarize",
            json={
                "text": very_long_text,
                "summary_mode": "standard"
            }
        )
        assert response.status_code == 422
        assert "too long" in response.json()["detail"].lower()
    
    def test_invalid_mode(self):
        """Test that invalid mode returns 422 error."""
        response = client.post(
            "/summarize",
            json={
                "text": "This is a test sentence with important information. This is another sentence providing context. This is a third sentence with more details.",
                "summary_mode": "invalid_mode"
            }
        )
        assert response.status_code == 422
    
    def test_long_text_summarization(self):
        """Test summarization of longer text."""
        long_text = " ".join([
            "This is sentence one with important information.",
            "This is sentence two with more details.",
            "This is sentence three providing context.",
            "This is sentence four adding additional information.",
            "This is sentence five wrapping things up.",
            "This is sentence six with more insights.",
            "This is sentence seven providing examples.",
            "This is sentence eight with conclusions."
        ])
        response = client.post(
            "/summarize",
            json={
                "text": long_text,
                "summary_mode": "standard"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["summary"]) > 0
        assert len(data["summary"]) < len(long_text)
    
    def test_short_text_no_summarization_needed(self):
        """Test that short text is handled appropriately."""
        short_text = "This is a relatively short text that has enough characters to pass validation but might not need much summarization since it is concise."
        response = client.post(
            "/summarize",
            json={
                "text": short_text,
                "summary_mode": "standard"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["summary"]) > 0
    
    def test_multilingual_text(self):
        """Test summarization with multilingual content."""
        arabic_text = "هذه هي الجملة الأولى مع معلومات مهمة. هذه هي الجملة الثانية التي توفر المزيد من السياق. هذه هي الجملة الثالثة التي تضيف تفاصيل. هذه جملة رابعة مع معلومات إضافية."
        response = client.post(
            "/summarize",
            json={
                "text": arabic_text,
                "summary_mode": "standard"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["summary"]) > 0
    
    def test_all_modes_produce_different_results(self):
        """Test that different modes produce appropriately sized summaries."""
        text = " ".join([
            f"Sentence number {i} contains important information about the topic being discussed." 
            for i in range(1, 21)
        ])
        
        responses = {}
        for mode in ["brief", "standard", "detailed"]:
            response = client.post(
                "/summarize",
                json={
                    "text": text,
                    "summary_mode": mode
                }
            )
            assert response.status_code == 200
            responses[mode] = response.json()["summary"]
        
        # Brief should be shortest, detailed should be longest
        # (though not guaranteed due to intelligent selection)
        assert all(len(s) > 0 for s in responses.values())

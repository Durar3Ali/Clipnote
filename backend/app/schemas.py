"""Pydantic models."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TextInput(BaseModel):
    """Summarization request."""
    text: str = Field(
        ...,
        min_length=1,
        description="Text to summarize"
    )
    summary_mode: Literal["brief", "standard", "detailed"] = Field(
        default="standard",
        description=(
            "Summarization mode: "
            "'brief' (15-25% of content, key highlights only), "
            "'standard' (30-40% of content, balanced summary), "
            "'detailed' (50-60% of content, comprehensive overview)"
        )
    )
    preserve_structure: bool = Field(
        default=False,
        description="Maintain paragraph breaks and document structure in summary"
    )
    
    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class SummaryResponse(BaseModel):
    """Summarization response."""
    summary: str = Field(
        ...,
        description="Intelligent summary preserving core concepts and meaning"
    )

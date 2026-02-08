"""FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.schemas import SummaryResponse, TextInput
from app.services.summarizer import summarize_text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown logging."""
    settings = get_settings()
    logger.info(f"Starting Clipnote API v{settings.api_version}")
    logger.info(f"Allowed origins: {settings.allowed_origins_list}")
    yield
    logger.info("Shutting down Clipnote API")


# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Text summarization API.",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Clipnote API - Intelligent Text Summarization",
        "version": settings.api_version,
        "description": "AI-driven summarization that preserves core concepts",
        "documentation": "/docs",
        "modes": ["brief", "standard", "detailed"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/summarize", response_model=SummaryResponse)
async def summarize(text_input: TextInput):
    """Summarize text."""
    try:
        text_length = len(text_input.text)
        if text_length < settings.min_text_length:
            raise HTTPException(
                status_code=422,
                detail=f"Text too short. Minimum length: {settings.min_text_length} characters."
            )
        
        if text_length > settings.max_text_length:
            raise HTTPException(
                status_code=422,
                detail=f"Text too long. Maximum length: {settings.max_text_length} characters."
            )

        logger.info(
            f"Summarization request: text_length={text_length}, "
            f"mode={text_input.summary_mode}, preserve_structure={text_input.preserve_structure}"
        )

        summary = summarize_text(
            text_input.text,
            mode=text_input.summary_mode,
            preserve_structure=text_input.preserve_structure
        )
        
        return SummaryResponse(summary=summary)
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during summarization: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your text. Please try again."
        )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

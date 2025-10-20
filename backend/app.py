from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from summarizer import summarize_text
import uvicorn

app = FastAPI(title="Clipnote API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str
    max_length: int = 100

class SummaryResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int

@app.get("/")
async def root():
    return {"message": "Clipnote API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/summarize", response_model=SummaryResponse)
async def summarize(text_input: TextInput):
    try:
        if not text_input.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        summary = summarize_text(text_input.text, text_input.max_length)
        
        return SummaryResponse(
            summary=summary,
            original_length=len(text_input.text),
            summary_length=len(summary)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Clipnote

**Intelligent AI-powered text summarization that preserves core concepts**

Clipnote is a modern text summarization tool built with FastAPI and React that uses advanced TextRank algorithm with TF-IDF and PageRank to extract the most important information while maintaining meaning and coherence.

## Features

- **Intelligent Summarization** - Uses TextRank with TF-IDF vectorization and PageRank scoring to identify key sentences
- **Three Smart Modes** - Brief (quick highlights), Standard (balanced), or Detailed (comprehensive)
- **Concept Preservation** - Focuses on preserving core meaning rather than arbitrary length targets
- **Position-Aware Scoring** - Gives appropriate weight to introduction and conclusion sentences
- **Diversity Selection** - Ensures sentences are selected from different parts of the document
- **Multilingual Support** - Handles English, Arabic, Spanish, and French text
- **Structure Preservation** - Option to maintain paragraph breaks in summaries
- **Modern UI** - Clean, intuitive interface with real-time validation
- **Professional API** - Well-documented FastAPI backend with automatic OpenAPI docs
- **Production-Ready** - Environment-based configuration, comprehensive error handling, and logging

## How It Works

Clipnote uses an enhanced **TextRank algorithm** that combines multiple techniques:

1. **Sentence Segmentation** - Splits text into sentences with multilingual punctuation support
2. **TF-IDF Vectorization** - Converts sentences into numerical vectors based on term importance
3. **Similarity Matrix** - Computes cosine similarity between all sentence pairs
4. **Graph Construction** - Builds a weighted graph where nodes are sentences and edges represent similarity
5. **PageRank Scoring** - Applies Google's PageRank algorithm to score sentence importance
6. **Intelligent Selection** - Selects sentences based on:
   - PageRank centrality score
   - Position in document (introduction/conclusion boost)
   - Length normalization (avoid fragments)
   - Diversity (coverage across document sections)
7. **Order Preservation** - Maintains original sentence order for readability

The result is an intelligent summary that captures the core concepts and key information, not just the first few sentences.

## Quick Start

### Prerequisites

- Python 3.11+ (recommended)
- Node.js 20+ (recommended)
- npm (comes with Node.js)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. (Optional) Configure environment variables:
   ```bash
   # Copy the example file
   cp .env.example .env
   # Edit .env with your settings if needed
   ```

6. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   
   **API Documentation:** Visit `http://localhost:8000/docs` for interactive API documentation

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. (Optional) Configure environment variables:
   ```bash
   # Copy the example file
   cp .env.example .env
   # Edit .env if your backend is running on a different URL
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

## Usage

1. **Start both servers** (backend and frontend) following the setup instructions above
2. **Open the application** in your browser at `http://localhost:5173`
3. **Paste or type** the text you want to summarize (minimum 100 characters)
4. **Select a mode:**
   - **Brief** - Quick highlights of key points (15-25% of content)
   - **Standard** - Balanced comprehensive summary (30-40% of content)
   - **Detailed** - In-depth overview with context (50-60% of content)
5. **Optional:** Enable "Preserve paragraph structure" for structured documents
6. **Click "Summarize"** or press Ctrl+Enter
7. **View your intelligent summary** that preserves core concepts
8. **Copy** the summary to clipboard with one click

## API Endpoints

### `GET /`
Returns API information and available modes.

**Response:**
```json
{
  "message": "Clipnote API - Intelligent Text Summarization",
  "version": "2.0.0",
  "description": "AI-driven summarization that preserves core concepts",
  "documentation": "/docs",
  "modes": ["brief", "standard", "detailed"]
}
```

### `GET /health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

### `POST /summarize`
Generate an intelligent summary that preserves core concepts.

**Request Body:**
```json
{
  "text": "Your text to summarize...",
  "summary_mode": "standard",
  "preserve_structure": false
}
```

**Parameters:**
- `text` (required): Text to summarize (100-50,000 characters)
- `summary_mode` (optional): Summarization mode - `"brief"`, `"standard"` (default), or `"detailed"`
- `preserve_structure` (optional): Maintain paragraph breaks (default: `false`)

**Response:**
```json
{
  "summary": "Intelligent summary preserving core concepts..."
}
```

**Error Responses:**
- `422 Unprocessable Entity`: Validation error (empty text, too short/long)
- `500 Internal Server Error`: Processing error

## API Examples

### Brief Summary
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long article or document text here...",
    "summary_mode": "brief"
  }'
```

### Standard Summary with Structure Preservation
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Paragraph one...\n\nParagraph two...",
    "summary_mode": "standard",
    "preserve_structure": true
  }'
```

### Detailed Summary
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your comprehensive document text...",
    "summary_mode": "detailed"
  }'
```

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `ALLOWED_ORIGINS` | Comma-separated CORS origins | `http://localhost:5173` |
| `MIN_TEXT_LENGTH` | Minimum text length (characters) | `100` |
| `MAX_TEXT_LENGTH` | Maximum text length (characters) | `50000` |
| `DEFAULT_SUMMARY_MODE` | Default mode (`brief`, `standard`, `detailed`) | `standard` |
| `API_TITLE` | API title (optional) | `Clipnote API` |
| `API_VERSION` | API version (optional) | `2.0.0` |

**Example .env:**
```bash
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com
MIN_TEXT_LENGTH=100
MAX_TEXT_LENGTH=50000
DEFAULT_SUMMARY_MODE=standard
```

### Frontend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8000` |

**Example .env:**
```bash
VITE_API_BASE_URL=http://localhost:8000
```

## Development

### Project Structure

```
clipnote/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── schemas.py           # Pydantic models
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py        # Configuration
│   │   └── services/
│   │       ├── __init__.py
│   │       └── summarizer.py    # TextRank implementation
│   ├── tests/                   # Test suite
│   ├── requirements.txt
│   ├── pytest.ini
│   └── ruff.toml               # Linting config
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # React application
│   │   ├── App.css             # Styles
│   │   └── main.jsx            # Entry point
│   ├── package.json
│   └── vite.config.js
└── README.md
```

### Running Tests

**Backend:**
```bash
cd backend
pytest -v
```

**Linting:**
```bash
# Backend
cd backend
ruff check .
ruff format --check .

# Frontend
cd frontend
npm run lint
```

### Building for Production

**Backend:**
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with gunicorn
pip install gunicorn[uvicorn]
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`. Serve with any static file server.

## Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Python 3.11+** - Programming language
- **Pydantic** - Data validation with type annotations
- **NetworkX** - Graph analysis for PageRank
- **scikit-learn** - TF-IDF vectorization and cosine similarity
- **NumPy** - Numerical computing
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **Modern CSS** - Responsive design with CSS variables

### Development Tools
- **pytest** - Testing framework
- **ruff** - Fast Python linter and formatter
- **ESLint** - JavaScript linting
- **GitHub Actions** - CI/CD pipeline

## Deployment

### Backend Deployment

1. Set environment variables:
   ```bash
   ALLOWED_ORIGINS=https://yourdomain.com
   MIN_TEXT_LENGTH=100
   MAX_TEXT_LENGTH=50000
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt gunicorn[uvicorn]
   ```

3. Run with production server:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Frontend Deployment

1. Set environment variables:
   ```bash
   VITE_API_BASE_URL=https://api.yourdomain.com
   ```

2. Build:
   ```bash
   npm run build
   ```

3. Deploy `dist/` folder to:
   - Vercel
   - Netlify
   - GitHub Pages
   - AWS S3 + CloudFront
   - Any static hosting service

## CI/CD

The project includes GitHub Actions workflows that automatically:
- Run backend tests with pytest
- Lint backend code with ruff
- Build and lint frontend
- Run smoke tests

All tests run on every push and pull request.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and test thoroughly
4. Run linting (`ruff check .` and `npm run lint`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- TextRank algorithm based on "TextRank: Bringing Order into Texts" by Mihalcea and Tarau
- PageRank algorithm by Google
- TF-IDF implementation from scikit-learn

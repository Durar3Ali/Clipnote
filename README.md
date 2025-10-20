# Clipnote

A modern text summarization application built with FastAPI and React. Clipnote helps you quickly summarize long texts into concise, readable summaries using intelligent text processing algorithms.

## Features
- **Smart text summarization** - Extract key sentences and information from long texts
- **Customizable summary length** - Control how long your summaries should be (default: 100 characters)
- **Real-time processing** - Fast and responsive summarization with instant results
- **Modern UI** - Clean, intuitive interface built with React and Vite
- **RESTful API** - Well-documented FastAPI backend with automatic OpenAPI documentation
- **CORS enabled** - Ready for cross-origin requests between frontend and backend
- **Keyword extraction** - Identify important keywords from your text
- **Error handling** - Robust error handling for edge cases

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

5. Run the FastAPI server:
   ```bash
   python app.py
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

3. Start the development server:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

4. **Optional:** Run linting to check code quality:
   ```bash
   npm run lint
   ```

## API Endpoints

### `GET /`
Returns a welcome message and API status.

**Response:**
```json
{
  "message": "Clipnote API is running!"
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
Summarizes the provided text using intelligent sentence extraction.

**Request Body:**
```json
{
  "text": "Your text to summarize...",
  "max_length": 100
}
```

**Response:**
```json
{
  "summary": "Summarized text...",
  "original_length": 150,
  "summary_length": 85
}
```

**Error Responses:**
- `400 Bad Request`: When text is empty
- `500 Internal Server Error`: When processing fails

## Usage

1. **Start both servers** (backend and frontend) following the setup instructions above
2. **Open the application** in your browser at `http://localhost:5173`
3. **Paste or type** the text you want to summarize in the input field
4. **Adjust the maximum summary length** if needed (default is 100 characters)
5. **Click "Summarize"** to process the text
6. **View the results** including:
   - The summarized text
   - Original text length
   - Summary length
   - Compression ratio

## How It Works

The summarization algorithm:
1. **Cleans and validates** the input text
2. **Splits text into sentences** using intelligent sentence detection
3. **Extracts key sentences** that fit within the specified length limit
4. **Preserves important information** while maintaining readability
5. **Handles edge cases** like very short texts or empty inputs

## Development

### Backend Development

The backend uses FastAPI with:
- **Automatic API documentation** at `http://localhost:8000/docs`
- **Interactive API testing** at `http://localhost:8000/redoc`
- **Type validation** with Pydantic models
- **CORS middleware** for cross-origin requests
- **Error handling** with proper HTTP status codes

### Frontend Development

The frontend uses Vite with:
- **Hot Module Replacement (HMR)** for instant updates
- **ESLint** for code quality and consistency
- **Modern React** with hooks and functional components
- **Axios** for HTTP requests to the backend

### Available Scripts

**Frontend:**
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run lint     # Run ESLint
npm run preview  # Preview production build
```

### Building for Production

**Backend:**
```bash
# No build step required for Python
# Just ensure all dependencies are installed
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm run build
```

The built files will be in the `frontend/dist` directory.

## Testing

The project includes automated testing via GitHub Actions:

- **Backend smoke tests** - Validates the summarization functionality
- **Frontend build tests** - Ensures the React app builds successfully
- **CI/CD pipeline** - Automated testing on every push and pull request

## Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and test them thoroughly
4. **Run linting** (`npm run lint` in frontend directory)
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to your branch** (`git push origin feature/amazing-feature`)
7. **Submit a pull request**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.11+** - Programming language
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for running FastAPI
- **CORS Middleware** - Cross-origin resource sharing

### Frontend
- **React 18** - JavaScript library for building user interfaces
- **Vite** - Fast build tool and development server
- **Axios** - HTTP client for API requests
- **ESLint** - Code linting and quality assurance
- **CSS3** - Modern styling with responsive design

### Development Tools
- **GitHub Actions** - CI/CD pipeline
- **Hot Module Replacement** - Instant development updates
- **TypeScript support** - Enhanced development experience

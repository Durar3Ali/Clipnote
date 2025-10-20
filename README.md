# Clipnote (FastAPI and React)

A modern text summarization application built with FastAPI and React. Clipnote helps you quickly summarize long texts into concise, readable summaries.

## Features
- **AI-powered text summarization** - Intelligent text processing to extract key information
- **Customizable summary length** - Control how long your summaries should be
- **Real-time processing** - Fast and responsive summarization
- **Modern UI** - Clean, intuitive interface built with React
- **RESTful API** - Well-documented FastAPI backend
- **CORS enabled** - Ready for cross-origin requests

## Project Structure
clipnote/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── summarizer.py       # Text summarization logic
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Component styles
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Global styles
│   ├── index.html          # HTML template
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── .gitignore
├── README.md
└── LICENSE

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

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

## API Endpoints

### `GET /`
Returns a welcome message.

### `GET /health`
Health check endpoint.

### `POST /summarize`
Summarizes the provided text.

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

## Usage

1. Open the application in your browser
2. Paste or type the text you want to summarize
3. Adjust the maximum summary length if needed
4. Click "Summarize" to process the text
5. View the summary and compression statistics

## Development

### Backend Development

The backend uses FastAPI with automatic API documentation available at `http://localhost:8000/docs` when running.

### Frontend Development

The frontend uses Vite for fast development with hot module replacement.

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

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Tech
- **Backend:** FastAPI, Python, Pydantic
- **Frontend:** React, Vite, Axios
- **Styling:** CSS3 with modern features
- **Development:** ESLint, Hot Module Replacement

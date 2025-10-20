import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [text, setText] = useState('')
  const [maxLength, setMaxLength] = useState(100)
  const [summary, setSummary] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSummarize = async () => {
    if (!text.trim()) {
      setError('Please enter some text to summarize')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await axios.post(`${API_BASE_URL}/summarize`, {
        text: text,
        max_length: maxLength
      })

      setSummary(response.data.summary)
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while summarizing')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setText('')
    setSummary('')
    setError('')
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1> Clipnote</h1>
        <p>AI-powered text summarizer</p>
      </header>

      <main className="app-main">
        <div className="input-section">
          <div className="input-group">
            <label htmlFor="text-input">Enter text to summarize:</label>
            <textarea
              id="text-input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste your text here..."
              rows={8}
            />
          </div>

          <div className="input-group">
            <label htmlFor="max-length">Maximum summary length:</label>
            <input
              id="max-length"
              type="number"
              value={maxLength}
              onChange={(e) => setMaxLength(parseInt(e.target.value) || 100)}
              min="10"
              max="1000"
            />
          </div>

          <div className="button-group">
            <button 
              onClick={handleSummarize} 
              disabled={loading || !text.trim()}
              className="primary-button"
            >
              {loading ? 'Summarizing...' : 'Summarize'}
            </button>
            <button 
              onClick={handleClear}
              className="secondary-button"
            >
              Clear
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {summary && (
          <div className="output-section">
            <h3>Summary:</h3>
            <div className="summary-box">
              {summary}
            </div>
            <div className="summary-stats">
              <span>Original: {text.length} characters</span>
              <span>Summary: {summary.length} characters</span>
              <span>Compression: {Math.round((1 - summary.length / text.length) * 100)}%</span>
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Built with FastAPI and React</p>
      </footer>
    </div>
  )
}

export default App

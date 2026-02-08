import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const SUMMARY_MODES = {
  brief: {
    label: 'Brief',
    description: 'Quick highlights of key points'
  },
  standard: {
    label: 'Standard',
    description: 'Balanced comprehensive summary'
  },
  detailed: {
    label: 'Detailed',
    description: 'In-depth overview with context'
  }
}

const MIN_TEXT_LENGTH = 100
const MAX_TEXT_LENGTH = 50000

function App() {
  const [text, setText] = useState('')
  const [summaryMode, setSummaryMode] = useState('standard')
  const [preserveStructure, setPreserveStructure] = useState(false)
  const [summary, setSummary] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const charCount = text.length
  const isValidLength = charCount >= MIN_TEXT_LENGTH && charCount <= MAX_TEXT_LENGTH

  const handleSummarize = async () => {
    const trimmedText = text.trim()
    if (!trimmedText) {
      setError('Please enter some text to summarize')
      return
    }

    if (!isValidLength) {
      setError(`Text must be between ${MIN_TEXT_LENGTH} and ${MAX_TEXT_LENGTH} characters`)
      return
    }

    setLoading(true)
    setError('')
    setSummary('')

    try {
      const response = await axios.post(`${API_BASE_URL}/summarize`, {
        text: trimmedText,
        summary_mode: summaryMode,
        preserve_structure: preserveStructure
      })

      setSummary(response.data.summary)
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'An error occurred while summarizing your text'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setText('')
    setSummary('')
    setError('')
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(summary)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleSummarize()
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Clipnote</h1>
      </header>

      <main className="app-main">
        <div className="input-section">
          <div className="input-group">
            <label htmlFor="text-input">Enter your text</label>
            <textarea
              id="text-input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Paste your article, document, or any long text here... (Ctrl+Enter to summarize)"
              rows={10}
              aria-label="Text input for summarization"
            />
            <div className="char-counter">
              <span className={charCount < MIN_TEXT_LENGTH ? 'text-warning' : charCount > MAX_TEXT_LENGTH ? 'text-danger' : 'text-success'}>
                {charCount.toLocaleString()} characters
              </span>
              {charCount < MIN_TEXT_LENGTH && charCount > 0 && (
                <span className="text-hint"> (minimum {MIN_TEXT_LENGTH})</span>
              )}
              {charCount > MAX_TEXT_LENGTH && (
                <span className="text-hint"> (maximum {MAX_TEXT_LENGTH})</span>
              )}
            </div>
          </div>

          <div className="mode-selector">
            <label className="mode-label">Summarization Mode</label>
            <div className="mode-cards">
              {Object.entries(SUMMARY_MODES).map(([key, mode]) => (
                <button
                  key={key}
                  className={`mode-card ${summaryMode === key ? 'active' : ''}`}
                  onClick={() => setSummaryMode(key)}
                  aria-pressed={summaryMode === key}
                >
                  <span className="mode-label">{mode.label}</span>
                  <span className="mode-description">{mode.description}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="options-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={preserveStructure}
                onChange={(e) => setPreserveStructure(e.target.checked)}
              />
              <span>Preserve paragraph structure</span>
            </label>
          </div>

          <div className="button-group">
            <button 
              onClick={handleSummarize} 
              disabled={loading || !text.trim() || !isValidLength}
              className="primary-button"
              aria-label="Summarize text"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Summarizing...
                </>
              ) : (
                'Summarize'
              )}
            </button>
            <button 
              onClick={handleClear}
              className="secondary-button"
              aria-label="Clear all text"
            >
              Clear
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {summary && (
          <div className="output-section">
            <div className="output-header">
              <h3>Summary</h3>
              <button 
                onClick={handleCopy}
                className="copy-button"
                aria-label="Copy summary to clipboard"
                title="Copy to clipboard"
              >
                Copy
              </button>
            </div>
            <div className="summary-box">
              {summary}
            </div>
          </div>
        )}
      </main>

    </div>
  )
}

export default App

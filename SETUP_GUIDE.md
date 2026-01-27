# LLMOps Setup Guide

## 🔧 Setup Instructions (Updated)

### Prerequisites
- Python 3.9 or higher
- Git (optional)

### Installation Steps

1. **Run the installation script:**
   ```
   install_and_setup.bat
   ```
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Set up the project

2. **Activate the virtual environment:**
   ```
   venv\Scripts\activate
   ```

3. **Run the application:**
   ```
   python main.py
   ```
   OR simply run:
   ```
   run_app.bat
   ```

4. **Open your browser:**
   Navigate to: http://localhost:8000

### Testing the Setup

Run the test script to verify everything is working:
```
test_setup.bat
```

### Configuration

The project uses:
- **LLM**: ChatGroq with `openai/gpt-oss-120b` model
- **Embeddings**: HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store**: FAISS with MMR (Maximal Marginal Relevance) search

All API keys are configured in the `.env` file.

### Troubleshooting

If you encounter any errors:

1. **Import errors**: Make sure virtual environment is activated
2. **API key errors**: Check `.env` file has all required keys
3. **Model errors**: Verify Groq API key is valid
4. **Port already in use**: Change port in main.py or stop other services

### Project Structure
```
LLMOps/
├── multi_doc_chat/          # Main application package
│   ├── config/              # Configuration files
│   ├── src/                 # Source code
│   ├── utils/               # Utility modules
│   └── ...
├── static/                  # Static files (CSS)
├── templates/               # HTML templates
├── data/                    # Uploaded documents (created at runtime)
├── faiss_index/             # Vector store indexes (created at runtime)
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (API keys)
├── install_and_setup.bat    # Installation script
├── run_app.bat             # Run application script
└── test_setup.bat          # Test setup script
```

## Features

- 📄 Multi-document upload (PDF, DOCX, TXT)
- 💬 Conversational RAG with chat history
- 🔍 MMR-based retrieval for diverse results
- 🚀 FastAPI backend with async support
- 🎨 Modern web interface
- 📊 LangSmith integration for monitoring

## API Endpoints

- `GET /` – Serves the web UI
- `GET /health` – Health check endpoint
- `POST /upload` – Upload documents for indexing
- `POST /chat` – Send messages and get AI responses

## Environment Variables

Required variables in `.env`:
- `GROQ_API_KEY` – Groq API key for LLM
- `HUGGINGFACEHUB_API_TOKEN` – HuggingFace token for embeddings
- `LANGCHAIN_API_KEY` – LangSmith API key (optional, for tracing)
- `LLM_PROVIDER` – Set to "groq"
- `ENV` – Set to "local" for development

## Quick Commands

**Install dependencies:**
```bash
install_and_setup.bat
```

**Run the application:**
```bash
run_app.bat
```

**Test configuration:**
```bash
test_setup.bat
```

**Manual setup:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## What Was Fixed

✅ Updated `.env` file with proper formatting (no quotes)
✅ Changed LLM model to `openai/gpt-oss-120b` in config.yaml
✅ Switched embedding model to HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
✅ Updated `model_loader.py` to use HuggingFace embeddings
✅ Added `langchain-huggingface` and `sentence-transformers` to requirements
✅ Created installation scripts for easy setup
✅ Added run scripts for convenience
✅ Updated all configurations to work together

## Next Steps

1. Run `install_and_setup.bat` to set up your environment
2. Once installation is complete, run `run_app.bat` to start the server
3. Open http://localhost:8000 in your browser
4. Upload documents and start chatting!

## Support

If you encounter any issues:
- Check the console output for error messages
- Verify all API keys are correct in `.env`
- Make sure Python 3.9+ is installed
- Ensure virtual environment is activated before running commands

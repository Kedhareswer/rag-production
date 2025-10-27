# Config Module

This module handles configuration management for the RAG system.

## File: config.py

### Purpose
Manages all configuration settings, loads environment variables, and validates required parameters.

### Key Features
- Loads settings from `.env` file
- Validates required configuration
- Provides default values
- Creates necessary directories
- Centralized configuration management

### Class: Config

#### Configuration Parameters

**API Keys:**
```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
```
Your Groq API key (required).

**Model Configuration:**
```python
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
```

**Vector Store Configuration:**
```python
VECTOR_DB_PATH = Path(os.getenv("VECTOR_DB_PATH", "./vector_db"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "docling_rag")
```

**Chunking Configuration:**
```python
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "128"))
```

**Docling Configuration:**
```python
ARTIFACTS_PATH = Path(os.getenv("ARTIFACTS_PATH", "./docling_models"))
```

#### Methods

**validate()**
```python
Config.validate()
```
Validates required configuration and creates directories.

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (defaults shown)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=llama-3.3-70b-versatile
VECTOR_DB_PATH=./vector_db
COLLECTION_NAME=docling_rag
CHUNK_SIZE=512
CHUNK_OVERLAP=128
ARTIFACTS_PATH=./docling_models
```

### Example Usage

**Access Configuration:**
```python
from Config.config import Config

# Validate configuration
Config.validate()

# Access settings
api_key = Config.GROQ_API_KEY
model = Config.LLM_MODEL
chunk_size = Config.CHUNK_SIZE
```

**In Main System:**
```python
from Config.config import Config

class DoclingRAGSystem:
    def __init__(self):
        Config.validate()  # Validate on initialization
        
        self.config = Config
        # Use config values
        self.chunk_size = Config.CHUNK_SIZE
        self.llm_model = Config.LLM_MODEL
```

### Configuration Options

**Embedding Models:**
- `sentence-transformers/all-MiniLM-L6-v2` (default, fast)
- `sentence-transformers/all-mpnet-base-v2` (more accurate)
- `sentence-transformers/all-MiniLM-L12-v2` (balanced)

**LLM Models:**
- `llama-3.3-70b-versatile` (default, best quality)
- `llama-3.1-70b-versatile` (alternative)
- `llama-3.1-8b-instant` (faster, smaller)
- `mixtral-8x7b-32768` (long context)

**Chunk Sizes:**
- Small documents: 256-512 tokens
- Medium documents: 512-1024 tokens
- Large documents: 1024-2048 tokens

**Chunk Overlap:**
- General: 10-20% of chunk_size
- Technical docs: 20-30%
- Simple docs: 5-10%

### Validation

The `validate()` method checks:
1. **GROQ_API_KEY** is set (raises ValueError if missing)
2. **VECTOR_DB_PATH** directory exists (creates if needed)
3. **ARTIFACTS_PATH** directory exists (creates if needed)

### Directory Management

Automatically creates:
- `vector_db/` - Vector database storage
- `docling_models/` - Docling model cache

### Security

- Never commit `.env` file to version control
- `.env` is in `.gitignore` by default
- Use `.env.example` as template
- Keep API keys secure

### Troubleshooting

**Issue: "GROQ_API_KEY is required"**
```bash
# Create .env file
cp .env.example .env
# Edit and add your API key
```

**Issue: Configuration not loading**
- Check `.env` file exists in root directory
- Verify file format (KEY=value)
- No spaces around `=`

**Issue: Directory errors**
- Config automatically creates directories
- Check write permissions
- Verify paths are valid

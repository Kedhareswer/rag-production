# Docling RAG System

A production-ready RAG (Retrieval-Augmented Generation) system built with Docling, LangChain, and Groq.

## 🌟 Features

### Core Features
- **Multi-Format Support**: PDF, DOCX, XLSX, PPTX, Images (with OCR), Markdown, HTML, CSV
- **Smart Chunking**: Hierarchical chunking that preserves document structure and metadata
- **Local Embeddings**: HuggingFace sentence-transformers for local embedding generation
- **Vector Storage**: ChromaDB for efficient local vector storage
- **LLM Integration**: Groq API with Llama 3.3 70B for high-quality responses
- **Auto-Discovery**: Automatically finds and processes all files in docs/ folder

### Advanced Features
- **OCR Support**: Extract text from images and scanned documents
- **Table Extraction**: Preserve table structure from documents
- **Detailed Metrics**: Similarity scores, relevance metrics at every stage
- **Source Attribution**: Track which chunks contributed to answers
- **Web API**: FastAPI integration for web access
- **Web Interface**: Beautiful UI for easy interaction

## 🏗️ Architecture

```
Documents → Docling → Chunks → Embeddings → ChromaDB
                                                ↓
User Query → Retrieval → Context → Groq LLM → Answer
```

## 📦 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Get Groq API Key
Get your free API key from: https://console.groq.com/

## 🚀 Quick Start

### Option 1: Web Interface (Easiest!)

```bash
# Start the web server
python api.py
```

Then open your browser:
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

Upload documents and ask questions through the beautiful web interface!

### Option 2: Command Line

#### Auto-Discovery Mode
```bash
# Automatically processes all files in docs/ folder
python examples/test_rag.py
```

#### Interactive Mode
```bash
python examples/interactive.py
```

Commands:
- `ingest all` - Process all files in docs/ folder
- `ingest filename.pdf` - Process specific file
- Type your question - Get answer with sources
- `quit` - Exit

### Option 3: Python Code

```python
from main import DoclingRAGSystem

# Initialize system
rag = DoclingRAGSystem()

# Auto-ingest all documents from docs/ folder
rag.ingest_documents()

# Or specify files
rag.ingest_documents(["docs/document1.pdf", "docs/document2.pdf"])

# Query with detailed metrics
result = rag.query("What are the main topics?")
print(result["answer"])
print(f"Similarity: {result['metrics']['average_similarity']:.1%}")
```

## Project Structure

```
.
├── Chunking/                # Document chunking module
│   ├── chunking_strategy.py
│   └── README.md
├── Processing/              # Document processing module
│   ├── document_processor.py
│   └── README.md
├── Storage/                 # Vector storage module
│   ├── vector_store.py
│   └── README.md
├── Pipeline/                # RAG pipeline module
│   ├── rag_pipeline.py
│   └── README.md
├── Config/                  # Configuration module
│   ├── config.py
│   └── README.md
├── examples/                # Usage examples
│   ├── test_rag.py
│   ├── interactive.py
│   └── basic_usage.py
├── docs/                   # Your PDF documents
├── main.py                 # Main orchestrator
└── requirements.txt        # Dependencies
```

## 🎯 Usage Modes

### 1. Web Interface (Recommended)
```bash
python api.py
```
- Beautiful UI at http://localhost:8000
- Drag & drop file upload
- Real-time question answering
- Visual metrics and sources
- No coding needed!

### 2. Interactive CLI
```bash
python examples/interactive.py
```
- Command-line interface
- Auto-discovery with `ingest all`
- Ask questions naturally
- See detailed metrics

### 3. Python API
```python
from main import DoclingRAGSystem

rag = DoclingRAGSystem()
rag.ingest_documents()  # Auto-discovers all files
result = rag.query("Your question?")
```

### 4. REST API
```python
import requests

# Upload
files = {'file': open('doc.pdf', 'rb')}
requests.post('http://localhost:8000/upload', files=files)

# Query
data = {'question': 'What is this about?'}
response = requests.post('http://localhost:8000/query', json=data)
print(response.json()['answer'])
```

## 📊 Supported Formats

### Documents
- ✅ PDF (with tables and layout analysis)
- ✅ Microsoft Office (DOCX, XLSX, PPTX, PPT)
- ✅ Markdown (.md)
- ✅ HTML (.html, .htm)
- ✅ CSV files

### Images (with OCR)
- ✅ PNG, JPEG, TIFF, BMP, WEBP
- ✅ Scanned documents
- ✅ Screenshots

## 🎨 Modules

Each module has detailed documentation:

- **[Chunking](Chunking/README.md)** - Document chunking with metadata
- **[Processing](Processing/README.md)** - Multi-format document processing
- **[Storage](Storage/README.md)** - Vector storage and retrieval
- **[Pipeline](Pipeline/README.md)** - RAG pipeline with Groq
- **[Config](Config/README.md)** - Configuration management

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# Required
GROQ_API_KEY=your_key_here

# Models (optional, defaults shown)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=llama-3.3-70b-versatile

# Storage
VECTOR_DB_PATH=./vector_db
COLLECTION_NAME=docling_rag

# Chunking
CHUNK_SIZE=512
CHUNK_OVERLAP=128
```

## 📈 Performance Metrics

The system provides detailed metrics at every stage:

### Document Processing
- File format and size
- Text elements extracted
- Tables and images found
- Sample text preview

### Chunking
- Total chunks created
- Average chunk size
- Chunk previews with headings

### Retrieval
- Similarity scores per chunk (0-100%)
- Average similarity across chunks
- Chunk previews

### Generation
- Model used
- Answer length
- Processing time

## 🌐 Web API Features

### Endpoints
- `POST /upload` - Upload and process documents
- `POST /query` - Ask questions
- `GET /status` - System status
- `GET /documents` - List documents
- `GET /health` - Health check

### Interactive Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Try all endpoints in browser
- See request/response examples

## 💡 Usage Examples

### Web Interface
```bash
python api.py
# Open http://localhost:8000
# Upload files, ask questions!
```

### Auto-Discovery
```python
from main import DoclingRAGSystem

rag = DoclingRAGSystem()
rag.ingest_documents()  # Finds all files in docs/
result = rag.query("What are the main topics?")
```

### With Detailed Metrics
```python
result = rag.query("Your question?")
print(f"Answer: {result['answer']}")
print(f"Similarity: {result['metrics']['average_similarity']:.1%}")

for source in result['sources'][:3]:  # Top 3 sources
    print(f"\nSource {source['source_number']}:")
    print(f"  Similarity: {source['relevance_score']:.1%}")
    print(f"  Text: {source['text']}")
```

### REST API
```python
import requests

# Upload
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    requests.post('http://localhost:8000/upload', files=files)

# Query
data = {'question': 'Summarize this', 'top_k': 10}
response = requests.post('http://localhost:8000/query', json=data)
result = response.json()
print(result['answer'])
```

## 🤖 Groq Models

Available models (configure in `.env`):
- `llama-3.3-70b-versatile` (default, best quality)
- `llama-3.1-70b-versatile` (alternative)
- `llama-3.1-8b-instant` (faster, smaller)
- `mixtral-8x7b-32768` (long context, 32K tokens)

## 🔧 Troubleshooting

### "GROQ_API_KEY is required"
```bash
cp .env.example .env
# Edit .env and add your key from https://console.groq.com/
```

### "No documents found"
```bash
# Add files to docs/ folder
cp your_files/* docs/
```

### Slow first run
- Normal! Downloads models (~500MB one-time)
- Subsequent runs are fast
- Models cached locally

### Low similarity scores
- Try rephrasing your question
- Check if documents contain the answer
- Increase retrieval count (k parameter)

### Web server won't start
```bash
# Install FastAPI dependencies
pip install fastapi uvicorn python-multipart
```

## ⚡ Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Document Processing | 2-5 sec/page | Depends on complexity |
| Embedding Generation | 0.1 sec/chunk | Local, no API calls |
| Query Response | 1-2 seconds | Groq is fast! |
| First Run | 2-5 minutes | Downloads models (one-time) |

### Optimization Tips
- Use auto-discovery for batch processing
- Adjust chunk size for your documents
- Increase retrieval count for better context
- Use web interface for easy access

## 📚 Documentation

### Quick Start
- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[README_FASTAPI.md](README_FASTAPI.md)** - Web API quick start

### Features & Guides
- **[FEATURES.md](FEATURES.md)** - Complete feature list
- **[FASTAPI_EXPLAINED.md](FASTAPI_EXPLAINED.md)** - FastAPI for beginners
- **[API_USAGE_EXAMPLES.md](API_USAGE_EXAMPLES.md)** - API code examples
- **[RETRIEVAL_IMPROVEMENTS.md](RETRIEVAL_IMPROVEMENTS.md)** - How retrieval works

### Module Documentation
- **[Chunking/README.md](Chunking/README.md)** - Chunking strategies
- **[Processing/README.md](Processing/README.md)** - Document processing
- **[Storage/README.md](Storage/README.md)** - Vector storage
- **[Pipeline/README.md](Pipeline/README.md)** - RAG pipeline
- **[Config/README.md](Config/README.md)** - Configuration

### Project Info
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project organization
- **[FIXES_APPLIED.md](FIXES_APPLIED.md)** - Recent improvements

## 🎓 Examples

### Command Line
```bash
python examples/test_rag.py        # Quick test
python examples/interactive.py     # Interactive mode
python examples/basic_usage.py     # Basic workflow
```

### Web Interface
```bash
python api.py                      # Start web server
# Open http://localhost:8000
```

### Python Code
See examples in `examples/` folder and documentation files.

## 🎯 Key Features Summary

✅ **Multi-format support** - PDF, Office, images, and more
✅ **OCR enabled** - Extract text from images
✅ **Auto-discovery** - Finds all files automatically
✅ **Web interface** - Beautiful UI for easy use
✅ **REST API** - Integrate with any application
✅ **Detailed metrics** - Similarity scores at every stage
✅ **Source attribution** - Know where answers come from
✅ **Local embeddings** - No external API for embeddings
✅ **Production-ready** - Comprehensive error handling

## 🚀 Get Started Now

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Add your GROQ_API_KEY

# 3. Run
python api.py

# 4. Open browser
# http://localhost:8000
```

## 📄 License

MIT License

## 🙏 Credits

Built with:
- [Docling](https://github.com/docling-project/docling) - Document processing
- [LangChain](https://github.com/langchain-ai/langchain) - RAG orchestration
- [Groq](https://groq.com/) - LLM inference (Llama 3.3 70B)
- [ChromaDB](https://www.trychroma.com/) - Vector storage
- [HuggingFace](https://huggingface.co/) - Embeddings
- [FastAPI](https://fastapi.tiangolo.com/) - Web API framework

---

**Made with ❤️ for easy document Q&A**

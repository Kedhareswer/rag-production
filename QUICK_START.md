# 🚀 Quick Start Guide

## Get Started in 3 Steps!

### Step 1: Install

```bash
pip install -r requirements.txt
```

### Step 2: Configure

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY from https://console.groq.com/
```

### Step 3: Run!

**Option A: Web Interface (Easiest!)**

```bash
python api.py
```

Then open: http://localhost:8000

**Option B: Command Line**

```bash
python examples/test_rag.py
```

**Option C: Interactive Mode**

```bash
python examples/interactive.py
```

## 🌐 Web Interface (Recommended!)

### Start the Server

```bash
python api.py
```

You'll see:

```
🚀 Starting Docling RAG API Server
📚 API Documentation: http://localhost:8000/docs
🔗 API Endpoints ready
```

### Access the System

- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Use the Web Interface

1. **Upload Documents**

   - Click or drag files to upload area
   - Supports: PDF, DOCX, XLSX, PPTX, images, Markdown, HTML, CSV
   - See processing status in real-time

2. **Ask Questions**

   - Type your question in the text box
   - Press Enter or click "Ask"
   - See answer with similarity scores
   - View sources with relevance metrics

3. **Check Status**
   - See document count
   - View system status
   - Check model information

## 💻 Command Line Usage

### Quick Test

```bash
python examples/test_rag.py
```

- Auto-discovers all files in `docs/` folder
- Processes and ingests them
- Runs test queries
- Shows detailed metrics

### Interactive Mode

```bash
python examples/interactive.py
```

Commands:

- `ingest all` - Process all files in docs/ folder
- `ingest filename.pdf` - Process specific file
- Type your question - Get answer
- `help` - Show help
- `quit` - Exit

### Basic Usage

```bash
python examples/basic_usage.py
```

- Demonstrates complete workflow
- Shows API usage
- Educational example

## 🐍 Python API

### Quick Example

```python
from main import DoclingRAGSystem

# Initialize
rag = DoclingRAGSystem()

# Auto-ingest all documents from docs/ folder
rag.ingest_documents()

# Query
result = rag.query("What are the main topics?")
print(result["answer"])
```

### With Metrics

```python
result = rag.query("Your question?")

print(f"Answer: {result['answer']}")
print(f"Similarity: {result['metrics']['average_similarity']:.1%}")
print(f"Sources: {len(result['sources'])}")

for source in result['sources'][:3]:
    print(f"\nSource {source['source_number']}:")
    print(f"  Similarity: {source['relevance_score']:.1%}")
    print(f"  Text: {source['text'][:100]}...")
```

### Specific Files

```python
# Process specific files
rag.ingest_documents([
    "docs/document1.pdf",
    "docs/document2.docx",
    "docs/image.png"
])
```

## 🌐 REST API

### Upload Document

```python
import requests

with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload', files=files)
    print(response.json())
```

### Ask Question

```python
import requests

data = {
    'question': 'What is this about?',
    'top_k': 10
}
response = requests.post('http://localhost:8000/query', json=data)
result = response.json()

print(f"Answer: {result['answer']}")
print(f"Similarity: {result['metrics']['average_similarity']:.1%}")
```

### Check Status

```python
import requests

response = requests.get('http://localhost:8000/status')
status = response.json()

print(f"Status: {status['status']}")
print(f"Documents: {status['documents_count']}")
```

## 📁 Supported Formats

### Documents

- ✅ PDF (with tables and layout)
- ✅ DOCX, XLSX, PPTX, PPT
- ✅ Markdown (.md)
- ✅ HTML (.html, .htm)
- ✅ CSV files

### Images (with OCR)

- ✅ PNG, JPEG, TIFF, BMP, WEBP
- ✅ Scanned documents
- ✅ Screenshots

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Required
GROQ_API_KEY=your_key_here

# Optional (defaults shown)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=llama-3.3-70b-versatile
CHUNK_SIZE=512
CHUNK_OVERLAP=128
```

### Available Models

- `llama-3.3-70b-versatile` (default, best)
- `llama-3.1-70b-versatile` (alternative)
- `llama-3.1-8b-instant` (faster)
- `mixtral-8x7b-32768` (long context)

## 🔧 Troubleshooting

### "GROQ_API_KEY is required"

```bash
cp .env.example .env
# Edit .env and add your key
```

### "No documents found"

```bash
# Add files to docs/ folder
mkdir docs
cp your_files/* docs/
```

### Slow first run

- Normal! Downloads models (~500MB)
- Subsequent runs are fast
- Models cached locally

### Web server won't start

```bash
pip install fastapi uvicorn python-multipart
```

## 📊 What to Expect

### Document Processing

```
📄 Processing: document.pdf
   Format: .pdf
   Size: 245.67 KB

📊 Extraction Results:
   ✓ Text elements: 45
   ✓ Tables: 3
   ✓ Pictures: 2
   ✓ Pages: 10
```

### Chunking

```
✂️  Chunking Document

📦 Chunk 1:
   Length: 512 characters
   Headings: ['Introduction']
   Preview: This document describes...

📊 Chunking Statistics:
   Total chunks: 30
   Average chunk size: 487 characters
```

### Query Results

```
🔍 Retrieval Phase
   Retrieved chunks: 10
   Chunk 1: Similarity: 87.5%
   Average similarity: 75.2%

🤖 Generation Phase
   Model: llama-3.3-70b-versatile
   ✓ Answer generated (234 chars)

💬 Answer:
   Based on the invoice, the total amount is...

📊 Performance Metrics:
   • Retrieved chunks: 10
   • Average similarity: 75.20%
   • Answer length: 234 chars
```

## 🎯 Next Steps

### 1. Try the Web Interface

```bash
python api.py
# Open http://localhost:8000
```

### 2. Upload Your Documents

- Drag & drop files
- Or use API to upload
- Supports all formats

### 3. Ask Questions

- Type naturally
- See detailed metrics
- Check similarity scores

### 4. Integrate

- Use REST API
- Build web apps
- Create chatbots

## 📚 Learn More

- **[README.md](README.md)** - Full documentation
- **[FEATURES.md](FEATURES.md)** - Complete feature list
- **[README_FASTAPI.md](README_FASTAPI.md)** - Web API guide
- **[API_USAGE_EXAMPLES.md](API_USAGE_EXAMPLES.md)** - Code examples
- **Module READMEs** - Detailed module docs

## 🎉 You're Ready!

Your RAG system is now:

- ✅ Installed and configured
- ✅ Ready to process documents
- ✅ Ready to answer questions
- ✅ Accessible via web interface
- ✅ Accessible via REST API

**Start now:**

```bash
python api.py
```

**Then open:** http://localhost:8000

**Happy querying! 🚀**

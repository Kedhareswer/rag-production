# Storage Module

This module manages vector embeddings and similarity search using ChromaDB.

## File: vector_store.py

### Purpose
Manages vector storage and retrieval for the RAG system using ChromaDB and HuggingFace embeddings.

### Key Features
- Local vector storage (ChromaDB)
- HuggingFace embeddings (no external API)
- Persistent storage (survives restarts)
- Fast similarity search
- Metadata filtering

### Class: VectorStore

#### Initialization
```python
from Storage.vector_store import VectorStore
from pathlib import Path

vector_store = VectorStore(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    persist_directory=Path("./vector_db"),
    collection_name="my_documents"
)
```

#### Parameters
- **embedding_model** (str): HuggingFace model for embeddings
- **persist_directory** (Path): Local directory for database
- **collection_name** (str): Name for the collection

#### Methods

**create_vectorstore(chunks)**
```python
vectorstore = vector_store.create_vectorstore(chunks)
```
Create a new vector store from chunks.

**load_vectorstore()**
```python
vectorstore = vector_store.load_vectorstore()
```
Load an existing vector store from disk.

**add_documents(chunks)**
```python
vector_store.add_documents(new_chunks)
```
Add new documents to existing store.

**similarity_search(query, k=4)**
```python
results = vector_store.similarity_search("What is Docling?", k=4)
```
Search for similar documents.

**as_retriever(k=4)**
```python
retriever = vector_store.as_retriever(k=4)
```
Get a retriever interface for LangChain.

### Embedding Models

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| all-MiniLM-L6-v2 | 80MB | Fast | Good | General (default) |
| all-mpnet-base-v2 | 420MB | Medium | Better | Higher quality |
| all-MiniLM-L12-v2 | 120MB | Medium | Good | Balance |

### Storage Structure

```
./vector_db/
├── chroma.sqlite3          # Database file
└── [collection_id]/        # Collection data
    ├── data_level0.bin
    └── ...
```

### Example Usage

**Basic Workflow:**
```python
from Storage.vector_store import VectorStore
from pathlib import Path

# Initialize
vector_store = VectorStore(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    persist_directory=Path("./vector_db")
)

# Create with initial documents
chunks = [
    {"text": "Docling is a document processing library", "metadata": {}},
    {"text": "It supports PDF, DOCX, and more", "metadata": {}}
]
vector_store.create_vectorstore(chunks)

# Search
results = vector_store.similarity_search("document processing", k=2)
print(results[0].page_content)
```

**Incremental Updates:**
```python
# Load existing store
vector_store.load_vectorstore()

# Add more documents
new_chunks = [{"text": "New information...", "metadata": {}}]
vector_store.add_documents(new_chunks)

# Search includes new documents
results = vector_store.similarity_search("new information")
```

### Performance

- **Embedding Generation**: ~100-200 chunks/second (CPU)
- **First Run**: Downloads model (~80MB for default)
- **Search Time**: ~10-50ms for 1000 documents
- **Memory**: ~1MB per 1000 documents

### Troubleshooting

**Issue: Slow embedding generation**
- Use smaller embedding model
- Process in batches

**Issue: High memory usage**
- Use smaller embedding model
- Reduce batch size

**Issue: Search returns irrelevant results**
- Try different embedding model
- Adjust chunk size
- Increase k parameter

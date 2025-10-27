# Chunking Module

This module handles document chunking using Docling's HierarchicalChunker.

## File: chunking_strategy.py

### Purpose
Splits documents into smaller, manageable chunks while preserving document structure and metadata.

### Key Features
- Uses HierarchicalChunker from docling-core
- Preserves document hierarchy (headings, sections)
- Maintains metadata (page numbers, document origin)
- Token-based splitting for accurate sizing

### Class: ChunkingStrategy

#### Initialization
```python
from Chunking.chunking_strategy import ChunkingStrategy

chunker = ChunkingStrategy(
    chunk_size=512,      # Maximum tokens per chunk
    chunk_overlap=128    # Overlapping tokens between chunks
)
```

#### Parameters
- **chunk_size** (int): Maximum tokens per chunk. Default: 512
- **chunk_overlap** (int): Overlapping tokens. Default: 128

#### Methods

**chunk_document(document)**
```python
chunks = chunker.chunk_document(document)
```
Chunks a single DoclingDocument.

**chunk_documents(documents)**
```python
chunks = chunker.chunk_documents([doc1, doc2, doc3])
```
Chunks multiple documents at once.

### Output Format

Each chunk is a dictionary:
```python
{
    "text": "Chunk content...",
    "metadata": {
        "doc_items": [...],      # Document structure items
        "headings": ["Section", "Subsection"],
        "origin": {
            "filename": "document.pdf",
            "mimetype": "application/pdf"
        }
    }
}
```

### Configuration

Adjust chunk size and overlap in `.env`:
```env
CHUNK_SIZE=512
CHUNK_OVERLAP=128
```

### Best Practices

**Chunk Size Selection:**
- Small documents (< 10 pages): 256-512 tokens
- Medium documents (10-50 pages): 512-1024 tokens
- Large documents (> 50 pages): 1024-2048 tokens

**Overlap Configuration:**
- General use: 10-20% of chunk_size
- Technical documents: 20-30% (more context needed)
- Simple documents: 5-10% (less overlap needed)

### Example Usage

```python
from Chunking.chunking_strategy import ChunkingStrategy
from Processing.document_processor import DocumentProcessor

# Initialize
processor = DocumentProcessor()
chunker = ChunkingStrategy(chunk_size=512, chunk_overlap=128)

# Process and chunk
document = processor.process_document("document.pdf")
chunks = chunker.chunk_document(document)

# Access chunk data
for chunk in chunks:
    print(f"Text: {chunk['text'][:100]}...")
    print(f"Headings: {chunk['metadata']['headings']}")
```

### How It Works

1. **Document Analysis**: Analyzes document structure
2. **Hierarchical Splitting**: Respects sections and headings
3. **Token Counting**: Uses tokenizer for accurate sizing
4. **Metadata Preservation**: Maintains all document metadata
5. **Overlap Creation**: Creates overlapping regions for context

### Troubleshooting

**Issue: Chunks too large**
- Reduce `chunk_size` parameter

**Issue: Lost context between chunks**
- Increase `chunk_overlap` parameter

**Issue: Too many chunks**
- Increase `chunk_size` or reduce `chunk_overlap`

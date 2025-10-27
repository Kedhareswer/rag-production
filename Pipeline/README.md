# Pipeline Module

This module implements the RAG pipeline using LangChain and Groq.

## File: rag_pipeline.py

### Purpose
Implements the Retrieval-Augmented Generation (RAG) pipeline that combines document retrieval with LLM generation.

### Key Features
- Retrieval from vector store
- Context augmentation
- Groq LLM integration (Llama 3.3 70B)
- Source attribution
- Customizable prompts

### Class: RAGPipeline

#### Initialization
```python
from Pipeline.rag_pipeline import RAGPipeline
from Storage.vector_store import VectorStore

vector_store = VectorStore(...)
rag_pipeline = RAGPipeline(
    groq_api_key="your_groq_api_key",
    vector_store=vector_store,
    model_name="llama-3.3-70b-versatile",
    temperature=0.1
)
```

#### Parameters
- **groq_api_key** (str): Your Groq API key
- **vector_store** (VectorStore): Initialized vector store
- **model_name** (str): Groq model name
- **temperature** (float): LLM temperature (0.0-1.0)

#### Methods

**query(question)**
```python
result = rag_pipeline.query("What is Docling?")
```
Full query with sources and metadata.

Returns:
```python
{
    "question": "What is Docling?",
    "answer": "Docling is...",
    "sources": [
        {
            "source_number": 1,
            "text": "Chunk content...",
            "metadata": {...}
        }
    ]
}
```

**query_simple(question)**
```python
answer = rag_pipeline.query_simple("What is Docling?")
```
Quick query returning only the answer string.

### Available Groq Models

| Model | Parameters | Speed | Quality | Use Case |
|-------|------------|-------|---------|----------|
| llama-3.3-70b-versatile | 70B | Fast | Excellent | Best (default) |
| llama-3.1-70b-versatile | 70B | Fast | Excellent | Alternative |
| llama-3.1-8b-instant | 8B | Very Fast | Good | Quick responses |
| mixtral-8x7b-32768 | 8x7B | Fast | Very Good | Long context |

### Prompt Template

Default prompt:
```
You are an AI assistant helping users understand Docling documentation.
Use the following context to answer the question. If you don't know the answer based on the context, say so.

Context:
{context}

Question: {question}

Answer: Let me help you with that based on the Docling documentation.
```

### Example Usage

**Basic Query:**
```python
from Pipeline.rag_pipeline import RAGPipeline
from Storage.vector_store import VectorStore

# Setup
vector_store = VectorStore(...)
vector_store.load_vectorstore()

rag = RAGPipeline(
    groq_api_key="gsk_...",
    vector_store=vector_store
)

# Query
result = rag.query("How do I convert a PDF?")
print(result["answer"])
```

**With Source Attribution:**
```python
result = rag.query("What AI models does Docling use?")

print(f"Answer: {result['answer']}\n")
print(f"Based on {len(result['sources'])} sources:")

for source in result['sources']:
    print(f"\nSource {source['source_number']}:")
    print(f"  {source['text']}")
```

**Multiple Queries:**
```python
questions = [
    "What is Docling?",
    "How do I install it?",
    "What formats are supported?"
]

for q in questions:
    answer = rag.query_simple(q)
    print(f"Q: {q}")
    print(f"A: {answer}\n")
```

### Configuration

**Retrieval Count:**
The pipeline retrieves top 4 chunks by default. Adjust in code:
```python
self.retriever = vector_store.as_retriever(k=8)  # Retrieve 8 chunks
```

**Temperature Settings:**
```python
temperature=0.0   # Factual, deterministic (recommended for RAG)
temperature=0.1   # Slightly varied (default)
temperature=0.5   # More creative
temperature=1.0   # Very creative (not recommended for RAG)
```

### Performance

- **Query Time**: ~1-2 seconds (includes retrieval + LLM)
- **Retrieval**: ~10-50ms
- **LLM Generation**: ~1-2 seconds (Groq is fast!)
- **Cost**: Groq offers generous free tier

### Troubleshooting

**Issue: "Invalid API key"**
- Check your Groq API key in .env file

**Issue: Rate limit errors**
- Wait and retry
- Upgrade Groq plan

**Issue: Poor answer quality**
- Increase retrieval count (k parameter)
- Improve document chunking
- Try different model

**Issue: Slow responses**
- Use faster model (llama-3.1-8b-instant)
- Reduce retrieval count
- Check network connection

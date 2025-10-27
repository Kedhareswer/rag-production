"""Chunking strategy for documents using Docling's HierarchicalChunker."""
from typing import List, Dict, Any
from docling_core.types.doc import DoclingDocument
from docling_core.transforms.chunker import HierarchicalChunker


class ChunkingStrategy:
    """Handle document chunking with metadata preservation."""

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 128):
        """Initialize chunking strategy.

        Args:
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Number of overlapping tokens between chunks
        """
        self.chunker = HierarchicalChunker(
            tokenizer="sentence-transformers/all-MiniLM-L6-v2",
            max_tokens=chunk_size,
            include_metadata=True,
        )

    def chunk_document(self, document: DoclingDocument) -> List[Dict[str, Any]]:
        """Chunk a single document with metadata.

        Args:
            document: DoclingDocument to chunk

        Returns:
            List of chunks with metadata
        """
        chunks = []
        
        print(f"\n{'='*70}")
        print(f"✂️  Chunking Document")
        print(f"{'='*70}")

        for i, chunk in enumerate(self.chunker.chunk(document), 1):
            chunk_data = {
                "text": chunk.text,
                "metadata": {
                    "doc_items": (
                        chunk.meta.doc_items if hasattr(chunk.meta, "doc_items") else []
                    ),
                    "headings": (
                        chunk.meta.headings if hasattr(chunk.meta, "headings") else []
                    ),
                    "origin": (
                        chunk.meta.origin.model_dump()
                        if hasattr(chunk.meta, "origin")
                        else {}
                    ),
                },
            }
            chunks.append(chunk_data)
            
            # Show chunk details
            if i <= 3:  # Show first 3 chunks
                print(f"\n📦 Chunk {i}:")
                print(f"   Length: {len(chunk.text)} characters")
                print(f"   Headings: {chunk_data['metadata']['headings']}")
                print(f"   Preview: {chunk.text[:150]}...")
        
        if len(chunks) > 3:
            print(f"\n   ... and {len(chunks) - 3} more chunks")
        
        print(f"\n📊 Chunking Statistics:")
        print(f"   Total chunks: {len(chunks)}")
        avg_length = sum(len(c['text']) for c in chunks) / len(chunks) if chunks else 0
        print(f"   Average chunk size: {avg_length:.0f} characters")
        print(f"{'='*70}\n")

        return chunks

    def chunk_documents(
        self, documents: List[DoclingDocument]
    ) -> List[Dict[str, Any]]:
        """Chunk multiple documents.

        Args:
            documents: List of DoclingDocument objects

        Returns:
            List of all chunks with metadata
        """
        all_chunks = []

        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)

        return all_chunks

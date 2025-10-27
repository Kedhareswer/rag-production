"""Vector store management using ChromaDB."""
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.documents import Document


class VectorStore:
    """Manage vector storage and retrieval."""

    def __init__(
        self,
        embedding_model: str,
        persist_directory: Path,
        collection_name: str = "docling_rag",
    ):
        """Initialize vector store.

        Args:
            embedding_model: HuggingFace model name for embeddings
            persist_directory: Directory to persist vector database
            collection_name: Name of the collection
        """
        self.embedding_model = embedding_model
        self.persist_directory = str(persist_directory)
        self.collection_name = collection_name

        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        # Initialize ChromaDB
        self.vectorstore = None

    def create_vectorstore(self, chunks: List[Dict[str, Any]]) -> Chroma:
        """Create vector store from chunks.

        Args:
            chunks: List of chunks with text and metadata

        Returns:
            Chroma vectorstore instance
        """
        print(f"\n{'='*70}")
        print(f"🔢 Creating Vector Embeddings")
        print(f"{'='*70}")
        
        # Convert chunks to LangChain documents
        documents = []
        for chunk in chunks:
            doc = Document(page_content=chunk["text"], metadata=chunk["metadata"])
            documents.append(doc)

        # Filter complex metadata that ChromaDB can't handle
        documents = filter_complex_metadata(documents)
        
        print(f"   Generating embeddings for {len(documents)} chunks...")
        print(f"   Model: {self.embedding_model}")

        # Create vectorstore
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
        )
        
        print(f"   ✓ Embeddings created and stored")
        print(f"   ✓ Vector database: {self.persist_directory}")
        print(f"{'='*70}\n")

        return self.vectorstore

    def load_vectorstore(self) -> Chroma:
        """Load existing vector store.

        Returns:
            Chroma vectorstore instance
        """
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
        )

        return self.vectorstore

    def add_documents(self, chunks: List[Dict[str, Any]]):
        """Add new documents to existing vectorstore.

        Args:
            chunks: List of chunks with text and metadata
        """
        if not self.vectorstore:
            self.load_vectorstore()

        documents = []
        for chunk in chunks:
            doc = Document(page_content=chunk["text"], metadata=chunk["metadata"])
            documents.append(doc)

        # Filter complex metadata that ChromaDB can't handle
        documents = filter_complex_metadata(documents)

        self.vectorstore.add_documents(documents)

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of similar documents
        """
        if not self.vectorstore:
            self.load_vectorstore()

        return self.vectorstore.similarity_search(query, k=k)

    def as_retriever(self, k: int = 4):
        """Get retriever interface.

        Args:
            k: Number of documents to retrieve

        Returns:
            Retriever instance
        """
        if not self.vectorstore:
            self.load_vectorstore()

        return self.vectorstore.as_retriever(search_kwargs={"k": k})

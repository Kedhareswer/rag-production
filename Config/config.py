"""Configuration management for RAG system."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for RAG system."""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Model Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    
    # Vector Store Configuration
    VECTOR_DB_PATH = Path(os.getenv("VECTOR_DB_PATH", "./vector_db"))
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "docling_rag")
    
    # Chunking Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "128"))
    
    # Docling Configuration
    ARTIFACTS_PATH = Path(os.getenv("ARTIFACTS_PATH", "./docling_models"))
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required. Please set it in .env file")
        
        # Create directories if they don't exist
        cls.VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
        cls.ARTIFACTS_PATH.mkdir(parents=True, exist_ok=True)

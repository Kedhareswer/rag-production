"""Main RAG system orchestrator."""
from pathlib import Path
from typing import List, Union
from Config.config import Config
from Processing.document_processor import DocumentProcessor
from Chunking.chunking_strategy import ChunkingStrategy
from Storage.vector_store import VectorStore
from Pipeline.rag_pipeline import RAGPipeline


class DoclingRAGSystem:
    """Complete RAG system using Docling."""

    def __init__(self):
        """Initialize RAG system with configuration."""
        Config.validate()

        self.config = Config
        self.document_processor = DocumentProcessor(
            artifacts_path=Config.ARTIFACTS_PATH
        )
        self.chunking_strategy = ChunkingStrategy(
            chunk_size=Config.CHUNK_SIZE, chunk_overlap=Config.CHUNK_OVERLAP
        )
        self.vector_store = VectorStore(
            embedding_model=Config.EMBEDDING_MODEL,
            persist_directory=Config.VECTOR_DB_PATH,
            collection_name=Config.COLLECTION_NAME,
        )
        self.rag_pipeline = None

    def ingest_documents(self, file_paths: List[Union[str, Path]] = None):
        """Ingest documents into the RAG system.

        Args:
            file_paths: List of document file paths. If None, auto-discovers all files in docs/ folder
        """
        # Auto-discover files if not provided
        if file_paths is None:
            docs_folder = Path("docs")
            if not docs_folder.exists():
                print(f"❌ 'docs' folder not found. Please create it and add documents.")
                return
            
            # Supported extensions
            supported_extensions = [
                '.pdf', '.docx', '.xlsx', '.pptx', '.ppt',
                '.md', '.html', '.htm', '.csv',
                '.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.webp'
            ]
            
            file_paths = []
            for ext in supported_extensions:
                file_paths.extend(docs_folder.glob(f"*{ext}"))
            
            if not file_paths:
                print(f"❌ No supported documents found in 'docs' folder")
                print(f"   Supported formats: {', '.join(supported_extensions)}")
                return
            
            print(f"\n{'='*70}")
            print(f"📁 Auto-discovered {len(file_paths)} document(s) in 'docs' folder")
            print(f"{'='*70}")
            for fp in file_paths:
                print(f"   • {fp.name}")
            print(f"{'='*70}\n")
        
        print(f"\n{'='*70}")
        print(f"🚀 Starting Document Ingestion Pipeline")
        print(f"{'='*70}\n")

        # Process documents with Docling
        documents = self.document_processor.process_documents(file_paths)
        
        print(f"\n{'='*70}")
        print(f"📊 Processing Summary")
        print(f"{'='*70}")
        print(f"   ✓ Processed {len(documents)} document(s)")
        print(f"{'='*70}\n")

        # Chunk documents
        chunks = self.chunking_strategy.chunk_documents(documents)
        
        print(f"\n{'='*70}")
        print(f"📊 Chunking Summary")
        print(f"{'='*70}")
        print(f"   ✓ Created {len(chunks)} total chunks")
        print(f"{'='*70}\n")

        # Create or update vector store
        try:
            self.vector_store.load_vectorstore()
            self.vector_store.add_documents(chunks)
            print(f"✓ Added chunks to existing vector store\n")
        except:
            self.vector_store.create_vectorstore(chunks)
            print(f"✓ Created new vector store with chunks\n")

    def initialize_rag(self):
        """Initialize RAG pipeline."""
        if not self.rag_pipeline:
            self.rag_pipeline = RAGPipeline(
                groq_api_key=self.config.GROQ_API_KEY,
                vector_store=self.vector_store,
                model_name=self.config.LLM_MODEL,
            )
            print(f"✓ RAG pipeline initialized with {self.config.LLM_MODEL}")

    def query(self, question: str, verbose: bool = True):
        """Query the RAG system.

        Args:
            question: User question
            verbose: Whether to print detailed output

        Returns:
            Query result
        """
        if not self.rag_pipeline:
            self.initialize_rag()

        result = self.rag_pipeline.query(question)

        if verbose:
            print(f"\n{'='*70}")
            print(f"💬 Query Results")
            print(f"{'='*70}")
            print(f"\n❓ Question: {result['question']}")
            print(f"\n✅ Answer:\n{result['answer']}")
            
            if 'metrics' in result:
                print(f"\n📊 Performance Metrics:")
                print(f"   • Retrieved chunks: {result['metrics']['retrieved_chunks']}")
                print(f"   • Average similarity: {result['metrics']['average_relevance']:.2%}")
                print(f"   • Answer length: {result['metrics']['answer_length']} chars")
            
            print(f"\n📚 Top Sources (showing top 5 of {len(result['sources'])}):")
            for source in result["sources"][:5]:  # Show top 5 most relevant
                print(f"\n  📄 Source {source['source_number']}:")
                if 'relevance_score' in source:
                    print(f"     Similarity: {source['relevance_score']:.2%}")
                print(f"     Text: {source['text']}")
                if source["metadata"].get("headings"):
                    print(f"     Headings: {source['metadata']['headings']}")
            
            print(f"\n{'='*70}\n")

        return result


def main():
    """Example usage of the RAG system."""
    # Initialize system
    rag_system = DoclingRAGSystem()

    # Example: Ingest documents
    # Uncomment and provide your document paths
    # documents = ["docs/document1.pdf", "docs/document2.pdf"]
    # rag_system.ingest_documents(documents)

    # Example: Query the system
    # rag_system.query("What are the main AI models in Docling?")

    print("RAG System initialized successfully!")
    print("\nUsage:")
    print("1. Ingest documents: rag_system.ingest_documents(['docs/file1.pdf'])")
    print("2. Query: rag_system.query('Your question here')")


if __name__ == "__main__":
    main()

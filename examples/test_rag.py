"""Quick test script for the RAG system."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import DoclingRAGSystem


def test_rag_system():
    """Test the RAG system with documents from docs folder."""

    print("\n" + "=" * 70)
    print("🚀 DOCLING RAG SYSTEM - Comprehensive Test")
    print("=" * 70)

    # Initialize system
    print("\n1️⃣  Initializing RAG system...")
    try:
        rag = DoclingRAGSystem()
        print("   ✓ System initialized successfully")
    except ValueError as e:
        print(f"   ✗ Error: {e}")
        print("\n   Please set GROQ_API_KEY in .env file")
        print("   1. Copy .env.example to .env")
        print("   2. Add your Groq API key from https://console.groq.com/")
        return

    # Auto-discover and ingest all documents
    print("\n2️⃣  Auto-discovering documents...")
    try:
        rag.ingest_documents()  # Auto-discovers all files in docs/
        print("   ✓ Documents ingested successfully")
    except Exception as e:
        print(f"   ✗ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test queries with detailed output
    print("\n3️⃣  Testing queries with detailed metrics...")

    test_questions = [
        "What is this document about?",
        "Summarize the main points",
        "What are the key topics discussed?",
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}/{len(test_questions)}")
        print(f"{'='*70}")
        try:
            result = rag.query(question, verbose=True)
        except Exception as e:
            print(f"   ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            break

    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE!")
    print("=" * 70)
    print("\n📊 System Capabilities Demonstrated:")
    print("   ✓ Multi-format document processing (PDF, DOCX, XLSX, PPTX, images)")
    print("   ✓ OCR for images and scanned documents")
    print("   ✓ Table extraction and structure preservation")
    print("   ✓ Hierarchical chunking with metadata")
    print("   ✓ Vector embeddings and similarity search")
    print("   ✓ RAG with source attribution")
    print("   ✓ Performance metrics at each stage")
    print("\n🎯 Next steps:")
    print("   1. Try interactive mode: python examples/interactive.py")
    print("   2. Add more documents to 'docs' folder (any supported format)")
    print("   3. Customize settings in .env file")
    print("\n📚 For detailed usage, see QUICKSTART.md and README.md")


if __name__ == "__main__":
    test_rag_system()

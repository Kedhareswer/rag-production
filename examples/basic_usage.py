"""Basic usage example of the Docling RAG system."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import DoclingRAGSystem


def basic_example():
    """Basic usage example with auto-discovery."""
    print("\n" + "=" * 70)
    print("🚀 DOCLING RAG SYSTEM - Basic Usage Example")
    print("=" * 70)

    # Initialize the RAG system
    print("\n1️⃣  Initializing system...")
    rag_system = DoclingRAGSystem()
    print("   ✓ System ready")

    # Auto-ingest all documents from docs folder
    print("\n2️⃣  Auto-ingesting all documents from 'docs' folder...")
    try:
        rag_system.ingest_documents()  # Auto-discovers all supported files
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPlease add documents to 'docs' folder:")
        print("   Supported: PDF, DOCX, XLSX, PPTX, images, Markdown, HTML, CSV")
        return

    # Query the system
    print("\n3️⃣  Querying the system with detailed metrics...")

    questions = [
        "What are the main topics in these documents?",
        "Summarize the key points",
        "What information is most important?",
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}/{len(questions)}")
        print(f"{'='*70}")
        result = rag_system.query(question, verbose=True)

    print("\n" + "=" * 70)
    print("✅ Example Complete!")
    print("=" * 70)
    print("\n📊 Demonstrated Features:")
    print("   ✓ Auto-discovery of all document formats")
    print("   ✓ Multi-format processing (PDF, Office, images, etc.)")
    print("   ✓ Detailed extraction and chunking metrics")
    print("   ✓ RAG with performance metrics")
    print("   ✓ Source attribution with relevance scores")
    print("\n🎯 Try interactive mode: python examples/interactive.py")


if __name__ == "__main__":
    basic_example()

"""Interactive mode for the RAG system."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import DoclingRAGSystem


def interactive_mode():
    """Interactive query mode."""
    rag_system = DoclingRAGSystem()

    print("\n" + "=" * 70)
    print("🤖 DOCLING RAG SYSTEM - Interactive Mode")
    print("=" * 70)
    print("\n📋 Commands:")
    print("  ingest <file_path>  - Add a specific document")
    print("  ingest all          - Auto-ingest all files from docs/ folder")
    print("  quit or exit        - Exit the program")
    print("  help                - Show this help message")
    print("\n💬 Or just type your question!\n")
    print("=" * 70)

    while True:
        try:
            user_input = input("\n> ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit"]:
                print("\n👋 Goodbye!")
                break

            if user_input.lower() == "help":
                print("\n📋 Commands:")
                print("  ingest <file_path>  - Add a specific document")
                print("  ingest all          - Auto-ingest all files from docs/")
                print("  quit or exit        - Exit")
                print("  help                - Show this help")
                print("\n💬 Or just ask a question!")
                continue

            if user_input.lower() == "ingest all":
                try:
                    rag_system.ingest_documents()  # Auto-discover all files
                except Exception as e:
                    print(f"✗ Error: {e}")
                continue

            if user_input.lower().startswith("ingest "):
                file_path = user_input[7:].strip()

                # Handle relative paths from docs folder
                if not Path(file_path).exists():
                    docs_path = Path("docs") / file_path
                    if docs_path.exists():
                        file_path = str(docs_path)

                if not Path(file_path).exists():
                    print(f"❌ File not found: {file_path}")
                    print("   Try: ingest yourfile.pdf")
                    print("   Or: ingest all")
                    continue

                try:
                    rag_system.ingest_documents([file_path])
                except Exception as e:
                    print(f"❌ Error: {e}")
                continue

            # It's a question
            try:
                rag_system.query(user_input, verbose=True)
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    interactive_mode()

"""RAG pipeline using LangChain and Groq."""
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from Storage.vector_store import VectorStore


class RAGPipeline:
    """RAG pipeline for question answering."""

    def __init__(
        self,
        groq_api_key: str,
        vector_store: VectorStore,
        model_name: str = "llama-3.3-70b-versatile",
        temperature: float = 0.1,
    ):
        """Initialize RAG pipeline.

        Args:
            groq_api_key: Groq API key
            vector_store: VectorStore instance
            model_name: Groq model name
            temperature: LLM temperature
        """
        self.vector_store = vector_store
        self.retriever = vector_store.as_retriever(k=10)  # Increased from 4 to 10

        # Initialize Groq LLM
        self.llm = ChatGroq(
            groq_api_key=groq_api_key, model_name=model_name, temperature=temperature
        )

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_template(
            """You are an AI assistant that answers questions based on the provided context.

Use the following pieces of context to answer the question at the end. The context comes from various documents including PDFs, Word documents, images, and other files.

If you can find relevant information in the context, provide a comprehensive answer. If you cannot find the answer in the context, say "I don't have enough information in the provided documents to answer this question."

Context:
{context}

Question: {question}

Answer:"""
        )

        # Create RAG chain
        self.rag_chain = (
            {
                "context": self.retriever | self._format_docs,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _format_docs(self, docs):
        """Format retrieved documents into context string."""
        return "\n\n".join(doc.page_content for doc in docs)

    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system.

        Args:
            question: User question

        Returns:
            Dictionary with answer and source documents
        """
        print(f"\n{'='*70}")
        print(f"🔍 Retrieval Phase")
        print(f"{'='*70}")
        print(f"Query: {question}")
        
        # Get relevant documents with scores
        source_docs_with_scores = self.vector_store.vectorstore.similarity_search_with_relevance_scores(
            question, k=10
        )
        
        # Extract documents and scores
        source_docs = [doc for doc, score in source_docs_with_scores]
        similarity_scores = [score for doc, score in source_docs_with_scores]
        
        print(f"\n📊 Retrieval Metrics:")
        print(f"   Retrieved chunks: {len(source_docs)}")
        
        # Show top chunks with actual similarity scores
        for i, (doc, score) in enumerate(source_docs_with_scores[:5], 1):  # Show top 5
            print(f"\n   Chunk {i}:")
            print(f"      Similarity score: {score:.2%}")
            print(f"      Length: {len(doc.page_content)} chars")
            print(f"      Preview: {doc.page_content[:150]}...")
            if doc.metadata.get('headings'):
                print(f"      Headings: {doc.metadata['headings']}")
        
        if len(source_docs) > 5:
            print(f"\n   ... and {len(source_docs) - 5} more chunks")
        
        avg_relevance = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0
        print(f"\n   Average similarity: {avg_relevance:.2%}")
        
        print(f"\n{'='*70}")
        print(f"🤖 Generation Phase")
        print(f"{'='*70}")
        print(f"   Model: {self.llm.model_name}")
        print(f"   Generating answer...")

        # Get answer from LLM
        answer = self.rag_chain.invoke(question)
        
        print(f"   ✓ Answer generated ({len(answer)} chars)")
        print(f"{'='*70}\n")

        # Format response
        response = {"question": question, "answer": answer, "sources": [], "metrics": {
            "retrieved_chunks": len(source_docs),
            "average_relevance": avg_relevance,
            "answer_length": len(answer)
        }}

        # Add source information with actual similarity scores
        for i, (doc, score) in enumerate(source_docs_with_scores, 1):
            source_info = {
                "source_number": i,
                "text": (
                    doc.page_content[:300] + "..."  # Increased preview length
                    if len(doc.page_content) > 300
                    else doc.page_content
                ),
                "metadata": doc.metadata,
                "relevance_score": score
            }
            response["sources"].append(source_info)

        return response

    def query_simple(self, question: str) -> str:
        """Simple query returning only the answer.

        Args:
            question: User question

        Returns:
            Answer string
        """
        return self.rag_chain.invoke(question)

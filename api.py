"""FastAPI server for Docling RAG System."""
import os
import shutil
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from main import DoclingRAGSystem

# Initialize FastAPI app
app = FastAPI(
    title="Docling RAG API",
    description="API for document processing and question answering using RAG",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files
static_folder = Path("static")
static_folder.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware to allow requests from web browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system (lazy loading)
rag_system = None
docs_folder = Path("docs")
docs_folder.mkdir(exist_ok=True)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 10
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the invoice about?",
                "top_k": 10
            }
        }

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[dict]
    metrics: dict

class StatusResponse(BaseModel):
    status: str
    documents_count: int
    chunks_count: Optional[int]
    model: str
    message: str

class UploadResponse(BaseModel):
    message: str
    filename: str
    size: str
    format: str

# Helper functions
def get_rag_system():
    """Get or initialize RAG system."""
    global rag_system
    if rag_system is None:
        print("🚀 Initializing RAG system...")
        rag_system = DoclingRAGSystem()
        print("✓ RAG system ready!")
    return rag_system

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

# API Endpoints

@app.get("/", tags=["General"])
async def root():
    """Serve the web interface."""
    html_file = Path("static/index.html")
    if html_file.exists():
        return FileResponse(html_file)
    else:
        return {
            "message": "Welcome to Docling RAG API!",
            "version": "1.0.0",
            "web_ui": "/static/index.html (not found)",
            "docs": "/docs",
            "endpoints": {
                "upload": "POST /upload - Upload documents",
                "query": "POST /query - Ask questions",
                "status": "GET /status - System status",
                "documents": "GET /documents - List documents",
                "health": "GET /health - Health check"
            }
        }

@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status", response_model=StatusResponse, tags=["System"])
async def get_status():
    """Get system status and statistics."""
    try:
        # Count documents
        supported_extensions = ['.pdf', '.docx', '.xlsx', '.pptx', '.ppt', 
                              '.md', '.html', '.htm', '.csv',
                              '.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.webp']
        
        doc_count = sum(1 for ext in supported_extensions 
                       for _ in docs_folder.glob(f"*{ext}"))
        
        # Get RAG system info
        rag = get_rag_system()
        
        return StatusResponse(
            status="ready",
            documents_count=doc_count,
            chunks_count=None,  # Could be calculated if needed
            model="llama-3.3-70b-versatile",
            message=f"System ready with {doc_count} documents"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents", tags=["Documents"])
async def list_documents():
    """List all uploaded documents."""
    try:
        documents = []
        supported_extensions = ['.pdf', '.docx', '.xlsx', '.pptx', '.ppt', 
                              '.md', '.html', '.htm', '.csv',
                              '.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.webp']
        
        for ext in supported_extensions:
            for file_path in docs_folder.glob(f"*{ext}"):
                stat = file_path.stat()
                documents.append({
                    "filename": file_path.name,
                    "size": format_file_size(stat.st_size),
                    "format": file_path.suffix,
                    "uploaded_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        return {
            "documents": sorted(documents, key=lambda x: x['uploaded_at'], reverse=True),
            "total": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", response_model=UploadResponse, tags=["Documents"])
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for processing.
    
    Supported formats:
    - PDF (.pdf)
    - Microsoft Office (.docx, .xlsx, .pptx)
    - Images (.png, .jpg, .jpeg, .tiff, .bmp, .webp)
    - Markdown (.md)
    - HTML (.html, .htm)
    - CSV (.csv)
    """
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        allowed_extensions = ['.pdf', '.docx', '.xlsx', '.pptx', '.ppt', 
                            '.md', '.html', '.htm', '.csv',
                            '.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.webp']
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not supported. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save file
        file_path = docs_folder / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = format_file_size(file_path.stat().st_size)
        
        # Process document
        print(f"\n📄 Processing uploaded file: {file.filename}")
        rag = get_rag_system()
        rag.ingest_documents([file_path])
        print(f"✓ File processed successfully\n")
        
        return UploadResponse(
            message="File uploaded and processed successfully",
            filename=file.filename,
            size=file_size,
            format=file_ext
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def query_documents(request: QueryRequest):
    """
    Ask a question about the uploaded documents.
    
    The system will:
    1. Retrieve relevant chunks from documents
    2. Generate an answer using the LLM
    3. Return answer with sources and metrics
    """
    try:
        # Get RAG system
        rag = get_rag_system()
        
        # Check if documents exist
        doc_count = sum(1 for _ in docs_folder.glob("*.*"))
        if doc_count == 0:
            raise HTTPException(
                status_code=400,
                detail="No documents uploaded. Please upload documents first using /upload endpoint."
            )
        
        # Query the system
        print(f"\n💬 Query: {request.question}")
        result = rag.query(request.question, verbose=False)
        print(f"✓ Answer generated\n")
        
        return QueryResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"][:5],  # Return top 5 sources
            metrics=result["metrics"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.delete("/documents/{filename}", tags=["Documents"])
async def delete_document(filename: str):
    """Delete a specific document."""
    try:
        file_path = docs_folder / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path.unlink()
        
        return {
            "message": "Document deleted successfully",
            "filename": filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest-all", tags=["System"])
async def ingest_all_documents():
    """
    Process all documents in the docs folder.
    Useful after uploading multiple files.
    """
    try:
        rag = get_rag_system()
        
        print("\n🚀 Ingesting all documents...")
        rag.ingest_documents()  # Auto-discovers all files
        print("✓ All documents processed\n")
        
        return {
            "message": "All documents processed successfully",
            "status": "complete"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run server
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 Starting Docling RAG API Server")
    print("="*70)
    print("\n📚 API Documentation:")
    print("   • Swagger UI: http://localhost:8000/docs")
    print("   • ReDoc: http://localhost:8000/redoc")
    print("\n🔗 API Endpoints:")
    print("   • Upload: POST http://localhost:8000/upload")
    print("   • Query: POST http://localhost:8000/query")
    print("   • Status: GET http://localhost:8000/status")
    print("   • Documents: GET http://localhost:8000/documents")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )

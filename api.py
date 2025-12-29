"""
FastAPI Backend for AI Study Buddy.
Provides REST API for the React frontend.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import io

from config import check_ollama_available, check_ollama_models
from rag_engine import RAGEngine
from document_processor import get_supported_formats

# Create FastAPI app
app = FastAPI(
    title="Study Buddy API",
    description="AI-powered study assistant API",
    version="2.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG engine instance
rag_engine = RAGEngine()


# Request/Response models
class AskRequest(BaseModel):
    question: str
    document_filter: Optional[str] = None


class AskResponse(BaseModel):
    answer: str
    sources: List[dict]
    documents_searched: List[str]
    error: Optional[str] = None


# Routes
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Study Buddy API is running"}


@app.get("/status")
async def get_status():
    """Get system status (Ollama availability, models)."""
    model_status = check_ollama_models()
    return {
        "ollama_available": model_status["available"],
        "llm_ready": model_status["llm_ready"],
        "embedding_ready": model_status["embedding_ready"],
        "missing_models": model_status["missing_models"],
    }


@app.get("/documents")
async def list_documents():
    """List all indexed documents."""
    return {
        "documents": rag_engine.get_documents(),
        "count": rag_engine.document_count,
        "total_chunks": rag_engine.chunk_count,
    }


@app.get("/documents/{document_name}")
async def get_document_info(document_name: str):
    """Get info about a specific document."""
    info = rag_engine.get_document_info(document_name)
    if not info:
        raise HTTPException(status_code=404, detail="Document not found")
    return info


@app.delete("/documents/{document_name}")
async def remove_document(document_name: str):
    """Remove a document from the index."""
    success = rag_engine.remove_document(document_name)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"success": True, "message": f"Removed {document_name}"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document."""
    # Validate file type
    supported = get_supported_formats()
    ext = file.filename.split('.')[-1].lower() if file.filename else ''
    
    if ext not in supported:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {ext}. Supported: {', '.join(supported.keys())}"
        )
    
    try:
        # Create a file-like object for the RAG engine
        content = await file.read()
        
        # Create a mock uploaded file object
        class MockUploadedFile:
            def __init__(self, name, content):
                self.name = name
                self._content = content
                self._position = 0
            
            def read(self):
                return self._content
            
            def seek(self, pos):
                self._position = pos
        
        mock_file = MockUploadedFile(file.filename, content)
        result = rag_engine.process_document(mock_file)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """Ask a question about the documents."""
    if not rag_engine.is_ready:
        return AskResponse(
            answer="Please upload a document first.",
            sources=[],
            documents_searched=[],
            error="no_documents"
        )
    
    result = rag_engine.ask_question(
        question=request.question,
        document_filter=request.document_filter
    )
    
    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        documents_searched=result["documents_searched"],
        error=result.get("error")
    )


@app.post("/clear-chat")
async def clear_chat():
    """Clear conversation history."""
    rag_engine.clear_conversation()
    return {"success": True, "message": "Chat cleared"}


@app.post("/clear-all")
async def clear_all():
    """Clear all documents and chat."""
    rag_engine.clear_all()
    return {"success": True, "message": "All data cleared"}


@app.get("/stats")
async def get_stats():
    """Get session statistics."""
    return rag_engine.get_session_stats()


@app.get("/export")
async def export_conversation(format: str = "markdown"):
    """Export conversation as markdown or JSON."""
    content = rag_engine.export_conversation(format)
    return {"content": content, "format": format}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

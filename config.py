"""
Configuration module for AI Study Buddy.
Phase 3: Added conversation memory settings and chunk optimization.
"""

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass
class Config:
    """Configuration settings for the RAG application."""
    
    # Ollama settings (runs locally, completely free)
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2"
    embedding_model: str = "nomic-embed-text"
    
    # Phase 3: Optimized chunking settings
    chunk_size: int = 400  # Smaller chunks = more precise retrieval
    chunk_overlap: int = 100  # More overlap = better context continuity
    
    # Retrieval settings
    top_k_results: int = 5  # Slightly more results for better context
    
    # ChromaDB settings
    collection_name: str = "study_documents"
    persist_directory: str = "./chroma_db"
    
    # Multi-document settings
    max_documents: int = 20
    
    # Phase 3: Conversation memory
    max_conversation_history: int = 5  # Number of previous Q&A pairs to remember
    include_conversation_context: bool = True  # Use chat history for follow-ups


def get_config() -> Config:
    """Get the application configuration."""
    config = Config()
    Path(config.persist_directory).mkdir(parents=True, exist_ok=True)
    return config


def check_ollama_available() -> bool:
    """Check if Ollama is running and accessible."""
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def check_ollama_models() -> dict:
    """
    Check which required models are installed.
    Phase 3: Better error handling with specific model checks.
    """
    import requests
    result = {
        "available": False,
        "llm_ready": False,
        "embedding_ready": False,
        "missing_models": []
    }
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            return result
        
        result["available"] = True
        models = [m["name"].split(":")[0] for m in response.json().get("models", [])]
        
        config = get_config()
        
        if config.llm_model.split(":")[0] in models:
            result["llm_ready"] = True
        else:
            result["missing_models"].append(config.llm_model)
        
        if config.embedding_model.split(":")[0] in models:
            result["embedding_ready"] = True
        else:
            result["missing_models"].append(config.embedding_model)
        
        return result
        
    except:
        return result

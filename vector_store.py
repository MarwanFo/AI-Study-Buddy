"""
Vector store module for AI Study Buddy.
Uses ChromaDB with Ollama embeddings (completely free).

Phase 2: Persistent storage and multi-document support.
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from pathlib import Path
import json


class VectorStore:
    """
    Manages document embeddings using ChromaDB and Ollama.
    
    Phase 2 Features:
    - Persistent storage (survives app restarts)
    - Multi-document support with document filtering
    - Rich metadata for citations
    """
    
    def __init__(
        self,
        collection_name: str = "study_documents",
        embedding_model: str = "nomic-embed-text",
        ollama_base_url: str = "http://localhost:11434",
        persist_directory: str = "./chroma_db"
    ):
        """
        Initialize the vector store with persistence.
        
        Args:
            collection_name: Name for the ChromaDB collection
            embedding_model: Ollama embedding model to use
            ollama_base_url: URL where Ollama is running
            persist_directory: Directory to persist the database
        """
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.ollama_base_url = ollama_base_url
        self.persist_directory = persist_directory
        
        # Ensure persist directory exists
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Study documents for RAG"}
        )
        
        # Track documents
        self._load_document_registry()
    
    def _load_document_registry(self):
        """Load the list of indexed documents."""
        registry_path = Path(self.persist_directory) / "document_registry.json"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                self._documents = json.load(f)
        else:
            self._documents = {}
    
    def _save_document_registry(self):
        """Save the list of indexed documents."""
        registry_path = Path(self.persist_directory) / "document_registry.json"
        with open(registry_path, 'w') as f:
            json.dump(self._documents, f, indent=2)
    
    def _get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for a single text using Ollama.
        """
        import requests
        
        response = requests.post(
            f"{self.ollama_base_url}/api/embeddings",
            json={
                "model": self.embedding_model,
                "prompt": text
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Ollama embedding failed: {response.text}")
        
        return response.json()["embedding"]
    
    def _get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts."""
        embeddings = []
        for text in texts:
            embedding = self._get_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def add_document(
        self,
        document_name: str,
        chunks: List[Dict[str, Any]]
    ) -> int:
        """
        Add a document's chunks to the vector store.
        
        Phase 2: Supports rich metadata for citations.
        
        Args:
            document_name: Name of the document
            chunks: List of dicts with 'text', 'page', 'document' keys
            
        Returns:
            Number of chunks added
        """
        if not chunks:
            return 0
        
        # Check if document already exists - remove old version first
        if document_name in self._documents:
            self.remove_document(document_name)
        
        # Extract text for embedding
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings
        print(f"  Generating embeddings for {len(chunks)} chunks...")
        embeddings = self._get_embeddings_batch(texts)
        
        # Create IDs and metadata
        base_id = len(self.collection.get()['ids'])
        ids = [f"doc_{document_name}_{i}" for i in range(len(chunks))]
        
        metadatas = [
            {
                "document": chunk['document'],
                "page": chunk['page'],
                "chunk_index": i
            }
            for i, chunk in enumerate(chunks)
        ]
        
        # Add to ChromaDB
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        
        # Update document registry
        self._documents[document_name] = {
            "chunk_count": len(chunks),
            "chunk_ids": ids
        }
        self._save_document_registry()
        
        print(f"  ✓ Added {len(chunks)} chunks from '{document_name}'")
        
        return len(chunks)
    
    def remove_document(self, document_name: str) -> bool:
        """
        Remove a document from the vector store.
        
        Args:
            document_name: Name of the document to remove
            
        Returns:
            True if removed, False if not found
        """
        if document_name not in self._documents:
            return False
        
        # Get chunk IDs for this document
        chunk_ids = self._documents[document_name]["chunk_ids"]
        
        # Remove from ChromaDB
        self.collection.delete(ids=chunk_ids)
        
        # Update registry
        del self._documents[document_name]
        self._save_document_registry()
        
        print(f"  ✓ Removed document '{document_name}'")
        return True
    
    def query(
        self,
        question: str,
        n_results: int = 4,
        document_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find the most relevant chunks for a question.
        
        Phase 2: Supports filtering by document and returns rich metadata.
        
        Args:
            question: The question to find relevant context for
            n_results: Number of results to return
            document_filter: Optional document name to filter by
            
        Returns:
            List of dicts with 'content', 'metadata', 'distance', 'page', 'document' keys
        """
        # Get question embedding
        question_embedding = self._get_embedding(question)
        
        # Build where filter if document specified
        where_filter = None
        if document_filter:
            where_filter = {"document": document_filter}
        
        # Query ChromaDB
        total_docs = len(self.collection.get()['ids'])
        results = self.collection.query(
            query_embeddings=[question_embedding],
            n_results=min(n_results, total_docs) if total_docs > 0 else 1,
            where=where_filter
        )
        
        # Format results with rich metadata
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                formatted_results.append({
                    'content': doc,
                    'metadata': metadata,
                    'distance': results['distances'][0][i] if results['distances'] else 0,
                    'page': metadata.get('page', 'Unknown'),
                    'document': metadata.get('document', 'Unknown')
                })
        
        return formatted_results
    
    def get_documents(self) -> List[str]:
        """Get list of indexed document names."""
        return list(self._documents.keys())
    
    def get_document_info(self, document_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific document."""
        return self._documents.get(document_name)
    
    def clear(self):
        """Clear all documents from the store."""
        # Delete and recreate collection
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Study documents for RAG"}
        )
        self._documents = {}
        self._save_document_registry()
        print("  ✓ Vector store cleared")
    
    @property
    def document_count(self) -> int:
        """Get the number of documents stored."""
        return len(self._documents)
    
    @property
    def chunk_count(self) -> int:
        """Get the total number of chunks stored."""
        return len(self.collection.get()['ids'])

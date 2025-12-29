"""
RAG Engine for AI Study Buddy.
Phase 4: Multi-format support, export features, session tracking.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import requests
import json

from config import Config, get_config
from document_processor import extract_text_from_file, smart_chunk_text, get_supported_formats
from vector_store import VectorStore


class RAGEngine:
    """
    The brain of your AI Study Buddy.
    
    Phase 4 Features:
    - Multi-format document support (PDF, DOCX, TXT, MD)
    - Export conversation to Markdown
    - Session statistics tracking
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the RAG engine."""
        self.config = config or get_config()
        
        # Initialize vector store
        self.vector_store = VectorStore(
            collection_name=self.config.collection_name,
            embedding_model=self.config.embedding_model,
            ollama_base_url=self.config.ollama_base_url,
            persist_directory=self.config.persist_directory
        )
        
        # Conversation memory
        self._conversation_history: List[Dict[str, str]] = []
        
        # Phase 4: Session statistics
        self._session_stats = {
            "documents_processed": 0,
            "questions_asked": 0,
            "chunks_retrieved": 0,
            "session_start": datetime.now().isoformat()
        }
    
    def get_supported_formats(self) -> Dict[str, str]:
        """Get supported file formats."""
        return get_supported_formats()
    
    def process_document(self, uploaded_file) -> Dict[str, Any]:
        """
        Process an uploaded file (PDF, DOCX, TXT, MD).
        Phase 4: Multi-format support.
        """
        document_name = uploaded_file.name
        print(f"\n📄 Processing: {document_name}")
        
        try:
            # Extract text (auto-detects format)
            print("  Extracting text...")
            text, page_map, file_type = extract_text_from_file(uploaded_file)
            
            print(f"  Detected format: {file_type.upper()}")
            
            # Chunk with smart algorithm
            print("  Creating semantic chunks...")
            chunks = smart_chunk_text(
                text,
                page_map,
                document_name,
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap
            )
            
            if not chunks:
                raise ValueError("No text could be extracted from the file")
            
            # Add to vector store
            self.vector_store.add_document(document_name, chunks)
            
            # Update stats
            self._session_stats["documents_processed"] += 1
            
            return {
                "success": True,
                "document_name": document_name,
                "file_type": file_type,
                "total_characters": len(text),
                "num_chunks": len(chunks),
                "num_pages": len(page_map),
                "total_documents": self.vector_store.document_count
            }
            
        except ValueError as e:
            raise
        except Exception as e:
            raise ValueError(f"Failed to process '{document_name}': {str(e)}")
    
    def remove_document(self, document_name: str) -> bool:
        """Remove a document from the vector store."""
        return self.vector_store.remove_document(document_name)
    
    def ask_question(
        self,
        question: str,
        document_filter: Optional[str] = None,
        use_conversation_memory: bool = True
    ) -> Dict[str, Any]:
        """Ask a question about the loaded documents."""
        if self.vector_store.document_count == 0:
            return {
                "answer": "📚 Please upload a document first before asking questions.",
                "sources": [],
                "documents_searched": [],
                "error": None
            }
        
        try:
            # Retrieve relevant chunks
            filter_msg = f" in '{document_filter}'" if document_filter else ""
            print(f"\n🔍 Finding relevant information{filter_msg}...")
            
            relevant_chunks = self.vector_store.query(
                question,
                n_results=self.config.top_k_results,
                document_filter=document_filter
            )
            
            # Update stats
            self._session_stats["questions_asked"] += 1
            self._session_stats["chunks_retrieved"] += len(relevant_chunks)
            
            if not relevant_chunks:
                return {
                    "answer": "I couldn't find any relevant information in the documents. Try rephrasing or uploading more content.",
                    "sources": [],
                    "documents_searched": self.get_documents(),
                    "error": None
                }
            
            # Build context
            context_parts = []
            for i, chunk in enumerate(relevant_chunks):
                source_info = f"[{chunk['document']}, Page {chunk['page']}]"
                context_parts.append(f"[Source {i+1}] {source_info}\n{chunk['content']}")
            
            context = "\n\n---\n\n".join(context_parts)
            
            # Conversation context
            conv_context = ""
            if use_conversation_memory and self.config.include_conversation_context:
                conv_context = self._build_conversation_context()
            
            # Generate answer
            print("  Generating answer...")
            answer = self._generate_answer(question, context, conv_context)
            
            # Update history
            self._add_to_history(question, answer)
            
            # Format sources
            sources = [
                {
                    "document": chunk["document"],
                    "page": chunk["page"],
                    "content": chunk["content"][:250] + "..." if len(chunk["content"]) > 250 else chunk["content"],
                    "relevance": round((1 - chunk["distance"]) * 100, 1)
                }
                for chunk in relevant_chunks
            ]
            
            return {
                "answer": answer,
                "sources": sources,
                "documents_searched": list(set(s["document"] for s in sources)),
                "error": None
            }
            
        except Exception as e:
            error_msg = str(e)
            if "connection" in error_msg.lower():
                return {
                    "answer": "❌ Cannot connect to Ollama. Please run: `ollama serve`",
                    "sources": [],
                    "documents_searched": [],
                    "error": "connection_error"
                }
            return {
                "answer": f"❌ An error occurred: {error_msg}",
                "sources": [],
                "documents_searched": [],
                "error": "unknown_error"
            }
    
    def _build_conversation_context(self) -> str:
        """Build context from recent conversation."""
        if not self._conversation_history:
            return ""
        
        recent = self._conversation_history[-self.config.max_conversation_history:]
        
        context_parts = ["PREVIOUS CONVERSATION:"]
        for exchange in recent:
            context_parts.append(f"User: {exchange['question']}")
            answer = exchange['answer']
            if len(answer) > 200:
                answer = answer[:200] + "..."
            context_parts.append(f"Assistant: {answer}")
        
        return "\n".join(context_parts)
    
    def _add_to_history(self, question: str, answer: str):
        """Add Q&A to history."""
        self._conversation_history.append({
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        })
        
        max_history = self.config.max_conversation_history * 2
        if len(self._conversation_history) > max_history:
            self._conversation_history = self._conversation_history[-max_history:]
    
    def _generate_answer(self, question: str, context: str, conv_context: str = "") -> str:
        """Generate answer using Ollama."""
        prompt_parts = [
            "You are a helpful, friendly study assistant. Answer questions based on the provided study materials.",
            "",
            "STUDY MATERIALS:",
            context,
        ]
        
        if conv_context:
            prompt_parts.extend(["", conv_context])
        
        prompt_parts.extend([
            "",
            f"CURRENT QUESTION: {question}",
            "",
            "INSTRUCTIONS:",
            "- Answer based ONLY on the study materials above",
            "- If the answer isn't in the materials, say so honestly",
            "- Reference the source document and page when relevant",
            "- Be clear, educational, and helpful",
            "",
            "YOUR ANSWER:"
        ])
        
        prompt = "\n".join(prompt_parts)
        
        try:
            response = requests.post(
                f"{self.config.ollama_base_url}/api/generate",
                json={
                    "model": self.config.llm_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 600
                    }
                },
                timeout=180
            )
            
            if response.status_code != 200:
                return f"Error from Ollama: {response.text}"
            
            return response.json()["response"].strip()
            
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Cannot connect to Ollama")
        except requests.exceptions.Timeout:
            return "⏱️ Response timed out. Try a shorter question."
        except Exception as e:
            raise RuntimeError(f"LLM error: {str(e)}")
    
    # Phase 4: Export features
    def export_conversation(self, format: str = "markdown") -> str:
        """
        Export the conversation history.
        
        Args:
            format: 'markdown' or 'json'
            
        Returns:
            Exported content as string
        """
        if format == "json":
            return json.dumps({
                "exported_at": datetime.now().isoformat(),
                "documents": self.get_documents(),
                "conversation": self._conversation_history,
                "stats": self._session_stats
            }, indent=2)
        
        # Markdown format
        lines = [
            "# AI Study Buddy - Conversation Export",
            f"",
            f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Documents:** {', '.join(self.get_documents()) or 'None'}",
            f"**Questions asked:** {self._session_stats['questions_asked']}",
            "",
            "---",
            ""
        ]
        
        for i, exchange in enumerate(self._conversation_history, 1):
            timestamp = exchange.get('timestamp', 'Unknown')
            if isinstance(timestamp, str) and 'T' in timestamp:
                timestamp = timestamp.split('T')[1][:5]
            
            lines.extend([
                f"## Question {i}",
                f"",
                f"**Q:** {exchange['question']}",
                f"",
                f"**A:** {exchange['answer']}",
                f"",
                "---",
                ""
            ])
        
        return "\n".join(lines)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics."""
        return {
            **self._session_stats,
            "conversation_length": len(self._conversation_history),
            "documents_loaded": self.vector_store.document_count,
            "total_chunks": self.vector_store.chunk_count
        }
    
    def clear_conversation(self):
        """Clear conversation history."""
        self._conversation_history = []
        print("  ✓ Conversation history cleared")
    
    def get_documents(self) -> List[str]:
        """Get list of all indexed documents."""
        return self.vector_store.get_documents()
    
    def get_document_info(self, document_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific document."""
        return self.vector_store.get_document_info(document_name)
    
    @property
    def is_ready(self) -> bool:
        """Check if any documents are loaded."""
        return self.vector_store.document_count > 0
    
    @property
    def document_count(self) -> int:
        """Get number of loaded documents."""
        return self.vector_store.document_count
    
    @property
    def chunk_count(self) -> int:
        """Get total number of chunks."""
        return self.vector_store.chunk_count
    
    @property
    def conversation_length(self) -> int:
        """Get number of exchanges."""
        return len(self._conversation_history)
    
    def clear_all(self):
        """Clear all documents and conversation."""
        self.vector_store.clear()
        self.clear_conversation()
        self._session_stats = {
            "documents_processed": 0,
            "questions_asked": 0,
            "chunks_retrieved": 0,
            "session_start": datetime.now().isoformat()
        }

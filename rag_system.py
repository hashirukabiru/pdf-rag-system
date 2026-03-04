"""
Main RAG System
Orchestrates PDF processing, vector search, and LLM generation
"""

from typing import List, Dict, Optional
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from llm_handler import LLMHandler
import config

try:
    from pruning_strategies import ContextWindowOptimizer
    PRUNING_AVAILABLE = True
except ImportError:
    PRUNING_AVAILABLE = False


class RAGSystem:
    """Complete RAG system for PDF question answering"""
    
    def __init__(self, llm_backend: str = "huggingface", enable_optimization: bool = None):
        """
        Initialize RAG system
        
        Args:
            llm_backend: Either "ollama" or "huggingface"
            enable_optimization: Enable token optimization (default: from config)
        """
        self.pdf_processor = PDFProcessor()
        self.vector_store = VectorStore()
        self.llm_handler = LLMHandler(backend=llm_backend)
        self.is_ready = False
        self.current_pdf = None
        
        # Token optimization
        if enable_optimization is None:
            enable_optimization = config.ENABLE_TOKEN_OPTIMIZATION
        
        self.enable_optimization = enable_optimization and PRUNING_AVAILABLE
        if self.enable_optimization:
            self.optimizer = ContextWindowOptimizer(
                max_context_tokens=config.MAX_CONTEXT_TOKENS
            )
            print("✓ Token optimization enabled")
    
    def load_and_process_pdf(self, pdf_path: str) -> Dict[str, any]:
        """
        Load a PDF and prepare it for Q&A
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with processing statistics
        """
        try:
            # Process PDF into chunks
            chunks = self.pdf_processor.process_pdf(pdf_path)
            
            if not chunks:
                raise ValueError("No text chunks were created from the PDF")
            
            # Build vector index
            self.vector_store.build_index(chunks)
            
            self.is_ready = True
            self.current_pdf = pdf_path
            
            return {
                "success": True,
                "num_chunks": len(chunks),
                "chunk_size": self.pdf_processor.chunk_size,
                "message": f"Successfully processed {len(chunks)} chunks"
            }
        
        except Exception as e:
            self.is_ready = False
            return {
                "success": False,
                "error": str(e),
                "message": f"Error processing PDF: {str(e)}"
            }
    
    def answer_question(self, question: str, top_k: int = None) -> Dict[str, any]:
        """
        Answer a question about the loaded PDF
        
        Args:
            question: User's question
            top_k: Number of chunks to retrieve
            
        Returns:
            Dictionary with answer and metadata
        """
        if not self.is_ready:
            return {
                "success": False,
                "answer": "Please load a PDF file first.",
                "context_chunks": [],
                "distances": []
            }
        
        try:
            # Retrieve relevant chunks
            top_k = top_k or config.TOP_K_CHUNKS
            chunks, distances = self.vector_store.search(question, top_k=top_k)
            
            # Token usage tracking
            original_tokens = 0
            optimized_tokens = 0
            
            # Apply token optimization if enabled
            if self.enable_optimization:
                # Count original tokens
                for chunk in chunks:
                    original_tokens += self._estimate_tokens(chunk)
                
                optimized_context = self.optimizer.optimize_context(
                    chunks, distances, question
                )
                optimized_tokens = self._estimate_tokens(optimized_context)
                
                # Generate answer with optimized context
                answer = self.llm_handler.generate_answer([optimized_context], question)
            else:
                # Generate answer with all chunks
                for chunk in chunks:
                    original_tokens += self._estimate_tokens(chunk)
                optimized_tokens = original_tokens
                answer = self.llm_handler.generate_answer(chunks, question)
            
            return {
                "success": True,
                "answer": answer,
                "context_chunks": chunks,
                "distances": distances,
                "num_chunks_used": len(chunks),
                "token_stats": {
                    "original_tokens": original_tokens,
                    "optimized_tokens": optimized_tokens,
                    "tokens_saved": original_tokens - optimized_tokens,
                    "reduction_percent": round(((original_tokens - optimized_tokens) / original_tokens * 100), 1) if original_tokens > 0 else 0
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "answer": f"Error generating answer: {str(e)}",
                "context_chunks": [],
                "distances": []
            }
    
    def reset(self):
        """Reset the RAG system"""
        self.vector_store.clear()
        self.is_ready = False
        self.current_pdf = None
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for a text string
        Rule of thumb: ~4 characters per token for English
        """
        return len(text) // 4

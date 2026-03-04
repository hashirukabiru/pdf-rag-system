"""
Simple RAG System - No LLM required
Uses FAISS for semantic search and returns relevant chunks
"""

import os
from typing import List, Dict
from pypdf import PdfReader
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class SimpleRAG:
    """Simple RAG system that returns relevant chunks without LLM generation"""
    
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunks = []
        self.index = None
        self.is_ready = False
        
        # Load embedding model (this should work offline if cached)
        print("Loading embedding model...")
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("✓ Embedding model loaded")
    
    def load_and_process_pdf(self, pdf_path: str) -> Dict:
        """Load PDF and create vector index"""
        try:
            # Extract text
            text = self._extract_pdf_text(pdf_path)
            
            # Chunk text
            self.chunks = self._chunk_text(text)
            
            if not self.chunks:
                return {
                    "success": False,
                    "message": "No text could be extracted from PDF"
                }
            
            # Create embeddings
            embeddings = self._create_embeddings(self.chunks)
            
            # Create FAISS index
            self._create_index(embeddings)
            
            self.is_ready = True
            
            return {
                "success": True,
                "num_chunks": len(self.chunks),
                "chunk_size": self.chunk_size
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
    
    def answer_question(self, question: str, top_k: int = 3) -> Dict:
        """Find and return most relevant chunks"""
        if not self.is_ready:
            return {
                "success": False,
                "answer": "Please upload and process a PDF first!"
            }
        
        try:
            # Get relevant chunks
            chunks, distances = self._search(question, top_k)
            
            # Combine chunks into answer
            answer = "\n\n---\n\n".join(chunks)
            
            return {
                "success": True,
                "answer": answer,
                "context_chunks": chunks,
                "distances": distances
            }
        
        except Exception as e:
            return {
                "success": False,
                "answer": f"Error: {str(e)}"
            }
    
    def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            if chunk.strip():
                chunks.append(chunk)
            
            start += self.chunk_size - self.chunk_overlap
        
        return chunks
    
    def _create_embeddings(self, chunks: List[str]) -> np.ndarray:
        """Create embeddings for chunks"""
        print(f"Creating embeddings for {len(chunks)} chunks...")
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        return np.array(embeddings).astype("float32")
    
    def _create_index(self, embeddings: np.ndarray):
        """Create FAISS index"""
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        print(f"✓ FAISS index created with {len(self.chunks)} chunks")
    
    def _search(self, question: str, top_k: int) -> tuple:
        """Search for most relevant chunks"""
        query_embedding = self.model.encode([question]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        
        top_chunks = [self.chunks[i] for i in indices[0]]
        return top_chunks, distances[0]

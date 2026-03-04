"""
Vector Store Module
Handles embeddings creation and FAISS indexing
"""

import numpy as np
import faiss
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import config


class VectorStore:
    """Manage embeddings and vector similarity search"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)
        self.index = None
        self.chunks = []
        self.dimension = None
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Create embeddings for a list of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            Numpy array of embeddings
        """
        if not texts:
            raise ValueError("No texts provided for embedding")
        
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return np.array(embeddings).astype("float32")
    
    def build_index(self, chunks: List[str]):
        """
        Build FAISS index from text chunks
        
        Args:
            chunks: List of text chunks
        """
        if not chunks:
            raise ValueError("No chunks provided to build index")
        
        self.chunks = chunks
        embeddings = self.create_embeddings(chunks)
        
        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)
        
        print(f"✓ Built FAISS index with {len(chunks)} chunks")
    
    def search(self, query: str, top_k: int = None) -> Tuple[List[str], List[float]]:
        """
        Search for most similar chunks to a query
        
        Args:
            query: Query string
            top_k: Number of top results to return
            
        Returns:
            Tuple of (top chunks, distances)
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        
        top_k = top_k or config.TOP_K_CHUNKS
        top_k = min(top_k, len(self.chunks))  # Don't exceed available chunks
        
        query_embedding = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        
        top_chunks = [self.chunks[i] for i in indices[0]]
        return top_chunks, distances[0].tolist()
    
    def clear(self):
        """Clear the index and chunks"""
        self.index = None
        self.chunks = []
        self.dimension = None

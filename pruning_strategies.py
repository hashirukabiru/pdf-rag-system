"""
Token Pruning Strategies for RAG Systems
Techniques to reduce token consumption while maintaining quality
"""

import re
from typing import List, Tuple
import numpy as np


class TextPruner:
    """Prune and optimize text chunks to reduce token consumption"""
    
    def __init__(self, max_tokens_per_chunk: int = 150):
        """
        Initialize pruner
        
        Args:
            max_tokens_per_chunk: Maximum tokens to keep per chunk
        """
        self.max_tokens_per_chunk = max_tokens_per_chunk
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count (rough approximation)
        More accurate: use tiktoken for OpenAI models
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        # Rough estimate: ~1 token per 4 characters for English
        return len(text) // 4
    
    def prune_by_relevance_score(
        self, 
        chunks: List[str], 
        distances: List[float],
        threshold: float = 0.5
    ) -> Tuple[List[str], List[float]]:
        """
        Prune chunks based on relevance score threshold
        
        Args:
            chunks: List of text chunks
            distances: FAISS distances (lower = more relevant)
            threshold: Maximum distance to keep (prune higher distances)
            
        Returns:
            Filtered chunks and distances
        """
        pruned_chunks = []
        pruned_distances = []
        
        for chunk, distance in zip(chunks, distances):
            if distance <= threshold:
                pruned_chunks.append(chunk)
                pruned_distances.append(distance)
        
        return pruned_chunks, pruned_distances
    
    def prune_by_token_limit(
        self,
        chunks: List[str],
        max_total_tokens: int = 500
    ) -> List[str]:
        """
        Prune chunks to fit within total token budget
        
        Args:
            chunks: List of text chunks
            max_total_tokens: Maximum total tokens across all chunks
            
        Returns:
            Pruned chunks that fit within token budget
        """
        pruned_chunks = []
        current_tokens = 0
        
        for chunk in chunks:
            chunk_tokens = self.estimate_tokens(chunk)
            
            if current_tokens + chunk_tokens <= max_total_tokens:
                pruned_chunks.append(chunk)
                current_tokens += chunk_tokens
            else:
                # Try to fit a truncated version
                remaining_tokens = max_total_tokens - current_tokens
                if remaining_tokens > 50:  # Only if we have meaningful space
                    truncated = self.truncate_to_token_limit(chunk, remaining_tokens)
                    pruned_chunks.append(truncated)
                break
        
        return pruned_chunks
    
    def truncate_to_token_limit(self, text: str, max_tokens: int) -> str:
        """
        Truncate text to fit token limit
        
        Args:
            text: Input text
            max_tokens: Maximum tokens to keep
            
        Returns:
            Truncated text
        """
        # Estimate character limit
        max_chars = max_tokens * 4
        
        if len(text) <= max_chars:
            return text
        
        # Truncate at sentence boundary if possible
        truncated = text[:max_chars]
        last_period = truncated.rfind('.')
        last_newline = truncated.rfind('\n')
        
        cutoff = max(last_period, last_newline)
        if cutoff > max_chars * 0.8:  # If we found a good break point
            return truncated[:cutoff + 1]
        else:
            return truncated + "..."
    
    def remove_redundant_content(self, chunks: List[str]) -> List[str]:
        """
        Remove highly similar/redundant chunks
        
        Args:
            chunks: List of text chunks
            
        Returns:
            Deduplicated chunks
        """
        if not chunks:
            return []
        
        unique_chunks = [chunks[0]]
        
        for chunk in chunks[1:]:
            # Simple similarity check (can be improved with embeddings)
            is_unique = True
            for existing in unique_chunks:
                similarity = self._jaccard_similarity(chunk, existing)
                if similarity > 0.7:  # 70% similar
                    is_unique = False
                    break
            
            if is_unique:
                unique_chunks.append(chunk)
        
        return unique_chunks
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def extract_key_sentences(
        self,
        text: str,
        question: str,
        max_sentences: int = 3
    ) -> str:
        """
        Extract most relevant sentences from text based on question
        
        Args:
            text: Input text
            question: User question
            max_sentences: Maximum sentences to extract
            
        Returns:
            Extracted key sentences
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Score sentences by keyword overlap with question
        question_words = set(question.lower().split())
        scored_sentences = []
        
        for sentence in sentences:
            sentence_words = set(sentence.lower().split())
            overlap = len(question_words.intersection(sentence_words))
            scored_sentences.append((sentence, overlap))
        
        # Sort by score and take top N
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in scored_sentences[:max_sentences]]
        
        return ' '.join(top_sentences)
    
    def compress_whitespace(self, text: str) -> str:
        """
        Remove excessive whitespace to save tokens
        
        Args:
            text: Input text
            
        Returns:
            Compressed text
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace multiple newlines with single newline
        text = re.sub(r'\n+', '\n', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def remove_boilerplate(self, text: str) -> str:
        """
        Remove common boilerplate text that adds no value
        
        Args:
            text: Input text
            
        Returns:
            Text with boilerplate removed
        """
        # Common boilerplate patterns
        boilerplate_patterns = [
            r'Copyright \d{4}.*',
            r'All rights reserved.*',
            r'Page \d+ of \d+',
            r'This page intentionally left blank',
            r'^\s*\d+\s*$',  # Page numbers alone
        ]
        
        for pattern in boilerplate_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        return text


class ContextWindowOptimizer:
    """Optimize context window to fit LLM token limits"""
    
    def __init__(self, max_context_tokens: int = 1000):
        """
        Initialize optimizer
        
        Args:
            max_context_tokens: Maximum tokens for context
        """
        self.max_context_tokens = max_context_tokens
        self.pruner = TextPruner()
    
    def optimize_context(
        self,
        chunks: List[str],
        distances: List[float],
        question: str
    ) -> str:
        """
        Optimize chunks to fit within token budget
        
        Args:
            chunks: Retrieved chunks
            distances: Relevance distances
            question: User question
            
        Returns:
            Optimized context string
        """
        # Step 1: Prune by relevance threshold
        chunks, distances = self.pruner.prune_by_relevance_score(
            chunks, distances, threshold=0.8
        )
        
        # Step 2: Remove redundant chunks
        chunks = self.pruner.remove_redundant_content(chunks)
        
        # Step 3: Compress whitespace
        chunks = [self.pruner.compress_whitespace(c) for c in chunks]
        
        # Step 4: Remove boilerplate
        chunks = [self.pruner.remove_boilerplate(c) for c in chunks]
        
        # Step 5: Extract key sentences if still too large
        processed_chunks = []
        for chunk in chunks:
            if self.pruner.estimate_tokens(chunk) > 200:
                chunk = self.pruner.extract_key_sentences(chunk, question, max_sentences=3)
            processed_chunks.append(chunk)
        
        # Step 6: Fit within token budget
        final_chunks = self.pruner.prune_by_token_limit(
            processed_chunks,
            max_total_tokens=self.max_context_tokens
        )
        
        return '\n\n'.join(final_chunks)


# Example usage
if __name__ == "__main__":
    # Example chunks from FAISS retrieval
    chunks = [
        "Machine learning is a subset of artificial intelligence that focuses on learning from data. " * 5,
        "Deep learning uses neural networks with multiple layers to process information. " * 5,
        "Natural language processing helps computers understand human language. " * 5,
        "Copyright 2024. All rights reserved. Page 1 of 100.",  # Boilerplate
    ]
    
    distances = [0.2, 0.4, 0.3, 0.9]  # FAISS distances
    question = "What is machine learning?"
    
    # Optimize context
    optimizer = ContextWindowOptimizer(max_context_tokens=300)
    optimized_context = optimizer.optimize_context(chunks, distances, question)
    
    print("Original token estimate:", sum(TextPruner().estimate_tokens(c) for c in chunks))
    print("Optimized token estimate:", TextPruner().estimate_tokens(optimized_context))
    print("\nOptimized context:")
    print(optimized_context)

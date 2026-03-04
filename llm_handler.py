"""
LLM Handler Module
Manages different LLM backends (Ollama, Hugging Face)
"""

from typing import List
import config


class LLMHandler:
    """Handle LLM interactions for answer generation"""
    
    def __init__(self, backend: str = "huggingface"):
        """
        Initialize LLM handler
        
        Args:
            backend: Either "ollama" or "huggingface"
        """
        self.backend = backend.lower()
        
        if self.backend == "ollama":
            try:
                import ollama
                self.ollama = ollama
            except ImportError:
                raise ImportError("Ollama not installed. Run: pip install ollama")
        
        elif self.backend == "huggingface":
            try:
                from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
                
                # Load model and tokenizer explicitly
                self.tokenizer = AutoTokenizer.from_pretrained(config.LLM_MODEL_HF)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(config.LLM_MODEL_HF)
                
                # Create pipeline with correct task name
                self.pipeline = pipeline(
                    "text2text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    max_length=512,
                    device=-1  # CPU
                )
            except ImportError:
                raise ImportError("Transformers not installed. Run: pip install transformers")
        else:
            raise ValueError(f"Unknown backend: {backend}. Use 'ollama' or 'huggingface'")
    
    def generate_answer(self, context_chunks: List[str], question: str) -> str:
        """
        Generate an answer using the LLM
        
        Args:
            context_chunks: List of relevant context chunks
            question: User's question
            
        Returns:
            Generated answer
        """
        context = "\n\n".join(context_chunks)
        prompt = self._create_prompt(context, question)
        
        if self.backend == "ollama":
            return self._generate_ollama(prompt)
        else:
            return self._generate_huggingface(prompt)
    
    def _create_prompt(self, context: str, question: str) -> str:
        """Create a prompt for the LLM"""
        return f"""Based on the following context, answer the question concisely and accurately.
If the answer cannot be found in the context, say "I cannot find this information in the provided document."

Context:
{context}

Question: {question}

Answer:"""
    
    def _generate_ollama(self, prompt: str) -> str:
        """Generate answer using Ollama"""
        try:
            response = self.ollama.chat(
                model=config.LLM_MODEL_OLLAMA,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response["message"]["content"]
        except Exception as e:
            return f"Error generating answer with Ollama: {str(e)}"
    
    def _generate_huggingface(self, prompt: str) -> str:
        """Generate answer using Hugging Face model"""
        try:
            result = self.pipeline(prompt, max_length=512, min_length=20)
            return result[0]["generated_text"]
        except Exception as e:
            return f"Error generating answer with Hugging Face: {str(e)}"

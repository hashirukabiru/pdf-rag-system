"""
LLM Handler Module
Manages different LLM backends (Ollama, Hugging Face)
Directly uses Model and Tokenizer to avoid Pipeline Task Errors
"""

from typing import List
import torch
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
                print(f"Ollama backend initialized with model: {config.LLM_MODEL_OLLAMA}")
            except ImportError:
                raise ImportError("Ollama not installed. Run: pip install ollama")
        
        elif self.backend == "huggingface":
            try:
                from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
                
                print(f"Loading Hugging Face model: {config.LLM_MODEL_HF}...")
                
                # Load model and tokenizer explicitly to avoid pipeline task KeyErrors
                self.tokenizer = AutoTokenizer.from_pretrained(config.LLM_MODEL_HF)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(config.LLM_MODEL_HF)
                
                # Set device to CPU
                self.device = torch.device("cpu")
                self.model.to(self.device)
                
                print("Hugging Face model loaded successfully!")
                
            except ImportError:
                raise ImportError("Transformers or Torch not installed. Run: pip install transformers torch")
            except Exception as e:
                raise Exception(f"Failed to load Hugging Face model: {str(e)}")
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
        # Combine context chunks into a single string
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
        """
        Generate answer using the model directly.
        This bypasses the 'pipeline' and avoids task-name errors.
        """
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512
            ).to(self.device)
            
            # Generate output
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                min_length=10,
                do_sample=False,  # Set to False for consistent, factual RAG results
                repetition_penalty=2.5
            )
            
            # Decode and return
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer if answer.strip() else "The model could not generate a clear answer."
            
        except Exception as e:
            return f"Error generating answer with Hugging Face: {str(e)}"

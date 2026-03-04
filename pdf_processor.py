"""
PDF Processing Module
Handles PDF loading, text extraction, and chunking
"""

import os
from typing import List
from pypdf import PdfReader
import config


class PDFProcessor:
    """Process PDF files and extract text"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP
    
    def load_pdf(self, file_path: str) -> str:
        """
        Load and extract text from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If no text could be extracted
            Exception: For other PDF reading errors
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Path is not a file: {file_path}")
        
        try:
            reader = PdfReader(file_path)
            
            if len(reader.pages) == 0:
                raise ValueError("PDF file has no pages")
            
            text = ""
            empty_pages = 0
            
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text += page_text + "\n"
                    else:
                        empty_pages += 1
                except Exception as page_error:
                    print(f"Warning: Could not extract text from page {page_num + 1}: {str(page_error)}")
                    empty_pages += 1
            
            if not text.strip():
                raise ValueError(f"No text could be extracted from the PDF. All {len(reader.pages)} pages appear to be empty or contain only images.")
            
            if empty_pages > 0:
                print(f"Note: {empty_pages} out of {len(reader.pages)} pages had no extractable text")
            
            return text
            
        except FileNotFoundError:
            raise
        except ValueError:
            raise
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
            
        Raises:
            ValueError: If text is empty or chunk_size is invalid
        """
        if not text:
            return []
        
        if self.chunk_size <= 0:
            raise ValueError(f"Invalid chunk_size: {self.chunk_size}. Must be positive.")
        
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(f"chunk_overlap ({self.chunk_overlap}) must be less than chunk_size ({self.chunk_size})")
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Only add non-empty chunks
            if chunk.strip():
                chunks.append(chunk.strip())
            
            # Move start position with overlap
            start += self.chunk_size - self.chunk_overlap
            
            # Prevent infinite loop
            if self.chunk_size - self.chunk_overlap <= 0:
                break
        
        return chunks
    
    def process_pdf(self, file_path: str) -> List[str]:
        """
        Complete pipeline: load PDF and chunk text
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of text chunks
        """
        text = self.load_pdf(file_path)
        chunks = self.chunk_text(text)
        return chunks

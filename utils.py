"""
Utility functions for validation, error handling, and helpers
"""

import os
from typing import Optional, Tuple
import config


def validate_file_path(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a file path
    
    Args:
        file_path: Path to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_path:
        return False, "No file path provided"
    
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"
    
    # Check file extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in config.ALLOWED_EXTENSIONS:
        return False, f"Invalid file type. Allowed: {', '.join(config.ALLOWED_EXTENSIONS)}"
    
    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > config.MAX_FILE_SIZE_MB:
        return False, f"File too large ({file_size_mb:.1f}MB). Max size: {config.MAX_FILE_SIZE_MB}MB"
    
    return True, None


def validate_question(question: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a question string
    
    Args:
        question: Question to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not question or not question.strip():
        return False, "Question cannot be empty"
    
    if len(question) < 3:
        return False, "Question too short (minimum 3 characters)"
    
    if len(question) > 1000:
        return False, "Question too long (maximum 1000 characters)"
    
    return True, None


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing special characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove path separators and special characters
    sanitized = re.sub(r'[^\w\s\-\.]', '', filename)
    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    return sanitized.strip()

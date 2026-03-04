"""
Configuration file for PDF RAG System
"""

import os

# Model settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_OLLAMA = "llama3.2:latest"
LLM_MODEL_HF = "google/flan-t5-small"  # Smaller model (77MB) - faster download, good quality

# Chunking settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval settings
TOP_K_CHUNKS = 3

# Token optimization settings
ENABLE_TOKEN_OPTIMIZATION = True  # ✅ Enabled for token reduction
MAX_CONTEXT_TOKENS = 600  # Maximum tokens for context (balanced setting)
RELEVANCE_THRESHOLD = 0.7  # Prune chunks with distance > this value

# Configuration profiles (see config_profiles.py for presets)
ACTIVE_PROFILE = "balanced"  # Options: balanced, speed, quality, minimal

# File settings
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = [".pdf"]

# Paths
DATA_DIR = "data"
UPLOAD_DIR = "uploads"

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

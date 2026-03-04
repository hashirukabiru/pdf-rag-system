# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-02-24

### Added
- Initial release of PDF RAG System
- PDF processing with text extraction and chunking
- Vector-based semantic search using FAISS
- Sentence Transformers for embeddings (all-MiniLM-L6-v2)
- Support for multiple LLM backends:
  - Hugging Face (Flan-T5-Large)
  - Ollama (Llama 3.2)
- Gradio web interface for easy interaction
- Command-line interface for batch processing
- Comprehensive error handling and validation
- Docker support for containerized deployment
- Full documentation and examples
- Type hints throughout codebase
- Configurable settings via config.py

### Features
- 📄 Upload and process PDF documents
- 🔍 Semantic search across document content
- 🤖 AI-powered answer generation
- 📊 View retrieved context chunks
- ⚙️ Adjustable retrieval parameters
- 🎨 Beautiful Gradio UI
- 🐳 Docker deployment ready
- 🤗 Hugging Face Spaces compatible

### Documentation
- Comprehensive README.md
- Deployment guide (DEPLOY.md)
- Contributing guidelines (CONTRIBUTING.md)
- Example usage scripts
- Test suite for validation

## [Unreleased]

### Planned Features
- Support for multiple PDFs simultaneously
- Conversation history tracking
- Document summarization feature
- Support for DOCX, TXT, and HTML formats
- Multi-language support
- Export Q&A history
- Fine-tuning options for embeddings
- Integration with OpenAI GPT models
- Improved chunking strategies (semantic chunking)
- Vector database integration (Pinecone, Weaviate)

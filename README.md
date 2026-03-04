# 📚 PDF Question Answering with RAG

A production-ready Retrieval-Augmented Generation (RAG) system that allows you to ask questions about PDF documents using semantic search and AI-powered answer generation.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **PDF Processing**: Extract and process text from PDF documents
- **Semantic Search**: Uses sentence transformers for intelligent text retrieval
- **Vector Search**: FAISS-based efficient similarity search
- **AI-Powered Answers**: Generate natural language answers using LLMs
- **Multiple Backends**: 
  - 🤗 Hugging Face (Flan-T5) - for cloud deployment
  - 🦙 Ollama (Llama 3.2) - for local deployment
- **Web Interface**: Beautiful Gradio UI for easy interaction
- **CLI Tool**: Command-line interface for batch processing
- **Production Ready**: Error handling, validation, and modular architecture

## 🏗️ Architecture

```
┌─────────────┐
│   PDF File  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ PDF Processor   │ ──► Text Extraction & Chunking
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vector Store    │ ──► Embeddings + FAISS Index
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ User Question   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Semantic Search │ ──► Retrieve Top-K Chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Handler    │ ──► Generate Answer
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Answer      │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- (Optional) Ollama installed for local LLM usage

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd pdf-rag-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the web interface**
```bash
python app.py
```

The Gradio interface will open in your browser at `http://localhost:7860`

## 💻 Usage

### Web Interface (Gradio)

1. Launch the app:
```bash
python app.py
```

2. Upload a PDF file
3. Click "Process PDF"
4. Ask questions about the document
5. View AI-generated answers with context

### Command Line Interface

For local usage with Ollama:

```bash
python cli.py path/to/your/document.pdf
```

With options:
```bash
python cli.py document.pdf --backend huggingface --top-k 5
```

### As a Python Module

```python
from rag_system import RAGSystem

# Initialize with Hugging Face backend
rag = RAGSystem(llm_backend="huggingface")

# Or use Ollama for local deployment
# rag = RAGSystem(llm_backend="ollama")

# Process a PDF
result = rag.load_and_process_pdf("path/to/document.pdf")
print(f"Processed {result['num_chunks']} chunks")

# Ask questions
answer = rag.answer_question("What is this document about?")
print(answer['answer'])
```

## 🤗 Deploy to Hugging Face Spaces

1. **Create a new Space** on [Hugging Face](https://huggingface.co/spaces)
   - Choose "Gradio" as the SDK
   - Select "Public" or "Private"

2. **Upload these files**:
   - `app.py`
   - `config.py`
   - `pdf_processor.py`
   - `vector_store.py`
   - `llm_handler.py`
   - `rag_system.py`
   - `requirements.txt`
   - `README.md`

3. **Your Space will automatically deploy!**

Alternatively, use the Hugging Face CLI:

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Push to Space
huggingface-cli upload your-username/pdf-rag-app . --repo-type space
```

## 📁 Project Structure

```
pdf-rag-system/
│
├── app.py                 # Gradio web interface (Hugging Face deployment)
├── cli.py                 # Command-line interface (local usage)
├── rag_system.py          # Main RAG orchestrator
├── pdf_processor.py       # PDF loading and chunking
├── vector_store.py        # Embeddings and FAISS indexing
├── llm_handler.py         # LLM backend management
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
│
├── test_pdf_read.py      # Original test script (kept for reference)
│
└── data/                 # Sample data folder
    └── sample.pdf        # Example PDF
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Model settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_OLLAMA = "llama3.2:latest"
LLM_MODEL_HF = "google/flan-t5-large"

# Chunking settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval settings
TOP_K_CHUNKS = 3
```

## 🔧 How It Works

1. **PDF Processing**: Extracts text from uploaded PDFs and splits into overlapping chunks
2. **Embedding Creation**: Converts text chunks into vector embeddings using Sentence Transformers
3. **Vector Indexing**: Stores embeddings in a FAISS index for fast similarity search
4. **Query Processing**: When you ask a question, it's converted to an embedding
5. **Retrieval**: FAISS finds the most similar chunks to your question
6. **Answer Generation**: The LLM generates a natural language answer using the retrieved context

## 📊 Performance

- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Vector Search**: FAISS L2 distance
- **LLM Options**:
  - Flan-T5-Large (780M parameters) - Cloud
  - Llama 3.2 - Local with Ollama

## 🛠️ Development

### Run Tests

```bash
# Process a sample PDF
python test_pdf_read.py
```

### Local Development with Ollama

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model:
```bash
ollama pull llama3.2
```

3. Run with Ollama backend:
```bash
python cli.py data/sample.pdf --backend ollama
```

## 📝 License

MIT License - feel free to use this project for any purpose!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

## 🎯 Roadmap

- [ ] Add support for multiple PDFs
- [ ] Implement conversation history
- [ ] Add document summarization
- [ ] Support for other document formats (DOCX, TXT)
- [ ] Fine-tuning options for embeddings
- [ ] Export Q&A history
- [ ] Multi-language support

## ⭐ Acknowledgments

- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [FAISS](https://github.com/facebookresearch/faiss) for vector search
- [Gradio](https://gradio.app/) for the web interface
- [Hugging Face](https://huggingface.co/) for model hosting
- [Ollama](https://ollama.ai/) for local LLM deployment

---

Made with ❤️ for the AI community

# 🚀 Quick Start Guide

Get started with the PDF RAG System in just a few minutes!

## 📦 Installation

### Option 1: Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-rag-system.git
cd pdf-rag-system

# Install dependencies
pip install -r requirements.txt

# Run the web interface
python app.py
```

Open your browser to `http://localhost:7860` and you're ready to go! 🎉

### Option 2: Using Docker

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-rag-system.git
cd pdf-rag-system

# Run with Docker Compose
docker-compose up
```

Access the app at `http://localhost:7860`

### Option 3: Command Line Only

```bash
# Install dependencies
pip install -r requirements.txt

# Run with a PDF file
python cli.py path/to/your/document.pdf
```

## 🎯 First Steps

### 1. Using the Web Interface

1. **Upload a PDF**
   - Click "Browse" and select your PDF file
   - Click "Process PDF"
   - Wait for processing to complete

2. **Ask Questions**
   - Type your question in the text box
   - Click "Ask Question" or press Enter
   - View the AI-generated answer

3. **Adjust Settings** (Optional)
   - Use the slider to change how many context chunks to retrieve
   - More chunks = more context but slower response

### 2. Using the Command Line

```bash
# Basic usage
python cli.py data/sample.pdf

# Then ask questions interactively
> What is this document about?
> What are the main topics?
> Type 'quit' to exit
```

### 3. Using as a Python Library

```python
from rag_system import RAGSystem

# Initialize
rag = RAGSystem(llm_backend="huggingface")

# Process PDF
result = rag.load_and_process_pdf("document.pdf")
print(f"Processed {result['num_chunks']} chunks")

# Ask questions
answer = rag.answer_question("What is the main topic?")
print(answer['answer'])
```

## 🎓 Example Workflow

Here's a complete example:

```python
from rag_system import RAGSystem

# Step 1: Initialize the system
rag = RAGSystem(llm_backend="huggingface")

# Step 2: Load your PDF
pdf_path = "data/sample.pdf"
result = rag.load_and_process_pdf(pdf_path)

if result["success"]:
    print(f"✓ Ready! Processed {result['num_chunks']} chunks")
    
    # Step 3: Ask questions
    questions = [
        "What is this document about?",
        "Who are the authors?",
        "What are the key findings?"
    ]
    
    for question in questions:
        answer = rag.answer_question(question, top_k=3)
        print(f"\nQ: {question}")
        print(f"A: {answer['answer']}\n")
else:
    print(f"Error: {result['message']}")
```

## ⚙️ Configuration

### Change the LLM Model

Edit `config.py`:

```python
# For Hugging Face
LLM_MODEL_HF = "google/flan-t5-base"  # Smaller, faster
# or
LLM_MODEL_HF = "google/flan-t5-xxl"   # Larger, better quality

# For Ollama (requires local installation)
LLM_MODEL_OLLAMA = "llama3.2:latest"
```

### Adjust Chunking

```python
# In config.py
CHUNK_SIZE = 500      # Characters per chunk
CHUNK_OVERLAP = 50    # Overlap between chunks
TOP_K_CHUNKS = 3      # Number of chunks to retrieve
```

## 🔧 Troubleshooting

### Problem: "Out of memory" error

**Solution:**
- Use a smaller model (e.g., `flan-t5-base` instead of `flan-t5-large`)
- Reduce `CHUNK_SIZE` in `config.py`
- Reduce `TOP_K_CHUNKS`

### Problem: Slow response times

**Solution:**
- Use a smaller model
- Reduce `TOP_K_CHUNKS`
- Consider using GPU if available
- Use Ollama with local models

### Problem: PDF not processing

**Solution:**
- Ensure PDF contains extractable text (not just images)
- Check PDF file size (max 50MB by default)
- Try a different PDF to verify the system works

### Problem: Poor answer quality

**Solution:**
- Increase `TOP_K_CHUNKS` for more context
- Use a larger model
- Ensure your question is clear and specific
- Check that the PDF contains relevant information

## 📚 Next Steps

- Read the [full README](README.md) for detailed documentation
- Check out [DEPLOY.md](DEPLOY.md) for deployment options
- See [examples.py](examples.py) for more usage examples
- Join our community (add Discord/Slack link)

## 💡 Tips

- **Better Questions**: Ask specific questions for better answers
- **Context Matters**: More relevant chunks = better answers
- **Test First**: Use the test script to verify everything works
  ```bash
  python test_system.py
  ```
- **Start Small**: Test with small PDFs first
- **Read Logs**: Check console output for helpful information

## 🆘 Need Help?

- 📖 Check the [full documentation](README.md)
- 🐛 [Report bugs](https://github.com/yourusername/pdf-rag-system/issues)
- 💬 Ask questions in [Discussions](https://github.com/yourusername/pdf-rag-system/discussions)
- ✉️ Email: support@example.com

---

Happy questioning! 🎉

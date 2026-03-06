---
title: PDF Question Answering RAG System
emoji: 📄
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app_hf.py
pinned: false
license: mit
---

# 📄 PDF Question Answering System

## 🚀 Try it Now!

Upload any PDF document and ask questions about its content using AI-powered semantic search!

## ✨ Features

- 📤 **Upload PDFs** - Supports any PDF document
- 🔍 **Semantic Search** - Uses sentence embeddings for intelligent matching
- ⚡ **Fast Retrieval** - FAISS vector similarity search
- 🎯 **Relevant Results** - Get the most relevant sections from your document
- 🎨 **User-Friendly** - Simple, intuitive interface

## 🛠️ How It Works

1. **Upload** your PDF document
2. **Process** - The app splits it into chunks and creates embeddings
3. **Ask** any question about the content
4. **Get** relevant excerpts from the document

## 🔧 Technology Stack

- **Gradio** - Interactive web interface
- **Sentence Transformers** - State-of-the-art text embeddings (all-MiniLM-L6-v2)
- **FAISS** - Fast vector similarity search
- **PyPDF** - PDF text extraction

## 💡 Example Questions

Try asking:
- "What is the main topic of this document?"
- "Summarize the key points"
- "What does it say about [specific topic]?"
- "List the important details"

## 🎯 Use Cases

- 📚 Research papers analysis
- 📋 Document Q&A
- 📖 Study material queries
- 📝 Report summarization
- 🔎 Information extraction

## 🚀 Local Development

```bash
git clone <your-repo>
cd pdf-rag-system
pip install -r requirements_hf.txt
python app_hf.py
```

## 📝 License

MIT License - Feel free to use and modify!

## 👨‍💻 Author

Built with ❤️ using Gradio and Hugging Face Spaces

---

**Note:** This is a retrieval-based system. It finds and displays relevant sections from your PDF rather than generating new text.

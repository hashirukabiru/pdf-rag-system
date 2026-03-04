# Contributing to PDF RAG System

Thank you for your interest in contributing to the PDF RAG System! We welcome contributions from the community.

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/pdf-rag-system.git
   cd pdf-rag-system
   ```
3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Development Workflow

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow Python PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Include type hints where appropriate

3. **Test your changes**
   ```bash
   python test_system.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Describe your changes clearly

## 📝 Code Style

- Use **4 spaces** for indentation
- Maximum line length: **100 characters**
- Use **meaningful variable names**
- Add **comments** for complex logic
- Write **docstrings** for all public functions

Example:
```python
def process_document(file_path: str, chunk_size: int = 500) -> List[str]:
    """
    Process a document and return chunks.
    
    Args:
        file_path: Path to the document file
        chunk_size: Size of each text chunk (default: 500)
        
    Returns:
        List of text chunks
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    # Implementation here
    pass
```

## 🧪 Testing

Before submitting a PR, ensure:
- [ ] All existing tests pass
- [ ] New features have tests
- [ ] Code is documented
- [ ] No unnecessary dependencies added

## 🐛 Reporting Bugs

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## 💡 Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Clearly describe the use case
- Explain why it would be beneficial

## 📋 Areas for Contribution

We especially welcome contributions in:
- [ ] Additional LLM backend support (OpenAI, Claude, etc.)
- [ ] Support for other document formats (DOCX, TXT, HTML)
- [ ] Improved chunking strategies
- [ ] Multi-language support
- [ ] Performance optimizations
- [ ] Better error handling
- [ ] Documentation improvements
- [ ] UI/UX enhancements

## 🙏 Thank You!

Your contributions make this project better for everyone!

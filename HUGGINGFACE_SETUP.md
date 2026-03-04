# 🤗 Hugging Face Spaces Deployment Guide

Deploy your PDF RAG System to Hugging Face Spaces in minutes!

## 🎯 Overview

Hugging Face Spaces provides free hosting for ML apps with Gradio. This guide shows you how to deploy the PDF RAG System.

## 📋 Prerequisites

- A Hugging Face account (free at [huggingface.co](https://huggingface.co))
- Git installed on your computer
- Basic familiarity with Git

## 🚀 Method 1: Web Interface (Easiest)

### Step 1: Create a New Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in the details:
   - **Owner**: Your username
   - **Space name**: `pdf-rag-qa` (or any name you prefer)
   - **License**: MIT
   - **Select SDK**: Gradio
   - **Space hardware**: CPU basic (free tier)
   - **Visibility**: Public or Private

3. Click **Create Space**

### Step 2: Upload Files

In your Space, click **Files** → **Add file** → **Upload files**

Upload these files:
```
✓ app.py
✓ config.py
✓ pdf_processor.py
✓ vector_store.py
✓ llm_handler.py
✓ rag_system.py
✓ requirements.txt
✓ README.md
```

### Step 3: Wait for Build

- Your Space will automatically build (takes 2-5 minutes)
- Watch the build logs at the bottom of the page
- Once complete, your app will be live!

### Step 4: Test Your Space

- Click on your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/pdf-rag-qa`
- Upload a test PDF
- Ask questions!

## 🚀 Method 2: Git (Recommended for Developers)

### Step 1: Create Space (as above)

Follow Step 1 from Method 1

### Step 2: Clone Your Space

```bash
# Install Git LFS (if not already installed)
git lfs install

# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/pdf-rag-qa
cd pdf-rag-qa
```

### Step 3: Copy Project Files

```bash
# Copy all necessary files
cp ../path/to/pdf-rag-system/app.py .
cp ../path/to/pdf-rag-system/config.py .
cp ../path/to/pdf-rag-system/pdf_processor.py .
cp ../path/to/pdf-rag-system/vector_store.py .
cp ../path/to/pdf-rag-system/llm_handler.py .
cp ../path/to/pdf-rag-system/rag_system.py .
cp ../path/to/pdf-rag-system/requirements.txt .
cp ../path/to/pdf-rag-system/README.md .
```

### Step 4: Commit and Push

```bash
git add .
git commit -m "Initial deployment"
git push
```

### Step 5: Monitor Build

- Go to your Space URL
- Watch the build progress
- Test once complete!

## 🚀 Method 3: Using Hugging Face CLI

### Step 1: Install HF CLI

```bash
pip install huggingface_hub[cli]
```

### Step 2: Login

```bash
huggingface-cli login
```

Enter your Hugging Face token (get it from [Settings](https://huggingface.co/settings/tokens))

### Step 3: Create and Push

```bash
# Create the Space
huggingface-cli repo create pdf-rag-qa --type space --space_sdk gradio

# Navigate to your project
cd pdf-rag-system

# Push files
huggingface-cli upload YOUR_USERNAME/pdf-rag-qa . --repo-type space
```

## ⚙️ Configuration for Hugging Face

### Optimize for CPU

In `config.py`, ensure you're using CPU-friendly settings:

```python
# Use smaller model for free tier
LLM_MODEL_HF = "google/flan-t5-base"  # Faster on CPU

# Adjust chunk settings for performance
CHUNK_SIZE = 400
TOP_K_CHUNKS = 2
```

### Add Space Metadata

Create a `README.md` header for your Space:

```markdown
---
title: PDF Question Answering
emoji: 📚
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.19.2
app_file: app.py
pinned: false
license: mit
---

# PDF Question Answering System

[Your README content here]
```

## 🔧 Troubleshooting

### Build Fails

**Check logs for errors:**
- Missing dependencies? Update `requirements.txt`
- Python version issues? Spaces use Python 3.10
- File not found? Ensure all files are uploaded

### Out of Memory

**Solutions:**
- Use `flan-t5-small` or `flan-t5-base` instead of `large`
- Reduce `CHUNK_SIZE` and `TOP_K_CHUNKS`
- Consider upgrading to a paid tier with more RAM

### Slow Performance

**Optimize:**
- Use smaller models
- Reduce number of chunks retrieved
- Enable caching for embeddings
- Consider using a paid tier with better hardware

### App Not Responding

**Check:**
- View logs in Space settings
- Verify all files are present
- Test locally first with `python app.py`

## 🎨 Customizing Your Space

### Change Theme

In `app.py`:

```python
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    # Options: Soft(), Monochrome(), Glass(), Base()
```

### Add Examples

```python
gr.Examples(
    examples=[
        "What is this document about?",
        "Summarize the main points",
        "Who are the authors?"
    ],
    inputs=question_input
)
```

### Add Analytics

Enable in Space Settings → "Enable Analytics"

## 📊 Hardware Options

| Tier | RAM | Price | Best For |
|------|-----|-------|----------|
| CPU basic | 16GB | Free | Testing, demos |
| CPU upgrade | 32GB | $0.60/hr | Production |
| T4 small (GPU) | 16GB | $0.60/hr | Faster inference |
| A10G small (GPU) | 24GB | $1.05/hr | Large models |

## 🔒 Private Spaces

For sensitive documents:
1. Set Space visibility to "Private"
2. Only you can access it
3. Share with specific users via Settings

## 🌐 Custom Domain

1. Go to Space Settings
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## 📈 Monitoring

View your Space analytics:
- Number of visitors
- Usage patterns
- Popular questions
- Performance metrics

Access via: Space Settings → Analytics

## 🎓 Next Steps

After deployment:
- [ ] Test with various PDFs
- [ ] Share with users for feedback
- [ ] Monitor performance
- [ ] Optimize based on usage
- [ ] Consider upgrading hardware if needed

## 🆘 Support

- [Hugging Face Docs](https://huggingface.co/docs/hub/spaces)
- [Gradio Docs](https://gradio.app/docs)
- [Community Forum](https://discuss.huggingface.co/)

---

Enjoy your deployed PDF RAG System! 🎉

# 🧪 Local Testing Guide

## Your Sample PDF
✅ You have: `data/sample.pdf` - "Python for LLM Engineering — Full Roadmap"

This is perfect for testing! It contains:
- 13 sections about Python and LLM topics
- Clear structure with bullet points
- Technical content ideal for Q&A testing

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies (if not done)
```bash
pip install -r requirements.txt
```

⏱️ **Time:** 2-5 minutes (downloads models ~1GB)

### Step 2: Start the App
**On Windows:**
```bash
run_app.bat
```

**On Mac/Linux:**
```bash
chmod +x run_app.sh
./run_app.sh
```

**Or directly:**
```bash
python app.py
```

### Step 3: Use the App
1. Browser will auto-open to `http://localhost:7860`
2. Click "Upload PDF Document" and select `data/sample.pdf`
3. Click "📤 Process PDF"
4. Wait for "✅ PDF Processed Successfully!"
5. Ask a question like: "What topics are covered in this roadmap?"

---

## 🎯 Sample Questions to Try

After uploading `sample.pdf`, try these questions:

### **Basic Questions:**
- "What is this document about?"
- "List all the Python topics mentioned"
- "What tools are mentioned for LLM engineering?"

### **Specific Questions:**
- "What topics are covered in the advanced Python section?"
- "Which tools are mentioned for working with LLMs?"
- "What are the final project suggestions?"

### **Testing Token Optimization:**
- Try changing "Number of chunks to retrieve" slider (1-10)
- Notice how response changes with different chunk counts
- Check the retrieved context section

---

## 📊 What You'll See

### **Processing Status:**
```
✅ PDF Processed Successfully!

📄 File: sample.pdf
💾 Size: 0.XX MB
📊 Chunks Created: 2-4 (depends on chunk size)
📏 Chunk Size: 500 characters

You can now ask questions about the document!
```

### **Sample Answer Format:**
```
### 🤖 Answer:
This roadmap covers 13 Python topics for LLM Engineering, 
from basics to advanced topics including...

---
### 📚 Retrieved Context (3 chunks):

**Chunk 1** (relevance score: 0.234):
```
Python for LLM Engineering — Full Roadmap
This roadmap outlines all Python topics...
```
```

---

## ⚙️ Configuration Options

### **Adjust Token Optimization:**
Edit `config.py`:
```python
ENABLE_TOKEN_OPTIMIZATION = True   # Enable/disable
MAX_CONTEXT_TOKENS = 600          # Adjust token budget
TOP_K_CHUNKS = 3                  # Default chunks to retrieve
```

### **Change Chunk Size:**
```python
CHUNK_SIZE = 500       # Smaller = more precise, more chunks
CHUNK_OVERLAP = 50     # Overlap between chunks
```

---

## 🐛 Troubleshooting

### **Model Download Takes Long:**
- First run downloads ~1GB (Flan-T5 model)
- Progress bar will show in terminal
- Subsequent runs are instant (model cached)

### **Out of Memory:**
- Use smaller model: `config.py` → `LLM_MODEL_HF = "google/flan-t5-base"`
- Or reduce chunk size: `CHUNK_SIZE = 300`

### **Port Already in Use:**
- Change port: `python app.py` will auto-find free port
- Or manually: modify `app.py` line 183 to `demo.launch(server_port=7861)`

### **Import Errors:**
```bash
pip install --upgrade -r requirements.txt
```

---

## ✅ Success Indicators

You'll know it's working when you see:

1. ✅ Terminal shows: "Running on local URL: http://127.0.0.1:7860"
2. ✅ Browser opens automatically
3. ✅ You can upload and process the PDF
4. ✅ Questions return relevant answers with context

---

## 📈 Performance Expectations

| Operation | Time | Notes |
|-----------|------|-------|
| First startup | 1-3 min | Downloads model |
| Subsequent startups | 5-10 sec | Model cached |
| PDF processing (sample.pdf) | 2-5 sec | Creates embeddings |
| Answer generation | 2-10 sec | Depends on hardware |

---

## 🎯 What to Check

### ✅ **Core Functionality:**
- [ ] PDF uploads successfully
- [ ] Processing shows chunk count
- [ ] Questions return relevant answers
- [ ] Context chunks are displayed
- [ ] System reset works

### ✅ **Token Optimization:**
- [ ] Token stats appear (if enabled)
- [ ] Changing top_k affects results
- [ ] Retrieved chunks are relevant
- [ ] Answers are coherent

### ✅ **UI Features:**
- [ ] Gradio interface loads
- [ ] All buttons work
- [ ] Sliders adjust settings
- [ ] Accordion expands/collapses

---

## 🚦 Next Steps After Testing

### **If Everything Works:**
1. ✅ Mark validation as complete
2. 🚀 Ready to deploy to HuggingFace
3. 💻 Ready to push to GitHub
4. 🎉 Your project is production-ready!

### **If You Find Issues:**
1. Check error messages in terminal
2. Verify all dependencies installed
3. Run `python validate_deployment.py`
4. Let me know the specific error!

---

## 💡 Pro Tips

1. **Keep terminal open** to see processing logs
2. **Use specific questions** for better answers
3. **Adjust top_k slider** to see how context affects answers
4. **Check "View Retrieved Context"** to see what was used
5. **Try token optimization** by toggling it in config.py

---

## 🎊 Ready to Test!

Run this now:
```bash
python app.py
```

Then come back and tell me:
- ✅ Did it start successfully?
- ✅ Could you upload the PDF?
- ✅ Did questions work?
- ❌ Any errors?

I'm here to help troubleshoot! 🚀

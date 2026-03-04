# Network Issues - Alternative Solutions

## Problem
The Flan-T5 Large model (890MB) failed to download due to network issues.

## Solutions (in order of preference)

### ✅ Solution 1: Use Smaller Model (RECOMMENDED - ALREADY APPLIED)
We've switched to `flan-t5-small` which is only 77MB (11x smaller!)

**Benefits:**
- Downloads in 30 seconds instead of 5+ minutes
- Still gives good quality answers
- Much more reliable on unstable networks

**Try again:**
```bash
python app.py
```

---

### ✅ Solution 2: Use Ollama (Local LLM - No Download)
If you have Ollama installed locally, use the CLI version:

```bash
# Start Ollama first
ollama serve

# In another terminal
python cli.py
```

This works 100% locally with no internet needed!

---

### ✅ Solution 3: Use Different HuggingFace Model
Edit `config.py` and try one of these:

```python
# Ultra-light (28MB) - very fast
LLM_MODEL_HF = "google/flan-t5-base"

# Tiny (60MB) - fastest
LLM_MODEL_HF = "t5-small"

# Already set (77MB) - good balance
LLM_MODEL_HF = "google/flan-t5-small"
```

---

### ✅ Solution 4: Improve Network Stability

**If you want to use the large model:**

1. **Use mobile hotspot** (sometimes more stable)
2. **Disable VPN** (if using one)
3. **Close other downloads/streams**
4. **Try at different time** (less network congestion)
5. **Use ethernet** instead of WiFi

Then change back to:
```python
LLM_MODEL_HF = "google/flan-t5-large"
```

---

## Current Configuration
✅ Already switched to `flan-t5-small` (77MB)
✅ Should download in under 1 minute
✅ Works great for PDF Q&A

**Just run:** `python app.py`

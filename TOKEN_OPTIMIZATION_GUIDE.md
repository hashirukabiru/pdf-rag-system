# 🎯 Token Optimization Guide for RAG Systems

A comprehensive guide to reducing token consumption in your PDF RAG system.

## 📊 Why Optimize Tokens?

- **Cost**: LLM APIs charge per token
- **Speed**: Fewer tokens = faster responses
- **Quality**: More focused context = better answers
- **Limits**: Stay within model context windows

## 🔧 Optimization Strategies

### 1️⃣ **Reduce Retrieved Chunks**

**Easiest and most effective!**

```python
# In config.py - reduce from 3 to 2 chunks
TOP_K_CHUNKS = 2  # Default was 3

# Or in code
answer = rag.answer_question("What is this about?", top_k=2)
```

**Impact**: 33% reduction in context tokens

### 2️⃣ **Smaller Chunk Sizes**

```python
# In config.py
CHUNK_SIZE = 300  # Reduced from 500
CHUNK_OVERLAP = 25  # Reduced from 50
```

**Impact**: 40% reduction per chunk

### 3️⃣ **Relevance-Based Pruning**

Filter chunks by relevance score:

```python
from pruning_strategies import TextPruner

# Only keep highly relevant chunks
pruner = TextPruner()
filtered_chunks, filtered_distances = pruner.prune_by_relevance_score(
    chunks, 
    distances,
    threshold=0.5  # Lower = more strict
)
```

**Impact**: Variable, removes low-quality matches

### 4️⃣ **Token Budget Limiting**

Set a hard token limit:

```python
from pruning_strategies import TextPruner

pruner = TextPruner()
pruned_chunks = pruner.prune_by_token_limit(
    chunks,
    max_total_tokens=500  # Total budget
)
```

**Impact**: Guaranteed to stay under limit

### 5️⃣ **Remove Redundancy**

Eliminate similar chunks:

```python
from pruning_strategies import TextPruner

pruner = TextPruner()
unique_chunks = pruner.remove_redundant_content(chunks)
```

**Impact**: 10-30% reduction depending on document

### 6️⃣ **Extract Key Sentences**

Get only the most relevant sentences:

```python
from pruning_strategies import TextPruner

pruner = TextPruner()
key_content = pruner.extract_key_sentences(
    chunk,
    question="What is machine learning?",
    max_sentences=3
)
```

**Impact**: 50-70% reduction per chunk

### 7️⃣ **Remove Boilerplate**

Clean up headers, footers, copyright notices:

```python
from pruning_strategies import TextPruner

pruner = TextPruner()
cleaned = pruner.remove_boilerplate(text)
cleaned = pruner.compress_whitespace(cleaned)
```

**Impact**: 5-15% reduction

### 8️⃣ **Use Context Window Optimizer**

Combine all strategies:

```python
from pruning_strategies import ContextWindowOptimizer

optimizer = ContextWindowOptimizer(max_context_tokens=500)
optimized_context = optimizer.optimize_context(chunks, distances, question)
```

**Impact**: 40-60% total reduction

## 🔄 Integration with Your RAG System

### Option 1: Update `vector_store.py`

Add pruning to the search method:

```python
# In vector_store.py
from pruning_strategies import TextPruner

def search(self, query: str, top_k: int = None) -> Tuple[List[str], List[float]]:
    # ... existing search code ...
    
    # Add pruning
    pruner = TextPruner()
    top_chunks, distances = pruner.prune_by_relevance_score(
        top_chunks, 
        distances,
        threshold=0.7  # Adjust as needed
    )
    
    return top_chunks, distances
```

### Option 2: Update `rag_system.py`

Add optimization before LLM call:

```python
# In rag_system.py
from pruning_strategies import ContextWindowOptimizer

def answer_question(self, question: str, top_k: int = None) -> Dict[str, any]:
    # ... existing retrieval code ...
    chunks, distances = self.vector_store.search(question, top_k=top_k)
    
    # Add optimization
    optimizer = ContextWindowOptimizer(max_context_tokens=800)
    optimized_chunks = optimizer.optimize_context(chunks, distances, question)
    
    # Generate answer with optimized context
    answer = self.llm_handler.generate_answer([optimized_chunks], question)
    # ...
```

### Option 3: Update `config.py`

Add optimization settings:

```python
# In config.py

# Token optimization settings
ENABLE_PRUNING = True
MAX_CONTEXT_TOKENS = 800
RELEVANCE_THRESHOLD = 0.6
REMOVE_REDUNDANCY = True
EXTRACT_KEY_SENTENCES = False  # More aggressive
```

## 📈 Token Reduction Examples

### Before Optimization:
```
Chunks: 3
Chunk size: 500 chars
Total tokens: ~375 tokens
```

### After Basic Optimization:
```python
TOP_K_CHUNKS = 2
CHUNK_SIZE = 300
# Total tokens: ~150 tokens (60% reduction)
```

### After Advanced Optimization:
```python
# Use ContextWindowOptimizer
optimizer = ContextWindowOptimizer(max_context_tokens=300)
# Total tokens: ~100 tokens (73% reduction)
```

## 🎯 Recommended Settings by Use Case

### ⚡ Speed Priority (Minimal tokens)
```python
TOP_K_CHUNKS = 1
CHUNK_SIZE = 250
MAX_CONTEXT_TOKENS = 300
EXTRACT_KEY_SENTENCES = True
```

### ⚖️ Balanced (Good quality, reasonable cost)
```python
TOP_K_CHUNKS = 2
CHUNK_SIZE = 400
MAX_CONTEXT_TOKENS = 600
REMOVE_REDUNDANCY = True
```

### 🎯 Quality Priority (Best answers)
```python
TOP_K_CHUNKS = 5
CHUNK_SIZE = 500
MAX_CONTEXT_TOKENS = 1500
RELEVANCE_THRESHOLD = 0.8
```

### 💰 Cost Priority (Minimum API costs)
```python
TOP_K_CHUNKS = 1
CHUNK_SIZE = 200
MAX_CONTEXT_TOKENS = 250
EXTRACT_KEY_SENTENCES = True
REMOVE_REDUNDANCY = True
```

## 📊 Monitoring Token Usage

### Add Token Counting:

```python
# Install tiktoken for accurate counting
# pip install tiktoken

import tiktoken

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count actual tokens for a model"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Use in your RAG system
context = "\n\n".join(chunks)
prompt = f"Context: {context}\n\nQuestion: {question}"
token_count = count_tokens(prompt)
print(f"Total tokens: {token_count}")
```

## 🔍 Quality vs Token Trade-offs

| Strategy | Token Reduction | Quality Impact | Speed Impact |
|----------|----------------|----------------|--------------|
| Reduce chunks | High (30%+) | Medium | High ⚡ |
| Smaller chunks | High (40%+) | Low-Medium | Medium |
| Relevance pruning | Variable | None-Low ✅ | Low |
| Token budget | Guaranteed | Medium | Low |
| Remove redundancy | Medium (20%) | None ✅ | Low |
| Key sentences | Very High (60%+) | Medium-High | Medium |
| Boilerplate removal | Low (10%) | None ✅ | Low |

✅ = Recommended (good trade-off)

## 🚀 Quick Implementation

### Add to your existing system:

```python
# 1. Copy pruning_strategies.py to your project

# 2. Update rag_system.py
from pruning_strategies import ContextWindowOptimizer

class RAGSystem:
    def __init__(self, llm_backend: str = "huggingface"):
        # ... existing code ...
        self.optimizer = ContextWindowOptimizer(max_context_tokens=800)
    
    def answer_question(self, question: str, top_k: int = None) -> Dict[str, any]:
        # ... existing retrieval ...
        chunks, distances = self.vector_store.search(question, top_k=top_k)
        
        # OPTIMIZE CONTEXT
        optimized_context = self.optimizer.optimize_context(
            chunks, distances, question
        )
        
        # Generate answer
        answer = self.llm_handler.generate_answer([optimized_context], question)
        # ...
```

## 💡 Pro Tips

1. **Start Conservative**: Begin with `TOP_K_CHUNKS = 2` and adjust
2. **Monitor Quality**: Track answer quality as you optimize
3. **A/B Test**: Compare optimized vs non-optimized responses
4. **Document-Specific**: Dense documents may need more chunks
5. **Question-Specific**: Complex questions may need more context

## 🧪 Testing Token Optimization

```python
# test_token_optimization.py
from pruning_strategies import ContextWindowOptimizer, TextPruner

# Test data
chunks = ["Test chunk 1" * 100, "Test chunk 2" * 100, "Test chunk 3" * 100]
distances = [0.2, 0.4, 0.6]
question = "What is the main topic?"

# Measure before
pruner = TextPruner()
before_tokens = sum(pruner.estimate_tokens(c) for c in chunks)

# Optimize
optimizer = ContextWindowOptimizer(max_context_tokens=500)
optimized = optimizer.optimize_context(chunks, distances, question)
after_tokens = pruner.estimate_tokens(optimized)

print(f"Before: {before_tokens} tokens")
print(f"After: {after_tokens} tokens")
print(f"Reduction: {((before_tokens - after_tokens) / before_tokens * 100):.1f}%")
```

## 📚 Additional Resources

- **tiktoken**: Accurate token counting for OpenAI models
- **spaCy**: Advanced sentence extraction
- **NLTK**: Text processing and summarization
- **TextRank**: Extractive summarization algorithm

---

**Remember**: The goal is to reduce tokens while maintaining answer quality. Always test your optimizations!

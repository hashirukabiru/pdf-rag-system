"""
Simple token optimization test - No model download required!
Tests the pruning logic directly
"""

from pruning_strategies import TextPruner, ContextWindowOptimizer
import config


def test_pruning_strategies():
    """Test token optimization strategies"""
    
    print("=" * 70)
    print("🧪 TESTING TOKEN OPTIMIZATION STRATEGIES")
    print("=" * 70)
    
    # Sample chunks (like what FAISS would return)
    chunks = [
        """Machine learning is a subset of artificial intelligence that enables 
        computers to learn from data without being explicitly programmed. It uses 
        algorithms to identify patterns and make decisions. Machine learning has 
        applications in various fields including healthcare, finance, and technology.
        The main types are supervised learning, unsupervised learning, and 
        reinforcement learning.""",
        
        """Deep learning is a specialized form of machine learning that uses neural 
        networks with multiple layers. These networks can process complex patterns 
        in large amounts of data. Deep learning has revolutionized fields like 
        computer vision and natural language processing. It requires significant 
        computational resources and large datasets.""",
        
        """Neural networks are computing systems inspired by biological neural networks.
        They consist of interconnected nodes called neurons that process information.
        Neural networks can learn to perform tasks by analyzing training examples.
        They are particularly good at pattern recognition and classification tasks.
        Modern neural networks can have millions of parameters.""",
        
        """Copyright 2024. All rights reserved. Page 1 of 100. 
        This document is confidential and proprietary.""",  # Boilerplate
        
        """Artificial intelligence is transforming many industries. It enables 
        automation of complex tasks and data analysis at scale. AI systems can 
        process information faster than humans in many cases."""
    ]
    
    # FAISS distances (lower = more relevant)
    distances = [0.15, 0.25, 0.30, 0.85, 0.40]
    
    question = "What is machine learning and deep learning?"
    
    pruner = TextPruner()
    
    # Calculate original token count
    original_tokens = sum(pruner.estimate_tokens(c) for c in chunks)
    
    print(f"\n📊 ORIGINAL DATA:")
    print(f"   Chunks: {len(chunks)}")
    print(f"   Total estimated tokens: ~{original_tokens}")
    print(f"   Average per chunk: ~{original_tokens // len(chunks)}")
    
    # Test 1: Relevance Pruning
    print("\n" + "=" * 70)
    print("TEST 1: Relevance-Based Pruning")
    print("=" * 70)
    
    pruned_chunks, pruned_distances = pruner.prune_by_relevance_score(
        chunks, distances, threshold=0.5
    )
    
    pruned_tokens = sum(pruner.estimate_tokens(c) for c in pruned_chunks)
    reduction = ((original_tokens - pruned_tokens) / original_tokens * 100)
    
    print(f"✓ Threshold: 0.5 (keep only highly relevant)")
    print(f"✓ Chunks kept: {len(pruned_chunks)} / {len(chunks)}")
    print(f"✓ Tokens: ~{pruned_tokens} (was ~{original_tokens})")
    print(f"✓ Reduction: {reduction:.1f}%")
    
    # Test 2: Remove Redundancy
    print("\n" + "=" * 70)
    print("TEST 2: Remove Redundant Content")
    print("=" * 70)
    
    unique_chunks = pruner.remove_redundant_content(chunks[:3])  # First 3 chunks
    unique_tokens = sum(pruner.estimate_tokens(c) for c in unique_chunks)
    
    print(f"✓ Original chunks: 3")
    print(f"✓ After deduplication: {len(unique_chunks)}")
    print(f"✓ Tokens saved: ~{sum(pruner.estimate_tokens(c) for c in chunks[:3]) - unique_tokens}")
    
    # Test 3: Remove Boilerplate
    print("\n" + "=" * 70)
    print("TEST 3: Remove Boilerplate")
    print("=" * 70)
    
    boilerplate_chunk = chunks[3]
    cleaned = pruner.remove_boilerplate(boilerplate_chunk)
    cleaned = pruner.compress_whitespace(cleaned)
    
    before = pruner.estimate_tokens(boilerplate_chunk)
    after = pruner.estimate_tokens(cleaned)
    
    print(f"✓ Before: ~{before} tokens")
    print(f"✓ After: ~{after} tokens")
    print(f"✓ Removed: ~{before - after} tokens")
    
    # Test 4: Token Budget Limiting
    print("\n" + "=" * 70)
    print("TEST 4: Token Budget Limiting")
    print("=" * 70)
    
    budget = 200  # Token budget
    limited_chunks = pruner.prune_by_token_limit(chunks, max_total_tokens=budget)
    limited_tokens = sum(pruner.estimate_tokens(c) for c in limited_chunks)
    
    print(f"✓ Budget: {budget} tokens")
    print(f"✓ Chunks that fit: {len(limited_chunks)} / {len(chunks)}")
    print(f"✓ Total tokens: ~{limited_tokens}")
    print(f"✓ Within budget: {'✓ Yes' if limited_tokens <= budget else '✗ No'}")
    
    # Test 5: Extract Key Sentences
    print("\n" + "=" * 70)
    print("TEST 5: Extract Key Sentences")
    print("=" * 70)
    
    full_chunk = chunks[0]
    key_sentences = pruner.extract_key_sentences(full_chunk, question, max_sentences=2)
    
    full_tokens = pruner.estimate_tokens(full_chunk)
    key_tokens = pruner.estimate_tokens(key_sentences)
    reduction_sent = ((full_tokens - key_tokens) / full_tokens * 100)
    
    print(f"✓ Full chunk: ~{full_tokens} tokens")
    print(f"✓ Key sentences: ~{key_tokens} tokens")
    print(f"✓ Reduction: {reduction_sent:.1f}%")
    print(f"✓ Extracted: {key_sentences[:100]}...")
    
    # Test 6: Full Optimization Pipeline
    print("\n" + "=" * 70)
    print("TEST 6: Full Optimization Pipeline")
    print("=" * 70)
    
    optimizer = ContextWindowOptimizer(max_context_tokens=300)
    optimized_context = optimizer.optimize_context(chunks, distances, question)
    
    optimized_tokens = pruner.estimate_tokens(optimized_context)
    total_reduction = ((original_tokens - optimized_tokens) / original_tokens * 100)
    
    print(f"✓ Original total: ~{original_tokens} tokens")
    print(f"✓ After optimization: ~{optimized_tokens} tokens")
    print(f"✓ Total reduction: {total_reduction:.1f}%")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Starting tokens: ~{original_tokens}")
    print(f"Final tokens: ~{optimized_tokens}")
    print(f"Tokens saved: ~{original_tokens - optimized_tokens}")
    print(f"Reduction: {total_reduction:.1f}%")
    
    print(f"\n💰 COST SAVINGS (if using paid API @ $0.002/1K tokens):")
    print(f"   Before: ${original_tokens * 0.002 / 1000:.4f} per query")
    print(f"   After: ${optimized_tokens * 0.002 / 1000:.4f} per query")
    print(f"   Saved per query: ${(original_tokens - optimized_tokens) * 0.002 / 1000:.4f}")
    print(f"   Saved per 1K queries: ${(original_tokens - optimized_tokens) * 0.002:.2f}")
    print(f"   Saved per 100K queries: ${(original_tokens - optimized_tokens) * 0.2:.2f}")
    
    print("\n" + "=" * 70)


def compare_config_settings():
    """Compare different configuration settings"""
    
    print("\n" + "=" * 70)
    print("⚙️ CONFIGURATION COMPARISON")
    print("=" * 70)
    
    configs = {
        "Default (Current)": {
            "TOP_K_CHUNKS": config.TOP_K_CHUNKS,
            "CHUNK_SIZE": config.CHUNK_SIZE,
            "OPTIMIZATION": config.ENABLE_TOKEN_OPTIMIZATION
        },
        "Recommended Balanced": {
            "TOP_K_CHUNKS": 2,
            "CHUNK_SIZE": 400,
            "OPTIMIZATION": True
        },
        "Speed/Cost Optimized": {
            "TOP_K_CHUNKS": 1,
            "CHUNK_SIZE": 300,
            "OPTIMIZATION": True
        },
        "Quality Focused": {
            "TOP_K_CHUNKS": 3,
            "CHUNK_SIZE": 500,
            "OPTIMIZATION": True
        }
    }
    
    print(f"\n{'Configuration':<25} {'Chunks':<8} {'Size':<8} {'Est. Tokens':<12} {'Cost/1K':<10}")
    print("-" * 70)
    
    for name, cfg in configs.items():
        base_tokens = cfg["TOP_K_CHUNKS"] * (cfg["CHUNK_SIZE"] // 4)
        if cfg["OPTIMIZATION"]:
            estimated_tokens = int(base_tokens * 0.5)  # ~50% reduction with optimization
            opt_marker = " ⚡"
        else:
            estimated_tokens = base_tokens
            opt_marker = ""
        
        cost = estimated_tokens * 0.002
        print(f"{name:<25} {cfg['TOP_K_CHUNKS']:<8} {cfg['CHUNK_SIZE']:<8} ~{estimated_tokens:<11} ${cost:<9.2f}{opt_marker}")
    
    print("\n⚡ = With optimization enabled")
    print("\n💡 Recommendations:")
    print("   • Start with 'Recommended Balanced' for best trade-off")
    print("   • Use 'Speed/Cost Optimized' for high-volume applications")
    print("   • Use 'Quality Focused' with optimization for best answers")


if __name__ == "__main__":
    # Run tests
    test_pruning_strategies()
    compare_config_settings()
    
    print("\n" + "=" * 70)
    print("✅ TESTING COMPLETE!")
    print("=" * 70)
    print("\n💡 To enable optimization in your system:")
    print("   1. Edit config.py")
    print("   2. Set: ENABLE_TOKEN_OPTIMIZATION = True")
    print("   3. Set: MAX_CONTEXT_TOKENS = 600")
    print("   4. Run your app: python app.py")
    print("\n" + "=" * 70)

"""
Compare token usage with and without optimization
Run this to see the impact of token pruning
"""

import os
from rag_system import RAGSystem
from pruning_strategies import TextPruner
import config


def compare_optimization(pdf_path: str, question: str):
    """
    Compare token usage with and without optimization
    
    Args:
        pdf_path: Path to PDF file
        question: Test question
    """
    print("=" * 70)
    print("TOKEN USAGE COMPARISON")
    print("=" * 70)
    
    pruner = TextPruner()
    
    # Test WITHOUT optimization
    print("\n📊 WITHOUT Optimization:")
    print("-" * 70)
    
    rag_standard = RAGSystem(llm_backend="huggingface", enable_optimization=False)
    result = rag_standard.load_and_process_pdf(pdf_path)
    
    if not result["success"]:
        print(f"Error: {result['message']}")
        return
    
    answer_result = rag_standard.answer_question(question, top_k=config.TOP_K_CHUNKS)
    
    if answer_result["success"]:
        context = "\n\n".join(answer_result['context_chunks'])
        tokens_standard = pruner.estimate_tokens(context)
        print(f"Chunks used: {len(answer_result['context_chunks'])}")
        print(f"Estimated tokens: ~{tokens_standard}")
        print(f"Average per chunk: ~{tokens_standard // len(answer_result['context_chunks'])}")
    
    # Test WITH optimization
    print("\n⚡ WITH Optimization:")
    print("-" * 70)
    
    rag_optimized = RAGSystem(llm_backend="huggingface", enable_optimization=True)
    rag_optimized.load_and_process_pdf(pdf_path)
    
    answer_result_opt = rag_optimized.answer_question(question, top_k=config.TOP_K_CHUNKS)
    
    if answer_result_opt["success"]:
        context_opt = "\n\n".join(answer_result_opt['context_chunks'])
        tokens_optimized = pruner.estimate_tokens(context_opt)
        print(f"Chunks used: {len(answer_result_opt['context_chunks'])}")
        print(f"Estimated tokens: ~{tokens_optimized}")
        
        if len(answer_result_opt['context_chunks']) > 0:
            print(f"Average per chunk: ~{tokens_optimized // len(answer_result_opt['context_chunks'])}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if answer_result["success"] and answer_result_opt["success"]:
        reduction = tokens_standard - tokens_optimized
        reduction_pct = (reduction / tokens_standard * 100) if tokens_standard > 0 else 0
        
        print(f"Tokens saved: {reduction}")
        print(f"Reduction: {reduction_pct:.1f}%")
        print(f"\n💰 Cost savings (@ $0.002/1K tokens):")
        print(f"   Standard: ${tokens_standard * 0.002 / 1000:.4f} per query")
        print(f"   Optimized: ${tokens_optimized * 0.002 / 1000:.4f} per query")
        print(f"   Savings: ${reduction * 0.002 / 1000:.4f} per query")
        print(f"\n📈 For 1000 queries:")
        print(f"   Save: ${reduction * 0.002:.2f}")
    
    print("\n" + "=" * 70)


def quick_config_test():
    """Test different config settings"""
    print("\n" + "=" * 70)
    print("CONFIG SETTINGS COMPARISON")
    print("=" * 70)
    
    configs = [
        {"name": "Default", "chunks": 3, "size": 500},
        {"name": "Balanced", "chunks": 2, "size": 400},
        {"name": "Minimal", "chunks": 1, "size": 300},
    ]
    
    pruner = TextPruner()
    
    for cfg in configs:
        # Simulate token usage
        est_tokens = cfg["chunks"] * (cfg["size"] // 4)
        print(f"\n{cfg['name']}:")
        print(f"  TOP_K_CHUNKS = {cfg['chunks']}")
        print(f"  CHUNK_SIZE = {cfg['size']}")
        print(f"  Estimated tokens: ~{est_tokens}")
        print(f"  Cost per 1K queries: ${est_tokens * 0.002:.2f}")


if __name__ == "__main__":
    # Quick config comparison
    quick_config_test()
    
    # Full comparison if sample PDF exists
    pdf_path = os.path.join("data", "sample.pdf")
    
    if os.path.exists(pdf_path):
        question = "What is this document about?"
        compare_optimization(pdf_path, question)
    else:
        print("\n📄 Note: Add a sample.pdf to data/ folder for full comparison")

"""
Command Line Interface for PDF RAG System
For local usage with Ollama
"""

import argparse
import os
from rag_system import RAGSystem
import config


def main():
    parser = argparse.ArgumentParser(description="PDF Question Answering System")
    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file"
    )
    parser.add_argument(
        "--backend",
        choices=["ollama", "huggingface"],
        default="ollama",
        help="LLM backend to use (default: ollama)"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=config.TOP_K_CHUNKS,
        help=f"Number of chunks to retrieve (default: {config.TOP_K_CHUNKS})"
    )
    
    args = parser.parse_args()
    
    # Validate PDF exists
    if not os.path.exists(args.pdf_path):
        print(f"❌ Error: PDF file not found: {args.pdf_path}")
        return
    
    # Initialize RAG system
    print(f"\n🚀 Initializing RAG system with {args.backend} backend...")
    rag = RAGSystem(llm_backend=args.backend)
    
    # Process PDF
    print(f"\n📄 Processing PDF: {args.pdf_path}")
    result = rag.load_and_process_pdf(args.pdf_path)
    
    if not result["success"]:
        print(f"❌ Error: {result['message']}")
        return
    
    print(f"\n✅ PDF processed successfully!")
    print(f"   📊 Number of chunks: {result['num_chunks']}")
    print(f"   📏 Chunk size: {result['chunk_size']} characters")
    
    # Interactive Q&A loop
    print("\n" + "="*60)
    print("💬 Ask questions about the PDF (type 'quit' to exit)")
    print("="*60 + "\n")
    
    while True:
        question = input("\n❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not question:
            continue
        
        # Get answer
        print("\n🤔 Thinking...\n")
        result = rag.answer_question(question, top_k=args.top_k)
        
        if result["success"]:
            print(f"🤖 Answer:\n{result['answer']}\n")
            print(f"📚 Used {result['num_chunks_used']} context chunks")
            
            # Optionally show context
            show_context = input("\n📖 Show retrieved context? (y/n): ").strip().lower()
            if show_context == 'y':
                print("\n" + "="*60)
                for i, chunk in enumerate(result['context_chunks'], 1):
                    print(f"\nChunk {i}:\n{chunk}\n")
                    print("-"*60)
        else:
            print(f"❌ {result['answer']}")


if __name__ == "__main__":
    main()

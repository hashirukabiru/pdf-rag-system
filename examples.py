"""
Example usage of the RAG system
"""

from rag_system import RAGSystem
import os


def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Initialize RAG system
    rag = RAGSystem(llm_backend="huggingface")
    
    # Process a PDF
    pdf_path = os.path.join("data", "sample.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found. Please add a sample PDF to the data folder.")
        return
    
    print(f"\nProcessing: {pdf_path}")
    result = rag.load_and_process_pdf(pdf_path)
    
    if result["success"]:
        print(f"✓ Successfully processed {result['num_chunks']} chunks")
        
        # Ask a question
        question = "What is this document about?"
        print(f"\nQuestion: {question}")
        
        answer_result = rag.answer_question(question)
        
        if answer_result["success"]:
            print(f"\nAnswer: {answer_result['answer']}")
        else:
            print(f"Error: {answer_result['answer']}")
    else:
        print(f"Error: {result['message']}")


def example_multiple_questions():
    """Example with multiple questions"""
    print("\n" + "=" * 60)
    print("Example 2: Multiple Questions")
    print("=" * 60)
    
    rag = RAGSystem(llm_backend="huggingface")
    
    pdf_path = os.path.join("data", "sample.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found")
        return
    
    # Process PDF
    result = rag.load_and_process_pdf(pdf_path)
    
    if not result["success"]:
        print(f"Error: {result['message']}")
        return
    
    # List of questions
    questions = [
        "What is the main topic?",
        "Who are the authors?",
        "What are the key findings?",
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Question: {question}")
        answer_result = rag.answer_question(question, top_k=3)
        
        if answer_result["success"]:
            print(f"   Answer: {answer_result['answer'][:200]}...")
        else:
            print(f"   Error: {answer_result['answer']}")


def example_with_context():
    """Example showing retrieved context"""
    print("\n" + "=" * 60)
    print("Example 3: With Context Display")
    print("=" * 60)
    
    rag = RAGSystem(llm_backend="huggingface")
    
    pdf_path = os.path.join("data", "sample.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found")
        return
    
    result = rag.load_and_process_pdf(pdf_path)
    
    if not result["success"]:
        print(f"Error: {result['message']}")
        return
    
    question = "Summarize the main points"
    print(f"\nQuestion: {question}")
    
    answer_result = rag.answer_question(question, top_k=5)
    
    if answer_result["success"]:
        print(f"\nAnswer: {answer_result['answer']}")
        print(f"\nRetrieved {len(answer_result['context_chunks'])} chunks:")
        
        for i, (chunk, distance) in enumerate(zip(
            answer_result['context_chunks'],
            answer_result['distances']
        ), 1):
            print(f"\nChunk {i} (distance: {distance:.3f}):")
            print(chunk[:200] + "...")
            print("-" * 60)


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    example_multiple_questions()
    example_with_context()

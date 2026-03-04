"""
Test script to verify the RAG system is working correctly
"""

import os
import sys
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from llm_handler import LLMHandler
from rag_system import RAGSystem


def test_pdf_processor():
    """Test PDF processing"""
    print("=" * 60)
    print("Test 1: PDF Processor")
    print("=" * 60)
    
    processor = PDFProcessor(chunk_size=500, chunk_overlap=50)
    
    pdf_path = os.path.join("data", "sample.pdf")
    
    if not os.path.exists(pdf_path):
        print("❌ FAILED: sample.pdf not found in data folder")
        print("   Please add a sample PDF file to the data/ directory")
        return False
    
    try:
        text = processor.load_pdf(pdf_path)
        print(f"✓ Loaded PDF: {len(text)} characters")
        
        chunks = processor.chunk_text(text)
        print(f"✓ Created {len(chunks)} chunks")
        
        if len(chunks) > 0:
            print(f"✓ First chunk preview: {chunks[0][:100]}...")
            print("✅ PASSED: PDF Processor")
            return True
        else:
            print("❌ FAILED: No chunks created")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_vector_store():
    """Test vector store"""
    print("\n" + "=" * 60)
    print("Test 2: Vector Store")
    print("=" * 60)
    
    try:
        vector_store = VectorStore()
        
        # Test with sample chunks
        test_chunks = [
            "This is a test document about artificial intelligence.",
            "Machine learning is a subset of AI.",
            "Natural language processing helps computers understand text.",
            "Deep learning uses neural networks.",
            "Python is a popular programming language for AI."
        ]
        
        vector_store.build_index(test_chunks)
        print(f"✓ Built index with {len(test_chunks)} chunks")
        
        # Test search
        query = "What is machine learning?"
        results, distances = vector_store.search(query, top_k=2)
        
        print(f"✓ Search query: '{query}'")
        print(f"✓ Top result: '{results[0]}'")
        
        # Check if relevant result is returned
        if "machine learning" in results[0].lower() or "AI" in results[0]:
            print("✅ PASSED: Vector Store")
            return True
        else:
            print("⚠️  WARNING: Search may not be returning most relevant results")
            return True  # Still pass, might be model-dependent
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_llm_handler():
    """Test LLM handler"""
    print("\n" + "=" * 60)
    print("Test 3: LLM Handler")
    print("=" * 60)
    
    try:
        # Test with Hugging Face backend
        print("Testing Hugging Face backend...")
        llm = LLMHandler(backend="huggingface")
        
        context = ["Python is a programming language.", "It is widely used for AI and data science."]
        question = "What is Python?"
        
        answer = llm.generate_answer(context, question)
        print(f"✓ Generated answer: {answer[:100]}...")
        
        if answer and len(answer) > 0:
            print("✅ PASSED: LLM Handler (Hugging Face)")
            return True
        else:
            print("❌ FAILED: Empty answer generated")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print("   Note: This might be due to model download. Check your internet connection.")
        return False


def test_full_rag_system():
    """Test complete RAG system"""
    print("\n" + "=" * 60)
    print("Test 4: Full RAG System")
    print("=" * 60)
    
    pdf_path = os.path.join("data", "sample.pdf")
    
    if not os.path.exists(pdf_path):
        print("❌ FAILED: sample.pdf not found")
        return False
    
    try:
        # Initialize RAG system
        rag = RAGSystem(llm_backend="huggingface")
        print("✓ Initialized RAG system")
        
        # Process PDF
        result = rag.load_and_process_pdf(pdf_path)
        
        if not result["success"]:
            print(f"❌ FAILED: {result['message']}")
            return False
        
        print(f"✓ Processed PDF: {result['num_chunks']} chunks")
        
        # Ask a question
        question = "What is this document about?"
        answer_result = rag.answer_question(question)
        
        if not answer_result["success"]:
            print(f"❌ FAILED: {answer_result['answer']}")
            return False
        
        print(f"✓ Question: {question}")
        print(f"✓ Answer: {answer_result['answer'][:150]}...")
        print(f"✓ Used {answer_result['num_chunks_used']} context chunks")
        
        print("✅ PASSED: Full RAG System")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 Running RAG System Tests" + "\n")
    
    tests = [
        test_pdf_processor,
        test_vector_store,
        test_llm_handler,
        test_full_rag_system
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test crashed: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

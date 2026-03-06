"""
Test script to verify the RAG system is working correctly
"""

import os
import sys
# Import zlib and struct to create a tiny valid PDF without external libs
import zlib

def create_minimal_pdf(filename):
    """Creates a tiny, valid PDF file to satisfy pypdf header requirements"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # Minimal PDF 1.4 syntax
    content = (
        b"%PDF-1.4\n"
        b"1 0 obj <</Type/Catalog/Pages 2 0 R>> endobj\n"
        b"2 0 obj <</Type/Pages/Count 1/Kids[3 0 R]>> endobj\n"
        b"3 0 obj <</Type/Page/Parent 2 0 R/Resources<<>>/Contents 4 0 R>> endobj\n"
        b"4 0 obj <</Length 51>> stream\n"
        b"BT /F1 12 Tf 100 700 Td (This is a test document.) ET\n"
        b"endstream\n"
        b"endobj\n"
        b"xref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000052 00000 n\n"
        b"0000000101 00000 n\n0000000178 00000 n\n"
        b"trailer <</Size 5/Root 1 0 R>>\nstartxref\n279\n%%EOF"
    )
    with open(filename, "wb") as f:
        f.write(content)
    print(f"✓ Created valid test PDF at: {filename}")

# Now import your project modules
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
    
    # Ensure file exists before testing
    if not os.path.exists(pdf_path):
        create_minimal_pdf(pdf_path)
    
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
        test_chunks = [
            "This is a test document about artificial intelligence.",
            "Machine learning is a subset of AI.",
            "Natural language processing helps computers understand text."
        ]
        vector_store.build_index(test_chunks)
        print(f"✓ Built index with {len(test_chunks)} chunks")
        
        query = "What is machine learning?"
        results, distances = vector_store.search(query, top_k=2)
        print(f"✓ Search query: '{query}'")
        
        if len(results) > 0:
            print("✅ PASSED: Vector Store")
            return True
        return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_llm_handler():
    """Test LLM handler"""
    print("\n" + "=" * 60)
    print("Test 3: LLM Handler")
    print("=" * 60)
    try:
        llm = LLMHandler(backend="huggingface")
        context = ["Python is a programming language."]
        question = "What is Python?"
        answer = llm.generate_answer(context, question)
        print(f"✓ Generated answer: {answer[:100]}...")
        
        if answer:
            print("✅ PASSED: LLM Handler")
            return True
        return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_full_rag_system():
    """Test complete RAG system"""
    print("\n" + "=" * 60)
    print("Test 4: Full RAG System")
    print("=" * 60)
    pdf_path = os.path.join("data", "sample.pdf")
    
    try:
        rag = RAGSystem(llm_backend="huggingface")
        result = rag.load_and_process_pdf(pdf_path)
        
        if not result["success"]:
            print(f"❌ FAILED: {result['message']}")
            return False
        
        answer_result = rag.answer_question("What is this about?")
        print(f"✓ Answer: {answer_result['answer'][:100]}...")
        print("✅ PASSED: Full RAG System")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n🧪 Running RAG System Tests\n")
    
    # Pre-create data directory and sample file
    if not os.path.exists("data"):
        os.makedirs("data")
    create_minimal_pdf(os.path.join("data", "sample.pdf"))

    tests = [test_pdf_processor, test_vector_store, test_llm_handler, test_full_rag_system]
    passed = 0
    for test in tests:
        if test(): passed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Summary | Passed: {passed}/{len(tests)}")
    return passed == len(tests)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

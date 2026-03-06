"""
PDF Question Answering System - Hugging Face Spaces Version
A simple RAG (Retrieval-Augmented Generation) system for PDF documents
"""

import gradio as gr
import os
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

# Initialize model globally
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("✓ Model loaded")

# Global variables
chunks = []
index = None
current_pdf_name = ""

def load_pdf(pdf_file):
    """Extract text from PDF"""
    try:
        reader = PdfReader(pdf_file.name)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks"""
    text_chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            text_chunks.append(chunk)
        start += (chunk_size - overlap)
    return text_chunks

def process_pdf(pdf_file):
    """Process uploaded PDF and create embeddings"""
    global chunks, index, current_pdf_name
    
    if pdf_file is None:
        return "❌ Please upload a PDF file", ""
    
    try:
        # Extract text
        text = load_pdf(pdf_file)
        if text.startswith("Error"):
            return text, ""
        
        # Create chunks
        chunks = chunk_text(text)
        
        if not chunks:
            return "❌ No text found in PDF", ""
        
        # Create embeddings
        embeddings = model.encode(chunks)
        embeddings = np.array(embeddings).astype('float32')
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        current_pdf_name = os.path.basename(pdf_file.name)
        
        stats = f"""✅ **PDF Processed Successfully!**

📄 **File:** {current_pdf_name}
📊 **Chunks Created:** {len(chunks)}
📏 **Chunk Size:** 500 characters

You can now ask questions about the document!"""
        
        return stats, "Ready"
        
    except Exception as e:
        return f"❌ Error: {str(e)}", ""

def answer_question(question, top_k):
    """Answer question based on PDF content"""
    global chunks, index
    
    if not question.strip():
        return "Please enter a question.", ""
    
    if index is None or not chunks:
        return "❌ Please upload and process a PDF first!", ""
    
    try:
        # Search for relevant chunks
        query_embedding = model.encode([question]).astype('float32')
        distances, indices = index.search(query_embedding, int(top_k))
        
        # Get top chunks
        top_chunks = [chunks[i] for i in indices[0]]
        
        # Format answer
        answer = f"""### 📚 Most Relevant Information:

"""
        
        for i, (chunk, dist) in enumerate(zip(top_chunks, distances[0]), 1):
            answer += f"""
**📄 Section {i}** (Relevance: {100 - min(dist, 100):.1f}%)

{chunk.strip()}

---
"""
        
        # Format context
        context = f"**Retrieved {len(top_chunks)} relevant sections from:** {current_pdf_name}"
        
        return answer, context
        
    except Exception as e:
        return f"❌ Error: {str(e)}", ""

# Create Gradio interface
with gr.Blocks(title="PDF Question Answering - RAG System") as demo:
    gr.Markdown("""
    # 📄 PDF Question Answering System
    
    ### 🚀 Upload a PDF and ask questions about its content!
    
    This app uses **Retrieval-Augmented Generation (RAG)** to find relevant information in your PDF:
    1. Upload a PDF document
    2. Process it to create searchable embeddings
    3. Ask questions and get relevant excerpts
    
    **Features:**
    - ✅ Semantic search using sentence embeddings
    - ✅ FAISS vector similarity search
    - ✅ Adjustable number of results
    - ✅ No sign-up required!
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📁 Step 1: Upload PDF")
            pdf_input = gr.File(
                label="Select PDF File",
                file_types=[".pdf"],
                type="filepath"
            )
            process_btn = gr.Button("🔄 Process PDF", variant="primary", size="lg")
            status_output = gr.Markdown("")
            
        with gr.Column(scale=1):
            gr.Markdown("### ❓ Step 2: Ask Questions")
            question_input = gr.Textbox(
                label="Your Question",
                placeholder="e.g., What is this document about?",
                lines=2
            )
            top_k_slider = gr.Slider(
                minimum=1,
                maximum=5,
                value=3,
                step=1,
                label="Number of relevant sections to retrieve"
            )
            ask_btn = gr.Button("🔍 Get Answer", variant="primary", size="lg")
    
    gr.Markdown("### 💡 Answer")
    answer_output = gr.Markdown("")
    context_output = gr.Markdown("")
    
    gr.Markdown("""
    ---
    ### 📖 How it works:
    1. **Upload**: Your PDF is processed and split into chunks
    2. **Embed**: Each chunk is converted to a vector using sentence-transformers
    3. **Index**: Vectors are stored in a FAISS index for fast search
    4. **Search**: Your question is embedded and matched against the index
    5. **Retrieve**: Most relevant chunks are returned
    
    ### 🔧 Tech Stack:
    - **Gradio** - Web interface
    - **Sentence Transformers** - Text embeddings
    - **FAISS** - Vector similarity search
    - **PyPDF** - PDF processing
    
    ---
    💡 **Tip:** Try asking specific questions about topics in your PDF for best results!
    """)
    
    # Event handlers
    process_btn.click(
        fn=process_pdf,
        inputs=[pdf_input],
        outputs=[status_output, context_output]
    )
    
    ask_btn.click(
        fn=answer_question,
        inputs=[question_input, top_k_slider],
        outputs=[answer_output, context_output]
    )
    
    # Allow Enter key to submit question
    question_input.submit(
        fn=answer_question,
        inputs=[question_input, top_k_slider],
        outputs=[answer_output, context_output]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()

"""
Gradio Web Interface for PDF RAG System
Deployable to Hugging Face Spaces
"""

import gradio as gr
import os
from rag_system import RAGSystem
import config


# Initialize RAG system with Hugging Face backend (for Spaces compatibility)
rag = RAGSystem(llm_backend="huggingface")


def process_pdf(pdf_file):
    """Process uploaded PDF file"""
    if pdf_file is None:
        return "❌ Please upload a PDF file", ""
    
    try:
        # Validate file
        if not pdf_file.name.lower().endswith('.pdf'):
            return "❌ Please upload a valid PDF file", ""
        
        # Get file size
        file_size = os.path.getsize(pdf_file.name)
        file_size_mb = file_size / (1024 * 1024)
        
        if file_size_mb > config.MAX_FILE_SIZE_MB:
            return f"❌ File too large ({file_size_mb:.1f}MB). Maximum size: {config.MAX_FILE_SIZE_MB}MB", ""
        
        result = rag.load_and_process_pdf(pdf_file.name)
        
        if result["success"]:
            stats = f"""✅ **PDF Processed Successfully!**
            
📄 **File:** {os.path.basename(pdf_file.name)}
💾 **Size:** {file_size_mb:.2f} MB
📊 **Chunks Created:** {result['num_chunks']}
📏 **Chunk Size:** {result['chunk_size']} characters

You can now ask questions about the document!"""
            return stats, "Ready for questions"
        else:
            return f"❌ Error: {result['message']}", ""
    
    except Exception as e:
        return f"❌ Error processing PDF: {str(e)}", ""


def answer_question(question, top_k):
    """Answer user question"""
    if not question or not question.strip():
        return "❌ Please enter a question.", ""
    
    if len(question.strip()) < 3:
        return "❌ Question too short. Please enter at least 3 characters.", ""
    
    if len(question) > 1000:
        return "❌ Question too long. Please keep it under 1000 characters.", ""
    
    try:
        result = rag.answer_question(question, top_k=int(top_k))
        
        if not result["success"]:
            return result["answer"], ""
        
        # Format answer with context
        answer_text = f"""### 🤖 Answer:
{result['answer']}

---
### 📚 Retrieved Context ({len(result['context_chunks'])} chunks):
"""
        
        context_text = ""
        for i, (chunk, distance) in enumerate(zip(result['context_chunks'], result['distances']), 1):
            chunk_preview = chunk[:300] + "..." if len(chunk) > 300 else chunk
            context_text += f"\n**Chunk {i}** (relevance score: {distance:.3f}):\n```\n{chunk_preview}\n```\n"
        
        return answer_text, context_text
    
    except Exception as e:
        return f"❌ Error generating answer: {str(e)}", ""


def reset_system():
    """Reset the RAG system"""
    rag.reset()
    return "System reset. Please upload a new PDF.", "", ""


# Create Gradio Interface
with gr.Blocks(title="PDF Question Answering System", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📚 PDF Question Answering with RAG
    
    Upload a PDF document and ask questions about its content. This system uses:
    - **Sentence Transformers** for embeddings
    - **FAISS** for vector similarity search
    - **Flan-T5** for answer generation
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1️⃣ Upload PDF")
            pdf_input = gr.File(
                label="Upload PDF Document",
                file_types=[".pdf"],
                type="filepath"
            )
            process_btn = gr.Button("📤 Process PDF", variant="primary")
            process_output = gr.Markdown(label="Processing Status")
            status_box = gr.Textbox(label="System Status", visible=False)
            
            gr.Markdown("### ⚙️ Settings")
            top_k_slider = gr.Slider(
                minimum=1,
                maximum=10,
                value=3,
                step=1,
                label="Number of chunks to retrieve",
                info="More chunks = more context but slower"
            )
            
            reset_btn = gr.Button("🔄 Reset System", variant="secondary")
        
        with gr.Column(scale=2):
            gr.Markdown("### 2️⃣ Ask Questions")
            question_input = gr.Textbox(
                label="Enter your question",
                placeholder="What is this document about?",
                lines=2
            )
            ask_btn = gr.Button("❓ Ask Question", variant="primary")
            
            answer_output = gr.Markdown(label="Answer")
            
            with gr.Accordion("📖 View Retrieved Context", open=False):
                context_output = gr.Markdown()
    
    gr.Markdown("""
    ---
    ### 💡 Tips:
    - Ask specific questions for best results
    - The system retrieves the most relevant sections from your PDF
    - Larger documents may take longer to process
    
    ### 🔧 How it works:
    1. **Upload**: Your PDF is split into chunks
    2. **Index**: Chunks are converted to embeddings and indexed
    3. **Retrieve**: When you ask a question, the most relevant chunks are found
    4. **Generate**: An AI model generates an answer based on the retrieved context
    """)
    
    # Event handlers
    process_btn.click(
        fn=process_pdf,
        inputs=[pdf_input],
        outputs=[process_output, status_box]
    )
    
    ask_btn.click(
        fn=answer_question,
        inputs=[question_input, top_k_slider],
        outputs=[answer_output, context_output]
    )
    
    question_input.submit(
        fn=answer_question,
        inputs=[question_input, top_k_slider],
        outputs=[answer_output, context_output]
    )
    
    reset_btn.click(
        fn=reset_system,
        outputs=[process_output, answer_output, context_output]
    )


# Launch the app
if __name__ == "__main__":
    demo.launch()

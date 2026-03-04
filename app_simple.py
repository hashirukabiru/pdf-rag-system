"""
Simple PDF RAG App - No LLM downloads required
Works offline, returns relevant context chunks
"""

import gradio as gr
import os
from simple_rag import SimpleRAG

# Initialize RAG system
print("Initializing Simple RAG system...")
rag = SimpleRAG()

def process_pdf(pdf_file):
    """Process uploaded PDF file"""
    if pdf_file is None:
        return "❌ Please upload a PDF file", ""
    
    try:
        result = rag.load_and_process_pdf(pdf_file.name)
        
        if result["success"]:
            stats = f"""✅ **PDF Processed Successfully!**
            
📄 **File:** {os.path.basename(pdf_file.name)}
📊 **Chunks Created:** {result['num_chunks']}
📏 **Chunk Size:** {result['chunk_size']} characters

You can now ask questions about the document!"""
            return stats, "Ready for questions"
        else:
            return f"❌ Error: {result['message']}", ""
    
    except Exception as e:
        return f"❌ Error processing PDF: {str(e)}", ""

def answer_question(question, top_k):
    """Answer user question by returning relevant chunks"""
    if not question.strip():
        return "Please enter a question.", ""
    
    try:
        result = rag.answer_question(question, top_k=int(top_k))
        
        if not result["success"]:
            return result["answer"], ""
        
        # Format answer with context
        answer_text = f"""### 📚 Most Relevant Information:

{result['answer']}

---
**Found {len(result['context_chunks'])} relevant sections**
"""
        
        context_text = ""
        for i, (chunk, distance) in enumerate(zip(result['context_chunks'], result['distances']), 1):
            context_text += f"\n**Section {i}** (relevance: {1/(1+distance):.1%}):\n```\n{chunk}\n```\n\n"
        
        return answer_text, context_text
    
    except Exception as e:
        return f"❌ Error: {str(e)}", ""

# Create Gradio interface
with gr.Blocks(title="PDF Question Answering", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📄 PDF Question Answering System (Simple Version)
    
    Upload a PDF and ask questions - get instant answers from the most relevant sections!
    
    **Features:**
    - ✅ Fast startup (no model downloads)
    - ✅ Works offline
    - ✅ Returns relevant text chunks
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            pdf_input = gr.File(
                label="📁 Upload PDF",
                file_types=[".pdf"],
                type="filepath"
            )
            process_btn = gr.Button("🔄 Process PDF", variant="primary", size="lg")
            
            pdf_status = gr.Markdown("Upload a PDF to get started...")
            
            gr.Markdown("---")
            
            question_input = gr.Textbox(
                label="❓ Ask a Question",
                placeholder="What is this document about?",
                lines=3
            )
            
            top_k_slider = gr.Slider(
                minimum=1,
                maximum=5,
                value=3,
                step=1,
                label="📊 Number of sections to retrieve"
            )
            
            ask_btn = gr.Button("🔍 Get Answer", variant="primary", size="lg")
        
        with gr.Column(scale=2):
            answer_output = gr.Markdown(label="📝 Answer")
            
            gr.Markdown("---")
            
            context_output = gr.Markdown(label="📚 Retrieved Context")
    
    # Event handlers
    process_btn.click(
        fn=process_pdf,
        inputs=[pdf_input],
        outputs=[pdf_status, gr.Textbox(visible=False)]
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

if __name__ == "__main__":
    print("✓ Simple RAG system initialized")
    print("Starting Gradio interface...")
    # Use environment variable for HuggingFace Spaces compatibility
    import os
    is_hf_space = os.getenv("SPACE_ID") is not None
    demo.launch(share=False, server_port=7865 if not is_hf_space else None)

import os
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# If using Ollama Python client
import ollama

# -------------------------------
# 1️⃣ Load PDF
# -------------------------------
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# -------------------------------
# 2️⃣ Split into chunks
# -------------------------------
def chunk_text(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

# -------------------------------
# 3️⃣ Create embeddings
# -------------------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def create_embeddings(chunks):
    embeddings = model.encode(chunks)
    return np.array(embeddings).astype("float32")

# -------------------------------
# 4️⃣ FAISS index
# -------------------------------
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

# -------------------------------
# 5️⃣ Retrieve top chunks
# -------------------------------
def get_top_chunks(index, chunks, question, top_k=3):
    query_embedding = model.encode(question).astype("float32").reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    top_chunks = [chunks[i] for i in indices[0]]
    return top_chunks

# -------------------------------
# 6️⃣ Generate AI answer via Ollama
# -------------------------------
def generate_ai_answer(top_chunks, question):
    context = "\n".join(top_chunks)
    prompt = f"Use the following context to answer the question concisely:\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    
    # Use Ollama client properly
    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response["message"]["content"]

# -------------------------------
# 7️⃣ MAIN PROGRAM
# -------------------------------
pdf_path = os.path.join("data", "sample.pdf")

text = load_pdf(pdf_path)
chunks = chunk_text(text)
print(f"Number of chunks: {len(chunks)}")

embeddings = create_embeddings(chunks)
print("Embeddings created")

index = create_faiss_index(embeddings)
print("FAISS index ready")

# Ask user question
question = input("Ask a question about the PDF: ")

# Get top chunks
top_chunks = get_top_chunks(index, chunks, question, top_k=3)
print("\nTop relevant chunks:\n")
for c in top_chunks:
    print(c)
    print("----")

# Generate natural AI answer
answer = generate_ai_answer(top_chunks, question)
print("\n=== AI Answer ===\n")
print(answer)
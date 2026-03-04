# 🚀 Deployment Guide

This guide covers deploying your PDF RAG system to different platforms.

## 📋 Table of Contents

- [Hugging Face Spaces](#hugging-face-spaces)
- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Platforms](#cloud-platforms)

## 🤗 Hugging Face Spaces

### Method 1: Web Interface

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: pdf-rag-qa (or your choice)
   - **License**: MIT
   - **SDK**: Gradio
   - **Visibility**: Public or Private
4. Click **"Create Space"**
5. Upload the following files:
   ```
   app.py
   config.py
   pdf_processor.py
   vector_store.py
   llm_handler.py
   rag_system.py
   requirements.txt
   README.md
   ```
6. Your Space will automatically build and deploy!

### Method 2: Git (Recommended)

```bash
# Install Hugging Face CLI
pip install huggingface_hub[cli]

# Login to Hugging Face
huggingface-cli login

# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/pdf-rag-qa
cd pdf-rag-qa

# Copy your files
cp ../app.py .
cp ../config.py .
cp ../pdf_processor.py .
cp ../vector_store.py .
cp ../llm_handler.py .
cp ../rag_system.py .
cp ../requirements.txt .
cp ../README.md .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### Method 3: Using the HF Hub Python API

```python
from huggingface_hub import HfApi

api = HfApi()

# Create a new Space
api.create_repo(
    repo_id="pdf-rag-qa",
    repo_type="space",
    space_sdk="gradio"
)

# Upload files
api.upload_folder(
    folder_path=".",
    repo_id="YOUR_USERNAME/pdf-rag-qa",
    repo_type="space"
)
```

## 💻 Local Deployment

### With Ollama (Recommended for Local)

1. **Install Ollama**
   - Download from [ollama.ai](https://ollama.ai)
   - Or use: `curl https://ollama.ai/install.sh | sh`

2. **Pull a model**
   ```bash
   ollama pull llama3.2
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the CLI**
   ```bash
   python cli.py data/sample.pdf --backend ollama
   ```

5. **Or run the Web UI**
   ```bash
   # Edit config.py to use Ollama by default
   python app.py
   ```

### With Hugging Face Models

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app will be available at `http://localhost:7860`

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py .
COPY data/ data/

# Expose Gradio port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
```

### Build and Run

```bash
# Build the image
docker build -t pdf-rag-system .

# Run the container
docker run -p 7860:7860 pdf-rag-system
```

### Docker Compose

```yaml
version: '3.8'

services:
  pdf-rag:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./data:/app/data
      - ./uploads:/app/uploads
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
```

Run with:
```bash
docker-compose up
```

## ☁️ Cloud Platforms

### AWS EC2

1. **Launch an EC2 instance**
   - Choose Ubuntu 22.04 LTS
   - t2.medium or larger (2GB+ RAM)
   - Configure security group to allow port 7860

2. **SSH into instance and install**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3-pip python3-venv -y
   
   # Clone your repo
   git clone your-repo-url
   cd pdf-rag-system
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the app
   python app.py --server-name 0.0.0.0
   ```

3. **Set up as a service** (optional)
   ```bash
   sudo nano /etc/systemd/system/pdf-rag.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=PDF RAG System
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/pdf-rag-system
   Environment="PATH=/home/ubuntu/pdf-rag-system/venv/bin"
   ExecStart=/home/ubuntu/pdf-rag-system/venv/bin/python app.py --server-name 0.0.0.0

   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl enable pdf-rag
   sudo systemctl start pdf-rag
   ```

### Google Cloud Run

1. **Create Dockerfile** (see Docker section)

2. **Build and push**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/pdf-rag
   ```

3. **Deploy**
   ```bash
   gcloud run deploy pdf-rag \
     --image gcr.io/YOUR_PROJECT/pdf-rag \
     --platform managed \
     --port 7860 \
     --memory 2Gi
   ```

### Heroku

1. **Create `Procfile`**
   ```
   web: python app.py --server-name 0.0.0.0 --server-port $PORT
   ```

2. **Deploy**
   ```bash
   heroku create pdf-rag-system
   git push heroku main
   ```

## 🔒 Production Considerations

### Environment Variables

Create a `.env` file:
```bash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=google/flan-t5-large
CHUNK_SIZE=500
MAX_FILE_SIZE_MB=50
```

Update `config.py` to use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
```

### Security

- Set file size limits
- Validate file types
- Add rate limiting
- Use HTTPS in production
- Sanitize user inputs
- Add authentication if needed

### Performance

- Use GPU for faster inference (if available)
- Cache embeddings
- Use batch processing
- Consider using a vector database for large-scale deployments

### Monitoring

- Add logging
- Track usage metrics
- Monitor resource usage
- Set up error alerts

## 📊 Resource Requirements

| Deployment Type | RAM | CPU | Storage | Notes |
|----------------|-----|-----|---------|-------|
| Local (HF) | 4GB | 2 cores | 2GB | CPU inference |
| Local (Ollama) | 8GB | 4 cores | 5GB | Includes model |
| HF Spaces | 16GB | 2 cores | 2GB | Free tier |
| Production | 8GB+ | 4+ cores | 10GB+ | With GPU recommended |

## 🆘 Troubleshooting

### Common Issues

**Out of Memory**
- Reduce `CHUNK_SIZE`
- Use a smaller model
- Increase instance RAM

**Slow Performance**
- Use GPU acceleration
- Reduce `TOP_K_CHUNKS`
- Use a faster embedding model

**Model Download Fails**
- Check internet connection
- Use HF_TOKEN for gated models
- Try a different model

## 📞 Support

For deployment issues:
- Check the [GitHub Issues](your-repo-url/issues)
- Join our [Discord](your-discord-link) (optional)
- Email: support@example.com (optional)

---

Happy Deploying! 🚀

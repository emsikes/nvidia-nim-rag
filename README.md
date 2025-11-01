# NVIDIA NIM RAG System

A Retrieval Augmented Generation (RAG) system built with NVIDIA NIM for both cloud-based and local LLM inference and embeddings. This project demonstrates building a production-ready RAG pipeline with a clean architecture suitable for enterprise deployment.

## Overview

This system provides intelligent question-answering over your documents using:
- **NVIDIA NIM** for LLM inference (Llama 3.1 8B Instruct)
- **NVIDIA NIM Embeddings** (NV-Embed-QA v5)
- **ChromaDB** for vector storage with persistent SQLite backend
- **FastAPI** for RESTful backend API
- **Streamlit** for interactive chat interface

## Architecture
```
User Query → Streamlit UI → FastAPI → RAG Pipeline
                                          ↓
                            Document Processor → Text Chunks
                                          ↓
                            Vector Store (ChromaDB) ← Embeddings (NIM)
                                          ↓
                            Vector Search → Context Retrieval
                                          ↓
                            LLM (NIM) → Generated Response
```

## Project Structure
```
nvidia-nim-rag/
├── src/
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── document_processor.py   # Text chunking and processing
│   │   ├── vector_store.py         # ChromaDB vector operations
│   │   └── rag_pipeline.py         # Main RAG orchestration
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py                 # FastAPI REST endpoints
│   └── frontend/
│       └── app.py                  # Streamlit chat interface
├── tests/
│   ├── test_nim_connection.py
│   ├── test_embeddings.py
│   ├── test_document_processor.py
│   ├── test_vector_store.py
│   └── test_rag_pipeline.py
├── data/
│   └── sample_doc.txt              # Sample knowledge base
├── .env                            # Environment variables (not in git)
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

### Hardware Requirements
- **For Cloud API:** Any system with internet connection
- **For Local Deployment:** 
  - NVIDIA GPU (RTX 3090/4090, A100, or better)
  - Minimum 16GB GPU VRAM
  - 20GB+ free disk space
  - CUDA-compatible drivers

### Software Requirements
- Python 3.10+
- Docker (for local NIM deployment)
- NVIDIA Container Toolkit (for local NIM deployment)
- NVIDIA Developer Account

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nvidia-nim-rag.git
cd nvidia-nim-rag
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:
```bash
# NVIDIA API Keys
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxx
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1

# For local NIM deployment (optional)
NGC_API_KEY=your_ngc_api_key_here
```

**Get your NVIDIA API Key:**
1. Visit https://build.nvidia.com
2. Sign in or create account
3. Navigate to any model and click "Get API Key"
4. Generate and copy your key

**Get your NGC API Key (for local deployment):**
1. Visit https://ngc.nvidia.com/setup/api-key
2. Sign in with NVIDIA account
3. Generate API Key
4. Copy the key

## Deployment Options

### Option A: Cloud API Deployment (Quick Start)

Perfect for development and testing without local GPU.

**Start the API server:**
```bash
uvicorn src.api.main:app --reload --port 8000
```

**In a new terminal, start the Streamlit UI:**
```bash
streamlit run src/frontend/app.py
```

**Access the application:**
- API Documentation: http://localhost:8000/docs
- Chat Interface: http://localhost:8501

### Option B: Local NIM Deployment (Production)

Much faster inference with local GPU execution.

#### Step 1: Verify GPU Setup
```bash
# Check Docker installation
docker --version

# Verify NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

# Check available disk space
df -h --total
```

**Expected output:**
- Docker version 20.10+
- nvidia-smi showing your GPU details
- At least 20GB free disk space

#### Step 2: Login to NGC Registry
```bash
docker login nvcr.io
# Username: $oauthtoken
# Password: <your NGC API key>
```

#### Step 3: Download NIM Container
```bash
docker pull nvcr.io/nim/meta/llama-3.1-8b-instruct:latest
```

**Note:** ~12GB download, takes 10-20 minutes.

#### Step 4: Run Local NIM
```bash
export NGC_API_KEY="your_ngc_key_here"
export LOCAL_NIM_CACHE=~/.cache/nim

mkdir -p $LOCAL_NIM_CACHE

docker run -it --rm \
  --gpus all \
  --shm-size=16GB \
  -e NGC_API_KEY \
  -v $LOCAL_NIM_CACHE:/opt/nim/.cache \
  -p 8001:8000 \
  nvcr.io/nim/meta/llama-3.1-8b-instruct:latest
```

**First run:** Downloads and optimizes model weights (~5-10 minutes)

**Look for:** `INFO: Uvicorn running on http://0.0.0.0:8000`

#### Step 5: Update Configuration

Edit `src/rag/rag_pipeline.py`:
```python
self.llm = ChatNVIDIA(
    model="meta/llama-3.1-8b-instruct",
    base_url="http://localhost:8001/v1",  # Point to local NIM
    temperature=0.2,
    max_tokens=512
)
```

Similarly, update `src/rag/vector_store.py` if you want local embeddings.

#### Step 6: Start Application
```bash
# Terminal 1: API Server
uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Streamlit UI
streamlit run src/frontend/app.py
```

## Usage

### Using the Chat Interface

1. **Load a Document:**
   - Use sidebar to browse or enter file path
   - Click "Load Document"
   - Wait for confirmation message

2. **Ask Questions:**
   - Type your question in the chat input
   - Press Enter
   - View AI-generated response based on your documents

3. **Chat History:**
   - All conversations are maintained in the session
   - Scroll up to view previous exchanges

### Using the API Directly

**Upload a document:**
```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"file_path": "data/sample_doc.txt"}'
```

**Query the system:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the benefits of RAG?"}'
```

**Health check:**
```bash
curl http://localhost:8000/health
```

## Testing

Run individual component tests:
```bash
# Test NIM connection
python -m tests.test_nim_connection

# Test embeddings
python -m tests.test_embeddings

# Test document processing
python -m tests.test_document_processor

# Test vector store
python -m tests.test_vector_store

# Test complete RAG pipeline
python -m tests.test_rag_pipeline
```

## Performance Comparison

| Deployment | First Query | Subsequent Queries | Setup Time |
|------------|-------------|-------------------|------------|
| Cloud API  | ~80s        | ~80s              | 5 minutes  |
| Local NIM  | ~10s (cold) | ~2-5s             | 30 minutes |

## Project Status

### Completed ✅
- [x] NVIDIA NIM API integration
- [x] Document processing and chunking
- [x] Vector storage with ChromaDB
- [x] RAG pipeline implementation
- [x] FastAPI REST backend
- [x] Streamlit chat interface
- [x] File upload functionality
- [x] Component testing suite
- [x] Local NIM deployment guide

### In Progress 🚧
- [ ] Local NIM deployment verification
- [ ] Performance benchmarking

### Planned 📋
- [ ] NeMo Guardrails integration
- [ ] Advanced content safety filters
- [ ] Jailbreak detection
- [ ] Fact-checking rails
- [ ] Multi-document support
- [ ] Conversation memory
- [ ] Evaluation with RAGAS framework
- [ ] Docker Compose deployment
- [ ] Monitoring and logging

## Troubleshooting

### ChromaDB SQLite Version Error

If you see: `SQLite version error (need 3.35.0+)`

**Solution:**
```bash
pip install pysqlite3-binary
```

Then add to the top of `src/rag/vector_store.py`:
```python
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
```

### GPU Not Detected
```bash
# Check NVIDIA driver
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

### Slow Cloud API Responses

- Expected: 80+ seconds per query
- Solution: Deploy locally for 2-5 second responses

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

## Configuration

### Chunk Size Tuning

Edit `src/rag/document_processor.py`:
```python
DocumentProcessor(
    chunk_size=500,      # Adjust based on your documents
    chunk_overlap=50     # Overlap between chunks
)
```

### Retrieval Settings

Edit `src/rag/rag_pipeline.py`:
```python
def query(self, question: str, top_k: int = 3):  # Change top_k
```

### Model Temperature

Edit `src/rag/rag_pipeline.py`:
```python
self.llm = ChatNVIDIA(
    temperature=0.2,  # Lower = more focused, Higher = more creative
    max_tokens=512    # Maximum response length
)
```

## Best Practices

1. **Document Preparation:**
   - Use clean, well-formatted text files
   - Remove excessive whitespace
   - Keep documents focused on specific topics

2. **Chunk Size:**
   - Too small: Loss of context
   - Too large: Less precise retrieval
   - Recommended: 300-700 characters

3. **Query Formulation:**
   - Be specific and clear
   - Ask one question at a time
   - Reference document topics

4. **Local Deployment:**
   - Monitor GPU memory usage
   - Use model caching for faster startups
   - Consider batch processing for multiple queries

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License

## Acknowledgments

- Built with [NVIDIA NIM](https://developer.nvidia.com/nim)
- Powered by [LangChain](https://www.langchain.com/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)
- UI built with [Streamlit](https://streamlit.io/)

## Resources

- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)
- [LangChain NVIDIA Integration](https://python.langchain.com/docs/integrations/providers/nvidia/)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)

## Contact

For questions or support, please open an issue on GitHub.
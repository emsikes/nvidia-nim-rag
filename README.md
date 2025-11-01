# NVIDIA NIM RAG System

A production-grade Retrieval Augmented Generation (RAG) system built with NVIDIA NIM for LLM inference and embeddings.

## Overview

This project demonstrates how to build an enterprise RAG system using:
- **NVIDIA NIM** for LLM inference (Llama 3.1)
- **NVIDIA NIM Embeddings** (NV-Embed-QA)
- **ChromaDB** for vector storage
- **FastAPI** for backend API
- **Streamlit** for frontend interface

## Project Structure
```
nvidia-nim-rag/
├── src/
│   ├── rag/
│   │   ├── document_processor.py   # Text splitting and processing
│   │   ├── vector_store.py         # Vector database operations
│   │   └── rag_pipeline.py         # Main RAG logic
│   ├── api/                        # FastAPI backend
│   └── evaluation/                 # RAGAS evaluation
├── tests/                          # Test scripts
├── data/                           # Sample documents
├── .env                            # Environment variables (not in git)
└── requirements.txt
```

## Setup

### Prerequisites
- Python 3.10+
- NVIDIA API Key (get from [build.nvidia.com](https://build.nvidia.com))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nvidia-nim-rag.git
cd nvidia-nim-rag
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
NVIDIA_API_KEY=your_api_key_here
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
```

## Usage

### Testing Components

Test document processing:
```bash
python -m tests.test_document_processor
```

Test embeddings:
```bash
python -m tests.test_embeddings
```

## Current Status

**Phase 1: Setup & Prerequisites** ✅
- [x] NVIDIA NIM API access
- [x] Project structure
- [x] Environment setup

**Phase 2: Core RAG Components** 🚧 (In Progress)
- [x] Document processor
- [X] Vector store
- [ ] RAG pipeline
- [ ] API backend

**Phase 3: Frontend & Deployment** ⏳
- [ ] Streamlit UI
- [ ] Docker deployment
- [ ] NeMo Guardrails integration

## Future Enhancements

- Local NIM deployment (when moving to production)
- NeMo Guardrails for safe AI responses
- Advanced evaluation with RAGAS
- Multi-document support
- Streaming responses

## License

MIT License

## Acknowledgments

Built with NVIDIA NIM and LangChain
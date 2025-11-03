from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag.nemo_guardrails_rag import NeMoGuardrailedRAG
# from src.rag.rag_pipeline import RAGPipeline
from typing import Optional
import os
from dotenv import load_dotenv


load_dotenv(override=True)

app = FastAPI(title="NVIDIA NIM RAG API")

# Initialize RAG pipeline
rag = NeMoGuardrailedRAG()

class DocumentUpload(BaseModel):
    file_path: str

class Query(BaseModel):
    question: str
    top_k: Optional[int] = 3

class QueryResponse(BaseModel):
    question: str
    answer: str

@app.get("/")
def root():
    return {"message": "NVIDIA NIM RAG API", "status": "running"}

@app.post("/upload")
def upload_document(doc: DocumentUpload):
    try:
        num_chunks = rag.load_documents(doc.file_path)
        return {"message": f"Successfully loaded {num_chunks} chunks"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
def query_rag(query: Query):
    try:
        answer = rag.query(query.question, top_k=query.top_k)
        return QueryResponse(question=query.question, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("health")
def health_check():
    return {"status": "healthy"}
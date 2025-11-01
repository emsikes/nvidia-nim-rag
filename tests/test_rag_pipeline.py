from dotenv import load_dotenv
from src.rag.rag_pipeline import RAGPipeline
import time


# Initialize pipeline
rag = RAGPipeline()

# Load documents
print("Loading documents...")
start_time = time.time()
num_chunks = rag.load_documents("data/sample_doc.txt")
load_time = time.time() - start_time

print(f"Loaded {num_chunks} chunks into vector store\n")
print(f"Time taken: {load_time:.2f} seconds\n")


# Ask some test questions
questions = [
    "What is RAG?",
    "What are the benefits of RAG?",
    "How does RAG work?"
]

for question in questions:
    print(f"Question: {questions}")
    print("-" * 50)

    # Time the query
    start = time.time()
    answer = rag.query(question)

    query_time = time.time() - start
    print(f"Answer: {answer}\n")
    print(f"Query time: {query_time:.2f} seconds")
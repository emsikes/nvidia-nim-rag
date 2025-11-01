from dotenv import load_dotenv

from src.rag.document_processor import DocumentProcessor
from src.rag.vector_store import VectorStore


load_dotenv(override=True)

# Initialize components
processor = DocumentProcessor(chunk_size=200, chunk_overlap=20)
vector_store = VectorStore(collection_name="test_collection")

# Load and process document
text = processor.load_text_file("data/sample_doc.txt")
chunks = processor.split_text(text)

print(f"Processing {len(chunks)} chunks...")

# Add to vector store
vector_store.add_documents(chunks)

# test search functionality
query = "What are the benefits of RAG?"
print(f"\nQuery: {query}")
print("-" * 50)

results = vector_store.search(query, top_k=2)

print(f"\nTop {len(results['documents'][0])} results:\n")

for i, doc in enumerate(results['documents'][0], 1):
    print(f"Result: {i}")
    print(f"{doc}\n")
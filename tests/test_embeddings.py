from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

embedder = NVIDIAEmbeddings(
    model="nvidia/nv-embedqa-e5-v5",
    api_key=os.getenv("NVIDIA_API_KEY")
)

text = "What is retrival augmented generation?"

embedding = embedder.embed_query(text)

print(f"Text: {text}")
print(f"Embedding dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
from src.rag.document_processor import DocumentProcessor


processor = DocumentProcessor(chunk_size=200, chunk_overlap=20)

text = processor.load_text_file("data/sample_doc.txt")
chunks = processor.split_text(text)

print(f"Original text length: {len(text)} characters")
print(f"Number of chunks: {len(chunks)}\n")

# Iterate through each chunk and keep track of each one numerically
for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i} ({len(chunk)} chars):")
    print(f"{chunk}\n")
    print("-" * 50)

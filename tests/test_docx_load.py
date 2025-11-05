from src.rag.document_processor import DocumentProcessor


processor = DocumentProcessor()


try:
    doc_path = "data/sample_doc.docx"
    text = processor.load_docx_file(doc_path)    

    print(f"Extraced {len(text)} characters from PDF")
    print("\nFirst 200 characters")
    print(text[:200])
except Exception as e:
    print(f"Error: {e}")
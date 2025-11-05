from src.rag.document_processor import DocumentProcessor


processor = DocumentProcessor()


try:
    pdf_path = "data/2312.12148v1.pdf"
    text = processor.load_pdf_file(pdf_path)    
    # test invalid file type
    # text = processor.load_file("test.xlsx")

    print(f"Extraced {len(text)} characters from PDF")
    print("\nFirst 200 characters")
    print(text[:200])
except Exception as e:
    print(f"Error: {e}")
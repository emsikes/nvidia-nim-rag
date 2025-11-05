from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
import pypdf
from docx import Document


class DocumentProcessor:
    def __init__(self, chunk_size=500, chunk_overlap=5):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_text_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
        
    def load_pdf_file(self, file_path: str) -> str:

        with open(file_path, 'rb') as file:
            pdf = pypdf.PdfReader(file)

            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text
        
    def load_docx_file(self, file_path: str) -> str:
        doc = Document(file_path)
        text = ""
        
        for paragraph in doc.paragraph:
            text += paragraph.text + "\n"

        return text
        
    def load_file(self, file_path: str) -> str:
        # Load either text or pdf
        if file_path.endswith('.pdf'):
            return self.load_pdf_file(file_path)
        elif file_path.endswith('.txt'):
            return self.load_text_file(file_path)
        elif file_path.endswith('.docx'):
            return self.load_docx_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
        
    def split_text(self, text: str) -> List[str]:
        chunks = self.text_splitter.split_text(text)
        return chunks
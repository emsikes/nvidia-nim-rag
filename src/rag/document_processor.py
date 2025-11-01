from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List


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
        
    def split_text(self, text: str) -> List[str]:
        chunks = self.text_splitter.split_text(text)
        return chunks
# from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.llms import Ollama
from src.rag.document_processor import DocumentProcessor
from src.rag.vector_store import VectorStore
from dotenv import load_dotenv
import os

load_dotenv(override=True)
LOCAL_MODEL_API_ENDPOINT = os.getenv("LOCAL_LLM")


class RAGPipeline:
    def __init__(self):
        """
        Initialize the document processor to load and chunk, the vector store for store and retrieval, and the model
        """
        self.processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
        self.vector_store = VectorStore(collection_name="rag_docs")

        # This is for use with NVIDIA hosted model and performaing API calls
        #
        # self.llm = ChatNVIDIA(
        #     model="meta/llama-3.1-8b-instruct",
        #     api_key=os.getenv("NVIDIA_API_KEY"),
        #     temperature=0.2,
        #     max_tokens=512
        # )

        self.llm = Ollama(
            model="llama3.1:8b",
            base_url=LOCAL_MODEL_API_ENDPOINT,
            temperature=0.2
        )

    def load_documents(self, file_path: str):
        """
        Load, split, chunk documents
        """
        text = self.processor.load_text_file(file_path)
        chunks = self.processor.split_text(text)
        self.vector_store.add_documents(chunks)
        return len(chunks)
    
    def query(self, question: str, top_k: int = 3) -> str:
        """
        Retrieve relevant context
        """
        results = self.vector_store.search(question, top_k=top_k)
        context_chunks = results['documents'][0]
        context = "\n\n".join(context_chunks)

        # Generate chunks
        prompt = f"""Answer the question based on the conext below.

        Context:
        {context}

        Question: {question}
        Answer:"""

        # Generate response
        response = self.llm.invoke(prompt)
        return response
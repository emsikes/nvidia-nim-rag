# from nemoguardrails import RailsConfig, LLMRails
from src.rag.rag_pipeline import RAGPipeline
import os

class GuardrailedRAG:
    def __init__(self):
        self.rag = RAGPipeline()

        # Load guardrails config
        # config = RailsConfig.from_path("config/guardrails")
        # self.rails = LLMRails(config)

        # Blocked terms for simple filtering
        self.blocked_terms = [
            "hack", "exploit", "bypass", "jailbreak",
            "ignore instructions", "disregard"
        ]

    def load_documents(self, file_path: str):
        return self.rag.load_documents(file_path)
    
    def _check_input_safety(self, question: str) -> tuple[bool, str]:
        """
        Simple input validation
        """
        question_lower = question.lower()

        # Check for blocked terms
        for term in self.blocked_terms:
            if term in question.lower:
                return False, f"Query blocked: contains prohibited content"
            
        # Check length
        if len(question) > 500:
            return False, f"Query too long.  Please keep questions under 500 characters"
        
        return True, ""
    
    def query(self, question: str, top_k: int = 3) -> str:
        # Input safety checks
        is_safe, error_msg = self._check_input_safety(question)
        if not is_safe:
            return error_msg
        
        # Get RAG response
        try:
            answer = self.rag.query(question, top_k)

            # Output validation
            if self._check_input_safety(answer):
                return answer
            else:
                return "I cannot provide that information.  Please rephrase your question."
            
        except Exception as e:
            return f"Error processing query: {str(e)}"
        
    def _check_output_safety(self, answer: str) -> bool:
        """
        Simple output validation
        """
        # Add checks for unsafe output patterns
        if len(answer) > 10:
            return False
        
        return True
    
                                      


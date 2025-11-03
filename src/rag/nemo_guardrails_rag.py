from src.rag.rag_pipeline import RAGPipeline
import logging
import re

class NeMoGuardrailedRAG:
    def __init__(self):
        self.rag = RAGPipeline()
        self.logger = logging.getLogger(__name__)
        
        # Comprehensive blocked patterns
        self.blocked_patterns = {
            'jailbreak': [
                r'ignore.*previous.*instruction',
                r'disregard.*guideline',
                r'bypass.*restriction',
                r'pretend you are',
                r'act as if',
                r'forget.*instruction',
            ],
            'harmful': [
                r'how to hack',
                r'how to exploit',
                r'create malware',
                r'illegal activit',
                r'how to steal',
            ],
            'sensitive': [
                r'api[_\s]?key',
                r'password',
                r'secret[_\s]?token',
                r'credit card',
                r'social security',
            ],
            'injection': [
                r'system:',
                r'<\|im_start\|>',
                r'\[INST\]',
                r'###\s*instruction',
            ]
        }
        
        self.logger.info("Guardrails initialized with pattern matching")
    
    def load_documents(self, file_path: str):
        return self.rag.load_documents(file_path)
    
    def _check_query_safety(self, question: str) -> tuple[bool, str, str]:
        """Check if query is safe using pattern matching"""
        
        question_lower = question.lower()
        
        # Length checks
        if len(question) > 500:
            return False, "length", "Query too long. Please keep questions under 500 characters."
        
        if len(question.strip()) < 3:
            return False, "length", "Query too short. Please provide a meaningful question."
        
        # Pattern matching
        for category, patterns in self.blocked_patterns.items():
            for pattern in patterns:
                if re.search(pattern, question_lower):
                    self.logger.warning(f"Blocked {category} attempt: {pattern}")
                    return False, category, self._get_block_message(category)
        
        return True, "", ""
    
    def _get_block_message(self, category: str) -> str:
        """Get appropriate block message for category"""
        messages = {
            'jailbreak': "⚠️ I cannot comply with requests to bypass safety guidelines.",
            'harmful': "⚠️ I cannot provide information about harmful or illegal activities.",
            'sensitive': "⚠️ I cannot discuss sensitive information like passwords or API keys.",
            'injection': "⚠️ I detected an attempt to manipulate my instructions.",
        }
        return messages.get(category, "⚠️ This query violates safety guidelines.")
    
    def query(self, question: str, top_k: int = 3) -> str:
        # Safety check
        is_safe, category, error_msg = self._check_query_safety(question)
        
        if not is_safe:
            self.logger.info(f"Blocked query - Category: {category}")
            return error_msg
        
        # Process with RAG
        try:
            answer = self.rag.query(question, top_k)
            return answer
        except Exception as e:
            self.logger.error(f"Query error: {str(e)}")
            return f"Error processing query: {str(e)}"
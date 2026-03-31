from openai import OpenAI, APIError
from app.config import get_settings
from app.utils.logger import logger
from app.utils.errors import OpenAIException
from typing import List, Dict

class OpenAIService:
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.MAX_TOKENS
    
    def generate_response(self, messages: List[Dict[str, str]]) -> Dict:
        """Generate response from OpenAI API"""
        try:
            logger.info(f"Calling OpenAI API with {len(messages)} messages")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7,
            )
            
            content = response.choices[0].message.content
            tokens = response.usage.completion_tokens
            
            logger.info(f"OpenAI response generated. Tokens: {tokens}")
            return {
                "content": content,
                "tokens_used": tokens
            }
        except APIError as e:
            logger.error(f"OpenAI API Error: {str(e)}")
            raise OpenAIException(f"Failed to generate response: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise OpenAIException(f"Unexpected error: {str(e)}")
    
    def generate_code(self, prompt: str) -> Dict:
        """Generate code with specific formatting"""
        system_message = """You are an expert code generation AI. 
        Generate clean, production-ready code with best practices.
        Always include comments for complex logic.
        Format code in markdown code blocks."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        return self.generate_response(messages)
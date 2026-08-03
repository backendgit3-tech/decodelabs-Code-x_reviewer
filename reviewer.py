import os
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from dotenv import load_dotenv

from groq import Groq

from models import Language, CodeReviewRequest
from prompt_builder import PromptBuilder
from validator import OutputValidator
from renderer import Renderer

load_dotenv()

class CodeReviewer:
    """Intelligent code reviewer with Groq API."""
    
    def __init__(self, provider: str = "groq", model: str = None):
        self.provider = provider
        self.model = model or "llama-3.3-70b-versatile"
        self.prompt_builder = PromptBuilder()
        self.validator = OutputValidator()
        self.renderer = Renderer()
        self._initialize_client()
        
        print(f"✅ Code Reviewer initialized!")
        print(f"   📋 Provider: {provider}")
        print(f"   🤖 Model: {self.model}")
    
    def _initialize_client(self):
        """Initialize the Groq client."""
        if self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in .env file")
            self.client = Groq(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def review_code(self, code: str, language: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Review code and return structured output.
        """
        request = CodeReviewRequest(
            code=code,
            language=language,
            filename=filename
        )
        
        system_prompt = self.prompt_builder.build_system_prompt()
        user_prompt = self.prompt_builder.build_user_prompt(
            code=request.code,
            language=request.language,
            filename=request.filename
        )
        
        print(f"🔍 Analyzing {request.language.value} code...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=4096,
            )
            
            result_text = response.choices[0].message.content
            
            is_valid, bug_report, refactored_code = self.validator.validate(result_text)
            
            if not is_valid:
                raise ValueError("Invalid response format from LLM")
            
            return {
                'bug_report': bug_report,
                'refactored_code': refactored_code,
                'raw_response': result_text,
                'metadata': {
                    'language': request.language.value,
                    'filename': filename,
                    'timestamp': datetime.now().isoformat(),
                    'model': self.model,
                    'provider': self.provider
                }
            }
            
        except Exception as e:
            raise RuntimeError(f"Code review failed: {str(e)}")
    
    def review_file(self, filepath: str) -> Dict[str, Any]:
        """
        Review a code file directly.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        language = self._detect_language(filepath)
        
        return self.review_code(
            code=code,
            language=language.value,
            filename=filepath
        )
    
    def _detect_language(self, filepath: str) -> Language:
        """Detect language from file extension."""
        ext = filepath.split('.')[-1].lower()
        mapping = {
            'py': Language.PYTHON,
            'js': Language.JAVASCRIPT,
            'ts': Language.TYPESCRIPT,
            'java': Language.JAVA,
            'c': Language.C,
            'cpp': Language.CPP,
            'go': Language.GO,
            'rs': Language.RUST,
            'sql': Language.SQL,
        }
        return mapping.get(ext, Language.UNKNOWN)
    
    def render_results(self, results: Dict[str, Any]):
        """Render the review results."""
        self.renderer.render(
            bug_report=results['bug_report'],
            refactored_code=results['refactored_code']
        )
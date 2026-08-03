from typing import Optional
from models import Language


class PromptBuilder:
    """Builds system prompts and user prompts for code review."""
    
    SYSTEM_INSTRUCTION = """You are an expert code reviewer and software architect with 20 years of experience.

Your task is to analyze the provided code and produce:
1. A detailed bug report
2. Refactored, optimized code

STRICT OUTPUT FORMAT - YOU MUST FOLLOW THIS EXACTLY:

## BUG_REPORT
- List each bug as a bullet point
- Each bug must include: file/line reference (if available), bug description, severity (Critical/High/Medium/Low), and suggested fix
- Group bugs by type: Syntax, Logic, Performance, Security, Style

## REFACTORED_CODE
Provide the complete refactored code inside a single Markdown-fenced code block with the language identifier after the opening triple backticks.

BEHAVIORAL RULES:
- Be thorough but concise
- Prioritize critical bugs first
- Provide clear, actionable fixes
- Maintain the original code's intent
- Do NOT change functionality, only improve code quality

If no bugs are found, still include ## BUG_REPORT with "No bugs found" and provide a brief improvement summary.

RULES:
1. You MUST include exactly these two section headers: ## BUG_REPORT and ## REFACTORED_CODE
2. The REFACTORED_CODE section MUST contain a valid code block with language specification
3. Never output anything outside these two sections
4. Never include explanations inside the REFACTORED_CODE code block"""

    def build_system_prompt(self) -> str:
        """Return the system instruction prompt."""
        return self.SYSTEM_INSTRUCTION

    @staticmethod
    def get_language_specific_guidelines(language: Language) -> str:
        """Get language-specific review guidelines."""
        guidelines = {
            Language.PYTHON: """
- Follow PEP 8 style guidelines
- Check for proper exception handling
- Verify type hints are used correctly
- Check for efficient list comprehensions
- Look for potential memory leaks
""",
            Language.JAVASCRIPT: """
- Follow ESLint recommended rules
- Check for proper async/await usage
- Verify variable scoping (let/const)
- Look for potential XSS vulnerabilities
- Check for callback hell or promise misuse
""",
            Language.JAVA: """
- Follow Java naming conventions
- Check for proper exception handling (try-catch)
- Verify memory management (null checks)
- Look for potential synchronization issues
- Check for proper encapsulation
""",
            Language.TYPESCRIPT: """
- Check for proper type annotations
- Verify interface definitions
- Look for type safety issues
- Check for proper use of 'any' type
- Verify strict mode compliance
""",
            Language.C: """
- Check for memory management issues
- Verify pointer safety
- Look for buffer overflow vulnerabilities
- Check for proper error handling
- Verify return value checking
""",
        }
        return guidelines.get(
            language, 
            "- Follow language best practices\n- Check for common anti-patterns\n- Verify error handling is present"
        )
    
    def build_user_prompt(self, code: str, language: Language, filename: Optional[str] = None) -> str:
        """
        Build the user prompt with code context.
        """
        filename_info = f"File: {filename}\n" if filename else ""
        guidelines = PromptBuilder.get_language_specific_guidelines(language)
        
        return f"""Analyze the following {language.value} code:

{filename_info}Guidelines:
{guidelines}

```{language.value}
{code}
```"""
"""
Markdown rendering with syntax highlighting using Rich.
"""

from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
import re

class Renderer:
    """Renders code review output with syntax highlighting."""
    
    def __init__(self):
        self.console = Console()
    
    def render(self, bug_report: str, refactored_code: str):
        """
        Render the bug report and refactored code.
        """
        # Header
        self.console.print("\n" + "=" * 80)
        self.console.print("[bold cyan]🤖 INTELLIGENT CODE REVIEWER[/bold cyan]")
        self.console.print("=" * 80 + "\n")
        
        # Render Bug Report
        self._render_bug_report(bug_report)
        
        # Render Refactored Code
        self._render_refactored_code(refactored_code)
    
    def _render_bug_report(self, bug_report: str):
        """Render the bug report section."""
        self.console.print("[bold yellow]🐛 BUG REPORT[/bold yellow]")
        self.console.print("-" * 40)
        
        # Remove the header if present
        clean_report = bug_report.replace("## BUG_REPORT", "").strip()
        
        # Render as markdown
        md = Markdown(clean_report)
        self.console.print(md)
        self.console.print()
    
    def _render_refactored_code(self, refactored_code: str):
        """Render the refactored code section with syntax highlighting."""
        self.console.print("[bold green]💡 REFACTORED CODE[/bold green]")
        self.console.print("-" * 40)
        
        # Extract code block
        code, language = self._extract_code_block(refactored_code)
        
        if code:
            # Use Rich's Syntax highlighting
            syntax = Syntax(
                code.strip(),
                language or "text",
                theme="monokai",
                line_numbers=True,
                word_wrap=True
            )
            self.console.print(syntax)
        else:
            # Fallback: render as markdown
            md = Markdown(refactored_code)
            self.console.print(md)
        
        self.console.print("\n" + "=" * 80)
    
    def _extract_code_block(self, text: str) -> tuple:
        """Extract code block and language from text."""
        pattern = r'```(\w+)?\n([\s\S]*?)\n```'
        match = re.search(pattern, text)
        if match:
            language = match.group(1) or "text"
            code = match.group(2)
            return code, language
        return None, None
    
    def render_summary(self, summary: str):
        """Render a summary section."""
        if summary:
            self.console.print("[bold cyan]📊 SUMMARY[/bold cyan]")
            self.console.print("-" * 40)
            self.console.print(summary)
            self.console.print()
    
    def render_error(self, error: str):
        """Render an error message."""
        self.console.print(f"[bold red]❌ ERROR:[/bold red] {error}")
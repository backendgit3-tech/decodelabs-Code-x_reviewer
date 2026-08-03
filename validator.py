"""
Output validation for code review responses.
Ensures the LLM response contains the required structured sections.
"""

import re
from typing import Tuple, Optional, List, Dict

class OutputValidator:
    """
    Validates LLM responses to ensure they contain the required
    ## BUG_REPORT and ## REFACTORED_CODE sections.
    """
    
    BUG_REPORT_HEADER = "## BUG_REPORT"
    REFACTORED_CODE_HEADER = "## REFACTORED_CODE"
    
    def validate(self, response: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate that response contains both required sections.
        
        Args:
            response: Raw LLM response string
            
        Returns:
            Tuple of (is_valid, bug_report_content, refactored_code_content)
        """
        if not response or not response.strip():
            return False, None, None
        
        # Check for required headers
        if self.BUG_REPORT_HEADER not in response:
            print(f"❌ Missing header: {self.BUG_REPORT_HEADER}")
            return False, None, None
        
        if self.REFACTORED_CODE_HEADER not in response:
            print(f"❌ Missing header: {self.REFACTORED_CODE_HEADER}")
            return False, None, None
        
        # Extract sections
        bug_report = self._extract_section(response, self.BUG_REPORT_HEADER, self.REFACTORED_CODE_HEADER)
        refactored_code = self._extract_section(response, self.REFACTORED_CODE_HEADER, None)
        
        # Validate bug report is not empty
        if not bug_report or len(bug_report.strip()) < 5:
            print("❌ Bug report is empty or too short")
            return False, None, None
        
        # Validate refactored code contains a code block
        if not self._contains_code_block(refactored_code):
            print("❌ Refactored code does not contain a valid code block")
            return False, None, None
        
        return True, bug_report, refactored_code
    
    def _extract_section(self, text: str, start_header: str, end_header: Optional[str]) -> str:
        """
        Extract content between two headers.
        
        Args:
            text: Full response text
            start_header: Header marking the start of section
            end_header: Header marking the end of section (optional)
            
        Returns:
            Extracted section content
        """
        start_idx = text.find(start_header) + len(start_header)
        
        if end_header:
            end_idx = text.find(end_header, start_idx)
            if end_idx == -1:
                end_idx = len(text)
        else:
            end_idx = len(text)
        
        return text[start_idx:end_idx].strip()
    
    def _contains_code_block(self, text: str) -> bool:
        """
        Check if text contains a Markdown code block.
        
        Args:
            text: Text to check
            
        Returns:
            True if code block exists
        """
        pattern = r'```\w*\n[\s\S]*?\n```'
        return bool(re.search(pattern, text))
    
    def extract_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """
        Extract all code blocks from text.
        
        Args:
            text: Text containing code blocks
            
        Returns:
            List of dicts with 'language' and 'code' keys
        """
        pattern = r'```(\w+)?\n([\s\S]*?)\n```'
        matches = re.findall(pattern, text)
        
        blocks = []
        for match in matches:
            language = match[0] or "text"
            code = match[1]
            blocks.append({
                'language': language,
                'code': code
            })
        
        return blocks
    
    def extract_first_code_block(self, text: str) -> Optional[Dict[str, str]]:
        """
        Extract the first code block from text.
        
        Args:
            text: Text containing code blocks
            
        Returns:
            Dict with 'language' and 'code' keys, or None
        """
        blocks = self.extract_code_blocks(text)
        return blocks[0] if blocks else None
    
    def count_bugs(self, bug_report: str) -> int:
        """
        Count the number of bug entries in a bug report.
        
        Args:
            bug_report: Bug report text
            
        Returns:
            Number of bug items found
        """
        # Count bullet points
        lines = bug_report.split('\n')
        bullet_count = sum(1 for line in lines if line.strip().startswith('-'))
        return bullet_count
    
    def get_bug_severities(self, bug_report: str) -> Dict[str, int]:
        """
        Count bugs by severity level.
        
        Args:
            bug_report: Bug report text
            
        Returns:
            Dict with severity counts
        """
        severities = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        
        lines = bug_report.split('\n')
        for line in lines:
            line_lower = line.lower()
            if 'critical' in line_lower:
                severities['Critical'] += 1
            elif 'high' in line_lower:
                severities['High'] += 1
            elif 'medium' in line_lower:
                severities['Medium'] += 1
            elif 'low' in line_lower:
                severities['Low'] += 1
        
        return severities
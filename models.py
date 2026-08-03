"""
Data models for code review.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum

class Language(str, Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    TYPESCRIPT = "typescript"
    C = "c"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    SQL = "sql"    
    UNKNOWN = "unknown"

class CodeReviewRequest(BaseModel):
    """Input model for code review."""
    code: str = Field(..., description="Raw code to review")
    language: Language = Field(..., description="Programming language")
    filename: Optional[str] = Field(None, description="Original filename")
    
    @validator('code')
    def validate_code(cls, v):
        if not v or not v.strip():
            raise ValueError("Code cannot be empty")
        return v

class BugReport(BaseModel):
    """Structured bug report output."""
    bugs: List[str] = Field(..., description="List of identified bugs")
    vulnerabilities: List[str] = Field(default_factory=list)
    performance_issues: List[str] = Field(default_factory=list)
    style_issues: List[str] = Field(default_factory=list)

class RefactoredCode(BaseModel):
    """Refactored code output."""
    code: str = Field(..., description="Refactored code")
    language: Language = Field(..., description="Language of refactored code")
    explanation: Optional[str] = Field(None, description="Explanation of changes")

class CodeReviewResponse(BaseModel):
    """Complete code review output."""
    bug_report: BugReport
    refactored_code: RefactoredCode
    summary: Optional[str] = None
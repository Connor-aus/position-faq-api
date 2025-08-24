from pydantic import BaseModel, Field, validator
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()
MAX_QUESTION_LENGTH = int(os.getenv("MAX_QUESTION_LENGTH", "5000"))

class ChatRequest(BaseModel):
    """
    Model for chat request validation
    """
    question: str = Field(..., description="The question from the user")
    positionId: int = Field(..., description="The ID of the position")
    
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError("Question cannot be empty.")
        if len(v) > MAX_QUESTION_LENGTH:
            raise ValueError(f"Question exceeds max length of {MAX_QUESTION_LENGTH} characters.")
        return v

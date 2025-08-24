from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PositionDetailsRequest(BaseModel):
    """
    Model for position details update request
    """
    position: Dict[str, Any] = Field(..., description="Position information")
    positionFAQs: Optional[List[Dict[str, Any]]] = Field(None, description="Position FAQs")
    positionInfo: Optional[List[Dict[str, Any]]] = Field(None, description="Position information items")

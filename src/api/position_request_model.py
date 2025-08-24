from pydantic import BaseModel, Field

class PositionRequest(BaseModel):
    """
    Model for position request validation
    """
    positionId: int = Field(..., description="The ID of the position")

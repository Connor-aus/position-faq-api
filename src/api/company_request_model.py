from pydantic import BaseModel, Field

class CompanyRequest(BaseModel):
    """
    Model for company request validation
    """
    companyId: int = Field(..., description="The ID of the company")

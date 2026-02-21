from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CompanyBase(BaseModel):
    domain: str
    industry: Optional[str] = None
    company_size: Optional[str] = None
    revenue_range: Optional[str] = None

class BatchResponse(BaseModel):
    id: UUID
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class BatchDetailResponse(BatchResponse):
    companies: List[CompanyBase]
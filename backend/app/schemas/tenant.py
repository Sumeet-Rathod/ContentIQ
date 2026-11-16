from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TenantBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

class TenantCreate(TenantBase):
    plan: Optional[str] = "free"

class TenantResponse(BaseModel):
    id: str
    name: str
    plan: str
    created_at: str

    class Config:
        from_attributes = True

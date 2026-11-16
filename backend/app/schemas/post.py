from pydantic import BaseModel, Field
from typing import Optional, List, Literal

PlatformType = Literal["instagram", "linkedin", "youtube"]
PostStatusType = Literal["draft", "scheduled", "published"]

class PostBase(BaseModel):
    platform: PlatformType = "instagram"
    caption: str = Field(..., min_length=1)
    hashtags: List[str] = []
    media_url: Optional[str] = None
    scheduled_time: Optional[str] = None  # Local datetime string e.g. "2026-10-25T15:00"
    status: PostStatusType = "draft"

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    platform: Optional[PlatformType] = None
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None
    media_url: Optional[str] = None
    scheduled_time: Optional[str] = None
    status: Optional[PostStatusType] = None

class PostResponse(BaseModel):
    id: str
    tenant_id: str
    created_by: str
    platform: PlatformType
    caption: str
    hashtags: List[str]
    media_url: Optional[str] = None
    scheduled_time: Optional[str] = None
    scheduled_hour: Optional[int] = None  # Plain integer 0-23 derived directly without UTC conversion
    status: PostStatusType
    predicted_tier: Optional[str] = None  # "low", "medium", "high"
    predicted_confidence: Optional[float] = None
    sentiment: Optional[float] = None
    readability: Optional[float] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

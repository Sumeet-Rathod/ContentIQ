from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ThumbnailMetricItem(BaseModel):
    name: str
    score: float
    percentage: int

class ThumbnailScoreResponse(BaseModel):
    dimensions: str
    brightness: float
    contrast: float
    sharpness: float
    colourfulness: float
    composition: float
    overall_score: float
    recommendations: List[str]
    metrics: List[ThumbnailMetricItem]

class TrendItem(BaseModel):
    hashtag: str
    this_week_count: int
    last_week_count: int
    total_count: int
    growth_rate: float
    status: str

class TrendResponse(BaseModel):
    tenant_id: str
    analyzed_posts_count: int
    total_unique_hashtags: int
    trending_hashtags: List[TrendItem]
    rising_count: int
    declining_count: int
    stable_count: int

class TopicRecommendationItem(BaseModel):
    id: str
    topic_title: str
    target_platform: str
    why_recommended: str
    suggested_angle: str
    recommended_hashtags: List[str]
    similarity_score: float

class RecommendationResponse(BaseModel):
    tenant_id: str
    status: str
    niche: Optional[str] = None
    message: Optional[str] = None
    analyzed_posts_count: Optional[int] = None
    mean_corpus_similarity: Optional[float] = None
    top_keywords: Optional[List[str]] = None
    recommendations: List[TopicRecommendationItem] = []

class FollowerSnapshotCreate(BaseModel):
    platform: str = "instagram"
    date: str  # YYYY-MM-DD
    follower_count: int = Field(..., ge=0)

class ForecastTimelinePoint(BaseModel):
    date: str
    actual: Optional[int] = None
    yhat: int
    yhat_lower: int
    yhat_upper: int
    is_projected: bool

class ForecastResponse(BaseModel):
    status: str
    message: Optional[str] = None
    count: Optional[int] = None
    min_required: Optional[int] = None
    days_ahead: Optional[int] = None
    historical_points: Optional[int] = None
    current_followers: Optional[int] = None
    projected_30d_followers: Optional[int] = None
    projected_growth_rate: Optional[float] = None
    trend_direction: Optional[str] = None
    timeline: Optional[List[ForecastTimelinePoint]] = None

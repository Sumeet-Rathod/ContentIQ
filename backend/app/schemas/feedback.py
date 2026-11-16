from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Metrics & Retraining Schemas ---
class PostMetricsCreate(BaseModel):
    post_id: str
    likes: int = Field(0, ge=0)
    comments: int = Field(0, ge=0)
    shares: int = Field(0, ge=0)
    reach: int = Field(1, ge=1)

class PostMetricsResponse(BaseModel):
    id: str
    tenant_id: str
    post_id: str
    likes: int
    comments: int
    shares: int
    reach: int
    engagement_rate: float
    actual_tier: str  # low, medium, high
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class RetrainResponse(BaseModel):
    status: str
    message: str
    real_samples_count: int
    min_required: int = 50
    accuracy_before: Optional[float] = None
    accuracy_after: Optional[float] = None
    improvement_delta: Optional[float] = None
    retrained_at: Optional[str] = None

# --- A/B Testing Schemas ---
class ABTestCreate(BaseModel):
    title: str = Field(..., min_length=2)
    description: Optional[str] = ""
    variant_post_ids: List[str] = Field(..., min_length=2, max_length=4)

class ABTestVariant(BaseModel):
    post_id: str
    platform: str
    caption: str
    likes: int
    comments: int
    shares: int
    reach: int
    engagement_rate: float
    is_winner: bool = False

class ABTestResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    description: Optional[str] = ""
    status: str  # running, completed
    winner_post_id: Optional[str] = None
    variants: List[ABTestVariant]
    created_at: str

# --- Competitor Benchmarking Schemas ---
class CompetitorCreate(BaseModel):
    handle: str = Field(..., min_length=2)
    platform: str = "instagram"
    follower_count: int = Field(..., ge=0)
    engagement_rate: float = Field(..., ge=0.0, le=100.0)

class CompetitorResponse(BaseModel):
    id: str
    tenant_id: str
    handle: str
    platform: str
    follower_count: int
    engagement_rate: float
    updated_at: Optional[str] = ""

class CompetitorBenchmarkResponse(BaseModel):
    tenant_average_engagement: float
    competitors: List[CompetitorResponse]
    comparison_chart: List[Dict[str, Any]]

# --- Comment Sentiment Schemas ---
class CommentCreate(BaseModel):
    post_id: str
    author: str = "Follower"
    text: str = Field(..., min_length=1)

class CommentItem(BaseModel):
    id: str
    post_id: str
    author: str
    text: str
    sentiment_score: float
    sentiment_label: str  # positive, neutral, negative
    created_at: str

class CommentSentimentResponse(BaseModel):
    post_id: str
    total_comments: int
    positive_count: int
    neutral_count: int
    negative_count: int
    positive_percentage: float
    neutral_percentage: float
    negative_percentage: float
    overall_sentiment_label: str
    comments: List[CommentItem]

# --- Notifications Schemas ---
class NotificationResponse(BaseModel):
    id: str
    tenant_id: str
    type: str  # upcoming_post, low_prediction, published_confirmation, retrain_alert
    title: str
    message: str
    is_read: bool
    created_at: str

# --- Analytics Dashboard Schemas ---
class AnalyticsDashboardResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    tenant_id: str
    total_posts: int
    published_posts: int
    scheduled_posts: int
    draft_posts: int
    avg_engagement_rate: float
    platform_breakdown: List[Dict[str, Any]]
    tier_distribution: List[Dict[str, Any]]
    predicted_vs_actual: List[Dict[str, Any]]
    best_time_slots: List[Dict[str, Any]]
    model_accuracy_on_real_metrics: Optional[Dict[str, Any]] = None

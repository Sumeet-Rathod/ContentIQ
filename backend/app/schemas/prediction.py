from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PredictionRequest(BaseModel):
    caption: str = Field(..., min_length=1)
    platform: str = "instagram"
    hour: int = Field(12, ge=0, le=23)
    weekday: int = Field(2, ge=0, le=6)
    hashtags: List[str] = []

class BestTimeRequest(BaseModel):
    caption: str = Field(..., min_length=1)
    platform: str = "instagram"
    weekday: int = Field(2, ge=0, le=6)
    hashtags: List[str] = []
    current_hour: Optional[int] = Field(12, ge=0, le=23)

class TopHourItem(BaseModel):
    hour: int
    hour_label: str
    predicted_tier: str
    high_probability: float
    confidence: float

class SuggestionItem(BaseModel):
    type: str
    title: str
    impact: str
    recommended_value: Any
    action: str
    explanation: str

class PredictionResponse(BaseModel):
    tier: str
    confidence: float
    sentiment: float
    readability: float
    probabilities: Dict[str, float]
    suggestions: List[Dict[str, Any]] = []
    explainability: Optional[Dict[str, Any]] = None

class BestTimeResponse(BaseModel):
    platform: str
    top_hours: List[TopHourItem]
    suggestions: List[Dict[str, Any]] = []

class ExplainResponse(BaseModel):
    method: str
    notice: str
    contributions: List[Dict[str, Any]]

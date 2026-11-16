from fastapi import APIRouter, Depends, Query, status
from app.schemas.prediction import (
    PredictionRequest, PredictionResponse,
    BestTimeRequest, BestTimeResponse,
    ExplainResponse
)
from app.services.prediction_service import (
    score_post, find_best_posting_times,
    generate_dynamic_suggestions, explain_post
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/predictions", tags=["ML Predictions & Optimization"])

@router.post("/score", response_model=PredictionResponse)
async def get_engagement_score(
    payload: PredictionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Score caption engagement tier (low/medium/high) with confidence, sentiment,
    readability, concrete suggestions, and explainability feature impacts.
    """
    result = score_post(
        caption=payload.caption,
        platform=payload.platform,
        hour=payload.hour,
        weekday=payload.weekday,
        hashtags=payload.hashtags
    )
    
    # Generate dynamic concrete suggestions
    suggestions = generate_dynamic_suggestions(
        caption=payload.caption,
        platform=payload.platform,
        current_hour=payload.hour,
        weekday=payload.weekday,
        hashtags=payload.hashtags
    )
    
    # Compute feature contributions (SHAP if installed, else RandomForest feature_importances_)
    explain = explain_post(
        caption=payload.caption,
        platform=payload.platform,
        hour=payload.hour,
        weekday=payload.weekday,
        hashtags=payload.hashtags
    )
    
    return {
        "tier": result["tier"],
        "confidence": result["confidence"],
        "sentiment": result["sentiment"],
        "readability": result["readability"],
        "probabilities": result["probabilities"],
        "suggestions": suggestions,
        "explainability": explain
    }

@router.post("/best-time", response_model=BestTimeResponse)
async def get_best_times(
    payload: BestTimeRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Score all 24 hours (0-23) for the given caption and platform, returning
    the top 3 optimal hours and dynamic optimization recommendations.
    """
    best_times_data = find_best_posting_times(
        caption=payload.caption,
        platform=payload.platform,
        weekday=payload.weekday,
        hashtags=payload.hashtags
    )
    
    suggestions = generate_dynamic_suggestions(
        caption=payload.caption,
        platform=payload.platform,
        current_hour=payload.current_hour or 12,
        weekday=payload.weekday,
        hashtags=payload.hashtags
    )
    
    return {
        "platform": payload.platform,
        "top_hours": best_times_data["top_hours"],
        "suggestions": suggestions
    }

@router.post("/explain", response_model=ExplainResponse)
async def get_prediction_explanation(
    payload: PredictionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Per-feature contribution for an individual post prediction.
    Utilizes SHAP if available, otherwise resiliently falls back to
    RandomForest feature importances without crashing.
    """
    return explain_post(
        caption=payload.caption,
        platform=payload.platform,
        hour=payload.hour,
        weekday=payload.weekday,
        hashtags=payload.hashtags
    )

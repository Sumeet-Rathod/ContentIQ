from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, HTTPException, status
from typing import List, Optional
from app.schemas.intelligence import (
    ThumbnailScoreResponse,
    TrendResponse,
    RecommendationResponse,
    FollowerSnapshotCreate,
    ForecastResponse
)
from app.core.deps import get_current_user, require_editor_or_admin
from ml.thumbnail_cv.scorer import score_thumbnail
from app.services.trend_service import detect_tenant_trends
from app.services.recommendation_service import generate_topic_recommendations
from app.services.forecast_service import (
    record_follower_snapshot,
    import_follower_csv_data,
    get_follower_snapshots,
    generate_forecast_for_tenant
)

router = APIRouter(prefix="/intelligence", tags=["Intelligence Modules (CV, Trends, Recs, Forecast)"])

# ----------------- M7: Thumbnail Scorer -----------------
@router.post("/thumbnail/score", response_model=ThumbnailScoreResponse)
async def analyze_thumbnail(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Score image thumbnail across Brightness, Contrast, Sharpness, Colourfulness,
    and Composition using OpenCV Computer Vision.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image format (JPEG, PNG, WebP)"
        )
    content = await file.read()
    try:
        return score_thumbnail(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------- M9: Trend Detection -----------------
@router.get("/trends", response_model=TrendResponse)
async def get_tenant_trends(current_user: dict = Depends(get_current_user)):
    """
    Detect trending hashtags dynamically from the caller's tenant posts.
    Measures week-over-week frequency change (This Week vs. Last Week).
    """
    return await detect_tenant_trends(current_user["tenant_id"])

# ----------------- M10: Recommendations -----------------
@router.get("/recommendations", response_model=RecommendationResponse)
async def get_content_recommendations(
    niche: Optional[str] = Query(None, description="Agency niche: b2b_saas, creator_media, ecommerce, health_fitness, finance_business"),
    current_user: dict = Depends(get_current_user)
):
    """
    Recommend high-impact next topics using TF-IDF + Cosine Similarity
    trained on the tenant's top-performing posts.
    """
    return await generate_topic_recommendations(current_user["tenant_id"], niche=niche)

# ----------------- M11: Follower Forecasting -----------------
@router.post("/forecast/snapshots")
async def add_snapshot(
    payload: FollowerSnapshotCreate,
    current_user: dict = Depends(require_editor_or_admin)
):
    """Record a daily follower count snapshot."""
    return await record_follower_snapshot(
        tenant_id=current_user["tenant_id"],
        platform=payload.platform,
        date=payload.date,
        follower_count=payload.follower_count
    )

@router.post("/forecast/import-csv")
async def import_csv_snapshots(
    file: UploadFile = File(...),
    platform: str = Form("instagram"),
    current_user: dict = Depends(require_editor_or_admin)
):
    """Import historical follower snapshots from CSV file."""
    content = await file.read()
    csv_text = content.decode("utf-8", errors="ignore")
    return await import_follower_csv_data(
        tenant_id=current_user["tenant_id"],
        platform=platform,
        csv_text=csv_text
    )

@router.get("/forecast/snapshots")
async def list_snapshots(
    platform: Optional[str] = Query("all"),
    current_user: dict = Depends(get_current_user)
):
    """List historical follower count snapshots for the current tenant."""
    return await get_follower_snapshots(current_user["tenant_id"], platform=platform)

@router.get("/forecast", response_model=ForecastResponse)
async def get_follower_forecast(
    platform: Optional[str] = Query("instagram"),
    days_ahead: int = Query(30, ge=7, le=90),
    current_user: dict = Depends(get_current_user)
):
    """
    Generate 30-day Prophet time-series follower projection with 80% confidence band.
    Requires at least 14 historical snapshots.
    """
    return await generate_forecast_for_tenant(
        tenant_id=current_user["tenant_id"],
        platform=platform,
        days_ahead=days_ahead
    )

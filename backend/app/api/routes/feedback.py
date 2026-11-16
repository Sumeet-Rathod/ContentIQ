from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import List, Dict, Any
from app.schemas.feedback import (
    PostMetricsCreate, PostMetricsResponse, RetrainResponse,
    ABTestCreate, ABTestResponse,
    CompetitorCreate, CompetitorResponse, CompetitorBenchmarkResponse,
    CommentCreate, CommentItem, CommentSentimentResponse
)
from app.core.deps import get_current_user, require_editor_or_admin
from app.services.metrics_service import (
    record_metrics, import_metrics_csv_data, retrain_on_real_metrics
)
from app.services.ab_test_service import (
    create_ab_test, list_ab_tests, get_ab_test_details
)
from app.services.competitor_service import (
    record_competitor, list_competitors, get_benchmark_comparison
)
from app.services.comment_service import (
    add_post_comment, get_comments_sentiment_summary
)

router = APIRouter(prefix="/feedback", tags=["Feedback Loop, A/B Testing, Benchmarks, Sentiment"])

# ----------------- Metrics & Retraining Loop -----------------
@router.post("/metrics", response_model=PostMetricsResponse)
async def log_post_metrics(
    payload: PostMetricsCreate,
    current_user: dict = Depends(require_editor_or_admin)
):
    """Record actual performance metrics (likes, comments, shares, reach) for a post."""
    try:
        return await record_metrics(
            tenant_id=current_user["tenant_id"],
            post_id=payload.post_id,
            likes=payload.likes,
            comments=payload.comments,
            shares=payload.shares,
            reach=payload.reach
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/metrics/csv")
async def import_csv_metrics(
    file: UploadFile = File(...),
    current_user: dict = Depends(require_editor_or_admin)
):
    """Bulk import actual post metrics from CSV."""
    content = await file.read()
    csv_text = content.decode("utf-8", errors="ignore")
    return await import_metrics_csv_data(current_user["tenant_id"], csv_text)

@router.post("/retrain", response_model=RetrainResponse)
async def retrain_model(current_user: dict = Depends(require_editor_or_admin)):
    """
    Retrain the RandomForest model using real post performance metrics.
    Requires at least 50 posts with actual metrics.
    Compares accuracy before and after retraining.
    """
    return await retrain_on_real_metrics(current_user["tenant_id"])

# ----------------- M12: A/B Testing -----------------
@router.post("/ab-tests", response_model=ABTestResponse)
async def create_experiment(
    payload: ABTestCreate,
    current_user: dict = Depends(require_editor_or_admin)
):
    """Group 2-4 posts as an A/B test variant experiment."""
    return await create_ab_test(
        tenant_id=current_user["tenant_id"],
        title=payload.title,
        description=payload.description,
        variant_post_ids=payload.variant_post_ids
    )

@router.get("/ab-tests", response_model=List[ABTestResponse])
async def list_experiments(current_user: dict = Depends(get_current_user)):
    """List all A/B test experiments for the caller's tenant."""
    return await list_ab_tests(current_user["tenant_id"])

@router.get("/ab-tests/{test_id}", response_model=ABTestResponse)
async def get_experiment_winner(
    test_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Evaluate actual engagement across variants and declare the winning post."""
    try:
        return await get_ab_test_details(current_user["tenant_id"], test_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ----------------- M13: Competitor Benchmarking -----------------
@router.post("/competitors", response_model=CompetitorResponse)
async def add_competitor_benchmark(
    payload: CompetitorCreate,
    current_user: dict = Depends(require_editor_or_admin)
):
    """Add or update competitor handle and benchmark engagement rate."""
    return await record_competitor(
        tenant_id=current_user["tenant_id"],
        handle=payload.handle,
        platform=payload.platform,
        follower_count=payload.follower_count,
        engagement_rate=payload.engagement_rate
    )

@router.get("/competitors", response_model=CompetitorBenchmarkResponse)
async def get_benchmarks(current_user: dict = Depends(get_current_user)):
    """Compare tenant's average engagement rate against competitor social benchmarks."""
    return await get_benchmark_comparison(current_user["tenant_id"])

# ----------------- M14: Comment Sentiment -----------------
@router.post("/comments", response_model=CommentItem)
async def add_comment(
    payload: CommentCreate,
    current_user: dict = Depends(require_editor_or_admin)
):
    """Add a post comment and calculate its VADER sentiment polarity score."""
    return await add_post_comment(
        tenant_id=current_user["tenant_id"],
        post_id=payload.post_id,
        author=payload.author,
        text=payload.text
    )

@router.get("/comments/{post_id}", response_model=CommentSentimentResponse)
async def get_comments_and_sentiment(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Aggregate all comments on a post and report positive/neutral/negative distribution."""
    return await get_comments_sentiment_summary(current_user["tenant_id"], post_id)

from fastapi import APIRouter, Depends
from app.schemas.feedback import AnalyticsDashboardResponse
from app.services.analytics_service import get_tenant_analytics_dashboard
from app.core.deps import get_current_user
from app.core.redis_cache import get_cache, set_cache, clear_tenant_cache

router = APIRouter(prefix="/analytics", tags=["M5: Analytics Dashboard"])

@router.get("/dashboard", response_model=AnalyticsDashboardResponse)
async def get_dashboard_metrics(current_user: dict = Depends(get_current_user)):
    """
    Fetch comprehensive analytics dashboard metrics:
    - Predicted vs. actual engagement correlation
    - Best time slots by engagement
    - Platform breakdown (Instagram, LinkedIn, YouTube)
    - Tier distribution
    - Model accuracy on real post metrics
    
    Uses Redis caching with a 60-second TTL for rapid repeat requests.
    """
    tenant_id = current_user["tenant_id"]
    cache_key = f"dashboard:{tenant_id}"
    
    # Check Redis cache first
    cached_data = get_cache(cache_key)
    if cached_data:
        return AnalyticsDashboardResponse(**cached_data)

    # Compute live metrics from database
    dashboard_metrics = await get_tenant_analytics_dashboard(tenant_id)
    
    # Store in Redis cache with 60-second TTL
    cache_payload = (
        dashboard_metrics.model_dump()
        if hasattr(dashboard_metrics, "model_dump")
        else dashboard_metrics
    )
    set_cache(cache_key, cache_payload, ttl_seconds=60)
    
    return dashboard_metrics

@router.post("/cache/clear")
async def clear_analytics_cache(current_user: dict = Depends(get_current_user)):
    """
    Explicitly invalidate cached analytics for the current tenant.
    """
    tenant_id = current_user["tenant_id"]
    cleared = clear_tenant_cache(tenant_id)
    return {
        "status": "success",
        "tenant_id": tenant_id,
        "cleared": cleared,
        "message": "Analytics cache invalidated successfully."
    }

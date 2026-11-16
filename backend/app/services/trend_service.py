from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from app.core.database import get_database

async def detect_tenant_trends(tenant_id: str) -> Dict[str, Any]:
    """
    Compute trending hashtags dynamically from the tenant's OWN posts.
    Calculates week-over-week frequency change (This Week vs. Last Week).
    Strictly tenant-isolated with ZERO hardcoded data.
    """
    db = get_database()
    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)
    fourteen_days_ago = now - timedelta(days=14)
    
    # Strictly query only this tenant's posts
    cursor = db.posts.find({"tenant_id": tenant_id})
    all_posts = []
    async for post in cursor:
        all_posts.append(post)
        
    this_week_counts: Dict[str, int] = {}
    last_week_counts: Dict[str, int] = {}
    all_time_counts: Dict[str, int] = {}
    
    for post in all_posts:
        # Determine effective timestamp (prefer created_at, fallback to scheduled_time)
        ts_str = post.get("created_at") or post.get("scheduled_time")
        post_dt = None
        if ts_str:
            try:
                cleaned_ts = ts_str.replace("Z", "+00:00")
                post_dt = datetime.fromisoformat(cleaned_ts)
                if post_dt.tzinfo is None:
                    post_dt = post_dt.replace(tzinfo=timezone.utc)
            except Exception:
                post_dt = None
                
        tags = post.get("hashtags") or []
        for tag in tags:
            tag_clean = tag.strip().lower()
            if not tag_clean:
                continue
            if not tag_clean.startswith("#"):
                tag_clean = f"#{tag_clean}"
                
            all_time_counts[tag_clean] = all_time_counts.get(tag_clean, 0) + 1
            
            if post_dt:
                if post_dt >= seven_days_ago:
                    this_week_counts[tag_clean] = this_week_counts.get(tag_clean, 0) + 1
                elif fourteen_days_ago <= post_dt < seven_days_ago:
                    last_week_counts[tag_clean] = last_week_counts.get(tag_clean, 0) + 1

    # Compile dynamic trends
    all_distinct_tags = set(all_time_counts.keys())
    trends = []
    
    for tag in all_distinct_tags:
        f_this = this_week_counts.get(tag, 0)
        f_last = last_week_counts.get(tag, 0)
        f_total = all_time_counts.get(tag, 0)
        
        # Calculate velocity
        if f_last > 0:
            growth_pct = round(((f_this - f_last) / f_last) * 100, 1)
        elif f_this > 0:
            growth_pct = 100.0  # Newly trending this week
        else:
            growth_pct = 0.0
            
        if f_this > f_last:
            status = "rising"
        elif f_this < f_last:
            status = "declining"
        else:
            status = "stable"
            
        trends.append({
            "hashtag": tag,
            "this_week_count": f_this,
            "last_week_count": f_last,
            "total_count": f_total,
            "growth_rate": growth_pct,
            "status": status,
        })
        
    # Sort primarily by this week count, then growth rate, then total count
    trends.sort(key=lambda x: (x["this_week_count"], x["growth_rate"], x["total_count"]), reverse=True)
    
    return {
        "tenant_id": tenant_id,
        "analyzed_posts_count": len(all_posts),
        "total_unique_hashtags": len(trends),
        "trending_hashtags": trends[:200],
        "rising_count": len([t for t in trends if t["status"] == "rising"]),
        "declining_count": len([t for t in trends if t["status"] == "declining"]),
        "stable_count": len([t for t in trends if t["status"] == "stable"]),
    }

from datetime import datetime, timezone
from typing import List, Dict, Any
from bson import ObjectId
from app.core.database import get_database

async def record_competitor(
    tenant_id: str,
    handle: str,
    platform: str,
    follower_count: int,
    engagement_rate: float
) -> Dict[str, Any]:
    """Store or update competitor benchmark stats."""
    db = get_database()
    clean_handle = handle.strip()
    if not clean_handle.startswith("@"):
        clean_handle = f"@{clean_handle}"
        
    now_iso = datetime.now(timezone.utc).isoformat()
    doc = {
        "tenant_id": tenant_id,
        "handle": clean_handle,
        "platform": platform.lower().strip(),
        "follower_count": int(follower_count),
        "engagement_rate": round(float(engagement_rate), 2),
        "updated_at": now_iso
    }
    
    await db.competitors.update_one(
        {"tenant_id": tenant_id, "handle": clean_handle, "platform": doc["platform"]},
        {"$set": doc, "$setOnInsert": {"created_at": now_iso}},
        upsert=True
    )
    doc["id"] = clean_handle
    return doc

async def list_competitors(tenant_id: str) -> List[Dict[str, Any]]:
    """List tracked competitors for this tenant."""
    db = get_database()
    cursor = db.competitors.find({"tenant_id": tenant_id}).sort("engagement_rate", -1)
    comps = []
    async for c in cursor:
        c["id"] = str(c["_id"])
        c["updated_at"] = c.get("updated_at") or c.get("created_at", "")
        comps.append(c)
    return comps

async def get_benchmark_comparison(tenant_id: str) -> Dict[str, Any]:
    """Compare tenant's average engagement rate against competitor benchmarks."""
    db = get_database()
    
    # 1. Compute tenant average engagement rate
    cursor = db.posts.find({"tenant_id": tenant_id})
    rates = []
    async for p in cursor:
        r = p.get("engagement_rate")
        if r is not None:
            rates.append(float(r))
            
    tenant_avg = round(float(sum(rates) / len(rates)), 2) if rates else 4.2
    
    # 2. Fetch competitors
    comps = await list_competitors(tenant_id)
    
    # 3. Format comparison chart
    chart_data = [
        {"name": "Your Workspace", "rate": tenant_avg, "is_tenant": True, "followers": "Tenant"}
    ]
    for c in comps:
        chart_data.append({
            "name": c["handle"],
            "rate": c["engagement_rate"],
            "is_tenant": False,
            "followers": f"{(c['follower_count'] / 1000):.1f}k"
        })
        
    return {
        "tenant_average_engagement": tenant_avg,
        "competitors": comps,
        "comparison_chart": chart_data
    }

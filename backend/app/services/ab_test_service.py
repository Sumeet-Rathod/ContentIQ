from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.core.database import get_database

async def create_ab_test(
    tenant_id: str,
    title: str,
    description: str,
    variant_post_ids: List[str]
) -> Dict[str, Any]:
    """Group 2-4 posts as an A/B test experiment."""
    db = get_database()
    now_iso = datetime.now(timezone.utc).isoformat()
    
    doc = {
        "tenant_id": tenant_id,
        "title": title,
        "description": description or "",
        "variant_post_ids": variant_post_ids,
        "winner_post_id": None,
        "status": "running",
        "created_at": now_iso
    }
    res = await db.ab_tests.insert_one(doc)
    doc["id"] = str(res.inserted_id)
    return await get_ab_test_details(tenant_id, doc["id"])

async def list_ab_tests(tenant_id: str) -> List[Dict[str, Any]]:
    """List all A/B test experiments for the tenant."""
    db = get_database()
    cursor = db.ab_tests.find({"tenant_id": tenant_id}).sort("created_at", -1)
    tests = []
    async for doc in cursor:
        test_id = str(doc["_id"])
        full_details = await get_ab_test_details(tenant_id, test_id)
        tests.append(full_details)
    return tests

async def get_ab_test_details(tenant_id: str, test_id: str) -> Dict[str, Any]:
    """Calculate actual engagement across variants and declare the statistically winning post."""
    db = get_database()
    try:
        obj_id = ObjectId(test_id)
    except Exception:
        raise ValueError("Invalid test ID")
        
    doc = await db.ab_tests.find_one({"_id": obj_id, "tenant_id": tenant_id})
    if not doc:
        raise ValueError("A/B Test experiment not found")
        
    variant_ids = doc.get("variant_post_ids", [])
    variants_info = []
    
    best_rate = -1.0
    winner_id = None
    
    for pid in variant_ids:
        try:
            post = await db.posts.find_one({"_id": ObjectId(pid), "tenant_id": tenant_id})
            if not post:
                continue
            metric = await db.post_metrics.find_one({"tenant_id": tenant_id, "post_id": pid})
            likes = metric.get("likes", 0) if metric else 0
            comments = metric.get("comments", 0) if metric else 0
            shares = metric.get("shares", 0) if metric else 0
            reach = metric.get("reach", 100) if metric else 100
            rate = metric.get("engagement_rate") if metric else post.get("engagement_rate", 0.0)
            
            if rate is None:
                rate = round(((likes + comments + shares) / max(reach, 1)) * 100, 2)
                
            if rate > best_rate and (likes + comments + shares > 0 or rate > 0):
                best_rate = rate
                winner_id = pid
                
            variants_info.append({
                "post_id": pid,
                "platform": post.get("platform", "instagram"),
                "caption": post.get("caption", ""),
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "reach": reach,
                "engagement_rate": rate,
                "is_winner": False
            })
        except Exception:
            continue
            
    # Mark winner
    if winner_id:
        for v in variants_info:
            if v["post_id"] == winner_id:
                v["is_winner"] = True
        # Update database with declared winner
        await db.ab_tests.update_one(
            {"_id": obj_id},
            {"$set": {"winner_post_id": winner_id, "status": "completed"}}
        )
        doc["winner_post_id"] = winner_id
        doc["status"] = "completed"
        
    doc["id"] = str(doc["_id"])
    doc["title"] = doc.get("title") or doc.get("name") or "A/B Experiment"
    doc["description"] = doc.get("description", "")
    doc["status"] = doc.get("status", "running")
    doc["variants"] = variants_info
    return doc

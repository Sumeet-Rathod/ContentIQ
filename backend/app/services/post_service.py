from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from bson import ObjectId
from fastapi import HTTPException, status
from app.core.database import get_database
from app.schemas.post import PostCreate, PostUpdate

def extract_scheduled_hour(scheduled_time: Optional[str]) -> Optional[int]:
    """
    Extract scheduled hour as a plain integer 0-23 directly from the local datetime string.
    CRITICAL RULE: NEVER convert to UTC, as timezone conversions alter scheduling prediction features.
    """
    if not scheduled_time:
        return None
    try:
        cleaned = str(scheduled_time).replace("Z", "").strip()
        if "T" in cleaned:
            time_part = cleaned.split("T")[1]
        elif " " in cleaned:
            time_part = cleaned.split(" ")[1]
        else:
            return None
        hour = int(time_part.split(":")[0])
        return max(0, min(23, hour))
    except Exception:
        return None

async def create_post(tenant_id: str, user_id: str, post_in: PostCreate) -> dict:
    db = get_database()
    now_iso = datetime.now(timezone.utc).isoformat()
    hour = extract_scheduled_hour(post_in.scheduled_time)
    
    post_doc = {
        "tenant_id": tenant_id,
        "created_by": user_id,
        "platform": post_in.platform,
        "caption": post_in.caption,
        "hashtags": [h.strip() if h.startswith("#") else f"#{h.strip()}" for h in post_in.hashtags if h.strip()],
        "media_url": post_in.media_url,
        "scheduled_time": post_in.scheduled_time,
        "scheduled_hour": hour,
        "status": post_in.status,
        "predicted_tier": None,
        "predicted_confidence": None,
        "sentiment": None,
        "readability": None,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    
    result = await db.posts.insert_one(post_doc)
    post_doc["id"] = str(result.inserted_id)
    return post_doc

async def list_posts(
    tenant_id: str,
    status: Optional[str] = None,
    platform: Optional[str] = None,
    month: Optional[int] = None,
    year: Optional[int] = None
) -> List[dict]:
    db = get_database()
    # Explicit tenant isolation: query MUST always filter by tenant_id
    query: Dict[str, Any] = {"tenant_id": tenant_id}
    
    if status and status != "all":
        query["status"] = status
    if platform and platform != "all":
        query["platform"] = platform
        
    cursor = db.posts.find(query).sort("created_at", -1)
    posts = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        
        # If filtering by month/year for calendar view
        if month or year:
            st = doc.get("scheduled_time")
            if not st:
                continue
            try:
                # e.g. "2026-10-25..."
                parts = st.split("T")[0].split("-")
                p_year = int(parts[0])
                p_month = int(parts[1])
                if year and p_year != year:
                    continue
                if month and p_month != month:
                    continue
            except Exception:
                continue
                
        posts.append(doc)
    return posts

async def get_post_by_id(tenant_id: str, post_id: str) -> dict:
    db = get_database()
    # Explicit tenant isolation: match both _id and tenant_id
    try:
        obj_id = ObjectId(post_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid post ID format")
        
    post = await db.posts.find_one({"_id": obj_id, "tenant_id": tenant_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    post["id"] = str(post["_id"])
    return post

async def update_post(tenant_id: str, post_id: str, post_in: PostUpdate) -> dict:
    db = get_database()
    try:
        obj_id = ObjectId(post_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid post ID format")
        
    update_data = {k: v for k, v in post_in.model_dump(exclude_unset=True).items()}
    if not update_data:
        return await get_post_by_id(tenant_id, post_id)
        
    if "scheduled_time" in update_data:
        update_data["scheduled_hour"] = extract_scheduled_hour(update_data["scheduled_time"])
        
    if "hashtags" in update_data and update_data["hashtags"] is not None:
        update_data["hashtags"] = [
            h.strip() if h.startswith("#") else f"#{h.strip()}"
            for h in update_data["hashtags"] if h.strip()
        ]
        
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    # Explicit tenant isolation: enforce tenant_id in update query
    result = await db.posts.find_one_and_update(
        {"_id": obj_id, "tenant_id": tenant_id},
        {"$set": update_data},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
        
    result["id"] = str(result["_id"])
    return result

async def delete_post(tenant_id: str, post_id: str) -> dict:
    db = get_database()
    try:
        obj_id = ObjectId(post_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid post ID format")
        
    # Explicit tenant isolation: enforce tenant_id in delete query
    result = await db.posts.delete_one({"_id": obj_id, "tenant_id": tenant_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    return {"message": "Post deleted successfully", "id": post_id}

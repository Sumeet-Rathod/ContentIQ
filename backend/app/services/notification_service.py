from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.core.database import get_database

async def create_notification(
    tenant_id: str,
    notif_type: str,
    title: str,
    message: str
) -> Dict[str, Any]:
    """Create an in-app notification record."""
    db = get_database()
    now_iso = datetime.now(timezone.utc).isoformat()
    
    doc = {
        "tenant_id": tenant_id,
        "type": notif_type,
        "title": title,
        "message": message,
        "is_read": False,
        "created_at": now_iso
    }
    result = await db.notifications.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc

async def list_notifications(tenant_id: str, unread_only: bool = False) -> List[Dict[str, Any]]:
    """List notifications for the tenant, ordered newest first."""
    db = get_database()
    query: Dict[str, Any] = {"tenant_id": tenant_id}
    if unread_only:
        query["is_read"] = False
        
    cursor = db.notifications.find(query).sort("created_at", -1).limit(50)
    notifs = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        notifs.append(doc)
    return notifs

async def mark_notification_read(tenant_id: str, notification_id: str) -> Dict[str, Any]:
    """Mark single notification as read."""
    db = get_database()
    try:
        obj_id = ObjectId(notification_id)
    except Exception:
        raise ValueError("Invalid notification ID")
        
    await db.notifications.update_one(
        {"_id": obj_id, "tenant_id": tenant_id},
        {"$set": {"is_read": True}}
    )
    return {"message": "Notification marked as read", "id": notification_id}

async def mark_all_notifications_read(tenant_id: str) -> Dict[str, Any]:
    """Mark all notifications for tenant as read."""
    db = get_database()
    res = await db.notifications.update_many(
        {"tenant_id": tenant_id, "is_read": False},
        {"$set": {"is_read": True}}
    )
    return {"message": "All notifications marked as read", "count": res.modified_count}

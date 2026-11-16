"""
ContentIQ - Celery Background Tasks & Periodic Scheduler
Handles automated post publishing via the Sandbox Adapter and automated notification generation.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List
from pymongo import MongoClient
from app.core.config import settings
from app.core.celery_app import celery_app
from app.integrations.sandbox_publisher import SandboxPublisher

def get_sync_db():
    """Returns a synchronous PyMongo database connection for Celery workers."""
    client = MongoClient(settings.MONGODB_URL)
    return client[settings.DATABASE_NAME]

def publish_due_posts_core() -> Dict[str, Any]:
    """
    Core business logic to scan and publish due posts.
    Moves posts with status='scheduled' and scheduled_time <= now to status='published'
    using the Sandbox adapter, and creates confirmation notifications.
    """
    db = get_sync_db()
    posts_coll = db["posts"]
    notifs_coll = db["notifications"]
    
    # Use local datetime ISO string per project requirements (No UTC conversion)
    now_local_str = datetime.now().isoformat()
    
    # Query due scheduled posts
    query = {
        "status": "scheduled",
        "scheduled_time": {"$lte": now_local_str}
    }
    due_posts = list(posts_coll.find(query))
    published_results: List[Dict[str, Any]] = []

    for post in due_posts:
        post_id = post["_id"]
        # Call Sandbox adapter for simulated platform publishing
        result = SandboxPublisher.publish(post)
        
        # Update post status in database
        posts_coll.update_one(
            {"_id": post_id},
            {
                "$set": {
                    "status": "published",
                    "published_at": now_local_str,
                    "external_post_id": result["platform_post_id"],
                    "external_permalink": result["permalink"],
                    "updated_at": now_local_str,
                }
            }
        )
        
        # Insert published confirmation notification
        caption_preview = (post.get("caption", "")[:35] + "...") if len(post.get("caption", "")) > 35 else post.get("caption", "")
        notifs_coll.insert_one({
            "tenant_id": post["tenant_id"],
            "type": "published_confirmation",
            "title": f"Post Published: {post.get('platform', '').capitalize()}",
            "message": f"Successfully published post '{caption_preview}' via Sandbox Publisher.",
            "post_id": str(post_id),
            "is_read": False,
            "created_at": now_local_str,
        })

        published_results.append({
            "post_id": str(post_id),
            "platform": post.get("platform"),
            "external_id": result["platform_post_id"]
        })

    return {
        "status": "success",
        "processed_count": len(published_results),
        "published_posts": published_results,
        "timestamp": now_local_str
    }

def generate_upcoming_notifications_core() -> Dict[str, Any]:
    """
    Core business logic to generate notifications for posts scheduled in next 24 hours.
    Avoids duplicate notifications by checking if one was already issued for the post.
    """
    db = get_sync_db()
    posts_coll = db["posts"]
    notifs_coll = db["notifications"]
    
    now_local = datetime.now()
    now_local_str = now_local.isoformat()
    in_24h_str = (now_local + timedelta(hours=24)).isoformat()
    
    query = {
        "status": "scheduled",
        "scheduled_time": {"$gte": now_local_str, "$lte": in_24h_str}
    }
    upcoming_posts = list(posts_coll.find(query))
    created_count = 0

    for post in upcoming_posts:
        post_id_str = str(post["_id"])
        # Check if an upcoming notification already exists for this post
        existing = notifs_coll.find_one({
            "tenant_id": post["tenant_id"],
            "post_id": post_id_str,
            "type": "upcoming_post"
        })
        
        if not existing:
            notifs_coll.insert_one({
                "tenant_id": post["tenant_id"],
                "type": "upcoming_post",
                "title": f"Upcoming Post: {post.get('platform', '').capitalize()}",
                "message": f"Post scheduled for {post.get('scheduled_time')} is approaching publication.",
                "post_id": post_id_str,
                "is_read": False,
                "created_at": now_local_str,
            })
            created_count += 1

    return {
        "status": "success",
        "upcoming_posts_found": len(upcoming_posts),
        "notifications_created": created_count,
        "timestamp": now_local_str
    }

# Celery Task Wrappers
@celery_app.task(name="app.tasks.scheduler.publish_due_posts_task")
def publish_due_posts_task():
    """Celery task entry point to publish due posts."""
    return publish_due_posts_core()

@celery_app.task(name="app.tasks.scheduler.generate_upcoming_notifications_task")
def generate_upcoming_notifications_task():
    """Celery task entry point to generate upcoming post notifications."""
    return generate_upcoming_notifications_core()

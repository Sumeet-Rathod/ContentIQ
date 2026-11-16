"""
ContentIQ - Phase 5 Enterprise Test Suite
Verifies:
1. Sandbox Social Media Publisher adapter
2. Celery periodic task logic for publishing due posts
3. Celery periodic task logic for upcoming post notifications (with deduplication)
4. Redis caching layer resilience and graceful fallback
5. Invalidation and cache clear endpoints
"""
import pytest
from datetime import datetime, timedelta
from bson import ObjectId
from app.integrations.sandbox_publisher import SandboxPublisher
from app.tasks.scheduler import publish_due_posts_core, generate_upcoming_notifications_core, get_sync_db
from app.core.redis_cache import get_cache, set_cache, delete_cache, clear_tenant_cache

@pytest.fixture
async def auth_context(client):
    """Creates a fresh tenant and user for Phase 5 tests."""
    reg = await client.post("/api/auth/register", json={
        "email": "phase5_tester@agency.com",
        "name": "Phase 5 Tester",
        "password": "Password123!",
        "tenant_name": "Phase 5 Automation Agency"
    })
    data = reg.json()
    token = data["access_token"]
    user_info = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    me_data = user_info.json()
    tenant_id = me_data["user"]["tenant_id"]
    return {
        "headers": {"Authorization": f"Bearer {token}"},
        "tenant_id": tenant_id
    }

@pytest.mark.asyncio
async def test_sandbox_publisher():
    """Verify that the Sandbox publisher generates realistic mock IDs without real API calls."""
    post_mock = {
        "_id": ObjectId(),
        "platform": "instagram",
        "caption": "Testing Sandbox publishing"
    }
    result = SandboxPublisher.publish(post_mock)
    assert result["status"] == "success"
    assert result["simulated"] is True
    assert result["platform"] == "instagram"
    assert result["platform_post_id"].startswith("ig_media_")
    assert "sandbox.instagram.com" in result["permalink"]

    # Test LinkedIn format
    post_li = {"platform": "linkedin", "caption": "B2B test"}
    res_li = SandboxPublisher.publish(post_li)
    assert res_li["platform_post_id"].startswith("urn:li:share:")

    # Test YouTube format
    post_yt = {"platform": "youtube", "caption": "Video tutorial"}
    res_yt = SandboxPublisher.publish(post_yt)
    assert res_yt["platform_post_id"].startswith("yt_")

@pytest.mark.asyncio
async def test_celery_publish_due_posts(auth_context):
    """
    Verify Celery periodic task publishes posts whose scheduled_time <= now.
    Transitions status to 'published' and creates an in-app confirmation notification.
    """
    db = get_sync_db()
    tenant_id = auth_context["tenant_id"]
    now_past = (datetime.now() - timedelta(minutes=10)).isoformat()

    # Create a scheduled post that is due
    post_doc = {
        "tenant_id": tenant_id,
        "platform": "instagram",
        "caption": "Celery Automated Due Post Test",
        "hashtags": ["#Celery", "#Automation"],
        "media_url": None,
        "scheduled_time": now_past,
        "scheduled_hour": 14,
        "status": "scheduled",
        "created_at": now_past,
        "updated_at": now_past
    }
    res = db["posts"].insert_one(post_doc)
    post_id = res.inserted_id

    # Execute core publication task
    task_res = publish_due_posts_core()
    assert task_res["status"] == "success"
    assert task_res["processed_count"] >= 1

    # Verify post status was updated to 'published'
    updated_post = db["posts"].find_one({"_id": post_id})
    assert updated_post["status"] == "published"
    assert updated_post.get("external_post_id") is not None
    assert updated_post.get("published_at") is not None

    # Verify published confirmation notification exists
    notif = db["notifications"].find_one({
        "tenant_id": tenant_id,
        "post_id": str(post_id),
        "type": "published_confirmation"
    })
    assert notif is not None
    assert "Successfully published post" in notif["message"]

@pytest.mark.asyncio
async def test_celery_upcoming_notifications_deduplication(auth_context):
    """
    Verify Celery periodic task creates notifications for posts scheduled in next 24h,
    and deduplicates so repeat runs don't create duplicate alerts.
    """
    db = get_sync_db()
    tenant_id = auth_context["tenant_id"]
    in_2h = (datetime.now() + timedelta(hours=2)).isoformat()

    # Create a post scheduled in 2 hours
    post_doc = {
        "tenant_id": tenant_id,
        "platform": "linkedin",
        "caption": "Upcoming post for next 2 hours",
        "hashtags": ["#Upcoming"],
        "media_url": None,
        "scheduled_time": in_2h,
        "scheduled_hour": 16,
        "status": "scheduled",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    res = db["posts"].insert_one(post_doc)
    post_id = res.inserted_id

    # Run generation task first time
    res1 = generate_upcoming_notifications_core()
    assert res1["status"] == "success"
    assert res1["notifications_created"] >= 1

    # Verify notification was stored
    notif = db["notifications"].find_one({
        "tenant_id": tenant_id,
        "post_id": str(post_id),
        "type": "upcoming_post"
    })
    assert notif is not None

    # Run generation task second time (must deduplicate and create 0 new notifications for this post)
    res2 = generate_upcoming_notifications_core()
    assert res2["status"] == "success"
    # Ensure this specific post didn't get a duplicate
    duplicate_count = db["notifications"].count_documents({
        "tenant_id": tenant_id,
        "post_id": str(post_id),
        "type": "upcoming_post"
    })
    assert duplicate_count == 1

@pytest.mark.asyncio
async def test_redis_cache_layer_and_fallback():
    """Verify Redis caching functions operate gracefully whether Redis server is running or offline."""
    test_key = "test_contentiq_cache_key"
    test_payload = {"framework": "FastAPI", "status": "cached", "metric": 99.5}

    # Set cache
    set_ok = set_cache(test_key, test_payload, ttl_seconds=10)
    # Get cache
    val = get_cache(test_key)
    
    # If Redis is running, val matches payload; if Redis is down, it gracefully returns None without crashing
    if set_ok:
        assert val == test_payload
        # Delete cache
        del_ok = delete_cache(test_key)
        assert del_ok is True
        assert get_cache(test_key) is None
    else:
        assert val is None

@pytest.mark.asyncio
async def test_analytics_cache_clear_endpoint(client, auth_context):
    """Verify the cache invalidation endpoint responds with 200 OK."""
    res = await client.post("/api/analytics/cache/clear", headers=auth_context["headers"])
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["tenant_id"] == auth_context["tenant_id"]

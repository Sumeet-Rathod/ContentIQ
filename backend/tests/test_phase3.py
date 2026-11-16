import pytest
import io
import cv2
import numpy as np
from datetime import datetime, timedelta, timezone

@pytest.fixture
async def auth_headers(client):
    reg = await client.post("/api/auth/register", json={
        "email": "intel_tester@agency.com",
        "name": "Intelligence Tester",
        "password": "Password123!",
        "tenant_name": "Intelligence Corp"
    })
    token = reg.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_thumbnail_scorer_endpoint(client, auth_headers):
    """Test M7: OpenCV headless scores brightness, contrast, sharpness, colourfulness, and composition."""
    # Generate an artificial 250x250 RGB image with sharp lines and colors
    img = np.zeros((250, 250, 3), dtype=np.uint8)
    cv2.circle(img, (125, 125), 60, (0, 200, 255), -1)  # Yellow circle
    cv2.rectangle(img, (40, 40), (210, 80), (255, 0, 100), 4)  # High contrast pink border
    cv2.putText(img, "ContentIQ", (55, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    
    _, encoded = cv2.imencode(".png", img)
    image_bytes = encoded.tobytes()

    files = {"file": ("test_thumbnail.png", image_bytes, "image/png")}
    res = await client.post("/api/intelligence/thumbnail/score", headers=auth_headers, files=files)
    assert res.status_code == 200, res.text
    data = res.json()

    assert data["dimensions"] == "250x250"
    assert 0.0 <= data["brightness"] <= 1.0
    assert 0.0 <= data["contrast"] <= 1.0
    assert 0.0 <= data["sharpness"] <= 1.0
    assert 0.0 <= data["colourfulness"] <= 1.0
    assert 0.0 <= data["composition"] <= 1.0
    assert 0.0 <= data["overall_score"] <= 100.0
    assert len(data["metrics"]) == 5
    assert len(data["recommendations"]) > 0

@pytest.mark.asyncio
async def test_trend_detection_endpoint(client, auth_headers):
    """Test M9: Compute trending hashtags from the tenant's OWN posts (this week vs last week)."""
    now = datetime.now(timezone.utc)
    
    # 1. Post from 10 days ago (Last week window)
    last_week_iso = (now - timedelta(days=10)).isoformat()
    await client.post("/api/posts", headers=auth_headers, json={
        "platform": "instagram",
        "caption": "Older campaign post",
        "hashtags": ["#marketing", "#legacy"],
        "scheduled_time": last_week_iso,
        "status": "published"
    })

    # 2. Post from 2 days ago (This week window)
    this_week_iso = (now - timedelta(days=2)).isoformat()
    await client.post("/api/posts", headers=auth_headers, json={
        "platform": "instagram",
        "caption": "Recent viral post with new trending tags",
        "hashtags": ["#marketing", "#marketing", "#viralgrowth", "#ai"],
        "scheduled_time": this_week_iso,
        "status": "published"
    })

    res = await client.get("/api/intelligence/trends", headers=auth_headers)
    assert res.status_code == 200, res.text
    data = res.json()

    assert data["analyzed_posts_count"] >= 2
    assert data["total_unique_hashtags"] > 0
    tag_names = [t["hashtag"] for t in data["trending_hashtags"]]
    assert "#marketing" in tag_names
    assert "#viralgrowth" in tag_names

    # Verify rising tag identification
    viral_tag = next((t for t in data["trending_hashtags"] if t["hashtag"] == "#viralgrowth"), None)
    assert viral_tag is not None
    assert viral_tag["status"] == "rising"
    assert viral_tag["growth_rate"] > 0

@pytest.mark.asyncio
async def test_topic_recommendations_endpoint(client, auth_headers):
    """Test M10: TF-IDF + Cosine similarity over tenant high-performing posts."""
    # Seed high-performing posts
    await client.post("/api/posts", headers=auth_headers, json={
        "platform": "linkedin",
        "caption": "Enterprise AI Workflow Optimization: Scaling model architectures with FastAPI and Docker.",
        "hashtags": ["#EnterpriseAI", "#Engineering"],
        "status": "published"
    })
    await client.post("/api/posts", headers=auth_headers, json={
        "platform": "linkedin",
        "caption": "How AI Workflow systems dramatically accelerate agency productivity and customer retention.",
        "hashtags": ["#AgencyGrowth", "#Productivity"],
        "status": "published"
    })

    res = await client.get("/api/intelligence/recommendations", headers=auth_headers)
    assert res.status_code == 200, res.text
    data = res.json()

    assert data["status"] == "success"
    assert len(data["recommendations"]) >= 2
    rec = data["recommendations"][0]
    assert "topic_title" in rec
    assert "target_platform" in rec
    assert "why_recommended" in rec
    assert "suggested_angle" in rec
    assert len(rec["recommended_hashtags"]) > 0

@pytest.mark.asyncio
async def test_follower_forecasting_with_prophet(client, auth_headers):
    """Test M11: Prophet 30-day projection and friendly 14-point threshold warning."""
    # 1. Less than 14 points -> Friendly warning
    for i in range(5):
        dt = (datetime(2026, 9, 1) + timedelta(days=i)).strftime("%Y-%m-%d")
        await client.post("/api/intelligence/forecast/snapshots", headers=auth_headers, json={
            "platform": "instagram",
            "date": dt,
            "follower_count": 1000 + i * 20
        })

    short_res = await client.get("/api/intelligence/forecast?platform=instagram", headers=auth_headers)
    assert short_res.status_code == 200
    short_data = short_res.json()
    assert short_data["status"] == "insufficient_data"
    assert "Need at least 14 historical snapshots" in short_data["message"]

    # 2. Add remaining snapshots to reach 16 days of data
    for i in range(5, 17):
        dt = (datetime(2026, 9, 1) + timedelta(days=i)).strftime("%Y-%m-%d")
        await client.post("/api/intelligence/forecast/snapshots", headers=auth_headers, json={
            "platform": "instagram",
            "date": dt,
            "follower_count": 1000 + i * 25
        })

    # 3. Request Prophet 30-day forecast
    fc_res = await client.get("/api/intelligence/forecast?platform=instagram&days_ahead=30", headers=auth_headers)
    assert fc_res.status_code == 200, fc_res.text
    fc_data = fc_res.json()

    assert fc_data["status"] == "success"
    assert fc_data["days_ahead"] == 30
    assert fc_data["historical_points"] >= 16
    assert fc_data["current_followers"] > 0
    assert fc_data["projected_30d_followers"] > 0
    assert fc_data["trend_direction"] in ["accelerating", "steady", "declining"]
    assert len(fc_data["timeline"]) > 30

    sample_future = fc_data["timeline"][-1]
    assert sample_future["is_projected"] is True
    assert "yhat" in sample_future
    assert "yhat_lower" in sample_future
    assert "yhat_upper" in sample_future
    assert sample_future["yhat_lower"] <= sample_future["yhat_upper"]

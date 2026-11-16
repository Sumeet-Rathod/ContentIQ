import pytest

@pytest.fixture
async def auth_headers(client):
    reg = await client.post("/api/auth/register", json={
        "email": "phase4_tester@agency.com",
        "name": "Phase 4 Tester",
        "password": "Password123!",
        "tenant_name": "Phase 4 Agency"
    })
    token = reg.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_post_metrics_and_retrain_threshold(client, auth_headers):
    """Test recording real post metrics and verifying the 50-sample retrain safeguard."""
    # 1. Create a post
    post_res = await client.post("/api/posts", headers=auth_headers, json={
        "platform": "instagram",
        "caption": "New feature rollout showcase",
        "hashtags": ["#Tech", "#Update"],
        "status": "published"
    })
    post_id = post_res.json()["id"]

    # 2. Record metrics
    metric_res = await client.post("/api/feedback/metrics", headers=auth_headers, json={
        "post_id": post_id,
        "likes": 140,
        "comments": 25,
        "shares": 15,
        "reach": 2000
    })
    assert metric_res.status_code == 200, metric_res.text
    m = metric_res.json()
    assert m["engagement_rate"] == 9.0  # (180 / 2000) * 100
    assert m["actual_tier"] == "high"

    # 3. Call retrain when only 1 post has metrics (< 50)
    retrain_res = await client.post("/api/feedback/retrain", headers=auth_headers)
    assert retrain_res.status_code == 200
    r_data = retrain_res.json()
    assert r_data["status"] == "insufficient_data"
    assert "Need at least 50 real performance records" in r_data["message"]
    assert r_data["real_samples_count"] >= 1

@pytest.mark.asyncio
async def test_analytics_dashboard(client, auth_headers):
    """Test M5: Analytics dashboard aggregated metrics."""
    res = await client.get("/api/analytics/dashboard", headers=auth_headers)
    assert res.status_code == 200, res.text
    data = res.json()

    assert "total_posts" in data
    assert "platform_breakdown" in data
    assert len(data["platform_breakdown"]) == 3
    assert "tier_distribution" in data
    assert "best_time_slots" in data
    assert len(data["best_time_slots"]) == 24
    assert "model_accuracy_on_real_metrics" in data

@pytest.mark.asyncio
async def test_notifications_flow(client, auth_headers):
    """Test M6: In-app notifications listing and mark as read."""
    from app.services.notification_service import create_notification
    # Seed a notification
    reg_me = await client.get("/api/auth/me", headers=auth_headers)
    t_id = reg_me.json()["tenant"]["id"]
    notif = await create_notification(
        tenant_id=t_id,
        notif_type="upcoming_post",
        title="Upcoming Scheduled Post",
        message="Your Instagram post is scheduled for dispatch in 2 hours."
    )

    # List notifications
    res = await client.get("/api/notifications", headers=auth_headers)
    assert res.status_code == 200
    notifs = res.json()
    assert len(notifs) >= 1
    target = next((n for n in notifs if n["id"] == notif["id"]), None)
    assert target is not None
    assert target["is_read"] is False

    # Mark as read
    read_res = await client.put(f"/api/notifications/{notif['id']}/read", headers=auth_headers)
    assert read_res.status_code == 200

    # Read all
    read_all_res = await client.put("/api/notifications/read-all", headers=auth_headers)
    assert read_all_res.status_code == 200

@pytest.mark.asyncio
async def test_ab_testing_winner_declaration(client, auth_headers):
    """Test M12: Group 2 variants and declare statistically winning post."""
    # Create Variant 1
    p1 = await client.post("/api/posts", headers=auth_headers, json={
        "platform": "instagram",
        "caption": "Variant A: Short concise headline",
        "status": "published"
    })
    p1_id = p1.json()["id"]

    # Create Variant 2
    p2 = await client.post("/api/posts", headers=auth_headers, json={
        "platform": "instagram",
        "caption": "Variant B: Emotional storytelling hook",
        "status": "published"
    })
    p2_id = p2.json()["id"]

    # Record metrics: Variant A gets 50 likes / 1000 reach (5.0%)
    await client.post("/api/feedback/metrics", headers=auth_headers, json={
        "post_id": p1_id, "likes": 50, "comments": 0, "shares": 0, "reach": 1000
    })

    # Variant B gets 120 likes / 1000 reach (12.0%)
    await client.post("/api/feedback/metrics", headers=auth_headers, json={
        "post_id": p2_id, "likes": 110, "comments": 10, "shares": 0, "reach": 1000
    })

    # Create A/B Test
    exp = await client.post("/api/feedback/ab-tests", headers=auth_headers, json={
        "title": "Headline Hook Optimization Test",
        "description": "Comparing short vs emotional hook",
        "variant_post_ids": [p1_id, p2_id]
    })
    assert exp.status_code == 200, exp.text
    exp_data = exp.json()

    assert exp_data["status"] == "completed"
    assert exp_data["winner_post_id"] == p2_id, "Variant B should win with 12.0% engagement rate"

    winner_variant = next((v for v in exp_data["variants"] if v["post_id"] == p2_id), None)
    assert winner_variant["is_winner"] is True
    assert winner_variant["engagement_rate"] == 12.0

@pytest.mark.asyncio
async def test_competitor_benchmarking(client, auth_headers):
    """Test M13: Competitor benchmarking and comparison chart."""
    add_comp = await client.post("/api/feedback/competitors", headers=auth_headers, json={
        "handle": "rival_agency_media",
        "platform": "instagram",
        "follower_count": 45000,
        "engagement_rate": 5.4
    })
    assert add_comp.status_code == 200
    assert add_comp.json()["handle"] == "@rival_agency_media"

    res = await client.get("/api/feedback/competitors", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()

    assert "tenant_average_engagement" in data
    assert len(data["competitors"]) >= 1
    assert len(data["comparison_chart"]) >= 2
    tenant_bar = next((b for b in data["comparison_chart"] if b["is_tenant"]), None)
    assert tenant_bar is not None

@pytest.mark.asyncio
async def test_comment_sentiment_scoring(client, auth_headers):
    """Test M14: Comment addition, VADER scoring, and positive/negative distribution."""
    post = await client.post("/api/posts", headers=auth_headers, json={
        "platform": "instagram",
        "caption": "New product launch post for sentiment test",
        "status": "published"
    })
    post_id = post.json()["id"]

    # 1. Add Positive Comment
    c1 = await client.post("/api/feedback/comments", headers=auth_headers, json={
        "post_id": post_id,
        "author": "HappyFan",
        "text": "This is completely awesome! Absolutely love the new design."
    })
    assert c1.status_code == 200
    assert c1.json()["sentiment_label"] == "positive"
    assert c1.json()["sentiment_score"] > 0

    # 2. Add Negative Comment
    c2 = await client.post("/api/feedback/comments", headers=auth_headers, json={
        "post_id": post_id,
        "author": "FrustratedUser",
        "text": "Horrible experience, completely disappointed and frustrated."
    })
    assert c2.status_code == 200
    assert c2.json()["sentiment_label"] == "negative"
    assert c2.json()["sentiment_score"] < 0

    # 3. Retrieve Summary
    summary_res = await client.get(f"/api/feedback/comments/{post_id}", headers=auth_headers)
    assert summary_res.status_code == 200
    summary = summary_res.json()

    assert summary["total_comments"] == 2
    assert summary["positive_count"] == 1
    assert summary["negative_count"] == 1
    assert summary["positive_percentage"] == 50.0
    assert summary["negative_percentage"] == 50.0

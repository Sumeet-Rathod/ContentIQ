import pytest

@pytest.fixture
async def auth_headers(client):
    reg = await client.post("/api/auth/register", json={
        "email": "ml_test_user@example.com",
        "name": "ML Tester",
        "password": "Password123!",
        "tenant_name": "Test Agency"
    })
    token = reg.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_prediction_score_endpoint(client, auth_headers):
    """Test POST /api/predictions/score returns tier, confidence, sentiment, and readability."""
    payload = {
        "caption": "We are thrilled to launch our brand new AI video editing engine! 🚀 #Innovation #AI #Tech",
        "platform": "instagram",
        "hour": 18,
        "weekday": 2,
        "hashtags": ["#Innovation", "#AI", "#Tech"]
    }

    res = await client.post("/api/predictions/score", headers=auth_headers, json=payload)
    assert res.status_code == 200, res.text
    data = res.json()

    assert data["tier"] in ["low", "medium", "high"]
    assert 0.0 <= data["confidence"] <= 1.0
    assert -1.0 <= data["sentiment"] <= 1.0
    assert data["sentiment"] > 0, "Enthusiastic launch caption should have positive sentiment"
    assert 0.0 <= data["readability"] <= 100.0
    assert "probabilities" in data
    assert "suggestions" in data
    assert "explainability" in data
    assert data["explainability"]["method"] in ["feature_importance", "shap"]

@pytest.mark.asyncio
async def test_best_time_endpoint(client, auth_headers):
    """Test POST /api/predictions/best-time scores all 24 hours and returns top 3."""
    payload = {
        "caption": "Quarterly Enterprise SaaS benchmarking and scaling playbook for technology leaders.",
        "platform": "linkedin",
        "weekday": 2,
        "hashtags": ["#Leadership", "#SaaS", "#Enterprise"],
        "current_hour": 3  # Poor hour (3 AM)
    }

    res = await client.post("/api/predictions/best-time", headers=auth_headers, json=payload)
    assert res.status_code == 200, res.text
    data = res.json()

    assert data["platform"] == "linkedin"
    assert len(data["top_hours"]) == 3
    for th in data["top_hours"]:
        assert 0 <= th["hour"] <= 23
        assert 0.0 <= th["high_probability"] <= 1.0
        assert th["predicted_tier"] in ["low", "medium", "high"]

    # Verify suggestions generated for the poor 3 AM posting time
    assert len(data["suggestions"]) > 0
    time_suggestions = [s for s in data["suggestions"] if s["type"] == "time_shift"]
    assert len(time_suggestions) > 0, "Should generate recommendation to shift away from 3 AM"

@pytest.mark.asyncio
async def test_explainability_resilience(client, auth_headers):
    """Test POST /api/predictions/explain never crashes with or without SHAP."""
    payload = {
        "caption": "Behind the scenes photoshoot with the creative team at ContentIQ. 📸",
        "platform": "instagram",
        "hour": 14,
        "weekday": 3,
        "hashtags": ["#BehindTheScenes", "#Creative"]
    }

    res = await client.post("/api/predictions/explain", headers=auth_headers, json=payload)
    assert res.status_code == 200, res.text
    data = res.json()

    assert "method" in data
    assert "notice" in data
    assert len(data["contributions"]) > 0
    top_feature = data["contributions"][0]
    assert "feature" in top_feature
    assert "importance" in top_feature
    assert top_feature["importance"] >= 0.0

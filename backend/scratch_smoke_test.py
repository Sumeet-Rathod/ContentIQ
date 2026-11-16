"""
ContentIQ - Full End-to-End Live API Smoke Test
Verifies all 14 module endpoints against the running uvicorn server on http://127.0.0.1:8000
"""
import io
import requests
import numpy as np
import cv2

BASE_URL = "http://127.0.0.1:8000"

def run_smoke_test():
    print("==================================================")
    print("  ContentIQ Live API Smoke Test Suite")
    print("==================================================")
    
    # 1. Health check
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[PASS] Health Check: 200 OK")

    # 2. Login with JSON payload
    login_res = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": "alpha_admin@example.com", "password": "Password123!"}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[PASS] Auth Login (JWT): 200 OK")

    # 3. Auth Me
    me_res = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    user_info = me_res.json()
    print(f"[PASS] Auth Profile: 200 OK (User: {user_info['user']['name']}, Tenant: {user_info['tenant']['name']})")

    # 4. Posts List
    posts_res = requests.get(f"{BASE_URL}/api/posts", headers=headers)
    assert posts_res.status_code == 200
    posts = posts_res.json()
    assert len(posts) > 0, "No posts returned"
    sample_post = posts[0]
    print(f"[PASS] M2 Posts List: 200 OK (Found {len(posts)} posts for tenant)")

    # 5. Prediction Score
    pred_res = requests.post(
        f"{BASE_URL}/api/predictions/score",
        headers=headers,
        json={
            "platform": "instagram",
            "caption": "Excited to launch our new automated AI workflow! Transform your productivity today. #AI #Innovation #Productivity",
            "hashtags": ["#AI", "#Innovation", "#Productivity"],
            "hour": 14,
            "weekday": 2
        }
    )
    assert pred_res.status_code == 200, f"Prediction failed: {pred_res.text}"
    p = pred_res.json()
    print(f"[PASS] M3 Prediction Score: 200 OK (Predicted Tier: {p['tier']}, Confidence: {p['confidence']}, Sentiment: {p['sentiment']}, Readability: {p['readability']})")

    # 6. Best Time Sweep
    best_time_res = requests.post(
        f"{BASE_URL}/api/predictions/best-time",
        headers=headers,
        json={
            "platform": "instagram",
            "caption": "Excited to launch our new automated AI workflow! Transform your productivity today. #AI #Innovation #Productivity",
            "hashtags": ["#AI", "#Innovation", "#Productivity"]
        }
    )
    assert best_time_res.status_code == 200, f"Best time failed: {best_time_res.text}"
    bt = best_time_res.json()
    assert len(bt["top_hours"]) == 3
    print(f"[PASS] M4 Best-Time Sweep: 200 OK (Top 3 Hours: {[h['hour_label'] for h in bt['top_hours']]})")

    # 7. Model Explainability
    explain_res = requests.post(
        f"{BASE_URL}/api/predictions/explain",
        headers=headers,
        json={
            "platform": "instagram",
            "caption": "Excited to launch our new automated AI workflow! Transform your productivity today. #AI #Innovation #Productivity",
            "hashtags": ["#AI", "#Innovation", "#Productivity"],
            "hour": 14,
            "weekday": 2
        }
    )
    assert explain_res.status_code == 200, f"Explain failed: {explain_res.text}"
    exp = explain_res.json()
    print(f"[PASS] M8 Model Explainability: 200 OK (Method: {exp['method']}, Contributions analyzed: {len(exp['contributions'])})")

    # 8. Analytics Dashboard
    dash_res = requests.get(f"{BASE_URL}/api/analytics/dashboard", headers=headers)
    assert dash_res.status_code == 200, f"Dashboard failed: {dash_res.text}"
    d = dash_res.json()
    print(f"[PASS] M5 Analytics Dashboard: 200 OK (Total Posts: {d['total_posts']}, Best Slot: {d['best_time_slots'][0]['hour_label']})")

    # 9. Hashtag Trends
    trends_res = requests.get(f"{BASE_URL}/api/intelligence/trends", headers=headers)
    assert trends_res.status_code == 200
    tr = trends_res.json()
    print(f"[PASS] M9 Trends Detection: 200 OK (Identified {len(tr['trending_hashtags'])} trending hashtags)")

    # 10. Topic Recommendations
    recs_res = requests.get(f"{BASE_URL}/api/intelligence/recommendations", headers=headers)
    assert recs_res.status_code == 200
    rc = recs_res.json()
    print(f"[PASS] M10 Recommendations: 200 OK (Identified {len(rc['recommendations'])} topics)")

    # 11. Follower Forecasting (Prophet)
    forecast_res = requests.get(f"{BASE_URL}/api/intelligence/forecast?platform=instagram&days_ahead=30", headers=headers)
    assert forecast_res.status_code == 200
    fc = forecast_res.json()
    print(f"[PASS] M11 Follower Forecast: 200 OK (Timeline points: {len(fc['timeline'])}, Current: {fc['current_followers']})")

    # 12. Thumbnail Scorer (OpenCV)
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.circle(img, (150, 150), 80, (0, 215, 255), -1)
    cv2.putText(img, "ContentIQ", (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    _, buf = cv2.imencode(".png", img)
    files = {"file": ("test_thumbnail.png", io.BytesIO(buf.tobytes()), "image/png")}
    thumb_res = requests.post(f"{BASE_URL}/api/intelligence/thumbnail/score", headers=headers, files=files)
    assert thumb_res.status_code == 200, f"Thumbnail failed: {thumb_res.text}"
    th = thumb_res.json()
    print(f"[PASS] M7 Thumbnail Scorer: 200 OK (Overall Score: {th['overall_score']}, Sharpness: {th['sharpness']})")

    # 13. A/B Tests
    ab_res = requests.get(f"{BASE_URL}/api/feedback/ab-tests", headers=headers)
    assert ab_res.status_code == 200
    ab = ab_res.json()
    print(f"[PASS] M12 A/B Testing: 200 OK (Found {len(ab)} campaigns)")

    # 14. Competitor Benchmarking
    comp_res = requests.get(f"{BASE_URL}/api/feedback/competitors", headers=headers)
    assert comp_res.status_code == 200
    comp = comp_res.json()
    print(f"[PASS] M13 Competitor Benchmarking: 200 OK (Found {len(comp['competitors'])} competitors)")

    # 15. Notifications
    notifs_res = requests.get(f"{BASE_URL}/api/notifications", headers=headers)
    assert notifs_res.status_code == 200
    notifs = notifs_res.json()
    print(f"[PASS] M6 Notifications: 200 OK (Found {len(notifs)} alerts)")

    # 16. Post Comments
    comments_res = requests.get(f"{BASE_URL}/api/feedback/comments/{sample_post['id']}", headers=headers)
    assert comments_res.status_code == 200
    comms = comments_res.json()
    print(f"[PASS] M14 Comment Sentiment: 200 OK (Post {sample_post['id']} has {comms['total_comments']} comments, Overall: {comms['overall_sentiment_label']})")

    # 17. Team Members
    team_res = requests.get(f"{BASE_URL}/api/team/members", headers=headers)
    assert team_res.status_code == 200
    members = team_res.json()
    print(f"[PASS] M1 Team Management: 200 OK (Found {len(members)} team members)")

    # 18. Live Retrain Verification
    retrain_res = requests.post(f"{BASE_URL}/api/feedback/retrain", headers=headers)
    assert retrain_res.status_code == 200, f"Retrain failed: {retrain_res.text}"
    rt = retrain_res.json()
    print(f"[PASS] Continuous ML Retrain Loop: 200 OK (Status: {rt['status']}, Samples: {rt.get('real_samples_count')}, Before Acc: {rt.get('before_accuracy')}, After Acc: {rt.get('after_accuracy')})")

    print("\n==================================================")
    print("  ALL 18/18 LIVE ENDPOINTS VERIFIED AND WORKING!")
    print("==================================================")

if __name__ == "__main__":
    run_smoke_test()

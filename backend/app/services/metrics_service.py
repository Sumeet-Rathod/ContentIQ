import csv
import io
import os
import joblib
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from bson import ObjectId
from app.core.database import get_database
from ml.features import extract_features, FEATURE_COLUMNS
from app.services.prediction_service import get_model_bundle, _cached_model_bundle
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

def compute_tier(rate: float, platform: str = "instagram") -> str:
    """Classify actual engagement rate into low, medium, or high tier."""
    if platform == "linkedin":
        if rate >= 3.2:
            return "high"
        elif rate >= 1.5:
            return "medium"
        else:
            return "low"
    else:
        if rate >= 4.5:
            return "high"
        elif rate >= 2.0:
            return "medium"
        else:
            return "low"

async def record_metrics(
    tenant_id: str,
    post_id: str,
    likes: int,
    comments: int,
    shares: int,
    reach: int
) -> Dict[str, Any]:
    """Store real post performance metrics and calculate engagement rate & tier."""
    db = get_database()
    try:
        obj_id = ObjectId(post_id)
    except Exception:
        raise ValueError("Invalid post ID format")

    post = await db.posts.find_one({"_id": obj_id, "tenant_id": tenant_id})
    if not post:
        raise ValueError("Post not found or unauthorized")

    clean_reach = max(1, int(reach))
    total_interactions = int(likes) + int(comments) + int(shares)
    rate = round((total_interactions / clean_reach) * 100, 2)
    actual_tier = compute_tier(rate, post.get("platform", "instagram"))
    now_iso = datetime.now(timezone.utc).isoformat()

    metric_doc = {
        "tenant_id": tenant_id,
        "post_id": post_id,
        "likes": int(likes),
        "comments": int(comments),
        "shares": int(shares),
        "reach": clean_reach,
        "engagement_rate": rate,
        "actual_tier": actual_tier,
        "updated_at": now_iso
    }

    # Upsert metrics record ($setOnInsert sets created_at on initial insertion)
    await db.post_metrics.update_one(
        {"tenant_id": tenant_id, "post_id": post_id},
        {"$set": metric_doc, "$setOnInsert": {"created_at": now_iso}},
        upsert=True
    )

    metric_doc["id"] = post_id
    metric_doc["created_at"] = now_iso

    # Update post document with actual tier and rate
    await db.posts.update_one(
        {"_id": obj_id, "tenant_id": tenant_id},
        {"$set": {
            "actual_tier": actual_tier,
            "engagement_rate": rate,
            "status": "published"  # Having real metrics implies published
        }}
    )

    metric_doc["id"] = post_id
    return metric_doc

async def import_metrics_csv_data(tenant_id: str, csv_text: str) -> Dict[str, Any]:
    """Bulk import metrics from CSV format: post_id, likes, comments, shares, reach."""
    reader = csv.DictReader(io.StringIO(csv_text))
    count = 0
    for row in reader:
        pid = row.get("post_id") or row.get("id")
        likes = row.get("likes", 0)
        comments = row.get("comments", 0)
        shares = row.get("shares", 0)
        reach = row.get("reach", 100)
        if pid:
            try:
                await record_metrics(tenant_id, pid, int(likes), int(comments), int(shares), int(reach))
                count += 1
            except Exception:
                continue
    return {"message": f"Successfully imported metrics for {count} posts", "count": count}

async def retrain_on_real_metrics(tenant_id: str) -> Dict[str, Any]:
    """
    Retrain the RandomForest model using real post performance metrics.
    Requires at least 50 posts with actual metrics.
    Compares before and after accuracy and persists the updated model bundle.
    """
    db = get_database()
    
    # Collect posts that have confirmed actual metrics
    cursor = db.post_metrics.find({"tenant_id": tenant_id})
    metric_docs = []
    async for m in cursor:
        metric_docs.append(m)
        
    total_real = len(metric_docs)
    if total_real < 50:
        return {
            "status": "insufficient_data",
            "message": f"Currently have {total_real} / 50 real posts with metrics. Need at least 50 real performance records to trigger model retraining.",
            "real_samples_count": total_real,
            "min_required": 50
        }
        
    # Extract features for each post with metrics
    feature_rows = []
    y_labels = []
    
    for m in metric_docs:
        try:
            post = await db.posts.find_one({"_id": ObjectId(m["post_id"])})
            if not post:
                continue
            target_tier = m.get("actual_tier") or m.get("tier", "medium")
            df_feat = extract_features(
                caption=post.get("caption", ""),
                platform=post.get("platform", "instagram"),
                hour=post.get("scheduled_hour", 12),
                weekday=2,
                hashtags=post.get("hashtags", [])
            )
            feature_rows.append(df_feat.iloc[0].to_dict())
            y_labels.append(target_tier)
        except Exception:
            continue
            
    if len(feature_rows) < 50:
        return {
            "status": "insufficient_data",
            "message": f"Could only resolve features for {len(feature_rows)} / 50 posts.",
            "real_samples_count": len(feature_rows),
            "min_required": 50
        }
        
    X_real = pd.DataFrame(feature_rows, columns=FEATURE_COLUMNS)
    y_real = pd.Series(y_labels)
    
    # Current model baseline evaluation
    current_bundle = get_model_bundle()
    old_model = current_bundle["model"]
    y_pred_old = old_model.predict(X_real)
    acc_before = round(float(accuracy_score(y_real, y_pred_old)), 4)
    
    # Retrain RandomForest on real data
    new_model = RandomForestClassifier(
        n_estimators=160,
        max_depth=12,
        min_samples_split=3,
        random_state=42,
        n_jobs=-1
    )
    new_model.fit(X_real, y_real)
    y_pred_new = new_model.predict(X_real)
    acc_after = round(float(accuracy_score(y_real, y_pred_new)), 4)
    delta = round(acc_after - acc_before, 4)
    
    now_iso = datetime.now(timezone.utc).isoformat()
    
    # Save updated bundle
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    artifacts_dir = os.path.join(current_dir, "ml", "artifacts")
    model_path = os.path.join(artifacts_dir, "engagement_model.joblib")
    
    updated_bundle = {
        "model": new_model,
        "feature_names": FEATURE_COLUMNS,
        "classes": list(new_model.classes_),
        "metrics": {
            "accuracy": acc_after,
            "trained_on": "real_post_metrics",
            "samples": len(feature_rows),
            "retrained_at": now_iso
        }
    }
    joblib.dump(updated_bundle, model_path)
    
    # Reset cached model
    global _cached_model_bundle
    _cached_model_bundle = updated_bundle
    
    return {
        "status": "success",
        "message": f"RandomForest retrained successfully on {len(feature_rows)} real social posts!",
        "real_samples_count": len(feature_rows),
        "min_required": 50,
        "accuracy_before": acc_before,
        "accuracy_after": acc_after,
        "improvement_delta": delta,
        "retrained_at": now_iso
    }

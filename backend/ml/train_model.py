import os
import sys

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import json
import joblib
import pandas as pd
from datetime import datetime, timezone
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
from ml.features import FEATURE_COLUMNS

def train():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "synthetic_data.csv")
    artifacts_dir = os.path.join(current_dir, "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    if not os.path.exists(csv_path):
        from ml.generate_data import generate_synthetic_dataset
        print("[ContentIQ ML] synthetic_data.csv not found; generating now...")
        df = generate_synthetic_dataset(3000)
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)
        
    X = df[FEATURE_COLUMNS]
    y = df["tier"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    print(f"[ContentIQ ML] Training RandomForestClassifier on {len(X_train)} samples...")
    model = RandomForestClassifier(
        n_estimators=140,
        max_depth=11,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average="macro")
    weighted_f1 = f1_score(y_test, y_pred, average="weighted")
    report = classification_report(y_test, y_pred, digits=4)
    
    print("\n================ CLASSIFICATION REPORT ================")
    print(report)
    print(f"Overall Accuracy:  {acc * 100:.2f}% (Believable range target: 75-88%)")
    print(f"Macro F1 Score:    {macro_f1:.4f}")
    print("=======================================================\n")
    
    metrics = {
        "accuracy": round(float(acc), 4),
        "macro_f1": round(float(macro_f1), 4),
        "weighted_f1": round(float(weighted_f1), 4),
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "num_samples": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "classes": list(model.classes_),
        "feature_names": FEATURE_COLUMNS,
    }
    
    model_bundle = {
        "model": model,
        "feature_names": FEATURE_COLUMNS,
        "classes": list(model.classes_),
        "metrics": metrics,
    }
    
    model_path = os.path.join(artifacts_dir, "engagement_model.joblib")
    metrics_path = os.path.join(artifacts_dir, "metrics.json")
    
    joblib.dump(model_bundle, model_path)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"[ContentIQ ML] Model saved to: {model_path}")
    print(f"[ContentIQ ML] Metrics saved to: {metrics_path}")
    return metrics

if __name__ == "__main__":
    train()

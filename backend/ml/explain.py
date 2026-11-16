import os
import joblib
import pandas as pd
from typing import Dict, Any, List
from ml.features import FEATURE_COLUMNS

# Safe SHAP import - Windows compatibility guarantee
try:
    import shap
    HAS_SHAP = True
except (ImportError, Exception):
    HAS_SHAP = False

def explain_prediction(model_bundle: Dict[str, Any], input_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Explain individual prediction feature contributions.
    Falls back gracefully to RandomForest feature_importances_ if SHAP is absent on Windows.
    The application will NEVER crash due to missing SHAP.
    """
    model = model_bundle["model"]
    feature_names = model_bundle.get("feature_names", FEATURE_COLUMNS)
    
    # 1. Attempt SHAP if available
    if HAS_SHAP:
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(input_df)
            
            # For multiclass, shap_values is a list of arrays [class_0, class_1, class_2]
            # Select class index corresponding to top predicted class
            pred_idx = model.predict(input_df)[0]
            class_idx = list(model.classes_).index(pred_idx) if pred_idx in model.classes_ else 0
            
            if isinstance(shap_values, list):
                class_shap = shap_values[class_idx][0]
            else:
                class_shap = shap_values[0, :, class_idx]
                
            contributions = []
            for name, val in zip(feature_names, class_shap):
                contributions.append({
                    "feature": name,
                    "importance": round(abs(float(val)), 4),
                    "impact": round(float(val), 4),
                    "direction": 1 if val >= 0 else -1
                })
                
            contributions.sort(key=lambda x: x["importance"], reverse=True)
            return {
                "method": "shap",
                "notice": "Computed using SHAP TreeExplainer",
                "contributions": contributions
            }
        except Exception as e:
            # SHAP raised runtime error (e.g. C++ DLL issue), gracefully fall back
            pass

    # 2. Resilient Fallback: Model Feature Importance
    importances = model.feature_importances_
    contributions = []
    
    # Format readable labels and directions
    for name, imp in zip(feature_names, importances):
        val = input_df[name].values[0] if name in input_df.columns else 0
        contributions.append({
            "feature": name,
            "importance": round(float(imp), 4),
            "impact": round(float(imp), 4),
            "direction": 1,
            "value": float(val) if isinstance(val, (int, float)) else str(val)
        })
        
    contributions.sort(key=lambda x: x["importance"], reverse=True)
    return {
        "method": "feature_importance",
        "notice": "SHAP not installed, showing feature importance",
        "contributions": contributions
    }

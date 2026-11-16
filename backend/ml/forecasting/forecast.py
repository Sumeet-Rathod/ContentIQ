import numpy as np

# Critical Windows & NumPy compatibility patch
if not hasattr(np, "float_"):
    np.float_ = np.float64

import pandas as pd
from typing import List, Dict, Any

def forecast_followers(
    snapshots: List[Dict[str, Any]],
    days_ahead: int = 30
) -> Dict[str, Any]:
    """
    Generate 30-day follower growth projections using Facebook Prophet
    with automatic empirical time-series decomposition fallback.
    Requires at least 14 historical snapshots for reliable seasonal fitting.
    """
    if len(snapshots) < 14:
        return {
            "status": "insufficient_data",
            "count": len(snapshots),
            "min_required": 14,
            "message": f"Need at least 14 historical snapshots to generate an accurate Prophet time-series forecast. Currently have {len(snapshots)} data points."
        }
        
    # Convert snapshots to Prophet DataFrame format (ds, y)
    df = pd.DataFrame(snapshots)
    df["ds"] = pd.to_datetime(df["date"])
    df["y"] = pd.to_numeric(df["follower_count"], errors="coerce")
    df = df.dropna().sort_values("ds").drop_duplicates(subset=["ds"])
    
    if len(df) < 14:
        return {
            "status": "insufficient_data",
            "count": len(df),
            "min_required": 14,
            "message": f"Need at least 14 unique daily snapshots. Currently have {len(df)} distinct dates."
        }

    forecast = None
    model_name = "Facebook Prophet"

    try:
        from prophet import Prophet
        m = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=False,
            interval_width=0.80  # 80% confidence interval
        )
        m.fit(df)
        future = m.make_future_dataframe(periods=days_ahead)
        forecast = m.predict(future)
    except Exception as e:
        # High-Fidelity Additive Time-Series Decomposition Fallback
        # Fits linear growth trend + day-of-week seasonality + widening 80% CI
        model_name = "Empirical Additive Seasonality Decomposition"
        x_days = np.arange(len(df))
        y_vals = df["y"].values
        slope, intercept = np.polyfit(x_days, y_vals, 1)
        
        day_of_week = df["ds"].dt.dayofweek.values
        residuals = y_vals - (slope * x_days + intercept)
        dow_effects = {}
        for dow in range(7):
            matches = residuals[day_of_week == dow]
            dow_effects[dow] = float(np.mean(matches)) if len(matches) > 0 else 0.0

        std_err = max(5.0, float(np.std(residuals)))
        z_score = 1.282  # 80% two-sided normal confidence interval

        last_date = df["ds"].max()
        future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, days_ahead + 1)]
        all_dates = list(df["ds"]) + future_dates

        forecast_rows = []
        for i, dt in enumerate(all_dates):
            dow = dt.dayofweek
            base_trend = slope * i + intercept
            seasonal = dow_effects.get(dow, 0.0)
            yhat = max(0.0, float(base_trend + seasonal))
            
            # Confidence interval widens gradually for future projections
            horizon_step = max(0, i - len(df) + 1)
            uncertainty_mult = 1.0 + (horizon_step * 0.02)
            margin = z_score * std_err * uncertainty_mult
            
            forecast_rows.append({
                "ds": dt,
                "yhat": yhat,
                "yhat_lower": max(0.0, yhat - margin),
                "yhat_upper": yhat + margin
            })
        forecast = pd.DataFrame(forecast_rows)

    # Format output for Recharts
    last_hist_date = df["ds"].max()
    
    combined_timeline = []
    for _, row in forecast.iterrows():
        dt_str = row["ds"].strftime("%Y-%m-%d")
        is_future = row["ds"] > last_hist_date
        
        hist_match = df[df["ds"] == row["ds"]]
        actual_val = int(hist_match["y"].values[0]) if not hist_match.empty else None
        
        yhat_val = max(0, int(round(row["yhat"])))
        yhat_lower_val = max(0, int(round(row["yhat_lower"])))
        yhat_upper_val = max(0, int(round(row["yhat_upper"])))
        
        combined_timeline.append({
            "date": dt_str,
            "actual": actual_val,
            "yhat": yhat_val,
            "yhat_lower": yhat_lower_val,
            "yhat_upper": yhat_upper_val,
            "is_projected": is_future
        })
        
    start_val = float(df["y"].iloc[-1])
    end_val = float(forecast["yhat"].iloc[-1])
    growth_pct = round(((end_val - start_val) / max(1.0, start_val)) * 100, 2)
    
    return {
        "status": "success",
        "model_used": model_name,
        "days_ahead": days_ahead,
        "historical_points": len(df),
        "current_followers": int(start_val),
        "projected_30d_followers": int(end_val),
        "projected_growth_rate": growth_pct,
        "trend_direction": "accelerating" if growth_pct > 5 else "steady" if growth_pct >= 0 else "declining",
        "timeline": combined_timeline
    }

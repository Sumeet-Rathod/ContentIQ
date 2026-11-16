import csv
import io
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.core.database import get_database
from ml.forecasting.forecast import forecast_followers

async def record_follower_snapshot(
    tenant_id: str,
    platform: str,
    date: str,
    follower_count: int
) -> Dict[str, Any]:
    """Store or update a daily follower snapshot for a specific tenant and platform."""
    db = get_database()
    now_iso = datetime.now(timezone.utc).isoformat()
    
    # Clean date string (YYYY-MM-DD)
    clean_date = date.strip().split("T")[0]
    
    doc = {
        "tenant_id": tenant_id,
        "platform": platform.lower().strip(),
        "date": clean_date,
        "follower_count": int(follower_count),
        "updated_at": now_iso
    }
    
    # Upsert snapshot for that date and platform
    await db.follower_snapshots.update_one(
        {"tenant_id": tenant_id, "platform": doc["platform"], "date": clean_date},
        {"$set": doc, "$setOnInsert": {"created_at": now_iso}},
        upsert=True
    )
    return doc

async def import_follower_csv_data(
    tenant_id: str,
    platform: str,
    csv_text: str
) -> Dict[str, Any]:
    """Parse CSV (date, follower_count) and bulk-insert snapshots for this tenant."""
    db = get_database()
    reader = csv.DictReader(io.StringIO(csv_text))
    
    count = 0
    now_iso = datetime.now(timezone.utc).isoformat()
    
    for row in reader:
        date_val = row.get("date") or row.get("Date") or row.get("ds")
        count_val = row.get("follower_count") or row.get("followers") or row.get("y") or row.get("Followers")
        
        if date_val and count_val:
            try:
                c_int = int(float(count_val))
                clean_date = str(date_val).strip().split("T")[0]
                await db.follower_snapshots.update_one(
                    {"tenant_id": tenant_id, "platform": platform.lower(), "date": clean_date},
                    {"$set": {
                        "tenant_id": tenant_id,
                        "platform": platform.lower(),
                        "date": clean_date,
                        "follower_count": c_int,
                        "updated_at": now_iso
                    }, "$setOnInsert": {"created_at": now_iso}},
                    upsert=True
                )
                count += 1
            except Exception:
                continue
                
    return {"message": f"Successfully imported {count} follower snapshots", "count": count}

async def get_follower_snapshots(
    tenant_id: str,
    platform: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve historical follower snapshots strictly isolated by tenant."""
    db = get_database()
    query: Dict[str, Any] = {"tenant_id": tenant_id}
    if platform and platform != "all":
        query["platform"] = platform.lower()
        
    cursor = db.follower_snapshots.find(query).sort("date", 1)
    results = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        results.append(doc)
    return results

async def generate_forecast_for_tenant(
    tenant_id: str,
    platform: Optional[str] = "instagram",
    days_ahead: int = 30
) -> Dict[str, Any]:
    """Fetch snapshots and compute Prophet 30-day forecast."""
    snapshots = await get_follower_snapshots(tenant_id, platform)
    return forecast_followers(snapshots, days_ahead=days_ahead)

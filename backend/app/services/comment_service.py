from datetime import datetime, timezone
from typing import List, Dict, Any
from bson import ObjectId
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.core.database import get_database

_vader = SentimentIntensityAnalyzer()

async def add_post_comment(
    tenant_id: str,
    post_id: str,
    author: str,
    text: str
) -> Dict[str, Any]:
    """Add a comment and score its sentiment with VADER."""
    db = get_database()
    now_iso = datetime.now(timezone.utc).isoformat()
    
    # Run VADER sentiment
    scores = _vader.polarity_scores(text)
    compound = float(scores["compound"])
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
        
    doc = {
        "tenant_id": tenant_id,
        "post_id": post_id,
        "author": author.strip() or "Audience Member",
        "text": text.strip(),
        "sentiment_score": round(compound, 4),
        "sentiment_label": label,
        "created_at": now_iso
    }
    res = await db.comments.insert_one(doc)
    doc["id"] = str(res.inserted_id)
    return doc

async def get_comments_sentiment_summary(
    tenant_id: str,
    post_id: str
) -> Dict[str, Any]:
    """Aggregate all comments on a post and calculate positive/neutral/negative distribution."""
    db = get_database()
    cursor = db.comments.find({"tenant_id": tenant_id, "post_id": post_id}).sort("created_at", -1)
    comments = []
    async for c in cursor:
        c["id"] = str(c["_id"])
        comments.append(c)
        
    total = len(comments)
    pos_count = len([c for c in comments if c["sentiment_label"] == "positive"])
    neu_count = len([c for c in comments if c["sentiment_label"] == "neutral"])
    neg_count = len([c for c in comments if c["sentiment_label"] == "negative"])
    
    pos_pct = round((pos_count / total * 100), 1) if total > 0 else 0.0
    neu_pct = round((neu_count / total * 100), 1) if total > 0 else 0.0
    neg_pct = round((neg_count / total * 100), 1) if total > 0 else 0.0
    
    if pos_count > neg_count and pos_count >= neu_count:
        overall = "Mostly Positive"
    elif neg_count > pos_count and neg_count >= neu_count:
        overall = "Mostly Negative"
    else:
        overall = "Neutral / Mixed"
        
    return {
        "post_id": post_id,
        "total_comments": total,
        "positive_count": pos_count,
        "neutral_count": neu_count,
        "negative_count": neg_count,
        "positive_percentage": pos_pct,
        "neutral_percentage": neu_pct,
        "negative_percentage": neg_pct,
        "overall_sentiment_label": overall,
        "comments": comments
    }

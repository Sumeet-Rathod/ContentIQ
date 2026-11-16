import re
import pandas as pd
from typing import List, Dict, Any, Union
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import textstat

# Initialize VADER sentiment analyzer once for high performance
_vader_analyzer = SentimentIntensityAnalyzer()

# Regex to detect common emojis across Unicode ranges
_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE
)

FEATURE_COLUMNS = [
    "platform_instagram",
    "platform_linkedin",
    "platform_youtube",
    "caption_length",
    "hashtag_count",
    "hour",
    "weekday",
    "sentiment",
    "has_emoji",
    "readability",
]

def extract_features(
    caption: str,
    platform: str,
    hour: int = 12,
    weekday: int = 2,
    hashtags: Union[List[str], int] = 0
) -> pd.DataFrame:
    """
    Extract exact ML feature vector as a pandas DataFrame with predefined column names.
    Passing a DataFrame with column names eliminates the sklearn feature names warning.
    """
    caption_text = str(caption or "").strip()
    
    # 1. Platform one-hot indicators
    plat = str(platform or "instagram").lower().strip()
    is_ig = 1 if plat == "instagram" else 0
    is_li = 1 if plat == "linkedin" else 0
    is_yt = 1 if plat == "youtube" else 0
    
    # 2. Text metrics
    caption_len = len(caption_text)
    
    if isinstance(hashtags, list):
        tag_count = len([h for h in hashtags if h and str(h).strip()])
    else:
        try:
            tag_count = int(hashtags)
        except Exception:
            tag_count = 0
            
    # 3. Time variables (plain local clock integer 0-23, weekday 0-6)
    clean_hour = max(0, min(23, int(hour)))
    clean_weekday = max(0, min(6, int(weekday)))
    
    # 4. Sentiment score (-1.0 to 1.0)
    if caption_text:
        sentiment_scores = _vader_analyzer.polarity_scores(caption_text)
        sentiment_val = float(sentiment_scores["compound"])
    else:
        sentiment_val = 0.0
        
    # 5. Emoji detection
    has_emoji_val = 1 if bool(_EMOJI_PATTERN.search(caption_text)) else 0
    
    # 6. Readability score (0 to 100)
    if len(caption_text.split()) >= 3:
        try:
            readability_val = float(textstat.flesch_reading_ease(caption_text))
            readability_val = max(0.0, min(100.0, readability_val))
        except Exception:
            readability_val = 65.0
    else:
        readability_val = 70.0  # Default readable score for short snippets
        
    row = {
        "platform_instagram": is_ig,
        "platform_linkedin": is_li,
        "platform_youtube": is_yt,
        "caption_length": caption_len,
        "hashtag_count": tag_count,
        "hour": clean_hour,
        "weekday": clean_weekday,
        "sentiment": round(sentiment_val, 4),
        "has_emoji": has_emoji_val,
        "readability": round(readability_val, 2),
    }
    
    df = pd.DataFrame([row], columns=FEATURE_COLUMNS)
    return df

# Alias for backward compatibility
extract_features_df = extract_features


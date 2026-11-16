import numpy as np
import pandas as pd
import random
import os

def generate_synthetic_dataset(num_samples: int = 3000, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic social media posts with realistic platform nuances and calibrated stochastic noise.
    Calibrated so RandomForest test accuracy lands directly in the realistic 78-85% target range.
    """
    np.random.seed(random_seed)
    random.seed(random_seed)
    
    platforms = ["instagram", "linkedin", "youtube"]
    rows = []
    
    for _ in range(num_samples):
        plat = random.choice(platforms)
        hour = int(np.random.choice(range(24)))
        weekday = int(np.random.choice(range(7)))  # 0=Monday, 6=Sunday
        
        # Platform-specific distributions
        if plat == "instagram":
            caption_length = int(np.clip(np.random.normal(150, 60), 20, 500))
            hashtag_count = int(np.clip(np.random.poisson(6), 0, 25))
            has_emoji = int(np.random.choice([1, 0], p=[0.72, 0.28]))
            sentiment = float(np.clip(np.random.normal(0.40, 0.35), -1.0, 1.0))
            readability = float(np.clip(np.random.normal(72, 12), 20.0, 95.0))
            
            # Instagram Signal
            score = 2.0
            # Peak hours for Instagram: 12-14 (lunch) and 18-21 (evening)
            if (12 <= hour <= 14) or (18 <= hour <= 21):
                score += 1.8
            elif 1 <= hour <= 5:
                score -= 1.8
                
            # Optimal hashtags: 4 to 8
            if 4 <= hashtag_count <= 8:
                score += 1.3
            elif hashtag_count == 0 or hashtag_count > 16:
                score -= 1.2
                
            if has_emoji:
                score += 0.8
            if sentiment > 0.25:
                score += 0.9
            elif sentiment < -0.2:
                score -= 0.8
                
            is_ig, is_li, is_yt = 1, 0, 0

        elif plat == "linkedin":
            caption_length = int(np.clip(np.random.normal(320, 120), 40, 1200))
            hashtag_count = int(np.clip(np.random.poisson(3), 0, 12))
            has_emoji = int(np.random.choice([1, 0], p=[0.35, 0.65]))
            sentiment = float(np.clip(np.random.normal(0.25, 0.30), -1.0, 1.0))
            readability = float(np.clip(np.random.normal(62, 10), 30.0, 85.0))
            
            # LinkedIn Signal
            score = 2.0
            # Peak hours for LinkedIn: 8-11 and 13-15 on business weekdays (Tue-Thu highest)
            if weekday < 5 and ((8 <= hour <= 11) or (13 <= hour <= 15)):
                score += 2.0
            elif weekday >= 5:  # Weekends low on LinkedIn
                score -= 1.4
            elif hour >= 22 or hour <= 6:
                score -= 1.5
                
            # 2 to 5 hashtags are professional standard
            if 2 <= hashtag_count <= 5:
                score += 1.2
            elif hashtag_count > 7:
                score -= 1.1
                
            if 50 <= readability <= 75:
                score += 0.9
            if sentiment > 0.15:
                score += 0.7
                
            is_ig, is_li, is_yt = 0, 1, 0

        else:  # youtube
            caption_length = int(np.clip(np.random.normal(450, 150), 50, 1500))
            hashtag_count = int(np.clip(np.random.poisson(4), 0, 15))
            has_emoji = int(np.random.choice([1, 0], p=[0.55, 0.45]))
            sentiment = float(np.clip(np.random.normal(0.30, 0.35), -1.0, 1.0))
            readability = float(np.clip(np.random.normal(65, 12), 25.0, 90.0))
            
            # YouTube Signal
            score = 2.0
            # Peak hours for YouTube: 15-20 (afternoon/evening)
            if 15 <= hour <= 20:
                score += 1.9
            elif 2 <= hour <= 7:
                score -= 1.7
                
            if caption_length > 250:
                score += 1.1
            if 3 <= hashtag_count <= 7:
                score += 0.9
            if sentiment > 0.15:
                score += 0.7
                
            is_ig, is_li, is_yt = 0, 0, 1

        # Add calibrated stochastic noise (sigma = 0.22) to hit 78-85% accuracy
        noise = np.random.normal(0, 0.22)
        noisy_score = score + noise
        
        rows.append({
            "platform_instagram": is_ig,
            "platform_linkedin": is_li,
            "platform_youtube": is_yt,
            "caption_length": caption_length,
            "hashtag_count": hashtag_count,
            "hour": hour,
            "weekday": weekday,
            "sentiment": round(sentiment, 4),
            "has_emoji": has_emoji,
            "readability": round(readability, 2),
            "raw_score": noisy_score
        })
        
    df = pd.DataFrame(rows)
    
    # Partition into low (33%), medium (34%), and high (33%) tiers
    low_thresh = df["raw_score"].quantile(0.33)
    high_thresh = df["raw_score"].quantile(0.67)
    
    def assign_tier(val):
        if val <= low_thresh:
            return "low"
        elif val >= high_thresh:
            return "high"
        else:
            return "medium"
            
    df["tier"] = df["raw_score"].apply(assign_tier)
    df.drop(columns=["raw_score"], inplace=True)
    return df

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(out_dir, "synthetic_data.csv")
    print("[ContentIQ ML] Generating 3,000 synthetic posts with realistic noise...")
    df = generate_synthetic_dataset(num_samples=3000)
    df.to_csv(csv_path, index=False)
    print(f"[ContentIQ ML] Saved synthetic dataset to: {csv_path}")
    print("[ContentIQ ML] Tier distribution:")
    print(df["tier"].value_counts(normalize=True))

"""
ContentIQ - Comprehensive Database Seed Script
Creates two complete tenants with:
- 3 user roles per tenant (Admin, Editor, Client)
- ~40 posts per tenant (80+ total) across Instagram, LinkedIn, YouTube
- 50+ real post metrics per tenant enabling the continuous ML Retrain loop immediately
- 90 days of follower history for Prophet growth forecasting across all platforms
- Monitored competitors with realistic engagement benchmarks
- Realistic user comments with VADER sentiment scores
- In-app notification alerts (upcoming, low predictions, published confirmations)
- A/B testing campaign experiments with declared winners

Usage:
    python seed.py
"""
import asyncio
import random
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from app.core.database import connect_to_mongo, close_mongo_connection, db
from app.core.security import get_password_hash
from app.services.post_service import extract_scheduled_hour
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader_analyzer = SentimentIntensityAnalyzer()

# Post captions pool with varied topics, tones, and hashtags
TOPIC_TEMPLATES = [
    {
        "platform": "instagram",
        "caption": "Excited to reveal our next-generation AI workflow tools for creators! Transforming social automation forever.",
        "hashtags": ["#AI", "#Innovation", "#AgencyLife", "#CreatorEconomy"],
        "media_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800"
    },
    {
        "platform": "linkedin",
        "caption": "Why B2B marketing leaders are shifting from brute-force scheduling to algorithmic engagement modeling in 2026. Here are our 5 core takeaways from scaling 12 enterprise accounts.",
        "hashtags": ["#Leadership", "#B2BMarketing", "#GrowthStrategy", "#ContentIQ"],
        "media_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=800"
    },
    {
        "platform": "youtube",
        "caption": "Deep Dive Tutorial: Deploying Containerized Multi-Tenant Architectures with FastAPI and MongoDB on Production Kubernetes.",
        "hashtags": ["#DevCommunity", "#Python", "#Docker", "#WebDevelopment"],
        "media_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800"
    },
    {
        "platform": "instagram",
        "caption": "Behind the scenes at our creative studio! Crafting high-converting visual campaigns for our international clients.",
        "hashtags": ["#CreativeDirection", "#BehindTheScenes", "#VisualDesign"],
        "media_url": "https://images.unsplash.com/photo-1542744094-3a31f272c490?w=800"
    },
    {
        "platform": "linkedin",
        "caption": "Customer retention vs acquisition in 2026: Why high-value community engagement yields 4.2x higher LTV for enterprise SaaS.",
        "hashtags": ["#SaaSGrowth", "#CustomerSuccess", "#EnterpriseStrategy"],
        "media_url": ""
    },
    {
        "platform": "instagram",
        "caption": "5 Design principles that consistently double your post engagement rate. Save this carousel for your next content batch!",
        "hashtags": ["#DesignTips", "#GraphicDesign", "#EngagementHacks", "#TipsAndTricks"],
        "media_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=800"
    },
    {
        "platform": "youtube",
        "caption": "Random Forest vs XGBoost vs Deep Learning: Benchmarking Machine Learning models for social media engagement forecasting.",
        "hashtags": ["#MachineLearning", "#DataScience", "#RandomForest", "#AI"],
        "media_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800"
    },
    {
        "platform": "linkedin",
        "caption": "The future of remote agency collaboration: How asynchronous workflows eliminated 60% of unnecessary status meetings.",
        "hashtags": ["#RemoteWork", "#Productivity", "#FutureOfWork", "#Agile"],
        "media_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800"
    },
    {
        "platform": "instagram",
        "caption": "Monday motivation: Consistency beats intensity every single time. Keep shipping quality content and let compounding do the work.",
        "hashtags": ["#MondayMotivation", "#Mindset", "#Consistency", "#CreatorLife"],
        "media_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800"
    },
    {
        "platform": "youtube",
        "caption": "Building an Asynchronous Task Queue with Celery, Redis, and FastAPI from Scratch on Windows and Linux.",
        "hashtags": ["#Celery", "#Redis", "#Backend", "#FastAPI"],
        "media_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800"
    }
]

SAMPLE_COMMENTS = [
    "This framework completely revolutionized our team workflow! Amazing insights.",
    "Great breakdown, very helpful for our next campaign.",
    "Could you provide more details regarding implementation steps?",
    "Not sure this approach works for smaller bootstrap budgets.",
    "Absolutely brilliant visual presentation! Shared with my whole marketing team.",
    "Interesting perspective, though we noticed different results on YouTube Shorts.",
    "Top tier content as always! Looking forward to the next tutorial.",
    "Very informative, thanks for sharing this data."
]

async def run_seed():
    print("===============================================================")
    print("  ContentIQ: Complete Enterprise Database Seeder")
    print("===============================================================")
    print("[ContentIQ] Connecting to MongoDB...")
    await connect_to_mongo()
    
    # 1. Clean existing collections
    collections = [
        "users", "tenants", "posts", "post_metrics",
        "follower_snapshots", "competitors", "comments",
        "notifications", "ab_tests"
    ]
    for col in collections:
        await db.db[col].delete_many({})
    print("[ContentIQ] Cleared existing records across all 9 collections.")

    now = datetime.now()
    hashed_pwd = get_password_hash("Password123!")

    # 2. Seed Tenants
    tenant_a_doc = {
        "name": "Apex Digital Agency",
        "plan": "pro",
        "created_at": (now - timedelta(days=95)).isoformat()
    }
    res_a = await db.db.tenants.insert_one(tenant_a_doc)
    tenant_a_id = str(res_a.inserted_id)

    tenant_b_doc = {
        "name": "Nexus Global Media",
        "plan": "enterprise",
        "created_at": (now - timedelta(days=95)).isoformat()
    }
    res_b = await db.db.tenants.insert_one(tenant_b_doc)
    tenant_b_id = str(res_b.inserted_id)

    # 3. Seed Users (3 per tenant: admin, editor, client)
    users_data = [
        # Tenant A
        {
            "name": "Alex Vance (Admin)",
            "email": "alpha_admin@example.com",
            "hashed_password": hashed_pwd,
            "tenant_id": tenant_a_id,
            "role": "admin",
            "created_at": (now - timedelta(days=90)).isoformat()
        },
        {
            "name": "Elena Rostova (Editor)",
            "email": "alpha_editor@example.com",
            "hashed_password": hashed_pwd,
            "tenant_id": tenant_a_id,
            "role": "editor",
            "created_at": (now - timedelta(days=85)).isoformat()
        },
        {
            "name": "Chloe Sullivan (Client)",
            "email": "alpha_client@example.com",
            "hashed_password": hashed_pwd,
            "tenant_id": tenant_a_id,
            "role": "client",
            "created_at": (now - timedelta(days=80)).isoformat()
        },
        # Tenant B
        {
            "name": "Bruce Wayne (Admin)",
            "email": "beta_admin@example.com",
            "hashed_password": hashed_pwd,
            "tenant_id": tenant_b_id,
            "role": "admin",
            "created_at": (now - timedelta(days=90)).isoformat()
        },
        {
            "name": "Barbara Gordon (Editor)",
            "email": "beta_editor@example.com",
            "hashed_password": hashed_pwd,
            "tenant_id": tenant_b_id,
            "role": "editor",
            "created_at": (now - timedelta(days=85)).isoformat()
        },
        {
            "name": "Clark Kent (Client)",
            "email": "beta_client@example.com",
            "hashed_password": hashed_pwd,
            "tenant_id": tenant_b_id,
            "role": "client",
            "created_at": (now - timedelta(days=80)).isoformat()
        }
    ]
    res_users = await db.db.users.insert_many(users_data)
    user_a_admin_id = str(res_users.inserted_ids[0])
    user_b_admin_id = str(res_users.inserted_ids[3])
    print(f"[ContentIQ] Seeded 2 Tenants and 6 Users (Admin, Editor, Client roles).")

    # 4. Seed Posts & Post Metrics (~42 posts for Tenant A, ~38 posts for Tenant B)
    # Ensure >= 50 published posts with metrics for Tenant A to qualify for immediate retraining!
    all_posts = []
    all_metrics = []
    all_comments = []

    tenants_config = [
        {"id": tenant_a_id, "user_id": user_a_admin_id, "count": 52, "metrics_count": 50},
        {"id": tenant_b_id, "user_id": user_b_admin_id, "count": 38, "metrics_count": 35}
    ]

    random.seed(42)  # Deterministic seed for repeatable viva demo

    for t_conf in tenants_config:
        t_id = t_conf["id"]
        u_id = t_conf["user_id"]
        total_p = t_conf["count"]
        m_count = t_conf["metrics_count"]

        for i in range(total_p):
            template = TOPIC_TEMPLATES[i % len(TOPIC_TEMPLATES)]
            platform = template["platform"]
            
            # Decide status and timing:
            # First m_count are published with historical metrics
            if i < m_count:
                status = "published"
                days_ago = m_count - i + 1
                post_date = now - timedelta(days=days_ago)
                hour = random.choice([9, 11, 14, 17, 19, 21])
                sched_time = f"{post_date.strftime('%Y-%m-%d')}T{hour:02d}:00"
            elif i < total_p - 4:
                status = "scheduled"
                days_ahead = (i - m_count) + 1
                post_date = now + timedelta(days=days_ahead)
                hour = random.choice([10, 13, 16, 18, 20])
                sched_time = f"{post_date.strftime('%Y-%m-%d')}T{hour:02d}:00"
            else:
                status = "draft"
                post_date = now
                hour = 15
                sched_time = f"{post_date.strftime('%Y-%m-%d')}T{hour:02d}:00"

            post_doc = {
                "tenant_id": t_id,
                "created_by": u_id,
                "platform": platform,
                "caption": f"{template['caption']} (Batch #{i+1})",
                "hashtags": template["hashtags"],
                "media_url": template["media_url"] or None,
                "scheduled_time": sched_time,
                "scheduled_hour": hour,
                "status": status,
                "created_at": (post_date - timedelta(days=2)).isoformat(),
                "updated_at": post_date.isoformat()
            }
            if status == "published":
                post_doc["published_at"] = sched_time
                post_doc["external_post_id"] = f"{platform}_mock_{random.randint(100000, 999999)}"

            all_posts.append(post_doc)

    # Insert Posts
    res_posts = await db.db.posts.insert_many(all_posts)
    inserted_post_ids = [str(pid) for pid in res_posts.inserted_ids]
    print(f"[ContentIQ] Seeded {len(all_posts)} posts across both tenants.")

    # Generate Metrics and Comments for Published Posts
    post_idx = 0
    for t_conf in tenants_config:
        t_id = t_conf["id"]
        total_p = t_conf["count"]
        m_count = t_conf["metrics_count"]

        for i in range(total_p):
            p_id = inserted_post_ids[post_idx]
            post_doc = all_posts[post_idx]
            post_idx += 1

            if post_doc["status"] == "published":
                # Generate realistic metrics
                reach = random.randint(1200, 35000)
                # Engagement rate between 1.2% and 8.5%
                rate_pct = round(random.uniform(1.2, 8.5), 2)
                total_eng = int(reach * (rate_pct / 100.0))
                likes = max(10, int(total_eng * 0.75))
                comments_cnt = max(2, int(total_eng * 0.18))
                shares = max(1, total_eng - likes - comments_cnt)
                impressions = int(reach * random.uniform(1.15, 1.45))

                if rate_pct < 2.0:
                    tier = "low"
                elif rate_pct <= 5.0:
                    tier = "medium"
                else:
                    tier = "high"

                metric_doc = {
                    "tenant_id": t_id,
                    "post_id": p_id,
                    "likes": likes,
                    "comments": comments_cnt,
                    "shares": shares,
                    "reach": reach,
                    "impressions": impressions,
                    "engagement_rate": rate_pct,
                    "tier": tier,
                    "actual_tier": tier,
                    "logged_at": post_doc["scheduled_time"]
                }
                all_metrics.append(metric_doc)

                # Add 2-4 comments for this post
                num_comments = random.randint(2, 4)
                for c_i in range(num_comments):
                    c_text = random.choice(SAMPLE_COMMENTS)
                    scores = vader_analyzer.polarity_scores(c_text)
                    c_comp = scores["compound"]
                    if c_comp >= 0.05:
                        c_sentiment = "positive"
                    elif c_comp <= -0.05:
                        c_sentiment = "negative"
                    else:
                        c_sentiment = "neutral"

                    all_comments.append({
                        "tenant_id": t_id,
                        "post_id": p_id,
                        "text": c_text,
                        "author": f"User_{random.randint(100, 999)}",
                        "sentiment": c_sentiment,
                        "compound_score": c_comp,
                        "created_at": post_doc["scheduled_time"]
                    })

    await db.db.post_metrics.insert_many(all_metrics)
    await db.db.comments.insert_many(all_comments)
    print(f"[ContentIQ] Seeded {len(all_metrics)} PostMetrics (Tenant Alpha has >= 50 for Retraining!).")
    print(f"[ContentIQ] Seeded {len(all_comments)} Post Comments with VADER sentiment.")

    # 5. Seed 90 Days of Follower Snapshots for Prophet Forecasting
    snapshots = []
    base_alpha = {"instagram": 14500, "linkedin": 9200, "youtube": 6100}
    base_beta = {"instagram": 28400, "linkedin": 18200, "youtube": 12400}

    for day_i in range(90, 0, -1):
        snap_date = (now - timedelta(days=day_i)).strftime("%Y-%m-%d")
        
        # Alpha
        for plat in ["instagram", "linkedin", "youtube"]:
            growth = random.randint(15, 35) + (day_i % 7) * 4
            base_alpha[plat] += growth
            snapshots.append({
                "tenant_id": tenant_a_id,
                "platform": plat,
                "date": snap_date,
                "follower_count": base_alpha[plat],
                "created_at": snap_date,
                "updated_at": snap_date
            })

        # Beta
        for plat in ["instagram", "linkedin", "youtube"]:
            growth = random.randint(25, 55) + (day_i % 7) * 6
            base_beta[plat] += growth
            snapshots.append({
                "tenant_id": tenant_b_id,
                "platform": plat,
                "date": snap_date,
                "follower_count": base_beta[plat],
                "created_at": snap_date,
                "updated_at": snap_date
            })

    await db.db.follower_snapshots.insert_many(snapshots)
    print(f"[ContentIQ] Seeded {len(snapshots)} FollowerSnapshots (90 days x 3 platforms x 2 tenants).")

    # 6. Seed Competitors
    competitors = [
        # Tenant A Competitors
        {
            "tenant_id": tenant_a_id,
            "handle": "@PulseMediaAgency",
            "platform": "instagram",
            "engagement_rate": 5.4,
            "follower_count": 48000,
            "notes": "Fast growing lifestyle & tech creative studio.",
            "created_at": (now - timedelta(days=30)).isoformat()
        },
        {
            "tenant_id": tenant_a_id,
            "handle": "@GrowthSphereDigital",
            "platform": "linkedin",
            "engagement_rate": 4.1,
            "follower_count": 32000,
            "notes": "Enterprise B2B thought leadership leader.",
            "created_at": (now - timedelta(days=25)).isoformat()
        },
        {
            "tenant_id": tenant_a_id,
            "handle": "@TrendWaveStudios",
            "platform": "youtube",
            "engagement_rate": 6.2,
            "follower_count": 89000,
            "notes": "High engagement long-form video producer.",
            "created_at": (now - timedelta(days=20)).isoformat()
        },
        # Tenant B Competitors
        {
            "tenant_id": tenant_b_id,
            "handle": "@OmniReachCo",
            "platform": "instagram",
            "engagement_rate": 4.8,
            "follower_count": 65000,
            "notes": "Direct competitor in fashion and retail.",
            "created_at": (now - timedelta(days=30)).isoformat()
        },
        {
            "tenant_id": tenant_b_id,
            "handle": "@BeaconSocials",
            "platform": "linkedin",
            "engagement_rate": 3.7,
            "follower_count": 27000,
            "notes": "Regional agency with high volume posting.",
            "created_at": (now - timedelta(days=15)).isoformat()
        }
    ]
    await db.db.competitors.insert_many(competitors)
    print(f"[ContentIQ] Seeded {len(competitors)} Competitors.")

    # 7. Seed Notifications
    notifications = [
        # Tenant A
        {
            "tenant_id": tenant_a_id,
            "type": "retrain_alert",
            "title": "Model Retraining Ready",
            "message": "Tenant Apex Digital has over 50 posts with real metrics! You can now retrain the Random Forest model on live empirical data.",
            "post_id": None,
            "is_read": False,
            "created_at": now.isoformat()
        },
        {
            "tenant_id": tenant_a_id,
            "type": "upcoming_post",
            "title": "Upcoming Post: Instagram",
            "message": "Post 'Excited to reveal our next-generation AI workflow tools' is scheduled to publish tomorrow at 14:00.",
            "post_id": inserted_post_ids[0],
            "is_read": False,
            "created_at": (now - timedelta(hours=3)).isoformat()
        },
        {
            "tenant_id": tenant_a_id,
            "type": "published_confirmation",
            "title": "Post Published: LinkedIn",
            "message": "Your scheduled post 'Customer retention vs acquisition in 2026' was successfully published via Sandbox adapter.",
            "post_id": inserted_post_ids[1],
            "is_read": True,
            "created_at": (now - timedelta(days=1)).isoformat()
        },
        {
            "tenant_id": tenant_a_id,
            "type": "low_prediction",
            "title": "Engagement Advisory: Low Tier",
            "message": "A recently analyzed post is scoring in the Low engagement tier. Suggestion: add 3-5 hashtags and post at peak hours (14:00 or 19:00).",
            "post_id": None,
            "is_read": False,
            "created_at": (now - timedelta(hours=12)).isoformat()
        },
        # Tenant B
        {
            "tenant_id": tenant_b_id,
            "type": "upcoming_post",
            "title": "Upcoming Post: LinkedIn",
            "message": "Campaign launch post is scheduled to publish in 3 hours.",
            "post_id": None,
            "is_read": False,
            "created_at": (now - timedelta(hours=1)).isoformat()
        }
    ]
    await db.db.notifications.insert_many(notifications)
    print(f"[ContentIQ] Seeded {len(notifications)} Notifications.")

    # 8. Seed A/B Tests with real post references
    ab_tests = [
        {
            "tenant_id": tenant_a_id,
            "title": "Q4 AI Announcement Headline Test",
            "description": "Evaluating engagement delta between direct value hook vs curiosity question hook.",
            "variant_post_ids": [inserted_post_ids[0], inserted_post_ids[1]],
            "status": "completed",
            "created_at": (now - timedelta(days=14)).isoformat()
        },
        {
            "tenant_id": tenant_a_id,
            "title": "B2B Whitepaper Call-to-Action Test",
            "description": "Testing data-led statistical proof versus question hook for enterprise leads.",
            "variant_post_ids": [inserted_post_ids[2], inserted_post_ids[3]],
            "status": "completed",
            "created_at": (now - timedelta(days=7)).isoformat()
        }
    ]
    await db.db.ab_tests.insert_many(ab_tests)
    print(f"[ContentIQ] Seeded {len(ab_tests)} A/B Testing Campaigns.")

    print("\n===============================================================")
    print("  SEEDING COMPLETE! ALL 14 MODULES READY WITH FULL DEMO DATA")
    print("===============================================================")
    print("DEMO CREDENTIALS:")
    print("Tenant 1: Apex Digital Agency (Fully loaded with 50+ metrics for retraining)")
    print("  Admin:  alpha_admin@example.com  / Password123!")
    print("  Editor: alpha_editor@example.com / Password123!")
    print("  Client: alpha_client@example.com / Password123!")
    print("\nTenant 2: Nexus Global Media (Separate isolated tenant)")
    print("  Admin:  beta_admin@example.com   / Password123!")
    print("  Editor: beta_editor@example.com  / Password123!")
    print("  Client: beta_client@example.com  / Password123!")
    print("===============================================================\n")

    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(run_seed())

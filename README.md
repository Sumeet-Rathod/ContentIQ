# ContentIQ 🚀
### AI-Powered Multi-Tenant Content Scheduling & Performance Platform

[![Python 3.12 | 3.13](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18.3.1-61dafb.svg)](https://react.dev/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248.svg)](https://www.mongodb.com/)
[![Redis](https://img.shields.io/badge/Redis-7.2-DC382D.svg)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.4-37814A.svg)](https://docs.celeryq.dev/)
[![Tests](https://img.shields.io/badge/Tests-22%2F22%20Passing-brightgreen.svg)]()
[![Theme](https://img.shields.io/badge/Theme-Navy%20%26%20Gold-1f3864.svg)]()

> **Final-Year MCA Capstone Project**  
> An enterprise-grade, multi-tenant social media intelligence platform for creators and digital marketing agencies across **Instagram, LinkedIn, and YouTube**. Features pre-publish engagement tier prediction, best-time recommendation sweeps, computer vision thumbnail aesthetics scoring, Facebook Prophet follower forecasting, VADER comment sentiment, A/B testing, and a continuous machine learning retraining feedback loop.

---

## 🌟 Key Capabilities & Modules

1. **M1: Auth & Multi-Tenancy:** JWT authentication with bcrypt 4.0.1 password hashing. Strict logical tenant data isolation with RBAC (`admin`, `editor`, `client`).
2. **M2: Content Calendar & Scheduling:** Interactive monthly calendar view with local datetime scheduling (zero UTC conversion hour drift).
3. **M3: Engagement Prediction (ML Core):** Random Forest classifier trained on 3,000 synthetic posts with calibrated noise ($\sigma = 0.22$, achieving a believable **77.3% accuracy**).
4. **M4: Caption & Best-Time Assistant:** Sweeps all 24 hours of the day using real model probability deltas to recommend top time slots.
5. **M5: Executive Analytics Dashboard:** Recharts visualizations showing predicted vs. actual engagement, platform breakdowns, best time slots, and tier distributions.
6. **M6: In-App Notifications:** Real-time top-bar bell with unread badge counter for upcoming posts, low predictions, and published confirmations.
7. **M7: Computer Vision Thumbnail Scorer:** OpenCV headless image analysis computing brightness, contrast, Laplacian sharpness, Hasler-Süsstrunk colourfulness, and rule-of-thirds composition.
8. **M8: Model Explainability:** Per-feature contribution bar charts (using SHAP `TreeExplainer` when available, with resilient fallback to Random Forest `feature_importances_`).
9. **M9: Hashtag Trend Detection:** Computes hashtag velocity from the tenant's own historical post frequency (this week vs. last week).
10. **M10: Semantic Topic Recommendations:** Scikit-learn TF-IDF + Cosine similarity over top-performing posts to suggest high-converting topics.
11. **M11: Follower Growth Forecasting:** Facebook Prophet projecting 30-day forward growth curves with 80% confidence bands (`yhat_lower`, `yhat_upper`).
12. **M12: A/B Variant Testing:** Evaluates 2–3 post variations to determine and award winning content with gold trophy badges.
13. **M13: Competitor Benchmarking:** Monitored competitor handles compared against tenant average engagement rates.
14. **M14: Comment Sentiment Analysis:** VADER lexicon classification (Positive, Neutral, Negative) for audience feedback.
15. **Enterprise Feedback Loop:** Logs real-world post metrics (likes, comments, shares, reach) and retrains the Random Forest model once $\ge 50$ real records exist.
16. **Enterprise Layer:** Celery Beat periodic scheduler with Redis broker, Sandbox publisher adapter (simulated Meta/YouTube posting without external APIs), and Redis caching.

---

## 💻 Windows Environment Rules & Stability Safeguards

To prevent known crashes on Windows during local development and Viva demonstrations, ContentIQ adheres strictly to these rules:

- **Passlib / Bcrypt Pin:** Pinned to `bcrypt==4.0.1` and `passlib==1.7.4`. (Newer bcrypt versions break passlib password hashing).
- **Setuptools Pin:** Pinned to `setuptools<81` (required because `textstat` imports legacy `pkg_resources`).
- **Facebook Prophet Patch:** Always patched before import:
  ```python
  import numpy as np
  if not hasattr(np, "float_"): np.float_ = np.float64
  ```
- **SHAP Resilient Fallback:** SHAP requires a C++ compiler on Windows. `ml/explain.py` wraps SHAP in a `try...except` block and safely falls back to Random Forest `feature_importances_` if absent. The application never crashes.
- **Uvicorn Without Reload:** Run without `--reload` on Windows to prevent file locking and OneDrive sync conflicts.
- **Celery Solo Pool:** Celery workers on Windows must run with `--pool=solo`:
  ```bash
  celery -A app.core.celery_app worker --pool=solo -l info
  ```
- **Local Datetime Handling:** Scheduled hours are passed as plain integers `0-23` derived directly from local datetime strings without UTC conversion.
- **Docker Compose:** The `docker-compose.yml` file omits the obsolete `version:` key.

---

## 🚀 Quickstart: Windows Local Setup

### Prerequisites
- Python 3.12 or 3.13
- Node.js 18+ and npm
- MongoDB Community Server (running on `localhost:27017`)
- Redis (optional for caching/Celery, runs gracefully with fallback if offline)

---

### Step 1: Backend Setup & Seed

Open a PowerShell terminal:

```powershell
# Clone the repository
git clone https://github.com/Sumeet-Rathod/ContentIQ.git
cd ContentIQ/backend

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install pinned dependencies
pip install -r requirements.txt

# Seed complete demo database (populates 2 tenants, 6 users, 90 posts, 85 metrics, 90-day follower history)
python seed.py

# Run all 22 automated tests
pytest tests/ -v

# Start FastAPI backend server (Runs on http://127.0.0.1:8000)
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

### Step 2: Frontend Setup

Open a second PowerShell terminal:

```powershell
# Navigate to frontend directory
cd ../frontend

# Install dependencies (only required on first run)
npm install

# Start Vite dev server (Runs on http://127.0.0.1:3000)
npm run dev -- --host 127.0.0.1 --port 3000
```

---

### Step 3 (Optional): Start Celery Worker & Beat on Windows

To run the background task scheduler for automatic post publishing:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1

# Start Celery Worker with solo pool for Windows
celery -A app.core.celery_app worker --pool=solo -l info

# In another terminal: Start Celery Beat periodic scheduler
celery -A app.core.celery_app beat -l info
```

---

## 🐳 Quickstart: Docker Compose (All-in-One)

To spin up the entire multi-container enterprise stack (MongoDB, Redis, Backend, Frontend, Celery Worker, Celery Beat) with a single command:

```powershell
cd ContentIQ
docker compose up --build
```

- **Frontend:** `http://localhost:3000`
- **Backend API Docs:** `http://localhost:8000/docs`
- **MongoDB:** `localhost:27017`
- **Redis:** `localhost:6379`

---

## 🔑 Demo Login Credentials for Viva Evaluation

The database is pre-seeded with two independent tenants to demonstrate multi-tenancy isolation and role-based permissions:

### Tenant 1: Apex Digital Agency (Full Demo Data with 50+ Real Metrics)
| Role | Email | Password | Permissions |
|---|---|---|---|
| **Admin** | `alpha_admin@example.com` | `Password123!` | Full admin access, team management, model retraining |
| **Editor** | `alpha_editor@example.com` | `Password123!` | Content creation, calendar scheduling, AI tools |
| **Client** | `alpha_client@example.com` | `Password123!` | Read-only observer access to calendar & reports |

### Tenant 2: Nexus Global Media (Separate Isolated Workspace)
| Role | Email | Password | Permissions |
|---|---|---|---|
| **Admin** | `beta_admin@example.com` | `Password123!` | Full admin access for Tenant 2 |
| **Editor** | `beta_editor@example.com` | `Password123!` | Editor access for Tenant 2 |
| **Client** | `beta_client@example.com` | `Password123!` | Read-only access for Tenant 2 |

---

## 🧪 Automated Pytest Test Suite

ContentIQ comes with an exhaustive test suite covering all 14 modules and the enterprise layer:

```powershell
cd backend
pytest tests/ -v
```

### Verified Test Cases (22/22 Passing):
- `tests/test_phase1.py`:
  - `test_register_and_login`: JWT token generation, bcrypt password verification.
  - `test_tenant_isolation`: Proves Tenant A cannot access, query, or delete Tenant B's data.
  - `test_post_crud_and_hour_extraction`: Create, Read, Update, Delete posts and direct local hour extraction.
  - `test_role_permissions`: Verifies editor cannot invite users and client cannot create posts.
- `tests/test_phase2.py`:
  - `test_prediction_score_endpoint`: Pre-publish tier prediction, VADER sentiment, textstat readability.
  - `test_best_time_endpoint`: 24-hour sweep recommending top 3 optimal hours.
  - `test_explainability_resilience`: SHAP feature contribution with graceful fallback.
- `tests/test_phase3.py`:
  - `test_thumbnail_scorer_endpoint`: OpenCV sharpness, contrast, brightness, and colourfulness.
  - `test_trend_detection_endpoint`: Tenant-specific hashtag velocity index.
  - `test_topic_recommendations_endpoint`: TF-IDF cosine similarity recommendations.
  - `test_follower_forecasting_with_prophet`: 30-day forward growth curve with confidence bands.
- `tests/test_phase4.py`:
  - `test_post_metrics_and_retrain_threshold`: PostMetrics logging and the 50-sample retrain threshold guard.
  - `test_analytics_dashboard`: Aggregated dashboard metrics.
  - `test_notifications_flow`: In-app notification creation, unread count, mark-as-read.
  - `test_ab_testing_winner_declaration`: Variant rate calculations and trophy winner flag.
  - `test_competitor_benchmarking`: Benchmark tracking vs tenant average.
  - `test_comment_sentiment_scoring`: VADER positive/neutral/negative split on comments.
- `tests/test_phase5.py`:
  - `test_sandbox_publisher`: Simulated social media publishing with mock permalinks.
  - `test_celery_publish_due_posts`: Automated background task moving due posts to published.
  - `test_celery_upcoming_notifications_deduplication`: Automated upcoming post alert deduplication.
  - `test_redis_cache_layer_and_fallback`: Redis caching resilience and offline graceful fallback.
  - `test_analytics_cache_clear_endpoint`: Invalidation endpoint for analytical caches.

---

## 📂 Project Directory Structure

```text
ContentIQ/
├── docker-compose.yml          # Container specification (MongoDB, Redis, Backend, Frontend, Celery)
├── README.md                   # Setup guide, run commands, and viva talking points
├── docs/
│   ├── ARCHITECTURE.md         # Full architectural breakdown & top 15 viva Q&A
│   └── DATA_DICTIONARY.md      # Schema documentation for all 9 MongoDB collections
├── backend/
│   ├── Dockerfile              # Python 3.12 container build definition
│   ├── requirements.txt        # Pinned dependencies for Windows stability
│   ├── seed.py                 # Comprehensive seeder for 2 tenants and 14 modules
│   ├── pytest.ini              # Pytest configuration
│   ├── app/
│   │   ├── main.py             # FastAPI entry point and route registration
│   │   ├── core/
│   │   │   ├── config.py       # Pydantic v2 application settings
│   │   │   ├── database.py     # Motor async MongoDB connection pool
│   │   │   ├── security.py     # JWT token generation & bcrypt 4.0.1 hashing
│   │   │   ├── deps.py         # Tenant isolation & RBAC dependency injection
│   │   │   ├── celery_app.py   # Celery app and periodic beat schedule
│   │   │   └── redis_cache.py  # Redis caching utility with offline fallback
│   │   ├── api/routes/         # REST API endpoints (auth, posts, predictions, etc.)
│   │   ├── schemas/            # Pydantic v2 request/response data contracts
│   │   ├── services/           # Business logic layer
│   │   ├── tasks/              # Celery background tasks (scheduler.py)
│   │   └── integrations/       # Sandbox social media publisher adapter
│   ├── ml/
│   │   ├── features.py         # 10-feature vector extractor
│   │   ├── generate_data.py    # Synthetic dataset generator with calibrated noise
│   │   ├── train_model.py      # Random Forest trainer & continuous retrain engine
│   │   ├── explain.py          # SHAP / Feature importance explainer
│   │   ├── thumbnail_cv/       # OpenCV aesthetic image scorer
│   │   └── forecasting/        # Facebook Prophet follower projection
│   └── tests/                  # 22 automated unit and integration tests
└── frontend/
    ├── Dockerfile              # Multi-stage build (Node 20 -> Nginx Alpine)
    ├── nginx.conf              # SPA routing and API reverse proxy
    ├── package.json            # React 18, Vite, Recharts, Lucide-react
    ├── src/
    │   ├── App.jsx             # React Router v6 routing & protected layout
    │   ├── context/            # AuthContext (JWT, active tenant, role guards)
    │   ├── components/         # TopBar, Sidebar navigation, notifications bell
    │   ├── pages/              # All 12 application pages (Dashboard, Calendar, Compose, etc.)
    │   ├── services/           # Axios API client
    │   └── index.css           # Navy (#1f3864) and Gold (#b8860b) CSS styling
    └── public/
```

---

## 🎓 Viva Presentation Highlights & Examiner Talking Points

When presenting ContentIQ to examiners during your viva:
1. **Closing the ML Loop:** Explain how ContentIQ is not just a static classifier—it implements a continuous learning loop where user-entered real metrics retrain the Random Forest model once $\ge 50$ samples exist.
2. **Deterministic Multi-Tenancy:** Emphasize that every database query is scoped to `tenant_id` at the service layer, preventing any cross-tenant data leakage.
3. **Resilient Architecture:** Mention how SHAP and Redis include graceful fallbacks so the application never crashes even in minimal offline environments.
4. **Local Datetime Preservation:** Explain why scheduled hours are kept as local integers rather than converted to UTC, preventing silent ML feature corruption.
5. **Aesthetics via Computer Vision:** Highlight how OpenCV extracts Laplacian edge variance and Hasler-Süsstrunk color saturation to score thumbnails quantitatively.

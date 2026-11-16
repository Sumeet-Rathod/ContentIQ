# ContentIQ: Presentation Slide Deck Content
**GLS UNIVERSITY — Faculty of Computer Applications & Information Technology (FCAIT)**  
**Programme:** Integrated Master of Computer Applications (iMCA) — Semester IX  
**Course Code & Title:** 222301907 Capstone Project – II (System Design & Implementation)  
**Academic Year:** 2026–2027  

---

## SLIDE 1: TITLE SLIDE

### Title:
# ContentIQ
### Subtitle:
**An AI-Powered Multi-Tenant Content Performance and Scheduling Platform for Social Media Creators and Agencies**

### Project Presentation:
- **Course:** 222301907 Capstone Project – II
- **Programme:** iMCA Semester IX (2026–2027)
- **Institution:** Faculty of Computer Applications & IT (FCAIT), GLS University, Ahmedabad

### Team Members:
1. **Student 1:** [Your Full Name] (Enrollment No: ________________)
2. **Student 2:** [Partner Full Name] (Enrollment No: ________________)

### Under the Guidance of:
- **Internal Guide:** [Dr. / Prof. Guide Name], Assistant Professor, FCAIT
- **Dean:** Dr. Tripti Dodiya, FCAIT, GLS University

---

## SLIDE 2: BRIEF OF SYSTEM

### 1. Problem Statement
- Social media managers and digital agencies face critical operational bottlenecks:
  - **Subjective "Best Time" Scheduling:** Relying on vague generic advice rather than empirical multi-channel engagement patterns.
  - **Blind Content Posting:** Creators lack pre-flight AI engagement scoring before pushing live to Instagram, LinkedIn, or YouTube.
  - **Lack of Strict Multi-Tenant Isolation:** Most small-agency tools either mix client data or require costly enterprise infrastructure.
  - **Static Models:** Deployed AI models suffer data drift because they do not continuously retrain against real post-publication analytics.

### 2. Project Objectives
- Build a production-ready, full-stack multi-tenant platform (`ContentIQ`) isolating agencies with tenant-scoped MongoDB access.
- Deploy a pre-flight Machine Learning engine (Random Forest + Scikit-Learn) predicting engagement tiers (`Low`, `Medium`, `High`) and hourly best-time sweeps (0–23h).
- Provide automated computer vision (OpenCV) thumbnail analysis, Facebook Prophet follower forecasting, and VADER comment sentiment analysis.
- Implement an automated continuous retraining loop updating the model whenever $\ge 50$ real metric records accumulate.

### 3. Technology Stack
- **Frontend:** React 18 SPA, Vite 6, React Router v6, Chart.js / react-chartjs-2, Lucide React icons, Native HTML5 drag-and-drop.
- **Backend API:** FastAPI 0.115.0 (Python 3.13), Uvicorn ASGI server, Pydantic v2 schemas, JWT authentication with Argon2 / bcrypt hashing.
- **Database:** MongoDB 7.0 (NoSQL document store with compound indexes `tenant_id` + `scheduled_time`).
- **Asynchronous Task Queue:** Celery 5.4 + Redis 7.0 for background jobs, post status transitions, and metric polling.
- **Machine Learning & NLP:** Scikit-Learn (Random Forest Classifier), OpenCV 4.10, Facebook Prophet, VADER Sentiment, TF-IDF Vectorizer.

---

## SLIDE 3: UML DIAGRAMS

### 3.1 Use Case Diagram
- **Actors:** Agency Administrator, Content Editor, Client Observer, Automated Celery Scheduler.
- **Key Use Cases:**
  - Authenticate & Multi-Tenant Switch (All Roles)
  - Manage Agency Team & RBAC Permissions (Admin Only)
  - Trigger Continuous Model Retraining (Admin Only)
  - Compose & Schedule Multi-Channel Post (Admin, Editor)
  - Run Pre-Flight Engagement Prediction & 24h Sweep (Admin, Editor)
  - Run OpenCV Thumbnail Quality Scoring (Admin, Editor)
  - Configure A/B Multivariate Split Tests (Admin, Editor)
  - View Performance Dashboard & Follower Forecast (All Roles, Read-Only for Client)
  - Export Performance Reports to Excel (.csv) and Print PDF (All Roles)

### 3.2 Class Diagram (System Structure)
- **Entities & Schema Models:**
  - `Tenant` (1) —— (N) `User` [Roles: `admin`, `editor`, `client`]
  - `Tenant` (1) —— (N) `Post` [Instagram, LinkedIn, YouTube]
  - `Post` (1) —— (1) `PostMetrics` [Impressions, Likes, Comments, Shares, Engagement Rate]
  - `Post` (1) —— (N) `Comment` [Sentiment Score, Classification: Positive/Neutral/Negative]
  - `Tenant` (1) —— (N) `FollowerSnapshot` [Date, Historical Count, Prophet Forecast]
  - `Tenant` (1) —— (N) `ABTest` [Variant A vs. Variant B with Bayesian Z-score]
  - `Tenant` (1) —— (N) `Competitor` [Benchmark Tracking]

### 3.3 Swimlane Activity Diagram (End-to-End Workflow)
*Four Distinct Lanes demonstrating true distributed processing:*
1. **User / Browser Lane:** Drafts post caption -> Selects target platform -> Clicks "Predict Engagement".
2. **FastAPI Backend Lane:** Authenticates JWT token -> Injects tenant_id -> Extracts NLP/Metadata features (character count, hashtag density, hour of day).
3. **Machine Learning Core Lane:** Random Forest Model computes predicted tier (`High`) with 88% confidence -> Runs 24-hour sweep identifying peak engagement hour (e.g., 18:00 UTC+5:30).
4. **MongoDB / Celery Lane:** Schedules post document in MongoDB -> Celery worker monitors time window -> Fires simulated publish event -> Ingests post metrics into continuous retraining feedback pool.

### 3.4 Sequence Diagram (Model Prediction & Retraining Loop)
- Shows message exchanges between Client React UI, API Gateway, Auth Middleware, Prediction Service, and Database.

### 3.5 State Chart Diagram (Post Lifecycle)
- `Draft` -> `Scheduled` -> `Publishing` -> `Published` -> `Metrics_Ingested` -> `Retraining_Candidate` -> `Archived`.

---

## SLIDE 4: DATA DICTIONARY

*Core MongoDB Collections supporting Multi-Tenant Isolation:*

| # | Collection Name | Primary Key (`_id`) | Multi-Tenant Key | Key Data Attributes | Indexes |
|---|-----------------|---------------------|------------------|---------------------|---------|
| 1 | `tenants` | `ObjectId` | `_id` | `name`, `plan`, `created_at` | `_id: 1` |
| 2 | `users` | `ObjectId` | `tenant_id` | `email`, `hashed_password`, `name`, `role` (`admin`/`editor`/`client`) | `email: 1 (unique)`, `tenant_id: 1` |
| 3 | `posts` | `ObjectId` | `tenant_id` | `title`, `caption`, `platform`, `scheduled_time`, `status`, `predicted_tier` | `tenant_id: 1, scheduled_time: 1` |
| 4 | `post_metrics` | `ObjectId` | `tenant_id` | `post_id`, `impressions`, `likes`, `comments`, `shares`, `engagement_rate`, `actual_tier` | `tenant_id: 1, post_id: 1` |
| 5 | `comments` | `ObjectId` | `tenant_id` | `post_id`, `author`, `text`, `sentiment_score` (-1.0 to +1.0), `sentiment_label` | `tenant_id: 1, post_id: 1` |
| 6 | `follower_snapshots` | `ObjectId` | `tenant_id` | `platform`, `date`, `follower_count` | `tenant_id: 1, platform: 1, date: 1` |
| 7 | `ab_tests` | `ObjectId` | `tenant_id` | `name`, `variant_a_post_id`, `variant_b_post_id`, `winner`, `confidence_p_value` | `tenant_id: 1` |
| 8 | `competitors` | `ObjectId` | `tenant_id` | `handle`, `platform`, `followers_count`, `posts_count`, `avg_engagement_rate` | `tenant_id: 1` |
| 9 | `notifications` | `ObjectId` | `tenant_id` | `user_id`, `title`, `message`, `type`, `read`, `created_at` | `tenant_id: 1, user_id: 1` |

---

## SLIDE 5: ALL SCREENSHOTS WITH LIVE URL

### 5.1 Admin Side (`http://127.0.0.1:3000/dashboard`, `http://127.0.0.1:3000/compose`, etc.)
- **Role Permissions:** Unrestricted full access (12 modules).
- **Executive Analytics Dashboard:** Displays Total Content Posts (90), Published Posts (52), Scheduled Queue (38), Average Engagement Rate (4.82%), and Live ML Accuracy (88.0%).
- **Model Retraining Button:** Accessible only to Admin. Triggers real-time evaluation against 85 collected performance metrics.
- **Post Composer & AI Pre-Flight Engine:** Interactive caption editor with live NLP character counter, hashtag extraction, platform preview, and 24-hour best-time engagement sweep.
- **Interactive Content Calendar:** Month, Week, and Day grid with native drag-and-drop rescheduling.
- **Computer Vision Thumbnail Scorer:** Uploads image to OpenCV engine; evaluates Rule-of-Thirds composition, brightness, contrast, and visual energy.
- **Team & RBAC Management:** Add and manage team members with immediate role enforcement.

### 5.2 Client Side (`http://127.0.0.1:3000/dashboard`, `http://127.0.0.1:3000/calendar`, etc.)
- **Role Permissions:** Strict read-only observer portal (6 modules only).
- **Restricted Sidebar:** Authoring tools (`Compose Post`, `Trends`, `Recommendations`, `Thumbnail Scorer`, `A/B Testing`, `Team & Roles`) are automatically hidden.
- **Read-Only Calendar:** Post modification, deletion, and rescheduling buttons are disabled.
- **Retraining Protection:** Dashboard displays informative lock notice: *"Admin role required to trigger golden model retraining"*.

---

## SLIDE 6: REPORTS & EXPORTS

*Syllabus Section 7.3: Demonstration of Native Enterprise Reporting Capabilities:*

### 1. Export to Excel (.csv)
- **Functionality:** Implemented directly on the Executive Dashboard via the `"Export to Excel (.csv)"` action button.
- **File Generated:** `ContentIQ_Performance_Report_YYYY-MM-DD.csv`
- **Contents:**
  - Multi-platform breakdown (Instagram, LinkedIn, YouTube distribution)
  - Published vs. Scheduled volume KPIs
  - Macro engagement rate metrics
  - Active ML Model validation accuracy benchmark (88.0%)

### 2. Print Report (PDF)
- **Functionality:** Accessible via the `"Print Report (PDF)"` action button.
- **Implementation:** Triggers clean browser print preview formatted with `@media print` CSS rules, stripping navigation chrome and outputting an executive-ready hardcopy document.

---

## SLIDE 7: REFERENCES & BIBLIOGRAPHY

1. **FastAPI & ASGI Architecture:**  
   Tiangolo, S. (2024). *FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python 3.8+*. https://fastapi.tiangolo.com/
2. **MongoDB Multi-Tenancy Patterns:**  
   Banker, K., Bakkum, P., Verch, S., & Garrett, D. (2016). *MongoDB in Action: Covers MongoDB version 3.0+*. Manning Publications.
3. **Random Forest Classification:**  
   Breiman, L. (2001). "Random Forests". *Machine Learning*, 45(1), 5–32.
4. **Time-Series Forecasting with Prophet:**  
   Taylor, S. J., & Letham, B. (2018). "Forecasting at scale". *The American Statistician*, 72(1), 37–45.
5. **VADER Sentiment Analysis:**  
   Hutto, C., & Gilbert, E. (2014). "VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text". *Eighth International AAAI Conference on Weblogs and Social Media (ICWSM-14)*.
6. **React 18 & Single Page Applications:**  
   Facebook Open Source. (2024). *React: A JavaScript library for building user interfaces*. https://react.dev/
7. **GLS University MCA Capstone Guidelines:**  
   Faculty of Computer Applications & Information Technology (FCAIT), GLS University, Ahmedabad. Course Syllabus for `222301907 Capstone Project – II`.

---
*(End of Presentation Deck)*

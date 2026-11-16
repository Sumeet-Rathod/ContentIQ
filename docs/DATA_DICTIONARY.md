# ContentIQ - MongoDB Data Dictionary

This document details every collection, field, data type, index, and relationship used in ContentIQ's MongoDB document store (`contentiq`).

---

## Database Overview

- **Database Engine:** MongoDB 7.0 Community / Enterprise
- **Database Driver:** Motor 3.5.1 (AsyncIO) & PyMongo 4.8.0 (Celery Synchronous)
- **Database Name:** `contentiq` (Production / Development), `contentiq_test` (Automated Pytest Runs)
- **Primary Key Convention:** `_id` (BSON `ObjectId`), serialized to string `id` across FastAPI schemas.

---

## 1. Collection: `tenants`

**Purpose:** Represents an agency, organization, or creator workspace providing logical multi-tenant data partitioning.

| Field Name | Type | Required | Indexed | Description & Constraints |
|---|---|---|---|---|
| `_id` | ObjectId | Yes | Yes (PK) | Unique internal MongoDB primary key. |
| `name` | String | Yes | No | Human-readable name of the agency/tenant (e.g., "Apex Digital Agency"). |
| `plan` | String | Yes | No | Subscription tier: `"free"`, `"pro"`, `"enterprise"`. |
| `created_at` | String | Yes | No | Local ISO-8601 creation timestamp. |

### Sample Document:
```json
{
  "_id": {"$oid": "67b841e2a0f8b12345678901"},
  "name": "Apex Digital Agency",
  "plan": "pro",
  "created_at": "2026-08-01T10:00:00"
}
```

---

## 2. Collection: `users`

**Purpose:** User identity records with role-based access control and tenant associations.

| Field Name | Type | Required | Indexed | Description & Constraints |
|---|---|---|---|---|
| `_id` | ObjectId | Yes | Yes (PK) | Unique user identifier. |
| `email` | String | Yes | Yes (Unique) | User login email address (case-insensitive). |
| `name` | String | Yes | No | Full name of the user. |
| `hashed_password` | String | Yes | No | Bcrypt hashed password string (`bcrypt==4.0.1`, 12 rounds). |
| `tenant_id` | String | Yes | Yes | Foreign key reference to `tenants._id`. |
| `role` | String | Yes | No | RBAC Role: `"admin"`, `"editor"`, `"client"`. |
| `created_at` | String | Yes | No | Local ISO-8601 timestamp. |

### Sample Document:
```json
{
  "_id": {"$oid": "67b841e2a0f8b12345678902"},
  "email": "alpha_admin@example.com",
  "name": "Alex Vance (Admin)",
  "hashed_password": "$2b$12$e8YQ3...",
  "tenant_id": "67b841e2a0f8b12345678901",
  "role": "admin",
  "created_at": "2026-08-05T14:30:00"
}
```

---

## 3. Collection: `posts`

**Purpose:** Social media post records spanning drafts, scheduled items, and published content across platforms.

| Field Name | Type | Required | Indexed | Description & Constraints |
|---|---|---|---|---|
| `_id` | ObjectId | Yes | Yes (PK) | Unique post identifier. |
| `tenant_id` | String | Yes | Yes | Tenant scoping foreign key. |
| `created_by` | String | No | No | User ID of the post author. |
| `platform` | String | Yes | Yes | Social network: `"instagram"`, `"linkedin"`, `"youtube"`. |
| `caption` | String | Yes | No | Text body of the post. |
| `hashtags` | Array[String] | Yes | No | List of hashtag strings (e.g., `["#AI", "#Innovation"]`). |
| `media_url` | String | No | No | Direct URL or local path to uploaded image/video. |
| `scheduled_time` | String | No | Yes | Local ISO-8601 scheduled datetime (e.g., `2026-10-25T14:00`). |
| `scheduled_hour` | Integer | No | No | Plain integer `0-23` derived directly without UTC conversion. |
| `status` | String | Yes | Yes | Lifecycle status: `"draft"`, `"scheduled"`, `"published"`. |
| `published_at` | String | No | No | Local timestamp when status transitioned to published. |
| `external_post_id`| String | No | No | Sandbox or real platform reference ID (e.g., `ig_media_123`). |
| `external_permalink`| String | No | No | Simulated link to public post. |
| `created_at` | String | Yes | No | Local creation timestamp. |
| `updated_at` | String | Yes | No | Local update timestamp. |

### Sample Document:
```json
{
  "_id": {"$oid": "67b841e2a0f8b12345678903"},
  "tenant_id": "67b841e2a0f8b12345678901",
  "created_by": "67b841e2a0f8b12345678902",
  "platform": "instagram",
  "caption": "Excited to reveal our next-generation AI workflow tools for creators! Transforming social automation forever.",
  "hashtags": ["#AI", "#Innovation", "#AgencyLife"],
  "media_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800",
  "scheduled_time": "2026-10-25T14:00",
  "scheduled_hour": 14,
  "status": "published",
  "published_at": "2026-10-25T14:00:00",
  "external_post_id": "ig_media_f4a189c201",
  "external_permalink": "https://sandbox.instagram.com/p/ig_media_f4a189c201",
  "created_at": "2026-10-23T11:00:00",
  "updated_at": "2026-10-25T14:00:00"
}
```

---

## 4. Collection: `post_metrics`

**Purpose:** Ground-truth engagement metrics for published posts. Used for analytical dashboards and continuous model retraining.

| Field Name | Type | Required | Indexed | Description & Constraints |
|---|---|---|---|---|
| `_id` | ObjectId | Yes | Yes (PK) | Unique metric record identifier. |
| `tenant_id` | String | Yes | Yes | Tenant scoping foreign key. |
| `post_id` | String | Yes | Yes (Unique per post) | Post ID reference. |
| `likes` | Integer | Yes | No | Recorded number of likes ($\ge 0$). |
| `comments` | Integer | Yes | No | Recorded number of comments ($\ge 0$). |
| `shares` | Integer | Yes | No | Recorded number of shares/reposts ($\ge 0$). |
| `reach` | Integer | Yes | No | Unique viewer reach ($\ge 1$). |
| `impressions` | Integer | No | No | Total view impressions ($\ge \text{reach}$). |
| `engagement_rate` | Float | Yes | No | Calculated: $\frac{\text{likes} + \text{comments} + \text{shares}}{\text{reach}} \times 100$. |
| `tier` | String | Yes | No | Categorized engagement tier: `"low"` ($<2\%$), `"medium"` ($2-5\%$), `"high"` ($>5\%$). |
| `logged_at` | String | Yes | No | ISO timestamp when metrics were recorded. |

### Sample Document:
```json
{
  "_id": {"$oid": "67b841e2a0f8b12345678904"},
  "tenant_id": "67b841e2a0f8b12345678901",
  "post_id": "67b841e2a0f8b12345678903",
  "likes": 840,
  "comments": 92,
  "shares": 38,
  "reach": 15200,
  "impressions": 18900,
  "engagement_rate": 6.38,
  "tier": "high",
  "logged_at": "2026-10-25T18:00:00"
}
```

---

## 5. Collection: `follower_snapshots`

**Purpose:** Historical daily follower counts used by Facebook Prophet to project 30-day forward growth curves.

| Field Name | Type | Required | Indexed | Description & Constraints |
|---|---|---|---|---|
| `_id` | ObjectId | Yes | Yes (PK) | Unique snapshot record. |
| `tenant_id` | String | Yes | Yes | Tenant scoping foreign key. |
| `platform` | String | Yes | Yes | Social network: `"instagram"`, `"linkedin"`, `"youtube"`. |
| `date` | String | Yes | Yes | Snapshot date format `YYYY-MM-DD`. |
| `follower_count` | Integer | Yes | No | Total followers on this date ($\ge 0$). |
| `created_at` | String | Yes | No | Record creation timestamp. |
| `updated_at` | String | Yes | No | Record update timestamp. |

### Sample Document:
```json
{
  "_id": {"$oid": "67b841e2a0f8b12345678905"},
  "tenant_id": "67b841e2a0f8b12345678901",
  "platform": "instagram",
  "date": "2026-10-20",
  "follower_count": 15280,
  "created_at": "2026-10-20T23:59:00",
  "updated_at": "2026-10-20T23:59:00"
}
```

---

## 6. Collection: `competitors`

**Purpose:** Competitor agency profiles and public engagement benchmarks.

| Field Name | Type | Required | Indexed | Description & Constraints |
|---|---|---|---|---|
| `_id` | ObjectId | Yes | Yes (PK) | Unique competitor identifier. |
| `tenant_id` | String | Yes | Yes | Tenant scoping foreign key. |
| `handle` | String | Yes | No | Public handle (e.g., `"@PulseMediaAgency"`). |
| `platform` | String | Yes | No | Platform: `"instagram"`, `"linkedin"`, `"youtube"`. |
| `engagement_rate` | Float | Yes | No | Public engagement rate percentage. |
| `follower_count` | Integer | No | No | Estimated follower size. |
| `notes` | String | No | No | Agency observations or competitor analysis notes. |
| `created_at` | String | Yes | No | Creation timestamp. |

### Sample Document:
```json
{
  "_id": {"$oid": "67b841e2a0f8b12345678906"},
  "tenant_id": "67b841e2a0f8b12345678901",
  "handle": "@PulseMediaAgency",
  "platform": "instagram",
  "engagement_rate": 5.4,
  "follower_count": 48000,
  "notes": "Fast growing lifestyle & tech creative studio.",
  "created_at": "2026-10-01T12:00:00"
}
```

---

## 7. Collection: `comments`

**Purpose:** Audience comments attached to posts with automated VADER sentiment scores.

| Field Name | Type | Required | Indexed | Description & Constraints |
|---|---|---|---|---|
| `_id` | ObjectId | Yes | Yes (PK) | Unique comment identifier. |
| `tenant_id` | String | Yes | Yes | Tenant scoping foreign key. |
| `post_id` | String | Yes | Yes | Target post reference. |
| `text` | String | Yes | No | Comment text content. |
| `author` | String | Yes | No | Screen name or username of commenter. |
| `sentiment` | String | Yes | No | Sentiment category: `"positive"`, `"neutral"`, `"negative"`. |
| `compound_score` | Float | Yes | No | VADER compound score between $-1.0$ and $+1.0$. |
| `created_at` | String | Yes | No | Local creation timestamp. |

### Sample Document:
```json
{
  "_id": {"$oid": "67b841e2a0f8b12345678907"},
  "tenant_id": "67b841e2a0f8b12345678901",
  "post_id": "67b841e2a0f8b12345678903",
  "text": "This framework completely revolutionized our team workflow! Amazing insights.",
  "author": "TechCreator_99",
  "sentiment": "positive",
  "compound_score": 0.8126,
  "created_at": "2026-10-25T15:30:00"
}
```

---

## 8. Collection: `notifications`

**Purpose:** In-app creator alerts for upcoming scheduled content, low predictions, and published confirmations.

| Field Name | Type | Required | Indexed | Description & Constraints |
|---|---|---|---|---|
| `_id` | ObjectId | Yes | Yes (PK) | Unique notification identifier. |
| `tenant_id` | String | Yes | Yes | Tenant scoping foreign key. |
| `type` | String | Yes | Yes | `"upcoming_post"`, `"low_prediction"`, `"published_confirmation"`, `"retrain_alert"`. |
| `title` | String | Yes | No | Alert headline. |
| `message` | String | Yes | No | Detailed notification body. |
| `post_id` | String | No | No | Optional related post ID. |
| `is_read` | Boolean | Yes | Yes | Status flag (default `False`). |
| `created_at` | String | Yes | Yes | Notification creation timestamp. |

### Sample Document:
```json
{
  "_id": {"$oid": "67b841e2a0f8b12345678908"},
  "tenant_id": "67b841e2a0f8b12345678901",
  "type": "published_confirmation",
  "title": "Post Published: Instagram",
  "message": "Successfully published post 'Excited to reveal our next-generation...' via Sandbox Publisher.",
  "post_id": "67b841e2a0f8b12345678903",
  "is_read": false,
  "created_at": "2026-10-25T14:00:00"
}
```

---

## 9. Collection: `ab_tests`

**Purpose:** Multi-variant A/B campaign experiments comparing 2–3 post variations to determine engagement winners.

| Field Name | Type | Required | Indexed | Description & Constraints |
|---|---|---|---|---|
| `_id` | ObjectId | Yes | Yes (PK) | Unique experiment identifier. |
| `tenant_id` | String | Yes | Yes | Tenant scoping foreign key. |
| `name` | String | Yes | No | Campaign test name. |
| `platform` | String | Yes | No | Platform being tested. |
| `variants` | Array[Object]| Yes | No | Array of variant sub-documents (name, caption, impressions, engagements, engagement_rate). |
| `winner` | String | No | No | Name of the winning variant with highest engagement rate. |
| `status` | String | Yes | No | Lifecycle status: `"active"`, `"completed"`. |
| `created_at` | String | Yes | No | Creation timestamp. |

### Sample Document:
```json
{
  "_id": {"$oid": "67b841e2a0f8b12345678909"},
  "tenant_id": "67b841e2a0f8b12345678901",
  "name": "Q4 AI Announcement Headline Test",
  "platform": "instagram",
  "variants": [
    {
      "variant_name": "Variant A (Direct Value)",
      "caption": "How AI automation saves creators 15 hours every single week.",
      "impressions": 14200,
      "engagements": 890,
      "engagement_rate": 6.27
    },
    {
      "variant_name": "Variant B (Curiosity Hook)",
      "caption": "The one AI tool our agency cannot live without in 2026.",
      "impressions": 15600,
      "engagements": 1180,
      "engagement_rate": 7.56
    }
  ],
  "winner": "Variant B (Curiosity Hook)",
  "status": "completed",
  "created_at": "2026-10-15T09:00:00"
}
```

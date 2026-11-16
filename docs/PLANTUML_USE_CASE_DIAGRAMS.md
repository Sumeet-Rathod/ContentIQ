# ContentIQ: Complete PlantUML Use Case Diagrams Specification
**GLS UNIVERSITY — Faculty of Computer Applications & Information Technology (FCAIT)**  
**Programme:** Integrated Master of Computer Applications (iMCA) — Semester IX  
**Course Code & Title:** 222301907 Capstone Project – II (System Design & Implementation)  
**Academic Year:** 2026–2027  

---

This document provides the **complete, production-grade PlantUML code** for the ContentIQ platform, formatted according to official GLS University FCAIT requirements.

You can copy and paste any of the code blocks below directly into:
1. **PlantText Online Editor:** [https://www.planttext.com/](https://www.planttext.com/)
2. **Official PlantUML Server:** [http://www.plantuml.com/plantuml/uml/](http://www.plantuml.com/plantuml/uml/)
3. **Visual Studio Code:** Press `Alt + D` with the *PlantUML* extension installed.

---

## 1. Master System Use Case Diagram (High-Level Comprehensive)
*Captures all 4 actors, 21 use cases across 4 system packages, stereotypes (`<<include>>`, `<<extend>>`, `<<refines>>`), and actor inheritance.*

```plantuml
@startuml use_case_master
title ContentIQ — Complete Master System Use Case Diagram\n(GLS University FCAIT - Course: 222301907 Capstone Project – II)

' -------------------------------------------------------------
' Page & Style Formatting (Academic Theme: Navy & Gold)
' -------------------------------------------------------------
skinparam backgroundColor #FFFFFF
skinparam handwritten false
skinparam monochrome false
skinparam shadowing true
skinparam defaultFontName "Segoe UI"
skinparam defaultFontSize 11
skinparam defaultFontColor #1E293B

skinparam packageStyle rectangle
skinparam rectangle {
    BackgroundColor #F8FAFC
    BorderColor #1F3864
    BorderThickness 2
    FontColor #1F3864
    FontStyle bold
    FontSize 14
}

skinparam actor {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    BorderThickness 1.8
    FontColor #1F3864
    FontStyle bold
    FontSize 12
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    BorderThickness 1.4
    FontColor #1E293B
    FontSize 11
    ArrowColor #1F3864
    ArrowThickness 1.2
}

' -------------------------------------------------------------
' Actors Definition
' -------------------------------------------------------------
actor "Agency Administrator" as Admin <<Human>>
actor "Content Editor" as Editor <<Human>>
actor "Agency Client / Observer" as Client <<Human>>
actor "Celery Background Scheduler" as Scheduler <<System>>

' Role Inheritance: Admin inherits all Content Editor capabilities
Editor <|-- Admin

' -------------------------------------------------------------
' ContentIQ System Boundary
' -------------------------------------------------------------
rectangle "ContentIQ Platform Boundary" {

    ' Package 1: Security, Multi-Tenancy & Governance
    package "1. Authentication, Multi-Tenancy & RBAC" {
        usecase "UC-01: Register Agency Tenant" as UC01
        usecase "UC-02: Authenticate & Generate JWT Token" as UC02
        usecase "UC-03: Manage Agency Team & Assign RBAC Roles" as UC03
        usecase "UC-04: Switch Workspace Tenant" as UC04
    }

    ' Package 2: Content Creation & Pre-Flight AI Engine
    package "2. Content Authoring & Pre-Flight AI" {
        usecase "UC-05: Compose Multi-Channel Post Draft\n(Instagram / LinkedIn / YouTube)" as UC05
        usecase "UC-06: Predict Engagement Tier\n(Low <2%, Med 2-5%, High >5%)" as UC06
        usecase "UC-07: Sweep 24-Hour Best-Time Curve" as UC07
        usecase "UC-08: Score Thumbnail Aesthetics\n(OpenCV Rule-of-Thirds & Energy)" as UC08
        usecase "UC-09: Schedule Post on Interactive Calendar" as UC09
        usecase "UC-10: Execute Multivariate A/B Test" as UC10
        usecase "UC-11: Detect Hashtag Velocity & Topics" as UC11
    }

    ' Package 3: Automated Publishing & Tasks
    package "3. Asynchronous Publishing & Queue Engine" {
        usecase "UC-12: Poll & Publish Due Scheduled Posts\n(Sandbox Adapter)" as UC12
        usecase "UC-13: Ingest Empirical Audience Metrics\n(Likes, Reach, Comments)" as UC13
        usecase "UC-14: Dispatch In-App Notification Alerts" as UC14
    }

    ' Package 4: Analytics, Feedback & Continuous Retraining
    package "4. Analytics, Reporting & Retraining Loop" {
        usecase "UC-15: View Executive Performance Dashboard" as UC15
        usecase "UC-16: Export Campaign Analytics to Excel (.csv)" as UC16
        usecase "UC-17: Print Executive Report (PDF)" as UC17
        usecase "UC-18: Analyze Comment Sentiment (VADER)" as UC18
        usecase "UC-19: Forecast 30-Day Follower Growth (Prophet)" as UC19
        usecase "UC-20: Benchmark Against Competitor Channels" as UC20
        usecase "UC-21: Trigger Continuous Model Retraining\n(Empirical Feedback Loop)" as UC21
    }
}

' -------------------------------------------------------------
' Actor Associations
' -------------------------------------------------------------

' Admin Exclusive Associations
Admin --> UC01
Admin --> UC03
Admin --> UC04
Admin --> UC21

' Content Editor Associations (Inherited by Admin)
Editor --> UC02
Editor --> UC05
Editor --> UC08
Editor --> UC09
Editor --> UC10
Editor --> UC11
Editor --> UC15
Editor --> UC18

' Client (Observer) Associations
Client --> UC02
Client --> UC09 #0284C7 : (Read-Only)
Client --> UC15 #0284C7
Client --> UC16 #0284C7
Client --> UC17 #0284C7
Client --> UC19 #0284C7
Client --> UC20 #0284C7

' Celery Worker Associations (System Actor)
Scheduler --> UC12 #475569
Scheduler --> UC13 #475569
Scheduler --> UC14 #475569

' -------------------------------------------------------------
' Use Case Relationships (<<include>> and <<extend>>)
' -------------------------------------------------------------
UC05 ..> UC06 : <<include>>
UC05 ..> UC07 : <<extend>>
UC09 ..> UC05 : <<include>>
UC12 ..> UC14 : <<include>>
UC13 ..> UC15 : <<include>>
UC15 ..> UC16 : <<extend>>
UC15 ..> UC17 : <<extend>>
UC21 ..> UC06 : <<refines>>

' -------------------------------------------------------------
' Notes & Business Constraints
' -------------------------------------------------------------
note right of UC21
  <b>Continuous Retraining Rule:</b>
  Requires accumulating <b>>= 50</b> real
  metric records across published posts.
  Retrains the Random Forest golden model
  and replaces artifacts on disk.
end note

note bottom of Client
  <b>Client Role Constraint (RBAC):</b>
  Client portal is strictly read-only.
  All creation, editing, deletion, and
  model retraining buttons are hidden.
end note

note left of UC01
  <b>Multi-Tenancy Rule:</b>
  Every tenant gets an isolated
  workspace scoped by <i>tenant_id</i>
  in MongoDB.
end note

@enduml
```

---

## 2. Subsystem Diagram 2A: Content Authoring & Pre-Flight AI Engine
*Focuses in detail on the post drafting workflow, 10-feature vector extraction, Random Forest tier prediction, 24-hour best-time probability sweep, OpenCV thumbnail aesthetics, and interactive calendar scheduling.*

```plantuml
@startuml use_case_content_ai
title ContentIQ — Content Authoring & Pre-Flight AI Engine Subsystem\n(Use Case Specification 2A)

skinparam backgroundColor #FFFFFF
skinparam defaultFontName "Segoe UI"
skinparam defaultFontSize 11
skinparam defaultFontColor #1E293B

skinparam packageStyle rectangle
skinparam rectangle {
    BackgroundColor #F8FAFC
    BorderColor #1F3864
    BorderThickness 2
    FontColor #1F3864
    FontStyle bold
    FontSize 13
}

skinparam actor {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    BorderThickness 1.8
    FontColor #1F3864
    FontStyle bold
    FontSize 12
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    BorderThickness 1.4
    FontColor #1E293B
    FontSize 11
    ArrowColor #1F3864
}

actor "Content Editor" as Editor
actor "Agency Administrator" as Admin

Editor <|-- Admin

rectangle "Content Authoring & Pre-Flight AI Subsystem" {

    usecase "UC-05: Compose Social Media Post\n(Instagram / LinkedIn / YouTube)" as UC_Compose
    usecase "UC-05A: Extract 10-Feature Vector\n(Length, Hashtag Ratio, Local Hour)" as UC_Extract
    usecase "UC-06: Pre-Flight ML Prediction\n(Low <2%, Med 2-5%, High >5%)" as UC_Predict
    usecase "UC-07: 24-Hour Best-Time Sweep\n(Simulates hours 0-23 for peak slot)" as UC_Sweep
    usecase "UC-08: Score Thumbnail Aesthetics\n(OpenCV Rule-of-Thirds & Energy)" as UC_Thumb
    usecase "UC-09: Schedule on Monthly Calendar" as UC_Cal
    usecase "UC-09A: Drag-and-Drop Reschedule" as UC_Drag
    usecase "UC-10: Configure A/B Variant Test\n(Variant A vs. Variant B)" as UC_AB
    usecase "UC-11: Recommend Trending Topics\n(TF-IDF & Cosine Similarity)" as UC_Topics
}

Editor --> UC_Compose
Editor --> UC_Thumb
Editor --> UC_Cal
Editor --> UC_AB
Editor --> UC_Topics

UC_Compose ..> UC_Extract : <<include>>
UC_Extract ..> UC_Predict : <<include>>
UC_Compose ..> UC_Sweep : <<extend>>
UC_Compose ..> UC_Thumb : <<extend>>
UC_Cal ..> UC_Drag : <<extend>>
UC_Cal ..> UC_Compose : <<include>>

note right of UC_Sweep
  <b>24-Hour Probability Sweep:</b>
  Iterates through 24 hourly feature vectors
  holding caption constant, identifying the
  global maximum probability of 'High' tier.
end note

note bottom of UC_Thumb
  <b>OpenCV 4.10 Vision Metric:</b>
  Evaluates Rule-of-Thirds grid intersections,
  Laplacian edge sharpness, brightness,
  and color variance (0 to 100 score).
end note

@enduml
```

---

## 3. Subsystem Diagram 2B: Analytics, Reporting & Continuous Retraining Loop
*Focuses on Executive Dashboard KPIs, native Excel (.csv) and PDF exports (GLS Syllabus Item 7.3), VADER sentiment analysis, Prophet growth curves, and the automated model continuous retraining loop.*

```plantuml
@startuml use_case_analytics_retraining
title ContentIQ — Analytics, Reporting & Continuous Retraining Subsystem\n(Use Case Specification 2B)

skinparam backgroundColor #FFFFFF
skinparam defaultFontName "Segoe UI"
skinparam defaultFontSize 11
skinparam defaultFontColor #1E293B

skinparam packageStyle rectangle
skinparam rectangle {
    BackgroundColor #F8FAFC
    BorderColor #1F3864
    BorderThickness 2
    FontColor #1F3864
    FontStyle bold
    FontSize 13
}

skinparam actor {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    BorderThickness 1.8
    FontColor #1F3864
    FontStyle bold
    FontSize 12
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    BorderThickness 1.4
    FontColor #1E293B
    FontSize 11
    ArrowColor #1F3864
}

actor "Agency Administrator" as Admin
actor "Agency Client (Observer)" as Client
actor "Celery Background Worker" as Celery <<System>>

rectangle "Analytics, Reporting & Retraining Subsystem" {

    usecase "UC-15: View Executive Analytics Dashboard\n(KPI Cards, Platform Pie, Best Hours)" as UC_Dash
    usecase "UC-16: Export Performance Report to Excel (.csv)\n(GLS Syllabus Item 7.3)" as UC_Excel
    usecase "UC-17: Print Executive Report (PDF)\n(@media print Stylesheet)" as UC_Print
    usecase "UC-13: Ingest Post-Publication Engagement Metrics\n(Likes, Reach, Actual Tier)" as UC_Ingest
    usecase "UC-18: Analyze Comment Sentiment\n(VADER Compound Polarity -1.0 to +1.0)" as UC_Sentiment
    usecase "UC-19: Forecast 30-Day Follower Growth\n(Facebook Prophet 80% Confidence Interval)" as UC_Prophet
    usecase "UC-20: Benchmark Competitor Accounts\n(Engagement Comparison)" as UC_Comp
    usecase "UC-21: Trigger Continuous Model Retraining\n(Empirical Feedback Loop)" as UC_Retrain
}

' Admin Connections
Admin --> UC_Dash
Admin --> UC_Retrain
Admin --> UC_Excel
Admin --> UC_Print
Admin --> UC_Sentiment
Admin --> UC_Prophet
Admin --> UC_Comp

' Client Connections (Read-Only Observer)
Client --> UC_Dash #0284C7
Client --> UC_Excel #0284C7
Client --> UC_Print #0284C7
Client --> UC_Prophet #0284C7
Client --> UC_Comp #0284C7

' Celery Worker (Background Ingestion)
Celery --> UC_Ingest #475569

' Relationships
UC_Dash ..> UC_Excel : <<extend>>
UC_Dash ..> UC_Print : <<extend>>
UC_Ingest ..> UC_Dash : <<include>>
UC_Ingest ..> UC_Retrain : <<feeds>>

note right of UC_Retrain
  <b>Continuous Retraining Gate:</b>
  Only accessible to <b>Admin</b> role.
  Validates count(post_metrics) >= 50.
  Trains candidate model against ground truth,
  evaluates accuracy delta, and updates
  the active production model pickle on disk.
end note

note bottom of Client
  <b>Observer Security Boundary:</b>
  Clients can monitor real-time KPIs
  and export reports, but the Retrain
  trigger is locked with a warning notice.
end note

@enduml
```

---

## 4. Subsystem Diagram 2C: Multi-Tenancy, Team Governance & RBAC Subsystem
*Focuses on tenant registration, workspace data scoping in MongoDB, JWT authentication, 1-click viva evaluator switcher, and dynamic UI permission adaptation.*

```plantuml
@startuml use_case_admin_rbac
title ContentIQ — Multi-Tenancy, Team Governance & RBAC Subsystem\n(Use Case Specification 2C)

skinparam backgroundColor #FFFFFF
skinparam defaultFontName "Segoe UI"
skinparam defaultFontSize 11
skinparam defaultFontColor #1E293B

skinparam packageStyle rectangle
skinparam rectangle {
    BackgroundColor #F8FAFC
    BorderColor #1F3864
    BorderThickness 2
    FontColor #1F3864
    FontStyle bold
    FontSize 13
}

skinparam actor {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    BorderThickness 1.8
    FontColor #1F3864
    FontStyle bold
    FontSize 12
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    BorderThickness 1.4
    FontColor #1E293B
    FontSize 11
    ArrowColor #1F3864
}

actor "Agency Administrator" as Admin
actor "Content Editor" as Editor
actor "Agency Client" as Client

rectangle "Multi-Tenancy, Team Governance & RBAC Subsystem" {

    usecase "UC-01: Register Agency Tenant & Workspace\n(Creates 'tenants' & admin in 'users')" as UC_Reg
    usecase "UC-02: Authenticate via Email & Password\n(Bcrypt 12 Rounds + HS256 JWT Token)" as UC_Auth
    usecase "UC-02A: 1-Click Viva Demo Role Switcher\n(Admin / Editor / Client / Tenant 2)" as UC_QuickLogin
    usecase "UC-03: Manage Team Members\n(/team Management Portal)" as UC_Team
    usecase "UC-03A: Assign RBAC Role\n('admin', 'editor', 'client')" as UC_AssignRole
    usecase "UC-04: Enforce Tenant-Level Data Scoping\n(Every MongoDB query filtered by tenant_id)" as UC_TenantScope
    usecase "UC-04A: Verify Cross-Tenant Data Isolation\n(Tenant A vs. Tenant B Partitioning)" as UC_Isolate
    usecase "UC-04B: Render Role-Adaptive UI Navigation\n(Admin: 12 links, Editor: 10, Client: 6)" as UC_AdaptNav
}

Admin --> UC_Reg
Admin --> UC_Auth
Admin --> UC_QuickLogin
Admin --> UC_Team
Admin --> UC_AssignRole
Admin --> UC_Isolate

Editor --> UC_Auth
Editor --> UC_QuickLogin

Client --> UC_Auth
Client --> UC_QuickLogin

UC_Auth ..> UC_TenantScope : <<include>>
UC_Auth ..> UC_AdaptNav : <<include>>
UC_QuickLogin ..> UC_Auth : <<extend>>
UC_Team ..> UC_AssignRole : <<include>>
UC_TenantScope ..> UC_Isolate : <<enforces>>

note right of UC_AdaptNav
  <b>Dynamic RBAC UI Adaptation:</b>
  - <b>Admin:</b> Full access (12 modules + Retrain button)
  - <b>Editor:</b> Content tools (10 modules, team hidden)
  - <b>Client:</b> Observer portal (6 modules, creation & retrain locked)
end note

note bottom of UC_Isolate
  <b>Hard Multi-Tenancy Architecture:</b>
  No shared collections without compound
  indexes on <i>tenant_id</i>. Prevents any
  cross-agency information leakage.
end note

@enduml
```

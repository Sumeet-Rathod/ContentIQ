"""
ContentIQ - Clean PlantUML Validator & Renderer
Encodes and validates PlantUML use case diagrams against the official PlantUML server,
saving both the .puml source code and rendered .png images.
"""
import os
import zlib
import urllib.request

PLANTUML_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\plantuml"
os.makedirs(PLANTUML_DIR, exist_ok=True)

def plantuml_encode(text):
    zlibbed = zlib.compress(text.encode('utf-8'))[2:-4]
    mapping = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    res = []
    for i in range(0, len(zlibbed), 3):
        b1 = zlibbed[i]
        b2 = zlibbed[i+1] if i+1 < len(zlibbed) else 0
        b3 = zlibbed[i+2] if i+2 < len(zlibbed) else 0
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        res.append(mapping[c1] + mapping[c2] + mapping[c3] + mapping[c4])
    return ''.join(res)

def validate_and_save(name, puml_code):
    puml_file = os.path.join(PLANTUML_DIR, f"{name}.puml")
    png_file = os.path.join(PLANTUML_DIR, f"{name}.png")

    with open(puml_file, "w", encoding="utf-8") as f:
        f.write(puml_code)
    print(f"[+] Saved PUML: {puml_file}")

    encoded = plantuml_encode(puml_code)
    url = f"http://www.plantuml.com/plantuml/png/~1{encoded}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            with open(png_file, "wb") as pf:
                pf.write(content)
            print(f"[+] Successfully validated & rendered PNG ({len(content)} bytes): {png_file}")
    except Exception as e:
        print(f"[-] Warning: Failed to fetch online PNG for {name}: {e}")

# -------------------------------------------------------------
# 1. Master System Use Case Diagram (Clean Layout)
# -------------------------------------------------------------
PUML_MASTER = """@startuml
left to right direction

title ContentIQ: Complete System Use Case Diagram
header GLS University | FCAIT | iMCA SEM IX (Course: 222301907)

skinparam backgroundColor #FFFFFF
skinparam defaultFontName "Segoe UI"
skinparam shadowing true
skinparam packageStyle rectangle

skinparam actor {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    FontColor #1F3864
    FontStyle bold
}

skinparam rectangle {
    BackgroundColor #F8FAFC
    BorderColor #1F3864
    BorderThickness 1.5
    FontColor #1F3864
    FontStyle bold
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    FontColor #1E293B
    ArrowColor #1F3864
}

' Human Actors on the Left
actor "Agency Administrator" as Admin <<Human>>
actor "Content Editor" as Editor <<Human>>
actor "Agency Client (Observer)" as Client <<Human>>

' System Actor on the Right
actor "Celery Background Worker" as Celery <<System>>

' Role Inheritance
Editor <|-- Admin

rectangle "ContentIQ Platform" {

    package "1. Authentication & Multi-Tenancy" {
        usecase "UC-01: Register Agency Workspace" as UC01
        usecase "UC-02: Authenticate (Email & Password)" as UC02
        usecase "UC-03: Manage Team & Assign RBAC Roles" as UC03
        usecase "UC-04: Switch Tenant Workspace" as UC04
    }

    package "2. Content Authoring & Pre-Flight AI" {
        usecase "UC-05: Compose Social Media Post Draft" as UC05
        usecase "UC-06: Pre-Flight Engagement Prediction" as UC06
        usecase "UC-07: 24-Hour Best-Time Probability Sweep" as UC07
        usecase "UC-08: Score Thumbnail Aesthetics (OpenCV)" as UC08
        usecase "UC-09: Schedule Post on Interactive Calendar" as UC09
        usecase "UC-10: Execute A/B Split Test" as UC10
    }

    package "3. Automated Queue & Publishing" {
        usecase "UC-11: Auto-Publish Due Posts (Sandbox)" as UC11
        usecase "UC-12: Ingest Post-Publication Metrics" as UC12
        usecase "UC-13: Dispatch In-App Notifications" as UC13
    }

    package "4. Analytics, Reporting & Retraining" {
        usecase "UC-14: View Executive Performance Dashboard" as UC14
        usecase "UC-15: Export Performance Report to Excel (.csv)" as UC15
        usecase "UC-16: Print Executive Report (PDF)" as UC16
        usecase "UC-17: Analyze Comment Sentiment (VADER)" as UC17
        usecase "UC-18: Forecast 30-Day Follower Growth" as UC18
        usecase "UC-19: Trigger Continuous Model Retraining" as UC19
    }
}

' Admin Associations
Admin --> UC01
Admin --> UC03
Admin --> UC04
Admin --> UC19

' Editor Associations (Inherited by Admin)
Editor --> UC02
Editor --> UC05
Editor --> UC08
Editor --> UC09
Editor --> UC10
Editor --> UC14
Editor --> UC17

' Client Associations (Read-Only)
Client --> UC02
Client --> UC09 #0284C7 : (Read-Only)
Client --> UC14 #0284C7
Client --> UC15 #0284C7
Client --> UC16 #0284C7
Client --> UC18 #0284C7

' Celery Worker Associations
Celery --> UC11 #475569
Celery --> UC12 #475569
Celery --> UC13 #475569

' Include & Extend Stereotypes
UC05 ..> UC06 : <<include>>
UC05 ..> UC07 : <<extend>>
UC09 ..> UC05 : <<include>>
UC11 ..> UC13 : <<include>>
UC12 ..> UC14 : <<include>>
UC14 ..> UC15 : <<extend>>
UC14 ..> UC16 : <<extend>>
UC19 ..> UC06 : <<refines>>

note right of UC19
  <b>Continuous Retraining:</b>
  Triggered when >= 50 real
  metric records accumulate.
end note

note bottom of Client
  <b>Observer Portal:</b>
  Read-only campaign tracking.
  Content authoring & retrain
  buttons are hidden.
end note

@enduml"""

# -------------------------------------------------------------
# 2. Subsystem 2A: Content Creation & Pre-Flight AI
# -------------------------------------------------------------
PUML_CONTENT_AI = """@startuml
left to right direction

title ContentIQ: Content Authoring & Pre-Flight AI Subsystem
header Module Specification 2A

skinparam backgroundColor #FFFFFF
skinparam defaultFontName "Segoe UI"
skinparam shadowing true

skinparam actor {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    FontColor #1F3864
    FontStyle bold
}

skinparam rectangle {
    BackgroundColor #F8FAFC
    BorderColor #1F3864
    BorderThickness 1.5
    FontColor #1F3864
    FontStyle bold
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    FontColor #1E293B
    ArrowColor #1F3864
}

actor "Content Editor" as Editor <<Human>>
actor "Agency Administrator" as Admin <<Human>>

Editor <|-- Admin

rectangle "Content Authoring & Pre-Flight AI Subsystem" {
    usecase "UC-05: Compose Social Media Post\n(Instagram / LinkedIn / YouTube)" as UC_Compose
    usecase "UC-05A: Extract 10-Feature Vector\n(Length, Hashtags, Local Hour)" as UC_Extract
    usecase "UC-06: Pre-Flight ML Prediction\n(Low <2%, Med 2-5%, High >5%)" as UC_Predict
    usecase "UC-07: 24-Hour Best-Time Probability Sweep\n(Simulates hours 0-23 for peak slot)" as UC_Sweep
    usecase "UC-08: Score Thumbnail Aesthetics\n(OpenCV Rule-of-Thirds & Energy)" as UC_Thumb
    usecase "UC-09: Schedule on Interactive Calendar" as UC_Calendar
    usecase "UC-09A: Drag-and-Drop Reschedule Post" as UC_Drag
    usecase "UC-10: Configure Multivariate A/B Test\n(Variant A vs. Variant B)" as UC_AB
}

Editor --> UC_Compose
Editor --> UC_Thumb
Editor --> UC_Calendar
Editor --> UC_AB

UC_Compose ..> UC_Extract : <<include>>
UC_Extract ..> UC_Predict : <<include>>
UC_Compose ..> UC_Sweep : <<extend>>
UC_Compose ..> UC_Thumb : <<extend>>
UC_Calendar ..> UC_Drag : <<extend>>
UC_Calendar ..> UC_Compose : <<include>>

note right of UC_Sweep
  <b>24-Hour Probability Sweep:</b>
  Iterates through hours 0-23
  holding caption constant to identify
  the peak engagement window.
end note

note bottom of UC_Thumb
  <b>OpenCV 4.10 Vision Metric:</b>
  Evaluates edge sharpness, contrast,
  colorfulness, and Rule-of-Thirds
  composition (0 to 100 score).
end note

@enduml"""

# -------------------------------------------------------------
# 3. Subsystem 2B: Analytics & Retraining Feedback Loop
# -------------------------------------------------------------
PUML_ANALYTICS_RETRAIN = """@startuml
left to right direction

title ContentIQ: Analytics, Reporting & Continuous Retraining Subsystem
header Module Specification 2B

skinparam backgroundColor #FFFFFF
skinparam defaultFontName "Segoe UI"
skinparam shadowing true

skinparam actor {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    FontColor #1F3864
    FontStyle bold
}

skinparam rectangle {
    BackgroundColor #F8FAFC
    BorderColor #1F3864
    BorderThickness 1.5
    FontColor #1F3864
    FontStyle bold
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    FontColor #1E293B
    ArrowColor #1F3864
}

actor "Agency Administrator" as Admin <<Human>>
actor "Agency Client (Observer)" as Client <<Human>>
actor "Celery Background Worker" as Celery <<System>>

rectangle "Analytics, Reporting & Retraining Subsystem" {
    usecase "UC-14: View Executive Analytics Dashboard\n(KPI Cards, Platform Distribution, Best Times)" as UC_Dash
    usecase "UC-15: Export Performance Report to Excel (.csv)\n(GLS Syllabus Item 7.3)" as UC_Excel
    usecase "UC-16: Print Executive Report (PDF)\n(@media print Stylesheet)" as UC_Print
    usecase "UC-12: Ingest Real Post Metrics\n(Likes, Comments, Shares, Reach)" as UC_Ingest
    usecase "UC-17: Analyze Comment Sentiment (VADER)\n(Compound Polarity -1.0 to +1.0)" as UC_Sentiment
    usecase "UC-18: Forecast 30-Day Follower Growth\n(Facebook Prophet 80% Confidence Interval)" as UC_Prophet
    usecase "UC-19: Trigger Continuous Model Retraining\n(Empirical Feedback Loop)" as UC_Retrain
}

Admin --> UC_Dash
Admin --> UC_Retrain
Admin --> UC_Excel
Admin --> UC_Print
Admin --> UC_Sentiment
Admin --> UC_Prophet

Client --> UC_Dash #0284C7
Client --> UC_Excel #0284C7
Client --> UC_Print #0284C7
Client --> UC_Prophet #0284C7

Celery --> UC_Ingest #475569

UC_Dash ..> UC_Excel : <<extend>>
UC_Dash ..> UC_Print : <<extend>>
UC_Ingest ..> UC_Dash : <<include>>
UC_Ingest ..> UC_Retrain : <<feeds>>

note right of UC_Retrain
  <b>Continuous Retraining Gate:</b>
  Only accessible to Admin role.
  Requires >= 50 real metric records.
  Re-fits Random Forest model and
  updates active production artifacts.
end note

note bottom of Client
  <b>Client Role (RBAC):</b>
  Read-only analytical access.
  Model retrain button is locked.
end note

@enduml"""

# -------------------------------------------------------------
# 4. Subsystem 2C: Multi-Tenancy & RBAC
# -------------------------------------------------------------
PUML_ADMIN_RBAC = """@startuml
left to right direction

title ContentIQ: Multi-Tenancy, Team Governance & RBAC Subsystem
header Module Specification 2C

skinparam backgroundColor #FFFFFF
skinparam defaultFontName "Segoe UI"
skinparam shadowing true

skinparam actor {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    FontColor #1F3864
    FontStyle bold
}

skinparam rectangle {
    BackgroundColor #F8FAFC
    BorderColor #1F3864
    BorderThickness 1.5
    FontColor #1F3864
    FontStyle bold
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #1F3864
    FontColor #1E293B
    ArrowColor #1F3864
}

actor "Agency Administrator" as Admin <<Human>>
actor "Content Editor" as Editor <<Human>>
actor "Agency Client" as Client <<Human>>

rectangle "Multi-Tenancy, Team Governance & RBAC Subsystem" {
    usecase "UC-01: Register Agency Workspace\n(Creates 'tenants' & admin in 'users')" as UC_Reg
    usecase "UC-02: Authenticate (Email & Password)\n(Bcrypt 12 Rounds + HS256 JWT Token)" as UC_Auth
    usecase "UC-02A: 1-Click Viva Demo Role Switcher\n(Admin / Editor / Client / Tenant 2)" as UC_QuickLogin
    usecase "UC-03: Manage Team Members & Roles\n(Invite staff & set role permissions)" as UC_Team
    usecase "UC-04: Enforce Tenant-Level Data Scoping\n(Every MongoDB query filtered by tenant_id)" as UC_TenantScope
    usecase "UC-04A: Verify Cross-Tenant Isolation\n(Tenant A vs. Tenant B Partitioning)" as UC_Isolate
    usecase "UC-04B: Render Role-Adaptive UI Navigation\n(Admin: 12 links, Editor: 10, Client: 6)" as UC_AdaptNav
}

Admin --> UC_Reg
Admin --> UC_Auth
Admin --> UC_QuickLogin
Admin --> UC_Team
Admin --> UC_Isolate

Editor --> UC_Auth
Editor --> UC_QuickLogin

Client --> UC_Auth
Client --> UC_QuickLogin

UC_Auth ..> UC_TenantScope : <<include>>
UC_Auth ..> UC_AdaptNav : <<include>>
UC_QuickLogin ..> UC_Auth : <<extend>>
UC_TenantScope ..> UC_Isolate : <<enforces>>

note right of UC_AdaptNav
  <b>Dynamic Navigation Adaptation:</b>
  - Admin: Full access (12 modules + Retrain)
  - Editor: Content authoring (10 modules)
  - Client: Observer portal (6 modules)
end note

note bottom of UC_Isolate
  <b>Row-Level Database Isolation:</b>
  All posts, metrics, comments, and
  competitors are tagged with tenant_id.
end note

@enduml"""

if __name__ == "__main__":
    validate_and_save("use_case_master_clean", PUML_MASTER)
    validate_and_save("use_case_content_ai_clean", PUML_CONTENT_AI)
    validate_and_save("use_case_analytics_retraining_clean", PUML_ANALYTICS_RETRAIN)
    validate_and_save("use_case_admin_rbac_clean", PUML_ADMIN_RBAC)
    print("\n[+] All PlantUML diagrams validated and saved successfully!")

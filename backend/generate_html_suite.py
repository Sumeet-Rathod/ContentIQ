"""
ContentIQ - Full HTML Suite Generator
Generates a complete, beautiful HTML document with embedded diagrams, screenshots,
tables for all 9 collections, and full academic report sections.
"""
import os
import base64

DIAGRAMS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\diagrams"
SCREENSHOTS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\screenshots"
OUT_HTML = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\ContentIQ_Final_Documentation_Report.html"

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/png;base64,{data}"
    return ""

def generate_full_html():
    img_uc = get_base64_img(os.path.join(DIAGRAMS_DIR, "use_case_diagram.png"))
    img_cls = get_base64_img(os.path.join(DIAGRAMS_DIR, "class_diagram.png"))
    img_swim = get_base64_img(os.path.join(DIAGRAMS_DIR, "swimlane_activity_diagram.png"))
    img_seq = get_base64_img(os.path.join(DIAGRAMS_DIR, "sequence_diagram.png"))
    img_state = get_base64_img(os.path.join(DIAGRAMS_DIR, "state_chart_diagram.png"))

    # Load all 17 screenshots as base64
    screenshots_b64 = {}
    for i in range(1, 18):
        prefix = f"screenshot_{i:02d}_"
        for f in os.listdir(SCREENSHOTS_DIR):
            if f.startswith(prefix) and f.endswith(".png"):
                screenshots_b64[i] = get_base64_img(os.path.join(SCREENSHOTS_DIR, f))
                break

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ContentIQ — Final Project Documentation Report (GLS University FCAIT)</title>
<style>
  @page {{
    size: A4;
    margin: 15mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background: #f1f5f9;
  }}
  .container {{
    max-width: 900px;
    margin: 30px auto;
    background: #ffffff;
    padding: 50px 60px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    border-radius: 8px;
  }}
  .border-box {{
    border: 3px double #1f3864;
    padding: 40px 30px;
    text-align: center;
    margin-bottom: 50px;
  }}
  .cert-box {{
    border: 2px solid #1f3864;
    padding: 40px;
    margin-bottom: 50px;
  }}
  h1 {{ color: #1f3864; font-size: 28pt; margin: 0 0 10px 0; }}
  h2 {{ color: #1f3864; font-size: 16pt; margin-top: 35px; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; }}
  h3 {{ color: #d97706; font-size: 13pt; margin-top: 20px; }}
  p {{ margin: 10px 0; font-size: 10.5pt; }}
  table {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 9.5pt; }}
  th, td {{ border: 1px solid #cbd5e1; padding: 8px 12px; text-align: left; }}
  th {{ background-color: #1f3864; color: #ffffff; font-weight: 600; }}
  tr:nth-child(even) td {{ background-color: #f8fafc; }}
  .diagram-img {{ width: 100%; height: auto; border: 1px solid #cbd5e1; border-radius: 6px; margin: 15px 0 5px 0; }}
  .caption {{ font-size: 9pt; font-style: italic; color: #64748b; text-align: center; margin-bottom: 25px; }}
  .footer-sig {{ display: flex; justify-content: space-between; margin-top: 50px; }}
  @media print {{
    body {{ background: transparent; }}
    .container {{ max-width: 100%; margin: 0; padding: 0; box-shadow: none; border-radius: 0; }}
    .page-break {{ page-break-after: always; }}
  }}
</style>
</head>
<body>

<div class="container">

  <!-- 1. COVER PAGE -->
  <div class="border-box page-break">
    <h1 style="font-family: Georgia, serif; font-size: 34pt; color: #1f3864;">ContentIQ</h1>
    <p style="font-style: italic; color: #64748b; font-size: 14pt; margin-bottom: 40px;">
      An AI-Powered Multi-Tenant Content Performance and Scheduling Platform
    </p>

    <div style="margin: 30px 0;">
      <p style="font-size: 13pt; font-weight: bold; margin-bottom: 4px;">Project Report</p>
      <p style="font-size: 11pt; color: #475569; margin-bottom: 12px;">Submitted for the subject of</p>
      <p style="font-size: 15pt; font-weight: bold; color: #1f3864; margin-bottom: 4px;">222301907 Capstone Project – II</p>
      <p style="font-size: 13pt; font-weight: bold; margin-bottom: 4px;">Integrated Master of Computer Applications (iMCA)</p>
      <p style="font-size: 12pt;">Semester IX</p>
    </div>

    <div style="margin: 30px 0;">
      <p style="font-weight: bold; font-size: 12pt; margin-bottom: 4px;">Submitted By:</p>
      <p style="font-size: 11pt;">Student 1: [Your Full Name] (Enrollment No: ____________________)</p>
      <p style="font-size: 11pt;">Student 2: [Partner Full Name] (Enrollment No: ____________________)</p>
    </div>

    <div style="margin: 30px 0;">
      <p style="font-weight: bold; font-size: 12pt; margin-bottom: 4px;">Under the Guidance of:</p>
      <p style="font-size: 11pt; font-weight: bold;">Dr./Prof. Name of Internal Guide</p>
      <p style="font-size: 10.5pt; color: #475569;">FCAIT, GLS University</p>
    </div>

    <div style="margin-top: 40px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
      <p style="font-size: 12pt; font-weight: bold; color: #1f3864; margin: 2px 0;">Faculty of Computer Applications & IT (FCAIT)</p>
      <p style="font-size: 11pt; font-weight: bold; margin: 2px 0;">iMCA Programme, Ahmedabad</p>
      <p style="font-size: 12pt; font-weight: bold; color: #1f3864; margin: 4px 0;">GLS UNIVERSITY</p>
      <p style="font-size: 11pt; font-weight: bold; margin-top: 10px;">Academic Year 2026–2027</p>
    </div>
  </div>

  <!-- 2. COLLEGE CERTIFICATE -->
  <div class="cert-box page-break">
    <div style="text-align: center; margin-bottom: 30px;">
      <h2 style="border: none; margin: 0; font-size: 16pt;">GLS UNIVERSITY</h2>
      <p style="font-weight: bold; font-size: 12pt; margin: 2px 0;">Faculty of Computer Applications & IT</p>
      <p style="font-weight: bold; font-size: 11pt; margin: 2px 0;">iMCA Programme, Ahmedabad</p>
      <h2 style="border: none; text-decoration: underline; margin-top: 25px; font-size: 17pt;">CERTIFICATE</h2>
    </div>

    <p style="font-size: 12pt; text-align: justify; line-height: 1.8;">
      This is to certify that the following students of <b>Semester IX Integrated Master of Computer Applications (iMCA) Programme</b>,
      Faculty of Computer Applications & IT (FCAIT), GLS University, Ahmedabad, have successfully completed the subject project titled:
    </p>

    <p style="text-align: center; font-size: 13pt; font-weight: bold; color: #1f3864; margin: 25px 0;">
      “ContentIQ: An AI-Powered Multi-Tenant Content Performance and Scheduling Platform for Social Media Creators and Agencies”
    </p>

    <p style="font-size: 12pt; text-align: justify; line-height: 1.8;">
      for the course <b>222301907 Capstone Project – II - System Design and Implementation</b> during the Academic Year <b>2026–2027</b>.
    </p>

    <p style="margin-top: 35px; font-size: 11pt;"><b>Date of Submission:</b> 23rd October 2026</p>

    <div class="footer-sig">
      <div>
        <p style="font-weight: bold; margin: 0;">Dr./Prof. Name of Internal Guide</p>
        <p style="margin: 2px 0; font-size: 10pt; color: #475569;">Project Guide</p>
        <p style="margin: 0; font-size: 10pt; color: #475569;">FCAIT, GLS University</p>
      </div>
      <div style="text-align: right;">
        <p style="font-weight: bold; margin: 0;">Dr. Tripti Dodiya</p>
        <p style="margin: 2px 0; font-size: 10pt; color: #475569;">Dean</p>
        <p style="margin: 0; font-size: 10pt; color: #475569;">FCAIT, GLS University</p>
      </div>
    </div>
  </div>

  <!-- 3. INDEX -->
  <div class="page-break">
    <h2>3. INDEX</h2>
    <table>
      <thead>
        <tr><th style="width: 10%;">Section</th><th style="width: 75%;">Topic / Chapter Name</th><th style="width: 15%; text-align: center;">Page No.</th></tr>
      </thead>
      <tbody>
        <tr><td>1</td><td><b>Cover Page</b></td><td style="text-align: center;">1</td></tr>
        <tr><td>2</td><td><b>College Certificate</b></td><td style="text-align: center;">2</td></tr>
        <tr><td>3</td><td><b>Index</b></td><td style="text-align: center;">3</td></tr>
        <tr><td>4</td><td><b>Brief of System</b> (Problem Statement, Scope, Objectives, Tech Stack)</td><td style="text-align: center;">4</td></tr>
        <tr><td>5</td><td><b>UML Diagrams</b> (Use Case, Class, Activity Swimlane, Sequence, State Chart)</td><td style="text-align: center;">7</td></tr>
        <tr><td>6</td><td><b>Data Dictionary</b> (Specifications for all 9 MongoDB Collections)</td><td style="text-align: center;">14</td></tr>
        <tr><td>7</td><td><b>All Screenshots with URL</b> (Admin Side, Client Side, Excel/PDF Reports)</td><td style="text-align: center;">20</td></tr>
        <tr><td>8</td><td><b>References & Bibliography</b> (IEEE Standards)</td><td style="text-align: center;">27</td></tr>
      </tbody>
    </table>

    <!-- 4. BRIEF OF SYSTEM -->
    <h2>4. BRIEF OF SYSTEM</h2>
    <h3>4.1 Introduction & Problem Statement</h3>
    <p>
      Conventional social media scheduling platforms like Buffer, Hootsuite, and Later suffer from the critical <b>"Blind Scheduling" Dilemma</b>:
      they accept drafts and schedule them at arbitrary user-chosen times without any predictive intelligence.
      Content creators lack pre-publication feedback on whether their copy, timing, and media will engage their target audience.
      Furthermore, post-publication metrics are never fed back into an intelligent model to improve future posts.
    </p>
    <p>
      <b>ContentIQ</b> is an AI-powered, multi-tenant content performance and scheduling platform. Built with a modern full-stack architecture
      (React 18, FastAPI, MongoDB 7.0, Redis 7, and Celery), ContentIQ solves these problems by embedding data science directly into the content lifecycle.
    </p>

    <h3>4.2 System Scope & Objectives</h3>
    <ul>
      <li><b>Production-Ready Multi-Tenancy:</b> Hard data isolation utilizing MongoDB tenant-scoped documents and JWT claims.</li>
      <li><b>Pre-Flight ML Scoring:</b> Real-time Random Forest engagement tier predictions (Low, Medium, High) with 24-hour best-time sweeps.</li>
      <li><b>Computer Vision & NLP Analysis:</b> Automated OpenCV 4.10 thumbnail balance scoring and VADER sentiment classification.</li>
      <li><b>Continuous Retraining Loop:</b> Automated feedback pipeline retraining the model once &ge; 50 real metric records accumulate.</li>
    </ul>

    <h3>4.3 Technology Stack Justification</h3>
    <table>
      <thead>
        <tr><th>Layer</th><th>Technology</th><th>Academic & Viva Justification</th></tr>
      </thead>
      <tbody>
        <tr><td><b>Frontend</b></td><td>React 18, Vite 6, Chart.js</td><td>Component-driven SPA, fast HMR, executive Navy & Gold theme.</td></tr>
        <tr><td><b>Backend</b></td><td>FastAPI 0.115.0, Pydantic v2</td><td>High-throughput asynchronous REST API with automatic OpenAPI Swagger docs.</td></tr>
        <tr><td><b>Database</b></td><td>MongoDB 7.0 Community</td><td>Document-oriented schema suited for polymorphic social media posts and comments.</td></tr>
        <tr><td><b>Cache & Broker</b></td><td>Redis Server 7.0</td><td>In-memory store providing sub-millisecond caching for dashboards and task queue.</td></tr>
        <tr><td><b>Async Worker</b></td><td>Celery 5.4 (--pool=solo)</td><td>Decoupled background scheduler for automated post publishing and notifications.</td></tr>
        <tr><td><b>Machine Learning</b></td><td>Scikit-Learn, OpenCV, Prophet, VADER</td><td>Random Forest classification, time-series forecasting, and computer vision.</td></tr>
      </tbody>
    </table>
  </div>

  <!-- 5. UML DIAGRAMS -->
  <div class="page-break">
    <h2>5. UML DIAGRAMS</h2>

    <h3>5.1 Use Case Diagram</h3>
    <p>Illustrates functional boundaries and relationships between Agency Admin, Content Editor, Client Observer, and the Celery Scheduler:</p>
    <img src="{img_uc}" class="diagram-img" alt="Use Case Diagram" />
    <p class="caption">Figure 5.1: ContentIQ System Use Case Diagram</p>

    <h3>5.2 Detailed Class Diagram</h3>
    <p>Models the Object-Oriented domain entities, visibility, attributes, member methods, and multiplicities:</p>
    <img src="{img_cls}" class="diagram-img" alt="Class Diagram" />
    <p class="caption">Figure 5.2: ContentIQ Domain Class Diagram with Multiplicities</p>

    <h3>5.3 Activity Diagram (Swimlane)</h3>
    <p>Adhering to GLS University's specific Swimlane format, the execution lifecycle is partitioned across four distinct operational lanes:</p>
    <img src="{img_swim}" class="diagram-img" alt="Swimlane Activity Diagram" />
    <p class="caption">Figure 5.3: ContentIQ 4-Lane Swimlane Activity Diagram</p>

    <h3>5.4 Sequence Diagram</h3>
    <p>Pre-flight machine learning scoring and 24-hour best-time probability sweep sequence:</p>
    <img src="{img_seq}" class="diagram-img" alt="Sequence Diagram" />
    <p class="caption">Figure 5.4: Pre-Flight AI Prediction & 24h Sweep Sequence Diagram</p>

    <h3>5.5 State Chart Diagram</h3>
    <p>State transitions from Draft to Scheduled, Published, Metrics Collected, and Continuous Retraining:</p>
    <img src="{img_state}" class="diagram-img" alt="State Chart Diagram" />
    <p class="caption">Figure 5.5: Post Lifecycle State Chart Diagram</p>
  </div>

  <!-- 6. DATA DICTIONARY -->
  <div class="page-break">
    <h2>6. DATA DICTIONARY</h2>
    <p>Specifications for all 9 MongoDB collections in the <code>contentiq</code> database:</p>

    <h3>Collection 1: tenants (Workspaces & Agencies)</h3>
    <table>
      <thead><tr><th>Field Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><b>_id</b></td><td>ObjectId</td><td>Primary Key</td><td>Unique workspace identifier</td></tr>
        <tr><td><b>name</b></td><td>String</td><td>Required</td><td>Agency Name (e.g. 'Apex Digital Agency')</td></tr>
        <tr><td><b>plan</b></td><td>String</td><td>Enum</td><td>Subscription tier: 'free', 'pro', 'enterprise'</td></tr>
        <tr><td><b>created_at</b></td><td>ISO Datetime</td><td>Required</td><td>Local ISO creation timestamp</td></tr>
      </tbody>
    </table>

    <h3>Collection 2: users (User Accounts & RBAC Roles)</h3>
    <table>
      <thead><tr><th>Field Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><b>_id</b></td><td>ObjectId</td><td>Primary Key</td><td>Unique user identifier</td></tr>
        <tr><td><b>tenant_id</b></td><td>String</td><td>Multi-Tenant Key</td><td>Foreign Key reference to tenants._id</td></tr>
        <tr><td><b>email</b></td><td>String</td><td>Unique, Required</td><td>Unique login email address</td></tr>
        <tr><td><b>name</b></td><td>String</td><td>Required</td><td>Full name of staff member</td></tr>
        <tr><td><b>hashed_password</b></td><td>String</td><td>Required</td><td>Bcrypt hashed password (12 salt rounds)</td></tr>
        <tr><td><b>role</b></td><td>String</td><td>Enum</td><td>'admin', 'editor', 'client'</td></tr>
        <tr><td><b>created_at</b></td><td>ISO Datetime</td><td>Required</td><td>Account creation timestamp</td></tr>
      </tbody>
    </table>

    <h3>Collection 3: posts (Social Media Posts)</h3>
    <table>
      <thead><tr><th>Field Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><b>_id</b></td><td>ObjectId</td><td>Primary Key</td><td>Unique post identifier</td></tr>
        <tr><td><b>tenant_id</b></td><td>String</td><td>Multi-Tenant Key</td><td>Foreign Key reference to tenants._id</td></tr>
        <tr><td><b>platform</b></td><td>String</td><td>Enum</td><td>'instagram', 'linkedin', 'youtube'</td></tr>
        <tr><td><b>caption</b></td><td>String</td><td>Required</td><td>Text caption and content</td></tr>
        <tr><td><b>hashtags</b></td><td>Array[String]</td><td>Required</td><td>List of hashtag strings</td></tr>
        <tr><td><b>scheduled_time</b></td><td>ISO Datetime</td><td>Indexed</td><td>Scheduled publication local ISO datetime</td></tr>
        <tr><td><b>scheduled_hour</b></td><td>Integer</td><td>Derived</td><td>Integer hour (0-23) without UTC drift</td></tr>
        <tr><td><b>status</b></td><td>String</td><td>Enum</td><td>'draft', 'scheduled', 'published'</td></tr>
      </tbody>
    </table>

    <h3>Collection 4: post_metrics (Performance Feedback)</h3>
    <table>
      <thead><tr><th>Field Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><b>_id</b></td><td>ObjectId</td><td>Primary Key</td><td>Unique metric identifier</td></tr>
        <tr><td><b>tenant_id</b></td><td>String</td><td>Multi-Tenant Key</td><td>Foreign Key to tenant</td></tr>
        <tr><td><b>post_id</b></td><td>String</td><td>Foreign Key</td><td>Foreign reference to posts._id</td></tr>
        <tr><td><b>likes</b></td><td>Integer</td><td>&ge; 0</td><td>Total likes count</td></tr>
        <tr><td><b>comments</b></td><td>Integer</td><td>&ge; 0</td><td>Total comments count</td></tr>
        <tr><td><b>reach</b></td><td>Integer</td><td>&ge; 0</td><td>Unique viewer reach</td></tr>
        <tr><td><b>engagement_rate</b></td><td>Float</td><td>Percentage</td><td>(interactions / reach) * 100</td></tr>
        <tr><td><b>tier</b></td><td>String</td><td>Enum</td><td>'low' (&lt;2%), 'medium' (2-5%), 'high' (&gt;5%)</td></tr>
      </tbody>
    </table>

    <h3>Collection 5: follower_snapshots (Historical Follower Records)</h3>
    <table>
      <thead><tr><th>Field Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><b>_id</b></td><td>ObjectId</td><td>Primary Key</td><td>Unique snapshot identifier</td></tr>
        <tr><td><b>tenant_id</b></td><td>String</td><td>Multi-Tenant Key</td><td>Foreign Key to tenant</td></tr>
        <tr><td><b>platform</b></td><td>String</td><td>Enum</td><td>'instagram', 'linkedin', 'youtube'</td></tr>
        <tr><td><b>date</b></td><td>String</td><td>YYYY-MM-DD</td><td>Snapshot date</td></tr>
        <tr><td><b>follower_count</b></td><td>Integer</td><td>&ge; 0</td><td>Total followers on this date</td></tr>
      </tbody>
    </table>

    <h3>Collection 6: competitors (Competitor Agencies)</h3>
    <table>
      <thead><tr><th>Field Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><b>_id</b></td><td>ObjectId</td><td>Primary Key</td><td>Unique competitor identifier</td></tr>
        <tr><td><b>tenant_id</b></td><td>String</td><td>Multi-Tenant Key</td><td>Foreign Key to tenant</td></tr>
        <tr><td><b>handle</b></td><td>String</td><td>Required</td><td>Competitor handle (e.g. '@PulseMedia')</td></tr>
        <tr><td><b>platform</b></td><td>String</td><td>Enum</td><td>'instagram', 'linkedin', 'youtube'</td></tr>
        <tr><td><b>engagement_rate</b></td><td>Float</td><td>Percentage</td><td>Competitor benchmark engagement rate</td></tr>
      </tbody>
    </table>

    <h3>Collection 7: comments (Audience Feedback & VADER Sentiment)</h3>
    <table>
      <thead><tr><th>Field Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><b>_id</b></td><td>ObjectId</td><td>Primary Key</td><td>Unique comment identifier</td></tr>
        <tr><td><b>tenant_id</b></td><td>String</td><td>Multi-Tenant Key</td><td>Foreign Key to tenant</td></tr>
        <tr><td><b>post_id</b></td><td>String</td><td>Foreign Key</td><td>Reference to target post</td></tr>
        <tr><td><b>text</b></td><td>String</td><td>Required</td><td>Comment text body</td></tr>
        <tr><td><b>sentiment</b></td><td>String</td><td>Enum</td><td>'positive', 'neutral', 'negative'</td></tr>
        <tr><td><b>compound_score</b></td><td>Float</td><td>Score</td><td>VADER polarity (-1.0 to +1.0)</td></tr>
      </tbody>
    </table>

    <h3>Collection 8: notifications (In-App Alerts)</h3>
    <table>
      <thead><tr><th>Field Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><b>_id</b></td><td>ObjectId</td><td>Primary Key</td><td>Unique alert identifier</td></tr>
        <tr><td><b>tenant_id</b></td><td>String</td><td>Multi-Tenant Key</td><td>Foreign Key to tenant</td></tr>
        <tr><td><b>type</b></td><td>String</td><td>Enum</td><td>'upcoming_post', 'low_prediction', 'retrain_alert'</td></tr>
        <tr><td><b>title</b></td><td>String</td><td>Required</td><td>Alert headline</td></tr>
        <tr><td><b>is_read</b></td><td>Boolean</td><td>Default False</td><td>Read status flag</td></tr>
      </tbody>
    </table>

    <h3>Collection 9: ab_tests (A/B Multivariate Campaigns)</h3>
    <table>
      <thead><tr><th>Field Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><b>_id</b></td><td>ObjectId</td><td>Primary Key</td><td>Unique test identifier</td></tr>
        <tr><td><b>tenant_id</b></td><td>String</td><td>Multi-Tenant Key</td><td>Foreign Key to tenant</td></tr>
        <tr><td><b>title</b></td><td>String</td><td>Required</td><td>Campaign title</td></tr>
        <tr><td><b>variant_post_ids</b></td><td>Array[String]</td><td>Required</td><td>Post IDs of variants A and B</td></tr>
        <tr><td><b>status</b></td><td>String</td><td>Enum</td><td>'running', 'completed'</td></tr>
      </tbody>
    </table>
  </div>

  <!-- 7. ALL SCREENSHOTS WITH URL (ALL 17 SCREENSHOTS) -->
  <div class="page-break">
    <h2>7. ALL SCREENSHOTS WITH URL</h2>

    <h3>7.1 Admin Side Screens & URLs (Full Access Modules)</h3>
    <p>The Administrator role possesses complete platform access across all 12 navigation modules, including content creation, scheduling, predictive ML scoring, and role governance.</p>

    <div class="screenshot-grid">
      <div class="screenshot-card">
        <img src="{screenshots_b64[1]}" class="diagram-img" alt="Login & Role Switcher" />
        <p class="caption">Figure 7.1: Authentication & Viva Demo Role Switcher (URL: http://127.0.0.1:3000/login)</p>
        <p class="desc">Universal login gateway featuring 1-click viva evaluator role switcher (Admin, Editor, Client) and instant credential prepopulation.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[2]}" class="diagram-img" alt="Executive Analytics Dashboard" />
        <p class="caption">Figure 7.2: Executive Analytics & ML Model Health Dashboard (URL: http://127.0.0.1:3000/dashboard)</p>
        <p class="desc">Real-time executive cockpit displaying cross-platform engagement metrics (88.0% ML model accuracy), audience distributions, and continuous model retraining trigger.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[3]}" class="diagram-img" alt="Content Calendar" />
        <p class="caption">Figure 7.3: Interactive Monthly Content Calendar Grid (URL: http://127.0.0.1:3000/calendar)</p>
        <p class="desc">Full-screen multi-platform content scheduling calendar with color-coded status badges, draft/published filters, and post inspection drawer.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[4]}" class="diagram-img" alt="Post Composer" />
        <p class="caption">Figure 7.4: Post Composer & Pre-Flight AI Assistant (URL: http://127.0.0.1:3000/compose)</p>
        <p class="desc">AI-powered creation suite featuring Random Forest engagement scoring, VADER sentiment analysis, 24-hour best-time sweep, and hashtag generator.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[5]}" class="diagram-img" alt="Thumbnail Aesthetic Scorer" />
        <p class="caption">Figure 7.5: OpenCV Headless Thumbnail Aesthetic Scorer (URL: http://127.0.0.1:3000/thumbnail)</p>
        <p class="desc">Computer vision thumbnail analyzer calculating visual rule-of-thirds, Shannon entropy contrast, facial detection, and CTR aesthetic grade.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[6]}" class="diagram-img" alt="Hashtag Velocity Trends" />
        <p class="caption">Figure 7.6: Hashtag Velocity Trends & Rising Tag Radar (URL: http://127.0.0.1:3000/trends)</p>
        <p class="desc">Hashtag momentum radar tracking volume growth velocity, competition index, and viral trend surges across social platforms.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[7]}" class="diagram-img" alt="Topic Recommendations" />
        <p class="caption">Figure 7.7: Semantic Topic Recommendations & Content Clusters (URL: http://127.0.0.1:3000/recommendations)</p>
        <p class="desc">TF-IDF content vectorization cluster engine generating audience-tailored content recommendations and high-performing themes.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[8]}" class="diagram-img" alt="Follower Growth Forecast" />
        <p class="caption">Figure 7.8: Follower Growth Forecasting with Facebook Prophet (URL: http://127.0.0.1:3000/forecast)</p>
        <p class="desc">Additive time-series predictive modeling engine displaying 30-day follower trajectory with 95% confidence intervals and weekly seasonality decomposition.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[9]}" class="diagram-img" alt="Multivariate A/B Testing" />
        <p class="caption">Figure 7.9: Multivariate A/B Testing Arena & Confidence Calculator (URL: http://127.0.0.1:3000/ab-tests)</p>
        <p class="desc">Multivariate post split testing module featuring 2-sample Z-test statistical significance, live CTR comparison, and auto-winner declaration.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[10]}" class="diagram-img" alt="Competitor Intelligence" />
        <p class="caption">Figure 7.10: Competitor Benchmark Intelligence & Share of Voice (URL: http://127.0.0.1:3000/competitors)</p>
        <p class="desc">Market benchmark tracking comparing posting frequency, engagement per post, follower growth velocity, and share of voice against rivals.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[11]}" class="diagram-img" alt="Notification Center" />
        <p class="caption">Figure 7.11: In-App Notification Center & Audit Stream (URL: http://127.0.0.1:3000/notifications)</p>
        <p class="desc">Centralized alerts stream showing scheduled post triggers, ML retraining completion notices, and system-wide audit logs.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[12]}" class="diagram-img" alt="Team RBAC Management" />
        <p class="caption">Figure 7.12: Team & Role-Based Access Control (RBAC) Management (URL: http://127.0.0.1:3000/team)</p>
        <p class="desc">Granular user permission management console with role assignment (Admin, Editor, Client), active user statuses, and permission enforcement.</p>
      </div>
    </div>

    <h3>7.2 Client Side Screens & URLs (Read-Only Observer Portal)</h3>
    <p>The Client role provides a restricted 6-module view. Content creation and modification tools are strictly hidden, calendar modification buttons are suppressed, and the model retraining trigger displays an admin-only security lock notice.</p>

    <div class="screenshot-grid">
      <div class="screenshot-card">
        <img src="{screenshots_b64[13]}" class="diagram-img" alt="Client Dashboard" />
        <p class="caption">Figure 7.13: Client Portal Executive Dashboard (URL: http://127.0.0.1:3000/dashboard)</p>
        <p class="desc">Restricted observer portal view with creation tools hidden, sidebar reduced to 6 modules, and Model Retraining button displaying admin-only lock.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[14]}" class="diagram-img" alt="Client Calendar" />
        <p class="caption">Figure 7.14: Client Read-Only Content Calendar View (URL: http://127.0.0.1:3000/calendar)</p>
        <p class="desc">Read-only calendar grid allowing external stakeholders to inspect scheduled campaigns without edit, reschedule, or delete controls.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[15]}" class="diagram-img" alt="Client Forecast" />
        <p class="caption">Figure 7.15: Client 30-Day Follower Projection View (URL: http://127.0.0.1:3000/forecast)</p>
        <p class="desc">Executive growth trajectory view tailored for clients and investors, displaying Prophet model projections and weekly seasonality trends.</p>
      </div>
    </div>

    <h3>7.3 Reports (Printable PDF & Export in Excel)</h3>
    <p>Fulfilling GLS University Syllabus Section 7.3, ContentIQ provides two native enterprise report export mechanisms on the Executive Dashboard:</p>
    <p><b>1. Export to Excel (.csv):</b> Located on the top-right of the dashboard. Downloads 'ContentIQ_Performance_Report_YYYY-MM-DD.csv' with platform distributions, summary KPIs, and ML accuracy (88.0%).<br>
       <b>2. Print Report (PDF):</b> Invokes browser print styling (@media print), cleanly formatting all cards and charts into an executive-ready hardcopy document.</p>

    <div class="screenshot-grid">
      <div class="screenshot-card">
        <img src="{screenshots_b64[16]}" class="diagram-img" alt="Excel Export" />
        <p class="caption">Figure 7.16: Real-Time Performance Export in Excel (.csv) (URL: http://127.0.0.1:3000/dashboard)</p>
        <p class="desc">Instant client-side CSV export generating 'ContentIQ_Performance_Report_YYYY-MM-DD.csv' with raw campaign distributions and engagement metrics.</p>
      </div>

      <div class="screenshot-card">
        <img src="{screenshots_b64[17]}" class="diagram-img" alt="Print PDF Report" />
        <p class="caption">Figure 7.17: Publication-Ready Printable Executive PDF Report (URL: http://127.0.0.1:3000/dashboard)</p>
        <p class="desc">Responsive @media print layout cleanly converting all KPI cards, engagement graphs, and platform charts into a publication-ready executive print report.</p>
      </div>
    </div>
  </div>

  <!-- 8. REFERENCES -->
  <div class="page-break">
    <h2>8. REFERENCES & BIBLIOGRAPHY</h2>
    <ol>
      <li>S. Tiangolo, <i>FastAPI: Modern Web Framework for Building APIs with Python 3.8+</i>, 2024. https://fastapi.tiangolo.com/</li>
      <li>K. Banker et al., <i>MongoDB in Action: Covers MongoDB version 3.0+</i>, 2nd ed. Manning Publications, 2016.</li>
      <li>L. Breiman, 'Random Forests', <i>Machine Learning</i>, vol. 45, no. 1, pp. 5–32, 2001.</li>
      <li>S. J. Taylor and B. Letham, 'Forecasting at scale', <i>The American Statistician</i>, vol. 72, no. 1, pp. 37–45, 2018.</li>
      <li>C. Hutto and E. Gilbert, 'VADER: A Parsimonious Rule-Based Model for Sentiment Analysis', <i>ICWSM-14</i>, 2014.</li>
      <li>Meta Open Source, <i>React 18: A JavaScript library for building user interfaces</i>, 2024. https://react.dev/</li>
      <li>Faculty of Computer Applications & IT (FCAIT), GLS University, <i>Capstone Project – II Guidelines (222301907)</i>, Ahmedabad, Academic Year 2026–2027.</li>
      <li>G. Bradski and A. Kaehler, <i>Learning OpenCV: Computer Vision with the OpenCV Library</i>, O'Reilly Media, 2008.</li>
      <li>A. Solem et al., <i>Celery: Distributed Task Queue</i>, Celery Documentation, 2024. https://docs.celeryq.dev/</li>
      <li>F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python', <i>JMLR</i>, vol. 12, pp. 2825–2830, 2011.</li>
    </ol>
  </div>

</div>

</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Successfully generated Full HTML Report: {OUT_HTML}")

if __name__ == "__main__":
    generate_full_html()

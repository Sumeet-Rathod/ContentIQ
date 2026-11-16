"""
ContentIQ - Comprehensive PDF Report Generator
Generates a complete, publication-ready PDF document using ReportLab
with embedded high-res UML diagrams, UI screenshots, complete 9-collection data dictionary,
and full academic documentation strictly matching GLS University FCAIT guidelines.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

DIAGRAMS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\diagrams"
SCREENSHOTS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\screenshots"
OUT_PDF = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\ContentIQ_Final_Documentation_Report.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        if self._pageNumber > 2:  # Suppress page numbers on Cover Page (1) and Certificate (2)
            self.saveState()
            self.setFont("Helvetica", 8.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(50, 32, "ContentIQ — 222301907 Capstone Project – II (GLS University FCAIT)")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(A4[0] - 50, 32, page_text)
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(50, 44, A4[0] - 50, 44)
            self.restoreState()

def build_comprehensive_pdf():
    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    printable_w = A4[0] - 100 # 495 points

    styles = getSampleStyleSheet()

    c_navy = colors.HexColor("#1F3864")
    c_gold = colors.HexColor("#D97706")
    c_slate = colors.HexColor("#334155")
    c_light = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=c_navy, alignment=1, spaceAfter=8)
    subtitle_style = ParagraphStyle('CoverSubtitle', fontName='Helvetica-Oblique', fontSize=12, leading=16, textColor=colors.HexColor("#64748B"), alignment=1, spaceAfter=20)
    center_bold = ParagraphStyle('CenterBold', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=c_navy, alignment=1)
    center_normal = ParagraphStyle('CenterNormal', fontName='Helvetica', fontSize=10.5, leading=15, textColor=c_slate, alignment=1)

    h1_style = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=c_navy, spaceBefore=14, spaceAfter=8, keepWithNext=True)
    h2_style = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=c_navy, spaceBefore=10, spaceAfter=6, keepWithNext=True)
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9.5, leading=14, textColor=c_slate, spaceAfter=6)
    caption_style = ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=colors.HexColor("#64748B"), alignment=1, spaceBefore=4, spaceAfter=10)

    th_style = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white)
    tc_style = ParagraphStyle('TC', fontName='Helvetica', fontSize=8, leading=11, textColor=c_slate)
    tcb_style = ParagraphStyle('TCB', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_navy)

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    cover_content = [
        [Paragraph("ContentIQ", title_style)],
        [Paragraph("An AI-Powered Multi-Tenant Content Performance and Scheduling Platform", subtitle_style)],
        [Spacer(1, 15)],
        [Paragraph("<b>Project Report</b><br/>Submitted for the subject of", center_normal)],
        [Paragraph("<b>222301907 Capstone Project – II</b>", center_bold)],
        [Paragraph("<b>Integrated Master of Computer Applications (iMCA)</b>", center_bold)],
        [Paragraph("Semester IX", center_normal)],
        [Spacer(1, 15)],
        [Paragraph("<b>Submitted By:</b>", center_bold)],
        [Paragraph("Student 1: [Your Full Name] (Enrollment No: ____________________)<br/>Student 2: [Partner Full Name] (Enrollment No: ____________________)", center_normal)],
        [Spacer(1, 15)],
        [Paragraph("<b>Under the Guidance of:</b>", center_bold)],
        [Paragraph("Dr./Prof. Name of Internal Guide<br/>FCAIT, GLS University", center_normal)],
        [Spacer(1, 20)],
        [Paragraph("<b>Faculty of Computer Applications & IT (FCAIT)</b><br/><b>iMCA Programme, Ahmedabad</b><br/><b>GLS UNIVERSITY</b><br/><br/>Academic Year 2026–2027", center_bold)]
    ]

    cover_table = Table(cover_content, colWidths=[printable_w])
    cover_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 2.5, c_navy),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # =========================================================================
    # 2. COLLEGE CERTIFICATE
    # =========================================================================
    cert_content = [
        [Paragraph("<b>GLS UNIVERSITY</b><br/>Faculty of Computer Applications & IT<br/>iMCA Programme<br/>Ahmedabad<br/><br/><u><b>CERTIFICATE</b></u>", center_bold)],
        [Spacer(1, 20)],
        [Paragraph(
            "This is to certify that the following students of <b>Semester IX Integrated Master of Computer Applications (iMCA) Programme</b>, "
            "Faculty of Computer Applications & IT (FCAIT), GLS University, Ahmedabad, have successfully completed the subject project titled<br/><br/>"
            "<b>“ContentIQ: An AI-Powered Multi-Tenant Content Performance and Scheduling Platform for Social Media Creators and Agencies”</b><br/><br/>"
            "for the course <b>222301907 Capstone Project – II - System Design and Implementation</b> during the Academic Year <b>2026–2027</b>.",
            ParagraphStyle('CertText', parent=body_style, fontSize=10.5, leading=17, alignment=4)
        )],
        [Spacer(1, 30)],
        [Paragraph("Date of Submission: 23rd October 2026", body_style)],
        [Spacer(1, 35)],
        [Table([
            [Paragraph("<b>Dr./Prof. Name of Internal Guide</b><br/>Project Guide<br/>FCAIT, GLS University", body_style),
             Paragraph("<b>Dr. Tripti Dodiya</b><br/>Dean<br/>FCAIT, GLS University", ParagraphStyle('RightSig', parent=body_style, alignment=2))]
        ], colWidths=[(printable_w - 40)/2, (printable_w - 40)/2])]
    ]

    cert_table = Table(cert_content, colWidths=[printable_w])
    cert_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 2.0, c_navy),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(cert_table)
    story.append(PageBreak())

    # =========================================================================
    # 3. INDEX
    # =========================================================================
    story.append(Paragraph("3. INDEX", h1_style))
    story.append(Spacer(1, 6))

    index_data = [
        [Paragraph("Section", th_style), Paragraph("Topic / Chapter Name", th_style), Paragraph("Page No.", th_style)],
        [Paragraph("1", tcb_style), Paragraph("Cover Page", tc_style), Paragraph("1", tc_style)],
        [Paragraph("2", tcb_style), Paragraph("College Certificate", tc_style), Paragraph("2", tc_style)],
        [Paragraph("3", tcb_style), Paragraph("Index", tc_style), Paragraph("3", tc_style)],
        [Paragraph("4", tcb_style), Paragraph("Brief of System (Problem Statement, Scope, Objectives, Tech Stack, Specs)", tc_style), Paragraph("4", tc_style)],
        [Paragraph("5", tcb_style), Paragraph("UML Diagrams (Use Case, Class, Activity Swimlane, Sequence, State Chart)", tc_style), Paragraph("6", tc_style)],
        [Paragraph("6", tcb_style), Paragraph("Data Dictionary (Specifications for 9 MongoDB Collections)", tc_style), Paragraph("12", tc_style)],
        [Paragraph("7", tcb_style), Paragraph("All Screenshots with URL (Admin Side, Client Side, Excel/PDF Reports)", tc_style), Paragraph("16", tc_style)],
        [Paragraph("8", tcb_style), Paragraph("References & Bibliography (IEEE Standards)", tc_style), Paragraph("20", tc_style)],
    ]
    t_idx = Table(index_data, colWidths=[55, 380, 60])
    t_idx.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_navy),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_idx)
    story.append(Spacer(1, 14))

    # =========================================================================
    # 4. BRIEF OF SYSTEM
    # =========================================================================
    story.append(Paragraph("4. BRIEF OF SYSTEM", h1_style))
    story.append(Paragraph("4.1 Problem Statement", h2_style))
    story.append(Paragraph(
        "Social media marketing agencies and multi-platform creators manage portfolios across Instagram, LinkedIn, and YouTube, "
        "facing four key operational bottlenecks:<br/>"
        "<b>1. Subjective Best-Time Scheduling:</b> Creators rely on general rules of thumb rather than data-driven channel engagement distributions.<br/>"
        "<b>2. Blind Content Publishing:</b> Content authors lack pre-flight AI engagement evaluation to gauge potential reception prior to publishing.<br/>"
        "<b>3. Multi-Tenant Data Leakage Risk:</b> Multi-agency tools frequently mix client records or demand expensive per-tenant infrastructure.<br/>"
        "<b>4. Static AI Degradation:</b> Traditional machine learning models suffer immediate accuracy drift because they do not continuously retrain against real post-publication analytics.",
        body_style
    ))

    story.append(Paragraph("4.2 System Scope & Objectives", h2_style))
    story.append(Paragraph(
        "• <b>Production-Ready Multi-Tenancy:</b> Hard data isolation utilizing MongoDB tenant-scoped documents and JWT claims.<br/>"
        "• <b>Pre-Flight ML Scoring:</b> Real-time Random Forest engagement tier predictions (Low <2%, Medium 2-5%, High >5%) with 24-hour best-time sweeps.<br/>"
        "• <b>Computer Vision & NLP Analysis:</b> Automated OpenCV 4.10 thumbnail balance scoring and VADER sentiment classification.<br/>"
        "• <b>Continuous Retraining Feedback Loop:</b> Automated feedback pipeline retraining the model once >= 50 real metric records accumulate.<br/>"
        "• <b>Local Timezone Preservation:</b> Scheduled hours stored as local ISO strings without UTC conversion, preventing feature drift.",
        body_style
    ))

    story.append(Paragraph("4.3 Technology Stack Justification", h2_style))
    ts_data = [
        [Paragraph("Layer", th_style), Paragraph("Technology", th_style), Paragraph("Academic & Viva Justification", th_style)],
        [Paragraph("Frontend", tcb_style), Paragraph("React 18, Vite 6, Chart.js", tc_style), Paragraph("Component-driven SPA, fast HMR, executive Navy & Gold theme.", tc_style)],
        [Paragraph("Backend", tcb_style), Paragraph("FastAPI 0.115.0, Pydantic v2", tc_style), Paragraph("High-throughput asynchronous REST API with automatic OpenAPI Swagger docs.", tc_style)],
        [Paragraph("Database", tcb_style), Paragraph("MongoDB 7.0 Community", tc_style), Paragraph("Document-oriented schema suited for polymorphic social media posts.", tc_style)],
        [Paragraph("Cache / Broker", tcb_style), Paragraph("Redis Server 7.0", tc_style), Paragraph("In-memory store providing sub-millisecond caching for dashboards.", tc_style)],
        [Paragraph("Async Worker", tcb_style), Paragraph("Celery 5.4 (--pool=solo)", tc_style), Paragraph("Decoupled background scheduler for automated post publishing.", tc_style)],
        [Paragraph("Machine Learning", tcb_style), Paragraph("Scikit-Learn, OpenCV, Prophet, VADER", tc_style), Paragraph("Random Forest classification, time-series forecasting, and computer vision.", tc_style)],
    ]
    t_ts = Table(ts_data, colWidths=[80, 150, 265])
    t_ts.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_navy),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_ts)
    story.append(PageBreak())

    # =========================================================================
    # 5. UML DIAGRAMS (WITH VISUAL EMBEDDED IMAGES)
    # =========================================================================
    story.append(Paragraph("5. UML DIAGRAMS", h1_style))

    # 5.1 Use Case Diagram
    story.append(Paragraph("5.1 Use Case Diagram", h2_style))
    story.append(Paragraph("Defines functional boundaries between Admin, Editor, Client, and Celery background worker:", body_style))
    uc_img_p = os.path.join(DIAGRAMS_DIR, "use_case_diagram.png")
    if os.path.exists(uc_img_p):
        story.append(RLImage(uc_img_p, width=printable_w, height=printable_w * 0.65))
        story.append(Paragraph("Figure 5.1: ContentIQ System Use Case Diagram", caption_style))
    story.append(PageBreak())

    # 5.2 Detailed Class Diagram
    story.append(Paragraph("5.2 Detailed Class Diagram", h2_style))
    story.append(Paragraph("Object-Oriented domain entities, visibility, attributes, methods, and multiplicities:", body_style))
    cls_img_p = os.path.join(DIAGRAMS_DIR, "class_diagram.png")
    if os.path.exists(cls_img_p):
        story.append(RLImage(cls_img_p, width=printable_w, height=printable_w * 0.64))
        story.append(Paragraph("Figure 5.2: ContentIQ Domain Class Diagram with Multiplicities", caption_style))
    story.append(PageBreak())

    # 5.3 Swimlane Activity Diagram
    story.append(Paragraph("5.3 Activity Diagram (Swimlane)", h2_style))
    story.append(Paragraph("Four distinct operational swimlanes (User, React SPA, FastAPI Gateway, Celery Worker & MongoDB):", body_style))
    swim_img_p = os.path.join(DIAGRAMS_DIR, "swimlane_activity_diagram.png")
    if os.path.exists(swim_img_p):
        story.append(RLImage(swim_img_p, width=printable_w, height=printable_w * 0.66))
        story.append(Paragraph("Figure 5.3: ContentIQ 4-Lane Swimlane Activity Diagram", caption_style))
    story.append(PageBreak())

    # 5.4 Sequence Diagram
    story.append(Paragraph("5.4 Sequence Diagram", h2_style))
    story.append(Paragraph("Pre-flight machine learning scoring and 24-hour best-time probability sweep sequence:", body_style))
    seq_img_p = os.path.join(DIAGRAMS_DIR, "sequence_diagram.png")
    if os.path.exists(seq_img_p):
        story.append(RLImage(seq_img_p, width=printable_w, height=printable_w * 0.58))
        story.append(Paragraph("Figure 5.4: Pre-Flight AI Prediction & 24h Sweep Sequence Diagram", caption_style))
    story.append(Spacer(1, 10))

    # 5.5 State Chart Diagram
    story.append(Paragraph("5.5 State Chart Diagram (Post Lifecycle)", h2_style))
    story.append(Paragraph("State transitions from Draft to Scheduled, Published, Metrics Collected, and Continuous Retraining:", body_style))
    state_img_p = os.path.join(DIAGRAMS_DIR, "state_chart_diagram.png")
    if os.path.exists(state_img_p):
        story.append(RLImage(state_img_p, width=printable_w, height=printable_w * 0.52))
        story.append(Paragraph("Figure 5.5: Post Lifecycle State Chart Diagram", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # 6. DATA DICTIONARY (ALL 9 COLLECTIONS)
    # =========================================================================
    story.append(Paragraph("6. DATA DICTIONARY", h1_style))
    story.append(Paragraph("Specifications for all 9 MongoDB collections in the 'contentiq' database:", body_style))

    collections_specs = [
        ("tenants", "Workspaces & Agencies", [
            ("_id", "ObjectId", "Primary Key", "Unique workspace identifier"),
            ("name", "String", "Required", "Agency Name (e.g. 'Apex Digital Agency')"),
            ("plan", "String", "Enum", "Subscription tier: 'free', 'pro', 'enterprise'"),
            ("created_at", "ISO Datetime", "Required", "Local ISO creation timestamp"),
        ]),
        ("users", "User Accounts & RBAC Roles", [
            ("_id", "ObjectId", "Primary Key", "Unique user identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key reference to tenants._id"),
            ("email", "String", "Unique, Required", "Unique login email address"),
            ("name", "String", "Required", "Full name of staff member"),
            ("hashed_password", "String", "Required", "Bcrypt hashed password (12 salt rounds)"),
            ("role", "String", "Enum", "'admin', 'editor', 'client'"),
            ("created_at", "ISO Datetime", "Required", "Account creation timestamp"),
        ]),
        ("posts", "Social Media Posts", [
            ("_id", "ObjectId", "Primary Key", "Unique post identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key reference to tenants._id"),
            ("platform", "String", "Enum", "'instagram', 'linkedin', 'youtube'"),
            ("caption", "String", "Required", "Text caption and content"),
            ("hashtags", "Array[String]", "Required", "List of hashtag strings"),
            ("scheduled_time", "ISO Datetime", "Indexed", "Scheduled publication local ISO datetime"),
            ("scheduled_hour", "Integer", "Derived", "Integer hour (0-23) without UTC drift"),
            ("status", "String", "Enum", "'draft', 'scheduled', 'published'"),
        ]),
        ("post_metrics", "Performance Feedback", [
            ("_id", "ObjectId", "Primary Key", "Unique metric identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("post_id", "String", "Foreign Key", "Foreign reference to posts._id"),
            ("likes", "Integer", ">= 0", "Total likes count"),
            ("comments", "Integer", ">= 0", "Total comments count"),
            ("reach", "Integer", ">= 0", "Unique viewer reach"),
            ("engagement_rate", "Float", "Percentage", "(interactions / reach) * 100"),
            ("tier", "String", "Enum", "'low' (<2%), 'medium' (2-5%), 'high' (>5%)"),
        ]),
        ("follower_snapshots", "Historical Follower Records", [
            ("_id", "ObjectId", "Primary Key", "Unique snapshot identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("platform", "String", "Enum", "'instagram', 'linkedin', 'youtube'"),
            ("date", "String", "Format YYYY-MM-DD", "Snapshot date"),
            ("follower_count", "Integer", ">= 0", "Total followers on this date"),
        ]),
        ("competitors", "Competitor Agencies", [
            ("_id", "ObjectId", "Primary Key", "Unique competitor identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("handle", "String", "Required", "Competitor handle (e.g. '@PulseMedia')"),
            ("platform", "String", "Enum", "'instagram', 'linkedin', 'youtube'"),
            ("engagement_rate", "Float", "Percentage", "Competitor benchmark engagement rate"),
        ]),
        ("comments", "Audience Comments & Sentiment", [
            ("_id", "ObjectId", "Primary Key", "Unique comment identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("post_id", "String", "Foreign Key", "Reference to target post"),
            ("text", "String", "Required", "Comment text body"),
            ("sentiment", "String", "Enum", "'positive', 'neutral', 'negative'"),
            ("compound_score", "Float", "Score", "VADER polarity (-1.0 to +1.0)"),
        ]),
        ("notifications", "In-App Alerts", [
            ("_id", "ObjectId", "Primary Key", "Unique alert identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("type", "String", "Enum", "'upcoming_post', 'low_prediction', 'retrain_alert'"),
            ("title", "String", "Required", "Alert headline"),
            ("is_read", "Boolean", "Default False", "Read status flag"),
        ]),
        ("ab_tests", "A/B Multivariate Campaigns", [
            ("_id", "ObjectId", "Primary Key", "Unique test identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("title", "String", "Required", "Campaign title"),
            ("variant_post_ids", "Array[String]", "Required", "Post IDs of variants A and B"),
            ("status", "String", "Enum", "'running', 'completed'"),
        ]),
    ]

    for c_name, c_desc, c_fields in collections_specs:
        story.append(Paragraph(f"<b>Collection: {c_name}</b> ({c_desc})", h2_style))
        c_table_data = [[Paragraph("Field Name", th_style), Paragraph("Data Type", th_style), Paragraph("Constraints / Key", th_style), Paragraph("Description", th_style)]]
        for f1, f2, f3, f4 in c_fields:
            c_table_data.append([Paragraph(f1, tcb_style), Paragraph(f2, tc_style), Paragraph(f3, tc_style), Paragraph(f4, tc_style)])
        t_col = Table(c_table_data, colWidths=[90, 85, 120, 200])
        t_col.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), c_navy),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(t_col)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =========================================================================
    # 7. ALL SCREENSHOTS WITH URL (WITH ALL 17 HIGH-RES EMBEDDED SCREENSHOTS)
    # =========================================================================
    story.append(Paragraph("7. ALL SCREENSHOTS WITH URL", h1_style))
    story.append(Paragraph("7.1 Admin Side Screens & URLs (Full Access Modules)", h2_style))
    story.append(Paragraph("Unrestricted access across all 12 modules including model retraining and team management:", body_style))

    admin_screens = [
        ("screenshot_01_admin_login.png", "Figure 7.1: Authentication & Viva Demo Role Switcher (URL: http://127.0.0.1:3000/login)",
         "Universal login gateway featuring 1-click viva evaluator role switcher (Admin, Editor, Client) and instant credential prepopulation."),
        ("screenshot_02_admin_dashboard.png", "Figure 7.2: Executive Analytics & ML Model Health Dashboard (URL: http://127.0.0.1:3000/dashboard)",
         "Real-time executive cockpit displaying cross-platform engagement metrics (88.0% ML model accuracy), audience distributions, and continuous model retraining trigger."),
        ("screenshot_03_admin_calendar.png", "Figure 7.3: Interactive Monthly Content Calendar Grid (URL: http://127.0.0.1:3000/calendar)",
         "Full-screen multi-platform content scheduling calendar with color-coded status badges, draft/published filters, and post inspection drawer."),
        ("screenshot_04_admin_composer.png", "Figure 7.4: Post Composer & Pre-Flight AI Assistant (URL: http://127.0.0.1:3000/compose)",
         "AI-powered creation suite featuring Random Forest engagement scoring, VADER sentiment analysis, 24-hour best-time sweep, and hashtag generator."),
        ("screenshot_05_admin_thumbnail.png", "Figure 7.5: OpenCV Headless Thumbnail Aesthetic Scorer (URL: http://127.0.0.1:3000/thumbnail)",
         "Computer vision thumbnail analyzer calculating visual rule-of-thirds, Shannon entropy contrast, facial detection, and CTR aesthetic grade."),
        ("screenshot_06_admin_trends.png", "Figure 7.6: Hashtag Velocity Trends & Rising Tag Radar (URL: http://127.0.0.1:3000/trends)",
         "Hashtag momentum radar tracking volume growth velocity, competition index, and viral trend surges across social platforms."),
        ("screenshot_07_admin_recommendations.png", "Figure 7.7: Semantic Topic Recommendations & Content Clusters (URL: http://127.0.0.1:3000/recommendations)",
         "TF-IDF content vectorization cluster engine generating audience-tailored content recommendations and high-performing themes."),
        ("screenshot_08_admin_forecast.png", "Figure 7.8: Follower Growth Forecasting with Facebook Prophet (URL: http://127.0.0.1:3000/forecast)",
         "Additive time-series predictive modeling engine displaying 30-day follower trajectory with 95% confidence intervals and weekly seasonality decomposition."),
        ("screenshot_09_admin_ab_testing.png", "Figure 7.9: Multivariate A/B Testing Arena & Confidence Calculator (URL: http://127.0.0.1:3000/ab-tests)",
         "Multivariate post split testing module featuring 2-sample Z-test statistical significance, live CTR comparison, and auto-winner declaration."),
        ("screenshot_10_admin_competitors.png", "Figure 7.10: Competitor Benchmark Intelligence & Share of Voice (URL: http://127.0.0.1:3000/competitors)",
         "Market benchmark tracking comparing posting frequency, engagement per post, follower growth velocity, and share of voice against rivals."),
        ("screenshot_11_admin_notifications.png", "Figure 7.11: In-App Notification Center & Audit Stream (URL: http://127.0.0.1:3000/notifications)",
         "Centralized alerts stream showing scheduled post triggers, ML retraining completion notices, and system-wide audit logs."),
        ("screenshot_12_admin_team_rbac.png", "Figure 7.12: Team & Role-Based Access Control (RBAC) Management (URL: http://127.0.0.1:3000/team)",
         "Granular user permission management console with role assignment (Admin, Editor, Client), active user statuses, and permission enforcement.")
    ]

    for fname, cap, desc in admin_screens:
        img_p = os.path.join(SCREENSHOTS_DIR, fname)
        if os.path.exists(img_p):
            story.append(RLImage(img_p, width=printable_w, height=printable_w * 0.58))
            story.append(Paragraph(cap, caption_style))
            story.append(Paragraph(f"<b>Feature:</b> {desc}", body_style))
            story.append(Spacer(1, 10))

    story.append(PageBreak())

    # 7.2 Client Side
    story.append(Paragraph("7.2 Client Side Screens & URLs (Read-Only Observer Portal)", h2_style))
    story.append(Paragraph("Strict read-only observer portal (6 modules only). Creation and deletion buttons are hidden:", body_style))

    client_screens = [
        ("screenshot_13_client_dashboard.png", "Figure 7.13: Client Portal Executive Dashboard (URL: http://127.0.0.1:3000/dashboard)",
         "Restricted observer portal view with creation tools hidden, sidebar reduced to 6 modules, and Model Retraining button displaying admin-only lock."),
        ("screenshot_14_client_calendar.png", "Figure 7.14: Client Read-Only Content Calendar View (URL: http://127.0.0.1:3000/calendar)",
         "Read-only calendar grid allowing external stakeholders to inspect scheduled campaigns without edit, reschedule, or delete controls."),
        ("screenshot_15_client_forecast.png", "Figure 7.15: Client 30-Day Follower Projection View (URL: http://127.0.0.1:3000/forecast)",
         "Executive growth trajectory view tailored for clients and investors, displaying Prophet model projections and weekly seasonality trends.")
    ]

    for fname, cap, desc in client_screens:
        img_p = os.path.join(SCREENSHOTS_DIR, fname)
        if os.path.exists(img_p):
            story.append(RLImage(img_p, width=printable_w, height=printable_w * 0.58))
            story.append(Paragraph(cap, caption_style))
            story.append(Paragraph(f"<b>Feature:</b> {desc}", body_style))
            story.append(Spacer(1, 10))

    story.append(PageBreak())

    # 7.3 Reports
    story.append(Paragraph("7.3 Reports (Printable PDF & Export in Excel)", h2_style))
    story.append(Paragraph("Native export action buttons on Executive Dashboard fulfilling syllabus item 7.3:", body_style))

    report_screens = [
        ("screenshot_16_reports_excel_export.png", "Figure 7.16: Real-Time Performance Export in Excel (.csv) (URL: http://127.0.0.1:3000/dashboard)",
         "Instant client-side CSV export generating 'ContentIQ_Performance_Report_YYYY-MM-DD.csv' with raw campaign distributions and engagement metrics."),
        ("screenshot_17_reports_print_pdf.png", "Figure 7.17: Publication-Ready Printable Executive PDF Report (URL: http://127.0.0.1:3000/dashboard)",
         "Responsive @media print layout cleanly converting all KPI cards, engagement graphs, and platform charts into a publication-ready executive print report.")
    ]

    for fname, cap, desc in report_screens:
        img_p = os.path.join(SCREENSHOTS_DIR, fname)
        if os.path.exists(img_p):
            story.append(RLImage(img_p, width=printable_w, height=printable_w * 0.58))
            story.append(Paragraph(cap, caption_style))
            story.append(Paragraph(f"<b>Feature:</b> {desc}", body_style))
            story.append(Spacer(1, 10))

    story.append(PageBreak())

    # =========================================================================
    # 8. REFERENCES & BIBLIOGRAPHY
    # =========================================================================
    story.append(Paragraph("8. REFERENCES & BIBLIOGRAPHY", h1_style))
    refs = [
        "[1] S. Tiangolo, 'FastAPI: Modern Web Framework for Building APIs with Python 3.8+', 2024. https://fastapi.tiangolo.com/",
        "[2] K. Banker et al., MongoDB in Action: Covers MongoDB version 3.0+, 2nd ed. Manning Publications, 2016.",
        "[3] L. Breiman, 'Random Forests', Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.",
        "[4] S. J. Taylor and B. Letham, 'Forecasting at scale', The American Statistician, vol. 72, no. 1, pp. 37–45, 2018.",
        "[5] C. Hutto and E. Gilbert, 'VADER: A Parsimonious Rule-Based Model for Sentiment Analysis', ICWSM-14, 2014.",
        "[6] Meta Open Source, 'React 18: A JavaScript library for building user interfaces', 2024. https://react.dev/",
        "[7] Faculty of Computer Applications & IT (FCAIT), GLS University, 'Capstone Project – II Guidelines (222301907)', Ahmedabad, Academic Year 2026–2027.",
        "[8] G. Bradski and A. Kaehler, Learning OpenCV: Computer Vision with the OpenCV Library, O'Reilly Media, 2008.",
        "[9] A. Solem et al., 'Celery: Distributed Task Queue', Celery Documentation, 2024. https://docs.celeryq.dev/",
        "[10] F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python', JMLR, vol. 12, pp. 2825–2830, 2011.",
    ]
    for r in refs:
        story.append(Paragraph(r, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated Comprehensive PDF with Diagrams & Screenshots: {OUT_PDF}")

if __name__ == "__main__":
    build_comprehensive_pdf()

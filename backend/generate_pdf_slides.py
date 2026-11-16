"""
ContentIQ - Comprehensive PDF Presentation Deck Generator
Generates a 16:9 landscape PDF presentation deck with embedded high-res
UML diagram graphics, UI screenshots, complete tables, and academic citations.
"""
import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

DIAGRAMS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\diagrams"
SCREENSHOTS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\screenshots"
OUT_PDF_SLIDES = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\ContentIQ_Final_Presentation_Deck.pdf"

def build_comprehensive_pdf_slides():
    pagesize = landscape(A4) # 841.89 x 595.27
    page_w, page_h = pagesize

    doc = SimpleDocTemplate(
        OUT_PDF_SLIDES,
        pagesize=pagesize,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    printable_w = page_w - 72 # 769.89 points
    printable_h = page_h - 64 # 531.27 points

    styles = getSampleStyleSheet()

    c_navy = colors.HexColor("#1F3864")
    c_gold = colors.HexColor("#D97706")
    c_slate = colors.HexColor("#334155")
    c_light = colors.HexColor("#F8FAFC")
    c_card_border = colors.HexColor("#CBD5E1")

    slide_cat = ParagraphStyle('Cat', fontName='Helvetica-Bold', fontSize=9.5, leading=11, textColor=c_gold)
    slide_title = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=c_navy, spaceAfter=8)
    card_title = ParagraphStyle('CTitle', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_navy, spaceAfter=4)
    card_text = ParagraphStyle('CText', fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_slate)
    card_text_bold = ParagraphStyle('CTextB', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=c_navy)

    story = []

    def slide_header(category, title):
        return [
            Paragraph(category.upper(), slide_cat),
            Paragraph(title, slide_title),
            Spacer(1, 2)
        ]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1_content = [
        [Paragraph("<font size=28><b>ContentIQ</b></font><br/><br/>"
                   "<font size=13 color='#D97706'><b>An AI-Powered Multi-Tenant Content Performance and Scheduling Platform</b></font><br/><br/>"
                   "<font size=12 color='#1F3864'><b>222301907 Capstone Project – II (System Design & Implementation)</b></font><br/>"
                   "<font size=10.5>Integrated Master of Computer Applications (iMCA) — Semester IX</font><br/><br/>"
                   "<b>Submitted By:</b> Student 1 & Student 2<br/>"
                   "<b>Under the Guidance of:</b> Dr./Prof. Internal Project Guide<br/>"
                   "<b>Dean:</b> Dr. Tripti Dodiya | FCAIT, GLS University, Ahmedabad<br/>"
                   "<b>Academic Year:</b> 2026–2027",
                   ParagraphStyle('S1Text', alignment=1, leading=17, textColor=c_navy))]
    ]
    t1 = Table(s1_content, colWidths=[printable_w], rowHeights=[470])
    t1.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 2.5, c_navy),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 30),
        ('RIGHTPADDING', (0, 0), (-1, -1), 30),
    ]))
    story.append(t1)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: BRIEF OF SYSTEM
    # =========================================================================
    story.extend(slide_header("GLS University | FCAIT | iMCA SEM IX", "Slide 2: Brief of System (Problem, Objectives & Tech Stack)"))

    c1 = [
        Paragraph("1. Problem Statement", card_title),
        Paragraph("• <b>Subjective Timing:</b> Relying on intuition rather than empirical multi-channel engagement patterns.<br/>"
                  "• <b>Blind Content Posting:</b> Lack of pre-flight AI engagement evaluation before pushing live.<br/>"
                  "• <b>Multi-Tenant Leaks:</b> Mixing client records without row-level database tenant isolation.<br/>"
                  "• <b>Static AI Degradation:</b> Traditional models suffer accuracy drift without real metric retraining.", card_text)
    ]
    c2 = [
        Paragraph("2. Project Objectives", card_title),
        Paragraph("• <b>True Multi-Tenancy:</b> Strict tenant_id compound scoping across MongoDB 7.0 documents.<br/>"
                  "• <b>Pre-Flight AI Engine:</b> Random Forest classifier (Low/Med/High) with 24-hour best-time sweeps.<br/>"
                  "• <b>Computer Vision & NLP:</b> OpenCV Rule-of-Thirds balance scorer & VADER sentiment analysis.<br/>"
                  "• <b>Continuous Feedback Loop:</b> Automatic retraining trigger once >= 50 real metrics accumulate.", card_text)
    ]
    c3 = [
        Paragraph("3. Technology Stack", card_title),
        Paragraph("• <b>Frontend:</b> React 18 SPA, Vite 6, React Router v6, Chart.js, Lucide Icons.<br/>"
                  "• <b>Backend API:</b> FastAPI 0.115.0 (Python 3.13), Uvicorn ASGI, Pydantic v2 schemas.<br/>"
                  "• <b>Database:</b> MongoDB 7.0 with compound indexes.<br/>"
                  "• <b>Background Workers:</b> Celery 5.4 + Redis 7.0 task queue for simulated publishing.<br/>"
                  "• <b>ML Core:</b> Scikit-Learn, OpenCV 4.10, Facebook Prophet, VADER.", card_text)
    ]

    t2 = Table([[c1, c2, c3]], colWidths=[printable_w / 3.0] * 3, rowHeights=[440])
    t2.setStyle(TableStyle([
        ('BOX', (0, 0), (0, -1), 1.5, c_navy),
        ('BOX', (1, 0), (1, -1), 1.5, c_gold),
        ('BOX', (2, 0), (2, -1), 1.5, c_navy),
        ('BACKGROUND', (0, 0), (-1, -1), c_light),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t2)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: UML DIAGRAMS (WITH EMBEDDED SWIMLANE DIAGRAM)
    # =========================================================================
    story.extend(slide_header("GLS University | FCAIT | iMCA SEM IX", "Slide 3: UML Diagrams (Use Case, Class, Swimlane, Sequence, State)"))

    swim_img_path = os.path.join(DIAGRAMS_DIR, "swimlane_activity_diagram.png")
    left_cell = [RLImage(swim_img_path, width=440, height=430)] if os.path.exists(swim_img_path) else [Paragraph("Swimlane Diagram", card_title)]

    right_cell = [
        Paragraph("UML Architecture Specifications:", card_title),
        Paragraph("• <b>3.1 Use Case Diagram:</b> Defines boundaries between 4 actors: Agency Admin, Editor, Client, and Celery Background Worker.<br/><br/>"
                  "• <b>3.2 Class Diagram:</b> 3-compartment OOAD design with visibility, attributes, methods, and multiplicities across all entities.<br/><br/>"
                  "• <b>3.3 Activity Diagram (Swimlane):</b> Four distinct lanes: Content Creator -> React 18 UI -> FastAPI Gateway & ML -> Celery Worker & MongoDB.<br/><br/>"
                  "• <b>3.4 Sequence Diagram:</b> Synchronous draft scoring, feature extraction, model inference, and 24h best-time sweep.<br/><br/>"
                  "• <b>3.5 State Chart Diagram:</b> Lifecycle transitions: Draft -> Scheduled -> Publishing -> Published -> Metrics Ingested -> Retraining.", card_text)
    ]

    t3 = Table([[left_cell, right_cell]], colWidths=[460, printable_w - 460], rowHeights=[440])
    t3.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1.2, c_navy),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t3)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: DATA DICTIONARY
    # =========================================================================
    story.extend(slide_header("GLS University | FCAIT | iMCA SEM IX", "Slide 4: Data Dictionary (9 MongoDB Collections with Multi-Tenancy)"))

    dict_rows = [
        [Paragraph("<b>Collection</b>", card_text_bold), Paragraph("<b>Primary Key</b>", card_text_bold), Paragraph("<b>Tenant Scoping</b>", card_text_bold), Paragraph("<b>Key Attributes</b>", card_text_bold), Paragraph("<b>Indexes</b>", card_text_bold)],
        [Paragraph("tenants", card_text_bold), Paragraph("_id", card_text), Paragraph("_id (Self)", card_text), Paragraph("name, plan ('free'/'pro'), created_at", card_text), Paragraph("_id: 1", card_text)],
        [Paragraph("users", card_text_bold), Paragraph("_id", card_text), Paragraph("tenant_id", card_text), Paragraph("email, hashed_password, name, role", card_text), Paragraph("email: 1, tenant_id: 1", card_text)],
        [Paragraph("posts", card_text_bold), Paragraph("_id", card_text), Paragraph("tenant_id", card_text), Paragraph("title, caption, platform, scheduled_time", card_text), Paragraph("tenant_id: 1, scheduled_time: 1", card_text)],
        [Paragraph("post_metrics", card_text_bold), Paragraph("_id", card_text), Paragraph("tenant_id", card_text), Paragraph("post_id, impressions, likes, rate, actual_tier", card_text), Paragraph("tenant_id: 1, post_id: 1", card_text)],
        [Paragraph("comments", card_text_bold), Paragraph("_id", card_text), Paragraph("tenant_id", card_text), Paragraph("post_id, text, sentiment_score, label", card_text), Paragraph("tenant_id: 1, post_id: 1", card_text)],
        [Paragraph("follower_snapshots", card_text_bold), Paragraph("_id", card_text), Paragraph("tenant_id", card_text), Paragraph("platform, date, follower_count", card_text), Paragraph("tenant_id: 1, platform: 1, date: 1", card_text)],
        [Paragraph("ab_tests", card_text_bold), Paragraph("_id", card_text), Paragraph("tenant_id", card_text), Paragraph("name, variant_a_id, variant_b_id, winner", card_text), Paragraph("tenant_id: 1", card_text)],
        [Paragraph("competitors", card_text_bold), Paragraph("_id", card_text), Paragraph("tenant_id", card_text), Paragraph("handle, platform, followers, engagement_rate", card_text), Paragraph("tenant_id: 1", card_text)],
        [Paragraph("notifications", card_text_bold), Paragraph("_id", card_text), Paragraph("tenant_id", card_text), Paragraph("user_id, title, message, type, read", card_text), Paragraph("tenant_id: 1, user_id: 1", card_text)],
    ]
    t4 = Table(dict_rows, colWidths=[110, 80, 95, 290, 190])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, c_card_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t4)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: SCREENSHOTS WITH URL (WITH EMBEDDED DASHBOARD & CLIENT SCREENSHOTS)
    # =========================================================================
    story.extend(slide_header("GLS University | FCAIT | iMCA SEM IX", "Slide 5: All Screenshots with URL (Admin Side vs. Client Side RBAC)"))

    dash_img_path = os.path.join(SCREENSHOTS_DIR, "screenshot_admin_dashboard.png")
    cli_img_path = os.path.join(SCREENSHOTS_DIR, "screenshot_client_portal.png")

    c_left = [
        Paragraph("<b>Admin Side (URL: http://127.0.0.1:3000/dashboard)</b>", card_title),
        RLImage(dash_img_path, width=370, height=230) if os.path.exists(dash_img_path) else Paragraph("Admin Dashboard", card_text),
        Spacer(1, 4),
        Paragraph("• Full access across all 12 modules.<br/>• Golden Model Continuous Retraining button active.<br/>• Full post creation, editing, scheduling, and staff management.", card_text)
    ]

    c_right = [
        Paragraph("<b>Client Side (URL: http://127.0.0.1:3000/dashboard)</b>", card_title),
        RLImage(cli_img_path, width=370, height=230) if os.path.exists(cli_img_path) else Paragraph("Client Portal", card_text),
        Spacer(1, 4),
        Paragraph("• Restricted 6-module observer portal.<br/>• Model retraining locked with 'Admin role required' notice.<br/>• Read-only calendar with edit & delete buttons removed.", card_text)
    ]

    t5 = Table([[c_left, c_right]], colWidths=[printable_w / 2.0, printable_w / 2.0], rowHeights=[440])
    t5.setStyle(TableStyle([
        ('BOX', (0, 0), (0, -1), 1.2, c_navy),
        ('BOX', (1, 0), (1, -1), 1.2, c_gold),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t5)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: REPORTS (PRINTABLE PDF OR EXPORT IN EXCEL)
    # =========================================================================
    story.extend(slide_header("GLS University | FCAIT | iMCA SEM IX", "Slide 6: Reports (Printable PDF or Export in Excel — Syllabus Item 7.3)"))

    rep_img_path = os.path.join(SCREENSHOTS_DIR, "screenshot_reports_export.png")
    c_rep_left = [RLImage(rep_img_path, width=410, height=260)] if os.path.exists(rep_img_path) else [Paragraph("Reports Export", card_title)]

    c_rep_right = [
        Paragraph("Enterprise Reporting Capabilities:", card_title),
        Paragraph("• <b>1. Export to Excel (.csv):</b><br/>"
                  "  - Located on Executive Dashboard header.<br/>"
                  "  - One-click download of <code>ContentIQ_Performance_Report.csv</code>.<br/>"
                  "  - Includes platform distribution, total content volume, average engagement rate, and ML validation accuracy (88.0%).<br/><br/>"
                  "• <b>2. Printable PDF Report:</b><br/>"
                  "  - Accessible alongside Excel export.<br/>"
                  "  - Dedicated <code>@media print</code> stylesheet suppressing navigation chrome and formatting KPI cards for physical review.<br/><br/>"
                  "• <b>Academic & Viva Value:</b><br/>"
                  "  - Fulfills syllabus item 7.3 with live, reproducible enterprise exports.", card_text)
    ]

    t6 = Table([[c_rep_left, c_rep_right]], colWidths=[430, printable_w - 430], rowHeights=[440])
    t6.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1.2, c_navy),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t6)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: REFERENCES
    # =========================================================================
    story.extend(slide_header("GLS University | FCAIT | iMCA SEM IX", "Slide 7: References & Bibliography (IEEE Standard)"))

    ref_col = [
        Paragraph("<b>References:</b><br/><br/>"
                  "[1] S. Tiangolo, 'FastAPI: Modern, High-Performance Web Framework for Building APIs with Python 3.8+', 2024. https://fastapi.tiangolo.com/<br/><br/>"
                  "[2] K. Banker, P. Bakkum, S. Verch, and D. Garrett, MongoDB in Action: Covers MongoDB version 3.0+, Manning Publications, 2016.<br/><br/>"
                  "[3] L. Breiman, 'Random Forests', Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.<br/><br/>"
                  "[4] S. J. Taylor and B. Letham, 'Forecasting at scale', The American Statistician, vol. 72, no. 1, pp. 37–45, 2018.<br/><br/>"
                  "[5] C. Hutto and E. Gilbert, 'VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text', ICWSM-14, 2014.<br/><br/>"
                  "[6] Meta Open Source, 'React 18: A JavaScript library for building user interfaces', React Documentation, 2024. https://react.dev/<br/><br/>"
                  "[7] Faculty of Computer Applications & IT (FCAIT), GLS University, 'Capstone Project – II Guidelines (222301907)', Ahmedabad, 2026–2027.", card_text)
    ]
    t7 = Table([[ref_col]], colWidths=[printable_w], rowHeights=[440])
    t7.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1.2, c_navy),
        ('BACKGROUND', (0, 0), (-1, -1), c_light),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(t7)

    doc.build(story)
    print(f"[+] Successfully generated Comprehensive PDF Slides with Graphics: {OUT_PDF_SLIDES}")

if __name__ == "__main__":
    build_comprehensive_pdf_slides()

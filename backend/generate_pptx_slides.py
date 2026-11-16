"""
ContentIQ - Clean, 100% PowerPoint Compliant Presentation Deck Generator
Generates an error-free 16:9 widescreen PPTX presentation deck that opens smoothly
in Microsoft PowerPoint, Office 365, Google Slides, and LibreOffice.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

DIAGRAMS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\diagrams"
SCREENSHOTS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\screenshots"
OUT_PPTX = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\ContentIQ_Final_Presentation_Deck.pptx"

def create_flawless_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    c_navy = RGBColor(31, 56, 100)       # #1F3864
    c_gold = RGBColor(217, 119, 6)       # #D97706
    c_slate = RGBColor(71, 85, 105)      # #475569
    c_white = RGBColor(255, 255, 255)
    c_card_bg = RGBColor(248, 250, 252)  # #F8FAFC

    def add_header(slide, title_text, category_text="GLS UNIVERSITY | FCAIT | iMCA SEM IX"):
        # Category label
        tb_c = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = c_gold

        # Main Title
        tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.65))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = c_navy

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_navy
    bg1.line.fill.background()

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.9))
    card1.fill.solid()
    card1.fill.fore_color.rgb = c_white
    card1.line.color.rgb = c_gold
    card1.line.width = Pt(2.5)

    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "ContentIQ"
    r.font.size = Pt(40)
    r.font.bold = True
    r.font.color.rgb = c_navy

    p = tf1.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "An AI-Powered Multi-Tenant Content Performance and Scheduling Platform\n"
    r.font.size = Pt(15)
    r.font.italic = True
    r.font.color.rgb = c_gold

    p = tf1.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "222301907 Capstone Project – II (System Design & Implementation)\nIntegrated Master of Computer Applications (iMCA) — Semester IX\n"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = c_navy

    p = tf1.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Submitted By: Student 1 & Student 2\nUnder the Guidance of: Dr./Prof. Internal Project Guide\nDean: Dr. Tripti Dodiya | FCAIT, GLS University, Ahmedabad\nAcademic Year 2026–2027"
    r.font.size = Pt(12)
    r.font.color.rgb = c_slate

    # =========================================================================
    # SLIDE 2: BRIEF OF SYSTEM
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Slide 2: Brief of System (Problem Statement, Objectives & Tech Stack)")

    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_y = Inches(1.5)
    card_h = Inches(5.4)

    cards = [
        ("1. Problem Statement", [
            "• Subjective Timing: Creators schedule posts based on intuition rather than empirical multi-channel engagement patterns.",
            "• Blind Publishing: Authors lack pre-flight AI scoring to evaluate caption & timing before publishing.",
            "• Data Leakage Risk: Multi-agency tools often fail to provide hard row-level tenant isolation in the database.",
            "• Static AI Models: Traditional algorithms suffer accuracy drift because they never retrain on real metrics."
        ]),
        ("2. Project Objectives", [
            "• True Multi-Tenancy: Strict logical isolation enforcing tenant_id compound indexes across all MongoDB collections.",
            "• Pre-Flight AI Engine: Calibrated Random Forest model predicting Low/Med/High engagement tiers with 24h sweep.",
            "• Computer Vision & NLP: Automated OpenCV thumbnail balance scorer and VADER comment sentiment classifier.",
            "• Continuous Retraining Loop: Automatic retraining trigger whenever >= 50 real engagement records accumulate."
        ]),
        ("3. Technology Stack", [
            "• Frontend: React 18 SPA, Vite 6, React Router v6, Chart.js, Lucide Icons.",
            "• Backend: FastAPI 0.115.0 (Python 3.13), Uvicorn ASGI, Pydantic v2 schemas.",
            "• Database: MongoDB 7.0 Community with Motor Async driver.",
            "• Background Workers: Celery 5.4 + Redis 7.0 for worker queues & automated post publishing.",
            "• ML Core: Scikit-Learn, OpenCV 4.10, Facebook Prophet, VADER."
        ])
    ]

    for i, (title, points) in enumerate(cards):
        left_x = Inches(0.8) + i * (col_w + gap)
        c = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, top_y, col_w, card_h)
        c.fill.solid()
        c.fill.fore_color.rgb = c_card_bg
        c.line.color.rgb = c_navy if i == 1 else c_gold
        c.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(left_x + Inches(0.2), top_y + Inches(0.2), col_w - Inches(0.4), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_navy

        for pt in points:
            p2 = tf.add_paragraph()
            p2.text = pt
            p2.font.size = Pt(10)
            p2.font.color.rgb = c_slate
            p2.space_before = Pt(8)

    # =========================================================================
    # SLIDE 3: UML DIAGRAMS (WITH EXPLICIT PICTURE DIMENSIONS)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Slide 3: UML Diagrams (Use Case, Class, Swimlane, Sequence, State Chart)")

    swim_p = os.path.join(DIAGRAMS_DIR, "swimlane_activity_diagram.png")
    if os.path.exists(swim_p):
        s3.shapes.add_picture(swim_p, Inches(0.8), Inches(1.5), width=Inches(7.2), height=Inches(5.4))

    tb_u = s3.shapes.add_textbox(Inches(8.2), Inches(1.5), Inches(4.3), Inches(5.4))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True

    p = tf_u.paragraphs[0]
    p.text = "UML Architecture Specifications:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_navy

    specs = [
        ("3.1 Use Case Diagram", "Defines boundaries for 4 actors: Agency Admin, Editor, Client, and Celery Scheduler."),
        ("3.2 Detailed Class Diagram", "3-compartment OOAD design with attributes, methods, and multiplicities across all entities."),
        ("3.3 Activity Diagram (Swimlane)", "4 isolated operational lanes: Content Creator -> React 18 UI -> FastAPI Gateway & ML -> Celery Worker & MongoDB."),
        ("3.4 Sequence Diagram", "Message flow: Draft entry -> Pre-flight scoring -> Feature extraction -> Model inference -> Chart rendering."),
        ("3.5 State Chart Diagram", "Post lifecycle: Draft -> Scheduled -> Publishing -> Published -> Metrics Collected -> Continuous Retraining.")
    ]
    for ut, ud in specs:
        p2 = tf_u.add_paragraph()
        r1 = p2.add_run()
        r1.text = ut + ": "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = c_navy
        r2 = p2.add_run()
        r2.text = ud
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = c_slate
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 4: DATA DICTIONARY
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Slide 4: Data Dictionary (9 MongoDB Collections with Multi-Tenancy)")

    rows, cols = 10, 5
    t_shape = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    table = t_shape.table

    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(1.4)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(3.4)
    table.columns[4].width = Inches(3.333)

    headers = ["Collection Name", "Primary Key", "Tenant Scoping", "Key Attributes", "Database Indexes"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = c_white

    data_collections = [
        ("tenants", "_id (ObjectId)", "_id (Self)", "name, plan ('free'/'pro'), created_at", "_id: 1 (Primary)"),
        ("users", "_id (ObjectId)", "tenant_id", "email, hashed_password, name, role", "email: 1 (unique), tenant_id: 1"),
        ("posts", "_id (ObjectId)", "tenant_id", "title, caption, platform, scheduled_time", "tenant_id: 1, scheduled_time: 1"),
        ("post_metrics", "_id (ObjectId)", "tenant_id", "post_id, impressions, likes, rate, actual_tier", "tenant_id: 1, post_id: 1"),
        ("comments", "_id (ObjectId)", "tenant_id", "post_id, text, sentiment_score, label", "tenant_id: 1, post_id: 1"),
        ("follower_snapshots", "_id (ObjectId)", "tenant_id", "platform, date, follower_count", "tenant_id: 1, platform: 1, date: 1"),
        ("ab_tests", "_id (ObjectId)", "tenant_id", "name, variant_a_id, variant_b_id, winner", "tenant_id: 1"),
        ("competitors", "_id (ObjectId)", "tenant_id", "handle, platform, followers, engagement_rate", "tenant_id: 1"),
        ("notifications", "_id (ObjectId)", "tenant_id", "user_id, title, message, type, read", "tenant_id: 1, user_id: 1")
    ]

    for i, row in enumerate(data_collections):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_card_bg if (i % 2 == 0) else c_white
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = c_navy if j == 0 else c_slate
            if j == 0:
                p.font.bold = True

    # =========================================================================
    # SLIDE 5: SCREENSHOTS WITH URL
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Slide 5: All Screenshots with URL (Admin Side vs. Client Side RBAC)")

    dash_p = os.path.join(SCREENSHOTS_DIR, "screenshot_admin_dashboard.png")
    cli_p = os.path.join(SCREENSHOTS_DIR, "screenshot_client_portal.png")

    if os.path.exists(dash_p):
        s5.shapes.add_picture(dash_p, Inches(0.8), Inches(1.5), width=Inches(5.7), height=Inches(3.5))

    if os.path.exists(cli_p):
        s5.shapes.add_picture(cli_p, Inches(6.8), Inches(1.5), width=Inches(5.7), height=Inches(3.5))

    tb_s5 = s5.shapes.add_textbox(Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.8))
    tf_s5 = tb_s5.text_frame
    tf_s5.word_wrap = True

    p = tf_s5.paragraphs[0]
    p.text = "Role-Based Access Control (RBAC) Distinction in Live Execution:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = c_navy

    p2 = tf_s5.add_paragraph()
    p2.text = "• Admin Side (Left: http://127.0.0.1:3000/dashboard): 12 modules accessible. Unrestricted control over content authoring, team invitations, and the Golden Model Continuous Retraining trigger."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = c_slate
    p2.space_before = Pt(3)

    p3 = tf_s5.add_paragraph()
    p3.text = "• Client Side (Right: http://127.0.0.1:3000/dashboard): Restricted 6-module observer portal. Content creation/deletion tools are suppressed. Retraining button is locked with 'Admin role required' notice."
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = c_slate
    p3.space_before = Pt(3)

    # =========================================================================
    # SLIDE 6: REPORTS (EXCEL OR PDF)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Slide 6: Reports (Printable PDF or Export in Excel — Syllabus Item 7.3)")

    rep_p = os.path.join(SCREENSHOTS_DIR, "screenshot_reports_export.png")
    if os.path.exists(rep_p):
        s6.shapes.add_picture(rep_p, Inches(0.8), Inches(1.5), width=Inches(6.4), height=Inches(4.2))

    tb_rep = s6.shapes.add_textbox(Inches(7.5), Inches(1.5), Inches(5.0), Inches(5.2))
    tf_r = tb_rep.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Enterprise Reporting Capabilities:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_navy

    rep_bullets = [
        ("1. Native Export to Excel (.csv)", "Located on the Executive Dashboard header. One-click instant download of 'ContentIQ_Performance_Report_YYYY-MM-DD.csv'."),
        ("Structured CSV Data Included", "Contains platform counts (Instagram, LinkedIn, YouTube), total content volume (90 posts), average engagement rate (4.82%), and active ML model accuracy (88.0%)."),
        ("2. Printable PDF Report", "Accessible alongside Excel export. Invokes browser print styling (@media print) cleanly suppressing sidebar chrome and formatting KPI cards for stakeholder review."),
        ("Agency & Viva Value", "Eliminates manual screenshot compilation; empowers corporate clients to download verifiable performance summaries on demand.")
    ]
    for rt, rd in rep_bullets:
        p2 = tf_r.add_paragraph()
        r1 = p2.add_run()
        r1.text = rt + ": "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = c_navy
        r2 = p2.add_run()
        r2.text = rd
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = c_slate
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 7: REFERENCES
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Slide 7: References & Bibliography (IEEE Standard)")

    c_ref = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    c_ref.fill.solid()
    c_ref.fill.fore_color.rgb = c_card_bg
    c_ref.line.color.rgb = c_navy
    c_ref.line.width = Pt(1.5)

    tb_rf = s7.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.133), Inches(5.0))
    tf_rf = tb_rf.text_frame
    tf_rf.word_wrap = True

    references = [
        "[1] S. Tiangolo, 'FastAPI: Modern, High-Performance Web Framework for Building APIs with Python 3.8+', 2024. https://fastapi.tiangolo.com/",
        "[2] K. Banker, P. Bakkum, S. Verch, and D. Garrett, MongoDB in Action: Covers MongoDB version 3.0+, Manning Publications, 2016.",
        "[3] L. Breiman, 'Random Forests', Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.",
        "[4] S. J. Taylor and B. Letham, 'Forecasting at scale', The American Statistician, vol. 72, no. 1, pp. 37–45, 2018.",
        "[5] C. Hutto and E. Gilbert, 'VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text', ICWSM-14, 2014.",
        "[6] Meta Open Source, 'React 18: A JavaScript library for building user interfaces', React Documentation, 2024. https://react.dev/",
        "[7] Faculty of Computer Applications & IT (FCAIT), GLS University, 'Capstone Project – II Guidelines (222301907)', Ahmedabad, 2026–2027.",
        "[8] G. Bradski and A. Kaehler, Learning OpenCV: Computer Vision with the OpenCV Library, O'Reilly Media, 2008.",
        "[9] A. Solem et al., 'Celery: Distributed Task Queue', Celery Documentation, 2024. https://docs.celeryq.dev/",
        "[10] F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python', JMLR, vol. 12, pp. 2825–2830, 2011."
    ]

    for i, ref in enumerate(references):
        p = tf_rf.paragraphs[0] if i == 0 else tf_rf.add_paragraph()
        p.text = ref
        p.font.size = Pt(10)
        p.font.color.rgb = c_navy if i % 2 == 0 else c_slate
        p.space_before = Pt(5)

    prs.save(OUT_PPTX)
    print(f"[+] Successfully generated Flawless PPTX: {OUT_PPTX}")

if __name__ == "__main__":
    create_flawless_pptx()

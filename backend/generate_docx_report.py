"""
ContentIQ - Comprehensive DOCX Report Generator
Generates a complete, publication-quality Microsoft Word document
with embedded high-res UML diagrams, UI screenshots, complete 9-collection data dictionary,
and full academic documentation strictly matching GLS University FCAIT guidelines.
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DIAGRAMS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\diagrams"
SCREENSHOTS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\screenshots"
OUT_DOCX = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\ContentIQ_Final_Documentation_Report.docx"

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_full_docx():
    doc = Document()

    # Set 0.9 inch margins
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # =========================================================================
    # 1. COVER PAGE (Bordered Box Format)
    # =========================================================================
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.7)
    set_cell_margins(cell, top=350, bottom=350, left=350, right=350)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="double" w:sz="18" w:space="0" w:color="1F3864"/>'
        f'<w:left w:val="double" w:sz="18" w:space="0" w:color="1F3864"/>'
        f'<w:bottom w:val="double" w:sz="18" w:space="0" w:color="1F3864"/>'
        f'<w:right w:val="double" w:sz="18" w:space="0" w:color="1F3864"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    cp = cell.paragraphs[0]
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cp.add_run("ContentIQ\n")
    r.font.name = 'Georgia'
    r.font.size = Pt(30)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 56, 100)

    r_sub = cp.add_run("An AI-Powered Multi-Tenant Content Performance and Scheduling Platform\n\n\n")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.add_run("Project Report\nSubmitted for the subject of\n").font.size = Pt(12)
    r2_code = p2.add_run("222301907 Capstone Project – II\n")
    r2_code.font.size = Pt(14)
    r2_code.font.bold = True
    r2_code.font.color.rgb = RGBColor(31, 56, 100)
    r2_prog = p2.add_run("Integrated Master of Computer Applications (iMCA)\n")
    r2_prog.font.size = Pt(13)
    r2_prog.font.bold = True
    p2.add_run("Semester IX\n\n\n").font.size = Pt(12)

    p3 = cell.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.add_run("Submitted By:\n").font.bold = True
    p3.add_run("Student 1: [Your Full Name] (Enrollment No: ____________________)\nStudent 2: [Partner Full Name] (Enrollment No: ____________________)\n\n\n")

    p4 = cell.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p4.add_run("Under the Guidance of:\n").font.bold = True
    r4_g = p4.add_run("Dr./Prof. Name of Internal Guide\nFCAIT, GLS University\n\n\n")
    r4_g.font.bold = True

    p5 = cell.add_paragraph()
    p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r5 = p5.add_run("Faculty of Computer Applications & IT (FCAIT)\niMCA Programme, Ahmedabad\nGLS UNIVERSITY\n\nAcademic Year 2026–2027")
    r5.font.size = Pt(12)
    r5.font.bold = True
    r5.font.color.rgb = RGBColor(31, 56, 100)

    doc.add_page_break()

    # =========================================================================
    # 2. COLLEGE CERTIFICATE
    # =========================================================================
    cert_table = doc.add_table(rows=1, cols=1)
    cert_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = cert_table.cell(0, 0)
    c_cell.width = Inches(6.7)
    set_cell_margins(c_cell, top=350, bottom=350, left=350, right=350)
    c_tcPr = c_cell._tc.get_or_add_tcPr()
    c_borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="16" w:space="0" w:color="1F3864"/>'
        f'<w:left w:val="single" w:sz="16" w:space="0" w:color="1F3864"/>'
        f'<w:bottom w:val="single" w:sz="16" w:space="0" w:color="1F3864"/>'
        f'<w:right w:val="single" w:sz="16" w:space="0" w:color="1F3864"/>'
        f'</w:tcBorders>'
    )
    c_tcPr.append(c_borders)

    cp1 = c_cell.paragraphs[0]
    cp1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr1 = cp1.add_run("GLS UNIVERSITY\nFaculty of Computer Applications & IT\niMCA Programme\nAhmedabad\n\n")
    cr1.font.size = Pt(14)
    cr1.font.bold = True
    cr1.font.color.rgb = RGBColor(31, 56, 100)

    cr_title = cp1.add_run("CERTIFICATE\n\n")
    cr_title.font.size = Pt(16)
    cr_title.font.bold = True
    cr_title.font.underline = True

    cp2 = c_cell.add_paragraph()
    cp2.paragraph_format.line_spacing = 1.4
    cp2.add_run(
        "This is to certify that the following students of Semester IX Integrated Master of Computer Applications (iMCA) Programme, "
        "Faculty of Computer Applications & IT (FCAIT), GLS University, Ahmedabad, have successfully completed the subject project titled\n\n"
    )

    cp_proj = c_cell.add_paragraph()
    cp_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr_proj = cp_proj.add_run("“ContentIQ: An AI-Powered Multi-Tenant Content Performance and Scheduling Platform for Social Media Creators and Agencies”\n\n")
    cr_proj.font.size = Pt(13)
    cr_proj.font.bold = True
    cr_proj.font.color.rgb = RGBColor(31, 56, 100)

    cp3 = c_cell.add_paragraph()
    cp3.paragraph_format.line_spacing = 1.4
    cp3.add_run(
        "for the course 222301907 Capstone Project – II - System Design and Implementation during the Academic Year 2026–2027.\n\n\n"
    )

    cp_date = c_cell.add_paragraph()
    cp_date.add_run("Date of Submission: 23rd October 2026\n\n\n\n").font.size = Pt(11)

    sig_table = c_cell.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_cell_left = sig_table.cell(0, 0)
    sig_cell_right = sig_table.cell(0, 1)
    sig_cell_left.width = Inches(3.2)
    sig_cell_right.width = Inches(3.2)

    sp_l = sig_cell_left.paragraphs[0]
    sr_l = sp_l.add_run("Dr./Prof. Name of Internal Guide\nProject Guide\nFCAIT, GLS University")
    sr_l.font.bold = True

    sp_r = sig_cell_right.paragraphs[0]
    sp_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    sr_r = sp_r.add_run("Dr. Tripti Dodiya\nDean\nFCAIT, GLS University")
    sr_r.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # 3. INDEX
    # =========================================================================
    h3 = doc.add_heading("3. INDEX", level=1)
    h3.runs[0].font.color.rgb = RGBColor(31, 56, 100)

    index_table = doc.add_table(rows=1, cols=3)
    index_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = index_table.rows[0].cells
    hdr[0].text = "Section"
    hdr[1].text = "Topic / Chapter Name"
    hdr[2].text = "Page No."
    for c in hdr:
        set_cell_background(c, "1F3864")
        p = c.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    index_rows = [
        ("1", "Cover Page", "1"),
        ("2", "College Certificate", "2"),
        ("3", "Index", "3"),
        ("4", "Brief of System (Problem Statement, Scope, Objectives, Tech Stack, Specs)", "4"),
        ("5", "UML Diagrams (Use Case, Class, Activity Swimlane, Sequence, State Chart)", "7"),
        ("6", "Data Dictionary (Exhaustive Specifications for 9 MongoDB Collections)", "14"),
        ("7", "All Screenshots with URL (Admin Side, Client Side, Excel/PDF Reports)", "20"),
        ("8", "References & Bibliography (IEEE Standards)", "27"),
    ]

    for r_idx, r_name, r_page in index_rows:
        row = index_table.add_row().cells
        row[0].text = r_idx
        row[1].text = r_name
        row[2].text = r_page
        for c in row:
            set_cell_margins(c, top=70, bottom=70, left=90, right=90)

    doc.add_page_break()

    # =========================================================================
    # 4. BRIEF OF SYSTEM
    # =========================================================================
    h4 = doc.add_heading("4. BRIEF OF SYSTEM", level=1)
    h4.runs[0].font.color.rgb = RGBColor(31, 56, 100)

    doc.add_heading("4.1 Introduction & Problem Statement", level=2)
    doc.add_paragraph(
        "Digital content creators and digital marketing agencies manage social presence across multiple platforms: "
        "Instagram (visual carousels and reels), LinkedIn (B2B thought leadership), and YouTube (long-form video).\n\n"
        "Conventional social management tools like Buffer, Hootsuite, and Later suffer from the critical 'Blind Scheduling' dilemma: "
        "they accept drafts and schedule them at arbitrary user-chosen times. They provide zero pre-publication intelligence "
        "regarding whether a drafted post has engaging copy, optimal hashtag density, positive audience sentiment, or whether posting "
        "at 2:00 PM is vastly superior to 9:00 AM. Furthermore, post-publication metrics are never fed back into an intelligent model to improve future posts.\n\n"
        "ContentIQ is an AI-powered, multi-tenant content performance and scheduling platform. Built with a modern full-stack architecture "
        "(React 18, FastAPI, Motor Async MongoDB, Redis 7, and Celery), ContentIQ embeds machine learning directly into every phase of the content lifecycle."
    )

    doc.add_heading("4.2 System Scope & Objectives", level=2)
    doc.add_paragraph(
        "• Production-Ready Multi-Tenancy: Strictly isolate workspaces using MongoDB tenant-scoped documents and JWT claims.\n"
        "• Pre-Flight Machine Learning Scoring: Deliver real-time Random Forest engagement tier predictions (Low <2%, Medium 2-5%, High >5%) with 24-hour best-time sweeps.\n"
        "• Multi-Modal Computer Vision & NLP: Analyze thumbnail imagery using OpenCV 4.10 (Rule-of-Thirds, contrast, visual balance) and evaluate user comments with VADER sentiment.\n"
        "• Continuous Retraining Feedback Loop: Automatically retrain the golden Random Forest classifier whenever >= 50 real engagement metrics accumulate.\n"
        "• Local Timezone Preservation: Scheduled hours are stored as local ISO strings without UTC conversion, preventing feature drift."
    )

    doc.add_heading("4.3 Technology Stack Justification", level=2)
    ts_table = doc.add_table(rows=1, cols=3)
    ts_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, title in enumerate(["Architecture Layer", "Technology Selection", "Academic & Viva Justification"]):
        c = ts_table.rows[0].cells[i]
        c.text = title
        set_cell_background(c, "1F3864")
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    ts_data = [
        ("Frontend", "React 18, Vite 6, Chart.js", "Component-driven SPA, fast HMR, executive Navy (#1f3864) & Gold theme."),
        ("Backend", "FastAPI 0.115.0, Pydantic v2", "High-throughput asynchronous REST API with automatic OpenAPI Swagger docs."),
        ("Database", "MongoDB 7.0 Community", "Document-oriented schema suited for polymorphic social media posts and comments."),
        ("Cache & Broker", "Redis Server 7.0", "In-memory store providing sub-millisecond caching for dashboards and task queue."),
        ("Async Worker", "Celery 5.4 (--pool=solo)", "Decoupled background scheduler for automated post publishing and notifications."),
        ("Machine Learning", "Scikit-Learn, OpenCV, Prophet, VADER", "Random Forest classification, time-series forecasting, and computer vision aesthetics."),
    ]
    for c1, c2, c3 in ts_data:
        r = ts_table.add_row().cells
        r[0].text = c1
        r[1].text = c2
        r[2].text = c3
        for cell in r:
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    doc.add_page_break()

    # =========================================================================
    # 5. UML DIAGRAMS (WITH EMBEDDED DIAGRAM IMAGES)
    # =========================================================================
    h5 = doc.add_heading("5. UML DIAGRAMS", level=1)
    h5.runs[0].font.color.rgb = RGBColor(31, 56, 100)

    # 5.1 Use Case Diagram
    doc.add_heading("5.1 Use Case Diagram", level=2)
    doc.add_paragraph(
        "The Use Case Diagram defines functional boundaries between four system actors: "
        "Agency Administrator, Content Editor, Client Observer, and the Automated Background Scheduler."
    )
    uc_img = os.path.join(DIAGRAMS_DIR, "use_case_diagram.png")
    if os.path.exists(uc_img):
        doc.add_picture(uc_img, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 5.1: ContentIQ System Use Case Diagram")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # 5.2 Detailed Class Diagram
    doc.add_heading("5.2 Detailed Class Diagram", level=2)
    doc.add_paragraph(
        "Models the Object-Oriented domain entities, attributes with visibility and data types, "
        "member methods, and relationships adhering strictly to OOAD standards."
    )
    cls_img = os.path.join(DIAGRAMS_DIR, "class_diagram.png")
    if os.path.exists(cls_img):
        doc.add_picture(cls_img, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 5.2: ContentIQ Domain Class Diagram with Multiplicities")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # 5.3 Swimlane Activity Diagram
    doc.add_heading("5.3 Activity Diagram (Swimlane)", level=2)
    doc.add_paragraph(
        "Adhering to GLS University's specific Swimlane format, the execution lifecycle is partitioned across "
        "four distinct operational lanes: Content Creator, React 18 Frontend, FastAPI Gateway & ML Engine, "
        "and Background Celery Worker & MongoDB."
    )
    swim_img = os.path.join(DIAGRAMS_DIR, "swimlane_activity_diagram.png")
    if os.path.exists(swim_img):
        doc.add_picture(swim_img, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 5.3: ContentIQ 4-Lane Swimlane Activity Diagram")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # 5.4 Sequence Diagram
    doc.add_heading("5.4 Sequence Diagram (Pre-Flight Prediction & Best-Time Sweep)", level=2)
    doc.add_paragraph(
        "Illustrates message exchanges between Content Creator, PostCompose.jsx UI, FastAPI Gateway, "
        "PredictionService, and the Random Forest Model Artifact."
    )
    seq_img = os.path.join(DIAGRAMS_DIR, "sequence_diagram.png")
    if os.path.exists(seq_img):
        doc.add_picture(seq_img, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 5.4: Pre-Flight AI Prediction & 24h Sweep Sequence Diagram")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # 5.5 State Chart Diagram
    doc.add_heading("5.5 State Chart Diagram (Post Lifecycle)", level=2)
    doc.add_paragraph(
        "Documents state transitions from initial draft creation to scheduled queuing, background publishing, "
        "metric feedback collection, and continuous retraining."
    )
    state_img = os.path.join(DIAGRAMS_DIR, "state_chart_diagram.png")
    if os.path.exists(state_img):
        doc.add_picture(state_img, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 5.5: Post Lifecycle State Chart Diagram")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # =========================================================================
    # 6. DATA DICTIONARY (ALL 9 COLLECTIONS IN FULL)
    # =========================================================================
    h6 = doc.add_heading("6. DATA DICTIONARY", level=1)
    h6.runs[0].font.color.rgb = RGBColor(31, 56, 100)

    doc.add_heading("6.1 Database Architecture & Multi-Tenancy Strategy", level=2)
    doc.add_paragraph(
        "• Database Engine: MongoDB 7.0 Community\n"
        "• Database Name: contentiq\n"
        "• Multi-Tenancy Model: Shared database with logical tenant isolation. Every document contains an indexed tenant_id field."
    )

    collections_data = [
        ("Collection 1: tenants", "Stores agency workspaces and subscription tiers.", [
            ("_id", "ObjectId", "Primary Key", "Unique workspace identifier"),
            ("name", "String", "Required", "Agency Name (e.g., 'Apex Digital Agency')"),
            ("plan", "String", "Enum", "Subscription tier: 'free', 'pro', 'enterprise'"),
            ("created_at", "ISO Datetime", "Required", "Local ISO creation timestamp"),
        ]),
        ("Collection 2: users", "Stores user authentication records and RBAC roles.", [
            ("_id", "ObjectId", "Primary Key", "Unique user identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key reference to tenants._id"),
            ("email", "String", "Unique, Required", "Unique login email address"),
            ("name", "String", "Required", "Full name of staff member"),
            ("hashed_password", "String", "Required", "Bcrypt hashed password (12 salt rounds)"),
            ("role", "String", "Enum", "'admin', 'editor', 'client'"),
            ("created_at", "ISO Datetime", "Required", "Account creation timestamp"),
        ]),
        ("Collection 3: posts", "Stores draft, scheduled, and published social media content.", [
            ("_id", "ObjectId", "Primary Key", "Unique post identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key reference to tenants._id"),
            ("created_by", "String", "Optional", "User ID of post author"),
            ("platform", "String", "Enum", "'instagram', 'linkedin', 'youtube'"),
            ("caption", "String", "Required", "Text caption and content"),
            ("hashtags", "Array[String]", "Required", "List of hashtag strings"),
            ("media_url", "String", "Optional", "URL or local path to cover image"),
            ("scheduled_time", "ISO Datetime", "Indexed", "Scheduled publication local ISO datetime"),
            ("scheduled_hour", "Integer", "Derived", "Integer hour (0-23) without UTC drift"),
            ("status", "String", "Enum", "'draft', 'scheduled', 'published'"),
            ("published_at", "ISO Datetime", "Optional", "Actual publication timestamp"),
        ]),
        ("Collection 4: post_metrics", "Stores ground-truth empirical metrics for continuous retraining.", [
            ("_id", "ObjectId", "Primary Key", "Unique metric identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("post_id", "String", "Foreign Key", "Foreign reference to posts._id"),
            ("likes", "Integer", ">= 0", "Total likes count"),
            ("comments", "Integer", ">= 0", "Total comments count"),
            ("shares", "Integer", ">= 0", "Total shares / retweets"),
            ("reach", "Integer", ">= 0", "Unique viewer reach"),
            ("impressions", "Integer", ">= 0", "Total post views"),
            ("engagement_rate", "Float", "Percentage", "(interactions / reach) * 100"),
            ("tier", "String", "Enum", "'low' (<2%), 'medium' (2-5%), 'high' (>5%)"),
        ]),
        ("Collection 5: follower_snapshots", "Historical follower records for Prophet growth forecasting.", [
            ("_id", "ObjectId", "Primary Key", "Unique snapshot identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("platform", "String", "Enum", "'instagram', 'linkedin', 'youtube'"),
            ("date", "String", "Format YYYY-MM-DD", "Snapshot date"),
            ("follower_count", "Integer", ">= 0", "Total followers on this date"),
        ]),
        ("Collection 6: competitors", "Competitor agencies tracked for benchmarking.", [
            ("_id", "ObjectId", "Primary Key", "Unique competitor identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("handle", "String", "Required", "Competitor handle (e.g. '@PulseMedia')"),
            ("platform", "String", "Enum", "'instagram', 'linkedin', 'youtube'"),
            ("engagement_rate", "Float", "Percentage", "Competitor benchmark engagement rate"),
            ("follower_count", "Integer", "Optional", "Estimated competitor follower count"),
        ]),
        ("Collection 7: comments", "Audience feedback with automated VADER compound polarity scores.", [
            ("_id", "ObjectId", "Primary Key", "Unique comment identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("post_id", "String", "Foreign Key", "Reference to target post"),
            ("text", "String", "Required", "Comment text body"),
            ("author", "String", "Required", "Screen name of commenter"),
            ("sentiment", "String", "Enum", "'positive', 'neutral', 'negative'"),
            ("compound_score", "Float", "Score", "VADER compound polarity (-1.0 to +1.0)"),
        ]),
        ("Collection 8: notifications", "In-app creator notification alerts.", [
            ("_id", "ObjectId", "Primary Key", "Unique alert identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("type", "String", "Enum", "'upcoming_post', 'low_prediction', 'published_confirmation', 'retrain_alert'"),
            ("title", "String", "Required", "Alert headline"),
            ("message", "String", "Required", "Alert description"),
            ("is_read", "Boolean", "Default False", "Read status flag"),
        ]),
        ("Collection 9: ab_tests", "Multivariate A/B testing campaigns with winner determination.", [
            ("_id", "ObjectId", "Primary Key", "Unique test identifier"),
            ("tenant_id", "String", "Multi-Tenant Key", "Foreign Key to tenant"),
            ("title", "String", "Required", "Campaign title"),
            ("description", "String", "Optional", "Experiment hypothesis"),
            ("variant_post_ids", "Array[String]", "Required", "Post IDs of variants A and B"),
            ("winner_post_id", "String", "Optional", "Post ID of winning variant"),
            ("status", "String", "Enum", "'running', 'completed'"),
        ]),
    ]

    for title, desc, fields in collections_data:
        doc.add_heading(title, level=2)
        doc.add_paragraph(desc)
        tbl = doc.add_table(rows=1, cols=4)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, h in enumerate(["Field Name", "Data Type", "Constraints / Key", "Description"]):
            c = tbl.rows[0].cells[i]
            c.text = h
            set_cell_background(c, "1F3864")
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

        for f_name, f_type, f_const, f_desc in fields:
            r = tbl.add_row().cells
            r[0].text = f_name
            r[1].text = f_type
            r[2].text = f_const
            r[3].text = f_desc
            for cell in r:
                set_cell_margins(cell, top=50, bottom=50, left=70, right=70)

    doc.add_page_break()

    # =========================================================================
    # 7. ALL SCREENSHOTS WITH URL (WITH ALL 17 HIGH-RES EMBEDDED SCREENSHOTS)
    # =========================================================================
    h7 = doc.add_heading("7. ALL SCREENSHOTS WITH URL", level=1)
    h7.runs[0].font.color.rgb = RGBColor(31, 56, 100)

    # 7.1 Admin Side
    doc.add_heading("7.1 Admin Side Screens & URLs (Full Access Modules)", level=2)
    doc.add_paragraph(
        "The Administrator role possesses complete platform access across all 12 navigation modules, "
        "including live content composition, multi-channel scheduling, computer vision thumbnail scoring, "
        "Facebook Prophet growth forecasting, multivariate A/B testing, and agency team role management."
    )

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
            doc.add_picture(img_p, width=Inches(6.2))
            p_cap = doc.add_paragraph(cap)
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.runs[0].font.italic = True
            p_cap.runs[0].font.size = Pt(9)
            p_d = doc.add_paragraph(desc)
            p_d.paragraph_format.space_after = Pt(10)

    # 7.2 Client Side
    doc.add_heading("7.2 Client Side Screens & URLs (Read-Only Observer Portal)", level=2)
    doc.add_paragraph(
        "The Client role provides a restricted 6-module view. Content creation and modification tools are strictly hidden, "
        "calendar modification buttons are suppressed, and the model retraining trigger displays an admin-only security lock notice."
    )

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
            doc.add_picture(img_p, width=Inches(6.2))
            p_cap = doc.add_paragraph(cap)
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.runs[0].font.italic = True
            p_cap.runs[0].font.size = Pt(9)
            p_d = doc.add_paragraph(desc)
            p_d.paragraph_format.space_after = Pt(10)

    # 7.3 Reports
    doc.add_heading("7.3 Reports (Printable PDF & Export in Excel)", level=2)
    doc.add_paragraph(
        "Fulfilling GLS University Syllabus Section 7.3, ContentIQ provides two native enterprise report export mechanisms on the Executive Dashboard: "
        "(1) Export to Excel (.csv): Located on the top-right of the dashboard. Downloads 'ContentIQ_Performance_Report_YYYY-MM-DD.csv' with platform distributions, summary KPIs, and ML accuracy (88.0%). "
        "(2) Print Report (PDF): Invokes browser print styling (@media print), cleanly formatting all cards and charts into an executive-ready hardcopy document."
    )

    report_screens = [
        ("screenshot_16_reports_excel_export.png", "Figure 7.16: Real-Time Performance Export in Excel (.csv) (URL: http://127.0.0.1:3000/dashboard)",
         "Instant client-side CSV export generating 'ContentIQ_Performance_Report_YYYY-MM-DD.csv' with raw campaign distributions and engagement metrics."),
        ("screenshot_17_reports_print_pdf.png", "Figure 7.17: Publication-Ready Printable Executive PDF Report (URL: http://127.0.0.1:3000/dashboard)",
         "Responsive @media print layout cleanly converting all KPI cards, engagement graphs, and platform charts into a publication-ready executive print report.")
    ]

    for fname, cap, desc in report_screens:
        img_p = os.path.join(SCREENSHOTS_DIR, fname)
        if os.path.exists(img_p):
            doc.add_picture(img_p, width=Inches(6.2))
            p_cap = doc.add_paragraph(cap)
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.runs[0].font.italic = True
            p_cap.runs[0].font.size = Pt(9)
            p_d = doc.add_paragraph(desc)
            p_d.paragraph_format.space_after = Pt(10)

    doc.add_page_break()

    # =========================================================================
    # 8. REFERENCES & BIBLIOGRAPHY
    # =========================================================================
    h8 = doc.add_heading("8. REFERENCES & BIBLIOGRAPHY", level=1)
    h8.runs[0].font.color.rgb = RGBColor(31, 56, 100)

    refs = [
        "[1] S. Tiangolo, 'FastAPI: Modern, High-Performance Web Framework for Building APIs with Python 3.8+', 2024. [Online]. Available: https://fastapi.tiangolo.com/",
        "[2] K. Banker, P. Bakkum, S. Verch, and D. Garrett, MongoDB in Action: Covers MongoDB version 3.0+, 2nd ed. Shelter Island, NY: Manning Publications, 2016.",
        "[3] L. Breiman, 'Random Forests', Machine Learning, vol. 45, no. 1, pp. 5–32, 2001. doi: 10.1023/A:1010933404324.",
        "[4] S. J. Taylor and B. Letham, 'Forecasting at scale', The American Statistician, vol. 72, no. 1, pp. 37–45, 2018. doi: 10.1080/00031305.2017.1380080.",
        "[5] C. Hutto and E. Gilbert, 'VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text', in Proc. 8th Int. AAAI Conf. Weblogs Social Media (ICWSM-14), 2014, pp. 216–225.",
        "[6] G. Bradski and A. Kaehler, Learning OpenCV: Computer Vision with the OpenCV Library, Sebastopol, CA: O'Reilly Media, 2008.",
        "[7] Meta Open Source, 'React: A JavaScript library for building user interfaces', React Documentation, 2024. [Online]. Available: https://react.dev/",
        "[8] Faculty of Computer Applications & Information Technology (FCAIT), GLS University, 'Syllabus and Project Guidelines for Course 222301907 Capstone Project – II', Ahmedabad, Academic Year 2026–2027.",
        "[9] A. Solem et al., 'Celery: Distributed Task Queue', Celery Documentation, 2024. [Online]. Available: https://docs.celeryq.dev/",
        "[10] F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python', Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
    ]
    for ref in refs:
        p = doc.add_paragraph(ref)
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)

    doc.save(OUT_DOCX)
    print(f"[+] Successfully generated Full DOCX with Diagrams & Screenshots: {OUT_DOCX}")

if __name__ == "__main__":
    create_full_docx()

"""
ContentIQ - High-Resolution Academic UML Diagram Renderer (600 DPI Vector-Quality)
Generates crystal-clear, razor-sharp diagrams with large, bold text for reports and presentations.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DIAGRAMS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\diagrams"
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

# 1. USE CASE DIAGRAM (Large, Crisp, Legible)
def render_clear_use_case():
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 96, "ContentIQ — System Use Case Diagram", ha='center', va='center',
            fontsize=20, fontweight='bold', color='#1F3864')

    # Boundary Box
    rect = patches.Rectangle((26, 6), 58, 86, linewidth=2.5, edgecolor='#1F3864', facecolor='#F8FAFC')
    ax.add_patch(rect)
    ax.text(28, 89, "ContentIQ Platform Boundary", fontsize=13, fontweight='bold', color='#1F3864')

    # Actors
    actors = [
        ("Agency Admin", 11, 75, '#1F3864'),
        ("Content Editor", 11, 48, '#D97706'),
        ("Agency Client", 11, 20, '#0284C7'),
    ]
    for name, x, y, col in actors:
        # Stick figure head
        ax.add_patch(patches.Circle((x, y + 4.5), 2.5, facecolor='white', edgecolor=col, linewidth=2.5))
        # Body
        ax.plot([x, x], [y + 2, y - 3], color=col, linewidth=2.5)
        # Arms
        ax.plot([x - 3, x + 3], [y + 0.5, y + 0.5], color=col, linewidth=2.5)
        # Legs
        ax.plot([x, x - 2.5], [y - 3, y - 6.5], color=col, linewidth=2.5)
        ax.plot([x, x + 2.5], [y - 3, y - 6.5], color=col, linewidth=2.5)
        ax.text(x, y - 9.5, f"«Actor»\n{name}", ha='center', va='top', fontsize=11, fontweight='bold', color=col)

    # Celery System Actor
    sx, sy = 91, 48
    ax.add_patch(patches.Rectangle((sx - 6, sy - 5), 12, 10, linewidth=2, edgecolor='#475569', facecolor='#F1F5F9'))
    ax.text(sx, sy, "«System Actor»\nCelery Worker", ha='center', va='center', fontsize=10, fontweight='bold', color='#475569')

    use_cases = [
        ("UC-01: Register & Authenticate", 40, 82),
        ("UC-02: Manage Team & Roles (RBAC)", 70, 82),
        ("UC-03: Create & Schedule Post", 40, 68),
        ("UC-04: Predict Engagement Tier", 70, 68),
        ("UC-05: Sweep Best Posting Hours", 70, 54),
        ("UC-06: Score Thumbnail Aesthetics", 40, 54),
        ("UC-07: Interactive Monthly Calendar", 40, 40),
        ("UC-08: Log Post Performance Metrics", 70, 40),
        ("UC-09: Retrain ML Model (Feedback Loop)", 70, 26),
        ("UC-10: Executive Analytics Dashboard", 40, 26),
        ("UC-11: Follower Growth Forecasting", 40, 13),
        ("UC-12: Auto-Publish Due Posts", 70, 13),
    ]

    uc_pos = {}
    for text, cx, cy in use_cases:
        ellipse = patches.Ellipse((cx, cy), 25, 8.5, facecolor='#FFFFFF', edgecolor='#1F3864', linewidth=2)
        ax.add_patch(ellipse)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=9, color='#1F3864', fontweight='bold')
        uc_pos[text] = (cx, cy)

    # Admin connectors
    for t in [use_cases[0][0], use_cases[1][0], use_cases[2][0], use_cases[7][0], use_cases[8][0], use_cases[9][0]]:
        ax.plot([14.5, uc_pos[t][0] - 12.5], [75, uc_pos[t][1]], color='#1F3864', linewidth=1.8)

    # Editor connectors
    for t in [use_cases[0][0], use_cases[2][0], use_cases[5][0], use_cases[6][0], use_cases[7][0]]:
        ax.plot([14.5, uc_pos[t][0] - 12.5], [48, uc_pos[t][1]], color='#D97706', linewidth=1.8)

    # Client connectors
    for t in [use_cases[0][0], use_cases[6][0], use_cases[9][0], use_cases[10][0]]:
        ax.plot([14.5, uc_pos[t][0] - 12.5], [20, uc_pos[t][1]], color='#0284C7', linewidth=1.8)

    # Celery connector
    ax.plot([85, uc_pos["UC-12: Auto-Publish Due Posts"][0] + 12.5], [48, uc_pos["UC-12: Auto-Publish Due Posts"][1]], color='#475569', linewidth=2)

    # Include & Extend
    ax.annotate("«include»", xy=(57.5, 68), xytext=(51, 71),
                arrowprops=dict(arrowstyle="->", linestyle="--", color="#1F3864", lw=1.5),
                fontsize=9.5, color="#1F3864", fontweight='bold')
    ax.annotate("«extend»", xy=(57.5, 57), xytext=(48, 63),
                arrowprops=dict(arrowstyle="->", linestyle="--", color="#D97706", lw=1.5),
                fontsize=9.5, color="#D97706", fontweight='bold')

    plt.tight_layout()
    out = os.path.join(DIAGRAMS_DIR, "use_case_diagram.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Rendered Clear Use Case Diagram: {out}")

# 2. CLASS DIAGRAM (Crisp 3-Compartment)
def render_clear_class_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(70, 96, "ContentIQ — Detailed Domain Class Diagram (OOAD Specification)", ha='center', va='center',
            fontsize=20, fontweight='bold', color='#1F3864')

    def draw_box(x, y, w, h_title, h_attr, h_meth, name, attrs, meths):
        total_h = h_title + h_attr + h_meth
        # Header
        ax.add_patch(patches.Rectangle((x, y - h_title), w, h_title, facecolor='#1F3864', edgecolor='#1F3864', lw=1.5))
        ax.text(x + w/2, y - h_title/2, name, ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        # Attrs
        ax.add_patch(patches.Rectangle((x, y - h_title - h_attr), w, h_attr, facecolor='#F8FAFC', edgecolor='#1F3864', lw=1.5))
        yc = y - h_title - 3
        for a in attrs:
            ax.text(x + 2, yc, a, fontsize=9, color='#1E293B', va='top')
            yc -= 3.5
        # Meths
        ax.add_patch(patches.Rectangle((x, y - total_h), w, h_meth, facecolor='#FFFFFF', edgecolor='#1F3864', lw=1.5))
        yc = y - h_title - h_attr - 3
        for m in meths:
            ax.text(x + 2, yc, m, fontsize=9, color='#0F172A', va='top', fontweight='bold')
            yc -= 3.5

    # Top Row
    draw_box(8, 90, 36, 6, 18, 14, "Tenant",
             ["- id: ObjectId", "+ name: String", "+ plan: String", "+ created_at: DateTime"],
             ["+ get_details()", "+ update_plan(plan)"])

    draw_box(50, 90, 40, 6, 24, 18, "User",
             ["- id: ObjectId", "+ email: String", "+ name: String", "- hashed_password: String", "+ tenant_id: String", "+ role: Role"],
             ["+ verify_password(): Bool", "+ generate_jwt(): String", "+ change_role(Role)"])

    draw_box(96, 90, 38, 6, 28, 18, "Post",
             ["- id: ObjectId", "+ tenant_id: String", "+ platform: Platform", "+ caption: String", "+ scheduled_time: DateTime", "+ scheduled_hour: Int", "+ status: PostStatus"],
             ["+ schedule()", "+ reschedule(new_time)", "+ extract_local_hour()"])

    # Bottom Row
    draw_box(8, 44, 38, 6, 28, 16, "PostMetrics",
             ["- id: ObjectId", "+ tenant_id: String", "+ post_id: String", "+ impressions: Int", "+ likes: Int", "+ comments: Int", "+ engagement_rate: Float", "+ tier: EngagementTier"],
             ["+ compute_rate(): Float", "+ classify_tier()"])

    draw_box(52, 44, 38, 6, 22, 14, "Comment",
             ["- id: ObjectId", "+ tenant_id: String", "+ post_id: String", "+ text: String", "+ sentiment: Sentiment", "+ score: Float"],
             ["+ score_vader_sentiment()"])

    draw_box(96, 44, 38, 6, 16, 22, "MLScoringEngine",
             ["- rf_model: RandomForest", "- topic_vectorizer: TFIDF"],
             ["+ extract_features(): DF", "+ predict_tier(): Result", "+ sweep_24_hours(): List", "+ retrain_model(): Metrics"])

    # Connectors
    # Tenant - User
    ax.annotate("", xy=(50, 72), xytext=(44, 72), arrowprops=dict(arrowstyle="<|-", lw=2, color="#1F3864"))
    ax.text(45, 74, "1", fontsize=11, fontweight='bold', color='#1F3864')
    ax.text(47, 74, "1..*", fontsize=11, fontweight='bold', color='#1F3864')
    ax.text(45, 68, "employs", fontsize=9, style='italic', color='#64748B')

    # User - Post
    ax.annotate("", xy=(96, 72), xytext=(90, 72), arrowprops=dict(arrowstyle="->", lw=2, color="#1F3864"))
    ax.text(91, 74, "1", fontsize=11, fontweight='bold')
    ax.text(94, 74, "0..*", fontsize=11, fontweight='bold')
    ax.text(91, 68, "authors", fontsize=9, style='italic', color='#64748B')

    # Post - PostMetrics
    ax.plot([105, 105, 27, 27], [38, 8, 8, 0], color='#1F3864', lw=1.8)
    ax.text(107, 34, "1", fontsize=11, fontweight='bold')
    ax.text(30, 2, "0..1", fontsize=11, fontweight='bold')

    # Post - Comment
    ax.plot([115, 115, 71, 71], [38, 12, 12, 4], color='#1F3864', lw=1.8)
    ax.text(117, 30, "1", fontsize=11, fontweight='bold')
    ax.text(73, 6, "0..*", fontsize=11, fontweight='bold')

    # Post ..> MLScoringEngine
    ax.annotate("«evaluates»", xy=(115, 38), xytext=(115, 44),
                arrowprops=dict(arrowstyle="->", linestyle="--", lw=1.8, color="#D97706"),
                ha='center', fontsize=9.5, color='#D97706', fontweight='bold')

    plt.tight_layout()
    out = os.path.join(DIAGRAMS_DIR, "class_diagram.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Rendered Clear Class Diagram: {out}")

# 3. SWIMLANE ACTIVITY DIAGRAM (Large, Clear, Legible)
def render_clear_swimlane():
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(50, 97, "ContentIQ — 4-Lane Swimlane Activity Diagram (End-to-End Workflow)",
            ha='center', va='center', fontsize=20, fontweight='bold', color='#1F3864')

    lanes = [
        ("Swimlane 1: Content Creator (Admin / Editor)", 2, 23.5, '#F8FAFC', '#1F3864'),
        ("Swimlane 2: React 18 Frontend UI", 25.5, 23.5, '#F1F5F9', '#D97706'),
        ("Swimlane 3: FastAPI Gateway & ML Engine", 49, 24.5, '#F8FAFC', '#1F3864'),
        ("Swimlane 4: Celery Background Worker & MongoDB", 73.5, 24.5, '#F1F5F9', '#0284C7')
    ]

    for name, x, w, bg, col in lanes:
        # Header
        ax.add_patch(patches.Rectangle((x, 90.5), w, 5, facecolor=col, edgecolor='#CBD5E1', lw=1.5))
        ax.text(x + w/2, 93, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color='white')
        # Body
        ax.add_patch(patches.Rectangle((x, 3), w, 87.5, facecolor=bg, edgecolor='#CBD5E1', lw=1.5))

    # Helper
    def act(x, y, w, h, text, col='#1F3864', fill='#FFFFFF'):
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.6,rounding_size=1",
                                      facecolor=fill, edgecolor=col, lw=1.8)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, color=col, fontweight='bold')

    # Start
    ax.add_patch(patches.Circle((13.75, 87), 1.8, facecolor='#1F3864'))

    # Step 1
    act(13.75, 79, 20, 6, "Drafts post caption &\nselects target platform")
    ax.annotate("", xy=(13.75, 82), xytext=(13.75, 85.2), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1F3864"))

    # Step 2
    act(13.75, 69, 20, 5, "Clicks 'Score Post with AI'")
    ax.annotate("", xy=(13.75, 71.5), xytext=(13.75, 76), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1F3864"))

    # To Frontend
    act(37.25, 69, 21, 6, "POST /api/predictions/score\n(Payload extracted)", '#D97706')
    ax.annotate("", xy=(26.75, 69), xytext=(23.75, 69), arrowprops=dict(arrowstyle="->", lw=1.8, color="#D97706"))

    # To Backend
    act(61.25, 69, 22, 6.5, "extract_features(): 10 features\nRandomForest.predict_proba()", '#1F3864')
    ax.annotate("", xy=(50.25, 69), xytext=(47.75, 69), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1F3864"))

    # Return to Frontend
    act(37.25, 57, 21, 6, "Renders Predicted Tier Badge\n& Confidence Gauge", '#D97706')
    ax.annotate("", xy=(37.25, 60), xytext=(55, 66), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1F3864", linestyle="--"))

    # 24h Sweep
    act(61.25, 48, 22, 6.5, "24-Hour Best-Time Sweep\nSorts top 3 peak hours", '#1F3864')
    ax.annotate("", xy=(61.25, 51.5), xytext=(43, 54), arrowprops=dict(arrowstyle="->", lw=1.8, color="#D97706"))

    # Creator Confirms
    act(13.75, 48, 20, 6, "Reviews peak hours &\nconfirms schedule time")
    ax.annotate("", xy=(23.75, 48), xytext=(50.25, 48), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1F3864", linestyle="--"))

    # Save to Frontend
    act(37.25, 37, 21, 5, "POST /api/posts\n(Saves scheduled datetime)", '#D97706')
    ax.annotate("", xy=(26.75, 37), xytext=(17, 45), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1F3864"))

    # MongoDB Inserts
    act(85.75, 37, 22, 6, "MongoDB: Inserts document\ninto 'posts' collection", '#0284C7')
    ax.annotate("", xy=(74.75, 37), xytext=(47.75, 37), arrowprops=dict(arrowstyle="->", lw=1.8, color="#0284C7"))

    # Celery Beat publishes
    act(85.75, 25, 22, 6.5, "Celery Beat Scheduler (30s)\nscheduled_time <= NOW?\nCalls SandboxPublisher", '#0284C7')
    ax.annotate("", xy=(85.75, 28.5), xytext=(85.75, 34), arrowprops=dict(arrowstyle="->", lw=1.8, color="#0284C7"))

    # Published & Notified
    act(85.75, 14, 22, 5, "UPDATE status='published'\nDispatches Notification", '#0284C7')
    ax.annotate("", xy=(85.75, 16.5), xytext=(85.75, 21.75), arrowprops=dict(arrowstyle="->", lw=1.8, color="#0284C7"))

    # Retrain Model
    act(13.75, 14, 20, 6, "Admin clicks 'Retrain Model'\non Executive Dashboard")
    act(61.25, 14, 22, 6.5, "Verifies >= 50 metrics\nRetrains RandomForest\nUpdates model on disk", '#1F3864')
    ax.annotate("", xy=(50.25, 14), xytext=(23.75, 14), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1F3864"))

    # End Node
    ax.add_patch(patches.Circle((61.25, 5), 2.2, facecolor='white', edgecolor='#1F3864', lw=2))
    ax.add_patch(patches.Circle((61.25, 5), 1.4, facecolor='#1F3864'))
    ax.annotate("", xy=(61.25, 7.2), xytext=(61.25, 10.75), arrowprops=dict(arrowstyle="->", lw=1.8, color="#1F3864"))

    plt.tight_layout()
    out = os.path.join(DIAGRAMS_DIR, "swimlane_activity_diagram.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Rendered Clear Swimlane Activity Diagram: {out}")

# 4. SEQUENCE DIAGRAM
def render_clear_sequence():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(50, 96, "ContentIQ — Sequence Diagram: Pre-Flight AI Prediction & 24h Sweep",
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1F3864')

    lifelines = [
        ("Content Editor\n(Actor)", 12, '#1F3864'),
        ("React 18 UI\n(PostCompose.jsx)", 34, '#D97706'),
        ("FastAPI Gateway\n(REST API)", 56, '#1F3864'),
        ("PredictionService\n(Core ML)", 78, '#0284C7'),
        ("RandomForest\n(Model Artifact)", 93, '#475569'),
    ]

    for name, x, col in lifelines:
        ax.add_patch(patches.Rectangle((x - 8, 86), 16, 7.5, facecolor=col, edgecolor='#CBD5E1', lw=1.5))
        ax.text(x, 89.75, name, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        ax.plot([x, x], [86, 5], color='#94A3B8', linestyle='--', lw=1.2)

    msgs = [
        (12, 34, 80, "1. Enters caption & platform", False),
        (12, 34, 73, "2. Clicks 'Score Post with AI'", False),
        (34, 56, 66, "3. POST /api/predictions/score {caption, platform, hour}", False),
        (56, 78, 59, "4. score_draft_post(extract_features)", False),
        (78, 93, 52, "5. predict_proba(10-feature vector)", False),
        (93, 78, 46, "6. [P(low), P(medium), P(high)]", True),
        (78, 56, 40, "7. {predicted_tier: 'high', confidence: 0.88}", True),
        (56, 34, 34, "8. 200 OK Response (JSON payload)", True),
        (34, 34, 28, "9. Renders High Tier Badge & Gauge", False),
        (34, 56, 22, "10. POST /api/predictions/best-time (24h Sweep)", False),
        (56, 78, 16, "11. sweep_best_time() -> top 3 peak hours", False),
        (78, 34, 10, "12. Returns Recommended Hours: [18:00, 19:00, 14:00]", True),
    ]

    for x1, x2, y, txt, is_return in msgs:
        ls = '--' if is_return else '-'
        col = '#0284C7' if is_return else '#1F3864'
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", linestyle=ls, lw=1.6, color=col))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 1.4, txt, ha='center', va='bottom', fontsize=8.5, color=col, fontweight='bold')

    plt.tight_layout()
    out = os.path.join(DIAGRAMS_DIR, "sequence_diagram.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Rendered Clear Sequence Diagram: {out}")

# 5. STATE CHART DIAGRAM
def render_clear_state_chart():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(50, 94, "ContentIQ — Post Lifecycle State Chart Diagram",
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1F3864')

    ax.add_patch(patches.Circle((8, 50), 2.5, facecolor='#1F3864'))

    def sbox(x, y, w, h, name, desc):
        r = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.6,rounding_size=1.5",
                                   facecolor='#F8FAFC', edgecolor='#1F3864', lw=2)
        ax.add_patch(r)
        ax.text(x, y + 2, name, ha='center', va='center', fontsize=11, fontweight='bold', color='#1F3864')
        ax.text(x, y - 2.5, desc, ha='center', va='center', fontsize=8.5, color='#475569')

    sbox(24, 50, 18, 14, "DRAFT", "Caption edit &\npre-flight AI score")
    ax.annotate("Create draft", xy=(15, 50), xytext=(10.5, 50), arrowprops=dict(arrowstyle="->", lw=1.6, color="#1F3864"), fontsize=9)

    sbox(52, 50, 20, 14, "SCHEDULED", "Target datetime set\nQueued in MongoDB")
    ax.annotate("Set target time", xy=(42, 50), xytext=(33, 50), arrowprops=dict(arrowstyle="->", lw=1.6, color="#1F3864"), fontsize=9)

    sbox(80, 50, 20, 14, "PUBLISHED", "Pushed via Sandbox\nIn-app alert sent")
    ax.annotate("Celery Beat worker\nscheduled_time <= NOW", xy=(70, 50), xytext=(62, 50), arrowprops=dict(arrowstyle="->", lw=1.6, color="#1F3864"), fontsize=8)

    sbox(80, 18, 22, 13, "METRICS_COLLECTED", "Empirical likes & reach\n>= 50 triggers retrain")
    ax.annotate("Audience engages (24-48h)", xy=(80, 24.5), xytext=(80, 43), arrowprops=dict(arrowstyle="->", lw=1.6, color="#D97706"), fontsize=8.5)

    ax.annotate("Retrained Model pickle saved on disk", xy=(24, 43), xytext=(69, 18),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#D97706", linestyle="--"),
                fontsize=9, color="#D97706", fontweight='bold')

    # Final
    ax.add_patch(patches.Circle((95, 50), 2.8, facecolor='white', edgecolor='#1F3864', lw=2))
    ax.add_patch(patches.Circle((95, 50), 1.8, facecolor='#1F3864'))
    ax.annotate("Archive", xy=(92, 50), xytext=(90, 50), arrowprops=dict(arrowstyle="->", lw=1.6, color="#1F3864"), fontsize=9)

    plt.tight_layout()
    out = os.path.join(DIAGRAMS_DIR, "state_chart_diagram.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Rendered Clear State Chart Diagram: {out}")

if __name__ == "__main__":
    render_clear_use_case()
    render_clear_class_diagram()
    render_clear_swimlane()
    render_clear_sequence()
    render_clear_state_chart()
    print("[+] All 5 High-Resolution Clear UML Diagrams successfully re-rendered!")

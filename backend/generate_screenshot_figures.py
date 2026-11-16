"""
ContentIQ - UI Screenshot Generator
Renders high-fidelity, publication-ready UI screenshots for the project report and slides.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

SCREENSHOTS_DIR = r"C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ\docs\ready_to_download\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def render_ui_window(title, url, draw_body_fn, filename):
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=220)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#0F172A')

    # Browser Outer Frame
    frame = patches.FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=0.5,rounding_size=1.5",
                                   facecolor='#FFFFFF', edgecolor='#334155', lw=1.5)
    ax.add_patch(frame)

    # Browser Chrome Header
    chrome = patches.Rectangle((1, 91), 98, 8, facecolor='#1E293B')
    ax.add_patch(chrome)

    # Window dots (Red, Yellow, Green)
    ax.add_patch(patches.Circle((4, 95), 1.2, facecolor='#EF4444'))
    ax.add_patch(patches.Circle((7, 95), 1.2, facecolor='#F59E0B'))
    ax.add_patch(patches.Circle((10, 95), 1.2, facecolor='#10B981'))

    # URL Address Bar
    url_bar = patches.FancyBboxPatch((16, 92.5), 68, 5, boxstyle="round,pad=0.3,rounding_size=0.8",
                                     facecolor='#0F172A', edgecolor='#475569', lw=1)
    ax.add_patch(url_bar)
    ax.text(18, 95, f"🔒 {url}", color='#94A3B8', fontsize=8.5, va='center', fontfamily='monospace')

    # Screen Title Header
    ax.text(88, 95, "ContentIQ v1.0", color='#F8FAFC', fontsize=8.5, fontweight='bold', va='center')

    # Body
    draw_body_fn(ax)

    plt.tight_layout()
    out = os.path.join(SCREENSHOTS_DIR, filename)
    plt.savefig(out, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"[+] Rendered Screenshot: {out}")

# 1. Admin Dashboard
def body_dashboard(ax):
    # Sidebar
    ax.add_patch(patches.Rectangle((1, 1), 18, 90, facecolor='#1F3864'))
    ax.text(10, 85, "ContentIQ", color='#F59E0B', fontsize=12, fontweight='bold', ha='center')
    ax.text(10, 81, "Apex Digital Agency", color='#94A3B8', fontsize=7.5, ha='center')

    navs = ["📊 Dashboard", "📅 Calendar", "✏️ Compose Post", "📈 Analytics", "🔥 Trends", "🖼️ Thumbnail Scorer", "👥 Team & Roles"]
    y_nav = 74
    for nav in navs:
        bg = '#334D7D' if 'Dashboard' in nav else '#1F3864'
        ax.add_patch(patches.Rectangle((2, y_nav - 2), 16, 4, facecolor=bg))
        ax.text(3, y_nav, nav, color='white', fontsize=7.5, va='center')
        y_nav -= 6

    # Top KPI Cards
    ax.text(22, 86, "Executive Analytics & Model Performance Dashboard", fontsize=13, fontweight='bold', color='#1F3864')

    # Golden Retrain Banner
    banner = patches.FancyBboxPatch((22, 74), 74, 8, boxstyle="round,pad=0.3,rounding_size=0.8",
                                     facecolor='#FEF3C7', edgecolor='#D97706', lw=1.2)
    ax.add_patch(banner)
    ax.text(24, 78, "✨ Continuous Retraining Active: Golden Random Forest Model at 88.0% Accuracy", color='#92400E', fontsize=8.5, fontweight='bold')
    ax.text(24, 75, "85 empirical metrics collected across Instagram, LinkedIn, and YouTube | Improvement: +4.2% delta", color='#B45309', fontsize=7.5)

    # Retrain button
    btn = patches.FancyBboxPatch((82, 75), 12, 6, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor='#D97706')
    ax.add_patch(btn)
    ax.text(88, 78, "⚡ Retrain Model", color='white', fontsize=7.5, fontweight='bold', ha='center', va='center')

    # KPI Metric Cards
    kpis = [
        ("Total Content Posts", "90", "#1F3864"),
        ("Published Live", "52", "#10B981"),
        ("Scheduled Queue", "38", "#D97706"),
        ("Avg Engagement Rate", "4.82%", "#0284C7"),
        ("Live ML Accuracy", "88.0%", "#8B5CF6")
    ]
    for i, (k_title, k_val, k_col) in enumerate(kpis):
        kx = 22 + i * 15.2
        c_box = patches.FancyBboxPatch((kx, 60), 13.8, 11, boxstyle="round,pad=0.3,rounding_size=0.8",
                                       facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1)
        ax.add_patch(c_box)
        ax.text(kx + 6.9, 68, k_title, fontsize=6.5, color='#64748B', ha='center')
        ax.text(kx + 6.9, 63.5, k_val, fontsize=12, fontweight='bold', color=k_col, ha='center')

    # Charts Mockup
    # Chart 1: Platform breakdown
    c1 = patches.FancyBboxPatch((22, 10), 35, 46, boxstyle="round,pad=0.3,rounding_size=0.8", facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1)
    ax.add_patch(c1)
    ax.text(39.5, 52, "Platform Distribution", fontsize=9, fontweight='bold', color='#1F3864', ha='center')
    ax.add_patch(patches.Wedge((39.5, 32), 14, 0, 150, facecolor='#E1306C')) # Instagram
    ax.add_patch(patches.Wedge((39.5, 32), 14, 150, 260, facecolor='#0077B5')) # LinkedIn
    ax.add_patch(patches.Wedge((39.5, 32), 14, 260, 360, facecolor='#FF0000')) # YouTube
    ax.text(39.5, 14, "Instagram: 40 | LinkedIn: 30 | YouTube: 20", fontsize=7.5, color='#475569', ha='center')

    # Chart 2: 24h Engagement Distribution
    c2 = patches.FancyBboxPatch((60, 10), 36, 46, boxstyle="round,pad=0.3,rounding_size=0.8", facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1)
    ax.add_patch(c2)
    ax.text(78, 52, "24-Hour Best Posting Hours (Sweep)", fontsize=9, fontweight='bold', color='#1F3864', ha='center')
    hours = [6, 9, 12, 14, 18, 20, 22]
    vals = [20, 45, 75, 88, 95, 82, 40]
    for idx, (h, v) in enumerate(zip(hours, vals)):
        bx = 64 + idx * 4.4
        bh = (v / 100) * 26
        col = '#D97706' if v >= 88 else '#1F3864'
        ax.add_patch(patches.Rectangle((bx, 20), 3.2, bh, facecolor=col))
        ax.text(bx + 1.6, 17, f"{h}h", fontsize=6.5, ha='center', color='#64748B')
    ax.text(78, 13, "Peak Posting Recommendation: 18:00 (95% Engagement Score)", fontsize=7.5, fontweight='bold', color='#D97706', ha='center')

# 2. Post Composer Screen
def body_composer(ax):
    # Sidebar
    ax.add_patch(patches.Rectangle((1, 1), 18, 90, facecolor='#1F3864'))
    ax.text(10, 85, "ContentIQ", color='#F59E0B', fontsize=12, fontweight='bold', ha='center')

    # Composer Form (Left 42%)
    ax.text(22, 85, "Compose Post & Pre-Flight AI Assistant", fontsize=13, fontweight='bold', color='#1F3864')

    form_box = patches.FancyBboxPatch((22, 8), 36, 73, boxstyle="round,pad=0.3,rounding_size=0.8", facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1)
    ax.add_patch(form_box)
    ax.text(25, 76, "Post Title & Channel", fontsize=8.5, fontweight='bold', color='#1F3864')
    ax.add_patch(patches.Rectangle((25, 70), 30, 4, facecolor='#F1F5F9', edgecolor='#CBD5E1'))
    ax.text(26, 72, "AI Workflow Innovation in 2026", fontsize=7.5, color='#1E293B')

    ax.text(25, 65, "Caption & Creative Content", fontsize=8.5, fontweight='bold', color='#1F3864')
    ax.add_patch(patches.Rectangle((25, 38), 30, 24, facecolor='#F8FAFC', edgecolor='#CBD5E1'))
    ax.text(26, 58, "Excited to share our breakthrough multi-tenant\narchitecture! #AI #Tech #Innovation\nOptimized for maximum creator engagement.", fontsize=7.5, color='#334155')

    ax.text(25, 32, "Scheduled Publication Time (Local):", fontsize=8, fontweight='bold', color='#1F3864')
    ax.add_patch(patches.Rectangle((25, 25), 30, 5, facecolor='#F1F5F9', edgecolor='#CBD5E1'))
    ax.text(26, 27.5, "2026-10-25T18:00 (Hour: 18)", fontsize=8, color='#0284C7', fontweight='bold')

    # Predict Button
    btn_pred = patches.FancyBboxPatch((25, 14), 30, 7, boxstyle="round,pad=0.3,rounding_size=0.8", facecolor='#D97706')
    ax.add_patch(btn_pred)
    ax.text(40, 17.5, "⚡ Score Post with Pre-Flight AI", color='white', fontsize=8.5, fontweight='bold', ha='center', va='center')

    # AI Pre-flight Output (Right 36%)
    ai_box = patches.FancyBboxPatch((60, 8), 36, 73, boxstyle="round,pad=0.3,rounding_size=0.8", facecolor='#F8FAFC', edgecolor='#D97706', lw=1.5)
    ax.add_patch(ai_box)
    ax.text(78, 76, "Pre-Flight ML Prediction", fontsize=11, fontweight='bold', color='#1F3864', ha='center')

    # Predicted Badge
    b_badge = patches.FancyBboxPatch((66, 64), 24, 8, boxstyle="round,pad=0.3,rounding_size=1", facecolor='#DCFCE7', edgecolor='#16A34A', lw=1.2)
    ax.add_patch(b_badge)
    ax.text(78, 68, "TIER: HIGH (>5% Engagement)", color='#15803D', fontsize=8.5, fontweight='bold', ha='center', va='center')

    ax.text(78, 59, "Random Forest Model Confidence: 88.0%", fontsize=8, fontweight='bold', color='#1F3864', ha='center')

    # Mini 24h curve
    ax.text(64, 52, "24-Hour Best-Time Probability Sweep:", fontsize=8, fontweight='bold', color='#475569')
    hours2 = [9, 12, 15, 18, 21]
    vals2 = [50, 70, 80, 95, 60]
    for idx, (h, v) in enumerate(zip(hours2, vals2)):
        bx = 65 + idx * 5.4
        bh = (v / 100) * 16
        ax.add_patch(patches.Rectangle((bx, 30), 4, bh, facecolor='#1F3864' if v < 90 else '#D97706'))
        ax.text(bx + 2, 27, f"{h}h", fontsize=7, ha='center', color='#64748B')

    ax.add_patch(patches.Rectangle((64, 14), 28, 8, facecolor='#FEF3C7', edgecolor='#D97706'))
    ax.text(78, 18, "⭐ Peak Window: 18:00 (6:00 PM)", fontsize=8, fontweight='bold', color='#92400E', ha='center')

# 3. Client Portal Screen
def body_client_portal(ax):
    # Sidebar
    ax.add_patch(patches.Rectangle((1, 1), 18, 90, facecolor='#1F3864'))
    ax.text(10, 85, "ContentIQ", color='#F59E0B', fontsize=12, fontweight='bold', ha='center')
    ax.text(10, 81, "Apex Agency Client Portal", color='#94A3B8', fontsize=7, ha='center')

    # Client specific restricted navigation (only 6 links)
    navs = ["📊 Dashboard", "📅 Calendar (Read-Only)", "📈 Analytics", "📈 Follower Forecast", "👥 Competitors", "🔔 Notifications"]
    y_nav = 72
    for nav in navs:
        ax.add_patch(patches.Rectangle((2, y_nav - 2), 16, 4, facecolor='#1F3864'))
        ax.text(3, y_nav, nav, color='white', fontsize=7.5, va='center')
        y_nav -= 7

    ax.text(22, 86, "Client Observer Portal (Read-Only Campaign Access)", fontsize=13, fontweight='bold', color='#0284C7')

    # Restricted notice banner
    lock_banner = patches.FancyBboxPatch((22, 75), 74, 8, boxstyle="round,pad=0.3,rounding_size=0.8",
                                         facecolor='#F1F5F9', edgecolor='#94A3B8', lw=1.2)
    ax.add_patch(lock_banner)
    ax.text(25, 79, "🔒 Client Observer Role (RBAC): Post creation, deletion, and model retraining are locked.", color='#334155', fontsize=8.5, fontweight='bold')
    ax.text(25, 76, "You have full read-only transparency to scheduled posts, campaign metrics, and export tools.", color='#64748B', fontsize=7.5)

    # 4 KPI cards for client
    kpis = [
        ("Total Posts Scheduled", "38 Posts", "#0284C7"),
        ("Live Published Posts", "52 Posts", "#10B981"),
        ("Audience Reach", "145,200", "#1F3864"),
        ("Overall Campaign Engagement", "4.82%", "#D97706")
    ]
    for i, (k_title, k_val, k_col) in enumerate(kpis):
        kx = 22 + i * 18.8
        c_box = patches.FancyBboxPatch((kx, 58), 17.5, 12, boxstyle="round,pad=0.3,rounding_size=0.8",
                                       facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1)
        ax.add_patch(c_box)
        ax.text(kx + 8.75, 66.5, k_title, fontsize=7.5, color='#64748B', ha='center')
        ax.text(kx + 8.75, 61.5, k_val, fontsize=13, fontweight='bold', color=k_col, ha='center')

    # Calendar preview (read-only)
    cal_box = patches.FancyBboxPatch((22, 10), 74, 44, boxstyle="round,pad=0.3,rounding_size=0.8", facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1)
    ax.add_patch(cal_box)
    ax.text(25, 50, "Scheduled Content Queue — Verification View (No Edit/Delete Permissions)", fontsize=9.5, fontweight='bold', color='#1F3864')

    sample_posts = [
        ("Oct 25, 18:00", "Instagram", "AI Workflow Innovation in 2026", "TIER: HIGH", "#E1306C"),
        ("Oct 26, 14:00", "LinkedIn", "Why Multi-Tenancy Matters for Enterprise SaaS", "TIER: HIGH", "#0077B5"),
        ("Oct 27, 11:00", "YouTube", "Full-Stack Tutorial: FastAPI & Celery", "TIER: MED", "#FF0000"),
    ]
    for idx, (dt, ch, cap, tr, pcol) in enumerate(sample_posts):
        py = 40 - idx * 10
        ax.add_patch(patches.Rectangle((25, py - 2), 68, 7, facecolor='#F8FAFC', edgecolor='#E2E8F0'))
        ax.text(27, py + 1.5, dt, fontsize=7.5, fontweight='bold', color='#1F3864')
        ax.add_patch(patches.FancyBboxPatch((40, py - 0.5), 12, 4, boxstyle="round,pad=0.2", facecolor=pcol))
        ax.text(46, py + 1.5, ch, color='white', fontsize=7, fontweight='bold', ha='center')
        ax.text(54, py + 1.5, cap, fontsize=7.5, color='#334155')
        ax.text(88, py + 1.5, tr, fontsize=7, fontweight='bold', color='#15803D')

# 4. Reports Export Screen
def body_reports(ax):
    ax.add_patch(patches.Rectangle((1, 1), 18, 90, facecolor='#1F3864'))
    ax.text(10, 85, "ContentIQ", color='#F59E0B', fontsize=12, fontweight='bold', ha='center')

    ax.text(22, 85, "Enterprise Reporting & Exports (GLS University Syllabus 7.3)", fontsize=13, fontweight='bold', color='#1F3864')

    # Action Bar Box
    act_bar = patches.FancyBboxPatch((22, 70), 74, 10, boxstyle="round,pad=0.3,rounding_size=0.8", facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.2)
    ax.add_patch(act_bar)
    ax.text(25, 75, "One-Click Executive Export Utilities:", fontsize=9, fontweight='bold', color='#1F3864')

    btn_excel = patches.FancyBboxPatch((55, 72), 18, 6, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor='#10B981')
    ax.add_patch(btn_excel)
    ax.text(64, 75, "📊 Export to Excel (.csv)", color='white', fontsize=8, fontweight='bold', ha='center', va='center')

    btn_pdf = patches.FancyBboxPatch((75, 72), 18, 6, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor='#0284C7')
    ax.add_patch(btn_pdf)
    ax.text(84, 75, "🖨️ Print Report (PDF)", color='white', fontsize=8, fontweight='bold', ha='center', va='center')

    # CSV Data Preview Table
    tbl = patches.FancyBboxPatch((22, 10), 74, 56, boxstyle="round,pad=0.3,rounding_size=0.8", facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1)
    ax.add_patch(tbl)
    ax.text(25, 61, "Generated CSV Output Preview (ContentIQ_Performance_Report_2026-10-23.csv):", fontsize=8.5, fontweight='bold', color='#1F3864')

    csv_rows = [
        ("Platform", "Count", "Category"),
        ("Instagram Posts", "40", "Platform Breakdown"),
        ("LinkedIn Posts", "30", "Platform Breakdown"),
        ("YouTube Posts", "20", "Platform Breakdown"),
        ("Total Content Posts", "90", "Summary KPI"),
        ("Published Posts", "52", "Summary KPI"),
        ("Scheduled Queue", "38", "Summary KPI"),
        ("Average Engagement Rate (%)", "4.82%", "Summary KPI"),
        ("ML Model Accuracy on Real Data (%)", "88.0%", "ML Validation"),
    ]
    for i, (col1, col2, col3) in enumerate(csv_rows):
        ry = 54 - i * 4.8
        bg_col = '#1F3864' if i == 0 else ('#F8FAFC' if i % 2 == 1 else '#FFFFFF')
        txt_col = 'white' if i == 0 else '#1E293B'
        ax.add_patch(patches.Rectangle((25, ry - 1.5), 68, 4.2, facecolor=bg_col, edgecolor='#E2E8F0'))
        ax.text(28, ry + 0.5, col1, fontsize=7.5, color=txt_col, fontweight='bold' if i == 0 else 'normal')
        ax.text(60, ry + 0.5, col2, fontsize=7.5, color=txt_col, fontweight='bold' if i == 0 else 'normal')
        ax.text(78, ry + 0.5, col3, fontsize=7.5, color=txt_col, fontweight='bold' if i == 0 else 'normal')

if __name__ == "__main__":
    render_ui_window("Dashboard", "http://127.0.0.1:3000/dashboard", body_dashboard, "screenshot_admin_dashboard.png")
    render_ui_window("Post Composer", "http://127.0.0.1:3000/compose", body_composer, "screenshot_post_composer.png")
    render_ui_window("Client Portal", "http://127.0.0.1:3000/dashboard (Client)", body_client_portal, "screenshot_client_portal.png")
    render_ui_window("Reports Export", "http://127.0.0.1:3000/dashboard (Reports)", body_reports, "screenshot_reports_export.png")
    print("[+] All UI screenshots successfully generated!")

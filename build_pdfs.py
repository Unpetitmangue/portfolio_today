"""
Builds the downloadable CV and slide deck for the portfolio site.

Edit the CONTENT section, then run:
    pip install reportlab
    python tools/build_pdfs.py

Output goes to downloads/. Both files are linked from index.html.

Font: if you own Gotham, put Gotham-Book.ttf, Gotham-Medium.ttf and
Gotham-Bold.ttf in a fonts/ folder next to this script's parent and the PDFs
will use it. Otherwise they fall back to Helvetica.
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ------------------------------------------------------------------ CONTENT
NAME = "Thyme Inn"
ROLE = "Financial analyst"
EMAIL = "you@example.com"
PHONE = "+60 12-345 6789"
PLACE = "City, Country"
LINKS = [
    ("LinkedIn", "https://www.linkedin.com/in/your-profile"),
    ("GitHub", "https://github.com/your-username"),
    ("YouTube", "https://www.youtube.com/channel/UCObCmO3cjvXgU2UhgttaAZw/"),
]
PROFILE = ("Financial analyst with eight years across equity research, FP&A and risk "
           "modelling. I build forecasts that finance teams trust and explain them in "
           "plain language. Open to analyst and associate roles in corporate finance "
           "and portfolio strategy.")
RESULTS = [("+18%", "forecast accuracy"), ("$2.4M", "annual savings"),
           ("-32%", "days to close"), ("11", "companies covered")]
EXPERIENCE = [
    ("Associate Director, Portfolio Strategy", "Harbor Group", "2026 - Present", [
        "Set allocation scenarios and reporting for a multi-asset portfolio reviewed by the board each quarter.",
        "Manage three analysts and the annual planning calendar."]),
    ("Lead Analyst, FP&A", "Harbor Group", "2024 - 2026", [
        "Rebuilt the rolling revenue forecast as a driver-based model, improving accuracy by 18%.",
        "Reviewed vendor spend and renegotiated the five largest contracts, saving $2.4M a year."]),
    ("Senior Analyst", "Northbridge Capital", "2022 - 2024", [
        "Automated month-end reconciliations and variance commentary in Python, cutting days to close by 32%.",
        "Passed CFA Level II and mentored two junior analysts."]),
    ("Analyst, Equity Research and Risk", "Northbridge Capital", "2018 - 2022", [
        "Built valuation models and initiated coverage on 11 consumer and industrial companies.",
        "Moved into risk modelling in 2020 to support stress testing through the downturn."]),
]
SKILLS = ["Discounted cash flow and comparables", "Scenario and sensitivity analysis",
          "Budgeting and variance reporting", "Credit and market risk basics",
          "Excel and VBA", "Python (pandas, NumPy)", "SQL", "Power BI and Bloomberg Terminal"]
CREDENTIALS = ["CFA Level III candidate", "FRM Part I", "B.Sc. Finance, University name"]
PROJECTS = [
    ("2025", "Rolling revenue forecast",
     "Replaced a quarterly spreadsheet process with a driver-based model that finance and sales both update.",
     "+18%", "forecast accuracy"),
    ("2024", "Vendor spend review",
     "Mapped three years of payables, flagged duplicate contracts and renegotiated the largest five suppliers.",
     "$2.4M", "annual savings"),
    ("2023", "Month-end close automation",
     "Scripted reconciliations and variance commentary in Python so the team reviews exceptions, not every line.",
     "-32%", "days to close"),
    ("2021", "Sector coverage initiation",
     "Built valuation models and wrote initiating reports for consumer and industrial names.",
     "11", "companies covered"),
]
MILESTONES = [(0, "2018", "Junior analyst at Northbridge Capital"),
              (2, "2020", "Moved into risk modelling during the downturn"),
              (4, "2022", "Promoted to senior analyst; passed CFA Level II"),
              (6, "2024", "Led the forecasting rebuild at Harbor Group"),
              (8, "2026", "Associate director, portfolio strategy")]
CHART = [.167, .229, .083, .3125, .417, .375, .625, .771, .958]  # 2018..2026, 0-1

# ------------------------------------------------------------------- STYLE
SALMON, SOFT, DEEP = HexColor("#FFA07A"), HexColor("#FFE6DC"), HexColor("#C9512C")
INK, G600, G300, G100 = HexColor("#2E3238"), HexColor("#5B616A"), HexColor("#D5D8DC"), HexColor("#F2F3F4")

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "downloads")


def load_fonts():
    names = {"Book": "Gotham-Book.ttf", "Medium": "Gotham-Medium.ttf", "Bold": "Gotham-Bold.ttf"}
    paths = {k: os.path.join(ROOT, "fonts", v) for k, v in names.items()}
    if all(os.path.exists(p) for p in paths.values()):
        for k, p in paths.items():
            pdfmetrics.registerFont(TTFont("Gotham-" + k, p))
        return "Gotham-Book", "Gotham-Medium", "Gotham-Bold"
    return "Helvetica", "Helvetica", "Helvetica-Bold"


BOOK, MED, BOLD = load_fonts()


def wrap(c, text, x, y, w, font, size, color, leading=None, align="left"):
    """Draw wrapped text; return the baseline for the next line."""
    leading = leading or size * 1.45
    c.setFont(font, size)
    c.setFillColor(color)
    for line in simpleSplit(text, font, size, w):
        if align == "center":
            c.drawCentredString(x + w / 2, y, line)
        else:
            c.drawString(x, y, line)
        y -= leading
    return y


def link(c, text, x, y, font, size, url, color):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, text)
    wd = pdfmetrics.stringWidth(text, font, size)
    c.setStrokeColor(color)
    c.setLineWidth(0.6)
    c.line(x, y - 2, x + wd, y - 2)
    c.linkURL(url, (x, y - 3, x + wd, y + size), relative=0)


# ---------------------------------------------------------------------- CV
def build_cv(path):
    W, H = A4
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle(f"{NAME} - CV")
    c.setAuthor(NAME)

    c.setFillColor(G100)
    c.rect(0, 0, 190, H, stroke=0, fill=1)
    c.setFillColor(SALMON)
    c.rect(0, H - 10, W, 10, stroke=0, fill=1)

    # Sidebar
    x, w, y = 24, 142, H - 72

    def head(title, y):
        c.setFont(BOLD, 10.5)
        c.setFillColor(INK)
        c.drawString(x, y, title)
        c.setFillColor(SALMON)
        c.rect(x, y - 8, 22, 2.5, stroke=0, fill=1)
        return y - 28

    y = head("Contact", y)
    for t in (EMAIL, PHONE, PLACE):
        y = wrap(c, t, x, y, w, BOOK, 9, INK, 13) - 4
    y = head("Links", y - 12)
    for label, url in LINKS:
        link(c, label, x, y, MED, 9.5, url, DEEP)
        y -= 18
    y = head("Skills", y - 10)
    for t in SKILLS:
        y = wrap(c, t, x, y, w, BOOK, 9, INK, 12.5) - 6
    y = head("Credentials", y - 8)
    for t in CREDENTIALS:
        y = wrap(c, t, x, y, w, BOOK, 9, INK, 12.5) - 6

    # Main column
    mx, mw = 222, W - 222 - 40
    c.setFont(BOLD, 30)
    c.setFillColor(INK)
    c.drawString(mx, H - 72, NAME)
    c.setFont(BOOK, 12.5)
    c.setFillColor(G600)
    c.drawString(mx, H - 94, ROLE)
    c.setFillColor(SALMON)
    c.rect(mx, H - 110, 40, 3, stroke=0, fill=1)

    def mhead(title, y):
        c.setFont(BOLD, 12)
        c.setFillColor(INK)
        c.drawString(mx, y, title)
        tw = pdfmetrics.stringWidth(title, BOLD, 12)
        c.setStrokeColor(G300)
        c.setLineWidth(1)
        c.line(mx + tw + 10, y + 4, mx + mw, y + 4)
        return y - 22

    y = mhead("Profile", H - 142)
    y = wrap(c, PROFILE, mx, y, mw, BOOK, 9.5, INK, 14.5) - 14

    y = mhead("Results", y)
    colw = mw / len(RESULTS)
    for i, (fig, label) in enumerate(RESULTS):
        cx = mx + i * colw
        c.setFont(BOLD, 17)
        c.setFillColor(DEEP)
        c.drawString(cx, y, fig)
        wrap(c, label, cx, y - 14, colw - 8, BOOK, 8.5, G600, 11)
    y -= 56

    y = mhead("Experience", y)
    for title, org, dates, bullets in EXPERIENCE:
        c.setFont(BOLD, 10.5)
        c.setFillColor(INK)
        c.drawString(mx, y, title)
        y -= 14
        c.setFont(MED, 9.5)
        c.setFillColor(G600)
        c.drawString(mx, y, org)
        c.setFont(BOOK, 9)
        c.drawRightString(mx + mw, y, dates)
        y -= 16
        for b in bullets:
            c.setFillColor(SALMON)
            c.rect(mx, y + 2.5, 3.5, 3.5, stroke=0, fill=1)
            y = wrap(c, b, mx + 11, y, mw - 11, BOOK, 9.2, INK, 12.8) - 3
        y -= 10

    c.showPage()
    c.save()


# ------------------------------------------------------------------- SLIDES
SW, SH = 960, 540


def chart_points(x0, x1, base, ht):
    n = len(CHART) - 1
    return [(x0 + i * (x1 - x0) / n, base + f * ht) for i, f in enumerate(CHART)]


def draw_line(c, pts, color, width):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.setLineJoin(1)
    c.setLineCap(1)
    c.drawPath(p, stroke=1, fill=0)


def slide_frame(c, title, n):
    c.setFillColor(white)
    c.rect(0, 0, SW, SH, stroke=0, fill=1)
    c.setFont(BOLD, 30)
    c.setFillColor(INK)
    c.drawString(60, SH - 80, title)
    c.setFillColor(SALMON)
    c.rect(60, SH - 98, 44, 3.5, stroke=0, fill=1)
    c.setFont(BOOK, 9)
    c.setFillColor(G600)
    c.drawString(60, 26, f"{NAME}  |  {ROLE}")
    c.drawRightString(SW - 60, 26, str(n))


def build_slides(path):
    c = canvas.Canvas(path, pagesize=(SW, SH))
    c.setTitle(f"{NAME} - Slides")
    c.setAuthor(NAME)

    # 1. Title
    c.setFillColor(SALMON)
    c.rect(0, 0, SW, SH, stroke=0, fill=1)
    pts = chart_points(520, 890, 90, 330)
    draw_line(c, pts, white, 6)
    c.setFillColor(SALMON)
    c.setStrokeColor(white)
    c.setLineWidth(4)
    for i in (0, 2, 4, 6, 8):
        c.circle(pts[i][0], pts[i][1], 7, stroke=1, fill=1)
    c.setFont(BOLD, 60)
    c.setFillColor(INK)
    c.drawString(64, 310, NAME)
    c.setFont(MED, 24)
    c.drawString(64, 268, ROLE)
    c.setFillColor(INK)
    c.rect(64, 244, 56, 4, stroke=0, fill=1)
    wrap(c, "Forecasting, valuation and risk modelling", 64, 214, 380, BOOK, 15, INK, 22)
    c.setFont(BOOK, 12)
    c.drawString(64, 64, EMAIL)
    c.showPage()

    # 2. About
    slide_frame(c, "About me", 2)
    wrap(c, PROFILE, 60, 400, 430, BOOK, 15, INK, 25)
    stats = [("8 years", "in finance and analysis"), ("+18%", "forecast accuracy at Harbor Group"),
             ("$2.4M", "annual vendor savings")]
    for i, (big, label) in enumerate(stats):
        yy = 400 - i * 100
        c.setStrokeColor(G300)
        c.setLineWidth(1)
        c.line(560, yy + 38, 900, yy + 38)
        c.setFont(BOLD, 40)
        c.setFillColor(INK)
        c.drawString(560, yy - 6, big)
        c.setFont(BOOK, 12)
        c.setFillColor(G600)
        c.drawString(560, yy - 28, label)
    c.showPage()

    # 3. Career chart
    slide_frame(c, "Career so far", 3)
    x0, x1, base, ht = 90, 870, 215, 190
    pts = chart_points(x0, x1, base, ht)
    c.setStrokeColor(G300)
    c.setLineWidth(0.8)
    for k in range(5):
        c.line(x0 - 20, base + k * ht / 4, x1 + 20, base + k * ht / 4)
    p = c.beginPath()
    p.moveTo(pts[0][0], base)
    for pt in pts:
        p.lineTo(*pt)
    p.lineTo(pts[-1][0], base)
    p.close()
    c.setFillColor(SOFT)
    c.drawPath(p, stroke=0, fill=1)
    draw_line(c, pts, DEEP, 3.5)
    c.setFillColor(white)
    c.setStrokeColor(DEEP)
    c.setLineWidth(3)
    for i, _, _ in MILESTONES:
        c.circle(pts[i][0], pts[i][1], 6, stroke=1, fill=1)
    c.setFont(BOOK, 10)
    c.setFillColor(G600)
    for i, year in enumerate(range(2018, 2027)):
        c.drawCentredString(pts[i][0], base - 18, str(year))
    for i, year, text in MILESTONES:
        cx = pts[i][0]
        c.setFont(BOLD, 13)
        c.setFillColor(INK)
        c.drawCentredString(cx, base - 52, year)
        wrap(c, text, cx - 70, base - 70, 140, BOOK, 10.5, G600, 14, align="center")
    c.showPage()

    # 4. Selected work
    slide_frame(c, "Selected work", 4)
    top = 430
    c.setStrokeColor(INK)
    c.setLineWidth(1.5)
    c.line(60, top, 900, top)
    for i, (year, title, desc, fig, label) in enumerate(PROJECTS):
        yt = top - i * 82
        c.setFont(BOOK, 12)
        c.setFillColor(G600)
        c.drawString(60, yt - 30, year)
        c.setFont(BOLD, 18)
        c.setFillColor(INK)
        c.drawString(140, yt - 30, title)
        wrap(c, desc, 140, yt - 50, 440, BOOK, 11, G600, 14)
        c.setFont(BOLD, 28)
        c.setFillColor(INK)
        c.drawString(690, yt - 36, fig)
        c.setFont(BOOK, 11)
        c.setFillColor(G600)
        c.drawString(690, yt - 54, label)
        c.setStrokeColor(G300)
        c.setLineWidth(1)
        c.line(60, yt - 82, 900, yt - 82)
    c.showPage()

    # 5. Skills and credentials
    slide_frame(c, "Skills and credentials", 5)
    cols = [("Analysis", SKILLS[:4]), ("Tools", SKILLS[4:]), ("Credentials", CREDENTIALS)]
    for i, (head, items) in enumerate(cols):
        cx = 60 + i * 290
        c.setFont(BOLD, 18)
        c.setFillColor(INK)
        c.drawString(cx, 396, head)
        c.setStrokeColor(INK)
        c.setLineWidth(1.5)
        c.line(cx, 384, cx + 250, 384)
        for j, t in enumerate(items):
            yy = 358 - j * 40
            c.setFont(BOOK, 13)
            c.setFillColor(INK)
            c.drawString(cx, yy, t)
            c.setStrokeColor(G300)
            c.setLineWidth(1)
            c.line(cx, yy - 12, cx + 250, yy - 12)
    c.showPage()

    # 6. Contact
    c.setFillColor(INK)
    c.rect(0, 0, SW, SH, stroke=0, fill=1)
    c.setFillColor(SALMON)
    c.rect(0, 0, 18, SH, stroke=0, fill=1)
    c.setFont(BOLD, 54)
    c.setFillColor(white)
    c.drawString(80, 340, "Let's talk")
    c.setFont(BOOK, 18)
    c.setFillColor(G300)
    c.drawString(80, 300, "Open to analyst and associate roles.")
    c.setFont(MED, 17)
    c.setFillColor(SALMON)
    c.drawString(80, 230, EMAIL)
    for i, (label, url) in enumerate(LINKS):
        link(c, label, 80, 196 - i * 30, MED, 17, url, SALMON)
    c.showPage()
    c.save()


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build_cv(os.path.join(OUT, "Thyme-Inn-CV.pdf"))
    build_slides(os.path.join(OUT, "Thyme-Inn-Slides.pdf"))
    print("Built downloads/Thyme-Inn-CV.pdf and downloads/Thyme-Inn-Slides.pdf")

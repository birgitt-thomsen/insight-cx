"""
Builds presentation/InsightCX_MVP.pptx per presentation/SLIDES.md's
"Build & delivery specification".

Run with the project venv:
    ../.venv/Scripts/python.exe build_deck.py
(from inside insight-cx/presentation/)
"""
import os
import sqlite3

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT_PATH = os.path.join(HERE, "InsightCX_MVP.pptx")
DB_PATH = os.path.join(HERE, "..", "backend", "data", "insightcx.db")

# ---------------------------------------------------------------------------
# Palette
#   The "dark" indigo/teal used throughout the deck (headline emphasis,
#   banners, table headers) are set to the EXACT hex values from the real
#   logo file (frontend/src/assets/brand/insightcx-logo-full.svg:
#   #2E2A6E / #0F5C56) so the deck's colors match the product's brand mark
#   precisely, not an approximated Tailwind shade.
#   Lighter/mid accent tones (arrows, pills, tinted card backgrounds) stay
#   on the standard Tailwind indigo/teal scale (confirmed unmodified in
#   frontend/src/index.css - no @theme color overrides), matching
#   frontend/DESIGN.md's broader indigo/teal visual language.
# ---------------------------------------------------------------------------
BG = RGBColor(0xF4, 0xF4, 0xF5)            # light neutral grey, complements indigo/teal
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INDIGO_DARK = RGBColor(0x2E, 0x2A, 0x6E)   # logo "Insight" glyph fill
TEAL_DARK = RGBColor(0x0F, 0x5C, 0x56)     # logo "CX" badge fill
INDIGO_ACCENT = RGBColor(0x4F, 0x46, 0xE5) # indigo-600
TEAL_ACCENT = RGBColor(0x0D, 0x94, 0x88)   # teal-600
INDIGO_LIGHT = RGBColor(0xE0, 0xE7, 0xFF)  # indigo-100
TEAL_LIGHT = RGBColor(0xE7, 0xF8, 0xF4)    # muted pale teal (softer than teal-100)
SLATE_900 = RGBColor(0x0F, 0x17, 0x2A)
SLATE_800 = RGBColor(0x1E, 0x29, 0x3B)
SLATE_600 = RGBColor(0x47, 0x55, 0x69)
SLATE_500 = RGBColor(0x64, 0x74, 0x8B)
SLATE_400 = RGBColor(0x94, 0xA3, 0xB8)
SLATE_200 = RGBColor(0xE2, 0xE8, 0xF0)
SLATE_100 = RGBColor(0xF1, 0xF5, 0xF9)
GREEN = RGBColor(0x16, 0xA3, 0x4A)
RED = RGBColor(0xDC, 0x26, 0x26)
AMBER = RGBColor(0xD9, 0x77, 0x06)

HEAD_FONT = "Roboto"
BODY_FONT = "Open Sans"

SLIDE_W = 13.333
SLIDE_H = 7.5
MARGIN = 0.5
CONTENT_W = SLIDE_W - 2 * MARGIN
CONTENT_X = MARGIN
CONTENT_TOP = 1.62
CONTENT_BOTTOM = 7.05

_ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
_ARIAL = r"C:\Windows\Fonts\arial.ttf"


def text_width_in(text, size_pt, bold=True):
    font = ImageFont.truetype(_ARIAL_BOLD if bold else _ARIAL, size_pt)
    bbox = font.getbbox(text)
    return (bbox[2] - bbox[0]) / 72.0


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def new_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG
    return slide


def set_tracking(run, val=150):
    rPr = run._r.get_or_add_rPr()
    rPr.set("spc", str(val))


def add_rect(slide, x, y, w, h, fill=WHITE, line=None, line_w=0.75, radius=0.08):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    try:
        shp.adjustments[0] = radius
    except IndexError:
        pass
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp


def add_oval(slide, x, y, d, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
    shp.shadow.inherit = False
    return shp


def style_run(r, size=14, color=SLATE_800, bold=False, italic=False, font=BODY_FONT, tracking=None):
    f = r.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = font
    f.color.rgb = color
    if tracking:
        set_tracking(r, tracking)


def add_text(slide, x, y, w, h, text, size=14, color=SLATE_800, bold=False, italic=False,
             font=BODY_FONT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.05,
             tracking=None, wrap=True):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        style_run(r, size, color, bold, italic, font, tracking)
    return box


def add_card(slide, x, y, w, h, title, desc=None, fill=WHITE, border=SLATE_200,
             title_size=15, title_color=SLATE_900, desc_size=11.5, desc_color=SLATE_600,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, pad=0.18, radius=0.08,
             subtitle=None, subtitle_size=12, subtitle_color=SLATE_800):
    shp = add_rect(slide, x, y, w, h, fill=fill, line=border, line_w=0.75, radius=radius)
    tf = shp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(pad)
    tf.margin_top = tf.margin_bottom = Inches(pad * 0.7)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = title
    style_run(r, title_size, title_color, True, False, HEAD_FONT)
    if subtitle:
        ps = tf.add_paragraph()
        ps.alignment = align
        ps.space_before = Pt(3)
        rs = ps.add_run()
        rs.text = subtitle
        style_run(rs, subtitle_size, subtitle_color, True, False, BODY_FONT)
    if desc:
        p2 = tf.add_paragraph()
        p2.alignment = align
        p2.space_before = Pt(4)
        p2.line_spacing = 1.08
        r2 = p2.add_run()
        r2.text = desc
        style_run(r2, desc_size, desc_color, False, False, BODY_FONT)
    return shp


def add_pill(slide, x, y, w, h, text, fill=TEAL_LIGHT, text_color=TEAL_DARK, size=11.5, bold=True,
             font=BODY_FONT, radius=0.5, border=None):
    shp = add_rect(slide, x, y, w, h, fill=fill, line=border, line_w=0.75, radius=radius)
    tf = shp.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.06)
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    style_run(r, size, text_color, bold, False, font)
    return shp


def add_arrow(slide, x, y, w, h, direction="right", color=TEAL_DARK):
    """A solid chevron ('>') connector, always in the logo's dark teal."""
    if direction == "right":
        shp = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(y), Inches(w), Inches(h))
    else:
        cx, cy = x + w / 2, y + h / 2
        shp = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(cx - h / 2), Inches(cy - w / 2),
                                      Inches(h), Inches(w))
        shp.rotation = 90
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def add_flow_horizontal(slide, items, x, y, w, h, card_fill=WHITE, border=SLATE_200,
                         text_color=SLATE_800, arrow_color=TEAL_DARK, font_size=11,
                         bold=False, arrow_w=0.28, anchor=MSO_ANCHOR.MIDDLE, radius=0.1):
    n = len(items)
    card_w = (w - (n - 1) * arrow_w) / n
    cx = x
    for i, label in enumerate(items):
        shp = add_card(slide, cx, y, card_w, h, label, fill=card_fill, border=border,
                        title_size=font_size, title_color=text_color, align=PP_ALIGN.CENTER,
                        anchor=anchor, pad=0.1, radius=radius)
        shp.text_frame.paragraphs[0].runs[0].font.bold = bold
        cx += card_w
        if i < n - 1:
            ay = y + h / 2 - (h * 0.28) / 2
            add_arrow(slide, cx, ay, arrow_w, h * 0.28, "right", arrow_color)
            cx += arrow_w


def add_down_arrow(slide, center_x, y, w=0.55, h=0.4, color=TEAL_DARK):
    add_arrow(slide, center_x - w / 2, y, w, h, "down", color)


def add_badge(slide, x, y, d, num, fill=INDIGO_ACCENT, text_color=WHITE, size=14):
    shp = add_oval(slide, x, y, d, fill)
    tf = shp.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = str(num)
    style_run(r, size, text_color, True, False, HEAD_FONT)
    return shp


def add_picture_framed(slide, path, frame_x, frame_y, frame_w, frame_h, pad=0.14,
                        frame_fill=WHITE, frame_border=SLATE_200, radius=0.06):
    if not os.path.exists(path):
        print(f"WARNING: asset not found, skipping visual element: {path}")
        return None
    add_rect(slide, frame_x, frame_y, frame_w, frame_h, fill=frame_fill, line=frame_border,
             line_w=0.75, radius=radius)
    im = Image.open(path)
    aspect = im.width / im.height
    avail_w = frame_w - 2 * pad
    avail_h = frame_h - 2 * pad
    if avail_w / aspect <= avail_h:
        img_w = avail_w
        img_h = avail_w / aspect
    else:
        img_h = avail_h
        img_w = avail_h * aspect
    img_x = frame_x + (frame_w - img_w) / 2
    img_y = frame_y + (frame_h - img_h) / 2
    slide.shapes.add_picture(path, Inches(img_x), Inches(img_y), width=Inches(img_w), height=Inches(img_h))
    return frame_y + frame_h


def frame_size_for_width(path, frame_w, pad=0.14):
    """Given a target frame width, returns (frame_w, frame_h) sized so the
    image (at that width, minus padding) fills the frame with no dead
    space — instead of picking an arbitrary frame height and letting the
    image float inside it."""
    im = Image.open(path)
    aspect = im.width / im.height
    img_h = (frame_w - 2 * pad) / aspect
    return frame_w, img_h + 2 * pad


def frame_size_for_height(path, frame_h, pad=0.14):
    """Mirror of frame_size_for_width, driven by a target height instead —
    for narrower snippets where matching a row height matters more than
    matching a row width."""
    im = Image.open(path)
    aspect = im.width / im.height
    img_w = (frame_h - 2 * pad) * aspect
    return img_w + 2 * pad, frame_h


WORDMARK_PATH = os.path.join(ASSETS, "insightcx_wordmark.png")
_wordmark_im = Image.open(WORDMARK_PATH)
WORDMARK_ASPECT = _wordmark_im.width / _wordmark_im.height


def add_logo_image(slide, center_x, y, width=5.0):
    """Places the real InsightCX wordmark (rasterized from
    frontend/src/assets/brand/insightcx-logo-full.svg) plus the tagline
    beneath it, centered on center_x."""
    height = width / WORDMARK_ASPECT
    x = center_x - width / 2
    slide.shapes.add_picture(WORDMARK_PATH, Inches(x), Inches(y), width=Inches(width), height=Inches(height))

    tagline_y = y + height + width * 0.03
    tagline_size = max(11, width * 2.6)
    add_text(slide, center_x - 3, tagline_y, 6, tagline_size / 72 * 1.4, "Every Voice. Every Insight.",
              size=tagline_size, color=TEAL_DARK, bold=True, font=BODY_FONT,
              align=PP_ALIGN.CENTER, tracking=100)
    return tagline_y + tagline_size / 72 * 1.4


def add_header(slide, kicker, title, subtitle=None, title_size=29):
    """Draws the kicker/title/(optional subtitle) block and returns the y
    coordinate immediately below it, so callers can position content
    without risking overlap when the subtitle wraps to two lines."""
    y = 0.42
    add_text(slide, MARGIN, y, CONTENT_W, 0.3, kicker.upper(), size=12.5, color=TEAL_ACCENT,
              bold=True, font=BODY_FONT, tracking=170)
    y += 0.34
    title_h = 0.92 if len(title) > 55 else 0.5
    add_text(slide, MARGIN, y, CONTENT_W, title_h, title, size=title_size, color=SLATE_900,
              bold=True, font=HEAD_FONT, line_spacing=1.05)
    bottom = y + title_h
    if subtitle:
        sub_size = 13.5
        text_w = text_width_in(subtitle, sub_size, bold=False)
        n_lines = max(1, -(-int(text_w * 100) // int(CONTENT_W * 100)))
        sub_h = n_lines * (sub_size * 1.15 / 72) + 0.08
        add_text(slide, MARGIN, bottom + 0.08, CONTENT_W, sub_h, subtitle, size=sub_size,
                  color=SLATE_600, italic=True, font=BODY_FONT)
        bottom = bottom + 0.08 + sub_h
    return bottom + 0.16


def add_footer(slide, page_num):
    add_text(slide, MARGIN, 7.18, 3, 0.25, "InsightCX", size=9, color=SLATE_400, bold=True, font=HEAD_FONT)
    add_text(slide, SLIDE_W - MARGIN - 1, 7.18, 1, 0.25, str(page_num), size=9, color=SLATE_400,
              font=BODY_FONT, align=PP_ALIGN.RIGHT)


def add_table(slide, x, y, w, headers, rows, col_widths=None, header_fill=INDIGO_DARK,
              header_text=WHITE, row_h=0.34, font_size=11.5, header_font_size=11.5,
              zebra=SLATE_100):
    n_rows = len(rows) + 1
    n_cols = len(headers)
    total_h = row_h * n_rows
    gshape = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(total_h))
    table = gshape.table
    if col_widths:
        for i, cw in enumerate(col_widths):
            table.columns[i].width = Inches(cw)
    for c, htext in enumerate(headers):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_fill
        cell.margin_left = cell.margin_right = Inches(0.08)
        cell.margin_top = cell.margin_bottom = Inches(0.03)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
        r = p.add_run()
        r.text = htext
        style_run(r, header_font_size, header_text, True, False, HEAD_FONT)
    for ri, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(ri + 1, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = zebra if ri % 2 == 1 else WHITE
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = str(val)
            style_run(r, font_size, SLATE_800, c == 0, False, BODY_FONT)
    return table, total_h


# ---------------------------------------------------------------------------
# Benchmark data (real values from backend/data/insightcx.db;
# consistency_score is NULL for every run, so it's marked as a placeholder)
# ---------------------------------------------------------------------------

def load_benchmark_stats():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    rows = cur.execute(
        "SELECT model, average_latency_ms, total_tokens, feedback_count, estimated_cost "
        "FROM benchmark_runs WHERE feedback_count = 25 ORDER BY id"
    ).fetchall()
    con.close()
    stats = []
    for model, latency, tokens, count, cost in rows:
        stats.append({
            "model": model,
            "latency": round(latency),
            "tokens_per_record": round(tokens / count),
            "cost_per_record": cost / count,
            "count": count,
        })
    return stats


# ---------------------------------------------------------------------------
# Slides
# ---------------------------------------------------------------------------

def slide_01_title(prs):
    slide = new_slide(prs)
    add_logo_image(slide, SLIDE_W / 2, 1.95, width=4.8)

    add_text(slide, SLIDE_W / 2 - 5, 3.75, 10, 0.5, "AI-powered Voice of Customer analytics",
              size=20, color=SLATE_600, bold=False, font=BODY_FONT,
              align=PP_ALIGN.CENTER)

    add_text(slide, SLIDE_W / 2 - 4.5, 4.35, 9, 0.6,
              "Transforming customer feedback into structured insight and actionable business intelligence.",
              size=13, color=SLATE_500, italic=True, font=BODY_FONT, align=PP_ALIGN.CENTER)

    flow_w = 8.6
    add_flow_horizontal(slide, ["Customer Feedback", "AI Analysis", "Actionable Insight"],
                         SLIDE_W / 2 - flow_w / 2, 5.25, flow_w, 0.85,
                         card_fill=WHITE, border=SLATE_200, text_color=INDIGO_DARK,
                         font_size=13.5, bold=True, arrow_w=0.4)


def slide_02_agenda(prs):
    slide = new_slide(prs)
    add_header(slide, "Agenda", "What we'll cover")

    items = [
        "The Problem",
        "The Business Scenario",
        "InsightCX Overview",
        "LLM Capability 1 — Structuring Feedback",
        "LLM Capability 2 — Executive Insight",
        "The Dashboard",
        "From AI Output to Business Decision",
        "AI Evaluation",
        "Lessons Learned — What It Took to Build",
        "What's Next — Beyond the MVP",
        "Live Demo",
    ]
    col_w = (CONTENT_W - 0.5) / 2
    col1_x = CONTENT_X
    col2_x = CONTENT_X + col_w + 0.5
    row_h = 0.75
    start_y = 2.0

    for i, label in enumerate(items):
        col, row = (0, i) if i < 6 else (1, i - 6)
        x = col1_x if col == 0 else col2_x
        y = start_y + row * row_h
        num = i + 1
        color = INDIGO_ACCENT if num % 2 else TEAL_ACCENT
        add_badge(slide, x, y, 0.36, num, fill=color, size=13)
        add_text(slide, x + 0.54, y, col_w - 0.54, 0.36, label, size=15, color=SLATE_800,
                  bold=True, font=HEAD_FONT, anchor=MSO_ANCHOR.MIDDLE)

    add_footer(slide, 2)


def slide_03_problem(prs):
    slide = new_slide(prs)
    add_header(slide, "The Problem", "Customer feedback contains the answers \u2014 but they're buried in text.")

    quotes = [
        "\u201cThe sofa is beautiful, but delivery was two days late.\u201d",
        "\u201cThe assembly instructions were impossible to follow.\u201d",
        "\u201cReturning the table was surprisingly easy.\u201d",
        "\u201cI couldn't find any information about my order.\u201d",
    ]
    gx, gy, gw, gh = CONTENT_X, 2.05, CONTENT_W, 2.0
    cw = (gw - 0.26) / 2
    ch = (gh - 0.22) / 2
    for i, q in enumerate(quotes):
        cx = gx + (i % 2) * (cw + 0.26)
        cy = gy + (i // 2) * (ch + 0.22)
        add_card(slide, cx, cy, cw, ch, q, fill=TEAL_LIGHT, border=TEAL_ACCENT, title_size=13,
                  title_color=TEAL_DARK, anchor=MSO_ANCHOR.MIDDLE, pad=0.28)

    flow_y = gy + gh + 0.28
    add_flow_horizontal(
        slide,
        ["Hundreds of\ncomments", "Unstructured\ncustomer language", "Manual\nanalysis",
         "Slow / inconsistent\ninsight", "Missed\nopportunities"],
        CONTENT_X, flow_y, CONTENT_W, 1.05, card_fill=WHITE, border=SLATE_200,
        text_color=SLATE_800, font_size=11.5, bold=True, arrow_w=0.28,
    )

    banner_y = flow_y + 1.05 + 0.3
    banner = add_rect(slide, CONTENT_X, banner_y, CONTENT_W, 0.82, fill=INDIGO_DARK, radius=0.12)
    tf = banner.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.3)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Can an LLM turn that unstructured customer voice into something we can actually analyze?"
    style_run(r, 16, WHITE, True, True, HEAD_FONT)

    add_footer(slide, 3)


def slide_04_scenario(prs):
    slide = new_slide(prs)
    add_header(slide, "The Business Scenario", "A home-furnishing retailer with hundreds of customer voices")

    journey_y = 1.85
    add_flow_horizontal(
        slide, ["Discover", "Purchase", "Delivery", "Assembly", "Use"],
        CONTENT_X, journey_y, CONTENT_W, 0.75, card_fill=INDIGO_LIGHT, border=None,
        text_color=INDIGO_DARK, arrow_color=INDIGO_DARK, font_size=12, bold=True, arrow_w=0.22,
    )

    body_y = journey_y + 0.75 + 0.4
    left_w = 3.85
    add_text(slide, CONTENT_X, body_y, left_w, 0.3, "Feedback sources", size=13, color=SLATE_900,
              bold=True, font=HEAD_FONT)
    sources = [
        ("NPS", "Recommendation / loyalty feedback",
         "Measures likelihood to recommend on a 0\u201310 scale, indicating overall "
         "customer loyalty and advocacy."),
        ("CSAT", "Customer satisfaction feedback",
         "Measures satisfaction with a specific experience on a 1\u20135 scale, helping "
         "identify how well the customer\u2019s expectations were met."),
    ]
    card_h = 1.55
    for i, (t, sub, d) in enumerate(sources):
        cy = body_y + 0.38 + i * (card_h + 0.2)
        add_card(slide, CONTENT_X, cy, left_w, card_h, t, d, subtitle=sub, fill=WHITE,
                  border=SLATE_200, title_size=14.5, desc_size=11, anchor=MSO_ANCHOR.MIDDLE)

    right_x = CONTENT_X + left_w + 0.45
    right_w = CONTENT_W - left_w - 0.45
    add_text(slide, right_x, body_y, right_w, 0.3, "Test dataset", size=13, color=SLATE_900,
              bold=True, font=HEAD_FONT)

    stats = ["Several hundred feedback records across multiple weeks", "NPS + CSAT",
              "Positive \u00b7 Neutral \u00b7\nNegative"]
    chip_w = (right_w - 2 * 0.15) / 3
    chip_h = 1.05
    cy = body_y + 0.38
    for i, s in enumerate(stats):
        cx = right_x + i * (chip_w + 0.15)
        add_card(slide, cx, cy, chip_w, chip_h, s, fill=TEAL_LIGHT, border=TEAL_ACCENT, title_size=11,
                  title_color=TEAL_DARK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    theme_y = cy + chip_h + 0.28
    add_text(slide, right_x, theme_y, right_w, 0.28, "Key CX themes", size=12, color=SLATE_900,
              bold=True, font=HEAD_FONT)
    themes = ["Delivery", "Product quality & assembly", "Returns", "Website experience",
              "Payment / billing", "Brand loyalty"]
    prow_y = theme_y + 0.36
    pill_w = (right_w - 2 * 0.15) / 3
    pill_h = 0.5
    for i, th in enumerate(themes):
        r_i, c_i = divmod(i, 3)
        px = right_x + c_i * (pill_w + 0.15)
        py = prow_y + r_i * (pill_h + 0.15)
        add_pill(slide, px, py, pill_w, pill_h, th, fill=INDIGO_LIGHT, text_color=INDIGO_DARK,
                  size=10.5, radius=0.25)

    note_y = prow_y + 2 * pill_h + 0.15 + 0.2
    add_text(slide, right_x, note_y, right_w, 0.4,
              "A controlled scenario for testing AI functionality \u2014 not production data.",
              size=10.5, color=SLATE_500, italic=True, font=BODY_FONT)

    add_footer(slide, 4)


def slide_05_overview(prs):
    slide = new_slide(prs)
    add_header(slide, "InsightCX Overview", "From customer voice to business insight")

    flow_y = CONTENT_TOP + 0.15
    steps = ["Customer\nFeedback", "CSV\nImport", "Feedback\nData", "LLM\nAnalysis",
             "Structured\nCX Data", "Dashboard +\nExec Insights", "Business\nDecisions"]
    add_flow_horizontal(slide, steps, CONTENT_X, flow_y, CONTENT_W, 0.95, card_fill=WHITE,
                         border=SLATE_200, text_color=SLATE_800,
                         font_size=10.3, bold=True, arrow_w=0.2)

    branch_x = CONTENT_X + CONTENT_W * 0.5
    down_y = flow_y + 0.95 + 0.06
    add_down_arrow(slide, branch_x, down_y, w=0.45, h=0.3)

    eval_y = down_y + 0.3 + 0.06
    eval_w = 6.0
    add_card(slide, CONTENT_X + (CONTENT_W - eval_w) / 2, eval_y, eval_w, 0.85, "AI Evaluation",
              "Model quality / consistency \u00b7 latency \u00b7 tokens \u00b7 cost", fill=TEAL_LIGHT,
              border=TEAL_ACCENT, title_color=TEAL_DARK, title_size=15, align=PP_ALIGN.CENTER,
              anchor=MSO_ANCHOR.MIDDLE)

    stages_y = eval_y + 0.85 + 0.32
    stages = [
        ("1", "Ingest", "Customer feedback flows in via CSV import."),
        ("2", "Analyze", "An LLM converts each comment into structured CX attributes."),
        ("3", "Aggregate", "Results roll up into dashboards and executive-level insights."),
    ]
    sw = (CONTENT_W - 2 * 0.3) / 3
    sh = 1.15
    for i, (num, t, d) in enumerate(stages):
        sx = CONTENT_X + i * (sw + 0.3)
        add_card(slide, sx, stages_y, sw, sh, t, d, fill=WHITE, border=SLATE_200, title_size=13.5,
                  desc_size=10.5)
        add_badge(slide, sx + 0.14, stages_y - 0.16, 0.32, num, fill=INDIGO_ACCENT, size=12)

    add_footer(slide, 5)


def slide_06_feature1(prs):
    slide = new_slide(prs)
    add_header(slide, "LLM Capability 1 of 2", "Turning customer language into structured CX data")

    left_x, left_w = CONTENT_X, 5.55
    add_pill(slide, left_x, CONTENT_TOP, 2.0, 0.35, "NATURAL LANGUAGE", fill=INDIGO_LIGHT,
              text_color=INDIGO_DARK, size=10.5, radius=0.5)

    quote_y = CONTENT_TOP + 0.5
    add_card(slide, left_x, quote_y, left_w, 1.9,
              "\u201cThe area rug showed up two days late with no explanation. Customer service was "
              "helpful when I asked about the delay, but I would\u2019ve liked to know what was going "
              "on without having to contact them.\u201d",
              fill=WHITE, border=SLATE_200, title_size=13.5, title_color=SLATE_800,
              anchor=MSO_ANCHOR.MIDDLE, pad=0.3)

    banner_y = quote_y + 1.9 + 0.3
    banner = add_rect(slide, left_x, banner_y, left_w, 1.15, fill=INDIGO_DARK, radius=0.1)
    tf = banner.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.22)
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Once the LLM output is structured, it stops being just text and becomes data the application can work with."
    style_run(r, 13.5, WHITE, True, True, HEAD_FONT)

    note_y = banner_y + 1.15 + 0.22
    add_text(slide, left_x, note_y, left_w, 0.7,
              "Customers describe the same experience in many different ways \u2014 the application needs consistent categories for analysis.",
              size=11, color=SLATE_600, italic=True, font=BODY_FONT)

    arrow_x = left_x + left_w + 0.15
    arrow_w = 0.75
    add_text(slide, arrow_x - 0.4, CONTENT_TOP + 1.9, arrow_w + 0.8, 0.6,
              "Natural\nlanguage \u2192\nstructured\ndata", size=9.5, color=TEAL_DARK, bold=True,
              align=PP_ALIGN.CENTER, font=BODY_FONT, line_spacing=1.0)
    add_arrow(slide, arrow_x, CONTENT_TOP + 2.55, arrow_w, 0.55, "right")

    right_x = arrow_x + arrow_w + 0.35
    right_w = SLIDE_W - MARGIN - right_x
    add_pill(slide, right_x, CONTENT_TOP, 2.4, 0.35, "STRUCTURED OUTPUT", fill=TEAL_LIGHT,
              text_color=TEAL_DARK, size=10.5, radius=0.5, border=TEAL_ACCENT)

    frame_y = CONTENT_TOP + 0.5
    frame_h = 4.55
    bottom = add_picture_framed(slide, os.path.join(ASSETS, "feedback_detail.png"), right_x,
                                  frame_y, right_w, frame_h)
    if bottom:
        add_text(slide, right_x, bottom + 0.06, right_w, 0.3, "Feedback Explorer \u2014 AI Assessment",
                  size=10, color=SLATE_500, italic=True, align=PP_ALIGN.CENTER, font=BODY_FONT)

    add_footer(slide, 6)


def slide_07_feature2(prs):
    slide = new_slide(prs)
    content_top = add_header(
        slide, "LLM Capability 2 of 2", "From individual comments to executive insight",
        subtitle="Feature 1: what is this customer saying?    \u2192    Feature 2: what does everything mean for the business?")

    table_y = content_top + 0.08
    headers = ["Feedback Analysis", "Executive Insights"]
    rows = [
        ("Individual comment", "Aggregated feedback"),
        ("What happened?", "What does it mean?"),
        ("Sentiment", "Customer health"),
        ("Themes", "Business impact"),
        ("Priority", "Leadership priorities"),
        ("Summary", "Recommended actions"),
    ]
    table_w = 5.6
    table, table_h = add_table(slide, CONTENT_X, table_y, table_w, headers, rows,
                                 col_widths=[table_w / 2, table_w / 2], row_h=0.34, font_size=11,
                                 header_font_size=12)
    table.cell(0, 1).fill.fore_color.rgb = TEAL_DARK

    right_x = CONTENT_X + table_w + 0.35
    right_w = SLIDE_W - MARGIN - right_x
    add_text(slide, right_x, table_y, right_w, 0.3, "Executive Insight \u2014 Leadership Priority",
              size=11.5, color=SLATE_900, bold=True, font=HEAD_FONT)
    # Snug-fit the screenshot's frame to its own aspect ratio (at the
    # available column width) instead of stretching it to match the
    # table's height, so there's no dead space above the image.
    lp_path = os.path.join(ASSETS, "leadership_priorities.png")
    lp_frame_w, lp_frame_h = frame_size_for_width(lp_path, right_w, pad=0.14)
    add_picture_framed(slide, lp_path, right_x, table_y + 0.36, lp_frame_w, lp_frame_h, pad=0.14)

    flow_y = table_y + table_h + 0.35
    add_flow_horizontal(
        slide, ["Hundreds of\ncustomer comments", "Patterns across\nfeedback",
                "Business\ninterpretation", "Recommended\naction"],
        CONTENT_X, flow_y, CONTENT_W, 0.9, card_fill=WHITE, border=SLATE_200, text_color=SLATE_800,
        font_size=11.5, bold=True, arrow_w=0.3,
    )

    callout_y = flow_y + 0.9 + 0.28
    callout_w = (CONTENT_W - 0.3) / 2
    add_card(slide, CONTENT_X, callout_y, callout_w, 0.95,
              "\u201cDelivery reliability is emerging as a significant driver of customer dissatisfaction.\u201d",
              fill=INDIGO_LIGHT, border=None, title_size=12, title_color=INDIGO_DARK,
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    add_card(slide, CONTENT_X + callout_w + 0.3, callout_y, callout_w, 0.95,
              "\u201cLeadership priority: investigate delivery reliability and communication around delays.\u201d",
              fill=TEAL_LIGHT, border=TEAL_ACCENT, title_size=12, title_color=TEAL_DARK,
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    add_footer(slide, 7)


def slide_08_dashboard(prs):
    slide = new_slide(prs)
    add_header(slide, "The Dashboard", "Making customer health visible")

    legend_x = CONTENT_X
    legend_w = 0.42

    key_metrics_path = os.path.join(ASSETS, "key_metrics.png")
    sentiment_path = os.path.join(ASSETS, "sentiment_metrics.png")
    main_driver1_path = os.path.join(ASSETS, "main_driver_1.png")
    main_driver2_path = os.path.join(ASSETS, "main_driver_2.png")

    y1 = CONTENT_TOP
    frame1_w, frame1_h = frame_size_for_width(key_metrics_path, 6.6, pad=0.16)
    add_badge(slide, legend_x, y1 + frame1_h / 2 - 0.16, 0.32, 1, fill=INDIGO_ACCENT)
    add_picture_framed(slide, key_metrics_path, legend_x + legend_w, y1, frame1_w, frame1_h, pad=0.16)
    add_text(slide, legend_x + legend_w, y1 + frame1_h + 0.06, 6, 0.3,
              "Customer health, NPS & CSAT at a glance", size=10.5, color=SLATE_500, italic=True,
              font=BODY_FONT)

    y2 = y1 + frame1_h + 0.42
    frame2_w, frame2_h = frame_size_for_width(sentiment_path, 3.6, pad=0.16)
    add_badge(slide, legend_x, y2 + frame2_h / 2 - 0.16, 0.32, 2, fill=TEAL_ACCENT)
    add_picture_framed(slide, sentiment_path, legend_x + legend_w, y2, frame2_w, frame2_h, pad=0.16)
    add_text(slide, legend_x + legend_w, y2 + frame2_h + 0.06, 6, 0.3, "Sentiment breakdown",
              size=10.5, color=SLATE_500, italic=True, font=BODY_FONT)

    y3 = y2 + frame2_h + 0.42
    driver1_w, driver1_h = frame_size_for_height(main_driver1_path, 1.6, pad=0.16)
    driver2_w, driver2_h = frame_size_for_height(main_driver2_path, 1.6, pad=0.16)
    add_badge(slide, legend_x, y3 + driver1_h / 2 - 0.16, 0.32, 3, fill=INDIGO_ACCENT)
    add_picture_framed(slide, main_driver1_path, legend_x + legend_w, y3, driver1_w, driver1_h, pad=0.16)
    driver2_x = legend_x + legend_w + driver1_w + 0.3
    add_picture_framed(slide, main_driver2_path, driver2_x, y3, driver2_w, driver2_h, pad=0.16)
    drivers_bottom = y3 + max(driver1_h, driver2_h)
    add_text(slide, legend_x + legend_w, drivers_bottom + 0.06, driver1_w + 0.3 + driver2_w, 0.35,
              "Two of several business drivers surfaced from structured feedback — ranked by "
              "impact and evidence-backed.",
              size=10.5, color=SLATE_500, italic=True, font=BODY_FONT)

    add_footer(slide, 8)


def slide_09_decision(prs):
    slide = new_slide(prs)
    add_header(slide, "From AI Output to Business Decision", "From customer voice to action")

    flow1_y = CONTENT_TOP + 0.1
    add_flow_horizontal(
        slide, ["Customer\nvoice", "Structured AI\nanalysis", "Aggregated\npatterns",
                "Business\ninterpretation", "Recommended\naction"],
        CONTENT_X, flow1_y, CONTENT_W, 0.95, card_fill=INDIGO_LIGHT, border=None,
        text_color=INDIGO_DARK, arrow_color=INDIGO_DARK, font_size=11.5, bold=True, arrow_w=0.26,
    )

    label_y = flow1_y + 0.95 + 0.08
    add_text(slide, CONTENT_X, label_y, CONTENT_W, 0.3, "For example", size=11.5, color=SLATE_500,
              italic=True, align=PP_ALIGN.CENTER, font=BODY_FONT)

    flow2_y = label_y + 0.35
    add_flow_horizontal(
        slide,
        ["Delivery appears in a\nlarge share of\nnegative feedback",
         "Delivery is\ndisproportionately\nrepresented among detractors",
         "Delivery may be a\ncustomer-health\ndriver",
         "Investigate carrier\nperformance and delivery\ncommunication"],
        CONTENT_X, flow2_y, CONTENT_W, 1.05, card_fill=TEAL_LIGHT, border=TEAL_ACCENT,
        text_color=TEAL_DARK, font_size=10, bold=False, arrow_w=0.3,
    )

    banner_y = flow2_y + 1.05 + 0.35
    banner = add_rect(slide, CONTENT_X, banner_y, CONTENT_W, 0.9, fill=INDIGO_DARK, radius=0.12)
    tf = banner.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "InsightCX is intended to augment CX expertise, not replace it."
    style_run(r, 18, WHITE, True, False, HEAD_FONT)

    add_footer(slide, 9)


def slide_10_trust(prs):
    slide = new_slide(prs)
    add_header(slide, "AI Evaluation", "Model performance isn't just about quality")

    stats = load_benchmark_stats()

    y = CONTENT_TOP + 0.05
    banner = add_rect(slide, CONTENT_X, y, CONTENT_W, 0.45, fill=INDIGO_DARK, radius=0.5)
    tf = banner.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "25 feedback records \u00b7 same task & prompts \u00b7 same dataset (v1)"
    style_run(r, 12.5, WHITE, True, False, HEAD_FONT)

    y2 = y + 0.45 + 0.07
    add_down_arrow(slide, SLIDE_W / 2, y2, w=0.36, h=0.2)

    y3 = y2 + 0.2 + 0.06
    model_labels = ["GPT-5-mini", "GPT-4.1-mini", "GPT-4o-mini"]
    mw = (CONTENT_W - 2 * 0.3) / 3
    mh = 0.5
    for i, m in enumerate(model_labels):
        mx = CONTENT_X + i * (mw + 0.3)
        add_card(slide, mx, y3, mw, mh, m, fill=WHITE, border=TEAL_ACCENT, title_size=14,
                  title_color=SLATE_900, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    y4 = y3 + mh + 0.06
    add_down_arrow(slide, SLIDE_W / 2, y4, w=0.36, h=0.2)
    add_text(slide, SLIDE_W / 2 + 0.32, y4 - 0.02, 1.2, 0.3, "Compare", size=10, color=SLATE_500,
              italic=True, font=BODY_FONT)

    y5 = y4 + 0.2 + 0.1
    metrics = ["Agreement", "Latency", "Tokens", "Cost"]
    cw = (CONTENT_W - 3 * 0.2) / 4
    ch = 0.4
    for i, met in enumerate(metrics):
        cx = CONTENT_X + i * (cw + 0.2)
        add_pill(slide, cx, y5, cw, ch, met, fill=TEAL_LIGHT, text_color=TEAL_DARK, size=11.5,
                  radius=0.5, border=TEAL_ACCENT)

    # Sentiment-agreement rate per model, from InsightCX's Model Comparison
    # view (model_comparison.png) \u2014 the benchmark run's consistency measure.
    agreement = {"gpt-5-mini": "100%", "gpt-4.1-mini": "100%", "gpt-4o-mini": "92%"}

    y6 = y5 + ch + 0.28
    left_w = 6.05
    headers = ["Model", "Latency (ms)", "Tokens/Rec.", "Cost/Rec.", "Agreement"]
    rows = []
    for s in stats:
        rows.append((s["model"], f'{s["latency"]:,}', f'{s["tokens_per_record"]:,}',
                     f'${s["cost_per_record"]:.4f}', agreement.get(s["model"], "\u2014")))
    if not rows:
        rows = [("GPT-5-mini", "\u2014", "\u2014", "\u2014", "\u2014"),
                ("GPT-4.1-mini", "\u2014", "\u2014", "\u2014", "\u2014"),
                ("GPT-4o-mini", "\u2014", "\u2014", "\u2014", "\u2014")]
    col_w = [1.2, 1.3, 1.25, 1.05, 1.25]
    table, table_h = add_table(slide, CONTENT_X, y6, left_w, headers, rows,
                                 col_widths=col_w, row_h=0.34, font_size=10.5, header_font_size=10)

    add_text(slide, CONTENT_X, y6 + table_h + 0.1, left_w, 0.4,
              "Based on a 25-record benchmark run per model (same dataset & prompts, v1) from "
              "InsightCX's AI Evaluation module.",
              size=9, color=SLATE_500, italic=True, font=BODY_FONT)

    right_x = CONTENT_X + left_w + 0.35
    right_w = SLIDE_W - MARGIN - right_x
    add_text(slide, right_x, y6, right_w, 0.28, "Model Comparison view", size=11.5, color=SLATE_900,
              bold=True, font=HEAD_FONT)
    add_picture_framed(slide, os.path.join(ASSETS, "model_comparison.png"), right_x, y6 + 0.34,
                        right_w, CONTENT_BOTTOM - (y6 + 0.34))

    add_footer(slide, 10)


def slide_11_learned(prs):
    slide = new_slide(prs)
    content_top = add_header(
        slide, "Lessons Learned", "What it took to build InsightCX",
        subtitle="Integrating an LLM is relatively easy \u2014 designing useful output, handling variability, "
                 "and evaluating whether the result is actually useful are the harder problems.")

    cards = [
        ("1", "From CX problem to AI product",
         "Turning unstructured customer feedback into business-ready insights.", INDIGO_ACCENT),
        ("2", "Creating meaningful test data",
         "Building realistic, varied feedback capable of revealing genuine patterns.", TEAL_ACCENT),
        ("3", "Evaluating AI, not just using it",
         "Comparing models across quality, consistency, latency and cost.", TEAL_ACCENT),
        ("4", "Integrating a full-stack AI application",
         "Connecting Flask, database, LLM services and React while learning the stack.", INDIGO_ACCENT),
    ]
    grid_y = content_top + 0.1
    grid_h = CONTENT_BOTTOM - grid_y
    cw = (CONTENT_W - 0.3) / 2
    ch = (grid_h - 0.25) / 2
    for i, (num, title, desc, color) in enumerate(cards):
        cx = CONTENT_X + (i % 2) * (cw + 0.3)
        cy = grid_y + (i // 2) * (ch + 0.25)
        add_card(slide, cx, cy, cw, ch, title, desc, fill=WHITE, border=SLATE_200, title_size=17,
                  desc_size=12.5, anchor=MSO_ANCHOR.MIDDLE, pad=0.35)
        add_badge(slide, cx + 0.2, cy + 0.2, 0.42, num, fill=color, size=15)

    add_footer(slide, 11)


def slide_12_next(prs):
    slide = new_slide(prs)
    add_header(slide, "What's Next", "Taking InsightCX beyond the MVP")

    cards = [
        ("Human-in-the-loop",
         "Allow users to review, validate and correct AI classifications, creating a feedback "
         "loop to improve analysis quality."),
        ("Trend analysis",
         "Track themes, sentiment and customer issues over time to identify emerging problems "
         "and measure whether actions are working."),
        ("Advanced evaluation",
         "Introduce ground-truth datasets and formal quality metrics to systematically measure "
         "and improve AI performance."),
    ]
    y = CONTENT_TOP + 0.3
    h = 3.15
    w = (CONTENT_W - 2 * 0.25) / 3
    colors = [TEAL_LIGHT, INDIGO_LIGHT, TEAL_LIGHT]
    tcolors = [TEAL_DARK, INDIGO_DARK, TEAL_DARK]
    borders = [TEAL_ACCENT, None, TEAL_ACCENT]
    for i, (t, d) in enumerate(cards):
        x = CONTENT_X + i * (w + 0.25)
        add_card(slide, x, y, w, h, t, d, fill=colors[i], border=borders[i], title_size=13,
                  title_color=tcolors[i], desc_size=10.5, desc_color=SLATE_600,
                  anchor=MSO_ANCHOR.TOP, pad=0.2)

    add_text(slide, CONTENT_X, y + h + 0.3, CONTENT_W, 0.4,
              "Not a committed roadmap \u2014 potential next steps based on what the MVP surfaced.",
              size=11.5, color=SLATE_500, italic=True, align=PP_ALIGN.CENTER, font=BODY_FONT)

    add_footer(slide, 12)


def slide_13_demo(prs):
    slide = new_slide(prs)
    add_header(slide, "Live Demo", "Let's see it in action")

    steps = ["Upload\nfeedback", "Analyze customer\nvoice", "Explore customer\nhealth",
             "Generate executive\ninsight"]
    flow_y = CONTENT_TOP + 1.1
    flow_h = 1.5
    n = len(steps)
    arrow_w = 0.32
    card_w = (CONTENT_W - (n - 1) * arrow_w) / n
    cx = CONTENT_X
    for i, label in enumerate(steps):
        add_badge(slide, cx + card_w / 2 - 0.2, flow_y - 0.55, 0.4, i + 1, fill=INDIGO_ACCENT, size=15)
        add_card(slide, cx, flow_y, card_w, flow_h, label, fill=WHITE, border=SLATE_200,
                  title_size=13.5, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        cx += card_w
        if i < n - 1:
            ay = flow_y + flow_h / 2 - (flow_h * 0.2) / 2
            add_arrow(slide, cx, ay, arrow_w, flow_h * 0.2, "right")
            cx += arrow_w

    add_footer(slide, 13)


def slide_14_closing(prs):
    slide = new_slide(prs)

    add_text(slide, SLIDE_W / 2 - 5, 1.5, 10, 1.6,
              "InsightCX is about using AI to make customer feedback more structured, scalable and "
              "actionable \u2014 so CX teams can spend less time processing feedback and more time acting on it.",
              size=21, color=SLATE_800, italic=True, bold=False, font=HEAD_FONT,
              align=PP_ALIGN.CENTER, line_spacing=1.25)

    add_logo_image(slide, SLIDE_W / 2, 4.35, width=4.4)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def main():
    prs = Presentation()
    prs.slide_width = Emu(int(SLIDE_W * 914400))
    prs.slide_height = Emu(int(SLIDE_H * 914400))

    slide_01_title(prs)
    slide_02_agenda(prs)
    slide_03_problem(prs)
    slide_04_scenario(prs)
    slide_05_overview(prs)
    slide_06_feature1(prs)
    slide_07_feature2(prs)
    slide_08_dashboard(prs)
    slide_09_decision(prs)
    slide_10_trust(prs)
    slide_11_learned(prs)
    slide_12_next(prs)
    slide_13_demo(prs)
    slide_14_closing(prs)

    prs.save(OUT_PATH)
    print(f"Saved {OUT_PATH} ({len(list(prs.slides))} slides)")


if __name__ == "__main__":
    main()

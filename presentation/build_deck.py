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


def add_rect(slide, x, y, w, h, fill=WHITE, line=None, line_w=0.75, radius=0.1):
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
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, pad=0.18, radius=0.1,
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
                         arrow_color=INDIGO_DARK, font_size=13.5, bold=True, arrow_w=0.4)


def slide_02_agenda(prs):
    """A narrative roadmap, not a table of contents - built from the exact
    same card idiom as Slide 13 (rounded card, numbered badge overlapping
    the top-left corner, bold header, secondary support line) so it reads
    as one consistent visual language rather than a one-off list style.
    Stage 7 gets Slide 13's "destination" treatment: light teal, full
    row width, dark teal number and header."""
    slide = new_slide(prs)
    add_header(slide, "The Journey", "From problem to proof")

    stages = [
        ("THE PROBLEM", "Why customer voice is difficult to scale"),
        ("THE APPROACH", "Turning customer language into structured insight"),
        ("THE VALUE", "From AI output to business action"),
        ("THE TEST", "Evaluating the AI behind the experience"),
        ("THE LEARNINGS", "What building the MVP revealed"),
        ("THE NEXT STEP", "Where InsightCX could go from here"),
        ("SEE IT IN ACTION", "Live demo"),
    ]

    gap = 0.28
    card_w = (CONTENT_W - 2 * gap) / 3
    card_h = 1.25
    pad = 0.24
    row_gap = 0.3

    def stage_card(x, y, w, num, label, support, fill, border, accent):
        add_rect(slide, x, y, w, card_h, fill=fill, line=border, line_w=0.75, radius=0.1)
        add_badge(slide, x + 0.16, y - 0.16, 0.32, num, fill=accent, size=12)
        cx, cw = x + pad, w - 2 * pad
        ty = y + pad
        add_text(slide, cx, ty, cw, 0.24, label, size=15, color=accent, bold=True, font=HEAD_FONT)
        add_text(slide, cx, ty + 0.32, cw, 0.3, support, size=10.5, color=SLATE_600,
                  font=BODY_FONT)

    arrow_w, arrow_h = 0.2, 0.3

    def row_arrow(x_after, y):
        add_arrow(slide, x_after + (gap - arrow_w) / 2, y + card_h / 2 - arrow_h / 2, arrow_w,
                  arrow_h, "right", INDIGO_DARK)

    row1_y = CONTENT_TOP + 0.3
    for i in range(3):
        x = CONTENT_X + i * (card_w + gap)
        label, support = stages[i]
        stage_card(x, row1_y, card_w, i + 1, label, support, WHITE, SLATE_200, INDIGO_ACCENT)
        if i < 2:
            row_arrow(x + card_w, row1_y)

    row2_y = row1_y + card_h + row_gap
    for i in range(3, 6):
        x = CONTENT_X + (i - 3) * (card_w + gap)
        label, support = stages[i]
        stage_card(x, row2_y, card_w, i + 1, label, support, WHITE, SLATE_200, INDIGO_ACCENT)
        if i < 5:
            row_arrow(x + card_w, row2_y)

    row3_y = row2_y + card_h + row_gap
    label7, support7 = stages[6]
    stage_card(CONTENT_X, row3_y, CONTENT_W, 7, label7, support7, INDIGO_LIGHT, None, INDIGO_ACCENT)

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
    gx, gy, gw, gh = CONTENT_X, CONTENT_TOP + 0.3, CONTENT_W, 2.0
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
    banner = add_rect(slide, CONTENT_X, banner_y, CONTENT_W, 0.82, fill=INDIGO_DARK, radius=0.1)
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
    """Four full-width levels, each a labelled group, read top to bottom:
    Customer Journey -> Feedback Sources -> Test Dataset -> Key CX Themes.
    Every level uses the same left-aligned, tracked-caps label idiom
    (from Slide 10) so the cascade reads as one consistent hierarchy."""
    slide = new_slide(prs)
    add_header(slide, "The Business Scenario",
                "A home-furnishing retailer \u2014 and hundreds of customer voices")

    label_kwargs = dict(size=11.5, bold=True, font=BODY_FONT, tracking=130)
    inter_gap = 0.2  # between one level's content and the next level's label
    intra_gap = 0.08  # between a level's label and its own content

    def level_label(y, text, color):
        add_text(slide, CONTENT_X, y, CONTENT_W, 0.2, text, color=color, **label_kwargs)
        return y + 0.2 + intra_gap

    # ---- Level 1: Customer Journey (unchanged) ----
    y = level_label(1.85, "CUSTOMER JOURNEY", INDIGO_ACCENT)
    add_flow_horizontal(
        slide, ["Discover", "Purchase", "Delivery", "Assembly", "Use"],
        CONTENT_X, y, CONTENT_W, 0.75, card_fill=INDIGO_LIGHT, border=None,
        text_color=INDIGO_DARK, arrow_color=INDIGO_DARK, font_size=12, bold=True, arrow_w=0.22,
    )
    y += 0.75 + inter_gap

    # ---- Level 2: Feedback Sources - NPS and CSAT side by side, full width ----
    y = level_label(y, "FEEDBACK SOURCES", SLATE_600)
    sources = [
        ("NPS", "Recommendation / loyalty feedback",
         "Measures likelihood to recommend on a 0\u201310 scale, indicating overall "
         "customer loyalty and advocacy."),
        ("CSAT", "Customer satisfaction feedback",
         "Measures satisfaction with a specific experience on a 1\u20135 scale, helping "
         "identify how well the customer\u2019s expectations were met."),
    ]
    card_gap = 0.3
    card_w = (CONTENT_W - card_gap) / 2
    card_h = 1.05
    for i, (t, sub, d) in enumerate(sources):
        cx = CONTENT_X + i * (card_w + card_gap)
        add_card(slide, cx, y, card_w, card_h, t, d, subtitle=sub, fill=WHITE, border=SLATE_200,
                  title_size=13.5, subtitle_size=11, desc_size=10, anchor=MSO_ANCHOR.MIDDLE)
    y += card_h + inter_gap

    # ---- Level 3: Test Dataset - one full-width box ----
    y = level_label(y, "TEST DATASET", TEAL_ACCENT)
    box_h = 0.72
    add_card(slide, CONTENT_X, y, CONTENT_W, box_h,
              "Several hundred feedback records across multiple weeks",
              "(Positive \u00b7 Neutral \u00b7 Negative)", fill=TEAL_LIGHT, border=TEAL_ACCENT,
              title_size=13, title_color=TEAL_DARK, desc_size=11.5, desc_color=TEAL_DARK,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    y += box_h + inter_gap

    # ---- Level 4: Key CX Themes - single row, full width ----
    y = level_label(y, "KEY CX THEMES", INDIGO_ACCENT)
    themes = ["Delivery", "Product quality & assembly", "Returns", "Website experience",
              "Payment / billing", "Brand loyalty"]
    pill_h = 0.42
    px = CONTENT_X
    for th in themes:
        pw = text_width_in(th, 10.5) + 0.28
        add_pill(slide, px, y, pw, pill_h, th, fill=INDIGO_LIGHT, text_color=INDIGO_DARK,
                  size=10.5, radius=0.3)
        px += pw + 0.14
    y += pill_h + 0.2

    add_text(slide, CONTENT_X, y, CONTENT_W, 0.3,
              "A controlled scenario for testing AI functionality \u2014 not production data.",
              size=10.5, color=SLATE_500, italic=True, align=PP_ALIGN.CENTER, font=BODY_FONT)

    add_footer(slide, 4)


def slide_05_overview(prs):
    """Three-stage conceptual model: customer voice -> AI structures it ->
    InsightCX interprets the patterns. AI Evaluation is drawn as a light
    cross-cutting strip beneath the stages, not a fourth pipeline step."""
    slide = new_slide(prs)
    add_header(slide, "InsightCX Overview", "From customer voice to business insight")

    # Tints used only for the compact sentiment/priority tags in the
    # ANALYZE stage's transformation example.
    RED_LIGHT = RGBColor(0xFE, 0xE2, 0xE2)
    AMBER_LIGHT = RGBColor(0xFE, 0xF3, 0xC7)

    row_y = CONTENT_TOP + 0.3
    row_h = 3.2
    gap = 0.34
    unit = (CONTENT_W - 2 * gap) / 3.3
    ingest_w = unit
    interpret_w = unit
    analyze_w = unit * 1.3

    pad_x = 0.26
    eyebrow_size = 12
    headline_size = 15
    support_size = 11.5
    eyebrow_h = eyebrow_size * 1.15 / 72
    headline_line_h = headline_size * 1.08 / 72
    support_line_h = support_size * 1.15 / 72

    def stage_shell(x, w, fill, border, border_w, num, badge_color):
        add_rect(slide, x, row_y, w, row_h, fill=fill, line=border, line_w=border_w, radius=0.1)
        add_badge(slide, x + 0.16, row_y - 0.16, 0.32, num, fill=badge_color, size=12)

    def stage_text(x, w, y, label, color, headline, support_lines):
        cx = x + pad_x
        cw = w - 2 * pad_x
        add_text(slide, cx, y, cw, eyebrow_h + 0.02, label, size=eyebrow_size, color=color,
                  bold=True, font=BODY_FONT, tracking=140)
        y += eyebrow_h + 0.14
        add_text(slide, cx, y, cw, 2 * headline_line_h + 0.06, headline, size=headline_size,
                  color=SLATE_900, bold=True, font=HEAD_FONT, line_spacing=1.08)
        y += 2 * headline_line_h + 0.16
        add_text(slide, cx, y, cw, len(support_lines) * support_line_h + 0.06,
                  "\n".join(support_lines), size=support_size, color=SLATE_600, font=BODY_FONT,
                  line_spacing=1.15)
        y += len(support_lines) * support_line_h
        return cx, cw, y

    # ---- Stage 1: INGEST ----
    x1 = CONTENT_X
    content_h1 = eyebrow_h + 0.14 + 2 * headline_line_h + 0.16 + support_line_h + 0.18 + 0.34
    y1 = row_y + (row_h - content_h1) / 2
    stage_shell(x1, ingest_w, WHITE, SLATE_200, 0.75, 1, INDIGO_ACCENT)
    cx, cw, y = stage_text(x1, ingest_w, y1, "INGEST", INDIGO_ACCENT,
                             "Bring customer feedback into one place",
                             ["NPS \u00b7 CSAT \u00b7 Customer comments"])
    y += 0.18
    pill_w = text_width_in("Raw customer voice", 11) + 0.34
    add_pill(slide, cx, y, pill_w, 0.34, "Raw customer voice", fill=INDIGO_LIGHT,
              text_color=INDIGO_DARK, size=11, radius=0.5)

    # ---- Stage 2: ANALYZE (visually emphasized) ----
    x2 = x1 + ingest_w + gap
    quote_size = 10.5
    quote_line_h = quote_size * 1.15 / 72
    tags_h = 0.28
    content_h2 = (eyebrow_h + 0.14 + 2 * headline_line_h + 0.16 + 2 * support_line_h + 0.16
                  + quote_line_h + 0.08 + tags_h)
    y2 = row_y + (row_h - content_h2) / 2
    stage_shell(x2, analyze_w, TEAL_LIGHT, TEAL_ACCENT, 1.5, 2, TEAL_ACCENT)
    cx, cw, y = stage_text(x2, analyze_w, y2, "ANALYZE", TEAL_DARK,
                             "Turn each comment into structured CX data",
                             ["Sentiment \u00b7 Emotion \u00b7 Themes", "Priority \u00b7 Confidence \u00b7 Summary"])
    y += 0.16
    add_text(slide, cx, y, cw, quote_line_h + 0.04,
              "\u201cThe sofa looks great, but delivery was two days late\u2026\u201d",
              size=quote_size, color=SLATE_500, italic=True, font=BODY_FONT)
    y += quote_line_h + 0.08
    tag_x = cx
    add_text(slide, tag_x, y, 0.2, tags_h, "\u2192", size=12, color=TEAL_DARK, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
    tag_x += 0.24
    for tag_text, tag_fill, tag_color in (("Negative", RED_LIGHT, RED),
                                            ("Delivery", INDIGO_LIGHT, INDIGO_DARK),
                                            ("High priority", AMBER_LIGHT, AMBER)):
        tw = text_width_in(tag_text, 10) + 0.22
        add_pill(slide, tag_x, y, tw, tags_h, tag_text, fill=tag_fill, text_color=tag_color,
                  size=10, radius=0.5)
        tag_x += tw + 0.1

    # ---- Stage 3: INTERPRET ----
    x3 = x2 + analyze_w + gap
    content_h3 = eyebrow_h + 0.14 + 2 * headline_line_h + 0.16 + 2 * support_line_h + 0.18 + 0.34
    y3 = row_y + (row_h - content_h3) / 2
    stage_shell(x3, interpret_w, WHITE, SLATE_200, 0.75, 3, INDIGO_ACCENT)
    cx, cw, y = stage_text(x3, interpret_w, y3, "INTERPRET", INDIGO_ACCENT,
                             "Turn feedback patterns into actionable insight",
                             ["Customer health \u00b7 Trends", "Business impact \u00b7 Leadership priorities"])
    y += 0.18
    pill_w = text_width_in("Executive insight", 11) + 0.34
    add_pill(slide, cx, y, pill_w, 0.34, "Executive insight", fill=INDIGO_LIGHT,
              text_color=INDIGO_DARK, size=11, radius=0.5)

    # ---- Connector chevrons between the three stages ----
    arrow_h = 0.5
    arrow_w = 0.2
    arrow_y = row_y + row_h / 2 - arrow_h / 2
    add_arrow(slide, x1 + ingest_w + (gap - arrow_w) / 2, arrow_y, arrow_w, arrow_h, "right",
              INDIGO_DARK)
    add_arrow(slide, x2 + analyze_w + (gap - arrow_w) / 2, arrow_y, arrow_w, arrow_h, "right")

    # ---- AI Evaluation: a light, cross-cutting layer, not a 4th stage ----
    rule_y = row_y + row_h + 0.35
    add_rect(slide, CONTENT_X, rule_y, CONTENT_W, 0.016, fill=SLATE_200, radius=0)

    label = "AI EVALUATION"
    metrics = "Consistency \u00b7 Latency \u00b7 Tokens \u00b7 Cost"
    # +tracking width: 140/100 pt per character, converted to inches.
    label_w = text_width_in(label, 11) + len(label) * 1.4 / 72 + 0.06
    metrics_w = text_width_in(metrics, 11.5, bold=False) + 0.05
    eval_gap = 0.22
    eval_x = CONTENT_X + (CONTENT_W - (label_w + eval_gap + metrics_w)) / 2
    eval_y = rule_y + 0.14
    add_text(slide, eval_x, eval_y, label_w, 0.3, label, size=11, color=TEAL_ACCENT, bold=True,
              font=BODY_FONT, tracking=140, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    add_text(slide, eval_x + label_w + eval_gap, eval_y, metrics_w, 0.3, metrics, size=11.5,
              color=SLATE_600, font=BODY_FONT, anchor=MSO_ANCHOR.MIDDLE)

    add_footer(slide, 5)


def slide_06_feature1(prs):
    slide = new_slide(prs)
    add_header(slide, "LLM Capability 1 of 2", "Turning customer language into structured CX data")

    left_x, left_w = CONTENT_X, 5.55
    add_text(slide, left_x, CONTENT_TOP, left_w, 0.26, "NATURAL LANGUAGE", size=13.5,
              color=INDIGO_DARK, bold=True, font=HEAD_FONT, align=PP_ALIGN.CENTER)

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
              size=11, color=SLATE_500, italic=True, font=BODY_FONT)

    arrow_x = left_x + left_w + 0.15
    arrow_w = 0.75
    add_arrow(slide, arrow_x, CONTENT_TOP + 2.55, arrow_w, 0.55, "right", INDIGO_DARK)

    right_x = arrow_x + arrow_w + 0.35
    right_w = SLIDE_W - MARGIN - right_x
    add_text(slide, right_x, CONTENT_TOP, right_w, 0.26, "STRUCTURED OUTPUT", size=13.5,
              color=TEAL_DARK, bold=True, font=HEAD_FONT, align=PP_ALIGN.CENTER)

    frame_y = CONTENT_TOP + 0.5
    frame_h = 4.55
    bottom = add_picture_framed(slide, os.path.join(ASSETS, "feedback_detail.png"), right_x,
                                  frame_y, right_w, frame_h)
    if bottom:
        add_text(slide, right_x, bottom + 0.06, right_w, 0.3, "Feedback Explorer \u2014 AI Assessment",
                  size=10, color=SLATE_500, italic=True, align=PP_ALIGN.CENTER, font=BODY_FONT)

    add_footer(slide, 6)


def slide_07_feature2(prs):
    """One progression, not two features: a question centered over each
    card sets up the pairing, a dark chevron connects the two cards, a
    numbered mechanism carries the flow (badges, not connectors, per
    request), and a small chevron plus "Transformation" label frame the
    quotes as that mechanism's concrete outcome."""
    slide = new_slide(prs)
    add_header(slide, "LLM Capability 2 of 2", "From individual comments to executive insight")

    gap = 0.45
    card_w = (CONTENT_W - gap) / 2
    x1, x2 = CONTENT_X, CONTENT_X + card_w + gap

    # ---- Question, centered above each card ----
    q_y = CONTENT_TOP
    add_text(slide, x1, q_y, card_w, 0.26, "WHAT IS THIS CUSTOMER SAYING?", size=13.5,
              color=INDIGO_DARK, bold=True, font=HEAD_FONT, align=PP_ALIGN.CENTER)
    add_text(slide, x2, q_y, card_w, 0.26, "WHAT DOES IT MEAN FOR THE BUSINESS?", size=13.5,
              color=TEAL_DARK, bold=True, font=HEAD_FONT, align=PP_ALIGN.CENTER)

    # ---- The two capabilities as separate, connected cards ----
    cards_y = q_y + 0.26 + 0.14
    card_h = 2.2

    def capability_card(x, fill, accent, title, analyzed, question, items, border=None):
        add_rect(slide, x, cards_y, card_w, card_h, fill=fill, line=border, line_w=0.75, radius=0.1)
        pad = 0.26
        cx, cw = x + pad, card_w - 2 * pad
        y = cards_y + pad

        # Header line: title, a thin arrow, and what's analyzed - inline,
        # with the latter matching the header's own color.
        header_box = slide.shapes.add_textbox(Inches(cx), Inches(y), Inches(cw), Inches(0.26))
        tf = header_box.text_frame
        tf.word_wrap = False
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        for text, size, bold, color, font in (
            (title, 14.5, True, accent, HEAD_FONT),
            ("  →  ", 12, False, SLATE_400, BODY_FONT),
            (analyzed, 12, False, accent, BODY_FONT),
        ):
            r = p.add_run()
            r.text = text
            style_run(r, size, color, bold, False, font)
        y += 0.26 + 0.12

        add_text(slide, cx, y, cw, 0.19, question, size=12, color=SLATE_800, bold=True,
                  font=BODY_FONT)
        y += 0.19 + 0.12
        add_rect(slide, cx, y, cw, 0.016, fill=accent, radius=0)
        y += 0.14
        for i, item in enumerate(items):
            add_text(slide, cx, y, cw, 0.19, f"{i + 1}.  {item}", size=11, color=SLATE_600,
                      bold=False, font=BODY_FONT)
            y += 0.245

    capability_card(x1, INDIGO_LIGHT, INDIGO_DARK, "Feedback Analysis", "Individual comment",
                     "What happened?", ["Sentiment", "Themes", "Priority", "Summary"])
    capability_card(x2, TEAL_LIGHT, TEAL_DARK, "Executive Insights", "Aggregated feedback",
                     "What does it mean?",
                     ["Customer health", "Business impact", "Leadership priorities",
                      "Recommended actions"], border=TEAL_DARK)

    # Dark chevron separating (and connecting) the two cards.
    add_arrow(slide, x1 + card_w + (gap - 0.22) / 2, cards_y + card_h / 2 - 0.16, 0.22, 0.32,
              "right", INDIGO_DARK)

    # ---- Bridge: the mechanism that turns column 1 into column 2 ----
    bridge_y = cards_y + card_h + 0.22
    add_text(slide, CONTENT_X, bridge_y, CONTENT_W, 0.22, "FROM ANALYSIS TO INSIGHT",
              size=11.5, color=SLATE_600, bold=True, font=BODY_FONT, tracking=130,
              align=PP_ALIGN.CENTER)

    flow_y = bridge_y + 0.44
    flow_h = 0.9
    steps = ["Hundreds of\ncustomer comments", "Patterns across\nfeedback",
             "Business\ninterpretation", "Recommended\naction"]
    fgap = 0.22
    fcard_w = (CONTENT_W - 3 * fgap) / 4
    for i, label in enumerate(steps):
        fx = CONTENT_X + i * (fcard_w + fgap)
        add_card(slide, fx, flow_y, fcard_w, flow_h, label, fill=WHITE, border=SLATE_200,
                  title_size=11.5, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_badge(slide, fx + fcard_w / 2 - 0.16, flow_y - 0.16, 0.32, i + 1, fill=INDIGO_ACCENT,
                  size=12)

    # ---- Example: the concrete outcome, framed by its own small header
    # and connected by the same chevron idiom used between the two cards
    # above - not a peer block, and no longer tied to the flow by an arrow. ----
    trans_y = flow_y + flow_h + 0.16
    add_text(slide, CONTENT_X, trans_y, CONTENT_W, 0.22, "TRANSFORMATION", size=11.5,
              color=SLATE_600, bold=True, font=BODY_FONT, tracking=130, align=PP_ALIGN.CENTER)

    callout_y = trans_y + 0.3
    callout_h = 0.8
    callout_w = (CONTENT_W - gap) / 2
    add_card(slide, CONTENT_X, callout_y, callout_w, callout_h,
              "\u201cDelivery reliability is emerging as a significant driver of customer dissatisfaction.\u201d",
              fill=INDIGO_LIGHT, border=None, title_size=12, title_color=INDIGO_DARK,
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    add_card(slide, CONTENT_X + callout_w + gap, callout_y, callout_w, callout_h,
              "\u201cLeadership priority: investigate delivery reliability and communication around delays.\u201d",
              fill=TEAL_LIGHT, border=TEAL_ACCENT, title_size=12, title_color=TEAL_DARK,
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    add_arrow(slide, CONTENT_X + callout_w + (gap - 0.22) / 2, callout_y + callout_h / 2 - 0.16,
              0.22, 0.32, "right", INDIGO_DARK)

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
    """Why the Slide 7 capability matters: one concrete business-value
    journey (signal -> pattern -> interpretation -> action), not a repeat
    of Slide 7's process flow. ACTION gets the same kind of emphasis
    Slide 5 gives ANALYZE, so the deck's "highlighted stage" idiom stays
    consistent."""
    slide = new_slide(prs)
    add_header(slide, "Business Impact", "From customer voice to action")

    row_y = CONTENT_TOP + 0.3
    row_h = 1.65
    gap = 0.3
    unit = (CONTENT_W - 3 * gap) / 4.15
    w_std = unit
    w_action = unit * 1.15

    pad_x = 0.24
    eyebrow_size = 11.5
    phrase_size = 12
    eyebrow_h = eyebrow_size * 1.15 / 72
    phrase_line_h = phrase_size * 1.15 / 72

    def stage_card(x, w, num, label, phrase, fill, border, border_w, badge_color, label_color,
                    phrase_color, phrase_bold):
        add_rect(slide, x, row_y, w, row_h, fill=fill, line=border, line_w=border_w, radius=0.1)
        add_badge(slide, x + 0.16, row_y - 0.16, 0.32, num, fill=badge_color, size=12)
        cx, cw = x + pad_x, w - 2 * pad_x
        content_h = eyebrow_h + 0.12 + 2 * phrase_line_h
        y = row_y + (row_h - content_h) / 2
        add_text(slide, cx, y, cw, eyebrow_h + 0.02, label, size=eyebrow_size, color=label_color,
                  bold=True, font=BODY_FONT, tracking=130)
        y += eyebrow_h + 0.12
        add_text(slide, cx, y, cw, 2 * phrase_line_h + 0.04, phrase, size=phrase_size,
                  color=phrase_color, bold=phrase_bold, font=BODY_FONT, line_spacing=1.1)

    x1 = CONTENT_X
    stage_card(x1, w_std, 1, "CUSTOMER SIGNAL",
               "Delivery appears in a large share of negative feedback",
               WHITE, SLATE_200, 0.75, TEAL_ACCENT, TEAL_ACCENT, SLATE_800, False)

    x2 = x1 + w_std + gap
    stage_card(x2, w_std, 2, "PATTERN",
               "Delivery is disproportionately represented among detractors",
               WHITE, SLATE_200, 0.75, TEAL_ACCENT, TEAL_ACCENT, SLATE_800, False)

    x3 = x2 + w_std + gap
    stage_card(x3, w_std, 3, "INTERPRETATION",
               "Delivery may be a customer-health driver",
               WHITE, SLATE_200, 0.75, TEAL_ACCENT, TEAL_ACCENT, SLATE_800, False)

    x4 = x3 + w_std + gap
    stage_card(x4, w_action, 4, "ACTION",
               "Investigate carrier performance and delivery communication",
               INDIGO_LIGHT, None, 1.5, INDIGO_ACCENT, INDIGO_DARK, INDIGO_DARK, True)

    arrow_h, arrow_w = 0.4, 0.18
    arrow_y = row_y + row_h / 2 - arrow_h / 2
    add_arrow(slide, x1 + w_std + (gap - arrow_w) / 2, arrow_y, arrow_w, arrow_h, "right")
    add_arrow(slide, x2 + w_std + (gap - arrow_w) / 2, arrow_y, arrow_w, arrow_h, "right")
    add_arrow(slide, x3 + w_std + (gap - arrow_w) / 2, arrow_y, arrow_w, arrow_h, "right")

    # Concluding takeaway - visually separated from the journey above, with
    # "augment CX expertise" carrying the emphasis rather than the whole
    # sentence, per house style for a closing statement (not a process step).
    msg_y = row_y + row_h + 0.7
    msg_box = slide.shapes.add_textbox(Inches(CONTENT_X + 1.2), Inches(msg_y),
                                         Inches(CONTENT_W - 2.4), Inches(0.6))
    tf = msg_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.line_spacing = 1.2
    for text, color, bold in (
        ("InsightCX is intended to ", SLATE_600, False),
        ("augment CX expertise", INDIGO_DARK, True),
        (", not replace it.", SLATE_600, False),
    ):
        r = p.add_run()
        r.text = text
        style_run(r, 16, color, bold, False, HEAD_FONT)

    add_footer(slide, 9)


def slide_10_trust(prs):
    """Two-part story: what the MVP currently evaluates (left, backed by
    the real benchmark table) and what still needs an evaluation approach
    (right, secondary and visually lighter) \u2014 framed as an engineering
    insight, not an apology."""
    slide = new_slide(prs)
    add_header(slide, "AI Evaluation", "A first benchmark \u2014 not the full picture")

    stats = load_benchmark_stats()
    agreement = {"gpt-5-mini": "100%", "gpt-4.1-mini": "100%", "gpt-4o-mini": "92%"}

    left_x, left_w = CONTENT_X, 6.05
    right_x = left_x + left_w + 0.4
    right_w = CONTENT_X + CONTENT_W - right_x

    # ---- Left: current MVP evaluation ----
    y = CONTENT_TOP + 0.3
    add_text(slide, left_x, y, left_w, 0.24, "CURRENT MVP EVALUATION", size=12, color=TEAL_ACCENT,
              bold=True, font=BODY_FONT, tracking=140)
    y += 0.3
    add_text(slide, left_x, y, left_w, 0.22,
              "25-record evaluation subset \u00b7 same task & prompts \u00b7 identical dataset (v1)",
              size=11, color=SLATE_500, italic=True, font=BODY_FONT)
    y += 0.38
    pills_y = y  # first of the left column's two "bullet rows" - the right
                 # column's boxes align to this and to table_y below.

    model_labels = ["GPT-5-mini", "GPT-4.1-mini", "GPT-4o-mini"]
    mw = (left_w - 2 * 0.15) / 3
    for i, m in enumerate(model_labels):
        add_pill(slide, left_x + i * (mw + 0.15), y, mw, 0.32, m, fill=WHITE,
                  text_color=SLATE_800, size=10.5, border=TEAL_ACCENT)
    y += 0.32 + 0.14

    metrics = ["Agreement", "Latency", "Tokens", "Cost"]
    cw = (left_w - 3 * 0.12) / 4
    for i, met in enumerate(metrics):
        add_pill(slide, left_x + i * (cw + 0.12), y, cw, 0.3, met, fill=TEAL_LIGHT,
                  text_color=TEAL_DARK, size=10, border=TEAL_ACCENT)
    y += 0.3 + 0.2
    table_y = y  # left column's table - the right column's second box
                 # aligns to this.

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
    table, table_h = add_table(slide, left_x, y, left_w, headers, rows,
                                 col_widths=col_w, row_h=0.32, font_size=10.5, header_font_size=10)
    y += table_h + 0.08
    add_text(slide, left_x, y, left_w, 0.35,
              "Based on a 25-record benchmark run per model (same dataset & prompts, v1).",
              size=9, color=SLATE_500, italic=True, font=BODY_FONT)
    left_bottom = y + 0.2

    # ---- Right: what's still missing (secondary, lighter treatment) ----
    # The label stays put at the top; the two boxes drop down to line up
    # with the left column's two "bullet rows" and its table, with more
    # air between the label and the boxes, and between the boxes themselves.
    add_text(slide, right_x, CONTENT_TOP + 0.3, right_w, 0.24, "WHAT'S STILL MISSING", size=12,
              color=INDIGO_ACCENT, bold=True, font=BODY_FONT, tracking=140)

    def gap_block(ry, block_h, num, label, phrase):
        add_rect(slide, right_x, ry, right_w, block_h, fill=WHITE, line=SLATE_200, line_w=0.75,
                  radius=0.1)
        add_badge(slide, right_x + 0.16, ry - 0.14, 0.3, num, fill=INDIGO_ACCENT, size=11.5)
        tx, tw = right_x + 0.22, right_w - 0.44
        add_text(slide, tx, ry + 0.34, tw, 0.2, label, size=10.5, color=INDIGO_ACCENT, bold=True,
                  font=BODY_FONT, tracking=120)
        add_text(slide, tx, ry + 0.6, tw, 0.36, phrase, size=11.5, color=SLATE_800,
                  font=BODY_FONT, line_spacing=1.12)

    block_h = 1.0
    block_gap = 0.4
    box1_y = pills_y  # aligns with the left column's model/metric pill rows
    box2_y = box1_y + block_h + block_gap  # lands alongside the table below
    gap_block(box1_y, block_h, 1, "STRUCTURED FEEDBACK",
              "Initial benchmark \u2192 deeper quality validation needed")
    gap_block(box2_y, block_h, 2, "EXECUTIVE INSIGHT",
              "Evaluation framework still to be developed")
    right_bottom = box2_y + block_h

    # ---- Takeaway ----
    msg_y = max(left_bottom, right_bottom) + 0.35
    msg_box = slide.shapes.add_textbox(Inches(CONTENT_X + 1.0), Inches(msg_y),
                                         Inches(CONTENT_W - 2.0), Inches(0.4))
    tf = msg_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    for text, color, bold in (
        ("The MVP establishes an evaluation ", SLATE_800, False),
        ("starting point", TEAL_DARK, True),
        (" \u2014 not a complete quality framework.", SLATE_800, False),
    ):
        r = p.add_run()
        r.text = text
        style_run(r, 15, color, bold, False, HEAD_FONT)

    add_footer(slide, 10)


def slide_11_learned(prs):
    slide = new_slide(prs)
    content_top = add_header(
        slide, "Lessons Learned", "What it took to build InsightCX",
        subtitle="Integrating an LLM is relatively easy \u2014 designing useful output, handling variability, "
                 "and evaluating whether the result is actually useful are the harder problems.")

    cards = [
        ("1", "Domain knowledge still matters",
         "Understanding the CX problem helped shape the AI requirements and interpret the results.",
         INDIGO_ACCENT),
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
    row_gap = 0.35
    ch = (grid_h - row_gap) / 2
    for i, (num, title, desc, color) in enumerate(cards):
        cx = CONTENT_X + (i % 2) * (cw + 0.3)
        cy = grid_y + (i // 2) * (ch + row_gap)
        add_card(slide, cx, cy, cw, ch, title, desc, fill=WHITE, border=SLATE_200, title_size=17,
                  desc_size=12.5, anchor=MSO_ANCHOR.MIDDLE, pad=0.35)
        add_badge(slide, cx + 0.21, cy - 0.21, 0.42, num, fill=color, size=15)

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
    """A transition slide, not a content slide: one continuous four-step
    journey (reusing Slide 5/9's badge-plus-eyebrow card idiom) carries
    the whole story, with generous whitespace so it reads as a hand-off
    into the live product rather than another explanatory slide."""
    slide = new_slide(prs)
    add_header(slide, "Live Demo", "From current state to new insight")

    steps = [
        ("REVIEW", "Review current-state insights", "What is happening today?"),
        ("ADD", "Upload new customer feedback", "Introduce a new set of customer voices"),
        ("GENERATE", "Generate a new executive summary",
         "Turn the updated feedback into business insight"),
        ("COMPARE", "Review changes in the Executive Brief", "What changed — and what does it mean?"),
    ]

    flow_y = CONTENT_TOP + 0.3
    card_h = 1.6
    gap = 0.28
    n = len(steps)
    card_w = (CONTENT_W - (n - 1) * gap) / n
    pad = 0.22

    for i, (eyebrow, headline, support) in enumerate(steps):
        is_endpoint = i == n - 1
        fill = INDIGO_LIGHT if is_endpoint else WHITE
        border = None if is_endpoint else SLATE_200
        accent = INDIGO_ACCENT

        x = CONTENT_X + i * (card_w + gap)
        add_rect(slide, x, flow_y, card_w, card_h, fill=fill, line=border, line_w=0.75,
                  radius=0.1)
        add_badge(slide, x + 0.16, flow_y - 0.16, 0.32, i + 1, fill=accent, size=12)
        cx, cw = x + pad, card_w - 2 * pad
        y = flow_y + pad
        add_text(slide, cx, y, cw, 0.18, eyebrow, size=10.5, color=accent, bold=True,
                  font=BODY_FONT, tracking=120)
        y += 0.26
        add_text(slide, cx, y, cw, 0.42, headline, size=13.5, color=SLATE_900, bold=True,
                  font=HEAD_FONT, line_spacing=1.08)
        y += 0.5
        add_text(slide, cx, y, cw, 0.36, support, size=10, color=SLATE_500, font=BODY_FONT,
                  line_spacing=1.1)

        if i < n - 1:
            ay = flow_y + card_h / 2 - 0.16
            add_arrow(slide, x + card_w + (gap - 0.2) / 2, ay, 0.2, 0.32, "right", INDIGO_DARK)

    add_text(slide, CONTENT_X, flow_y + card_h + 0.5, CONTENT_W, 0.35,
              "New customer feedback → updated analysis → changed business insight",
              size=13, color=SLATE_500, italic=True, align=PP_ALIGN.CENTER, font=BODY_FONT)

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

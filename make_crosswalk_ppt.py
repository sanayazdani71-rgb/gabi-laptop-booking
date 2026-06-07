from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

# ── Slide size: widescreen 16:9 ──────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

# ── Palette ───────────────────────────────────────────────────────────────────
C_DARK    = RGBColor(0x1A, 0x1A, 0x2E)
C_BLUE    = RGBColor(0x22, 0x77, 0xCC)
C_AMBER   = RGBColor(0xD9, 0x77, 0x06)
C_GREEN   = RGBColor(0x16, 0xA3, 0x4A)
C_PURPLE  = RGBColor(0x7C, 0x3A, 0xED)
C_TEAL    = RGBColor(0x0D, 0x94, 0x88)
C_GREY    = RGBColor(0x6B, 0x72, 0x80)
C_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
C_LINE    = RGBColor(0xC4, 0xC9, 0xD1)

# ── Single combined box: coloured title line + bullet body, ONE shape ────────
def add_card(slide, left, top, width, height, title, bullets,
             accent_rgb, title_size=10, body_size=8.5, fill_rgb=None):
    fill_rgb = fill_rgb or C_WHITE
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    shape.line.color.rgb = accent_rgb
    shape.line.width = Pt(1.5)

    # rounded corners + thicker left accent edge via XML
    sp = shape.element
    prstGeom = sp.find(qn('p:spPr')).find(qn('a:prstGeom'))
    if prstGeom is not None:
        prstGeom.set('prst', 'roundRect')
        avLst = prstGeom.find(qn('a:avLst'))
        if avLst is None:
            avLst = etree.SubElement(prstGeom, qn('a:avLst'))
        for gd in avLst.findall(qn('a:gd')):
            avLst.remove(gd)
        gd = etree.SubElement(avLst, qn('a:gd'))
        gd.set('name', 'adj')
        gd.set('fmla', 'val 6000')

    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.14)
    tf.margin_right = Inches(0.10)
    tf.margin_top = Inches(0.07)
    tf.margin_bottom = Inches(0.05)

    # Title paragraph (single run, coloured + bold, inside same shape)
    p_title = tf.paragraphs[0]
    p_title.alignment = PP_ALIGN.LEFT
    r_title = p_title.add_run()
    r_title.text = title
    r_title.font.bold = True
    r_title.font.size = Pt(title_size)
    r_title.font.color.rgb = accent_rgb
    p_title.space_after = Pt(3)

    # Bullet lines
    for b in bullets:
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = b
        r.font.size = Pt(body_size)
        r.font.color.rgb = C_DARK
        p.space_after = Pt(1)

    return shape


def add_label(slide, left, top, width, height, text, rgb,
              size=8, bold=False, align=PP_ALIGN.CENTER, italic=False):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = rgb


def v_arrow(slide, cx, top, length, color=C_LINE):
    conn = slide.shapes.add_connector(1, Inches(cx), Inches(top), Inches(cx), Inches(top + length))
    conn.line.color.rgb = color
    conn.line.width = Pt(1.5)
    tri = slide.shapes.add_shape(5, Inches(cx - 0.055), Inches(top + length - 0.005), Inches(0.11), Inches(0.11))
    tri.fill.solid()
    tri.fill.fore_color.rgb = color
    tri.line.fill.background()
    sp = tri.element
    pg = sp.find(qn('p:spPr')).find(qn('a:prstGeom'))
    pg.set('prst', 'downArrow')


def h_line(slide, left, top, width, color=C_LINE):
    conn = slide.shapes.add_connector(1, Inches(left), Inches(top), Inches(left + width), Inches(top))
    conn.line.color.rgb = color
    conn.line.width = Pt(1.5)


# ── Background & title bar ────────────────────────────────────────────────────
bg = slide.background.fill
bg.solid()
bg.fore_color.rgb = RGBColor(0xF8, 0xF8, 0xFC)

add_card(slide, 0, 0, 13.33, 0.5, "", [], C_DARK, fill_rgb=C_DARK)
add_label(slide, 0.2, 0.07, 9, 0.36,
          "Source Profiling & FST Harmonization — Two Data Sources Converging into One Crosswalk",
          C_WHITE, size=13, bold=True, align=PP_ALIGN.LEFT)

# ── Layout constants ──────────────────────────────────────────────────────────
MARGIN = 0.35
COL_GAP = 0.5
COL_W = (13.33 - 2 * MARGIN - COL_GAP) / 2
LEFT_X = MARGIN
RIGHT_X = MARGIN + COL_W + COL_GAP

CARD_H = 1.05
GAP_V = 0.16
TOP0 = 0.78

cx_left  = LEFT_X + COL_W / 2
cx_right = RIGHT_X + COL_W / 2

# ── COLUMN 1 — Data Source 1 chain ────────────────────────────────────────────
y = TOP0
add_card(slide, LEFT_X, y, COL_W, 0.5,
         "📁  Data Source 1 — fo-um-011 Eco-Balance File", [],
         C_DARK, title_size=10, fill_rgb=C_DARK)
y_src1 = y
y += 0.5 + GAP_V

add_card(slide, LEFT_X, y, COL_W, CARD_H,
         "🔍  Source Profiling", [
             "•  Existing environmental reporting workbook",
             "•  Contains input/output environmental data",
             "•  Contains calculated phantom product mass",
         ], C_BLUE)
y_prof1 = y
y += CARD_H + GAP_V

add_card(slide, LEFT_X, y, COL_W, CARD_H,
         "✅  Selected Data", [
             "•  Measured energy per FST",
             "•  Measured water per FST",
             "•  Measured wastewater per FST",
             "•  Available FST list",
         ], C_GREEN)
y_sel1 = y
y += CARD_H + GAP_V

add_card(slide, LEFT_X, y, COL_W, CARD_H + 0.15,
         "🚫  Excluded / Not Used at This Stage", [
             "•  Calculated product quantity",
             "•  Packaging allocation",
             "•  Waste allocation",
             "•  Product-based KPIs from phantom product mass",
         ], C_GREY, fill_rgb=RGBColor(0xF2, 0xF2, 0xF5))
y_excl1 = y
col1_bottom = y + CARD_H + 0.15

# Connectors column 1
v_arrow(slide, cx_left, y_src1 + 0.5, GAP_V)
v_arrow(slide, cx_left, y_prof1 + CARD_H, GAP_V)
v_arrow(slide, cx_left, y_sel1 + CARD_H, GAP_V)

# ── COLUMN 2 — Data Source 2 chain ────────────────────────────────────────────
y = TOP0
add_card(slide, RIGHT_X, y, COL_W, 0.5,
         "📁  Data Source 2 — ERP / Fredl Production List", [],
         C_DARK, title_size=10, fill_rgb=C_DARK)
y_src2 = y
y += 0.5 + GAP_V

add_card(slide, RIGHT_X, y, COL_W, CARD_H,
         "🔍  Source Profiling", [
             "•  Transaction-level production / order data",
             "•  Contains FST, product, part, quantity, value",
             "•  Contains material consumption in kg",
         ], C_AMBER)
y_prof2 = y
y += CARD_H + GAP_V

add_card(slide, RIGHT_X, y, COL_W, CARD_H + 0.55,
         "✂️  Column Scope Filtering", [
             "Removed project-specific columns:",
             "•  Firma_Referenz       •  Auftrag_Referenz_Bzg",
             "•  Anwendung_Referenz   •  IP_Nr",
             "•  Auftrag_Referenz     •  FA_Nr",
         ], C_PURPLE)
y_filt2 = y
y += CARD_H + 0.55 + GAP_V

add_card(slide, RIGHT_X, y, COL_W, CARD_H + 0.15,
         "🧩  Core Analytical Structure", [
             "•  Central key: Teilenummer",
             "•  Product group: PPG_Produkt_BK · Description: Produkt / Teil",
             "•  FST involved: FST_beteiligt",
             "•  Quantities and material consumption",
         ], C_TEAL)
y_core2 = y
y += CARD_H + 0.15 + GAP_V

add_card(slide, RIGHT_X, y, COL_W, CARD_H,
         "🌐  Semantic Enrichment", [
             "•  Decode PPG_Produkt_BK into product division",
             "•  Identify unit logic: ST or m²",
             "•  Interpret NULL / zero values",
         ], C_GREEN)
y_sem2 = y
col2_bottom = y + CARD_H

# Connectors column 2
v_arrow(slide, cx_right, y_src2 + 0.5, GAP_V)
v_arrow(slide, cx_right, y_prof2 + CARD_H, GAP_V)
v_arrow(slide, cx_right, y_filt2 + CARD_H + 0.55, GAP_V)
v_arrow(slide, cx_right, y_core2 + CARD_H + 0.15, GAP_V)

# ── CONVERGENCE — FST Boundary Harmonization ──────────────────────────────────
conv_top = max(col1_bottom, col2_bottom) + 0.35
conv_w = 13.33 - 2 * MARGIN
conv_left = MARGIN
cx_conv = conv_left + conv_w / 2

add_card(slide, conv_left, conv_top, conv_w, 0.5,
         "🔀  FST Boundary Harmonization / Crosswalk", [],
         C_DARK, title_size=11, fill_rgb=C_DARK)

y_cw = conv_top + 0.5 + GAP_V + 0.05
add_card(slide, conv_left + conv_w * 0.18, y_cw, conv_w * 0.64, 1.15,
         "📊  Compare FSTs from Both Sources", [
             "•  FSTs present in both lists      •  FSTs only in fo-um-011 list",
             "•  FSTs only in Fredl's ERP list   •  Availability of energy values",
             "•  Assignment to production area / Bereich",
         ], C_DARK, body_size=9)

# Convergence connectors: from each column bottom down + across to crosswalk title
mid_y = (max(col1_bottom, col2_bottom) + conv_top) / 2
v_arrow(slide, cx_left, col1_bottom, mid_y - col1_bottom)
v_arrow(slide, cx_right, col2_bottom, mid_y - col2_bottom)
h_line(slide, min(cx_left, cx_right), mid_y, abs(cx_right - cx_left))
v_arrow(slide, cx_conv, mid_y, conv_top - mid_y)

# arrow from harmonization title down into compare card
v_arrow(slide, cx_conv, conv_top + 0.5, GAP_V + 0.05)

# ── Footer ────────────────────────────────────────────────────────────────────
add_label(slide, 0.2, 7.28, 13.0, 0.18,
          "Lindner Group · Eco-Balance & ERP Data Integration · Source Profiling Stage",
          C_GREY, size=7, align=PP_ALIGN.CENTER, italic=True)

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = "/home/user/gabi-laptop-booking/source_profiling_crosswalk.pptx"
prs.save(out_path)
print(f"Saved: {out_path}")

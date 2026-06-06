from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.oxml.ns import qn
from lxml import etree
import copy

# ── Slide size: widescreen 16:9 ──────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

slide_layout = prs.slide_layouts[6]   # blank
slide = prs.slides.add_slide(slide_layout)

# ── Colour palette ────────────────────────────────────────────────────────────
C_DARK      = RGBColor(0x1A, 0x1A, 0x2E)   # near-black (title bar)
C_ORANGE    = RGBColor(0xF5, 0x9E, 0x0B)   # amber accent
C_BLUE      = RGBColor(0x22, 0x77, 0xCC)   # blue accent
C_PURPLE    = RGBColor(0x7C, 0x3A, 0xED)   # purple accent
C_GREEN     = RGBColor(0x16, 0xA3, 0x4A)   # green accent
C_TEAL      = RGBColor(0x0D, 0x94, 0x88)   # teal accent
C_RED       = RGBColor(0xDC, 0x26, 0x26)   # red accent
C_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
C_LIGHT_BG  = RGBColor(0xF8, 0xF9, 0xFA)
C_BORDER    = RGBColor(0xE5, 0xE7, 0xEB)
C_MUTED     = RGBColor(0x6B, 0x72, 0x80)

# ── Helpers ───────────────────────────────────────────────────────────────────

def add_box(slide, left, top, width, height,
            fill_rgb, border_rgb=None, border_pt=1.5, radius=0.06):
    """Add a rounded rectangle with solid fill and optional border."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE → we'll apply rounding via XML
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    if border_rgb:
        shape.line.color.rgb = border_rgb
        shape.line.width = Pt(border_pt)
    else:
        shape.line.fill.background()

    # Apply corner rounding
    sp = shape.element
    prstGeom = sp.find(qn('p:spPr')).find(qn('a:prstGeom'))
    if prstGeom is not None:
        prstGeom.set('prst', 'roundRect')
        avLst = prstGeom.find(qn('a:avLst'))
        if avLst is None:
            avLst = etree.SubElement(prstGeom, qn('a:avLst'))
        # remove old gd
        for gd in avLst.findall(qn('a:gd')):
            avLst.remove(gd)
        gd = etree.SubElement(avLst, qn('a:gd'))
        gd.set('name', 'adj')
        gd.set('fmla', f'val {int(radius * 100000)}')
    return shape


def add_text_box(slide, left, top, width, height,
                 title, body_lines,
                 header_fill, header_text_rgb=None,
                 body_fill=None, body_text_rgb=None,
                 font_size_title=10, font_size_body=8.5,
                 border_rgb=None):
    """
    Draw a card: coloured header strip + white body with bullet lines.
    Uses two separate shapes stacked.
    """
    header_text_rgb = header_text_rgb or C_WHITE
    body_fill = body_fill or C_WHITE
    body_text_rgb = body_text_rgb or C_DARK
    border_rgb = border_rgb or header_fill

    header_h = 0.30
    body_h = height - header_h

    # Header
    hdr = add_box(slide, left, top, width, header_h, header_fill, border_rgb, 1.2)
    tf = hdr.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title
    run.font.bold = True
    run.font.size = Pt(font_size_title)
    run.font.color.rgb = header_text_rgb

    # Body
    body = add_box(slide, left, top + header_h, width, body_h,
                   body_fill, border_rgb, 1.2)
    tf2 = body.text_frame
    tf2.word_wrap = True
    tf2.margin_left  = Inches(0.10)
    tf2.margin_right = Inches(0.06)
    tf2.margin_top   = Inches(0.06)

    first = True
    for line in body_lines:
        p2 = tf2.paragraphs[0] if first else tf2.add_paragraph()
        first = False
        p2.alignment = PP_ALIGN.LEFT
        run2 = p2.add_run()
        run2.text = line
        run2.font.size = Pt(font_size_body)
        run2.font.color.rgb = body_text_rgb
        p2.space_after = Pt(1)


def add_label(slide, left, top, width, height, text,
              rgb, font_size=8, bold=False, align=PP_ALIGN.CENTER, italic=False):
    txb = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = rgb
    run.font.bold = bold
    run.font.italic = italic


def add_connector_v(slide, left, top, height, color=C_BORDER):
    """Vertical line connector."""
    from pptx.util import Inches, Pt
    connector = slide.shapes.add_connector(
        1,  # straight
        Inches(left), Inches(top),
        Inches(left), Inches(top + height)
    )
    connector.line.color.rgb = color
    connector.line.width = Pt(1.5)


def add_connector_h(slide, left, top, width, color=C_BORDER):
    connector = slide.shapes.add_connector(
        1,
        Inches(left), Inches(top),
        Inches(left + width), Inches(top)
    )
    connector.line.color.rgb = color
    connector.line.width = Pt(1.5)


def add_arrow_down(slide, cx, top, length, color=C_BORDER):
    """Downward arrow: vertical line + arrowhead triangle."""
    add_connector_v(slide, cx, top, length, color)
    # triangle arrowhead
    from pptx.util import Inches
    tri = slide.shapes.add_shape(
        5,  # isoceles triangle
        Inches(cx - 0.06), Inches(top + length - 0.01),
        Inches(0.12), Inches(0.12)
    )
    tri.fill.solid()
    tri.fill.fore_color.rgb = color
    tri.line.fill.background()
    sp = tri.element
    prstGeom = sp.find(qn('p:spPr')).find(qn('a:prstGeom'))
    if prstGeom is not None:
        prstGeom.set('prst', 'downArrow')


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE BACKGROUND
# ─────────────────────────────────────────────────────────────────────────────
bg = slide.background
bg_fill = bg.fill
bg_fill.solid()
bg_fill.fore_color.rgb = RGBColor(0xF8, 0xF8, 0xFC)

# ─────────────────────────────────────────────────────────────────────────────
# TITLE BAR
# ─────────────────────────────────────────────────────────────────────────────
title_bar = add_box(slide, 0, 0, 13.33, 0.55, C_DARK)
add_label(slide, 0.15, 0.08, 8, 0.38,
          "ERP Data Architecture — From Raw Source to Analytical Output",
          C_WHITE, font_size=13, bold=True, align=PP_ALIGN.LEFT)
add_label(slide, 0.15, 0.34, 8, 0.22,
          "How ERP fields are structured into reference dimensions, linked, and converted into production & material KPIs",
          RGBColor(0xA0, 0xAE, 0xC0), font_size=7.5, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
Y0 = 0.70   # top of first row
ROW1_H = 1.35
ROW2_H = 1.45
ROW3_H = 1.30

GAP_V = 0.28   # vertical gap between rows

Y1 = Y0 + ROW1_H + GAP_V          # row 2 top
Y2 = Y1 + ROW2_H + GAP_V          # row 3 top

W_SOURCE = 3.20
W_REF    = 3.60
W_MID    = 5.60
W_BOT    = 5.60

MARGIN = 0.28

# ─────────────────────────────────────────────────────────────────────────────
# ROW 0 — RAW ERP DATA SOURCE (centred)
# ─────────────────────────────────────────────────────────────────────────────
src_left = (13.33 - W_SOURCE) / 2
src_top  = Y0

add_text_box(slide,
    left=src_left, top=src_top, width=W_SOURCE, height=0.62,
    title="🗄  Raw ERP Data Source",
    body_lines=[],
    header_fill=C_DARK,
    body_fill=C_DARK,
    font_size_title=11,
)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 1 — THREE REFERENCE BOXES
# ─────────────────────────────────────────────────────────────────────────────
total_refs_w = 13.33 - 2 * MARGIN
gap_refs = 0.22
ref_w = (total_refs_w - 2 * gap_refs) / 3

ref_tops = Y0 + 0.62 + GAP_V

# Org Reference
ref1_left = MARGIN
add_text_box(slide,
    left=ref1_left, top=ref_tops, width=ref_w, height=ROW1_H,
    title="🏢  Organizational Reference",
    body_lines=[
        "FST_beteiligt",
        "Firma_Referenz",
        "Anwendung_Referenz",
    ],
    header_fill=C_BLUE,
    font_size_title=9.5, font_size_body=9,
)

# Order Reference
ref2_left = ref1_left + ref_w + gap_refs
add_text_box(slide,
    left=ref2_left, top=ref_tops, width=ref_w, height=ROW1_H,
    title="📋  Order / Project Reference",
    body_lines=[
        "Auftrag_Referenz",
        "Auftrag_Referenz_Bzg",
        "IP_Nr",
        "FA_Nr",
    ],
    header_fill=C_ORANGE,
    font_size_title=9.5, font_size_body=9,
)

# Product Reference
ref3_left = ref2_left + ref_w + gap_refs
add_text_box(slide,
    left=ref3_left, top=ref_tops, width=ref_w, height=ROW1_H,
    title="📦  Product / Part Reference",
    body_lines=[
        "PPG_Produkt_BK",
        "Produkt",
        "Teil",
        "Teilenummer",
    ],
    header_fill=C_PURPLE,
    font_size_title=9.5, font_size_body=9,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONNECTORS: source → refs  (straight lines down)
# ─────────────────────────────────────────────────────────────────────────────
src_cx = src_left + W_SOURCE / 2

gap1_top    = Y0 + 0.62
gap1_bottom = ref_tops

mid_gap = (gap1_top + gap1_bottom) / 2

# vertical from source box down to horizontal bar
add_connector_v(slide, src_cx, gap1_top, mid_gap - gap1_top, C_BORDER)

# horizontal bar spanning all three ref boxes centres
ref1_cx = ref1_left + ref_w / 2
ref2_cx = ref2_left + ref_w / 2
ref3_cx = ref3_left + ref_w / 2

add_connector_h(slide, ref1_cx, mid_gap, ref3_cx - ref1_cx, C_BORDER)

# verticals from horizontal bar down to each ref box
for cx in [ref1_cx, ref2_cx, ref3_cx]:
    add_connector_v(slide, cx, mid_gap, gap1_bottom - mid_gap, C_BORDER)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 2 — LINKAGE  +  MEASURE
# ─────────────────────────────────────────────────────────────────────────────
gap_mid = 0.30
mid_w   = (13.33 - 2 * MARGIN - gap_mid) / 2

link_left    = MARGIN
measure_left = MARGIN + mid_w + gap_mid

row2_top = ref_tops + ROW1_H + GAP_V

add_text_box(slide,
    left=link_left, top=row2_top, width=mid_w, height=ROW2_H,
    title="🔗  Linkage / Connection Logic",
    body_lines=[
        "Which product / order line belongs to which FST?",
        "",
        "Which product consists of which part number?",
    ],
    header_fill=C_TEAL,
    font_size_title=9.5, font_size_body=9,
)

add_text_box(slide,
    left=measure_left, top=row2_top, width=mid_w, height=ROW2_H,
    title="📊  Measure / Fact Data",
    body_lines=[
        "Menge_Original",
        "Menge_statistisch",
        "PPG_MEH_Statistik",
        "Wert",
        "Materialverbrauch_kg",
    ],
    header_fill=C_GREEN,
    font_size_title=9.5, font_size_body=9,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONNECTORS: refs → row2
# ─────────────────────────────────────────────────────────────────────────────
link_cx    = link_left    + mid_w / 2
measure_cx = measure_left + mid_w / 2

row1_bottom = ref_tops + ROW1_H
row2_top_y  = row2_top

mid2 = (row1_bottom + row2_top_y) / 2

# horizontal across ref box centres
add_connector_h(slide, ref1_cx, mid2, ref3_cx - ref1_cx, C_BORDER)
# vertical from bar up to ref row bottom (all three)
for cx in [ref1_cx, ref2_cx, ref3_cx]:
    add_connector_v(slide, cx, row1_bottom, mid2 - row1_bottom, C_BORDER)
# vertical from bar down to link + measure
add_connector_h(slide, link_cx, mid2, measure_cx - link_cx, C_BORDER)
for cx in [link_cx, measure_cx]:
    add_connector_v(slide, cx, mid2, row2_top_y - mid2, C_BORDER)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 3 — OUTPUTS
# ─────────────────────────────────────────────────────────────────────────────
row3_top = row2_top + ROW2_H + GAP_V

out_w = mid_w

add_text_box(slide,
    left=link_left, top=row3_top, width=out_w, height=ROW3_H,
    title="🔀  Connection Outputs",
    body_lines=[
        "•  FST system boundary definition",
        "•  Product ↔ FST routing",
        "•  Order ↔ product mapping",
        "•  Part ↔ product mapping",
    ],
    header_fill=C_TEAL,
    body_fill=RGBColor(0xEF, 0xFB, 0xF9),
    body_text_rgb=C_DARK,
    font_size_title=9.5, font_size_body=9,
)

add_text_box(slide,
    left=measure_left, top=row3_top, width=out_w, height=ROW3_H,
    title="📈  Analytical Outputs",
    body_lines=[
        "•  Actual production volume",
        "•  Material consumption (kg)",
        "•  Material intensity (kg / unit)",
        "•  Product mix analysis",
    ],
    header_fill=C_GREEN,
    body_fill=RGBColor(0xF0, 0xFD, 0xF4),
    body_text_rgb=C_DARK,
    font_size_title=9.5, font_size_body=9,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONNECTORS: row2 → row3
# ─────────────────────────────────────────────────────────────────────────────
row2_bottom = row2_top + ROW2_H
for cx in [link_cx, measure_cx]:
    add_connector_v(slide, cx, row2_bottom, row3_top - row2_bottom, C_BORDER)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
add_label(slide, 0.15, 7.30, 13.0, 0.18,
          "Lindner Group · IMS Department · Integrated Management System",
          C_MUTED, font_size=7, align=PP_ALIGN.CENTER, italic=True)

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
out_path = "/home/user/gabi-laptop-booking/erp_data_architecture.pptx"
prs.save(out_path)
print(f"Saved: {out_path}")

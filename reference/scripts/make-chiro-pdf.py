#!/usr/bin/env python3
"""Generate a printable PDF for chiropractor visit — Dorsal Scapular Nerve Pain"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

HERE = os.path.dirname(os.path.abspath(__file__))

# Colors
DARK = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")
BLUE = HexColor("#0f3460")
LIGHT_BG = HexColor("#f5f5f5")
WHITE = HexColor("#ffffff")
GRAY = HexColor("#666666")
LIGHT_GRAY = HexColor("#e0e0e0")
GREEN = HexColor("#2d6a4f")
AMBER = HexColor("#b45309")

# Styles
style_title = ParagraphStyle(
    "Title", fontName="Helvetica-Bold", fontSize=22,
    textColor=DARK, spaceAfter=4, alignment=TA_CENTER
)
style_subtitle = ParagraphStyle(
    "Subtitle", fontName="Helvetica", fontSize=11,
    textColor=GRAY, spaceAfter=16, alignment=TA_CENTER
)
style_h2 = ParagraphStyle(
    "H2", fontName="Helvetica-Bold", fontSize=14,
    textColor=BLUE, spaceBefore=16, spaceAfter=8
)
style_body = ParagraphStyle(
    "Body", fontName="Helvetica", fontSize=10,
    textColor=DARK, spaceAfter=6, leading=14
)
style_label = ParagraphStyle(
    "Label", fontName="Helvetica-Bold", fontSize=9,
    textColor=WHITE, alignment=TA_CENTER
)
style_small = ParagraphStyle(
    "Small", fontName="Helvetica", fontSize=8,
    textColor=GRAY, spaceAfter=4
)
style_bullet = ParagraphStyle(
    "Bullet", fontName="Helvetica", fontSize=10,
    textColor=DARK, spaceAfter=4, leading=14,
    leftIndent=20, bulletIndent=8
)

def build_pdf():
    output_path = os.path.join(HERE, "..", "Dorsal-Scapular-Nerve-Pain-Map.pdf")
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        topMargin=0.6*inch, bottomMargin=0.6*inch,
        leftMargin=0.75*inch, rightMargin=0.75*inch
    )
    story = []

    # Title
    story.append(Paragraph("Where My Pain Is", style_title))
    story.append(Paragraph("For my chiropractor  |  Upper cervical patient", style_subtitle))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=12))

    # ── SECTION 1: WHERE THE PAIN IS ──
    story.append(Paragraph("1. Where the Pain Is", style_h2))

    symptoms_data = [
        [Paragraph("<b>Location</b>", style_body),
         Paragraph("Along the <b>inner edge of my right shoulder blade</b> (medial border of the scapula)", style_body)],
        [Paragraph("<b>What it feels like</b>", style_body),
         Paragraph("<b>Sharp</b> — feels like a nerve, not a muscle ache", style_body)],
        [Paragraph("<b>What makes it worse</b>", style_body),
         Paragraph("Turning my head to the <b>right</b>; tilting my neck <b>upward/back</b>", style_body)],
        [Paragraph("<b>What helps</b>", style_body),
         Paragraph("Upper cervical adjustment — relieves it about <b>70% of the time</b>", style_body)],
    ]
    symptoms_table = Table(symptoms_data, colWidths=[1.5*inch, 5.0*inch])
    symptoms_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
    ]))
    story.append(symptoms_table)

    # ── SECTION 2: WHY I THINK IT'S CERVICAL ──
    story.append(Paragraph("2. Why I Believe This Is a Cervical Alignment Issue", style_h2))

    story.append(Paragraph(
        "I have a hard time explaining exactly where this pain is every visit, so I put this together. "
        "The pain is sharp and nerve-like, and it responds to upper cervical adjustments — not muscle work. "
        "That tells me the <b>root cause is alignment</b>, not the muscles themselves.",
        style_body
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "When the upper cervical spine is properly aligned, this pain goes away. When it's not, the pain comes back. "
        "I'm not looking for muscle treatment or outside care — I believe in getting the alignment right "
        "and letting everything else fall into place from there.",
        style_body
    ))

    # ── SECTION 3: THE NERVE CONNECTION ──
    story.append(Paragraph("3. The Nerve That Connects Them", style_h2))

    story.append(Paragraph(
        "The <b>dorsal scapular nerve</b> runs from the cervical spine down to exactly where my pain is. "
        "It originates from the <b>C3, C4, and C5</b> nerve roots:",
        style_body
    ))

    # Nerve path diagram
    path_data = [
        [Paragraph("<b>C3 - C4 - C5 nerve roots</b> (cervical spine)", style_body)],
        [Paragraph("&darr;", style_body)],
        [Paragraph("Descends through the neck", style_body)],
        [Paragraph("&darr;", style_body)],
        [Paragraph("Runs along the <b>inner border of the shoulder blade</b>", style_body)],
        [Paragraph("&darr;", style_body)],
        [Paragraph("<b>= where my pain is</b>", style_body)],
    ]
    path_table = Table(path_data, colWidths=[5.5*inch])
    path_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), HexColor("#e8f0fe")),
        ("BACKGROUND", (0, 2), (0, 2), HexColor("#e8f0fe")),
        ("BACKGROUND", (0, 4), (0, 4), HexColor("#e8f0fe")),
        ("BACKGROUND", (0, 6), (0, 6), HexColor("#fef3c7")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("BOX", (0, 0), (-1, -1), 1, BLUE),
    ]))
    story.append(path_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "This is why upper cervical adjustments relieve the pain — correcting alignment at the top "
        "takes pressure off C3-C5 where this nerve originates. The shoulder blade pain is the <b>symptom</b>; "
        "the cervical misalignment is the <b>cause</b>.",
        style_body
    ))

    # ── SECTION 4: WHICH CERVICALS ──
    story.append(Paragraph("4. Which Cervicals Are Related", style_h2))

    cerv_data = [
        [Paragraph("<b>Level</b>", style_label),
         Paragraph("<b>Relevance to this pain</b>", style_label)],
        [Paragraph("<b>C1 / C2</b>", style_body),
         Paragraph("Upper cervical alignment — when corrected here, compensatory strain down the cervical spine is relieved. "
                    "This is where my adjustments happen.", style_body)],
        [Paragraph("<b>C3 / C4</b>", style_body),
         Paragraph("Contributing nerve roots to the dorsal scapular nerve. "
                    "When C1/C2 misalignment creates strain at these levels, it can irritate the nerve where it originates.", style_body)],
        [Paragraph("<b>C5</b>", style_body),
         Paragraph("Primary root of the dorsal scapular nerve. C5 is typically listed as the main origin, "
                    "but the C3-C4 contributions likely matter in my case since upper cervical work helps.", style_body)],
    ]
    cerv_table = Table(cerv_data, colWidths=[1.0*inch, 5.5*inch])
    cerv_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, 1), WHITE),
        ("BACKGROUND", (0, 2), (-1, 2), LIGHT_BG),
        ("BACKGROUND", (0, 3), (-1, 3), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("BOX", (0, 0), (-1, -1), 1, BLUE),
    ]))
    story.append(cerv_table)

    # ── SECTION 5: WHAT I'M ASKING FOR ──
    story.append(Paragraph("5. What I'm Asking For", style_h2))

    story.append(Paragraph(
        "I'm not looking for muscle work, stretches, or referrals. I believe in the upper cervical approach — "
        "get the alignment right and the body heals itself. What I need help with is:",
        style_body
    ))

    requests = [
        "<bullet>&bull;</bullet> <b>Locating the misalignment</b> — which cervical is out and in what direction?",
        "<bullet>&bull;</bullet> <b>Understanding the adjustment vector</b> — does the correction specifically decompress the C3-C5 nerve roots?",
        "<bullet>&bull;</bullet> <b>Why it works ~70% of the time</b> — what might explain the 30% where adjustment doesn't fully relieve this pain?",
        "<bullet>&bull;</bullet> <b>Consistency</b> — anything I can do (posture, sleeping position) to hold the adjustment longer between visits?",
    ]
    for r in requests:
        story.append(Paragraph(r, style_bullet))

    # ── SECTION 6: HOW I'D DESCRIBE IT ──
    story.append(Spacer(1, 8))
    story.append(Paragraph("6. In My Own Words", style_h2))

    quote_style = ParagraphStyle(
        "QuoteBox", fontName="Helvetica-Oblique", fontSize=10.5,
        textColor=DARK, leading=15,
        leftIndent=16, rightIndent=16,
        spaceBefore=4, spaceAfter=4
    )

    quote_content = [
        [Paragraph(
            '"I get a sharp pain along the inner edge of my right shoulder blade. It\'s not muscular — '
            'it feels like a nerve. It gets worse when I turn my head right or tilt my neck back. '
            'When I get my upper cervical adjustment and it\'s done right, this pain goes away. '
            'I think it\'s the <b>dorsal scapular nerve</b> being affected by misalignment at <b>C3-C5</b>, '
            'and correcting at C1/C2 relieves the strain downstream. I just need help pinpointing '
            'exactly where my alignment is off so we can get this one right."',
            quote_style
        )]
    ]
    quote_table = Table(quote_content, colWidths=[6.2*inch])
    quote_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#fef3c7")),
        ("BOX", (0, 0), (-1, -1), 1.5, AMBER),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(quote_table)

    # ── SECTION 7: VISIT NOTES ──
    story.append(Spacer(1, 12))
    story.append(Paragraph("7. Notes", style_h2))
    story.append(Paragraph("(Space for notes during the visit)", style_small))

    notes_data = []
    for _ in range(6):
        notes_data.append([""])
    notes_table = Table(notes_data, colWidths=[6.5*inch], rowHeights=[0.35*inch]*6)
    notes_table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(notes_table)

    # Footer
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=6))
    story.append(Paragraph(
        "<i>This document was prepared to help communicate pain location and history to my chiropractor. "
        "All clinical decisions are made by the treating provider.</i>",
        ParagraphStyle("Footer", fontName="Helvetica-Oblique", fontSize=7.5, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    print(f"PDF saved to: {output_path}")

if __name__ == "__main__":
    build_pdf()

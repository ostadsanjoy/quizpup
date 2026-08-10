import os
from html import escape
from fpdf import FPDF

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "fonts")


def render_summary_html(structured_summary):
    parts = []
    for ch in structured_summary:
        if ch.get("chapter"):
            parts.append(f"<h4>{escape(ch['chapter'])}</h4>")
        for t in ch.get("topics", []):
            if t.get("heading"):
                parts.append(f"<strong>{escape(t['heading'])}</strong>")
            parts.append(f"<ul>{''.join(f'<li>{escape(b)}</li>' for b in t.get('bullets', []))}</ul>")
    return "\n".join(parts)


def generate_pdf_bytes(title, structured_summary):
    pdf = FPDF(format="A4")
    pdf.add_font("DejaVu", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 15)
    pdf.multi_cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(180, 146, 134)
    pdf.line(15, pdf.get_y(), pdf.w - 15, pdf.get_y())
    pdf.ln(3)

    with pdf.text_columns(ncols=2, gutter=8, text_align="LEFT", line_height=1.2) as cols:
        for chapter in structured_summary:
            if chapter.get("chapter"):
                pdf.set_font("DejaVu", "B", 9.5)
                cols.write(text=f"{chapter['chapter']}\n")
            for topic in chapter.get("topics", []):
                if topic.get("heading"):
                    pdf.set_font("DejaVu", "B", 8)
                    cols.write(text=f"{topic['heading']}\n")
                pdf.set_font("DejaVu", "", 7.5)
                for bullet in topic.get("bullets", []):
                    with cols.paragraph(bullet_string="\u2022", indent=4, bottom_margin=1) as par:
                        par.write(bullet)

    return bytes(pdf.output())
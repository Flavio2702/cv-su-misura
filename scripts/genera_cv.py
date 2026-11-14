"""Genera un CV in PDF da un file Markdown con la struttura dei CV master.

Uso, dalla radice del progetto:
  python scripts/genera_cv.py INPUT.md OUTPUT.pdf

Il testo dopo "## Note d'uso" non finisce nel PDF. Il comando si ferma se
restano marcatori [DA CONFERMARE] o se OUTPUT esiste già.
"""
import re
import sys
import io
from html import escape
from pathlib import Path
from urllib.parse import urlparse

try:
    from reportlab.lib.colors import HexColor
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph, SimpleDocTemplate
except ImportError:
    raise SystemExit('Dipendenze PDF mancanti: python -m pip install -r requirements.txt')

COLORE = HexColor("#173B42")
STILI = {
    "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=23, leading=27, textColor=COLORE, spaceAfter=3),
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceAfter=4),
    "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=9, leading=12, spaceAfter=4),
    "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=COLORE, spaceBefore=8, spaceAfter=3),
    "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=9.5, leading=12, spaceBefore=6, spaceAfter=2),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9, leading=11.8, spaceAfter=2),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=11.8, leftIndent=10, firstLineIndent=-8, spaceAfter=1.5),
}


def inline(testo):
    """Converte grassetti e link Markdown nel markup di ReportLab."""
    testo = escape(testo.strip(), quote=True)
    testo = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", testo)
    def link(match):
        if urlparse(match[2]).scheme not in {'https', 'http', 'mailto'}:
            raise ValueError('Link non supportato: usare https, http o mailto')
        return f'<a href="{match[2]}" color="#173B42"><u>{match[1]}</u></a>'
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, testo)


def costruisci(markdown):
    corpo = markdown.split("## Note d'uso")[0]
    if not corpo.strip().startswith('# ') or corpo.count('\n# ') > 0:
        raise ValueError('Serve una sola intestazione # Nome all’inizio del CV')
    if re.search(r'\[(?:DA |INSERIRE)|filecite', corpo, flags=re.I):
        raise ValueError('Nel testo restano marcatori da completare')
    try:
        corpo.encode('cp1252')
    except UnicodeEncodeError:
        raise ValueError('Caratteri non supportati dal font base: usare Canva o testo latino senza emoji') from None
    storia, nome = [], ""
    righe = [r for r in corpo.splitlines() if r.strip() and r.strip() != "---"]
    for i, riga in enumerate(righe):
        if riga.startswith("### "):
            storia.append(Paragraph(inline(riga[4:]), STILI["role"]))
        elif riga.startswith("## "):
            storia.append(Paragraph(inline(riga[3:]).upper(), STILI["section"]))
        elif riga.startswith("# "):
            nome = riga[2:].strip()
            storia.append(Paragraph(inline(nome), STILI["name"]))
        elif riga.startswith("- "):
            storia.append(Paragraph("• " + inline(riga[2:]), STILI["bullet"]))
        elif i == 1:
            storia.append(Paragraph(inline(riga).replace("<b>", "").replace("</b>", ""), STILI["title"]))
        elif i == 2:
            storia.append(Paragraph(inline(riga), STILI["contact"]))
        else:
            storia.append(Paragraph(inline(riga), STILI["body"]))
    if not nome or len(righe) < 4:
        raise ValueError('CV incompleto: inserire nome, titolo, contatti e contenuto')
    return storia, nome


def genera(sorgente, destinazione):
    sorgente, destinazione = Path(sorgente), Path(destinazione)
    if destinazione.exists() or sorgente.resolve() == destinazione.resolve():
        raise ValueError('Destinazione già esistente: usare un nome nuovo')
    storia, _ = costruisci(sorgente.read_text(encoding='utf-8'))
    buffer = io.BytesIO()
    SimpleDocTemplate(
        buffer, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=28, bottomMargin=24,
        title='Curriculum vitae', author='', subject='', creator='cv-su-misura', invariant=1,
    ).build(storia)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    with destinazione.open('xb') as stream:
        stream.write(buffer.getvalue())


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sorgente, destinazione = Path(sys.argv[1]), Path(sys.argv[2])
    if destinazione.exists():
        sys.exit(f"Fermo: esiste già {destinazione}. Usa un nome nuovo.")
    try:
        genera(sorgente, destinazione)
    except (ValueError, OSError) as error:
        sys.exit(f'Generazione non completata: {error}')
    print("creato", destinazione)


if __name__ == "__main__":
    main()

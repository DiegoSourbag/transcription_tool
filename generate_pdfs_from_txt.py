from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Folder paths
COMBINED_FOLDER = Path("combined_transcripts")
PDF_OUTPUT_FOLDER = Path("combined_transcripts_pdfs")
PDF_OUTPUT_FOLDER.mkdir(exist_ok=True)

# Styles
styles = getSampleStyleSheet()
normal_style = ParagraphStyle(
    'NormalWithSpacing',
    parent=styles['Normal'],
    fontSize=11,
    leading=14,
    spaceAfter=6,
)

speaker_style = ParagraphStyle(
    'Speaker',
    parent=styles['Normal'],
    fontSize=12,
    leading=16,
    spaceBefore=10,
    spaceAfter=4,
    fontName='Helvetica-Bold',
)

def create_pdf_from_txt(txt_path, pdf_path):
    with txt_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        elif stripped.startswith("@"):
            elements.append(Paragraph(stripped[1:], speaker_style))  # Speaker name
        else:
            elements.append(Paragraph(stripped, normal_style))       # Dialogue

    doc.build(elements)
    print(f"📄 PDF created: {pdf_path.name}")

def main():
    txt_files = COMBINED_FOLDER.glob("*.txt")
    for txt_file in txt_files:
        pdf_file = PDF_OUTPUT_FOLDER / f"{txt_file.stem}.pdf"
        if pdf_file.exists():
            print(f"⏭️ Skipping {pdf_file.name}, already exists.")
            continue
        create_pdf_from_txt(txt_file, pdf_file)

if __name__ == "__main__":
    main()

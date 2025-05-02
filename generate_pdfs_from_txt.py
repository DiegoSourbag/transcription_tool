from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# Folder paths
COMBINED_FOLDER = Path("combined_transcripts")
PDF_OUTPUT_FOLDER = Path("combined_transcripts_pdfs")
PDF_OUTPUT_FOLDER.mkdir(exist_ok=True)

def create_pdf_from_txt(txt_path, pdf_path):
    with txt_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4
    x, y = 2 * cm, height - 2 * cm
    line_height = 12  # Points

    for line in lines:
        if y < 2 * cm:
            c.showPage()
            y = height - 2 * cm

        c.drawString(x, y, line.strip())
        y -= line_height

    c.save()
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

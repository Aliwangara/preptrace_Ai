import pdfplumber
from docx import document


def extract_text_from_cv(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber .open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = document(file_path)
        for para in doc.paragraphs:
            text +=para.text + "\n"

    return text.lower()
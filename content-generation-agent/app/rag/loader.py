import os
from typing import List, Dict, Any

from pypdf import PdfReader
from docx import Document


# =========================
# TXT
# =========================
def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


# =========================
# PDF (TEXTE GLOBAL - COMPATIBILITÉ)
# =========================
def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)


# =========================
# PDF (PAR PAGE - NOUVEAU)
# =========================
def load_pdf_pages(file_path: str) -> List[Dict[str, Any]]:
    """
    Charge un PDF page par page pour permettre les citations (source + page).
    """
    reader = PdfReader(file_path)
    pages = []

    for index, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            pages.append({
                "page": index + 1,   # pages commencent à 1
                "text": page_text.strip()
            })

    return pages


# =========================
# DOCX
# =========================
def load_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


# =========================
# LOADER GÉNÉRIQUE (INCHANGÉ)
# =========================
def load_document(file_path: str) -> str:
    """
    Load document text depending on file extension.
    (Conservé pour compatibilité)
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return load_txt(file_path)

    if ext == ".pdf":
        return load_pdf(file_path)

    if ext == ".docx":
        return load_docx(file_path)

    raise ValueError(f"Unsupported document type: {ext}")

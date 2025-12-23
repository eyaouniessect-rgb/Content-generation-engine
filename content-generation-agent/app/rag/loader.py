import os
from typing import Optional

from pypdf import PdfReader
from docx import Document


def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        if page.extract_text():
            text.append(page.extract_text())
    return "\n".join(text)


def load_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)


def load_document(file_path: str) -> str:
    """
    Load document text depending on file extension.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return load_txt(file_path)

    if ext == ".pdf":
        return load_pdf(file_path)

    if ext == ".docx":
        return load_docx(file_path)

    raise ValueError(f"Unsupported document type: {ext}")

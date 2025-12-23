import os

from app.rag.loader import load_document, load_pdf_pages
from app.rag.chunker import chunk_text
from app.rag.chroma_store import upsert_document


def ingest_document(doc_id: str, file_path: str) -> None:
    ext = os.path.splitext(file_path)[1].lower()
    source = os.path.basename(file_path)
    
    global_chunk_index = 0  # 🔹 Compteur global

    if ext == ".pdf":
        pages = load_pdf_pages(file_path)

        for page in pages:
            page_number = page["page"]
            page_text = page["text"]
            chunks = chunk_text(page_text)

            for chunk in chunks:
                upsert_document(
                    doc_id=doc_id,
                    text=chunk,
                    metadata={
                        "source": source,
                        "page": page_number,
                        "doc_id": doc_id,
                        "chunk_index": global_chunk_index  # 🔹 AJOUTÉ
                    }
                )
                global_chunk_index += 1  # 🔹 Incrémentation

    else:
        text = load_document(file_path)
        chunks = chunk_text(text)

        for chunk in chunks:
            upsert_document(
                doc_id=doc_id,
                text=chunk,
                metadata={
                    "source": source,
                    "page": None,
                    "doc_id": doc_id,
                    "chunk_index": global_chunk_index  # 🔹 AJOUTÉ
                }
            )
            global_chunk_index += 1  # 🔹 Incrémentation
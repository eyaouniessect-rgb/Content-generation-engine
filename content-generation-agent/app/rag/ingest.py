from app.rag.loader import load_document
from app.rag.chunker import chunk_text
from app.rag.chroma_store import upsert_document

def ingest_document(doc_id: str, file_path: str) -> None:
    text = load_document(file_path)
    chunks = chunk_text(text)
    upsert_document(doc_id, chunks)

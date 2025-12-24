import os

from app.rag.loader import load_document, load_pdf_pages
from app.rag.chunker import chunk_text
from app.rag.chroma_store import upsert_document


def ingest_document(
    doc_id: str,
    file_path: str,
    extra_metadata: dict = None
) -> None:
    """
    Ingest a document into ChromaDB with optional enriched metadata.
    
    Args:
        doc_id: Unique document identifier
        file_path: Path to the document file
        extra_metadata: Optional dict with title, authors, published, etc.
    """
    ext = os.path.splitext(file_path)[1].lower()
    source = os.path.basename(file_path)
    
    # Métadonnées de base
    base_metadata = {
        "source": source,
        "doc_id": doc_id,
    }
    
    # Fusion avec les métadonnées supplémentaires
    if extra_metadata:
        # ✅ Convertir les listes en strings pour ChromaDB
        sanitized_metadata = {}
        for key, value in extra_metadata.items():
            if isinstance(value, list):
                # Joindre les éléments avec " | "
                sanitized_metadata[key] = " | ".join(str(v) for v in value)
            else:
                sanitized_metadata[key] = value
        
        base_metadata.update(sanitized_metadata)
    
    global_chunk_index = 0

    if ext == ".pdf":
        pages = load_pdf_pages(file_path)

        for page in pages:
            page_number = page["page"]
            page_text = page["text"]
            chunks = chunk_text(page_text)

            for chunk in chunks:
                # Métadonnées complètes pour ce chunk
                chunk_metadata = {
                    **base_metadata,
                    "page": page_number,
                    "chunk_index": global_chunk_index
                }
                
                upsert_document(
                    doc_id=doc_id,
                    text=chunk,
                    metadata=chunk_metadata
                )
                global_chunk_index += 1

    else:
        text = load_document(file_path)
        chunks = chunk_text(text)

        for chunk in chunks:
            chunk_metadata = {
                **base_metadata,
                "page": None,
                "chunk_index": global_chunk_index
            }
            
            upsert_document(
                doc_id=doc_id,
                text=chunk,
                metadata=chunk_metadata
            )
            global_chunk_index += 1
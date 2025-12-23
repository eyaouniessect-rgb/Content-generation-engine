from __future__ import annotations

import os
from typing import List, Dict, Any, Optional

import chromadb
from chromadb.config import Settings

from app.rag.embeddings import embed_texts, embed_query


# =========================
# ChromaDB setup
# =========================
PERSIST_DIR = os.path.join("app", "storage", "chroma_db")

_client = chromadb.PersistentClient(
    path=PERSIST_DIR,
    settings=Settings(anonymized_telemetry=False),
)

_collection = _client.get_or_create_collection(name="documents")


# =========================
# UPSERT (avec metadata)
# =========================
def upsert_document(
    doc_id: str,
    text: str,
    metadata: Dict[str, Any]
) -> None:
    """
    Store ONE chunk into ChromaDB with metadata (source, page, doc_id).
    """
    embedding = embed_texts([text])[0]

    chunk_index = metadata.get("chunk_index", 0)

    chunk_id = f"{doc_id}_chunk_{chunk_index}"

    _collection.upsert(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
    )


# =========================
# QUERY
# =========================
def query_top_k(
    query: str,
    k: int = 5,
    doc_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Retrieve top-k chunks with metadata.
    """
    q_emb = embed_query(query)
    where = {"doc_id": doc_id} if doc_id else None

    res = _collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    results = []
    for doc, meta, dist in zip(docs, metas, dists):
        results.append({
            "text": doc,
            "metadata": meta,
            "score": dist,
        })

    return results

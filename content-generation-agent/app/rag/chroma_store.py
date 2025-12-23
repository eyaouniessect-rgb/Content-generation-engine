from __future__ import annotations

import os
from typing import List, Optional

import chromadb
from chromadb.config import Settings

from app.rag.embeddings import embed_texts, embed_query


# Dossier de persistance (tu peux le changer si tu veux)
PERSIST_DIR = os.path.join("app", "storage", "chroma_db")

_client = chromadb.PersistentClient(
    path=PERSIST_DIR,
    settings=Settings(anonymized_telemetry=False),
)

_collection = _client.get_or_create_collection(name="documents")


def upsert_document(doc_id: str, chunks: List[str]) -> None:
    """
    Index a document into ChromaDB (store text + embeddings + metadata).
    doc_id is used to filter later at query time.
    """
    embeddings = embed_texts(chunks)

    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]

    # upsert (add/update)
    _collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )




def query_top_k(query: str, k: int = 5, doc_id: Optional[str] = None) -> List[str]:
    """
    Retrieve top-k chunks, optionally filtered by doc_id.
    """
    q_emb = embed_query(query)

    where = {"doc_id": doc_id} if doc_id else None

    res = _collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        where=where,
    )

    # Chroma returns list-of-lists
    docs = res.get("documents", [[]])[0]
    return docs

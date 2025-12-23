import numpy as np
from app.rag.embeddings import embed_texts, embed_query


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_top_k(
    query: str,
    chunks: list[str],
    k: int = 3
) -> list[str]:
    """
    Retrieve top-k most similar chunks using cosine similarity.
    """
    chunk_embeddings = embed_texts(chunks)
    query_embedding = embed_query(query)

    scores = [
        cosine_similarity(query_embedding, emb)
        for emb in chunk_embeddings
    ]

    top_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    return [chunks[i] for i in top_indices]

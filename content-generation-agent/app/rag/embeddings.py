from sentence_transformers import SentenceTransformer

# Chargé une seule fois
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of texts using a local model.
    """
    return _model.encode(texts, convert_to_numpy=True).tolist()


def embed_query(query: str) -> list[float]:
    """
    Generate embedding for a query string.
    """
    return _model.encode([query], convert_to_numpy=True)[0].tolist()

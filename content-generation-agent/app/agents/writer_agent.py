from app.graph.state import ContentState
from app.services.llm_service import generate_text


def build_prompt(
    question: str,
    retrieved_chunks: list[dict] | None
) -> str:
    """
    Build the final prompt depending on whether RAG is active or not.
    """

    # 🟢 Cas 1 — Pas de document → LLM normal
    if retrieved_chunks is None:
        return question

    # 🔵 Cas 2 — Document fourni MAIS info absente
    if not retrieved_chunks:
        return f"""
Le document fourni ne contient pas d'information permettant
de répondre à la question suivante :

QUESTION:
{question}

Réponds clairement que l'information n'est pas disponible
dans le document.
"""

    # 🔵 Cas 3 — RAG actif avec contenu (avec source + page)
    context_blocks = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        text = chunk["text"]
        meta = chunk["metadata"]
        source = meta.get("source")
        page = meta.get("page")

        label = f"[SOURCE {i} | {source}"
        if page is not None:
            label += f" | page {page}"
        label += "]"

        context_blocks.append(
            f"{label}\n{text}"
        )

    context = "\n\n".join(context_blocks)

    return f"""
Tu es un assistant qui répond STRICTEMENT
en te basant sur le CONTEXTE ci-dessous.

CONTEXTE:
{context}

QUESTION:
{question}

RÈGLES IMPORTANTES:
- Utilise uniquement les informations du CONTEXTE.
- Tu peux utiliser les définitions implicites ou classifications clairement indiquées dans le document.
- Si la réponse n'est pas présente, dis-le clairement.
- N'utilise aucune connaissance externe.
- Donne une réponse complète (2 à 6 phrases) et pédagogique.
- Si possible, ajoute 2 puces "À retenir".
- Termine par une section "Sources" en citant [SOURCE X | ...].
"""


def writer_node(state: ContentState) -> ContentState:
    question = state["prompt"]
    retrieved_chunks = state.get("retrieved_chunks")

    final_prompt = build_prompt(question, retrieved_chunks)

    generated = generate_text(final_prompt)

    # 🔹 Construction des sources (source + page)
    sources = []
    seen = set()

    if retrieved_chunks:
        for chunk in retrieved_chunks:
            meta = chunk["metadata"]
            key = (meta.get("source"), meta.get("page"))

            if key not in seen:
                seen.add(key)
                sources.append({
                    "source": meta.get("source"),
                    "page": meta.get("page")
                })

    state["generated_text"] = generated
    state["sources"] = sources

    return state

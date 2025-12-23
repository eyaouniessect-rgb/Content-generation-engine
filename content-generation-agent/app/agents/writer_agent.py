from app.graph.state import ContentState
from app.services.llm_service import generate_text


def build_prompt(
    question: str,
    retrieved_chunks: list[str] | None
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

    # 🔵 Cas 3 — RAG actif avec contenu
    context = "\n\n".join(f"- {chunk}" for chunk in retrieved_chunks)

    return f"""
Tu es un assistant qui répond STRICTEMENT
en te basant sur le CONTEXTE ci-dessous.

CONTEXTE:
{context}

QUESTION:
{question}

RÈGLES IMPORTANTES:
- Utilise uniquement les informations du CONTEXTE.
- Si la réponse n'est pas présente, dis-le clairement.
- N'utilise aucune connaissance externe.
"""


def writer_node(state: ContentState) -> ContentState:
    question = state["prompt"]
    retrieved_chunks = state.get("retrieved_chunks")

    final_prompt = build_prompt(question, retrieved_chunks)

    generated = generate_text(final_prompt)

    state["generated_text"] = generated
    return state

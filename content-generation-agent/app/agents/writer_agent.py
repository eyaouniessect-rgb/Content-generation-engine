from app.graph.state import ContentState
from app.services.llm_service import generate_text


def build_prompt(
    question: str,
    retrieved_chunks: list[dict] | None
) -> str:
    """
    Build the final prompt depending on whether RAG is active or not.
    """

    #  Cas 1 — Pas de document → LLM normal
    if retrieved_chunks is None:
        return question

    # Cas 2 — Document fourni MAIS info absente
    if not retrieved_chunks:
        return f"""
Le document fourni ne contient pas d'information permettant
de répondre à la question suivante :

QUESTION:
{question}

Réponds clairement que l'information n'est pas disponible
dans le document.
"""

    #  Cas 3 — RAG actif avec contenu (avec métadonnées enrichies)
    context_blocks = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        text = chunk["text"]
        meta = chunk["metadata"]
        
        # Extraction des métadonnées
        source = meta.get("source")
        page = meta.get("page")
        title = meta.get("title")
        authors = meta.get("authors")
        published = meta.get("published")

        # Construction du label enrichi
        label_parts = [f"SOURCE {i}"]
        
        if title:
            label_parts.append(f'"{title}"')
        
        label_parts.append(source)
        
        if page is not None:
            label_parts.append(f"page {page}")
        
        if authors:
            # Convertir la string en liste si nécessaire
            if isinstance(authors, str):
                author_list = authors.split(" | ")
            else:
                author_list = [authors]
            
            # Limiter à 3 premiers auteurs
            if len(author_list) > 3:
                author_str = ", ".join(author_list[:3]) + " et al."
            else:
                author_str = ", ".join(author_list)
            label_parts.append(f"({author_str})")
        
        if published:
            label_parts.append(f"[{published[:4]}]")  # Année seulement

        label = " | ".join(label_parts)
        
        context_blocks.append(
            f"[{label}]\n{text}"
        )

    context = "\n\n".join(context_blocks)

    return f"""
Tu es un expert en intelligence artificielle et modèles multimodaux.
Réponds de manière technique et détaillée en te basant STRICTEMENT
sur le CONTEXTE ci-dessous.

CONTEXTE:
{context}

QUESTION:
{question}

RÈGLES IMPORTANTES:
- Utilise UNIQUEMENT les informations du CONTEXTE fourni
- Cite les modèles, architectures et techniques spécifiques mentionnés
- Structure ta réponse de manière claire et pédagogique
- N'utilise AUCUNE connaissance externe au contexte

FORMAT DE RÉPONSE:
1. Introduction (2-3 phrases de synthèse)
2. Points principaux (3-5 points détaillés avec exemples concrets du contexte)
3. Section "À retenir" (2-3 puces essentielles)
4. Section "Sources" citant [SOURCE X | ...]

Si la réponse n'est pas dans le contexte, dis-le clairement.
"""


def writer_node(state: ContentState) -> ContentState:
    question = state["prompt"]
    retrieved_chunks = state.get("retrieved_chunks")

    final_prompt = build_prompt(question, retrieved_chunks)

    generated = generate_text(final_prompt)

    # 🔹 Construction des sources enrichies
    sources = []
    seen = set()

    if retrieved_chunks:
        for chunk in retrieved_chunks:
            meta = chunk["metadata"]
            
            # Clé unique basée sur source + page
            key = (meta.get("source"), meta.get("page"))

            if key not in seen:
                seen.add(key)
                sources.append({
                    "source": meta.get("source"),
                    "page": meta.get("page"),
                    "title": meta.get("title"),
                    "authors": meta.get("authors"),
                    "published": meta.get("published"),
                    "doc_id": meta.get("doc_id")
                })

    state["generated_text"] = generated
    state["sources"] = sources

    return state
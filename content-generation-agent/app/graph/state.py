from typing import Optional, List, Dict, Any
from typing_extensions import TypedDict


class SourceMetadata(TypedDict, total=False):
    """Metadata for a source document."""
    source: str
    page: Optional[int]
    title: Optional[str]
    authors: Optional[List[str]]
    published: Optional[str]
    doc_id: Optional[str]


class ContentState(TypedDict, total=False):
    """
    Shared state for the content generation workflow.
    This state is passed between LangGraph nodes (agents).
    """

    # =========================
    # Input
    # =========================
    prompt: str
    document: Optional[str]

    # =========================
    # RAG
    # =========================
    retrieved_chunks: List[Dict[str, Any]]
    sources: List[SourceMetadata]  # ✅ Typé avec les métadonnées enrichies

    # =========================
    # Text generation
    # =========================
    generated_text: Optional[str]

    # =========================
    # Image generation
    # =========================
    image_prompt: Optional[str]
    image_path: Optional[str]
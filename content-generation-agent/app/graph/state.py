from typing import Optional, List, Dict, Any
from typing_extensions import TypedDict


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
    sources: List[Dict[str, Any]]  # [{ "source": str, "page": int | None }]

    # =========================
    # Text generation
    # =========================
    generated_text: Optional[str]

    # =========================
    # Image generation
    # =========================
    image_prompt: Optional[str]
    image_path: Optional[str]

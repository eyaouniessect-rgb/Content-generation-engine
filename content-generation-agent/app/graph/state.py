from typing import Optional, List
from typing_extensions import TypedDict


class ContentState(TypedDict):
    """
    Shared state for the content generation workflow.
    This state is passed between LangGraph nodes (agents).
    """

    # Input
    prompt: str
    document: Optional[str]

    # RAG
    retrieved_chunks: Optional[List[str]]

    # Text generation
    generated_text: Optional[str]

    # Image generation
    image_prompt: Optional[str]
    image_path: Optional[str]

from app.graph.state import ContentState
from app.rag.chroma_store import query_top_k

def retrieval_node(state: ContentState) -> ContentState:
    query = state["prompt"]
    doc_id = state.get("document")  # on va utiliser state["document"] comme doc_id

    top_chunks = query_top_k(query=query, k=5, doc_id=doc_id)

    state["retrieved_chunks"] = top_chunks
    return state

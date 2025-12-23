from app.graph.state import ContentState

def router_node(state: ContentState) -> ContentState:
    """
    Router node: does not modify the state,
    only prepares the decision step.
    """
    return state


def route_decision(state: ContentState) -> str:
    """
    Decide the next step in the graph.
    - If a document is provided → go to retrieval (RAG)
    - Otherwise → go directly to writer
    """
    document = state.get("document")

    if document:
        return "retrieval"
    else:
        return "writer"

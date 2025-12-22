from app.graph.state import ContentState

def router_node(state: ContentState) -> ContentState:
    # Pour l'instant: ne fait rien, juste passe le state
    return state

def route_decision(state: ContentState) -> str:
    """
    Décide où aller après router.
    Pour l'instant: toujours vers writer.
    (Plus tard: si document => RAG, sinon writer)
    """
    return "writer"

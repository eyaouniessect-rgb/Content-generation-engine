from app.graph.state import ContentState

def writer_node(state: ContentState) -> ContentState:
    # Version simple (sans LLM) juste pour tester le graph
    prompt = state["prompt"]
    state["generated_text"] = f"✅ (TEST) Contenu généré pour: {prompt}"
    return state

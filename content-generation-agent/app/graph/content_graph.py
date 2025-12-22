from langgraph.graph import StateGraph, END
from app.graph.state import ContentState

# Import des nodes (agents)
from app.agents.router_agent import router_node, route_decision
from app.agents.writer_agent import writer_node


def build_graph():
    """
    Build and compile the LangGraph workflow.
    """
    graph = StateGraph(ContentState)

    # Nodes
    graph.add_node("router", router_node)
    graph.add_node("writer", writer_node)

    # Entry point
    graph.set_entry_point("router")

    # Conditional routing:
    # route_decision returns either "writer" or END
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "writer": "writer",
            "end": END,
        },
    )

    # After writer -> END
    graph.add_edge("writer", END)

    return graph.compile()

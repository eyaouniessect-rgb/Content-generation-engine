from fastapi import APIRouter
from pydantic import BaseModel
from app.graph.content_graph import build_graph

router = APIRouter()
graph = build_graph()

class GenerateRequest(BaseModel):
    prompt: str

@router.post("/generate")
def generate_content(payload: GenerateRequest):
    initial_state = {
        "prompt": payload.prompt,
        "document": None,
        "retrieved_chunks": None,
        "generated_text": None,
        "image_prompt": None,
        "image_path": None,
    }
    result = graph.invoke(initial_state)
    return result

from fastapi import APIRouter , UploadFile, File
from pydantic import BaseModel
from app.graph.content_graph import build_graph
import os
import hashlib
from app.rag.ingest import ingest_document

router = APIRouter()
graph = build_graph()

class GenerateRequest(BaseModel):
    prompt: str
    document: str | None = None  # doc_id

@router.post("/generate")
def generate_content(payload: GenerateRequest):
    initial_state = {
        "prompt": payload.prompt,
        "document": payload.document,  # doc_id ou None
        "retrieved_chunks": None,
        "generated_text": None,
        "image_prompt": None,
        "image_path": None,
    }
    result = graph.invoke(initial_state)
    return result

@router.post("/ingest")
def ingest(file: UploadFile = File(...)):
    content = file.file.read()
    doc_id = hashlib.sha256(content).hexdigest()[:16]  # id stable

    uploads_dir = os.path.join("app", "storage", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    original_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(uploads_dir, f"{doc_id}{original_ext}")

    with open(file_path, "wb") as f:
        f.write(content)

    ingest_document(doc_id=doc_id, file_path=file_path)

    return {"doc_id": doc_id, "stored_as": file_path}


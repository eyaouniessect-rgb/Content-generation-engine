from fastapi import APIRouter , UploadFile, File
from pydantic import BaseModel
from app.graph.content_graph import build_graph
import os
import hashlib
from app.rag.ingest import ingest_document
from sources.arxiv_client import search_arxiv, download_pdf
from typing import Optional


router = APIRouter()
# Construction du graphe d'agents UNE SEULE FOIS au démarrage
graph = build_graph()

class GenerateRequest(BaseModel):
    prompt: str
    document: Optional[str] = None
   

@router.post("/generate")
def generate_content(payload: GenerateRequest):
    initial_state = {
        "prompt": payload.prompt,
        "document": payload.document,  # doc_id ou None
        "retrieved_chunks": None,    # Rempli par le retrieval agent
        "generated_text": None,      # Rempli par le writer agent

    }

    # Lancement du pipeline RAG / agents
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

@router.post("/arxiv/generate")
def generate_from_arxiv(payload: GenerateRequest):
    # 1. Recherche arXiv
    papers = search_arxiv(payload.prompt, max_results=3)

    # 2. Download + ingest auto avec métadonnées enrichies
    for paper in papers:
        pdf_path = download_pdf(
            arxiv_id=paper["arxiv_id"],
            pdf_url=paper["pdf_url"]
        )
        
        # ✅ Passer les métadonnées du paper
        ingest_document(
            doc_id=paper["arxiv_id"],
            file_path=pdf_path,
            extra_metadata={
                "title": paper["title"],
                "authors": paper["authors"],
                "published": paper["published"],
                "summary": paper["summary"]
            }
        )

    # 3. Pipeline avec RAG
    initial_state = {
        "prompt": payload.prompt,
        "document": "all",
        "retrieved_chunks": [],
        "generated_text": None,
    }

    result = graph.invoke(initial_state)
    return result

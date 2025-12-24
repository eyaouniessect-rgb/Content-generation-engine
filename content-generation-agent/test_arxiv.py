from sources.arxiv_client import search_arxiv, download_pdf
from app.rag.ingest import ingest_document

query = "multimodal large language models"

papers = search_arxiv(query, max_results=3)

for paper in papers:
    print(f"Téléchargement : {paper['title']}")
    pdf_path = download_pdf(
        arxiv_id=paper["arxiv_id"],
        pdf_url=paper["pdf_url"]
    )
    
    if pdf_path:
        print(f"Ingestion de {paper['arxiv_id']}...")
        ingest_document(doc_id=paper["arxiv_id"], file_path=pdf_path)
        print("✓ Terminé\n")
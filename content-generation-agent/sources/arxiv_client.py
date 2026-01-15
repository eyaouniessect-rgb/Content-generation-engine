from __future__ import annotations

import os
import re
import requests
import feedparser
from typing import List, Dict

# =========================
# Configuration
# =========================

ARXIV_API_URL = "http://export.arxiv.org/api/query"
PDF_DIR = os.path.join("app", "storage", "arxiv_papers")

os.makedirs(PDF_DIR, exist_ok=True)

# =========================
# Utils
# =========================

def clean_query(query: str) -> str:
    """
    Nettoie une requête utilisateur pour l'API arXiv
    - enlève ponctuation, accents simples, caractères spéciaux
    - normalise les espaces
    """
    query = query.lower()
    query = re.sub(r"[^\w\s]", "", query)   # enlève ?, accents, ponctuation
    query = re.sub(r"\s+", " ", query).strip()
    return query


# =========================
# arXiv Search
# =========================

def search_arxiv(
    query: str,
    max_results: int = 5
) -> List[Dict]:
    """
    Search articles on arXiv and return metadata.
    """

    cleaned_query = clean_query(query)

    params = {
        "search_query": f"all:{cleaned_query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    try:
        response = requests.get(ARXIV_API_URL, params=params, timeout=10)
    except requests.RequestException as e:
        print("❌ arXiv request failed:", e)
        return []

    if response.status_code != 200:
        print("❌ arXiv error:", response.status_code, response.text)
        return []

    feed = feedparser.parse(response.text)

    results: List[Dict] = []

    for entry in feed.entries:
        arxiv_id = entry.id.split("/")[-1]

        pdf_url = next(
            (link.href for link in entry.links if link.type == "application/pdf"),
            None
        )

        if not pdf_url:
            continue

        results.append({
            "arxiv_id": arxiv_id,
            "title": entry.title,
            "summary": entry.summary,
            "authors": [a.name for a in entry.authors],
            "pdf_url": pdf_url,
            "published": entry.published,
        })

    return results


# =========================
# PDF Download
# =========================

def download_pdf(arxiv_id: str, pdf_url: str) -> str:
    """
    Download arXiv PDF and return local file path.
    """

    file_path = os.path.join(PDF_DIR, f"{arxiv_id}.pdf")

    if os.path.exists(file_path):
        return file_path  # already downloaded

    try:
        response = requests.get(pdf_url, timeout=20)
    except requests.RequestException as e:
        print("❌ PDF download failed:", e)
        return ""

    if response.status_code != 200:
        print("❌ PDF download error:", response.status_code)
        return ""

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path

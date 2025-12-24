# app/sources/arxiv_client.py

from __future__ import annotations

import os
import requests
import feedparser
from typing import List, Dict

ARXIV_API_URL = "http://export.arxiv.org/api/query"
PDF_DIR = os.path.join("app", "storage", "arxiv_papers")

os.makedirs(PDF_DIR, exist_ok=True)


def search_arxiv(
    query: str,
    max_results: int = 5
) -> List[Dict]:
    """
    Search articles on arXiv and return metadata.
    """
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    response = requests.get(ARXIV_API_URL, params=params, timeout=10)
    response.raise_for_status()

    feed = feedparser.parse(response.text)

    results = []

    for entry in feed.entries:
        arxiv_id = entry.id.split("/")[-1]

        results.append({
            "arxiv_id": arxiv_id,
            "title": entry.title,
            "summary": entry.summary,
            "authors": [a.name for a in entry.authors],
            "pdf_url": next(
                link.href for link in entry.links if link.type == "application/pdf"
            ),
            "published": entry.published,
        })

    return results


def download_pdf(arxiv_id: str, pdf_url: str) -> str:
    """
    Download arXiv PDF and return local file path.
    """
    file_path = os.path.join(PDF_DIR, f"{arxiv_id}.pdf")

    if os.path.exists(file_path):
        return file_path  # already downloaded

    response = requests.get(pdf_url, timeout=20)
    response.raise_for_status()

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path

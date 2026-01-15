# ⚡ GUIDE RAPIDE - APPELS ENTRE FICHIERS

## 🔄 QUAND UNE REQUÊTE ARRIVE, QUELS FICHIERS SONT APPELÉS?

### SCÉNARIO 1: Upload + Génération

```
1. client/src/App.js
   └─> handleFileUpload()
       └─> POST /ingest
           │
           ▼
2. app/api/routes.py
   └─> @router.post("/ingest")
       └─> ingest_document(doc_id, file_path)
           │
           ▼
3. app/rag/ingest.py
   ├─> load_document() OU load_pdf_pages()
   │   └─> app/rag/loader.py
   │
   ├─> chunk_text()
   │   └─> app/rag/chunker.py
   │
   ├─> embed_texts()
   │   └─> app/rag/embeddings.py
   │
   └─> upsert_document()
       └─> app/rag/chroma_store.py
           └─> app/rag/embeddings.py (pour embedding)

───────────────────────────────────────

4. client/src/App.js
   └─> handleGenerate()
       └─> POST /generate
           │
           ▼
5. app/api/routes.py
   └─> @router.post("/generate")
       └─> graph.invoke(initial_state)
           │
           ▼
6. app/graph/content_graph.py
   └─> build_graph() (graphe déjà construit)
       └─> Entry: "router"
           │
           ▼
7. app/agents/router_agent.py
   ├─> router_node(state) → passe l'état
   └─> route_decision(state) → "retrieval"
       │
       ▼
8. app/agents/retrieval_agent.py
   └─> retrieval_node(state)
       └─> query_top_k(query, k=5, doc_id)
           └─> app/rag/chroma_store.py
               ├─> embed_query(query)
               │   └─> app/rag/embeddings.py
               └─> _collection.query() → ChromaDB
       │
       ▼
9. app/agents/writer_agent.py
   └─> writer_node(state)
       ├─> build_prompt(question, retrieved_chunks)
       └─> generate_text(prompt)
           └─> app/services/llm_service.py
               └─> genai.GenerativeModel() → Gemini API
       │
       ▼
10. Retour à routes.py → JSON response → Frontend
```

---

### SCÉNARIO 2: Recherche arXiv

```
1. client/src/App.js
   └─> handleGenerate() (mode arxiv)
       └─> POST /arxiv/generate
           │
           ▼
2. app/api/routes.py
   └─> @router.post("/arxiv/generate")
       ├─> search_arxiv(prompt, max_results=3)
       │   └─> sources/arxiv_client.py
       │       └─> requests.get(ARXIV_API_URL)
       │
       ├─> download_pdf(arxiv_id, pdf_url) × 3
       │   └─> sources/arxiv_client.py
       │       └─> requests.get(pdf_url) → Sauvegarde PDF
       │
       ├─> ingest_document(arxiv_id, pdf_path, extra_metadata) × 3
       │   └─> app/rag/ingest.py
       │       └─> (même flux que Scénario 1, ingestion)
       │
       └─> graph.invoke(initial_state)
           └─> (même flux que Scénario 1, génération)
```

---

## 📋 TABLEAU RÉCAPITULATIF DES APPELS

| Fichier Appelant | Fichier Appelé | Fonction/Méthode |
|------------------|----------------|------------------|
| `main.py` | `routes.py` | `include_router(router)` |
| `routes.py` | `content_graph.py` | `build_graph()` (1x au démarrage) |
| `routes.py` | `ingest.py` | `ingest_document()` |
| `routes.py` | `arxiv_client.py` | `search_arxiv()`, `download_pdf()` |
| `content_graph.py` | `router_agent.py` | `router_node()`, `route_decision()` |
| `content_graph.py` | `retrieval_agent.py` | `retrieval_node()` |
| `content_graph.py` | `writer_agent.py` | `writer_node()` |
| `retrieval_agent.py` | `chroma_store.py` | `query_top_k()` |
| `writer_agent.py` | `llm_service.py` | `generate_text()` |
| `ingest.py` | `loader.py` | `load_document()`, `load_pdf_pages()` |
| `ingest.py` | `chunker.py` | `chunk_text()` |
| `ingest.py` | `chroma_store.py` | `upsert_document()` |
| `chroma_store.py` | `embeddings.py` | `embed_texts()`, `embed_query()` |
| `App.js` | API Backend | `POST /ingest`, `POST /generate`, `POST /arxiv/generate` |

---

## 🗂️ ORGANISATION PAR RÔLE

### ENTRY POINTS (Point d'entrée)
- `app/main.py` - Démarrage FastAPI
- `client/src/index.js` - Démarrage React
- `client/src/App.js` - Composant principal React

### ROUTING (Routage)
- `app/api/routes.py` - Routes HTTP
- `app/graph/content_graph.py` - Routage dans le graphe
- `app/agents/router_agent.py` - Décision de routage

### ORCHESTRATION (Orchestration)
- `app/graph/content_graph.py` - Construction du graphe LangGraph
- `app/graph/state.py` - Structure de l'état

### AGENTS (Agents)
- `app/agents/router_agent.py` - Agent de routage
- `app/agents/retrieval_agent.py` - Agent de récupération RAG
- `app/agents/writer_agent.py` - Agent de génération

### RAG PIPELINE (Pipeline RAG)
- `app/rag/ingest.py` - Orchestration de l'indexation
- `app/rag/loader.py` - Chargement de documents
- `app/rag/chunker.py` - Découpage en chunks
- `app/rag/embeddings.py` - Génération d'embeddings
- `app/rag/chroma_store.py` - Interface ChromaDB

### SERVICES EXTERNES (Services externes)
- `app/services/llm_service.py` - Interface Gemini
- `sources/arxiv_client.py` - Interface arXiv

---

## 🔍 DÉTAIL DES IMPORTATIONS

### routes.py
```python
from app.graph.content_graph import build_graph
from app.rag.ingest import ingest_document
from sources.arxiv_client import search_arxiv, download_pdf
```

### content_graph.py
```python
from app.graph.state import ContentState
from app.agents.router_agent import router_node, route_decision
from app.agents.writer_agent import writer_node
from app.agents.retrieval_agent import retrieval_node
```

### retrieval_agent.py
```python
from app.graph.state import ContentState
from app.rag.chroma_store import query_top_k
```

### writer_agent.py
```python
from app.graph.state import ContentState
from app.services.llm_service import generate_text
```

### ingest.py
```python
from app.rag.loader import load_document, load_pdf_pages
from app.rag.chunker import chunk_text
from app.rag.chroma_store import upsert_document
```

### chroma_store.py
```python
from app.rag.embeddings import embed_texts, embed_query
```

---

## 🎯 ORDRE D'EXÉCUTION TYPE

### Au démarrage du serveur:
1. `main.py` s'exécute
2. `routes.py` s'importe → `build_graph()` appelé 1x
3. Graphe compilé et stocké en mémoire
4. Serveur FastAPI prêt

### Lors d'un POST /ingest:
1. `routes.py` → `ingest_document()`
2. `ingest.py` → `loader.py` → `chunker.py` → `embeddings.py` → `chroma_store.py`

### Lors d'un POST /generate:
1. `routes.py` → `graph.invoke()`
2. `content_graph.py` → `router_node()` → `route_decision()`
3. Si RAG: `retrieval_node()` → `chroma_store.py` → `embeddings.py`
4. `writer_node()` → `llm_service.py` → Gemini API
5. Retour JSON → Frontend

---

## 💡 POINTS CLÉS À RETENIR

1. **Le graphe est construit UNE SEULE FOIS** au démarrage (pas à chaque requête)
2. **Les embeddings utilisent un modèle local** (SentenceTransformer) - pas d'API
3. **ChromaDB est persistant** - les données restent entre les redémarrages
4. **Trois chemins possibles** dans le graphe:
   - Router → Writer (pas de document)
   - Router → Retrieval → Writer (avec document)
   - Router → Writer (si retrieved_chunks déjà présent)
5. **Les métadonnées sont enrichies** uniquement pour arXiv (extra_metadata)

---

FIN DU GUIDE RAPIDE ⚡


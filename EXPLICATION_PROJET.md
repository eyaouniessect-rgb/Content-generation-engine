# 📚 EXPLICATION COMPLÈTE DU PROJET ARXIPULSE

## 🎯 Vue d'ensemble du projet

**ArxiPulse** est un système de veille technologique intelligent qui utilise l'IA pour analyser automatiquement les publications arXiv et vos documents personnels. Le projet combine:
- **Backend Python** (FastAPI) avec des agents LangGraph
- **Frontend React** (interface utilisateur moderne)
- **RAG (Retrieval-Augmented Generation)** avec ChromaDB
- **Intégration arXiv** pour les publications scientifiques

---

## 🔄 FLUX COMPLET DU PROJET

### **PARTIE 1: DÉMARRAGE DE L'APPLICATION**

```
1. Frontend (React)
   └─> client/src/index.js
       └─> Charge App.js
           └─> Affiche la page d'accueil (HomePage)

2. Backend (FastAPI)
   └─> content-generation-agent/app/main.py
       └─> Crée l'application FastAPI
       └─> Configure CORS (pour permettre les requêtes du frontend)
       └─> Importe les routes depuis app/api/routes.py
       └─> Construit le graphe d'agents UNE SEULE FOIS au démarrage
           └─> app/graph/content_graph.py → build_graph()
```

---

## 📂 STRUCTURE DES FICHIERS ET LEURS RÔLES

### **BACKEND PYTHON**

#### 1. **Point d'entrée: `app/main.py`**
**Rôle:** Configuration de l'API FastAPI
- Crée l'application FastAPI
- Configure le middleware CORS (permet les requêtes depuis localhost:3000)
- Inclut les routes de l'API
- Endpoint `/health` pour vérifier que l'API fonctionne

**Code clé:**
```python
app = FastAPI(...)
app.add_middleware(CORSMiddleware, ...)
app.include_router(router)  # Routes définies dans routes.py
```

---

#### 2. **Routes API: `app/api/routes.py`**
**Rôle:** Définit tous les endpoints de l'API

**Endpoints disponibles:**

**a) POST `/generate`**
- **But:** Génère du contenu à partir d'un prompt et d'un document (optionnel)
- **Flux:**
  1. Reçoit `prompt` et `document` (doc_id) dans le body
  2. Crée un état initial avec ces données
  3. Lance le graphe d'agents: `graph.invoke(initial_state)`
  4. Retourne le résultat final

**b) POST `/ingest`**
- **But:** Téléverse et indexe un document dans ChromaDB
- **Flux:**
  1. Reçoit un fichier (PDF, TXT, etc.)
  2. Génère un `doc_id` unique (hash SHA256)
  3. Sauvegarde le fichier dans `app/storage/uploads/`
  4. Appelle `ingest_document()` pour indexer le contenu
  5. Retourne le `doc_id` pour utilisation ultérieure

**c) POST `/arxiv/generate`**
- **But:** Recherche sur arXiv, télécharge les PDFs, puis génère du contenu
- **Flux:**
  1. Recherche sur arXiv avec le prompt: `search_arxiv(prompt, max_results=3)`
  2. Pour chaque article trouvé:
     - Télécharge le PDF: `download_pdf()`
     - Indexe avec métadonnées enrichies: `ingest_document()` (avec title, authors, published, summary)
  3. Lance le graphe d'agents avec `document: "all"` (recherche dans tous les documents)

**Code clé:**
```python
graph = build_graph()  # Construit UNE SEULE FOIS au démarrage

@router.post("/generate")
def generate_content(payload: GenerateRequest):
    initial_state = {
        "prompt": payload.prompt,
        "document": payload.document,
        "retrieved_chunks": None,
        "generated_text": None,
    }
    result = graph.invoke(initial_state)  # Lance le pipeline
    return result
```

---

#### 3. **Graphe d'agents: `app/graph/content_graph.py`**
**Rôle:** Orchestre le workflow avec LangGraph

**Architecture du graphe:**
```
ENTRY POINT: "router"
    ↓
[ROUTER AGENT] → Décide quel chemin prendre
    ↓
    ├─> Si document fourni → "retrieval" (RAG)
    │       ↓
    │   [RETRIEVAL AGENT] → Récupère les chunks pertinents
    │       ↓
    │   [WRITER AGENT] → Génère la réponse avec contexte
    │       ↓
    │   END
    │
    └─> Si pas de document → "writer" (direct)
            ↓
        [WRITER AGENT] → Génère la réponse sans RAG
            ↓
        END
```

**Fonction `build_graph()`:**
- Crée un `StateGraph` avec `ContentState`
- Ajoute 3 nodes: `router`, `writer`, `retrieval`
- Configure les edges conditionnels (routage)
- Compile et retourne le graphe

**Code clé:**
```python
graph = StateGraph(ContentState)
graph.add_node("router", router_node)
graph.add_node("writer", writer_node)
graph.add_node("retrieval", retrieval_node)
graph.set_entry_point("router")

# Routage conditionnel
graph.add_conditional_edges("router", route_decision, {...})
graph.add_edge("retrieval", "writer")
graph.add_edge("writer", END)
```

---

#### 4. **État partagé: `app/graph/state.py`**
**Rôle:** Définit la structure de données partagée entre les agents

**ContentState (TypedDict):**
```python
{
    "prompt": str,                    # Question de l'utilisateur
    "document": Optional[str],        # doc_id ou None
    "retrieved_chunks": List[Dict],   # Chunks récupérés par RAG
    "generated_text": Optional[str],  # Réponse finale générée
    "sources": List[SourceMetadata]   # Métadonnées des sources utilisées
}
```

**SourceMetadata:**
- `source`: nom du fichier
- `page`: numéro de page (si PDF)
- `title`: titre (si arXiv)
- `authors`: auteurs (si arXiv)
- `published`: date de publication (si arXiv)
- `doc_id`: identifiant du document

---

#### 5. **AGENT 1: Router (`app/agents/router_agent.py`)**
**Rôle:** Décide quel chemin prendre dans le graphe

**Fonction `router_node()`:**
- Ne modifie pas l'état
- Prépare la décision

**Fonction `route_decision()`:**
- **Si `document` est fourni OU `retrieved_chunks` existe:**
  → Route vers `"retrieval"` (active RAG)
- **Sinon:**
  → Route vers `"writer"` (génération directe sans RAG)

**Logique:**
```python
if document or retrieved is not None:
    return "retrieval"  # Active RAG
else:
    return "writer"     # Pas de RAG
```

---

#### 6. **AGENT 2: Retrieval (`app/agents/retrieval_agent.py`)**
**Rôle:** Récupère les chunks pertinents depuis ChromaDB

**Fonction `retrieval_node()`:**
1. Extrait `prompt` et `document` (doc_id) de l'état
2. Appelle `query_top_k(query, k=5, doc_id=doc_id)`
3. Stocke les résultats dans `state["retrieved_chunks"]`

**Structure des chunks récupérés:**
```python
[
    {
        "text": "contenu du chunk...",
        "metadata": {"source": "...", "page": 1, ...},
        "score": 0.85  # distance de similarité
    },
    ...
]
```

---

#### 7. **AGENT 3: Writer (`app/agents/writer_agent.py`)**
**Rôle:** Génère la réponse finale avec ou sans contexte RAG

**Fonction `build_prompt()`:**
Construit le prompt final selon 3 cas:

**Cas 1 - Pas de RAG (pas de chunks):**
```python
return question  # Prompt simple, LLM répond avec ses connaissances
```

**Cas 2 - RAG mais aucun chunk trouvé:**
```python
return "Le document ne contient pas d'information..."
```

**Cas 3 - RAG actif avec chunks:**
Construit un prompt enrichi avec:
- Contexte structuré (chunks avec métadonnées)
- Instructions pour utiliser UNIQUEMENT le contexte
- Format de réponse demandé (introduction, points principaux, sources)

**Fonction `writer_node()`:**
1. Appelle `build_prompt()` pour créer le prompt final
2. Appelle `generate_text(prompt)` via le service LLM
3. Construit la liste des `sources` (dédupliquées)
4. Stocke `generated_text` et `sources` dans l'état

**Extraction des sources:**
- Dédoublonne par (source, page)
- Conserve toutes les métadonnées (title, authors, published, etc.)

---

#### 8. **Service LLM: `app/services/llm_service.py`**
**Rôle:** Interface avec Google Gemini

**Fonction `generate_text()`:**
- Utilise `gemini-2.5-flash`
- Envoie le prompt et retourne la réponse textuelle
- Nécessite `GOOGLE_API_KEY` dans les variables d'environnement

---

### **SYSTÈME RAG (Retrieval-Augmented Generation)**

#### 9. **Ingestion de documents: `app/rag/ingest.py`**
**Rôle:** Indexe un document dans ChromaDB

**Fonction `ingest_document()`:**

**Flux complet:**
```
1. Charge le document
   └─> app/rag/loader.py
       ├─> PDF → load_pdf_pages() (par page)
       └─> Autres → load_document() (tout le texte)

2. Découpe en chunks
   └─> app/rag/chunker.py → chunk_text()
       └─> Divise en chunks de 500 mots avec overlap de 100

3. Génère les embeddings
   └─> app/rag/embeddings.py → embed_texts()
       └─> Utilise SentenceTransformer "all-MiniLM-L6-v2"

4. Stocke dans ChromaDB
   └─> app/rag/chroma_store.py → upsert_document()
       └─> Sauvegarde: texte + embedding + métadonnées
```

**Métadonnées stockées:**
- `source`: nom du fichier
- `doc_id`: identifiant unique
- `page`: numéro de page (si PDF)
- `chunk_index`: index du chunk
- `title`, `authors`, `published` (si arXiv)

---

#### 10. **Stockage ChromaDB: `app/rag/chroma_store.py`**
**Rôle:** Interface avec la base de données vectorielle

**Configuration:**
- Client persistant: `app/storage/chroma_db/`
- Collection: `"documents"`

**Fonctions principales:**

**a) `upsert_document()`:**
- Génère l'embedding du chunk
- Crée un `chunk_id` unique: `{doc_id}_chunk_{index}`
- Stocke: texte, embedding, métadonnées

**b) `query_top_k()`:**
- Génère l'embedding de la requête
- Si `doc_id` spécifié (et != "all"), filtre par document
- Effectue une recherche vectorielle (similarité cosinus)
- Retourne les k chunks les plus similaires avec scores

**Logique de filtrage:**
```python
if doc_id and doc_id not in ["all", "arxiv"]:
    where = {"doc_id": doc_id}  # Cherche dans un seul document
else:
    where = None  # Cherche dans tous les documents
```

---

#### 11. **Embeddings: `app/rag/embeddings.py`**
**Rôle:** Génère les embeddings vectoriels

**Modèle:** `sentence-transformers/all-MiniLM-L6-v2`
- Modèle local (pas besoin d'API)
- 384 dimensions
- Optimisé pour la similarité sémantique

**Fonctions:**
- `embed_texts()`: embeddings pour plusieurs textes
- `embed_query()`: embedding pour une requête

---

#### 12. **Découpage: `app/rag/chunker.py`**
**Rôle:** Découpe le texte en chunks

**Algorithme:**
- Taille par chunk: 500 mots
- Overlap: 100 mots (pour garder le contexte)
- Divise par mots (pas par caractères)

---

#### 13. **Chargement de documents: `app/rag/loader.py`**
**Rôle:** Extrait le texte de différents formats

**Formats supportés:**
- **PDF:** `PdfReader` (pypdf) - extraction page par page
- **TXT:** Lecture directe du fichier
- **DOCX:** `python-docx`

**Fonctions:**
- `load_pdf_pages()`: retourne liste de dicts `{page: int, text: str}`
- `load_document()`: retourne le texte complet

---

### **INTÉGRATION ARXIV**

#### 14. **Client arXiv: `sources/arxiv_client.py`**
**Rôle:** Interagit avec l'API arXiv

**Fonction `search_arxiv()`:**
1. Nettoie la requête (`clean_query()`)
2. Appelle l'API arXiv: `http://export.arxiv.org/api/query`
3. Parse le feed XML
4. Extrait pour chaque article:
   - `arxiv_id`
   - `title`
   - `summary`
   - `authors`
   - `pdf_url`
   - `published`

**Fonction `download_pdf()`:**
1. Vérifie si le PDF existe déjà localement
2. Télécharge depuis `pdf_url`
3. Sauvegarde dans `app/storage/arxiv_papers/`
4. Retourne le chemin local

---

### **FRONTEND REACT**

#### 15. **Point d'entrée: `client/src/index.js`**
**Rôle:** Démarre l'application React
- Rend le composant `App` dans `#root`

---

#### 16. **Composant principal: `client/src/App.js`**
**Rôle:** Interface utilisateur complète

**Composants internes:**

**a) `HomePage`:**
- Page d'accueil avec présentation
- Bouton "Démarrer ArxiPulse"

**b) `ModeSelector`:**
- Choix entre 2 modes:
  - **"arxiv"**: Recherche en temps réel sur arXiv
  - **"upload"**: Analyse de vos documents

**c) `UploadSection` (mode upload uniquement):**
- Upload de fichiers PDF
- Appelle `/ingest` pour indexer
- Stocke le `doc_id` reçu

**d) `QuerySection`:**
- Zone de saisie pour la question
- Options (afficher chunks, métadonnées)
- Bouton "Lancer l'analyse"
- Appelle `/generate` ou `/arxiv/generate` selon le mode

**e) `ResultsSection`:**
- 3 onglets:
  1. **Résultat:** Texte généré
  2. **Sources:** Liste des sources avec métadonnées
  3. **Analyse:** Chunks récupérés avec scores

**Flux de données frontend:**

```
1. Mode "arxiv":
   Utilisateur saisit question
   → Appelle POST /arxiv/generate
   → Backend recherche arXiv + télécharge + indexe + génère
   → Affiche résultats

2. Mode "upload":
   Utilisateur upload un PDF
   → Appelle POST /ingest
   → Reçoit doc_id
   → Utilisateur saisit question
   → Appelle POST /generate avec doc_id
   → Backend génère avec RAG
   → Affiche résultats
```

**État React:**
```javascript
{
  mode: 'arxiv' | 'upload',
  query: string,
  response: {generated_text, sources, retrieved_chunks},
  loading: boolean,
  uploadedFile: File,
  documentId: string  // Pour mode upload
}
```

---

## 🔄 FLUX COMPLET D'UNE REQUÊTE

### **Scénario 1: Génération avec document uploadé**

```
1. FRONTEND (App.js)
   ├─> Utilisateur upload un PDF
   └─> POST /ingest
       └─> Fichier sauvegardé + doc_id retourné

2. FRONTEND (App.js)
   ├─> Utilisateur saisit question
   └─> POST /generate
       Body: {prompt: "...", document: "doc_id_xyz"}

3. BACKEND (routes.py)
   └─> Crée initial_state
       └─> graph.invoke(initial_state)

4. GRAPHE (content_graph.py)
   └─> ENTRY: "router"

5. AGENT ROUTER (router_agent.py)
   ├─> router_node() → passe l'état
   └─> route_decision() → "retrieval" (car document fourni)

6. AGENT RETRIEVAL (retrieval_agent.py)
   ├─> query_top_k(query, k=5, doc_id="doc_id_xyz")
   │   └─> chroma_store.py
   │       ├─> embed_query(query)
   │       ├─> Recherche vectorielle dans ChromaDB
   │       └─> Retourne top 5 chunks
   └─> state["retrieved_chunks"] = chunks

7. AGENT WRITER (writer_agent.py)
   ├─> build_prompt(question, retrieved_chunks)
   │   └─> Construit prompt avec contexte RAG
   ├─> generate_text(prompt)
   │   └─> llm_service.py → Gemini API
   └─> state["generated_text"] = réponse
       state["sources"] = métadonnées sources

8. BACKEND (routes.py)
   └─> Retourne result (état final)

9. FRONTEND (App.js)
   └─> Affiche response.generated_text + response.sources
```

### **Scénario 2: Génération avec arXiv**

```
1. FRONTEND (App.js)
   ├─> Mode "arxiv" sélectionné
   └─> POST /arxiv/generate
       Body: {prompt: "modèles multimodaux"}

2. BACKEND (routes.py)
   ├─> search_arxiv("modèles multimodaux", max_results=3)
   │   └─> arxiv_client.py
   │       └─> Retourne liste de papers avec métadonnées
   │
   ├─> Pour chaque paper:
   │   ├─> download_pdf(arxiv_id, pdf_url)
   │   │   └─> Télécharge PDF localement
   │   │
   │   └─> ingest_document(arxiv_id, pdf_path, extra_metadata)
   │       └─> Indexe avec title, authors, published, summary
   │
   └─> graph.invoke({prompt: "...", document: "all"})

3. GRAPHE → ROUTER → RETRIEVAL → WRITER
   (même flux que Scénario 1, mais cherche dans TOUS les documents)

4. FRONTEND
   └─> Affiche résultats avec sources arXiv enrichies
```

---

## 📊 DIAGRAMME DE FLUX GLOBAL

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │ HomePage │ → │ App.js   │ → │ Results  │          │
│  └──────────┘    └──────────┘    └──────────┘          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ HTTP (POST /generate, /ingest, etc.)
                       │
┌──────────────────────▼──────────────────────────────────┐
│              BACKEND (FastAPI)                          │
│  ┌────────────────────────────────────────────┐        │
│  │  main.py                                   │        │
│  │  └─> routes.py                             │        │
│  │      ├─> POST /ingest                      │        │
│  │      │   └─> ingest_document()             │        │
│  │      │       ├─> loader.py                 │        │
│  │      │       ├─> chunker.py                │        │
│  │      │       ├─> embeddings.py             │        │
│  │      │       └─> chroma_store.py           │        │
│  │      │                                       │        │
│  │      ├─> POST /arxiv/generate              │        │
│  │      │   ├─> arxiv_client.py (search)      │        │
│  │      │   ├─> arxiv_client.py (download)    │        │
│  │      │   └─> graph.invoke()                │        │
│  │      │                                       │        │
│  │      └─> POST /generate                    │        │
│  │          └─> graph.invoke(initial_state)   │        │
│  │                                              │        │
│  └────────────────────────────────────────────┘        │
│                                                          │
│  ┌────────────────────────────────────────────┐        │
│  │  content_graph.py (LangGraph)              │        │
│  │                                            │        │
│  │  ENTRY → router_node()                    │        │
│  │           │                                │        │
│  │           ├─> route_decision()            │        │
│  │           │                                │        │
│  │           ├─> retrieval_node()            │        │
│  │           │   └─> query_top_k()           │        │
│  │           │       └─> chroma_store.py     │        │
│  │           │                                │        │
│  │           └─> writer_node()               │        │
│  │               ├─> build_prompt()          │        │
│  │               └─> generate_text()         │        │
│  │                   └─> llm_service.py      │        │
│  │                       └─> Gemini API      │        │
│  └────────────────────────────────────────────┘        │
│                                                          │
│  ┌────────────────────────────────────────────┐        │
│  │  ChromaDB (Storage)                        │        │
│  │  app/storage/chroma_db/                    │        │
│  │  - Documents indexés                       │        │
│  │  - Embeddings vectoriels                   │        │
│  │  - Métadonnées (source, page, title, etc.)│        │
│  └────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 POINTS CLÉS POUR LA PRÉSENTATION

### **Architecture générale:**
1. **Frontend/Backend séparés:** React (UI) + FastAPI (API)
2. **Agents orchestrés:** LangGraph coordonne 3 agents (router, retrieval, writer)
3. **RAG intégré:** ChromaDB pour la recherche vectorielle
4. **Double mode:** arXiv (en ligne) + Upload (local)

### **Technologies principales:**
- **LangGraph:** Orchestration d'agents avec workflow conditionnel
- **ChromaDB:** Base de données vectorielle (similarité sémantique)
- **Gemini API:** Génération de texte avec contexte
- **SentenceTransformers:** Embeddings locaux (pas d'API externe)
- **arXiv API:** Récupération automatique de publications

### **Points forts:**
- **Modularité:** Chaque agent a un rôle précis
- **Flexibilité:** Gère avec ou sans RAG automatiquement
- **Métadonnées enrichies:** Citations précises (source, page, auteurs)
- **Double source:** Documents locaux + arXiv en temps réel

---

## 📝 RÉSUMÉ DES FICHIERS PAR CATÉGORIE

### **Configuration & Entry Points**
- `app/main.py` - Application FastAPI
- `app/config.py` - Configuration (vide actuellement)
- `client/src/index.js` - Point d'entrée React

### **API Routes**
- `app/api/routes.py` - Tous les endpoints HTTP

### **Orchestration**
- `app/graph/content_graph.py` - Construction du graphe LangGraph
- `app/graph/state.py` - Structure de l'état partagé

### **Agents**
- `app/agents/router_agent.py` - Routage conditionnel
- `app/agents/retrieval_agent.py` - Récupération RAG
- `app/agents/writer_agent.py` - Génération de texte

### **RAG System**
- `app/rag/ingest.py` - Pipeline d'indexation
- `app/rag/chroma_store.py` - Interface ChromaDB
- `app/rag/loader.py` - Chargement de documents
- `app/rag/chunker.py` - Découpage en chunks
- `app/rag/embeddings.py` - Génération d'embeddings

### **Services**
- `app/services/llm_service.py` - Interface Gemini API

### **Sources externes**
- `sources/arxiv_client.py` - Client arXiv

### **Frontend**
- `client/src/App.js` - Interface utilisateur complète

---

**FIN DU DOCUMENT** 🎉


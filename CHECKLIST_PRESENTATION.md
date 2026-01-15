# ✅ CHECKLIST POUR LA PRÉSENTATION - ARXIPULSE

## 🎯 POINTS CLÉS À EXPLIQUER

### 1. VUE D'ENSEMBLE (2-3 min)
- [ ] **Qu'est-ce qu'ArxiPulse?**
  - Système de veille technologique intelligent
  - Analyse automatique d'arXiv + documents personnels
  - Réponses sourcées avec citations précises

- [ ] **Architecture générale:**
  - Frontend React (interface moderne)
  - Backend FastAPI (API REST)
  - Agents LangGraph (orchestration intelligente)
  - RAG avec ChromaDB (recherche vectorielle)

---

### 2. DEUX MODES DE FONCTIONNEMENT (3-4 min)

#### Mode 1: Upload de Documents
- [ ] Utilisateur upload un PDF/TXT
- [ ] Document indexé dans ChromaDB
- [ ] Question posée → RAG activé → Réponse basée sur le document

#### Mode 2: arXiv en Temps Réel
- [ ] Question posée → Recherche automatique sur arXiv
- [ ] Téléchargement des PDFs pertinents
- [ ] Indexation avec métadonnées enrichies (titre, auteurs, date)
- [ ] Génération avec contexte de tous les articles

---

### 3. ARCHITECTURE DES AGENTS (5-6 min)

#### Le Graphe LangGraph
- [ ] **3 agents orchestrés:**
  1. **ROUTER** → Décide le chemin (avec/sans RAG)
  2. **RETRIEVAL** → Récupère les chunks pertinents depuis ChromaDB
  3. **WRITER** → Génère la réponse avec contexte

- [ ] **Flux conditionnel:**
  ```
  ENTRY → ROUTER
           ├─> Si document → RETRIEVAL → WRITER
           └─> Si pas de document → WRITER (direct)
  ```

- [ ] **État partagé (ContentState):**
  - prompt, document, retrieved_chunks, generated_text, sources

---

### 4. SYSTÈME RAG - Récupération Augmentée (5-6 min)

#### A) Indexation (Ingestion)
- [ ] **Pipeline en 4 étapes:**
  1. **Loader** → Extrait le texte (PDF page par page, TXT direct)
  2. **Chunker** → Découpe en chunks de 500 mots (overlap 100)
  3. **Embeddings** → Génère vecteurs avec SentenceTransformer (local)
  4. **ChromaDB** → Stocke texte + embedding + métadonnées

#### B) Recherche (Retrieval)
- [ ] Question convertie en vecteur
- [ ] Recherche vectorielle (similarité cosinus)
- [ ] Top 5 chunks les plus pertinents retournés
- [ ] Métadonnées conservées (source, page, titre, auteurs, date)

---

### 5. GÉNÉRATION DE RÉPONSE (3-4 min)

#### Prompt Builder (dans Writer Agent)
- [ ] **3 cas gérés:**
  1. Pas de RAG → Prompt simple, LLM répond librement
  2. RAG sans résultats → Indique que l'info n'est pas dans le document
  3. RAG avec chunks → Prompt enrichi avec contexte structuré

#### Instructions au LLM
- [ ] Utiliser UNIQUEMENT le contexte fourni
- [ ] Citer les sources [SOURCE X | ...]
- [ ] Format structuré (introduction, points principaux, sources)

#### Service LLM
- [ ] Google Gemini 2.5 Flash
- [ ] API key via variables d'environnement

---

### 6. MÉTADONNÉES ENRICHIES (2-3 min)

#### Pour les documents uploadés
- [ ] source (nom fichier)
- [ ] page (numéro de page si PDF)
- [ ] doc_id (identifiant unique)

#### Pour les articles arXiv
- [ ] title (titre de l'article)
- [ ] authors (liste des auteurs)
- [ ] published (date de publication)
- [ ] summary (résumé de l'article)

#### Affichage dans le frontend
- [ ] Onglet "Sources" avec toutes les métadonnées
- [ ] Citations précises dans la réponse générée

---

### 7. DÉMONSTRATION (5-10 min)

#### Scénario 1: Upload de Document
- [ ] Uploader un PDF
- [ ] Poser une question
- [ ] Montrer le résultat avec sources
- [ ] Montrer les chunks récupérés (onglet Analyse)

#### Scénario 2: Recherche arXiv
- [ ] Poser une question générale
- [ ] Attendre la recherche + téléchargement
- [ ] Montrer le résultat avec sources arXiv enrichies

---

### 8. TECHNOLOGIES UTILISÉES (2-3 min)

- [ ] **LangGraph:** Orchestration d'agents avec workflow conditionnel
- [ ] **ChromaDB:** Base de données vectorielle (recherche sémantique)
- [ ] **SentenceTransformers:** Embeddings locaux (pas d'API)
- [ ] **Gemini API:** Génération de texte avec contexte
- [ ] **FastAPI:** API REST moderne et rapide
- [ ] **React:** Interface utilisateur réactive
- [ ] **arXiv API:** Récupération automatique de publications

---

### 9. POINTS FORTS / AVANTAGES (2-3 min)

- [ ] **Modularité:** Chaque agent a un rôle précis et testable
- [ ] **Flexibilité:** Gère automatiquement avec ou sans RAG
- [ ] **Précision:** Citations exactes avec numéros de pages
- [ ] **Double source:** Documents locaux + arXiv en temps réel
- [ ] **Métadonnées:** Enrichissement automatique pour arXiv
- [ ] **Scalabilité:** ChromaDB persistant, pas de perte de données

---

### 10. QUESTIONS POSSIBLES

#### "Comment fonctionne la recherche vectorielle?"
- [ ] Embeddings convertissent texte en vecteurs numériques
- [ ] Similarité cosinus entre vecteur question et vecteurs chunks
- [ ] Top k résultats = chunks les plus similaires sémantiquement

#### "Pourquoi utiliser des chunks avec overlap?"
- [ ] Overlap de 100 mots garde le contexte entre chunks
- [ ] Évite de couper une phrase/paragraphe au milieu
- [ ] Améliore la cohérence des résultats

#### "Que se passe-t-il si aucun chunk pertinent n'est trouvé?"
- [ ] Writer agent détecte le cas
- [ ] Génère un message indiquant que l'info n'est pas disponible
- [ ] Pas de réponse inventée

#### "Comment sont gérées les métadonnées pour arXiv?"
- [ ] Extraites de l'API arXiv (titre, auteurs, date, résumé)
- [ ] Passées à `ingest_document()` via `extra_metadata`
- [ ] Stockées avec chaque chunk dans ChromaDB
- [ ] Présentées dans l'interface utilisateur

---

## 📊 DIAGRAMMES À MONTRER

1. [ ] Diagramme général Frontend → Backend → Agents
2. [ ] Flux du graphe LangGraph (Router → Retrieval → Writer)
3. [ ] Pipeline d'indexation RAG (Loader → Chunker → Embeddings → DB)
4. [ ] Structure de ContentState

---

## 💡 ASTUCES POUR LA PRÉSENTATION

- [ ] **Commencez par la démo** → Plus impactant visuellement
- [ ] **Expliquez le flux en suivant une requête** → Du clic au résultat
- [ ] **Mettez l'accent sur les agents** → Point différenciant du projet
- [ ] **Montrez les métadonnées enrichies** → Démontre la valeur ajoutée
- [ ] **Parlez de la modularité** → Facilite les évolutions futures

---

## ⚠️ À NE PAS OUBLIER

- [ ] Mentionner que le graphe est construit UNE SEULE FOIS au démarrage
- [ ] Expliquer pourquoi ROUTER puis WRITER (pas directement WRITER)
- [ ] Clarifier la différence entre `document: doc_id` et `document: "all"`
- [ ] Mentionner que SentenceTransformer est local (pas d'API externe pour embeddings)
- [ ] Expliquer que ChromaDB est persistant (données conservées)

---

## 🎬 ORDRE DE PRÉSENTATION RECOMMANDÉ

1. **Introduction** (1 min) - Qu'est-ce qu'ArxiPulse?
2. **Démonstration** (5 min) - Montrer les deux modes
3. **Architecture générale** (3 min) - Frontend/Backend/Agents
4. **Flux détaillé** (5 min) - Suivre une requête complète
5. **Système RAG** (4 min) - Indexation + Recherche
6. **Agents LangGraph** (4 min) - Router/Retrieval/Writer
7. **Métadonnées enrichies** (2 min) - Sources et citations
8. **Technologies** (2 min) - Stack technique
9. **Questions** (4 min) - Réponses aux questions

**Total: ~30 minutes**

---

BONNE PRÉSENTATION! 🚀


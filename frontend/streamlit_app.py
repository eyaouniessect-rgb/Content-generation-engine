import streamlit as st
import requests
import json
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="RAG arXiv Generator",
    page_icon="📚",
    layout="wide"
)

# URL de l'API
API_URL = "http://localhost:8000"

# Titre principal
st.title("📚 arXiv Research Assistant")
st.markdown("Recherchez et générez du contenu basé sur les derniers articles arXiv")

# Sidebar pour les options
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Choix du mode
    mode = st.radio(
        "Mode de recherche",
        ["🔬 arXiv (auto)", "📄 Document uploadé"],
        help="arXiv télécharge automatiquement les papers, Document utilise vos fichiers"
    )
    
    st.divider()
    
    # Statistiques (optionnel)
    st.header("📊 Statistiques")
    if st.button("🔄 Rafraîchir stats"):
        try:
            response = requests.get(f"{API_URL}/debug/chunks")
            if response.status_code == 200:
                data = response.json()
                st.metric("Documents indexés", data.get("total", 0))
        except:
            st.warning("API non accessible")

# Zone principale
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Votre question")
    
    # Input pour la question
    user_query = st.text_area(
        "Posez votre question de recherche",
        placeholder="Ex: What are the main architectures used in multimodal large language models?",
        height=100
    )
    
    # Options avancées (collapsible)
    with st.expander("🔧 Options avancées"):
        show_chunks = st.checkbox("Afficher les chunks récupérés", value=True)
        show_metadata = st.checkbox("Afficher les métadonnées complètes", value=False)

with col2:
    st.header("🎯 Actions")
    
    # Upload de document (si mode Document)
    if mode == "📄 Document uploadé":
        uploaded_file = st.file_uploader(
            "Uploader un PDF",
            type=["pdf"],
            help="Le document sera indexé avant la recherche"
        )
        
        if uploaded_file and st.button("📤 Ingérer le document"):
            with st.spinner("Ingestion en cours..."):
                files = {"file": uploaded_file}
                response = requests.post(f"{API_URL}/ingest", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Document ingéré ! ID: {data['doc_id']}")
                    st.session_state['last_doc_id'] = data['doc_id']
                else:
                    st.error("❌ Erreur lors de l'ingestion")

# Bouton de génération
if st.button("🚀 Générer la réponse", type="primary", use_container_width=True):
    if not user_query.strip():
        st.warning("⚠️ Veuillez entrer une question")
    else:
        # Déterminer l'endpoint
        if mode == "🔬 arXiv (auto)":
            endpoint = f"{API_URL}/arxiv/generate"
            payload = {"prompt": user_query}
        else:
            endpoint = f"{API_URL}/generate"
            doc_id = st.session_state.get('last_doc_id')
            payload = {
                "prompt": user_query,
                "document": doc_id if doc_id else None
            }
        
        # Appel API avec spinner
        with st.spinner("🔍 Recherche en cours... (cela peut prendre 10-30 secondes pour arXiv)"):
            try:
                response = requests.post(endpoint, json=payload, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Affichage de la réponse générée
                    st.success("✅ Réponse générée avec succès !")
                    
                    # Onglets pour organiser l'affichage
                    tab1, tab2, tab3 = st.tabs(["📝 Réponse", "📚 Sources", "🔍 Détails"])
                    
                    with tab1:
                        st.markdown("### Réponse")
                        st.markdown(data.get("generated_text", "Aucune réponse générée"))
                    
                    with tab2:
                        st.markdown("### Sources citées")
                        sources = data.get("sources", [])
                        
                        if sources:
                            for i, source in enumerate(sources, 1):
                                with st.expander(f"📄 Source {i}: {source.get('title', source.get('source', 'N/A'))}"):
                                    col_a, col_b = st.columns(2)
                                    
                                    with col_a:
                                        st.write("**Fichier:**", source.get('source', 'N/A'))
                                        st.write("**Page:**", source.get('page', 'N/A'))
                                        st.write("**Doc ID:**", source.get('doc_id', 'N/A'))
                                    
                                    with col_b:
                                        if source.get('authors'):
                                            authors = source['authors'].split(' | ')
                                            st.write("**Auteurs:**", ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""))
                                        if source.get('published'):
                                            date = source['published'][:10]
                                            st.write("**Publié:**", date)
                        else:
                            st.info("Aucune source disponible (mode LLM pur)")
                    
                    with tab3:
                        if show_chunks and data.get("retrieved_chunks"):
                            st.markdown("### Chunks récupérés")
                            
                            for i, chunk in enumerate(data["retrieved_chunks"], 1):
                                with st.expander(f"Chunk {i} - Score: {chunk.get('score', 0):.4f}"):
                                    st.text_area(
                                        "Contenu",
                                        chunk.get("text", ""),
                                        height=150,
                                        key=f"chunk_{i}"
                                    )
                                    
                                    if show_metadata:
                                        st.json(chunk.get("metadata", {}))
                        else:
                            st.info("Aucun chunk récupéré ou option désactivée")
                        
                        # JSON brut
                        with st.expander("📋 Réponse JSON complète"):
                            st.json(data)
                
                else:
                    st.error(f"❌ Erreur API: {response.status_code}")
                    st.code(response.text)
            
            except requests.exceptions.Timeout:
                st.error("⏱️ Timeout: La requête a pris trop de temps")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Erreur de connexion: Vérifiez que l'API tourne sur http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🤖 Powered by FastAPI + ChromaDB + OpenAI | 📚 arXiv API</p>
</div>
""", unsafe_allow_html=True)
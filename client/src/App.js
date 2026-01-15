import React, { useState } from 'react';
import { Search, Upload, FileText, Database, Sparkles, ChevronDown, Loader2, BookOpen, Users, Calendar, ArrowRight, Zap, Shield, TrendingUp, CheckCircle2, Brain, Lightbulb, Target, Activity } from 'lucide-react';

// ============= COMPOSANT: Page d'accueil =============
const HomePage = ({ onStart }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-gray-50 to-neutral-100 relative overflow-hidden">
      {/* Effets de fond géométriques */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-20 -left-20 w-96 h-96 bg-gradient-to-r from-cyan-100 to-blue-100 rounded-full mix-blend-multiply blur-3xl opacity-60"></div>
        <div className="absolute -bottom-40 -right-20 w-96 h-96 bg-gradient-to-r from-emerald-100 to-teal-100 rounded-full mix-blend-multiply blur-3xl opacity-60"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-violet-100 to-purple-100 rounded-full mix-blend-multiply blur-3xl opacity-40"></div>
      </div>

      {/* Grille de fond */}
      <div className="absolute inset-0 bg-[linear-gradient(90deg,#f8fafc_1px,transparent_1px),linear-gradient(#f8fafc_1px,transparent_1px)] bg-[size:80px_80px] opacity-10"></div>

      {/* Contenu principal */}
      <div className="relative z-10">
        {/* Hero Section */}
        <div className="max-w-7xl mx-auto px-6 py-20">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* Colonne gauche - Texte */}
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 bg-white/80 backdrop-blur-sm border border-neutral-200 rounded-full px-4 py-2 text-sm shadow-sm">
                <Sparkles className="w-4 h-4 text-amber-500" />
                <span className="text-neutral-700 font-medium">Système de veille technologique intelligent</span>
              </div>

              <h1 className="text-5xl md:text-6xl font-bold leading-tight">
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-600 to-blue-600">
                  ArxiPulse
                </span>
                <span className="block mt-4 text-neutral-900 text-4xl md:text-5xl">
                  Le pouls de la recherche
                </span>
              </h1>

              <p className="text-xl text-neutral-600 leading-relaxed max-w-xl">
                Exploitez l'IA pour analyser automatiquement les publications arXiv et vos documents personnels avec une précision inégalée.
              </p>

              <div className="flex flex-wrap gap-4">
                <button
                  onClick={onStart}
                  className="group inline-flex items-center gap-3 bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-semibold px-8 py-4 rounded-xl hover:from-cyan-700 hover:to-blue-700 transition-all shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-95"
                >
                  Démarrer ArxiPulse
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
                

              </div>


            </div>

            {/* Colonne droite - Illustration */}
            <div className="relative">
              <div className="relative bg-white/80 backdrop-blur-xl rounded-3xl p-8 border border-neutral-200 shadow-2xl">
                {/* Illustration stylisée */}
                <div className="relative aspect-square">
                  <div className="absolute inset-0 flex items-center justify-center">
                    {/* Écran central avec logo ArxiPulse */}
                    <div className="w-4/5 h-4/5 bg-gradient-to-br from-neutral-900 to-neutral-800 rounded-2xl shadow-2xl border-2 border-neutral-700 overflow-hidden">
                      <div className="bg-gradient-to-r from-cyan-600 to-blue-600 h-8 flex items-center px-3 gap-2">
                        <div className="w-2 h-2 rounded-full bg-red-400"></div>
                        <div className="w-2 h-2 rounded-full bg-amber-400"></div>
                        <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
                      </div>
                      <div className="p-4 space-y-2">
                        <div className="h-3 bg-gradient-to-r from-cyan-500/30 to-blue-500/30 rounded animate-pulse"></div>
                        <div className="h-3 bg-gradient-to-r from-emerald-500/30 to-teal-500/30 rounded animate-pulse delay-100"></div>
                        <div className="h-3 bg-gradient-to-r from-violet-500/30 to-purple-500/30 rounded animate-pulse delay-200"></div>
                        <div className="h-20 bg-neutral-800/50 rounded-lg mt-4 flex flex-col items-center justify-center">
                          <div className="flex items-center gap-2 mb-2">
                            <Activity className="w-6 h-6 text-cyan-400 animate-pulse" />
                            <span className="text-cyan-400 font-bold text-xl">Arxi</span>
                            <span className="text-blue-400 font-bold text-xl">Pulse</span>
                          </div>
                          <Brain className="w-8 h-8 text-cyan-400 animate-pulse" />
                        </div>
                      </div>
                    </div>

                    {/* Éléments flottants */}
                    <div className="absolute -top-4 -right-4 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl p-3 shadow-lg animate-bounce">
                      <Lightbulb className="w-6 h-6 text-white" />
                    </div>
                    <div className="absolute -bottom-4 -left-4 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl p-3 shadow-lg animate-bounce delay-500">
                      <Target className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </div>

                {/* Badge "AI Powered" */}
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-amber-500 to-orange-500 text-white px-4 py-2 rounded-full text-sm font-semibold shadow-lg flex items-center gap-2">
                  <Sparkles className="w-4 h-4" />
                  Powered by AI
                </div>
              </div>

              {/* Points décoratifs */}
              <div className="absolute top-10 right-10 w-3 h-3 bg-cyan-400 rounded-full animate-ping"></div>
              <div className="absolute bottom-20 left-10 w-2 h-2 bg-emerald-400 rounded-full animate-ping delay-300"></div>
            </div>
          </div>
        </div>

        {/* Section Features */}
        <div className="max-w-7xl mx-auto px-6 py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-neutral-900 mb-4">
              Pourquoi choisir ArxiPulse ?
            </h2>
            <p className="text-neutral-600 text-lg">
              Une suite complète d'outils pour votre veille technologique
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Zap className="w-8 h-8 text-white" />,
                title: "Recherche en temps réel",
                desc: "Accédez instantanément aux dernières publications arXiv avec des analyses en direct",
                gradient: "from-cyan-500 to-blue-600",
                shadow: "shadow-cyan-500/20"
              },
              {
                icon: <Shield className="w-8 h-8 text-white" />,
                title: "Analyse sécurisée",
                desc: "Traitez vos documents sensibles localement avec une protection totale des données",
                gradient: "from-emerald-500 to-teal-600",
                shadow: "shadow-emerald-500/20"
              },
              {
                icon: <TrendingUp className="w-8 h-8 text-white" />,
                title: "Insights intelligents",
                desc: "Obtenez des réponses sourcées avec métadonnées complètes et analyses contextuelles",
                gradient: "from-violet-500 to-purple-600",
                shadow: "shadow-violet-500/20"
              }
            ].map((feature, idx) => (
              <div key={idx} className="group bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-neutral-200 hover:border-transparent transition-all hover:shadow-2xl hover:scale-[1.02]">
                <div className={`w-16 h-16 bg-gradient-to-br ${feature.gradient} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform shadow-lg`}>
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-semibold text-neutral-900 mb-3">{feature.title}</h3>
                <p className="text-neutral-600 leading-relaxed">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Section Technologies */}
        <div className="max-w-7xl mx-auto px-6 py-16 border-t border-neutral-200">
          <p className="text-center text-neutral-500 text-sm mb-6 uppercase tracking-wider">Technologies derrière ArxiPulse</p>
          <div className="flex flex-wrap justify-center gap-6">
            {['FastAPI', 'ChromaDB', 'Gemini AI', 'arXiv API'].map((tech, idx) => (
              <div key={idx} className="flex items-center gap-3 bg-white border border-neutral-200 px-6 py-3 rounded-xl hover:border-neutral-300 hover:shadow-md transition-all">
                <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                <span className="font-semibold text-neutral-700">{tech}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// ============= COMPOSANT: Header =============
const Header = ({ onHomeClick }) => {
  return (
    <header className="bg-white/90 backdrop-blur-sm border-b border-neutral-200 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <button 
          onClick={onHomeClick}
          className="flex items-center gap-3 hover:scale-105 transition-transform group"
        >
          <div className="w-11 h-11 bg-gradient-to-br from-cyan-600 to-blue-600 rounded-xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-shadow">
            <Activity className="w-6 h-6 text-white" />
          </div>
          <div className="text-left">
            <div className="flex items-baseline gap-2">
              <h1 className="text-xl font-bold text-neutral-900">
                <span className="text-cyan-600">Arxi</span>
                <span className="text-blue-600">Pulse</span>
              </h1>
              <span className="text-xs bg-gradient-to-r from-cyan-500 to-blue-500 text-white px-2 py-1 rounded-full font-bold">
                Beta
              </span>
            </div>
            <p className="text-xs text-neutral-500">Le pouls de la recherche scientifique</p>
          </div>
        </button>
      </div>
    </header>
  );
};

// ============= COMPOSANT: Mode Selector =============
const ModeSelector = ({ mode, setMode }) => {
  return (
    <div className="bg-white rounded-2xl shadow-lg border border-neutral-200 p-8 mb-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-cyan-600 to-blue-600 rounded-xl flex items-center justify-center">
            <Search className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-neutral-900">Mode de recherche</h2>
            <p className="text-sm text-neutral-500">Sélectionnez votre source d'information</p>
          </div>
        </div>
        <div className="text-sm bg-cyan-50 text-cyan-700 px-3 py-1 rounded-full border border-cyan-200">
          ArxiPulse
        </div>
      </div>
      <div className="grid grid-cols-2 gap-6">
        <button
          onClick={() => setMode('arxiv')}
          className={`group p-8 rounded-2xl border-2 transition-all duration-300 ${
            mode === 'arxiv'
              ? 'border-cyan-500 bg-gradient-to-br from-cyan-50 to-blue-50 shadow-lg scale-105'
              : 'border-neutral-200 bg-white hover:border-cyan-300 hover:shadow-md hover:scale-[1.02]'
          }`}
        >
          <Search className={`w-12 h-12 mb-4 transition-colors ${mode === 'arxiv' ? 'text-cyan-600' : 'text-neutral-400 group-hover:text-cyan-600'}`} />
          <h3 className={`font-bold text-xl mb-2 ${mode === 'arxiv' ? 'text-neutral-900' : 'text-neutral-700'}`}>
            Live arXiv
          </h3>
          <p className={`text-sm ${mode === 'arxiv' ? 'text-neutral-600' : 'text-neutral-500'}`}>
            Recherche en temps réel dans arXiv
          </p>
        </button>
        <button
          onClick={() => setMode('upload')}
          className={`group p-8 rounded-2xl border-2 transition-all duration-300 ${
            mode === 'upload'
              ? 'border-emerald-500 bg-gradient-to-br from-emerald-50 to-teal-50 shadow-lg scale-105'
              : 'border-neutral-200 bg-white hover:border-emerald-300 hover:shadow-md hover:scale-[1.02]'
          }`}
        >
          <Upload className={`w-12 h-12 mb-4 transition-colors ${mode === 'upload' ? 'text-emerald-600' : 'text-neutral-400 group-hover:text-emerald-600'}`} />
          <h3 className={`font-bold text-xl mb-2 ${mode === 'upload' ? 'text-neutral-900' : 'text-neutral-700'}`}>
            Mes Documents
          </h3>
          <p className={`text-sm ${mode === 'upload' ? 'text-neutral-600' : 'text-neutral-500'}`}>
            Analyse de vos propres documents
          </p>
        </button>
      </div>
    </div>
  );
};

// ============= COMPOSANT: Upload Section =============
const UploadSection = ({ uploadedFile, handleFileUpload, documentId }) => {
  return (
    <div className="bg-white rounded-2xl shadow-lg border border-neutral-200 p-8 mb-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center">
            <Upload className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-neutral-900">Importer un document</h2>
            <p className="text-sm text-neutral-500">Analysez vos propres fichiers avec ArxiPulse</p>
          </div>
        </div>
      </div>
      <label className="block">
        <div className="border-2 border-dashed border-neutral-300 rounded-2xl p-16 text-center hover:border-emerald-400 hover:bg-emerald-50/50 transition-all cursor-pointer group">
          <Upload className="w-20 h-20 text-neutral-400 group-hover:text-emerald-500 mx-auto mb-6 transition-all group-hover:scale-110" />
          <p className="text-neutral-900 font-bold mb-2 text-xl">
            {uploadedFile ? uploadedFile.name : 'Déposez votre PDF ici'}
          </p>
          <p className="text-sm text-neutral-500">Maximum 200MB • Format PDF uniquement</p>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            className="hidden"
          />
        </div>
      </label>
      {uploadedFile && (
        <div className="mt-4 p-4 bg-emerald-50 rounded-xl border border-emerald-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <FileText className="w-5 h-5 text-emerald-600" />
              <span className="text-emerald-700 font-medium">Document prêt pour l'analyse</span>
            </div>
            <span className="text-xs bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full">
              Prêt
            </span>
          </div>
          {documentId && (
            <div className="mt-3 text-sm">
              <p className="text-emerald-600 font-medium">
                ID du document : <span className="font-mono text-xs bg-emerald-100 px-2 py-1 rounded">{documentId}</span>
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// ============= COMPOSANT: Query Section =============
const QuerySection = ({ query, setQuery, loading, showChunks, setShowChunks, showMetadata, setShowMetadata, handleGenerate, mode, documentId }) => {
  return (
    <div className="bg-white rounded-2xl shadow-lg border border-neutral-200 p-8 mb-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-purple-500 rounded-xl flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-neutral-900">Votre question</h2>
            <p className="text-sm text-neutral-500">ArxiPulse va analyser et répondre</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-sm text-violet-600">
          <Brain className="w-4 h-4" />
          <span className="font-medium">IA Active</span>
        </div>
      </div>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ex: Quelles sont les architectures principales utilisées dans les modèles de langage multimodaux ?"
        className="w-full px-6 py-5 border-2 border-neutral-300 rounded-2xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none resize-none transition-all text-neutral-800 bg-neutral-50/50 text-base hover:border-neutral-400"
        rows="5"
      />
      
      <details className="mt-6 bg-neutral-50/80 rounded-xl p-4 border border-neutral-200">
        <summary className="cursor-pointer text-sm font-semibold text-neutral-700 flex items-center gap-2 hover:text-blue-600 transition-colors">
          <ChevronDown className="w-5 h-5" />
          Options d'analyse ArxiPulse
        </summary>
        <div className="mt-4 space-y-3 pl-7">
          <label className="flex items-center gap-3 text-sm text-neutral-600 hover:text-neutral-900 cursor-pointer">
            <input
              type="checkbox"
              checked={showChunks}
              onChange={(e) => setShowChunks(e.target.checked)}
              className="rounded border-neutral-300 text-blue-600 focus:ring-blue-500 w-5 h-5"
            />
            <span className="font-medium">Afficher les extraits analysés</span>
          </label>
          <label className="flex items-center gap-3 text-sm text-neutral-600 hover:text-neutral-900 cursor-pointer">
            <input
              type="checkbox"
              checked={showMetadata}
              onChange={(e) => setShowMetadata(e.target.checked)}
              className="rounded border-neutral-300 text-blue-600 focus:ring-blue-500 w-5 h-5"
            />
            <span className="font-medium">Afficher les métadonnées détaillées</span>
          </label>
        </div>
      </details>

      <button
        onClick={handleGenerate}
        disabled={loading || !query.trim()}
        className="mt-8 w-full bg-gradient-to-r from-blue-600 to-violet-600 text-white font-bold py-5 px-8 rounded-2xl hover:from-blue-700 hover:to-violet-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-3 text-lg group"
      >
        {loading ? (
          <>
            <Loader2 className="w-7 h-7 animate-spin" />
            <span>ArxiPulse analyse...</span>
          </>
        ) : (
          <>
            <div className="relative">
              <Activity className="w-7 h-7 group-hover:animate-pulse" />
            </div>
            <span>Lancer l'analyse ArxiPulse</span>
          </>
        )}
      </button>
    </div>
  );
};

// ============= COMPOSANT: Results Section =============
const ResultsSection = ({ response, activeTab, setActiveTab, showChunks, showMetadata }) => {
  return (
    <div className="bg-white rounded-2xl shadow-lg border border-neutral-200 overflow-hidden">
      <div className="border-b border-neutral-200 flex bg-gradient-to-r from-neutral-50 to-blue-50/50">
        {[
          { id: 'response', label: 'Résultat', icon: <FileText className="w-6 h-6" /> },
          { id: 'sources', label: `Sources (${response.sources?.length || 0})`, icon: <BookOpen className="w-6 h-6" /> },
          { id: 'details', label: 'Analyse', icon: <Database className="w-6 h-6" /> }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-8 py-5 font-semibold transition-all flex items-center gap-3 ${
              activeTab === tab.id
                ? 'text-blue-700 border-b-4 border-blue-600 bg-white'
                : 'text-neutral-600 hover:text-neutral-900 hover:bg-white/70'
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      <div className="p-8">
        {activeTab === 'response' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-xl flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-neutral-900">Analyse ArxiPulse</h3>
                  <p className="text-sm text-neutral-500">Généré avec les dernières technologies d'IA</p>
                </div>
              </div>
              <span className="text-xs bg-gradient-to-r from-cyan-500 to-blue-500 text-white px-3 py-1 rounded-full font-bold">
                Live
              </span>
            </div>
            <div className="text-neutral-900 leading-relaxed whitespace-pre-wrap text-lg bg-gradient-to-br from-neutral-50 to-blue-50/30 p-8 rounded-2xl border-2 border-neutral-100">
              {response.generated_text}
            </div>
          </div>
        )}

        {activeTab === 'sources' && (
          <div className="space-y-6">
            {response.sources?.length > 0 ? (
              <>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-neutral-900 text-lg">Sources utilisées</h3>
                  <span className="text-sm text-neutral-500">{response.sources.length} source{response.sources.length > 1 ? 's' : ''}</span>
                </div>
                {response.sources.map((source, idx) => (
                  <div key={idx} className="border-2 border-neutral-200 rounded-2xl p-8 hover:shadow-lg hover:border-blue-300 transition-all bg-white group">
                    <div className="flex items-start justify-between mb-5">
                      <h3 className="font-bold text-neutral-900 text-xl group-hover:text-blue-700 transition-colors">
                        {source.title || source.source || 'Source sans titre'}
                      </h3>
                      <span className="text-xs bg-gradient-to-r from-blue-500 to-violet-500 text-white px-4 py-2 rounded-full font-bold shadow-sm">
                        Source {idx + 1}
                      </span>
                    </div>
                    <div className="grid md:grid-cols-2 gap-6 text-sm">
                      <div className="space-y-3">
                        <p className="text-neutral-700 flex items-center gap-3">
                          <FileText className="w-5 h-5 text-blue-500" />
                          <strong className="font-medium">Fichier:</strong> {source.source || 'N/A'}
                        </p>
                        <p className="text-neutral-700 flex items-center gap-3">
                          <BookOpen className="w-5 h-5 text-blue-500" />
                          <strong className="font-medium">Page:</strong> {source.page || 'N/A'}
                        </p>
                      </div>
                      <div className="space-y-3">
                        {source.authors && (
                          <p className="text-neutral-700 flex items-start gap-3">
                            <Users className="w-5 h-5 text-blue-500 mt-0.5" />
                            <span>
                              <strong className="font-medium">Auteurs:</strong> {source.authors.split(' | ').slice(0, 3).join(', ')}
                              {source.authors.split(' | ').length > 3 && ' et al.'}
                            </span>
                          </p>
                        )}
                        {source.published && (
                          <p className="text-neutral-700 flex items-center gap-3">
                            <Calendar className="w-5 h-5 text-blue-500" />
                            <strong className="font-medium">Publié:</strong> {source.published.slice(0, 10)}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </>
            ) : (
              <div className="text-center py-16 bg-neutral-50/50 rounded-2xl border-2 border-dashed border-neutral-200">
                <Database className="w-20 h-20 text-neutral-300 mx-auto mb-6" />
                <p className="text-neutral-500 text-xl font-medium">Aucune source disponible</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'details' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-neutral-900 text-lg">Analyse détaillée</h3>
              <span className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
                Score de pertinence
              </span>
            </div>
            {showChunks && response.retrieved_chunks?.length > 0 ? (
              response.retrieved_chunks.map((chunk, idx) => (
                <details key={idx} className="border-2 border-neutral-200 rounded-2xl overflow-hidden hover:border-blue-300 transition-all bg-white group">
                  <summary className="cursor-pointer p-6 font-semibold text-neutral-900 hover:bg-blue-50 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-gradient-to-br from-cyan-100 to-blue-100 rounded-lg flex items-center justify-center">
                        <Database className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <span className="flex items-center gap-2 text-lg">
                          Extrait {idx + 1}
                          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                            {chunk.score ? `${(chunk.score * 100).toFixed(1)}%` : 'N/A'}
                          </span>
                        </span>
                        <p className="text-sm text-neutral-500 font-normal">Cliquez pour développer</p>
                      </div>
                    </div>
                    <ChevronDown className="w-5 h-5 text-neutral-400 group-hover:text-blue-600 transition-transform group-open:rotate-180" />
                  </summary>
                  <div className="p-6 pt-0 border-t border-neutral-100 bg-gradient-to-br from-slate-50 to-blue-50">
                    <p className="text-base text-neutral-800 whitespace-pre-wrap bg-white p-6 rounded-xl border-2 border-neutral-100 leading-relaxed">
                      {chunk.text}
                    </p>
                    {showMetadata && chunk.metadata && (
                      <div className="mt-4">
                        <h4 className="font-semibold text-neutral-700 mb-2">Métadonnées techniques</h4>
                        <pre className="text-xs text-neutral-600 bg-neutral-100 p-4 rounded-xl overflow-auto border-2 border-neutral-200 font-mono">
                          {JSON.stringify(chunk.metadata, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                </details>
              ))
            ) : (
              <div className="text-center py-16 bg-neutral-50/50 rounded-2xl border-2 border-dashed border-neutral-200">
                <Database className="w-20 h-20 text-neutral-300 mx-auto mb-6" />
                <p className="text-neutral-500 text-xl font-medium">Aucun extrait disponible</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

// ============= COMPOSANT PRINCIPAL: App =============
const ArxiPulseApp = () => {
  const [showHome, setShowHome] = useState(true);
  const [mode, setMode] = useState('arxiv');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showChunks, setShowChunks] = useState(true);
  const [showMetadata, setShowMetadata] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [documentId, setDocumentId] = useState(null); // ✅ NOUVEAU STATE
  const [activeTab, setActiveTab] = useState('response');

  const API_URL = 'http://localhost:8000';

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setUploadedFile(file);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_URL}/ingest`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();

      setDocumentId(data.doc_id); // ✅ STOCKER LE DOC_ID

      alert(`Document ingéré avec succès par ArxiPulse ! ID: ${data.doc_id}`);
    } catch (err) {
      alert('Erreur lors de l\'ingestion du document');
    }
  };

  const handleGenerate = async () => {
    if (!query.trim()) return;

    // ✅ VÉRIFIER SI DOCUMENT EST PRÉSENT EN MODE UPLOAD
    if (mode === 'upload' && !documentId) {
      alert("Veuillez d'abord importer un document.");
      return;
    }

    setLoading(true);
    const endpoint = mode === 'arxiv' ? `${API_URL}/arxiv/generate` : `${API_URL}/generate`;
    
    
    const payload = {
      prompt: query,
      document: mode === 'upload' ? documentId : null
    };

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setResponse(data);
      setActiveTab('response');
    } catch (err) {
      alert('Erreur lors de la génération par ArxiPulse');
    } finally {
      setLoading(false);
    }
  };

  if (showHome) {
    return <HomePage onStart={() => setShowHome(false)} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-gray-50 to-neutral-100">
      <Header onHomeClick={() => setShowHome(true)} />

      <div className="max-w-7xl mx-auto px-6 py-8">
        <ModeSelector mode={mode} setMode={setMode} />

        {mode === 'upload' && (
          <UploadSection 
            uploadedFile={uploadedFile} 
            handleFileUpload={handleFileUpload}
            documentId={documentId} // ✅ PASSER DOCUMENT ID
          />
        )}

        <QuerySection 
          query={query}
          setQuery={setQuery}
          loading={loading}
          showChunks={showChunks}
          setShowChunks={setShowChunks}
          showMetadata={showMetadata}
          setShowMetadata={setShowMetadata}
          handleGenerate={handleGenerate}
          mode={mode} // ✅ PASSER MODE POUR VALIDATION
          documentId={documentId} // ✅ PASSER DOCUMENT ID
        />

        {response && (
          <ResultsSection 
            response={response}
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            showChunks={showChunks}
            showMetadata={showMetadata}
          />
        )}
      </div>

      <footer className="mt-12 py-8 border-t border-neutral-200 bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-3 mb-4 md:mb-0">
              <div className="w-10 h-10 bg-gradient-to-br from-cyan-600 to-blue-600 rounded-xl flex items-center justify-center">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="flex items-baseline gap-2">
                  <h3 className="text-lg font-bold text-neutral-900">
                    <span className="text-cyan-600">Arxi</span>
                    <span className="text-blue-600">Pulse</span>
                  </h3>
                  <span className="text-xs text-neutral-500">v1.0</span>
                </div>
                <p className="text-sm text-neutral-500">Le pouls de la recherche scientifique</p>
              </div>
            </div>
            <div className="text-center md:text-right">
              <p className="text-sm text-neutral-600 mb-2">
                Propulsé par <span className="font-bold text-cyan-600">FastAPI</span> • 
                <span className="font-bold text-emerald-600"> ChromaDB</span> • 
                <span className="font-bold text-violet-600"> Gemini AI</span>
              </p>
              <p className="text-xs text-neutral-500">© 2026 ArxiPulse • Système de veille technologique avancé</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ArxiPulseApp;
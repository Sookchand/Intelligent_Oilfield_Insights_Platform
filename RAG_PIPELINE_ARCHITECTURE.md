# 🔍 RAG Pipeline & Vector Embeddings Architecture

## 🎯 **Overview**

This system implements a **production-grade RAG (Retrieval-Augmented Generation) pipeline** that combines:
- **Vector embeddings** for semantic search
- **Hybrid search** (semantic + keyword)
- **Structured data grounding** (SQL + Graph)
- **Unstructured data retrieval** (documents, manuals, logs)

---

## 🏗️ **Architecture Components**

### **1. Embedding Generation Pipeline**

```python
# backend/embeddings/embedding_service.py
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import numpy as np

class EmbeddingService:
    """
    Production embedding service for Oil & Gas domain
    
    Features:
    - Domain-specific model fine-tuning
    - Batch processing for efficiency
    - Caching for repeated queries
    - Multi-modal embeddings (text + metadata)
    """
    
    def __init__(self):
        # Use domain-adapted model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # TODO: Fine-tune on Oil & Gas corpus (WITSML, PRODML docs)
        
        self.cache = {}  # Query cache
        
    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for user query"""
        if query in self.cache:
            return self.cache[query]
        
        embedding = self.model.encode(query, normalize_embeddings=True)
        self.cache[query] = embedding
        return embedding
    
    def embed_documents(self, documents: List[Dict]) -> List[np.ndarray]:
        """
        Batch embed documents with metadata enrichment
        
        Metadata enrichment:
        - Document type (manual, log, report)
        - Asset tags (rig, well, equipment)
        - Temporal context (date, time period)
        """
        texts = []
        for doc in documents:
            # Enrich text with metadata for better retrieval
            enriched_text = f"""
            Title: {doc['title']}
            Type: {doc['type']}
            Asset: {doc.get('asset', 'N/A')}
            Content: {doc['content']}
            """
            texts.append(enriched_text.strip())
        
        # Batch encoding for efficiency
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True
        )
        
        return embeddings
```

---

### **2. Vector Database Integration (Qdrant)**

```python
# backend/vector_store/qdrant_client.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class VectorStore:
    """
    Qdrant vector database for semantic search
    
    Collections:
    - technical_manuals: Equipment manuals, procedures
    - maintenance_logs: Historical maintenance records
    - incident_reports: Safety incidents, failures
    - production_reports: Daily/monthly production summaries
    """
    
    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)
        self._initialize_collections()
    
    def _initialize_collections(self):
        """Create collections with appropriate schemas"""
        collections = {
            "technical_manuals": {
                "vector_size": 384,  # MiniLM embedding size
                "distance": Distance.COSINE
            },
            "maintenance_logs": {
                "vector_size": 384,
                "distance": Distance.COSINE
            },
            "incident_reports": {
                "vector_size": 384,
                "distance": Distance.COSINE
            }
        }
        
        for name, config in collections.items():
            if not self.client.collection_exists(name):
                self.client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(**config)
                )
    
    def hybrid_search(
        self,
        query: str,
        collection: str,
        top_k: int = 10,
        filters: Dict = None
    ) -> List[Dict]:
        """
        Hybrid search: Semantic (vector) + Keyword (BM25)
        
        Process:
        1. Generate query embedding
        2. Vector similarity search (cosine)
        3. Keyword search (BM25)
        4. Reciprocal Rank Fusion (RRF) to combine results
        5. Apply metadata filters (asset, date range, type)
        """
        # 1. Vector search
        query_embedding = embedding_service.embed_query(query)
        
        vector_results = self.client.search(
            collection_name=collection,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=self._build_filter(filters)
        )
        
        # 2. Keyword search (BM25)
        keyword_results = self.client.search(
            collection_name=collection,
            query_text=query,  # Qdrant's built-in BM25
            limit=top_k,
            query_filter=self._build_filter(filters)
        )
        
        # 3. Reciprocal Rank Fusion
        fused_results = self._reciprocal_rank_fusion(
            vector_results,
            keyword_results,
            k=60  # RRF constant
        )
        
        return fused_results
    
    def _reciprocal_rank_fusion(
        self,
        vector_results: List,
        keyword_results: List,
        k: int = 60
    ) -> List[Dict]:
        """
        RRF: score(d) = Σ 1 / (k + rank_i(d))
        
        Combines rankings from multiple retrieval methods
        """
        scores = {}
        
        # Score vector results
        for rank, result in enumerate(vector_results, 1):
            doc_id = result.id
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
        
        # Score keyword results
        for rank, result in enumerate(keyword_results, 1):
            doc_id = result.id
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
        
        # Sort by combined score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Retrieve full documents
        return [self._get_document(doc_id) for doc_id, _ in ranked[:10]]
```

---

### **3. RAG Agent Integration**

```python
# backend/agents/rag_agent.py
from typing import List, Dict

class RAGAgent:
    """
    Retrieval-Augmented Generation Agent
    
    Workflow:
    1. Query understanding & expansion
    2. Multi-source retrieval (vector + SQL + graph)
    3. Context ranking & filtering
    4. Grounded generation with citations
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedding_service = EmbeddingService()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    async def retrieve_and_generate(
        self,
        query: str,
        context: Dict
    ) -> Dict:
        """
        Full RAG pipeline
        
        Steps:
        1. Query expansion (add domain terms)
        2. Parallel retrieval from multiple sources
        3. Re-ranking with cross-encoder
        4. Context compression
        5. Grounded generation
        6. Citation extraction
        """
        # 1. Query expansion
        expanded_query = await self._expand_query(query)
        
        # 2. Parallel retrieval
        retrieval_tasks = [
            self._retrieve_documents(expanded_query),
            self._retrieve_structured_data(query, context),
            self._retrieve_graph_context(query, context)
        ]
        
        docs, structured, graph = await asyncio.gather(*retrieval_tasks)
        
        # 3. Re-ranking
        ranked_docs = self._rerank_documents(query, docs)
        
        # 4. Context compression
        compressed_context = self._compress_context(ranked_docs[:5])
        
        # 5. Grounded generation
        answer = await self._generate_answer(
            query=query,
            context=compressed_context,
            structured_data=structured,
            graph_data=graph
        )
        
        # 6. Extract citations
        citations = self._extract_citations(answer, ranked_docs)
        
        return {
            "answer": answer,
            "citations": citations,
            "retrieved_docs": ranked_docs[:5],
            "confidence": self._calculate_confidence(answer, ranked_docs)
        }
```

---

## 🔄 **Hybrid Search Strategy**

### **Why Hybrid Search?**

| Search Type | Strengths | Weaknesses |
|-------------|-----------|------------|
| **Vector (Semantic)** | ✅ Understands meaning<br/>✅ Handles synonyms<br/>✅ Cross-lingual | ❌ Misses exact matches<br/>❌ Struggles with rare terms |
| **Keyword (BM25)** | ✅ Exact matches<br/>✅ Rare term retrieval<br/>✅ Fast | ❌ No semantic understanding<br/>❌ Synonym blind |
| **Hybrid (RRF)** | ✅ Best of both<br/>✅ Robust to query variations | ⚠️ Slightly slower |

### **Example:**
```
Query: "ESP failure at Well B-12"

Vector Search Results:
1. "Electric Submersible Pump malfunction at B-12" (score: 0.92)
2. "Downhole pump issues in Well B-12" (score: 0.88)
3. "Production decline due to equipment fault" (score: 0.75)

Keyword Search Results:
1. "ESP failure at Well B-12" (exact match, score: 1.0)
2. "Well B-12 maintenance log" (score: 0.85)
3. "ESP troubleshooting guide" (score: 0.80)

Hybrid (RRF) Results:
1. "ESP failure at Well B-12" (combined rank: 1)
2. "Electric Submersible Pump malfunction at B-12" (combined rank: 2)
3. "Well B-12 maintenance log" (combined rank: 3)
```

---

## 📊 **Multi-Source Retrieval**

```
User Query: "Why is production dropping at Rig Alpha?"

┌─────────────────────────────────────────────────────────┐
│                    RAG Orchestrator                      │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Vector Store │  │  SQL Database│  │ Graph Database│
│              │  │              │  │              │
│ • Manuals    │  │ • Production │  │ • Equipment  │
│ • Logs       │  │   time-series│  │   topology   │
│ • Reports    │  │ • Sensor data│  │ • Fault tree │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                  ┌──────────────┐
                  │  Re-Ranker   │
                  │ (Cross-Enc.) │
                  └──────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │   Generator  │
                  │   (GPT-4)    │
                  └──────────────┘
```

---

## ✅ **Key Features**

1. **Domain-Specific Embeddings** - Fine-tuned on Oil & Gas corpus
2. **Hybrid Search** - Combines semantic + keyword retrieval
3. **Multi-Source Grounding** - Vector + SQL + Graph
4. **Re-Ranking** - Cross-encoder for relevance
5. **Context Compression** - Reduces token usage
6. **Citation Tracking** - Full provenance for answers

**This RAG pipeline ensures answers are grounded in both structured data (SQL/Graph) and unstructured knowledge (documents/manuals).**


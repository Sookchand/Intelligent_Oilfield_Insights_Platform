# 🛢️ Intelligent Oilfield Insights Platform

**Enterprise-Grade Agentic RAG System for Oil & Gas Data Unification**

A production-ready multi-agent AI system that unifies structured and unstructured data from oil & gas operations, providing intelligent insights through natural language queries.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 🎯 Overview

This platform demonstrates a sophisticated **Agentic RAG (Retrieval-Augmented Generation)** architecture that:

- 🤖 **Orchestrates multiple AI agents** (Parser, SQL, Graph, Reasoning) to process complex queries
- 📊 **Unifies multi-modal data** from PostgreSQL (time-series), Neo4j (graph), Qdrant (vectors), and MinIO (documents)
- 🔍 **Provides explainable AI** with reasoning traces and confidence scores
- 🏗️ **Production-ready architecture** with Docker, FastAPI, and enterprise-grade databases
- 📈 **Real-time insights** for production optimization, equipment monitoring, and safety analysis

---

## 🏗️ Architecture

### Multi-Agent System
```
User Query → Parser Agent → [SQL Agent, Graph Agent, Vector Agent] → Reasoning Agent → Response
```

### Technology Stack

**Backend:**
- **FastAPI** - High-performance async API framework
- **LangGraph** - Agent orchestration and workflow management
- **Python 3.11+** - Modern Python with type hints

**Databases:**
- **PostgreSQL** - Time-series production data
- **Neo4j** - Asset relationships and graph traversal
- **Qdrant** - Vector embeddings for semantic search
- **MinIO** - Document storage (HSE reports, logs)

**Infrastructure:**
- **Docker & Docker Compose** - Containerized deployment
- **Uvicorn** - ASGI server for FastAPI

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Python 3.11+ (for local development)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/IntelligentOilfieldInsightPlatform.git
cd IntelligentOilfieldInsightPlatform
```

### 2. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env if needed (defaults work for local development)
```

### 3. Start the Databases
```bash
docker-compose up -d
```

Wait ~30 seconds for all databases to be healthy:
```bash
docker ps
```

### 4. Seed the Databases
```bash
# Seed PostgreSQL (production data)
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -f /docker-entrypoint-initdb.d/seed_production.sql

# Seed Neo4j (graph data)
docker cp seed_neo4j_simple.cypher oilfield-neo4j:/tmp/seed.cypher
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass -f /tmp/seed.cypher
```

### 5. Install Python Dependencies
```bash
pip install -r requirements.txt
cd backend
pip install -r requirements.txt
```

### 6. Start the Backend
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Test the API
Open your browser to:
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Database Status:** http://localhost:8000/api/status/databases

---

## 📖 Usage Examples

### Example 1: Production Analysis
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is production dropping at Rig Alpha?"}'
```

**Response:**
- SQL Agent retrieves production trends from PostgreSQL
- Graph Agent finds faulty equipment (G-40 pressure gauge) from Neo4j
- Reasoning Agent synthesizes: "Production declining due to faulty pressure gauge at Well W-12"
- Confidence: 90%

### Example 2: Equipment Monitoring
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me all faulty equipment at Rig Alpha"}'
```

**Response:**
- Graph traversal: Rig Alpha → Well W-12 → Sensor G-40
- Status: FAULTY
- Type: Pressure Gauge
- Reading: 2450.5 psi (abnormal)

---

## 📊 Sample Data

The platform includes realistic sample data:

**PostgreSQL:**
- 13 production records with timestamps, rates, pressure, temperature
- Moving averages and trend analysis

**Neo4j:**
- 2 Basins (Permian, Eagle Ford)
- 2 Rigs (Rig Alpha, Rig Beta)
- 3 Wells (W-12, W-15, W-18)
- 3 Sensors (G-40, PUMP-45, VALVE-12)
- 2 Incidents (equipment failure, pressure drop)

---

## 🔧 Configuration

### Environment Variables
See `.env.example` for all configuration options. Key variables:

```bash
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=oilfield_production

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_PASSWORD=oilfield_neo4j_pass

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333

# MinIO
MINIO_ENDPOINT=localhost:9002
MINIO_ACCESS_KEY=minio_admin
```

---

## 🧪 Testing

### Check Database Connectivity
```bash
GET http://localhost:8000/api/status/databases
```

Expected response:
```json
{
  "databases": {
    "postgres": true,
    "neo4j": true,
    "qdrant": true,
    "minio": true
  },
  "all_healthy": true
}
```

### Run Test Queries
Use the Swagger UI at http://localhost:8000/docs to test queries interactively.

---

## 📁 Project Structure

```
IntelligentOilfieldInsightPlatform/
├── backend/
│   ├── agents/              # AI agents (Parser, SQL, Graph, Reasoning)
│   ├── database/            # Database connection managers
│   ├── main.py              # FastAPI application
│   └── graph_engine.py      # Multi-agent orchestration
├── data/                    # Seed data files
├── docker-compose.yml       # Database services
├── .env.example             # Environment template
└── README.md
```

---

## 🛠️ Development

### Adding New Agents
1. Create agent in `backend/agents/`
2. Register in `graph_engine.py`
3. Update query routing logic

### Adding New Data Sources
1. Add connection manager in `backend/database/connections.py`
2. Create agent to query the data source
3. Update orchestration workflow

---

## 🚢 Deployment

### Docker Production Build
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes
See `k8s/` directory for Kubernetes manifests (coming soon).

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for the Oil & Gas Industry**


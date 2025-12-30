# Implementation Guide: Test Questions Solutions

This guide provides comprehensive solutions for the demonstration scenarios outlined in `Project_Specification.md` with Docker, MinIO, Kubernetes (K8s), and CI/CD implementation.

## 📋 Table of Contents

1. [Infrastructure Setup](#infrastructure-setup)
2. [Test Questions Implementation](#test-questions-implementation)
3. [Deployment Guide](#deployment-guide)
4. [CI/CD Pipeline](#cicd-pipeline)

---

## 🏗️ Infrastructure Setup

### Local Development with Docker

#### Prerequisites

- Docker Desktop (with Kubernetes enabled) or Docker Engine + Minikube
- Docker Compose v2.0+
- kubectl CLI
- Git
- OpenAI API Key

#### Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd IntelligentOilfieldInsightPlatform

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Start all services
docker-compose up -d

# 4. Verify services are running
docker-compose ps

# 5. Initialize databases
docker-compose exec postgres psql -U oilfield_user -d oilfield_production -f /docker-entrypoint-initdb.d/seed_sql.sql
docker-compose exec neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass -f /var/lib/neo4j/import/seed_graph.cypher

# 6. Access services
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Neo4j Browser: http://localhost:7474
# - MinIO Console: http://localhost:9001
# - Qdrant Dashboard: http://localhost:6333/dashboard
```

### Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│                    Port: 3000                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI + LangGraph)               │
│                    Port: 8000                                │
└─────┬──────────┬──────────┬──────────┬────────────┬─────────┘
      │          │          │          │            │
      ▼          ▼          ▼          ▼            ▼
┌──────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
│PostgreSQL│ │ Neo4j  │ │ Qdrant │ │ MinIO  │ │  OpenAI  │
│  :5432   │ │ :7687  │ │ :6333  │ │ :9000  │ │   API    │
└──────────┘ └────────┘ └────────┘ └────────┘ └──────────┘
```

---

## 🎯 Test Questions Implementation

### Scenario A: Operational Performance & Root Cause Analysis

#### Question 1: "Why is production dropping at Rig Alpha?"

**Implementation Path:**

1. **Parser Agent** (`backend/agents/parser.py`)
   - Identifies intent: Root cause analysis
   - Extracts entity: "Rig Alpha"
   - Plans execution: SQL → Graph → Vector

2. **SQL Agent** (`backend/agents/sql_agent.py`)

   ```python
   # Query production trends
   SELECT 
       timestamp, 
       production_rate, 
       AVG(production_rate) OVER (
           ORDER BY timestamp 
           ROWS BETWEEN 30 PRECEDING AND CURRENT ROW
       ) as moving_avg
   FROM production_data
   WHERE rig_name = 'Rig Alpha'
   ORDER BY timestamp DESC
   LIMIT 100;
   ```

3. **Graph Agent** (`backend/agents/graph_agent.py`)

   ```cypher
   // Find linked equipment with anomalies
   MATCH (r:Rig {name: 'Rig Alpha'})-[:HAS_WELL]->(w:Well)
         -[:HAS_SENSOR]->(s:Sensor)
   WHERE s.status = 'FAULTY' OR s.last_reading_anomaly = true
   RETURN r, w, s, s.sensor_type, s.last_reading
   ```

4. **Vector Agent** (Qdrant search)

   ```python
   # Search HSE reports for recent maintenance
   query_vector = embed("Rig Alpha sensor failure repair")
   results = qdrant_client.search(
       collection_name="hse_reports",
       query_vector=query_vector,
       limit=5,
       filter={
           "must": [
               {"key": "rig_name", "match": {"value": "Rig Alpha"}},
               {"key": "timestamp", "range": {"gte": "2024-12-01"}}
           ]
       }
   )
   ```

5. **Reasoning Agent** (`backend/agents/reasoning.py`)
   - Synthesizes: "Production dropped 15% due to faulty Pressure Gauge G-40"
   - Provides reasoning trace with timestamps and data sources

**Expected Output:**

```json
{
  "answer": "Production at Rig Alpha dropped 15% starting Dec 20, 2024 due to faulty Pressure Gauge G-40 on Well W-12. Maintenance logs show the sensor has been reporting anomalous readings since Dec 18.",
  "reasoning_trace": [
    {"step": 1, "agent": "SQL", "action": "Queried production trends", "result": "15% drop detected"},
    {"step": 2, "agent": "Graph", "action": "Traversed Rig→Well→Sensor", "result": "Found faulty G-40"},
    {"step": 3, "agent": "Vector", "action": "Retrieved HSE reports", "result": "Maintenance scheduled"}
  ],
  "graph_path": ["Rig Alpha", "Well W-12", "Pressure Gauge G-40"],
  "confidence": 0.92
}
```

---

#### Question 2: "Which wells in the Permian Basin are currently producing below their 30-day average?"

**Implementation:**

```python
# SQL Agent query
SELECT 
    w.well_name,
    w.basin,
    AVG(p.production_rate) as current_avg,
    (
        SELECT AVG(production_rate) 
        FROM production_data 
        WHERE well_id = w.id 
        AND timestamp >= NOW() - INTERVAL '30 days'
    ) as thirty_day_avg,
    ROUND(
        ((current_avg - thirty_day_avg) / thirty_day_avg * 100), 2
    ) as percent_change
FROM wells w
JOIN production_data p ON w.id = p.well_id
WHERE w.basin = 'Permian Basin'
  AND p.timestamp >= NOW() - INTERVAL '7 days'
GROUP BY w.id, w.well_name, w.basin
HAVING current_avg < (
    SELECT AVG(production_rate) 
    FROM production_data 
    WHERE well_id = w.id 
    AND timestamp >= NOW() - INTERVAL '30 days'
)
ORDER BY percent_change ASC;
```

---

#### Question 3: "Identify all assets currently affected by the pump failure at Block-12."

**Implementation:**

```cypher
// Multi-hop graph traversal
MATCH path = (failed:Equipment {name: 'Pump-Block-12', status: 'FAILED'})
             -[:SUPPLIES|CONNECTED_TO*1..5]->(affected)
WHERE affected:Well OR affected:Rig OR affected:Equipment
RETURN 
    failed.name as source,
    [node in nodes(path) | node.name] as impact_chain,
    affected.name as affected_asset,
    affected.type as asset_type,
    length(path) as hops
ORDER BY hops ASC;
```

---

### Scenario B: Safety, Compliance, and Risk Exposure

#### Question 4: "Are there any recurring safety incidents linked to the pressure gauge anomalies we saw last week?"

**Implementation:**

```python
# Step 1: Graph Agent - Find pressure gauges with anomalies last week
cypher_query = """
MATCH (g:Gauge)-[:RECORDED]->(a:Anomaly)
WHERE a.timestamp >= datetime() - duration('P7D')
  AND g.type = 'PRESSURE'
RETURN g.id as gauge_id, g.name, collect(a.timestamp) as anomaly_times
"""

# Step 2: Vector Agent - Search HSE reports for incidents
for gauge in gauge_results:
    query = f"safety incident {gauge['name']} pressure anomaly"
    vector_results = qdrant_client.search(
        collection_name="hse_reports",
        query_vector=embed(query),
        filter={
            "must": [
                {"key": "severity", "match": {"any": ["HIGH", "CRITICAL"]}},
                {"key": "equipment_id", "match": {"value": gauge['gauge_id']}}
            ]
        }
    )

# Step 3: Reasoning Agent - Identify patterns
# Correlate anomaly timestamps with incident timestamps
# Flag recurring patterns (>2 incidents within 30 days)
```

---

#### Question 5: "Show me high-severity incidents for wells that are currently in 'Maintenance' status."

**Implementation:**

```python
# SQL Agent - Get wells in maintenance
sql_query = """
SELECT id, well_name, maintenance_start_date, maintenance_reason
FROM wells
WHERE status = 'MAINTENANCE'
  AND maintenance_start_date >= NOW() - INTERVAL '90 days'
"""

# Vector Agent - Retrieve high-severity incidents
for well in maintenance_wells:
    incidents = qdrant_client.search(
        collection_name="hse_reports",
        query_vector=embed(f"incident {well['well_name']}"),
        filter={
            "must": [
                {"key": "well_id", "match": {"value": well['id']}},
                {"key": "severity", "match": {"value": "HIGH"}},
                {"key": "timestamp", "range": {
                    "gte": well['maintenance_start_date']
                }}
            ]
        },
        limit=10
    )
```

---

### Scenario C: Maintenance Optimization & Reliability

#### Question 6: "Which rigs have overdue preventive maintenance tasks and have also reported mechanical vibrations?"

**Implementation:**

```python
# SQL Agent - Find overdue maintenance
sql_query = """
SELECT
    r.rig_name,
    m.task_description,
    m.due_date,
    CURRENT_DATE - m.due_date as days_overdue
FROM rigs r
JOIN maintenance_schedule m ON r.id = m.rig_id
WHERE m.status = 'PENDING'
  AND m.due_date < CURRENT_DATE
  AND m.task_type = 'PREVENTIVE'
ORDER BY days_overdue DESC
"""

# Vector Agent - Search for vibration mentions
for rig in overdue_rigs:
    vibration_reports = qdrant_client.search(
        collection_name="operator_notes",
        query_vector=embed("mechanical vibration abnormal"),
        filter={
            "must": [
                {"key": "rig_name", "match": {"value": rig['rig_name']}},
                {"key": "timestamp", "range": {"gte": "2024-11-01"}}
            ]
        },
        score_threshold=0.7
    )

    # Flag rigs with both conditions
    if vibration_reports:
        critical_rigs.append({
            "rig": rig['rig_name'],
            "overdue_days": rig['days_overdue'],
            "vibration_count": len(vibration_reports)
        })
```

---

#### Question 7: "What is the correlation between downtime at Rig Delta and historical sensor malfunctions?"

**Implementation:**

```python
# SQL Agent - Get downtime events
downtime_query = """
SELECT
    timestamp,
    duration_hours,
    reason
FROM downtime_events
WHERE rig_name = 'Rig Delta'
  AND timestamp >= NOW() - INTERVAL '1 year'
ORDER BY timestamp
"""

# Graph Agent - Get sensor malfunction history
cypher_query = """
MATCH (r:Rig {name: 'Rig Delta'})-[:HAS_WELL]->(w:Well)
      -[:HAS_SENSOR]->(s:Sensor)-[:HAD_MALFUNCTION]->(m:Malfunction)
WHERE m.timestamp >= datetime() - duration('P1Y')
RETURN
    m.timestamp,
    s.sensor_type,
    m.malfunction_type,
    m.severity
ORDER BY m.timestamp
"""

# Reasoning Agent - Calculate correlation
# Use time-series analysis to find temporal patterns
# within ±48 hours of downtime events
correlation_analysis = {
    "total_downtime_events": len(downtime_events),
    "total_sensor_malfunctions": len(sensor_malfunctions),
    "correlated_events": count_within_48h_window(downtime, malfunctions),
    "correlation_coefficient": calculate_pearson_correlation(),
    "key_patterns": [
        "80% of downtime events preceded by sensor anomalies within 24h",
        "Pressure sensors account for 60% of correlated malfunctions"
    ]
}
```

---

## 🚀 Deployment Guide

### Kubernetes Production Deployment

#### 1. Prepare Kubernetes Cluster

```bash
# For cloud providers:
# - AWS: eksctl create cluster --name oilfield-cluster
# - GCP: gcloud container clusters create oilfield-cluster
# - Azure: az aks create --name oilfield-cluster

# For local testing with Minikube:
minikube start --cpus=4 --memory=8192 --disk-size=50g
minikube addons enable ingress
minikube addons enable metrics-server
```

#### 2. Install Required Components

```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# Install cert-manager for TLS
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Verify installations
kubectl get pods -n ingress-nginx
kubectl get pods -n cert-manager
```

#### 3. Deploy Application

```bash
# Create namespace and apply configurations
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml

# Create secrets (update values first!)
kubectl create secret generic oilfield-secrets \
  --from-literal=POSTGRES_PASSWORD=<your-password> \
  --from-literal=NEO4J_PASSWORD=<your-password> \
  --from-literal=MINIO_ACCESS_KEY=<your-key> \
  --from-literal=MINIO_SECRET_KEY=<your-secret> \
  --from-literal=OPENAI_API_KEY=<your-api-key> \
  -n oilfield-platform

# Deploy databases
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/neo4j-deployment.yaml
kubectl apply -f k8s/minio-deployment.yaml
kubectl apply -f k8s/qdrant-deployment.yaml

# Wait for databases to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n oilfield-platform --timeout=300s
kubectl wait --for=condition=ready pod -l app=neo4j -n oilfield-platform --timeout=300s

# Deploy application
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml

# Check deployment status
kubectl get all -n oilfield-platform
```

#### 4. Initialize Data

```bash
# Port-forward to access databases
kubectl port-forward -n oilfield-platform svc/postgres-service 5432:5432 &
kubectl port-forward -n oilfield-platform svc/neo4j-service 7687:7687 &

# Load seed data
psql -h localhost -U oilfield_user -d oilfield_production -f data/seed_sql.sql
cypher-shell -a bolt://localhost:7687 -u neo4j -p <password> -f data/seed_graph.cypher

# Initialize MinIO bucket
kubectl port-forward -n oilfield-platform svc/minio-service 9000:9000 &
mc alias set oilfield http://localhost:9000 <access-key> <secret-key>
mc mb oilfield/hse-reports
mc cp data/sample_hse_reports/* oilfield/hse-reports/
```

#### 5. Verify Deployment

```bash
# Check pod status
kubectl get pods -n oilfield-platform

# Check logs
kubectl logs -n oilfield-platform -l app=backend --tail=50
kubectl logs -n oilfield-platform -l app=frontend --tail=50

# Test API endpoint
kubectl port-forward -n oilfield-platform svc/backend-service 8000:8000
curl http://localhost:8000/health

# Access application
# Update /etc/hosts or DNS to point to your ingress IP
kubectl get ingress -n oilfield-platform
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline (`.github/workflows/ci-cd.yaml`) automates:

1. **Testing** (on every push/PR)
   - Backend: pytest with coverage
   - Frontend: Jest tests and build verification
   - Linting: black, flake8, eslint

2. **Building** (on main/develop push)
   - Multi-stage Docker builds
   - Push to GitHub Container Registry
   - Semantic versioning with tags

3. **Deployment** (on main push)
   - Automated K8s deployment
   - Rolling updates with health checks
   - Rollback on failure

### Setup Instructions

```bash
# 1. Add GitHub Secrets
# Go to Settings → Secrets and variables → Actions
# Add the following secrets:
# - KUBE_CONFIG: Base64-encoded kubeconfig file
# - OPENAI_API_KEY: Your OpenAI API key

# Generate base64 kubeconfig
cat ~/.kube/config | base64 -w 0

# 2. Enable GitHub Container Registry
# Settings → Packages → Enable improved container support

# 3. Trigger deployment
git add .
git commit -m "feat: implement test questions"
git push origin main

# 4. Monitor workflow
# Go to Actions tab in GitHub repository
```

### Manual Deployment

```bash
# Build images locally
docker build -t oilfield-backend:latest ./backend
docker build -t oilfield-frontend:latest ./frontend

# Tag for registry
docker tag oilfield-backend:latest ghcr.io/<username>/oilfield-backend:latest
docker tag oilfield-frontend:latest ghcr.io/<username>/oilfield-frontend:latest

# Push to registry
docker push ghcr.io/<username>/oilfield-backend:latest
docker push ghcr.io/<username>/oilfield-frontend:latest

# Update K8s deployments
kubectl set image deployment/backend backend=ghcr.io/<username>/oilfield-backend:latest -n oilfield-platform
kubectl set image deployment/frontend frontend=ghcr.io/<username>/oilfield-frontend:latest -n oilfield-platform
```

---

## 📊 Monitoring & Observability

### Logging

```bash
# View aggregated logs
kubectl logs -n oilfield-platform -l app=backend --tail=100 -f

# Export logs to file
kubectl logs -n oilfield-platform deployment/backend > backend-logs.txt

# Use stern for multi-pod logging (install: brew install stern)
stern -n oilfield-platform backend
```

### Metrics

```bash
# View resource usage
kubectl top pods -n oilfield-platform
kubectl top nodes

# Check HPA status
kubectl get hpa -n oilfield-platform
kubectl describe hpa backend-hpa -n oilfield-platform
```

### Health Checks

```bash
# Backend health
curl http://api.oilfield.yourdomain.com/health

# Database connectivity
kubectl exec -it -n oilfield-platform deployment/backend -- python -c "
from database.connections import test_connections
test_connections()
"
```

---

## 🔒 Security Best Practices

1. **Secrets Management**
   - Use external secret managers (Vault, AWS Secrets Manager)
   - Rotate credentials regularly
   - Never commit secrets to Git

2. **Network Policies**

   ```bash
   # Apply network policies to restrict pod communication
   kubectl apply -f k8s/network-policies.yaml
   ```

3. **RBAC**

   ```bash
   # Create service accounts with minimal permissions
   kubectl apply -f k8s/rbac.yaml
   ```

4. **Image Scanning**
   - Enable Dependabot alerts
   - Use Trivy for vulnerability scanning

   ```bash
   trivy image oilfield-backend:latest
   ```

---

## 🧪 Testing the Implementation

### End-to-End Test

```bash
# 1. Start local environment
docker-compose up -d

# 2. Wait for services
sleep 30

# 3. Run test queries
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is production dropping at Rig Alpha?"}'

# 4. Verify response structure
# Should include: answer, reasoning_trace, graph_path, confidence

# 5. Check frontend
open http://localhost:3000
```

### Unit Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=agents --cov-report=html

# Frontend tests
cd frontend
npm test -- --coverage

# Integration tests
pytest tests/integration/ -v
```

---

## 📚 Additional Resources

- **LangGraph Documentation**: <https://langchain-ai.github.io/langgraph/>
- **Neo4j Cypher Guide**: <https://neo4j.com/docs/cypher-manual/>
- **Qdrant Vector DB**: <https://qdrant.tech/documentation/>
- **MinIO Documentation**: <https://min.io/docs/>
- **Kubernetes Best Practices**: <https://kubernetes.io/docs/concepts/>

---

## 🆘 Troubleshooting

### Common Issues

**Issue**: Backend can't connect to PostgreSQL

```bash
# Check if PostgreSQL is running
kubectl get pods -n oilfield-platform -l app=postgres

# Check logs
kubectl logs -n oilfield-platform -l app=postgres

# Verify connection from backend pod
kubectl exec -it -n oilfield-platform deployment/backend -- \
  psql -h postgres-service -U oilfield_user -d oilfield_production
```

**Issue**: Neo4j authentication fails

```bash
# Reset Neo4j password
kubectl exec -it -n oilfield-platform deployment/neo4j -- \
  cypher-shell -u neo4j -p <old-password> \
  "ALTER CURRENT USER SET PASSWORD FROM '<old-password>' TO '<new-password>'"
```

**Issue**: MinIO bucket not accessible

```bash
# Check MinIO service
kubectl port-forward -n oilfield-platform svc/minio-service 9001:9001
# Access console at http://localhost:9001

# Create bucket manually
mc alias set k8s-minio http://localhost:9000 <access-key> <secret-key>
mc mb k8s-minio/hse-reports
```

---

## ✅ Success Criteria Validation

After implementation, verify:

- [ ] All 7 test questions return accurate answers
- [ ] Reasoning traces show correct agent execution order
- [ ] Graph visualizations display traversal paths
- [ ] Response time < 5 seconds for multi-agent queries
- [ ] Translation accuracy > 90% for SQL and Cypher
- [ ] Industry terminology used correctly (BOP, SCADA, etc.)
- [ ] CI/CD pipeline passes all tests
- [ ] Kubernetes deployment scales automatically
- [ ] All health checks pass

---

**Last Updated**: 2024-12-30
**Version**: 1.0.0

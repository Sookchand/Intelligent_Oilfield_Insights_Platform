# Quick Start Guide

Get the Intelligent Oilfield Insights Platform running in 5 minutes!

## 🚀 Local Development (Fastest)

### Prerequisites
- Docker Desktop with 8GB+ RAM
- OpenAI API Key

### Steps

```bash
# 1. Clone and setup
git clone <repository-url>
cd IntelligentOilfieldInsightPlatform

# 2. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Start everything
docker-compose up -d

# 4. Wait for services (30 seconds)
sleep 30

# 5. Initialize databases
docker-compose exec postgres psql -U oilfield_user -d oilfield_production -f /docker-entrypoint-initdb.d/seed_sql.sql
docker-compose exec neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass -f /var/lib/neo4j/import/seed_graph.cypher

# 6. Verify
curl http://localhost:8000/health
```

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | - |
| **Backend API** | http://localhost:8000/docs | - |
| **Neo4j Browser** | http://localhost:7474 | neo4j / oilfield_neo4j_pass |
| **MinIO Console** | http://localhost:9001 | minio_admin / minio_admin_pass |
| **Qdrant Dashboard** | http://localhost:6333/dashboard | - |

---

## 🧪 Test the Platform

### Test Question 1: Production Analysis

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Why is production dropping at Rig Alpha?"
  }'
```

**Expected Response:**
```json
{
  "answer": "Production at Rig Alpha dropped 15% due to faulty Pressure Gauge G-40...",
  "reasoning_trace": [
    {"step": 1, "agent": "SQL", "action": "Queried production trends"},
    {"step": 2, "agent": "Graph", "action": "Traversed Rig→Well→Sensor"},
    {"step": 3, "agent": "Vector", "action": "Retrieved HSE reports"}
  ],
  "graph_path": ["Rig Alpha", "Well W-12", "Pressure Gauge G-40"],
  "confidence": 0.92
}
```

### Test Question 2: Basin Analysis

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Which wells in the Permian Basin are producing below their 30-day average?"
  }'
```

### Test Question 3: Asset Impact

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Identify all assets affected by the pump failure at Block-12"
  }'
```

---

## 🛠️ Common Commands

### Using Makefile

```bash
# Start services
make up

# View logs
make logs

# Stop services
make down

# Run tests
make test

# Check health
make health-check

# Reset databases
make db-reset

# Open shells
make shell-backend
make shell-postgres
make shell-neo4j
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Stop everything
docker-compose down

# Clean up (including volumes)
docker-compose down -v
```

---

## ☸️ Kubernetes Deployment

### Minikube (Local K8s)

```bash
# 1. Start Minikube
minikube start --cpus=4 --memory=8192

# 2. Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# 3. Deploy
make k8s-deploy

# 4. Check status
make k8s-status

# 5. Access services
minikube service frontend-service -n oilfield-platform
```

### Cloud Kubernetes

```bash
# 1. Configure kubectl for your cluster
# AWS: aws eks update-kubeconfig --name oilfield-cluster
# GCP: gcloud container clusters get-credentials oilfield-cluster
# Azure: az aks get-credentials --name oilfield-cluster

# 2. Create secrets
kubectl create secret generic oilfield-secrets \
  --from-literal=OPENAI_API_KEY=<your-key> \
  --from-literal=POSTGRES_PASSWORD=<password> \
  --from-literal=NEO4J_PASSWORD=<password> \
  --from-literal=MINIO_ACCESS_KEY=<key> \
  --from-literal=MINIO_SECRET_KEY=<secret> \
  -n oilfield-platform

# 3. Deploy
make k8s-deploy

# 4. Get ingress IP
kubectl get ingress -n oilfield-platform
```

---

## 🔍 Troubleshooting

### Services won't start

```bash
# Check Docker resources
docker system df

# Clean up
docker system prune -f

# Restart Docker Desktop
```

### Database connection errors

```bash
# Check if databases are ready
docker-compose ps

# View database logs
docker-compose logs postgres
docker-compose logs neo4j

# Restart databases
docker-compose restart postgres neo4j
```

### Port already in use

```bash
# Find process using port
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Kill process or change port in docker-compose.yml
```

---

## 📚 Next Steps

1. **Read Full Documentation**
   - `IMPLEMENTATION_GUIDE.md` - Complete implementation details
   - `DEPLOYMENT.md` - Production deployment guide
   - `SOLUTION_SUMMARY.md` - Architecture overview

2. **Explore the Code**
   - `backend/agents/` - Agent implementations
   - `backend/database/` - Database models
   - `frontend/components/` - UI components

3. **Run Tests**
   ```bash
   make test
   ```

4. **Deploy to Production**
   - Follow `DEPLOYMENT.md` for cloud deployment
   - Configure CI/CD with GitHub Actions

---

## 🆘 Getting Help

- **Documentation**: Check `IMPLEMENTATION_GUIDE.md`
- **Issues**: Review `DEPLOYMENT.md` troubleshooting section
- **Logs**: `make logs` or `docker-compose logs -f`

---

**Ready to go!** 🎉

Start with `make up` and access http://localhost:3000


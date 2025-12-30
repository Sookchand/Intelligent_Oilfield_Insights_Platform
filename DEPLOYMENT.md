# Deployment Guide

This document provides step-by-step instructions for deploying the Intelligent Oilfield Insights Platform.

## 🎯 Deployment Options

1. **Local Development** - Docker Compose
2. **Production** - Kubernetes (K8s)
3. **Cloud Providers** - AWS EKS, GCP GKE, Azure AKS

---

## 🐳 Local Development Deployment

### Prerequisites

- Docker Desktop 4.0+ (with Kubernetes enabled) or Docker Engine + Docker Compose
- 8GB+ RAM available
- 20GB+ disk space
- OpenAI API Key

### Quick Start

```bash
# 1. Clone and setup
git clone <repository-url>
cd IntelligentOilfieldInsightPlatform
cp .env.example .env

# 2. Edit .env and add your OPENAI_API_KEY
nano .env

# 3. Start all services
make up

# 4. Initialize databases
make db-init

# 5. Verify deployment
make health-check

# 6. Access services
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
# Neo4j Browser: http://localhost:7474
# MinIO Console: http://localhost:9001
```

### Common Commands

```bash
# View logs
make logs

# Restart services
make restart

# Run tests
make test

# Stop services
make down

# Clean everything
make clean
```

---

## ☸️ Kubernetes Production Deployment

### Prerequisites

- Kubernetes cluster (1.25+)
- kubectl CLI configured
- 16GB+ RAM across nodes
- 100GB+ storage
- Ingress controller (NGINX)
- cert-manager (for TLS)

### Step 1: Prepare Cluster

#### Option A: Cloud Providers

**AWS EKS**

```bash
eksctl create cluster \
  --name oilfield-cluster \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.xlarge \
  --nodes 3 \
  --nodes-min 3 \
  --nodes-max 10 \
  --managed
```

**GCP GKE**

```bash
gcloud container clusters create oilfield-cluster \
  --zone us-central1-a \
  --machine-type n1-standard-4 \
  --num-nodes 3 \
  --enable-autoscaling \
  --min-nodes 3 \
  --max-nodes 10
```

**Azure AKS**

```bash
az aks create \
  --resource-group oilfield-rg \
  --name oilfield-cluster \
  --node-count 3 \
  --node-vm-size Standard_D4s_v3 \
  --enable-cluster-autoscaler \
  --min-count 3 \
  --max-count 10
```

#### Option B: Local Minikube

```bash
minikube start \
  --cpus=4 \
  --memory=8192 \
  --disk-size=50g \
  --driver=docker

minikube addons enable ingress
minikube addons enable metrics-server
```

### Step 2: Install Dependencies

```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Verify installations
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

kubectl wait --namespace cert-manager \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/instance=cert-manager \
  --timeout=120s
```

### Step 3: Configure Secrets

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets (replace with actual values)
kubectl create secret generic oilfield-secrets \
  --from-literal=POSTGRES_PASSWORD='<strong-password>' \
  --from-literal=NEO4J_PASSWORD='<strong-password>' \
  --from-literal=MINIO_ACCESS_KEY='<access-key>' \
  --from-literal=MINIO_SECRET_KEY='<secret-key>' \
  --from-literal=OPENAI_API_KEY='<your-openai-key>' \
  -n oilfield-platform

# Verify secret creation
kubectl get secrets -n oilfield-platform
```

### Step 4: Deploy Application

```bash
# Deploy using Makefile
make k8s-deploy

# OR deploy manually
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/neo4j-deployment.yaml
kubectl apply -f k8s/minio-deployment.yaml
kubectl apply -f k8s/qdrant-deployment.yaml

# Wait for databases to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n oilfield-platform --timeout=300s
kubectl wait --for=condition=ready pod -l app=neo4j -n oilfield-platform --timeout=300s

# Deploy application services
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml

# Check deployment status
make k8s-status
```

### Step 5: Initialize Data

```bash
# Port-forward to databases
kubectl port-forward -n oilfield-platform svc/postgres-service 5432:5432 &
kubectl port-forward -n oilfield-platform svc/neo4j-service 7687:7687 &

# Load seed data
psql -h localhost -U oilfield_user -d oilfield_production -f data/seed_sql.sql
cypher-shell -a bolt://localhost:7687 -u neo4j -p <password> -f data/seed_graph.cypher

# Kill port-forwards
pkill -f "port-forward"
```

### Step 6: Configure DNS

```bash
# Get ingress IP
kubectl get ingress -n oilfield-platform

# Add to DNS or /etc/hosts
# <INGRESS_IP> oilfield.yourdomain.com
# <INGRESS_IP> api.oilfield.yourdomain.com
```

### Step 7: Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n oilfield-platform

# Check services
kubectl get svc -n oilfield-platform

# Test backend health
kubectl port-forward -n oilfield-platform svc/backend-service 8000:8000 &
curl http://localhost:8000/health

# Test frontend
kubectl port-forward -n oilfield-platform svc/frontend-service 3000:3000 &
curl http://localhost:3000

# View logs
kubectl logs -n oilfield-platform -l app=backend --tail=50
kubectl logs -n oilfield-platform -l app=frontend --tail=50
```

---

## 🔄 CI/CD Deployment

### GitHub Actions Setup

1. **Add Repository Secrets**

   Go to: Settings → Secrets and variables → Actions

   Add the following secrets:
   - `KUBE_CONFIG`: Base64-encoded kubeconfig
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `POSTGRES_PASSWORD`: Production database password
   - `NEO4J_PASSWORD`: Production Neo4j password
   - `MINIO_ACCESS_KEY`: MinIO access key
   - `MINIO_SECRET_KEY`: MinIO secret key

2. **Generate kubeconfig**

   ```bash
   # Get kubeconfig and encode
   cat ~/.kube/config | base64 -w 0

   # Copy output and add as KUBE_CONFIG secret
   ```

3. **Enable GitHub Container Registry**

   Settings → Packages → Enable improved container support

4. **Trigger Deployment**

   ```bash
   # Push to main branch triggers deployment
   git add .
   git commit -m "feat: deploy to production"
   git push origin main

   # Monitor in GitHub Actions tab
   ```

### Manual CI/CD Deployment

```bash
# Build images
docker build -t ghcr.io/<username>/oilfield-backend:latest ./backend
docker build -t ghcr.io/<username>/oilfield-frontend:latest ./frontend

# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u <username> --password-stdin

# Push images
docker push ghcr.io/<username>/oilfield-backend:latest
docker push ghcr.io/<username>/oilfield-frontend:latest

# Update K8s deployments
kubectl set image deployment/backend \
  backend=ghcr.io/<username>/oilfield-backend:latest \
  -n oilfield-platform

kubectl set image deployment/frontend \
  frontend=ghcr.io/<username>/oilfield-frontend:latest \
  -n oilfield-platform

# Wait for rollout
kubectl rollout status deployment/backend -n oilfield-platform
kubectl rollout status deployment/frontend -n oilfield-platform
```

---

## 🔒 Security Hardening

### 1. Network Policies

Create `k8s/network-policies.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: oilfield-platform
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: neo4j
    ports:
    - protocol: TCP
      port: 7687
```

Apply:

```bash
kubectl apply -f k8s/network-policies.yaml
```

### 2. RBAC Configuration

Create `k8s/rbac.yaml`:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: oilfield-backend-sa
  namespace: oilfield-platform
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: oilfield-backend-role
  namespace: oilfield-platform
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: oilfield-backend-rolebinding
  namespace: oilfield-platform
subjects:
- kind: ServiceAccount
  name: oilfield-backend-sa
roleRef:
  kind: Role
  name: oilfield-backend-role
  apiGroup: rbac.authorization.k8s.io
```

### 3. Pod Security Standards

```bash
# Label namespace with security standard
kubectl label namespace oilfield-platform \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted
```

### 4. External Secrets (Recommended)

Install External Secrets Operator:

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets \
  external-secrets/external-secrets \
  -n external-secrets-system \
  --create-namespace
```

---

## 📊 Monitoring Setup

### Prometheus & Grafana

```bash
# Install Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3001:80
# Default credentials: admin/prom-operator
```

### Application Metrics

Add to backend deployment:

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"
  prometheus.io/path: "/metrics"
```

---

## 🔧 Troubleshooting

### Pod Not Starting

```bash
# Describe pod
kubectl describe pod <pod-name> -n oilfield-platform

# Check events
kubectl get events -n oilfield-platform --sort-by='.lastTimestamp'

# Check logs
kubectl logs <pod-name> -n oilfield-platform --previous
```

### Database Connection Issues

```bash
# Test from backend pod
kubectl exec -it -n oilfield-platform deployment/backend -- \
  python -c "from database.connections import test_connections; test_connections()"

# Check service endpoints
kubectl get endpoints -n oilfield-platform
```

### Ingress Not Working

```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ingress resource
kubectl describe ingress oilfield-ingress -n oilfield-platform

# Test from within cluster
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://backend-service.oilfield-platform.svc.cluster.local:8000/health
```

---

## 🔄 Rollback Procedures

### Rollback Deployment

```bash
# View rollout history
kubectl rollout history deployment/backend -n oilfield-platform

# Rollback to previous version
kubectl rollout undo deployment/backend -n oilfield-platform

# Rollback to specific revision
kubectl rollout undo deployment/backend --to-revision=2 -n oilfield-platform
```

### Database Rollback

```bash
# Restore from backup
kubectl exec -it -n oilfield-platform deployment/postgres -- \
  psql -U oilfield_user -d oilfield_production < backup.sql
```

---

## 📈 Scaling

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment/backend --replicas=5 -n oilfield-platform

# Scale frontend
kubectl scale deployment/frontend --replicas=3 -n oilfield-platform
```

### Auto-scaling (HPA already configured)

```bash
# Check HPA status
kubectl get hpa -n oilfield-platform

# Adjust HPA
kubectl patch hpa backend-hpa -n oilfield-platform -p \
  '{"spec":{"maxReplicas":20}}'
```

---

## 🎯 Production Checklist

- [ ] Secrets configured with strong passwords
- [ ] TLS certificates configured
- [ ] Network policies applied
- [ ] RBAC configured
- [ ] Resource limits set
- [ ] Health checks configured
- [ ] Monitoring enabled
- [ ] Logging configured
- [ ] Backup strategy implemented
- [ ] Disaster recovery plan documented
- [ ] Load testing completed
- [ ] Security scanning performed

---

**Last Updated**: 2024-12-30

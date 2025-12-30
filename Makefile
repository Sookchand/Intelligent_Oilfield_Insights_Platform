.PHONY: help build up down logs test clean deploy k8s-deploy

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Docker Compose Commands
build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## View logs from all services
	docker-compose logs -f

restart: ## Restart all services
	docker-compose restart

ps: ## Show running containers
	docker-compose ps

# Database Commands
db-init: ## Initialize databases with seed data
	@echo "Initializing PostgreSQL..."
	docker-compose exec postgres psql -U oilfield_user -d oilfield_production -f /docker-entrypoint-initdb.d/seed_sql.sql
	@echo "Initializing Neo4j..."
	docker-compose exec neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass -f /var/lib/neo4j/import/seed_graph.cypher

db-reset: ## Reset all databases
	docker-compose down -v
	docker-compose up -d
	sleep 30
	$(MAKE) db-init

# Testing Commands
test: ## Run all tests
	@echo "Running backend tests..."
	cd backend && pytest tests/ -v
	@echo "Running frontend tests..."
	cd frontend && npm test

test-backend: ## Run backend tests only
	cd backend && pytest tests/ -v --cov=. --cov-report=html

test-frontend: ## Run frontend tests only
	cd frontend && npm test -- --coverage

lint: ## Run linters
	cd backend && black --check . && flake8 .
	cd frontend && npm run lint

format: ## Format code
	cd backend && black .
	cd frontend && npm run format

# Kubernetes Commands
k8s-deploy: ## Deploy to Kubernetes
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/secrets.yaml
	kubectl apply -f k8s/postgres-deployment.yaml
	kubectl apply -f k8s/neo4j-deployment.yaml
	kubectl apply -f k8s/minio-deployment.yaml
	kubectl apply -f k8s/qdrant-deployment.yaml
	kubectl apply -f k8s/backend-deployment.yaml
	kubectl apply -f k8s/frontend-deployment.yaml
	kubectl apply -f k8s/ingress.yaml

k8s-delete: ## Delete Kubernetes resources
	kubectl delete namespace oilfield-platform

k8s-status: ## Check Kubernetes deployment status
	kubectl get all -n oilfield-platform

k8s-logs: ## View Kubernetes logs
	kubectl logs -n oilfield-platform -l app=backend --tail=100 -f

# Development Commands
dev-backend: ## Run backend in development mode
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run frontend in development mode
	cd frontend && npm run dev

# Cleanup Commands
clean: ## Clean up containers, volumes, and images
	docker-compose down -v
	docker system prune -f

clean-all: ## Clean everything including images
	docker-compose down -v --rmi all
	docker system prune -af

# Utility Commands
shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

shell-postgres: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U oilfield_user -d oilfield_production

shell-neo4j: ## Open Neo4j Cypher shell
	docker-compose exec neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass

health-check: ## Check health of all services
	@echo "Checking backend..."
	@curl -f http://localhost:8000/health || echo "Backend is down"
	@echo "\nChecking frontend..."
	@curl -f http://localhost:3000 || echo "Frontend is down"
	@echo "\nChecking PostgreSQL..."
	@docker-compose exec postgres pg_isready -U oilfield_user || echo "PostgreSQL is down"
	@echo "\nChecking Neo4j..."
	@curl -f http://localhost:7474 || echo "Neo4j is down"

# Production Commands
prod-build: ## Build production images
	docker build -t oilfield-backend:latest ./backend
	docker build -t oilfield-frontend:latest ./frontend

prod-push: ## Push images to registry
	docker tag oilfield-backend:latest ghcr.io/$(GITHUB_USER)/oilfield-backend:latest
	docker tag oilfield-frontend:latest ghcr.io/$(GITHUB_USER)/oilfield-frontend:latest
	docker push ghcr.io/$(GITHUB_USER)/oilfield-backend:latest
	docker push ghcr.io/$(GITHUB_USER)/oilfield-frontend:latest


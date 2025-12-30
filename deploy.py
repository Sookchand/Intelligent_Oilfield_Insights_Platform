"""
Automated deployment script for Intelligent Oilfield Insights Platform
"""
import subprocess
import time
import os
import sys
from pathlib import Path

def run_command(cmd, shell=True, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=shell, check=check, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def print_header(message):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(message)
    print("="*60 + "\n")

def print_step(step, total, message):
    """Print a step message"""
    print(f"[{step}/{total}] {message}")

def main():
    print_header("Intelligent Oilfield Insights Platform - Local Deployment")
    
    total_steps = 8
    
    # Step 1: Check Docker
    print_step(1, total_steps, "Checking Docker...")
    success, stdout, stderr = run_command("docker --version", check=False)
    if not success:
        print("❌ ERROR: Docker is not installed or not running")
        print("Please install Docker Desktop and start it")
        sys.exit(1)
    print(f"✅ Docker is running: {stdout.strip()}")
    
    # Step 2: Check environment
    print_step(2, total_steps, "Checking environment configuration...")
    if not os.path.exists(".env"):
        print("Creating .env file from .env.example...")
        run_command("copy .env.example .env" if os.name == 'nt' else "cp .env.example .env")
        print("\n⚠️  IMPORTANT: Please edit .env file and add your OPENAI_API_KEY")
        input("Press Enter after you've added your API key...")
    print("✅ Environment configured!")
    
    # Step 3: Stop existing containers
    print_step(3, total_steps, "Stopping existing containers...")
    run_command("docker-compose down", check=False)
    print("✅ Existing containers stopped!")
    
    # Step 4: Start Docker services
    print_step(4, total_steps, "Starting Docker services...")
    print("This may take a few minutes on first run...")
    success, stdout, stderr = run_command("docker-compose up -d")
    if not success:
        print(f"❌ ERROR: Failed to start Docker services")
        print(f"Error: {stderr}")
        sys.exit(1)
    print("✅ Docker services started!")
    
    # Step 5: Wait for services
    print_step(5, total_steps, "Waiting for services to initialize...")
    for i in range(30, 0, -1):
        print(f"\rWaiting {i} seconds...", end="", flush=True)
        time.sleep(1)
    print("\n✅ Services should be ready!")
    
    # Step 6: Initialize PostgreSQL
    print_step(6, total_steps, "Initializing PostgreSQL database...")
    if os.path.exists("data/seed_sql.sql"):
        cmd = 'docker-compose exec -T postgres psql -U oilfield_user -d oilfield_production < data/seed_sql.sql'
        success, stdout, stderr = run_command(cmd, check=False)
        if success:
            print("✅ PostgreSQL initialized!")
        else:
            print("⚠️  PostgreSQL initialization may have failed (this is normal if already initialized)")
    else:
        print("⚠️  Seed data file not found, skipping...")
    
    # Step 7: Initialize Neo4j
    print_step(7, total_steps, "Initializing Neo4j graph database...")
    if os.path.exists("data/seed_graph.cypher"):
        cmd = 'docker-compose exec -T neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data/seed_graph.cypher'
        success, stdout, stderr = run_command(cmd, check=False)
        if success:
            print("✅ Neo4j initialized!")
        else:
            print("⚠️  Neo4j initialization may have failed (this is normal if already initialized)")
    else:
        print("⚠️  Seed data file not found, skipping...")
    
    # Step 8: Verify deployment
    print_step(8, total_steps, "Verifying deployment...")
    time.sleep(5)
    
    success, stdout, stderr = run_command("curl -s http://localhost:8000/health", check=False)
    if success and "healthy" in stdout:
        print("✅ Backend is healthy!")
    else:
        print("⚠️  Backend may not be ready yet. Give it a few more seconds.")
    
    # Print summary
    print_header("Deployment Complete!")
    
    print("Services are now running:\n")
    print("  📱 Frontend:         http://localhost:3000")
    print("  🔧 Backend API:      http://localhost:8000")
    print("  📚 API Docs:         http://localhost:8000/docs")
    print("  🕸️  Neo4j Browser:    http://localhost:7474")
    print("  📦 MinIO Console:    http://localhost:9001")
    print("  🔍 Qdrant Dashboard: http://localhost:6333/dashboard")
    
    print("\nCredentials:")
    print("  Neo4j:  neo4j / oilfield_neo4j_pass")
    print("  MinIO:  minio_admin / minio_admin_pass")
    
    print("\nTo test the platform:")
    print('  curl -X POST http://localhost:8000/api/query -H "Content-Type: application/json" -d "{\\"query\\": \\"Why is production dropping at Rig Alpha?\\"}"')
    
    print("\nTo view logs:")
    print("  docker-compose logs -f backend")
    
    print("\nTo stop all services:")
    print("  docker-compose down")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()


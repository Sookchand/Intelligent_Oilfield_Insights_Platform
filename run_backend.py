"""
Simple script to start the backend server
Run this with: python run_backend.py
"""
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_docker_services():
    """Check if Docker services are running"""
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "--services", "--filter", "status=running"],
            capture_output=True,
            text=True,
            check=False
        )
        running_services = result.stdout.strip().split('\n')
        return 'postgres' in running_services
    except Exception as e:
        print(f"Warning: Could not check Docker services: {e}")
        return False

def start_docker_services():
    """Start Docker services if not running"""
    print("Starting Docker services...")
    try:
        subprocess.run(
            ["docker-compose", "up", "-d", "postgres", "neo4j", "qdrant", "minio"],
            check=True
        )
        print("✅ Docker services started!")
        print("⏳ Waiting 15 seconds for databases to initialize...")
        time.sleep(15)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Docker services: {e}")
        return False
    except FileNotFoundError:
        print("❌ Docker or docker-compose not found. Please install Docker Desktop.")
        return False

def start_backend():
    """Start the FastAPI backend"""
    backend_dir = Path(__file__).parent / "backend"
    venv_dir = Path(__file__).parent / "venv"

    print("\n" + "="*60)
    print("Starting Intelligent Oilfield Insights Platform Backend")
    print("="*60)
    print()

    # Check if venv exists
    if venv_dir.exists():
        print("✅ Virtual environment found")
        # Use the venv's Python interpreter
        venv_python = venv_dir / "Scripts" / "python.exe"
        if not venv_python.exists():
            print(f"⚠️  venv Python not found at {venv_python}, using system Python")
            python_executable = sys.executable
        else:
            print(f"✅ Using venv Python: {venv_python}")
            python_executable = str(venv_python)
    else:
        print("⚠️  No virtual environment found, using system Python")
        python_executable = sys.executable

    # Check if backend directory exists
    if not backend_dir.exists():
        print(f"❌ Backend directory not found: {backend_dir}")
        return False

    # Check if main.py exists
    main_file = backend_dir / "main.py"
    if not main_file.exists():
        print(f"❌ main.py not found: {main_file}")
        return False
    
    # Check Docker services
    if not check_docker_services():
        print("⚠️  Database services not running.")
        response = input("Start Docker services now? (y/n): ")
        if response.lower() == 'y':
            if not start_docker_services():
                return False
        else:
            print("⚠️  Continuing without databases (some features may not work)")
    else:
        print("✅ Database services are running")
    
    print()
    print("🚀 Starting FastAPI server...")
    print()
    print("📍 Backend API:      http://localhost:8000")
    print("📚 API Docs:         http://localhost:8000/docs")
    print("📖 ReDoc:            http://localhost:8000/redoc")
    print()
    print("Press Ctrl+C to stop the server")
    print("="*60)
    print()
    
    # Wait a moment then open browser
    time.sleep(2)
    print("🌐 Opening API documentation in browser...")
    webbrowser.open("http://localhost:8000/docs")
    
    # Start uvicorn
    try:
        subprocess.run(
            [python_executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            cwd=backend_dir,
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n✅ Backend server stopped")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting backend: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    try:
        success = start_backend()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✅ Stopped by user")
        sys.exit(0)


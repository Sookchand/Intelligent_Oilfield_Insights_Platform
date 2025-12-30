# Startup Guide - Intelligent Oilfield Insights Platform

## Quick Start (Windows)

### Option 1: Using Batch Scripts (Recommended)

1. **Start Database Services**
   ```cmd
   docker-compose up -d postgres neo4j qdrant minio
   ```

2. **Start Backend Server**
   - Open **Command Prompt** (not PowerShell)
   - Navigate to project directory:
     ```cmd
     cd c:\Project\IntelligentOilfieldInsightPlatform
     ```
   - Run the startup script:
     ```cmd
     start_backend.bat
     ```

3. **Test the Backend** (in a new Command Prompt window)
   ```cmd
   test_backend.bat
   ```

### Option 2: Manual Startup

1. **Start Databases**
   ```cmd
   docker-compose up -d postgres neo4j qdrant minio
   ```

2. **Wait for databases to be healthy** (30-60 seconds)
   ```cmd
   docker-compose ps
   ```

3. **Start Backend** (in Command Prompt, not PowerShell)
   ```cmd
   cd backend
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**
   - Health Check: http://localhost:8000/health
   - API Docs: http://localhost:8000/docs
   - Interactive API: http://localhost:8000/redoc

## Troubleshooting

### Issue: "Activation of the selected Python environment is not supported in PowerShell"

**Solution**: Use Command Prompt instead of PowerShell
- Press `Win + R`
- Type `cmd` and press Enter
- Navigate to the project directory
- Run the commands

### Issue: "Port already in use"

**Solution**: The ports have been configured to avoid conflicts:
- PostgreSQL: 5433 (external) → 5432 (internal)
- Neo4j: 7474, 7687
- MinIO: 9002 (API), 9003 (Console)
- Qdrant: 6333
- Backend: 8000

If you still have conflicts, check what's using the ports:
```cmd
netstat -ano | findstr :8000
```

### Issue: "Connection refused" when accessing http://localhost:8000

**Checklist**:
1. Is the backend running? Check the Command Prompt window
2. Are databases healthy? Run `docker-compose ps`
3. Any errors in the backend logs? Check the Command Prompt output
4. Try accessing http://127.0.0.1:8000/docs instead

### Issue: Backend starts but shows errors

**Common causes**:
1. **Missing dependencies**: Run `pip install -r requirements.txt`
2. **Database not ready**: Wait 30 seconds after starting Docker services
3. **Wrong Python version**: Requires Python 3.11+

## Verification Steps

### 1. Check Docker Services

```cmd
docker-compose ps
```

Expected output: All services should show "healthy" or "running"

### 2. Test Health Endpoint

```cmd
curl http://localhost:8000/health
```

Expected output:
```json
{"status": "healthy", "timestamp": "..."}
```

### 3. Test Query Endpoint

```cmd
curl -X POST http://localhost:8000/api/query -H "Content-Type: application/json" -d "{\"query\": \"Why is production dropping at Rig Alpha?\"}"
```

Expected output: JSON with answer, reasoning_trace, and confidence

### 4. Access API Documentation

Open in browser: http://localhost:8000/docs

You should see the FastAPI Swagger UI with all endpoints documented.

## Service URLs

Once everything is running:

| Service | URL | Credentials |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| PostgreSQL | localhost:5433 | oilfield_user / oilfield_pass |
| Neo4j Browser | http://localhost:7474 | neo4j / oilfield_neo4j_pass |
| MinIO Console | http://localhost:9003 | minio_admin / minio_admin_pass |
| Qdrant Dashboard | http://localhost:6333/dashboard | - |

## Sample API Requests

### Health Check
```bash
GET http://localhost:8000/health
```

### Natural Language Query
```bash
POST http://localhost:8000/api/query
Content-Type: application/json

{
  "query": "Why is production dropping at Rig Alpha?"
}
```

### Database Status
```bash
GET http://localhost:8000/api/status/databases
```

## Next Steps

1. ✅ Start the backend using Command Prompt
2. ✅ Verify http://localhost:8000/docs loads
3. ✅ Test a sample query
4. 🔄 Build the frontend (Next.js)
5. 🔄 Write tests
6. 🔄 Deploy to production

## Getting Help

If you encounter issues:

1. Check the backend logs in the Command Prompt window
2. Check Docker logs: `docker-compose logs -f postgres neo4j`
3. Verify all dependencies are installed: `pip list`
4. Ensure you're using Command Prompt, not PowerShell
5. Check that port 8000 is not in use by another application

## Stopping Services

### Stop Backend
- Press `Ctrl+C` in the Command Prompt window running uvicorn

### Stop Databases
```cmd
docker-compose down
```

### Stop Everything and Clean Up
```cmd
docker-compose down -v
```
(Warning: This will delete all database data)


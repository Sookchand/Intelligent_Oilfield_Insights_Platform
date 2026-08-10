# ⚡ Startup Cheat Sheet

## 🚀 Method 1: One-Click Startup (EASIEST!)

**Just double-click:** `START_ALL.bat`

✅ Done! Everything starts automatically.

---

## 🚀 Method 2: Manual Startup (3 Terminals)

### Terminal 1: Databases
```cmd
docker-compose up -d
```

### Terminal 2: Backend (with venv)
```cmd
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

### Terminal 3: Frontend
```cmd
cd frontend
npm run dev
```

**Open:** http://localhost:3000

---

## ✅ Success Check

| Service | Check | Expected |
|---------|-------|----------|
| **Databases** | `docker ps` | 4 containers |
| **Backend** | http://localhost:8000/docs | Swagger UI |
| **Frontend** | http://localhost:3000 | "All Systems Operational" |

---

## 🛑 Stop Everything

```cmd
Ctrl+C          # In backend terminal
Ctrl+C          # In frontend terminal
docker-compose down
```

---

## 🐛 Quick Fixes

### Port in use?
```cmd
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Frontend exits immediately?
❌ Using PowerShell  
✅ Use Command Prompt (cmd.exe)

### Venv not found?
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📚 Full Docs

- **STARTUP_PIPELINE.md** - Complete pipeline
- **QUICK_REFERENCE.md** - Detailed reference
- **TESTING_CHECKLIST.md** - Test everything

---

## 🎯 URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000/docs |
| Neo4j | http://localhost:7474 |
| MinIO | http://localhost:9001 |


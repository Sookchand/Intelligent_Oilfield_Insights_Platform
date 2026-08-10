# 🎨 Frontend Startup Guide

## ⚡ Quick Start (30 Seconds) - VERIFIED WORKING ✅

### **Method 1: Command Prompt** (RECOMMENDED - 100% Working!)

This is the **ONLY** method that works reliably on Windows with PowerShell issues.

1. **Open Command Prompt** (NOT PowerShell!)
   - Press `Win + R`
   - Type `cmd`
   - Press Enter

2. **Navigate to frontend:**

   ```cmd
   cd C:\Project\IntelligentOilfieldInsightPlatform\frontend
   ```

3. **Start the server:**

   ```cmd
   npm run dev
   ```

4. **Wait for this message:**

   ```text
   ▲ Next.js 14.2.0
   - Local:        http://localhost:3000

   ✓ Ready in 2.9s
   ```

   **IMPORTANT:** The terminal should **stay open** and NOT return to a prompt!

5. **Open browser to:**

   ```text
   http://localhost:3000
   ```

6. **Verify it's working:**
   - ✅ You should see "All Systems Operational"
   - ✅ All 4 databases showing "Connected" (green)
   - ✅ Demo query cards are clickable
   - ✅ Query input box is ready

---

### **Method 2: Double-Click Batch File** (Alternative)

1. Navigate to: `C:\Project\IntelligentOilfieldInsightPlatform\frontend`
2. **Double-click** `start-dev.bat`
3. A Command Prompt window will open
4. Wait for "✓ Ready in X.Xs" message
5. Open browser to: **<http://localhost:3000>**

---

## ⚠️ IMPORTANT: Use Command Prompt, NOT PowerShell

### Why?

PowerShell has issues with Node.js process management and environment activation.

### How to tell which shell you're using

- **Command Prompt**: Prompt looks like `C:\>`
- **PowerShell**: Prompt looks like `PS C:\>`

### How to switch to Command Prompt in VS Code

1. Click the dropdown next to `+` in the terminal
2. Select **"Command Prompt"**
3. Close any PowerShell terminals

---

## ✅ Verify It's Running

### Check 1: Terminal Output

You should see:

```
✓ Ready in 2.9s
```

And the terminal should **stay open** (not return to prompt).

### Check 2: Browser

Open <http://localhost:3000> - you should see the Query Dashboard.

### Check 3: Process

In a new Command Prompt:

```cmd
netstat -ano | findstr :3000
```

Should show a LISTENING process.

---

## 🎮 Try It Out

Once the frontend is running:

1. **Go to**: <http://localhost:3000>
2. **You should see**:
   - Beautiful gradient UI
   - "Ask Anything About Your Oilfield" header
   - Database connectivity status
   - 4 demo query cards
   - Query input box

3. **Click a demo query** like:
   - "Why is production dropping at Rig Alpha?"

4. **Click "Ask AI"**

5. **See the results** with:
   - Typewriter effect answer
   - Confidence score
   - Data sources used
   - Processing steps

6. **Click "View Explainability"** to see:
   - Agent workflow visualization
   - Detailed reasoning timeline
   - SQL/Cypher queries
   - Confidence breakdown
   - Data source attribution
   - Knowledge graph

---

## 🐛 Troubleshooting

### Problem: "ERR_CONNECTION_REFUSED"

**Cause**: Server not running or crashed

**Solution**:

```cmd
# Check if Node is running
tasklist | findstr node

# If not, start the server
cd frontend
npm run dev
```

### Problem: "Port 3000 already in use"

**Solution**:

```cmd
# Find the process using port 3000
netstat -ano | findstr :3000

# Kill it (replace <PID> with the actual PID)
taskkill /PID <PID> /F

# Start again
npm run dev
```

### Problem: "Module not found" errors

**Solution**:

```cmd
cd frontend
npm install
npm run dev
```

### Problem: Server says "Ready" but then exits

**Cause**: Using PowerShell instead of Command Prompt

**Solution**:

1. Close PowerShell
2. Open Command Prompt (cmd.exe)
3. Run `npm run dev` again

### Problem: Blank page in browser

**Check**:

1. Is backend running? (<http://localhost:8000/docs>)
2. Open browser console (F12) - any errors?
3. Check terminal for errors

**Solution**:

```cmd
# Rebuild the frontend
npm run build

# Start dev server
npm run dev
```

---

## 🛑 Stop the Server

### Method 1: Keyboard

Press `Ctrl + C` in the Command Prompt window

### Method 2: Close Window

Just close the Command Prompt window

### Method 3: Kill Process

```cmd
taskkill /F /IM node.exe
```

---

## 📁 What's Running?

When you start the frontend, you're running:

- **Next.js Development Server** on port 3000
- **Hot Module Replacement** (auto-refresh on code changes)
- **TypeScript Compiler** (type checking)
- **Tailwind CSS** (styling)

---

## 🔧 Development Mode Features

### Auto-Refresh

- Edit any file in `frontend/`
- Browser automatically refreshes
- No need to restart server

### Error Overlay

- TypeScript errors show in browser
- Helpful error messages
- Click to open file in editor

### Fast Refresh

- Component state preserved on edit
- Instant feedback
- No full page reload

---

## 📊 Available Pages

Once running, you can access:

- **`/`** - Query Dashboard (main page)
- **`/explainability`** - AI Explainability Dashboard
- **`/business`** - Business Impact (placeholder)
- **`/data`** - Data Explorer (placeholder)
- **`/system`** - System Monitor (placeholder)

---

## 🚀 Production Build

To create a production build:

```cmd
cd frontend
npm run build
npm start
```

This creates an optimized build in `.next/` folder.

---

## 📝 Common Commands

```cmd
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Install dependencies
npm install

# Add a new package
npm install <package-name>
```

---

## 🎯 Next Steps

1. ✅ Start the frontend using this guide
2. ✅ Make sure backend is running (see `QUICK_START.md`)
3. ✅ Test the Query Dashboard
4. ✅ Explore the Explainability features
5. 📖 Read `frontend/README.md` for more details

---

## 🆘 Still Having Issues?

### Checklist

- [ ] Using Command Prompt (not PowerShell)?
- [ ] Node.js installed? (`node --version`)
- [ ] Dependencies installed? (`npm install`)
- [ ] Port 3000 free? (`netstat -ano | findstr :3000`)
- [ ] Backend running? (<http://localhost:8000/docs>)

### Get Help

1. Check the terminal output for error messages
2. Check browser console (F12) for errors
3. Read `frontend/README.md`
4. Read `START_SERVERS.md`

---

**Ready to start?** Just double-click `frontend/start-dev.bat` and you're good to go! 🚀

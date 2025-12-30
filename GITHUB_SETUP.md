# GitHub Repository Setup Guide

This guide will help you create and push the Intelligent Oilfield Insights Platform to GitHub.

## 📋 Prerequisites

- Git installed on your system
- GitHub account (https://github.com/Sookchand)
- GitHub Personal Access Token (for authentication)

---

## 🚀 Method 1: Automated Setup (Recommended)

### For Windows (PowerShell)

```powershell
# 1. Run the setup script
.\setup-github.ps1

# 2. Follow the prompts to enter your Git username and email

# 3. Create the repository on GitHub (see step-by-step below)

# 4. Push to GitHub
.\setup-github.ps1 -Push
```

### For Linux/Mac (Bash)

```bash
# 1. Make script executable
chmod +x setup-github.sh

# 2. Run the setup script
./setup-github.sh

# 3. Follow the prompts to enter your Git username and email

# 4. Create the repository on GitHub (see step-by-step below)

# 5. Push to GitHub
./setup-github.sh --push
```

---

## 🔧 Method 2: Manual Setup

### Step 1: Initialize Git Repository

```bash
# Navigate to project directory
cd c:\Project\IntelligentOilfieldInsightPlatform

# Initialize git
git init

# Configure git user
git config user.name "Sookchand"
git config user.email "your-email@example.com"
```

### Step 2: Add Files and Commit

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Intelligent Oilfield Insights Platform

- Complete Docker Compose setup for local development
- Kubernetes manifests for production deployment
- CI/CD pipeline with GitHub Actions
- Implementation guide for all 7 test questions
- MinIO for object storage
- Multi-agent orchestration with LangGraph
- PostgreSQL, Neo4j, and Qdrant integration
- Comprehensive documentation"
```

### Step 3: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new

2. **Fill in repository details**:
   - **Repository name**: `Intelligent_Oilfield_Insights_Platform`
   - **Description**: `Enterprise-Grade Agentic RAG system built with LangGraph, Neo4j, and PostgreSQL to unify siloed Oil & Gas data into a single, natural-language reasoning interface`
   - **Visibility**: Choose Public or Private
   - **⚠️ IMPORTANT**: Do NOT check any of these boxes:
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license

3. **Click**: "Create repository"

### Step 4: Connect and Push

```bash
# Add remote origin
git remote add origin https://github.com/Sookchand/Intelligent_Oilfield_Insights_Platform.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## 🔐 Authentication Options

### Option 1: Personal Access Token (Recommended)

1. **Generate Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `workflow`
   - Click "Generate token"
   - **Copy the token** (you won't see it again!)

2. **Use Token for Authentication**:
   ```bash
   # When prompted for password, use the token instead
   git push -u origin main
   # Username: Sookchand
   # Password: <paste-your-token-here>
   ```

3. **Cache Credentials** (optional):
   ```bash
   # Windows
   git config --global credential.helper wincred
   
   # Linux/Mac
   git config --global credential.helper cache
   ```

### Option 2: SSH Key

1. **Generate SSH Key**:
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```

2. **Add to GitHub**:
   - Copy public key: `cat ~/.ssh/id_ed25519.pub`
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste and save

3. **Use SSH URL**:
   ```bash
   git remote set-url origin git@github.com:Sookchand/Intelligent_Oilfield_Insights_Platform.git
   git push -u origin main
   ```

---

## ✅ Verify Setup

After pushing, verify your repository:

1. **Visit**: https://github.com/Sookchand/Intelligent_Oilfield_Insights_Platform

2. **Check that all files are present**:
   - ✅ README.md
   - ✅ docker-compose.yml
   - ✅ k8s/ directory
   - ✅ .github/workflows/
   - ✅ Documentation files

3. **Enable GitHub Actions**:
   - Go to "Actions" tab
   - Click "I understand my workflows, go ahead and enable them"

---

## 🎯 Next Steps After Setup

### 1. Configure Repository Settings

```bash
# Add repository description
# Go to: https://github.com/Sookchand/Intelligent_Oilfield_Insights_Platform/settings

# Add topics:
# - langgraph
# - neo4j
# - postgresql
# - kubernetes
# - docker
# - oil-and-gas
# - agentic-rag
# - fastapi
# - nextjs
```

### 2. Set Up GitHub Secrets (for CI/CD)

Go to: Settings → Secrets and variables → Actions

Add these secrets:
- `OPENAI_API_KEY`: Your OpenAI API key
- `KUBE_CONFIG`: Base64-encoded kubeconfig (for K8s deployment)

### 3. Enable GitHub Pages (Optional)

If you want to host documentation:
- Go to: Settings → Pages
- Source: Deploy from a branch
- Branch: main / docs

### 4. Protect Main Branch

- Go to: Settings → Branches
- Add rule for `main`
- Enable:
  - ✅ Require pull request reviews
  - ✅ Require status checks to pass
  - ✅ Require branches to be up to date

---

## 🔄 Common Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create new branch
git checkout -b feature/new-feature

# Push branch
git push -u origin feature/new-feature

# Pull latest changes
git pull origin main

# View remotes
git remote -v
```

---

## 🆘 Troubleshooting

### Issue: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/Sookchand/Intelligent_Oilfield_Insights_Platform.git
```

### Issue: "failed to push some refs"

```bash
# Pull first, then push
git pull origin main --rebase
git push -u origin main
```

### Issue: Authentication failed

```bash
# Use Personal Access Token instead of password
# Or set up SSH authentication (see above)
```

### Issue: Large files rejected

```bash
# Check file sizes
git ls-files -s | awk '{print $4, $2}' | sort -n -r | head -20

# Remove large files from git
git rm --cached large-file.bin
git commit --amend
```

---

## 📚 Additional Resources

- **GitHub Docs**: https://docs.github.com/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **GitHub Actions**: https://docs.github.com/en/actions

---

**Ready to push!** 🚀

Run `.\setup-github.ps1` (Windows) or `./setup-github.sh` (Linux/Mac) to get started!


#!/bin/bash

# GitHub Repository Setup Script
# This script initializes git and pushes to GitHub

set -e

GITHUB_USERNAME="Sookchand"
REPO_NAME="Intelligent_Oilfield_Insights_Platform"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "🚀 Setting up GitHub repository: ${REPO_NAME}"
echo "================================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already initialized"
fi

# Configure git user (update with your details)
echo "👤 Configuring git user..."
read -p "Enter your Git username (default: ${GITHUB_USERNAME}): " GIT_USER
GIT_USER=${GIT_USER:-$GITHUB_USERNAME}

read -p "Enter your Git email: " GIT_EMAIL

git config user.name "$GIT_USER"
git config user.email "$GIT_EMAIL"
echo "✅ Git user configured"

# Add all files
echo "📝 Adding files to git..."
git add .
echo "✅ Files added"

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Intelligent Oilfield Insights Platform

- Complete Docker Compose setup for local development
- Kubernetes manifests for production deployment
- CI/CD pipeline with GitHub Actions
- Implementation guide for all 7 test questions
- MinIO for object storage
- Multi-agent orchestration with LangGraph
- PostgreSQL, Neo4j, and Qdrant integration
- Comprehensive documentation"
echo "✅ Initial commit created"

# Add remote origin
echo "🔗 Adding remote origin..."
if git remote | grep -q origin; then
    echo "⚠️  Remote 'origin' already exists. Removing..."
    git remote remove origin
fi
git remote add origin "$REPO_URL"
echo "✅ Remote origin added: $REPO_URL"

# Rename branch to main if needed
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "🔄 Renaming branch to 'main'..."
    git branch -M main
    echo "✅ Branch renamed to 'main'"
fi

echo ""
echo "================================================"
echo "✅ Git repository setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Create the repository on GitHub:"
echo "   👉 Go to: https://github.com/new"
echo "   👉 Repository name: ${REPO_NAME}"
echo "   👉 Description: Enterprise-Grade Agentic RAG system for Oil & Gas data unification"
echo "   👉 Make it Public or Private"
echo "   👉 DO NOT initialize with README, .gitignore, or license"
echo "   👉 Click 'Create repository'"
echo ""
echo "2. After creating the repository, run:"
echo "   git push -u origin main"
echo ""
echo "3. Or run this script with --push flag:"
echo "   ./setup-github.sh --push"
echo "================================================"

# If --push flag is provided, push to GitHub
if [ "$1" == "--push" ]; then
    echo ""
    echo "🚀 Pushing to GitHub..."
    git push -u origin main
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Repository is now available at:"
    echo "   https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
fi


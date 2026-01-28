# GitHub Repository Setup Guide

This guide walks you through pushing the SIRA project to GitHub.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click **+** → **New repository**
3. Repository name: `sira`
4. Description: `Shipping Intelligence & Risk Analytics Platform`
5. Keep it **Private** (recommended for production code)
6. **Do NOT** initialize with README (we already have one)
7. Click **Create repository**

## Step 2: Add Remote and Push

In your terminal:

```bash
cd /Users/sackson/Sira

# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/sira.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Using SSH (if configured)

```bash
git remote add origin git@github.com:YOUR_USERNAME/sira.git
git push -u origin main
```

## Step 3: Configure Repository Secrets

For CI/CD to work, add these secrets in GitHub:

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:

| Secret Name | Description |
|-------------|-------------|
| `PYTHONANYWHERE_USERNAME` | Your PythonAnywhere username |
| `PYTHONANYWHERE_API_TOKEN` | PythonAnywhere API token |
| `PYTHONANYWHERE_DOMAIN` | Your app domain (e.g., username.pythonanywhere.com) |

### Get PythonAnywhere API Token

1. Log into PythonAnywhere
2. Go to **Account** → **API token**
3. Create new token if needed

## Step 4: Configure Branch Protection (Optional)

1. Go to **Settings** → **Branches**
2. Add rule for `main` branch:
   - Require pull request reviews
   - Require status checks to pass
   - Require conversation resolution

## Step 5: Enable GitHub Actions

GitHub Actions should be enabled by default. Verify:

1. Go to **Actions** tab
2. You should see the CI workflow
3. It will run on every push to `main`

## Step 6: Create Development Branch

```bash
git checkout -b develop
git push -u origin develop
```

## Workflow

### Feature Development

```bash
# Create feature branch
git checkout -b feature/new-feature develop

# Make changes, then commit
git add .
git commit -m "Add new feature"

# Push and create PR
git push -u origin feature/new-feature
```

### Hotfix

```bash
git checkout -b hotfix/fix-bug main
# Fix the bug
git commit -m "Fix critical bug"
git push -u origin hotfix/fix-bug
# Create PR to main
```

## CI/CD Pipeline

The pipeline automatically:

1. **On Push to any branch**:
   - Runs linting (flake8)
   - Runs type checking (mypy)
   - Runs tests (pytest)

2. **On Push to main**:
   - All of above
   - Deploys to PythonAnywhere (if secrets configured)

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline -10

# Pull latest changes
git pull origin main

# Create and switch to new branch
git checkout -b branch-name

# Merge branch into main
git checkout main
git merge branch-name

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name
```

## Repository Structure

```
sira/
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI pipeline
│       └── deploy.yml      # Deployment pipeline
├── backend/                # FastAPI backend
├── frontend/               # React frontend
├── scripts/                # Setup scripts
├── docs/                   # Documentation
├── .gitignore
└── README.md
```

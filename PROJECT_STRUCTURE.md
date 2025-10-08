# Project Structure

## 📁 Clean & Organized File Structure

```
WMUStudentsUpdate/
│
├── backend/                        # Backend API (AWS Lambda)
│   ├── main.py                    # Flask REST API application
│   ├── students.db                # SQLite database (56 students)
│   └── __init__.py                # Python package marker
│
├── frontend/                       # Frontend (GitHub Pages)
│   └── index.html                 # Student submission form UI
│
├── documentation/                  # All project documentation
│   ├── AWS_DEPLOYMENT.md          # Step-by-step deployment guide
│   ├── AWS_IMPLEMENTATION.md      # Technical implementation details
│   ├── CHANGELOG.md               # Version history and updates
│   └── NEXT_STEPS.md              # Maintenance & troubleshooting
│
├── env/                            # Virtual environment (local only, not in git)
│
├── .gitignore                      # Git ignore rules
├── README.md                       # Main project documentation
├── requirements.txt                # Python dependencies
├── zappa_settings.json             # AWS Lambda deployment config
└── PROJECT_STRUCTURE.md            # This file
```

---

## 🗂️ File Descriptions

### Root Level

| File | Purpose |
|------|---------|
| **README.md** | Main project overview, API docs, quick start guide |
| **requirements.txt** | Python dependencies (Flask, Zappa, etc.) |
| **zappa_settings.json** | AWS Lambda deployment configuration |
| **.gitignore** | Files/folders excluded from git |

### backend/

| File | Purpose | Lines |
|------|---------|-------|
| **main.py** | Flask REST API with 4 endpoints | ~180 |
| **students.db** | SQLite database (56 student records) | 36 KB |
| **__init__.py** | Python package marker | 1 |

**Endpoints in main.py:**
- `GET /` - API information
- `POST /submit` - Add/update student
- `GET /students` - List all students
- `GET /students/<nama>` - Get specific student

### frontend/

| File | Purpose | Lines |
|------|---------|-------|
| **index.html** | Complete web app (HTML + CSS + JavaScript) | ~250 |

**Features:**
- Student submission form
- Real-time validation
- Success/error messaging
- Modern dark UI design
- Mobile responsive

### documentation/

| File | Purpose | Size |
|------|---------|------|
| **AWS_DEPLOYMENT.md** | Detailed deployment guide for beginners | 4.4 KB |
| **AWS_IMPLEMENTATION.md** | Technical architecture & AWS resources | 13 KB |
| **CHANGELOG.md** | Version history (v1.0 → v2.0) | 4.5 KB |
| **NEXT_STEPS.md** | Maintenance procedures & troubleshooting | 7.4 KB |

---

## 🗑️ Removed Files (Cleanup)

These files were **deleted** as they're no longer needed:

- ❌ `WMU Stuedents Upgrade 1.xlsx` - Original Excel file (migrated to SQLite)
- ❌ `temp_excel.xlsx` - Temporary Excel file
- ❌ `migrate_to_sqlite.py` - One-time migration script
- ❌ `templates/` folder - Old template (replaced by frontend/)
- ❌ `CLEANUP_GUIDE.md` - Redundant documentation

---

## 📊 Project Statistics

### Code Metrics
- **Total Files**: 11 (excluding env/, .git/)
- **Python Files**: 2 (main.py, __init__.py)
- **HTML Files**: 1 (index.html)
- **Documentation Files**: 5 (*.md)
- **Configuration Files**: 3 (.gitignore, requirements.txt, zappa_settings.json)

### Size Breakdown
- **Backend Code**: ~5 KB
- **Frontend Code**: ~9 KB
- **Database**: ~36 KB
- **Documentation**: ~29 KB
- **Total**: ~79 KB (excluding dependencies)

---

## 🔄 File Dependencies

```
zappa_settings.json
    └─> backend/main.py (app_function: "backend.main.app")
        └─> backend/students.db (database file)

requirements.txt
    ├─> Flask==3.0.0
    ├─> flask-cors==4.0.0
    ├─> Werkzeug==3.0.1
    ├─> gunicorn==21.2.0
    └─> zappa==0.59.0

frontend/index.html
    └─> API_URL: https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production
        └─> backend/main.py (Lambda function)
```

---

## 🚫 What's NOT in Git (.gitignore)

### Excluded Files/Folders:
```
# Virtual Environment
env/
venv/
ENV/

# Database (deployed separately)
*.db
students.db

# Python Cache
__pycache__/
*.pyc
*.pyo

# Excel Files
*.xlsx

# IDE
.vscode/
.idea/
.claude/

# OS
.DS_Store
Thumbs.db

# AWS Credentials
.aws/
```

---

## 📋 Maintenance Checklist

### Before Deploying
- [ ] Activate virtual environment: `.\env\Scripts\activate`
- [ ] Test locally: `python backend/main.py`
- [ ] Check database exists: `backend/students.db`
- [ ] Verify Python version: `python --version` (must be 3.12.x)

### Deploying Backend
- [ ] Run: `zappa update production`
- [ ] Check logs: `zappa tail production`
- [ ] Test API endpoint with curl

### Deploying Frontend
- [ ] Update `frontend/index.html` if needed
- [ ] Commit: `git add frontend/index.html && git commit -m "Update frontend"`
- [ ] Push: `git push`
- [ ] Wait 1-2 minutes for GitHub Pages to update

---

## 🎯 Quick Reference

### Common Commands
```bash
# Activate environment
.\env\Scripts\activate

# Run locally
python backend/main.py

# Deploy to Lambda
zappa update production

# View logs
zappa tail production

# Commit changes
git add .
git commit -m "Description"
git push
```

### Important URLs
- **Frontend**: https://rfldn0.github.io/WMUStudentsUpdate/
- **API**: https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production
- **Repo**: https://github.com/rfldn0/WMUStudentsUpdate

---

**Last Updated**: October 8, 2025
**Structure Version**: 2.0 (Reorganized)

# WMU Student Data Update System

A modern serverless web application for managing Western Michigan University student information. Built with AWS Lambda, API Gateway, and GitHub Pages.

## 🏗️ Architecture

- **Frontend**: Static HTML/CSS/JavaScript → GitHub Pages
- **Backend**: Flask REST API → AWS Lambda (Serverless)
- **API Gateway**: RESTful endpoints with auto-scaling
- **Database**: SQLite (bundled with Lambda function)

## 📁 Project Structure

```
WMUStudentsUpdate/
├── backend/                    # Backend API (AWS Lambda)
│   ├── main.py                # Flask application
│   ├── students.db            # SQLite database
│   └── __init__.py            # Package marker
├── frontend/                   # Frontend (GitHub Pages)
│   └── index.html             # Student submission form
├── documentation/              # Project documentation
│   ├── AWS_DEPLOYMENT.md      # Deployment guide
│   ├── AWS_IMPLEMENTATION.md  # Technical details
│   ├── CHANGELOG.md           # Version history
│   └── NEXT_STEPS.md          # Maintenance guide
├── env/                        # Virtual environment (local only)
├── requirements.txt            # Python dependencies
├── zappa_settings.json         # AWS Lambda configuration
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🚀 Live Deployment

- **Frontend**: https://rfldn0.github.io/WMUStudentsUpdate/
- **Backend API**: https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production
- **Platform**: AWS Lambda + API Gateway (Serverless)
- **Cost**: ~$0.05/year (99% savings vs traditional hosting)

## ✨ Features

- ✅ Clean web form for data entry
- ✅ SQLite database for fast, reliable storage
- ✅ Case-insensitive duplicate detection
- ✅ Auto-generates unique student IDN
- ✅ Update existing or add new students
- ✅ CORS enabled for cross-origin requests
- ✅ RESTful API with multiple endpoints
- ✅ Modern dark UI design
- ✅ Serverless auto-scaling

## 📡 API Endpoints

### GET /
Returns API information and statistics

**Response:**
```json
{
  "message": "WMU Student Update API",
  "database": "SQLite",
  "total_students": 56,
  "frontend": "https://rfldn0.github.io/WMUStudentsUpdate/",
  "endpoints": { ... }
}
```

### POST /submit
Submit or update student data (accepts form-data or JSON)

**Request:**
```json
{
  "nama": "John Doe",
  "jurusan": "Computer Science",
  "university": "Western Michigan University",
  "year": "Junior",
  "provinsi": "Papua"
}
```

**Response:**
```json
{
  "status": "added",
  "message": "Successfully added new record for John Doe",
  "data": {
    "idn": 57,
    "nama": "John Doe",
    ...
  }
}
```

### GET /students
List all students (ordered by name)

### GET /students/<nama>
Get specific student by name (case-insensitive)

## 🗄️ Database Schema

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idn INTEGER UNIQUE,
    nama TEXT NOT NULL UNIQUE COLLATE NOCASE,
    jurusan TEXT,
    university TEXT,
    year TEXT,
    provinsi TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 💻 Local Development

### Prerequisites

```bash
# Python 3.12 required
python --version  # Should be 3.12.x

# Create virtual environment
py -3.12 -m venv env

# Activate environment
.\env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Run Backend Locally

```bash
# Activate virtual environment
.\env\Scripts\activate

# Run Flask app
python backend/main.py

# Server starts at http://localhost:5000
```

## 🚀 Deployment

### Backend (AWS Lambda)

See [documentation/AWS_DEPLOYMENT.md](documentation/AWS_DEPLOYMENT.md) for detailed guide.

**Quick Deploy:**
```bash
# Activate virtual environment (Python 3.12)
.\env\Scripts\activate

# Deploy to AWS Lambda
zappa deploy production

# For updates
zappa update production

# View logs
zappa tail production
```

**Requirements:**
- AWS account
- AWS CLI configured
- Python 3.12 virtual environment
- Zappa installed

### Frontend (GitHub Pages)

1. Go to Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/frontend`
4. Save

Your frontend will be live at: `https://YOUR_USERNAME.github.io/WMUStudentsUpdate/`

## 📦 Dependencies

```
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
zappa==0.59.0
```

SQLite is included with Python (no installation needed)

## 📚 Documentation

- **[AWS_DEPLOYMENT.md](documentation/AWS_DEPLOYMENT.md)** - Step-by-step deployment guide
- **[AWS_IMPLEMENTATION.md](documentation/AWS_IMPLEMENTATION.md)** - Technical implementation details
- **[CHANGELOG.md](documentation/CHANGELOG.md)** - Version history and updates
- **[NEXT_STEPS.md](documentation/NEXT_STEPS.md)** - Maintenance and troubleshooting guide

## 🛠️ Troubleshooting

**Database not found**: Ensure `backend/students.db` exists in deployment

**CORS errors**: Check CORS configuration in `backend/main.py`

**Duplicate student error**: Name already exists (case-insensitive match)

**Lambda deployment fails**: Verify Python 3.12 virtual environment is active

**Cold starts**: First request after inactivity may take 1-2 seconds (normal for serverless)

**View logs**: Run `zappa tail production` to see real-time Lambda logs

## 🔐 Security & Best Practices

- ✅ Database excluded from version control
- ✅ CORS enabled for authorized domains
- ✅ SQL injection protection (parameterized queries)
- ✅ Case-insensitive unique constraints
- ✅ Input validation and sanitization
- ✅ AWS IAM roles for least privilege access

## 🤝 Contributing

1. Clone the repository
2. Create a feature branch
3. Make changes
4. Test locally
5. Update Lambda: `zappa update production`
6. Push to GitHub

## 📄 License

MIT License - Feel free to use for educational purposes

---

**Built with ❤️ for Western Michigan University Indonesian Students**

**Deployed on**: AWS Lambda (Serverless)
**Maintained by**: Victor Tabuni (rfldn0)
**Repository**: https://github.com/rfldn0/WMUStudentsUpdate

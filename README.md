# WMU Papuan Student Data Update System

``` save links:
https://us-east-1.console.aws.amazon.com/singlesignon/home?region=us-east-1#/instances/7223ffcfae0b672b/dashboard
```

A modern serverless web application for managing Western Michigan University student information. Built with AWS Lambda, API Gateway, and GitHub Pages.

## 🏗️ Architecture

- **Frontend**: Static HTML/CSS/JavaScript → GitHub Pages
- **Backend**: Flask REST API → AWS Lambda (Serverless)
- **API Gateway**: RESTful endpoints with auto-scaling
- **Database**: AWS DynamoDB (Serverless, fully persistent)

## 📁 Project Structure

```
WMUStudentsUpdate/
├── backend/                    # Backend API (AWS Lambda)
│   ├── main.py                # Flask application with DynamoDB
│   ├── db_manager.py          # Database management CLI tool
│   ├── students.db            # SQLite backup (deprecated)
│   └── __init__.py            # Package marker
├── docs/                       # Frontend (GitHub Pages)
│   └── index.html             # Student submission form
├── documentation/              # Project documentation
│   ├── AWS_DEPLOYMENT.md      # Deployment guide
│   ├── AWS_IMPLEMENTATION.md  # Technical details
│   ├── CHANGELOG.md           # Version history
│   ├── DYNAMODB_MIGRATION.md  # DynamoDB migration guide
│   └── NEXT_STEPS.md          # Maintenance guide
├── scripts/                    # Utility scripts
│   ├── create_dynamodb_table.py
│   ├── migrate_to_dynamodb.py
│   └── test_db_write.py
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
- ✅ **DynamoDB** - Fully persistent serverless database
- ✅ **Auto-formatting** - Names/majors auto-formatted to Title Case
- ✅ **Database Manager** - Interactive CLI tool for data management
- ✅ Case-insensitive duplicate detection
- ✅ Auto-generates unique student IDN
- ✅ Update existing or add new students
- ✅ CORS enabled for cross-origin requests
- ✅ RESTful API with multiple endpoints
- ✅ Modern dark UI design
- ✅ Serverless auto-scaling
- ✅ Export to CSV functionality

## 📡 API Endpoints

### GET /
Returns API information and statistics

**Response:**
```json
{
  "message": "WMU Student Update API",
  "database": "DynamoDB",
  "total_students": 58,
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

## 🗄️ Database Schema (DynamoDB)

**Table**: `wmu-students` (us-east-1)
**Billing**: Pay-per-request (on-demand)

| Field | Type | Description |
|-------|------|-------------|
| `idn` | Number | Primary key, unique student ID |
| `nama` | String | Student name (auto-formatted to Title Case) |
| `jurusan` | String | Major/field of study (auto-formatted) |
| `university` | String | University name |
| `year` | String | Academic year or graduation semester |
| `provinsi` | String | Province/region (auto-formatted) |
| `created_at` | String | ISO timestamp |
| `updated_at` | String | ISO timestamp |

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
3. Folder: `/docs`
4. Save

Your frontend will be live at: `https://YOUR_USERNAME.github.io/WMUStudentsUpdate/`

## 📦 Dependencies

```
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
zappa==0.59.0
boto3>=1.26.0
```

## 🛠️ Database Manager

Interactive CLI tool for managing DynamoDB data:

```bash
python backend/db_manager.py
```

**Features:**
- View all students in formatted table
- Search students by name
- Count by major/province
- Count graduated students (vs current students)
- Add/delete students
- Export to CSV

**Student Classification:**
- **Current Students**: Freshman, Sophomore, Junior, Senior
- **Graduated Students**: Graduation semester format (e.g., "FALL 2025", "SPRING 2026")

## 📚 Documentation

- **[AWS_DEPLOYMENT.md](documentation/AWS_DEPLOYMENT.md)** - Step-by-step deployment guide
- **[AWS_IMPLEMENTATION.md](documentation/AWS_IMPLEMENTATION.md)** - Technical implementation details
- **[CHANGELOG.md](documentation/CHANGELOG.md)** - Version history and updates
- **[NEXT_STEPS.md](documentation/NEXT_STEPS.md)** - Maintenance and troubleshooting guide

## 🛠️ Troubleshooting

**DynamoDB connection errors**: Verify AWS credentials and IAM permissions for DynamoDB

**CORS errors**: Check CORS configuration in `backend/main.py`

**GitHub Pages not updating**: Change folder to `/docs` in Settings → Pages

**Duplicate student detection**: Uses firstName + lastName matching (e.g., "John Doe" matches "John Middle Doe")

**Lambda deployment fails**: Verify Python 3.12 virtual environment is active

**Cold starts**: First request after inactivity may take 1-2 seconds (normal for serverless)

**View logs**: Run `zappa tail production` to see real-time Lambda logs

**DynamoDB permissions**: Lambda needs `AmazonDynamoDBFullAccess` policy attached

## 🔐 Security & Best Practices

- ✅ Serverless architecture (no exposed servers)
- ✅ CORS enabled for authorized domains
- ✅ DynamoDB parameterized queries (no injection vulnerabilities)
- ✅ Smart duplicate detection (firstName + lastName matching)
- ✅ Input validation and auto-formatting
- ✅ AWS IAM roles for least privilege access
- ✅ HTTPS-only via API Gateway

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

# WMU Student Data Update System

A modern web application for managing Western Michigan University student information. Built with a decoupled architecture featuring a static frontend on GitHub Pages and a Flask REST API backend on Render, using SQLite for data persistence.

## Architecture

- **Frontend**: Static HTML/CSS/JavaScript → GitHub Pages
- **Backend**: Flask REST API → Render
- **Database**: SQLite (lightweight, serverless, perfect for <100 students)

## Features

- ✅ Clean web form for data entry
- ✅ SQLite database for fast, reliable storage
- ✅ Case-insensitive duplicate detection
- ✅ Auto-generates unique student IDN
- ✅ Update existing or add new students
- ✅ CORS enabled for cross-origin requests
- ✅ RESTful API with multiple endpoints
- ✅ Modern dark UI design

## Live Deployment

- **Frontend**: https://rfldn0.github.io/WMUStudentsUpdate/
- **Backend API**: https://wmustudentsupdate.onrender.com

## API Endpoints

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

**Response (New Student):**
```json
{
  "status": "added",
  "message": "Successfully added new record for John Doe",
  "data": {
    "idn": 57,
    "nama": "John Doe",
    "jurusan": "Computer Science",
    "university": "Western Michigan University",
    "year": "Junior",
    "provinsi": "Papua"
  }
}
```

**Response (Existing Student):**
```json
{
  "status": "updated",
  "message": "Successfully updated record for John Doe",
  "data": { ... }
}
```

### GET /students
List all students (ordered by name)

**Response:**
```json
{
  "status": "success",
  "count": 56,
  "data": [ ... ]
}
```

### GET /students/<nama>
Get specific student by name (case-insensitive)

## Database Schema

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

## Local Development

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
python main.py
```

Server starts at `http://localhost:5000`

### Database Setup

The `students.db` file contains all student data. To recreate from Excel:

1. Download Excel file from SharePoint
2. Run migration script:
```bash
python migrate_to_sqlite.py
```

## Deployment

### Backend (Render)

1. **Push code to GitHub**
2. **Connect to Render**
3. **Configure Build Settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`

4. **Upload Database:**
   - Go to Render Dashboard → Shell
   - Upload `students.db` using Render's file upload
   - Or use `scp` if you have SSH access

### Frontend (GitHub Pages)

1. Go to Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/docs`
4. Save

Your frontend will be live at: `https://YOUR_USERNAME.github.io/WMUStudentsUpdate/`

## File Structure

```
WMUStudentsUpdate/
├── main.py                    # Flask API (SQLite backend)
├── docs/
│   └── index.html            # Static frontend
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── students.db              # SQLite database (not in git)
└── migrate_to_sqlite.py     # Excel → SQLite migration script
```

## How It Works

1. **User submits form** on GitHub Pages
2. **Frontend sends POST** request to Render API
3. **Backend checks** if student name exists (case-insensitive)
4. **Database updates** existing record or inserts new one
5. **API responds** with success/error message
6. **Frontend displays** result to user

## Data Migration from Excel

The original data was migrated from a SharePoint Excel file to SQLite:

- 56 students successfully migrated
- IDN numbers preserved from original data
- Timestamps added for created_at/updated_at tracking

## Security & Best Practices

- ✅ Database excluded from version control
- ✅ CORS enabled for authorized domains
- ✅ SQL injection protection (parameterized queries)
- ✅ Case-insensitive unique constraints
- ✅ Input validation and sanitization

## Dependencies

```
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

SQLite is included with Python (no installation needed)

## Troubleshooting

**Database not found**: Upload `students.db` to Render server

**CORS errors**: Check backend CORS configuration

**Duplicate student error**: Name already exists (case-insensitive match)

**Render build fails**: Verify `requirements.txt` is correct

## Contributing

1. Clone the repository
2. Make changes
3. Test locally
4. Push to GitHub
5. Render auto-deploys from main branch

## License

MIT License - Feel free to use for educational purposes

---

**Built with ❤️ for Western Michigan University Indonesian Students**

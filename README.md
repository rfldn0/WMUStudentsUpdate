# WMU Student Data Update System

A web application for updating student information in the "MICHIGAN STUDENTS DATA" Excel worksheet. The system uses a modern architecture with a static frontend hosted on GitHub Pages and a Flask backend API on Render.

## Architecture

- **Frontend**: Static HTML/CSS/JavaScript hosted on GitHub Pages
- **Backend**: Flask REST API deployed on Render
- **Database**: Excel file (WMU Stuedents Upgrade 1.xlsx)

## Features

- ✅ Web form for data entry
- ✅ Updates existing Excel file automatically
- ✅ Case-insensitive duplicate detection (by name)
- ✅ Update existing records or append new ones
- ✅ Auto-generates IDN for new students
- ✅ CORS enabled for cross-origin requests
- ✅ Modern dark UI design

## Live Deployment

- **Frontend**: https://rfldn0.github.io/WMUStudentsUpdate/
- **Backend API**: https://wmustudentsupdate.onrender.com

## Local Development

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run Backend Locally

```bash
python main.py
```

The API server will start at `http://localhost:5000`

### Test Locally

To test with the local backend, update the API_URL in `docs/index.html`:

```javascript
const API_URL = 'http://localhost:5000';
```

## API Endpoints

### GET /
Returns API information and available endpoints.

### POST /submit
Submit student data (accepts both form-data and JSON).

**Request (JSON)**:
```json
{
  "nama": "John Doe",
  "jurusan": "Computer Science",
  "university": "Western Michigan University",
  "year": "Junior",
  "provinsi": "Papua"
}
```

**Response**:
```json
{
  "status": "added",
  "message": "Successfully added new record for John Doe",
  "data": {
    "idn": 61,
    "nama": "John Doe",
    "jurusan": "Computer Science",
    "university": "Western Michigan University",
    "year": "Junior",
    "provinsi": "Papua"
  }
}
```

## Excel File Structure

The application works with these columns in the "MICHIGAN STUDENTS DATA" worksheet:

| Column | Field      | Description                    |
|--------|------------|--------------------------------|
| C      | IDN        | Auto-generated student ID      |
| D      | Nama       | Student name (used for lookup) |
| E      | Jurusan    | Major                          |
| F      | University | University name                |
| G      | Year       | Academic year                  |
| H      | Provinsi   | Province                       |

**Note**: Headers are in Row 3, data starts at Row 4

## How It Works

1. **Duplicate Detection**: Compares student names (case-insensitive)
   - "John Doe" = "john doe" = "JOHN DOE" (same person)
   - If match found: updates existing record (keeps same IDN)
   - If no match: adds new record with new IDN

2. **Cross-Origin Requests**: CORS enabled to allow GitHub Pages frontend to communicate with Render backend

3. **Data Persistence**: All changes are saved directly to the Excel file

## File Structure

```
WMUStudentsUpdate/
├── main.py                           # Flask API backend
├── docs/
│   └── index.html                   # Frontend (GitHub Pages)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── .gitignore                       # Git ignore rules
└── WMU Stuedents Upgrade 1.xlsx    # Excel database (not in git)
```

## Deployment

### Backend (Render)

1. Push code to GitHub
2. Connect repository to Render
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`

### Frontend (GitHub Pages)

1. Go to repository Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/docs`
4. Save

## Security Notes

- Excel file is excluded from git (.gitignore)
- CORS is enabled for all origins (configure as needed)
- Ensure Excel file exists on Render deployment

## Troubleshooting

**Excel file permission error**: Close Excel file if open

**CORS errors**: Ensure backend has flask-cors installed

**Render deployment fails**: Check that gunicorn is in requirements.txt

**Name not found when it should exist**: Check for extra spaces or special characters

## Dependencies

- Flask 3.0.0
- flask-cors 4.0.0
- openpyxl 3.1.2
- gunicorn 21.2.0
- Werkzeug 3.0.1

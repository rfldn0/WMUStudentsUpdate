# WMU Student Data Update System

A Flask web application that allows students to submit and update their information in the "MICHIGAN STUDENTS DATA" Excel worksheet. Data is automatically updated if the student name already exists (case-insensitive), or appended if it's a new student.

## Features

- ✅ Web form for data entry
- ✅ Updates existing Excel file: `WMU Stuedents Upgrade 1.xlsx`
- ✅ Works with "MICHIGAN STUDENTS DATA" worksheet
- ✅ Case-insensitive duplicate detection (by name)
- ✅ Update existing records or append new ones
- ✅ Auto-generates IDN for new students
- ✅ Simple dark UI (black, grey, white, blue, orange)

## Installation

### 1. Install Python Dependencies

```bash
pip install Flask openpyxl
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

The server will start at `http://localhost:5000`

## Usage

### Web Interface

1. Open your browser and go to `http://localhost:5000`
2. Fill in the form:
   - **Nama** (required) - Student's full name
   - **Jurusan** - Major
   - **University** - Default is "Western Michigan University"
   - **Year** - Freshman, Sophomore, Junior, or Senior
   - **Provinsi** - Province
3. Click Submit
4. If the student name exists (case-insensitive), their record will be updated
5. If the student is new, a new row will be appended with auto-generated IDN

### API Endpoint

You can also submit data programmatically using the JSON API:

```bash
curl -X POST http://localhost:5000/api/submit \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "John Doe",
    "jurusan": "Computer Science",
    "university": "Western Michigan University",
    "year": "Junior",
    "provinsi": "Jakarta"
  }'
```

Response:
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
    "provinsi": "Jakarta"
  }
}
```

## Excel File Structure

The application works with the following columns in the "MICHIGAN STUDENTS DATA" worksheet:

| Column | Field      | Description                    |
|--------|------------|--------------------------------|
| C      | IDN        | Auto-generated student ID      |
| D      | Nama       | Student name (used for lookup) |
| E      | Jurusan    | Major                          |
| F      | University | University name                |
| G      | Year       | Academic year                  |
| H      | Provinsi   | Province                       |

**Note**: Headers start at Row 3, Data starts at Row 4

## How Duplicate Detection Works

The system compares student names in a **case-insensitive** manner:
- "John Doe" = "john doe" = "JOHN DOE" (all treated as the same person)
- If a match is found, the existing record is updated (same IDN kept)
- If no match is found, a new record is added with a new IDN

## Color Scheme

- Background: Black (#1a1a1a)
- Container: Dark Grey (#2a2a2a)
- Text: White/Light Grey
- Primary Button: Blue (#2196F3)
- Required Field: Orange (#FF9800)
- Success: Green
- Update: Orange
- Error: Red

## File Structure

```
WMUStudentsUpdate/
├── main.py                           # Flask application
├── templates/
│   └── index.html                   # Web form
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── WMU Stuedents Upgrade 1.xlsx    # Your Excel file
└── inspect_excel.py                 # Helper script to view Excel structure
```

## Deployment Options

### Option 1: Run Locally
- Run `python main.py` on your machine
- Access via `http://localhost:5000`

### Option 2: Deploy to Cloud
- **PythonAnywhere**: Upload files and configure web app
- **Railway/Render**: Connect GitHub repo and deploy
- **Heroku**: Add `Procfile` with `web: python main.py`

### Option 3: Use ngrok for Public URL
```bash
# Run the app
python main.py

# In another terminal
ngrok http 5000
```

Then share the ngrok URL with students.

## Troubleshooting

**Excel file permission error**: Close the Excel file if it's open

**Port already in use**: Change the port number in main.py (last line)

**Module not found**: Run `pip install Flask openpyxl`

**Name not found when it should exist**: Check for extra spaces or special characters in the name

## Notes

- The Excel file must be closed when the application is writing to it
- IDN numbers are auto-incremented based on the highest existing IDN
- The application does NOT create a new Excel file - it uses the existing one
- Make sure to backup your Excel file before testing

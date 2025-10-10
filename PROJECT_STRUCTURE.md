# Project Structure

## Clean & Organized Structure

```
WMUStudentsUpdate/
├── backend/                        # Backend (Lambda + DynamoDB)
│   ├── main.py                    # Flask API with smart name matching + timezone
│   ├── db_manager.py              # Database management CLI (entry point)
│   ├── student_manager.py         # Core data operations module
│   ├── student_viewer.py          # Viewing operations module
│   ├── student_editor.py          # Editing operations module
│   ├── csv_exporter.py            # CSV export module
│   ├── menu_system.py             # Menu navigation module
├── docs/                           # Frontend (GitHub Pages)
│   ├── index.html                 # Student submission form
│   ├── script.js                  # Frontend JavaScript (modular)
│   └── style.css                  # Frontend styles (modular)
├── documentation/                  # All documentation
│   ├── README.md                  # Documentation index
│   ├── AWS_DEPLOYMENT.md          # Deployment guide
│   ├── AWS_IMPLEMENTATION.md      # Technical details
│   ├── CHANGELOG.md               # Version history (v2.3.0)
│   ├── DYNAMODB_MIGRATION.md      # DynamoDB migration guide
│   └── NEXT_STEPS.md              # Maintenance guide
├── scripts/                        # Utility scripts
│   ├── create_dynamodb_table.py   # Create DynamoDB table
│   ├── migrate_to_dynamodb.py     # Migrate SQLite → DynamoDB
│   └── test_db_write.py           # Test DynamoDB write
├── env/                            # Virtual environment (local only)
├── .gitignore                      # Git ignore rules
├── README.md                       # Main documentation
├── PROJECT_STRUCTURE.md            # This file (quick reference)
├── requirements.txt                # Python dependencies (incl. tzdata)
└── zappa_settings.json             # AWS Lambda configuration
```

---

## Key Features

### Timezone Fix (v2.3.0)
- **Eastern Time (America/Detroit)** - Timestamps match Michigan local time
- **Automatic DST handling** - No manual timezone adjustments needed
- **ISO 8601 with offset** - e.g., `2025-10-08T08:00:00-04:00`
- Fixes 4-5 hour UTC offset issue

### Smart Name Matching (v2.2.0)
- **firstName + lastName matching** - Prevents duplicates
- Example: "Aprilia Mabel" updates "Aprilia Weni Irjani Mabel"
- Preserves full legal names in database

### Graduated Students Tracking (v2.2.0)
- Count current vs graduated students
- Database Manager option #6
- Classification: Freshman/Sophomore/Junior/Senior vs graduation semester

### Auto-Formatting (v2.1.0)
- **Names**: `victor tabuni` → `Victor Tabuni`
- **Major**: `computer science` → `Computer Science`
- **Province**: `papua barat` → `Papua Barat`

### Database Manager Tool
```bash
python backend/db_manager.py
```

**Organized Menu System (v2.8.0):**

**Main Menu:**
1. View Data
2. Manage Students
3. Analytics & Statistics
4. Generate CSV Export
5. Exit

**Submenus:**
- **View Data:** Show all (sorting), Recent changes, Search
- **Manage Students:** Add, Edit (single/batch), Remove (single/batch)
- **Analytics:** Count total, by major, by province, graduated students
- **CSV Export:** All students or by province

---

## Database: DynamoDB

**Table**: `wmu-students` (us-east-1)
**Billing**: Pay-per-request (on-demand)

| Field | Type | Auto-Format | Description |
|-------|------|-------------|-------------|
| idn | Number | - | Primary key |
| nama | String | ✅ Title Case | Full name (preserved) |
| jurusan | String | ✅ Title Case | Major |
| university | String | - | University name |
| year | String | - | Year or graduation semester |
| provinsi | String | ✅ Title Case | Province |
| created_at | String | - | ISO timestamp with timezone (EDT/EST) |
| updated_at | String | - | ISO timestamp with timezone (EDT/EST) |

---

## Quick Commands

### Deploy
```bash
.\env\Scripts\activate       # Activate environment
zappa update production      # Update Lambda
zappa tail production        # View logs
```

### Manage Database
```bash
python backend/db_manager.py  # Interactive CLI tool
```

### Local Development
```bash
python backend/main.py        # Run API locally (port 5000)
```

---

## URLs

- **Frontend**: https://rfldn0.github.io/WMUStudentsUpdate/
- **API**: https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production
- **DynamoDB**: [Console](https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=wmu-students)

---

**Version**: 3.0.0 | **Status**: Production | **Students**: 58+

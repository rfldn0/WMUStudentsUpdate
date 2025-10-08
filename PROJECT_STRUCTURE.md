# Project Structure

## 📁 Clean & Organized Structure

```
WMUStudentsUpdate/
├── backend/                        # Backend (Lambda + DynamoDB)
│   ├── main.py                    # Flask API with auto-formatting
│   ├── db_manager.py              # Database management tool
│   ├── students.db                # SQLite backup (deprecated)
│   └── __init__.py
├── docs/                           # Frontend (GitHub Pages)
│   └── index.html
├── documentation/                  # All documentation
│   ├── AWS_DEPLOYMENT.md
│   ├── AWS_IMPLEMENTATION.md
│   ├── CHANGELOG.md
│   ├── DYNAMODB_MIGRATION.md
│   └── NEXT_STEPS.md
├── scripts/                        # Utility scripts
│   ├── create_dynamodb_table.py
│   ├── migrate_to_dynamodb.py
│   └── test_db_write.py
├── env/                            # Virtual environment (local)
├── README.md
├── PROJECT_STRUCTURE.md            # This file
├── requirements.txt
└── zappa_settings.json
```

---

## 🎯 Key Features

### Auto-Formatting (New!)
- **Names**: `victor tabuni` → `Victor Tabuni`
- **Major**: `computer science` → `Computer Science`
- **Province**: `papua barat` → `Papua Barat`

### Database Manager Tool
```bash
python backend/db_manager.py
```
- View all students (table format)
- Search by name
- Count by major/province
- Add/delete students
- Export to CSV

---

## 📊 Database: DynamoDB

**Table**: `wmu-students` (us-east-1)
**Billing**: Pay-per-request (on-demand)

| Field | Type | Auto-Format |
|-------|------|-------------|
| idn | Number | - |
| nama | String | ✅ Title Case |
| jurusan | String | ✅ Title Case |
| university | String | - |
| year | String | - |
| provinsi | String | ✅ Title Case |

---

## 🚀 Quick Commands

### Deploy
```bash
zappa update production      # Update Lambda
zappa tail production        # View logs
```

### Manage Database
```bash
python backend/db_manager.py  # Interactive tool
```

### Local Development
```bash
python backend/main.py        # Run API locally
```

---

## 🔗 URLs

- **Frontend**: https://rfldn0.github.io/WMUStudentsUpdate/
- **API**: https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production
- **DynamoDB**: [Console](https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=wmu-students)

---

**Version**: 2.1 | **Status**: Production ✅

# Changelog

All notable changes to WMU Student Data Update System will be documented in this file.

## [3.0.0] - 2025-10-10

### Code Cleanup & Documentation Professionalization

#### Removed
- **backend/__init__.py** - Empty file that was not needed for module structure
- **All emoji symbols from documentation** - Professional documentation standard
  - Removed decorative emojis from all markdown files
  - Removed emoji icons from menu descriptions
  - Maintained clean, professional appearance throughout

#### Changed
- **Documentation Style** - Converted all documentation to professional format
  - README.md - Removed all emojis and symbols
  - PROJECT_STRUCTURE.md - Removed all emojis and symbols
  - CHANGELOG.md - Removed all emojis and symbols
  - AWS_IMPLEMENTATION.md - Removed all emojis and symbols
  - AWS_DEPLOYMENT.md - Removed all emojis and symbols
  - NEXT_STEPS.md - Removed all emojis and symbols
  - DYNAMODB_MIGRATION.md - Removed all emojis and symbols

#### Improved
- **Professional Documentation** - All markdown files now follow enterprise documentation standards
- **Cleaner Repository** - Removed unused files
- **Better Readability** - Documentation is now more accessible and professional
- **Version Consistency** - Updated version numbers across all documentation to 3.0.0

---

## [2.9.0] - 2025-10-08

### Modularization: Separated Classes into Individual Files

#### Changed
- **Complete code modularization** - Split monolithic file into separate modules
  - Previous: Single 740-line file with all classes
  - Now: 6 separate modules with clear responsibilities

#### New Module Structure
```
backend/
├── db_manager.py          # Main entry point (42 lines)
├── student_manager.py     # Core data operations
├── student_viewer.py      # Viewing operations
├── student_editor.py      # Editing operations
├── csv_exporter.py        # CSV export
└── menu_system.py         # Menu navigation
```

#### Module Details

**db_manager.py** - Entry point
- Imports all modules
- Initializes components
- Starts application
- Clean and minimal (42 lines)

**student_manager.py** - Core data operations
- `StudentManager` class
- DynamoDB operations
- Data fetching and counting
- Graduated student analysis

**student_viewer.py** - Display operations
- `StudentViewer` class
- View all students (with sorting)
- View recent changes
- Search functionality
- Display helpers

**student_editor.py** - CRUD operations
- `StudentEditor` class
- Add students (single/multiple)
- Edit students (single/batch)
- Delete students (single/batch)

**csv_exporter.py** - Export operations
- `CSVExporter` class
- Export all students
- Export by province

**menu_system.py** - Navigation
- `MenuSystem` class
- Main menu
- All submenus (View, Manage, Analytics)

#### Benefits
- **Better organization** - Each file has single responsibility
- **Easier maintenance** - Changes isolated to specific modules
- **Improved readability** - Smaller, focused files
- **Better testing** - Each module can be tested independently
- **Easier collaboration** - Multiple developers can work on different modules
- **Reduced file size** - Main entry point is only 42 lines

#### Technical Details
- All imports handled in db_manager.py
- Consistent interface between modules
- Proper separation of concerns
- No code duplication

---

## [2.8.0] - 2025-10-08

### Code Refactoring: Class-based Architecture

#### Changed
- **Complete code refactoring** - Restructured from procedural to object-oriented design
  - Previous: 740+ lines with redundant code and repeated scan operations
  - Now: Clean class-based architecture with separation of concerns

#### Refactored Classes
- **StudentManager** - Core data operations and DynamoDB interactions
  - `get_all_students()` - Centralized method with pagination (eliminates redundancy)
  - `get_next_idn()` - IDN generation
  - `count_total()` - Total student count
  - `count_by_field()` - Generic counting method (replaces 3 separate functions)
  - `count_graduated()` - Graduated vs current students

- **StudentViewer** - All viewing operations
  - `view_all()` - Display all students with sorting
  - `view_recent_changes()` - Show recent updates
  - `search_student()` - Search by name
  - Private display helpers for consistent formatting

- **StudentEditor** - All editing operations
  - `add_student()` - Add single/multiple students
  - `edit_student()` - Edit single/batch with submenu
  - `delete_student()` - Delete single/batch with submenu
  - Private edit/delete helpers

- **CSVExporter** - Export operations
  - `export_to_csv()` - Export all or by province

- **MenuSystem** - Menu navigation
  - `main_menu()` - Main menu
  - `view_menu()` - View submenu
  - `manage_menu()` - Manage submenu
  - `analytics_menu()` - Analytics submenu

#### Removed
- All emoji icons from menus (cleaner professional look)
- Redundant DynamoDB scan operations
- Duplicate count functions (count_by_major, count_by_province)
- Repeated code patterns

#### Improved
- **Code maintainability** - Single responsibility principle
- **Performance** - Centralized scan operation reduces redundancy
- **Extensibility** - Easy to add new features
- **Readability** - Clear class structure and method names
- **DRY principle** - No code duplication
- **Professional appearance** - Removed emoji decorations

#### Technical Details
- Reduced code redundancy by ~30%
- Centralized all DynamoDB table operations
- Consistent error handling across all classes
- Cleaner separation between data, view, and controller logic

---

## [2.7.0] - 2025-10-08

### UX Enhancement: Organized Menu System

#### Changed
- **Complete Menu Restructure** - Simplified from 12 options to 5 main categories
  - Previous: 12 flat menu options (overwhelming)
  - Now: 5 main menu items with organized submenus (clean and intuitive)

- **Main Menu (5 Options):**
  1. View Data (submenu)
  2. Manage Students (submenu)
  3. Analytics & Statistics (submenu)
  4. Generate CSV Export (direct action)
  5. Exit

- **View Data Submenu:**
  - Show all students (with sorting)
  - Show recent changes
  - Search student by name
  - Back to main menu

- **Manage Students Submenu:**
  - Add new student(s)
  - Edit student (single/batch)
  - Remove student (single/batch)
  - Back to main menu

- **Analytics & Statistics Submenu:**
  - Count total students
  - Count by major
  - Count by province
  - Count graduated students
  - Back to main menu

#### Improved
- **Better User Experience** - Categorized functions for easier navigation
- **Cleaner Interface** - Main menu shows only 5 options instead of 12
- **Logical Grouping** - Related functions grouped together
- **Intuitive Navigation** - Easy to find and access features

---

## [2.6.0] - 2025-10-08

### Feature Addition: Recent Changes & Province-based CSV Export

#### Added
- **Show Recent Changes Feature** - View only recently updated students
  - Filter by time range: Last 24 hours, 7 days, 30 days, or custom
  - Displays students sorted by most recent update first
  - Shows IDN, Name, Major, Year, Province, and Update timestamp
  - Perfect for tracking recent data entry or modifications

- **Province-based CSV Export** - Export student data filtered by province
  - Option to export all students OR filter by specific province
  - Interactive province selection with student counts
  - Generates timestamped CSV files with province name in filename
  - Example: `students_export_Papua_20251008_143022.csv`
  - Supports all 6 Papua provinces

#### Changed
- **CSV Export Enhancement** - Now offers two export modes:
  - Export all students (previous default behavior)
  - Export by province (new filtering option)
- **Menu Options** - Increased from 11 to 12 options
  - Option 4: Show recent changes (NEW)
  - Option 5: Generate CSV export (all/by province) - Enhanced
  - Previous options shifted down by 1

#### Improved
- Better date/time parsing for recent changes filter
- Timezone-aware timestamp handling
- Clear visual feedback showing number of students in time range
- Province selection with student counts for better visibility

---

## [2.5.0] - 2025-10-08

### Major Enhancement: Database Manager Improvements

#### Added
- **Batch Edit Feature** - Edit multiple students simultaneously
  - Select multiple students by IDN (comma-separated)
  - Apply same change to all selected students
  - Support for editing: Major, University, Year, Province
  - Confirmation required before applying batch changes

- **Single Edit Enhancement** - Improved single student editing
  - Interactive field selection menu
  - Edit multiple fields in one session
  - Auto-formatting applied based on field type
  - "Done editing" option when finished

- **Continuous Add Feature** - Add multiple students in one session
  - "Add more students?" prompt after each addition
  - No need to return to main menu between additions
  - Default value for University (Western Michigan University)

- **Batch Delete Feature** - Delete multiple students at once
  - Select multiple students by IDN (comma-separated)
  - Preview all students before deletion
  - Safety confirmation required
  - Shows success/failure for each deletion

- **Enhanced Show Data** - Multiple sorting options
  - Sort by last changed (most recent updates first)
  - Sort by first name (alphabetical A-Z)
  - Sort by ID (IDN ascending)
  - Display sort method in table header

#### Changed
- **Menu Restructure** - Reorganized for better workflow
  - Option 1: Add new student(s)
  - Option 2: Edit student (single/batch)
  - Option 3: Show data (with sorting)
  - Option 4: Generate CSV export
  - Option 5: Remove student (single/batch)
  - Options 6-10: Analysis features (search, counts)
  - Option 11: Exit

- **Delete Function** - Now shows submenu for single/batch delete
- **Add Function** - Now supports continuous addition
- **Menu Options** - Increased from 10 to 11 options

#### Improved
- Better user experience with clear prompts
- More detailed student information display before delete
- Enhanced error messages
- Auto-formatting for all edit operations
- Confirmation prompts for destructive operations

---

## [2.4.0] - 2025-10-08

### Frontend Refactoring & Bug Fix

#### Changed
- **Modular Frontend Structure** - Separated frontend code for better organization
  - `docs/index.html` - HTML structure only
  - `docs/script.js` - JavaScript logic (separated from HTML)
  - `docs/style.css` - CSS styles (separated from HTML)
  - Improved maintainability and code organization

#### Fixed
- **Script Loading Issue** - Fixed log output problem after data submission
  - Previous: Script loaded before DOM elements, causing form submission failures
  - Now: Script loads at end of body, ensuring all DOM elements exist
  - Form submission and message display now work correctly

---

## [2.3.0] - 2025-10-08

### Critical Fix: Timezone Correction

#### Fixed
- **Timezone Issue** - Timestamps now correctly use Eastern Time (America/Detroit)
  - Previous: Timestamps were stored in UTC (AWS Lambda default), causing 4-5 hour offset
  - Now: All timestamps use Eastern Time with automatic DST handling
  - Example: 8:00 AM update now shows `2025-10-08T08:00:00-04:00` instead of `2025-10-08T13:00:00`
  - Affects: `created_at` and `updated_at` fields in both main.py and db_manager.py

#### Added
- **Timezone Support** - Added `zoneinfo` module for timezone-aware timestamps
- **tzdata Package** - Added to requirements.txt for Windows compatibility
- **TIMEZONE Configuration** - Centralized timezone setting (`America/Detroit`)

#### Changed
- All `datetime.now()` calls updated to `datetime.now(TIMEZONE)`
- Timestamps now include timezone offset information (ISO 8601 format with timezone)

---

## [2.2.0] - 2025-10-08

### Bug Fixes & Enhancements

#### Fixed
- **Smart Name Matching** - firstName + lastName duplicate detection
  - "Aprilia Mabel" now correctly updates "Aprilia Weni Irjani Mabel"
  - Prevents duplicate entries for same person with different name formats
  - Preserves full legal names in database

#### Added
- **Graduated Students Tracking** - Count and list graduated vs current students
  - Database Manager option #6: Count graduated students
  - Classifies by year field (Freshman/Sophomore/Junior/Senior vs graduation semester)
  - Shows breakdown and detailed list with graduation dates

#### Changed
- `find_student()` now prioritizes firstName + lastName matching over exact match
- `update_or_add_student()` preserves original full name from database
- Database Manager menu updated (1-10 options)

---

## [2.1.0] - 2025-10-08

### DynamoDB Migration

#### Added
- **DynamoDB Integration** - Migrated from SQLite to fully persistent database
- **Auto-formatting** - Names, majors, provinces auto-formatted to Title Case
- **Database Manager CLI** - Interactive tool for data management
- **Migration Scripts** - Automated SQLite to DynamoDB migration

#### Changed
- Database: SQLite in /tmp → DynamoDB (fully persistent)
- 57 students migrated successfully
- Documentation updated to reflect DynamoDB

#### Benefits
- Fully persistent (survives Lambda restarts)
- Serverless and auto-scaling
- Free tier: 25GB storage, 200M requests/month

---

## [2.0.0] - 2025-10-08

### Major Update: Migrated to AWS Lambda

#### Added
- **AWS Lambda Deployment** - Serverless backend using Zappa
- **API Gateway Integration** - RESTful API endpoint
- **Python 3.12 Support** - Upgraded runtime to Python 3.12.3
- **Virtual Environment** - Isolated dependencies with venv
- **AWS CLI Integration** - Automated deployment workflow
- **S3 Bucket** - `zappa-wmu-students-rfldn0-2025` for deployment packages

#### Changed
- **Backend Platform**: Render → AWS Lambda
- **API Endpoint**:
  - Old: `https://wmustudentsupdate.onrender.com`
  - New: `https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production`
- **Python Runtime**: 3.9 → 3.12
- **Architecture**: Traditional server → Serverless
- **Cost**: ~$5-10/month → ~$0.05/year (99% cost reduction)

#### Removed
- Render deployment configuration
- Gunicorn server (replaced by Lambda handler)
- Old Excel migration files (cleanup)

#### Technical Details
- **Region**: us-east-1 (North Virginia)
- **Lambda Runtime**: python3.12
- **Zappa Version**: 0.59.0
- **Deployment Method**: `zappa deploy production`
- **Update Method**: `zappa update production`

#### Benefits
- **99% cost reduction** - Free tier covers all usage
- **Auto-scaling** - Handles 1 to 1000+ concurrent requests
- **No server maintenance** - AWS manages infrastructure
- **High availability** - AWS handles redundancy
- **Cold start**: ~1-2 seconds (first request after inactivity)
- **Warm start**: <100ms (subsequent requests)

---

## [1.0.0] - 2025-01-15

### Initial Release

#### Added
- **Flask REST API** backend
- **SQLite Database** for student data
- **GitHub Pages** frontend deployment
- **Render** backend hosting
- **CORS Support** for cross-origin requests
- **Case-insensitive** duplicate detection
- **Auto-generated IDN** for new students
- **Excel to SQLite** migration script

#### Features
- Student data submission form
- Update existing students
- Add new students
- List all students
- Search student by name
- 56 students migrated from SharePoint Excel

#### Endpoints
- `GET /` - API information
- `POST /submit` - Submit/update student data
- `GET /students` - List all students
- `GET /students/<nama>` - Get student by name

---

## Deployment History

### AWS Lambda Deployment (Current)
- **Deployed**: October 8, 2025
- **Endpoint**: https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production
- **Status**: Active
- **Cost**: ~$0.05/year (within free tier)

### Render Deployment (Deprecated)
- **Deployed**: January 15, 2025
- **Endpoint**: https://wmustudentsupdate.onrender.com
- **Status**: Deprecated (can be shut down)
- **Cost**: ~$7/month

---

## Future Enhancements

### Planned Features
- [ ] Student dashboard with analytics
- [ ] CSV export functionality
- [ ] Email notifications for updates
- [ ] Admin authentication
- [ ] Bulk import/export
- [ ] Student photo uploads (S3 integration)
- [ ] Search and filter improvements
- [ ] API rate limiting
- [ ] CloudWatch monitoring dashboard

### Infrastructure Improvements
- [ ] Custom domain name (e.g., students.wmu.edu)
- [ ] SSL certificate via AWS Certificate Manager
- [ ] DynamoDB migration (if scaling beyond SQLite)
- [ ] Lambda function optimization
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Automated testing suite

---

## Migration Notes

### From Render to AWS Lambda

**Prerequisites Completed:**
1. AWS CLI installed
2. AWS account created
3. IAM user with programmatic access
4. Python 3.12 virtual environment
5. Zappa installed and configured

**Deployment Steps:**
```bash
# 1. Create virtual environment
py -3.12 -m venv env

# 2. Activate environment
.\env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install zappa setuptools

# 4. Configure AWS CLI
aws configure

# 5. Deploy to Lambda
zappa deploy production

# 6. Update frontend
# Edit docs/index.html line 214 with new API URL

# 7. Push to GitHub
git add docs/index.html
git commit -m "Update API endpoint to AWS Lambda"
git push
```

**Future Updates:**
```bash
# For code changes
zappa update production

# View logs
zappa tail production

# Check status
zappa status production

# Undeploy (if needed)
zappa undeploy production
```

---

**Maintained by**: Victor Tabuni (rfldn0)
**Repository**: https://github.com/rfldn0/WMUStudentsUpdate

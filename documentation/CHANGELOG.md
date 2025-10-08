# Changelog

All notable changes to WMU Student Data Update System will be documented in this file.

## [2.0.0] - 2025-10-08

### 🚀 Major Update: Migrated to AWS Lambda

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
- ✅ **99% cost reduction** - Free tier covers all usage
- ✅ **Auto-scaling** - Handles 1 to 1000+ concurrent requests
- ✅ **No server maintenance** - AWS manages infrastructure
- ✅ **High availability** - AWS handles redundancy
- ✅ **Cold start**: ~1-2 seconds (first request after inactivity)
- ✅ **Warm start**: <100ms (subsequent requests)

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
- **Status**: ✅ Active
- **Cost**: ~$0.05/year (within free tier)

### Render Deployment (Deprecated)
- **Deployed**: January 15, 2025
- **Endpoint**: https://wmustudentsupdate.onrender.com
- **Status**: ⚠️ Deprecated (can be shut down)
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
1. ✅ AWS CLI installed
2. ✅ AWS account created
3. ✅ IAM user with programmatic access
4. ✅ Python 3.12 virtual environment
5. ✅ Zappa installed and configured

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

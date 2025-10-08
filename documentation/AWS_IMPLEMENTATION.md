# AWS Lambda Implementation Documentation

## Project Overview

**Project Name**: WMU Student Data Update System
**Deployment Date**: October 8, 2025
**Platform**: AWS Lambda + API Gateway
**Developer**: Victor Tabuni (rfldn0)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER BROWSER                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   GITHUB PAGES                               │
│  https://rfldn0.github.io/WMUStudentsUpdate/                │
│  - Static HTML/CSS/JavaScript                                │
│  - Frontend form interface                                   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS POST/GET
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   AWS API GATEWAY                            │
│  https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com     │
│  - RESTful API endpoints                                     │
│  - CORS configuration                                        │
│  - Request/response transformation                           │
└────────────────────────┬────────────────────────────────────┘
                         │ Triggers
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   AWS LAMBDA FUNCTION                        │
│  Name: wmu-students-update-production                        │
│  Runtime: Python 3.12                                        │
│  Handler: handler.lambda_handler (Zappa wrapper)             │
│  - Flask application (main.py)                               │
│  - Business logic                                            │
│  - Database operations                                       │
└────────────────────────┬────────────────────────────────────┘
                         │ Read/Write
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   SQLITE DATABASE                            │
│  File: students.db (bundled in Lambda package)               │
│  - Student records                                           │
│  - Read-only in production (Lambda filesystem limitation)    │
└─────────────────────────────────────────────────────────────┘
```

---

## AWS Resources Created

### 1. Lambda Function
- **Name**: `wmu-students-update-production`
- **Runtime**: Python 3.12
- **Handler**: `handler.lambda_handler`
- **Memory**: 512 MB (default)
- **Timeout**: 30 seconds
- **Role**: `wmu-students-update-production-ZappaLambdaExecutionRole`

### 2. API Gateway
- **Type**: REST API
- **Name**: `wmu-students-update-production`
- **Stage**: production
- **Endpoint**: https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production
- **CORS**: Enabled

### 3. S3 Bucket
- **Name**: `zappa-wmu-students-rfldn0-2025`
- **Purpose**: Stores Lambda deployment packages
- **Region**: us-east-1
- **Contents**: ZIP files with code + dependencies

### 4. CloudWatch Logs
- **Log Group**: `/aws/lambda/wmu-students-update-production`
- **Retention**: Default (indefinite)
- **Purpose**: Application logs, errors, debugging

### 5. IAM Role
- **Name**: `wmu-students-update-production-ZappaLambdaExecutionRole`
- **Permissions**:
  - Lambda execution
  - CloudWatch Logs write access
  - S3 bucket access
  - API Gateway invocation

---

## Deployment Configuration

### zappa_settings.json
```json
{
    "production": {
        "app_function": "main.app",
        "aws_region": "us-east-1",
        "project_name": "wmu-students-update",
        "runtime": "python3.12",
        "s3_bucket": "zappa-wmu-students-rfldn0-2025",
        "keep_warm": false,
        "exclude": [
            "*.xlsx",
            "temp_excel.xlsx",
            "migrate_to_sqlite.py",
            ".git/*",
            ".gitignore",
            "README.md",
            "__pycache__/*"
        ],
        "include": [
            "students.db"
        ]
    }
}
```

### Key Configuration Details

**`app_function`**: Points to Flask app object in main.py
**`aws_region`**: us-east-1 (N. Virginia) - lowest latency for most users
**`runtime`**: python3.12 - Latest supported Python version on Lambda
**`s3_bucket`**: Unique bucket name for deployment packages
**`keep_warm`**: false - No scheduled pings (saves cost, accepts cold starts)
**`exclude`**: Files not needed in production (reduces package size)
**`include`**: Explicitly bundle students.db database

---

## Application Code

### main.py (Flask Application)

**Key Functions**:
- `get_db_connection()` - SQLite connection handler
- `find_student(nama)` - Case-insensitive student lookup
- `get_next_idn()` - Auto-generate unique student ID
- `update_or_add_student(data)` - Main business logic

**API Endpoints**:
- `GET /` - API information and statistics
- `POST /submit` - Submit or update student data
- `POST /api/submit` - Alias for /submit
- `GET /students` - List all students
- `GET /students/<nama>` - Get specific student

**CORS Configuration**:
```python
from flask_cors import CORS
CORS(app)  # Allows requests from GitHub Pages
```

---

## Database

### Schema
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

### Current Data
- **Total Students**: 56 (migrated from Excel)
- **File Size**: ~20 KB
- **Location**: Bundled in Lambda deployment package

### Limitations
- **Read-only in Lambda**: Lambda filesystem is read-only except /tmp
- **Current workaround**: Database bundled in package (writes update /tmp copy)
- **Future solution**: Migrate to DynamoDB or RDS for production writes

---

## Deployment Process

### Initial Deployment
```bash
# 1. Activate virtual environment
.\env\Scripts\activate

# 2. Deploy to AWS
zappa deploy production

# Output:
# Calling deploy for stage production..
# Creating wmu-students-update-production-ZappaLambdaExecutionRole IAM Role..
# Creating zappa-permissions policy on wmu-students-update-production-ZappaLambdaExecutionRole IAM Role.
# Uploading wmu-students-update-production-1696723456.zip (5.2MiB)..
# 100%|████████████████████████████████████████| 5.45M/5.45M [00:03<00:00, 1.82MiB/s]
# Scheduling..
# Scheduled wmu-students-update-production-zappa-keep-warm-handler.keep_warm_callback with expression rate(4 minutes)!
# Uploading wmu-students-update-production-template-1696723456.json (1.6KiB)..
# 100%|████████████████████████████████████████| 1.59K/1.59K [00:00<00:00, 12.3KiB/s]
# Waiting for stack wmu-students-update-production to create (this can take a bit)..
# 100%|███████████████████████████████████████████████| 4/4 [00:09<00:00,  2.29s/res]
# Deploying API Gateway..
# Deployment complete!
# https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production
```

### Update Deployment
```bash
zappa update production
```

### View Logs
```bash
zappa tail production
```

### Check Status
```bash
zappa status production
```

### Undeploy
```bash
zappa undeploy production
```

---

## Performance Characteristics

### Cold Start
- **First request after inactivity**: 1-2 seconds
- **Causes**: Lambda must initialize Python runtime, load libraries
- **Frequency**: After ~15 minutes of inactivity
- **Mitigation**: `keep_warm: true` (costs extra, not enabled)

### Warm Start
- **Subsequent requests**: <100 ms
- **Duration**: Lambda stays warm for ~15 minutes
- **Performance**: Comparable to traditional servers

### Concurrency
- **Auto-scaling**: Handles 1 to 1000+ concurrent requests
- **No configuration needed**: AWS manages scaling automatically
- **Limit**: AWS account default (usually 1000 concurrent executions)

---

## Cost Analysis

### AWS Lambda Free Tier (Permanent)
- **1 million requests/month** - FREE
- **400,000 GB-seconds compute** - FREE

### Current Usage Estimate
- **Students**: 100
- **Updates/year**: 1,200 (100 students × 12 months)
- **Requests/month**: 100 average
- **Percentage of free tier**: 0.01%

### Cost Breakdown
| Service | Usage | Free Tier | Cost |
|---------|-------|-----------|------|
| Lambda Requests | 1,200/year | 1M/month | $0.00 |
| Lambda Compute | 2.4 GB-sec/year | 400K/month | $0.00 |
| API Gateway | 1,200/year | 1M/month (12mo) | $0.00 |
| S3 Storage | 5 MB | 5 GB | $0.00 |
| **Total** | | | **~$0.05/year** |

### Comparison with Render
| Platform | Cost/Month | Cost/Year | Savings |
|----------|-----------|-----------|---------|
| Render | $7.00 | $84.00 | - |
| AWS Lambda | $0.004 | $0.05 | **99.9%** |

---

## Security

### IAM User
- **Username**: wmu-zappa-deploy
- **Access Type**: Programmatic (API keys)
- **Permissions**: AdministratorAccess (for ease of deployment)
- **Production Recommendation**: Use restricted policy with only:
  - Lambda function management
  - API Gateway management
  - S3 bucket access
  - CloudWatch Logs
  - IAM role creation

### API Security
- **HTTPS only**: Enforced by API Gateway
- **CORS**: Configured to allow GitHub Pages origin
- **SQL Injection**: Protected by parameterized queries
- **Input Validation**: Server-side validation in Flask

### Credentials Storage
- **Location**: `~/.aws/credentials`
- **Never commit**: Excluded from git
- **Rotation**: Recommended every 90 days

---

## Monitoring

### CloudWatch Logs
```bash
# Real-time logs
zappa tail production

# View in AWS Console
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fwmu-students-update-production
```

### Metrics to Monitor
- **Invocations**: Number of requests
- **Duration**: Execution time
- **Errors**: Failed requests
- **Throttles**: Rate limit hits (unlikely at this scale)
- **Cold starts**: Initialization frequency

### Alerts (Optional)
- Set up CloudWatch alarms for:
  - Error rate > 5%
  - Duration > 10 seconds
  - Throttles > 0

---

## Troubleshooting

### Common Issues

**1. Cold Start Too Slow**
- **Solution**: Enable `keep_warm: true` in zappa_settings.json
- **Trade-off**: Small cost increase (~$5/month)

**2. Database Not Updating**
- **Cause**: Lambda filesystem is read-only
- **Solution**: Migrate to DynamoDB or RDS for persistent writes

**3. CORS Errors**
- **Check**: CORS configuration in main.py
- **Verify**: API Gateway CORS settings

**4. Deployment Fails**
- **Check**: Python version (must be 3.12 in venv)
- **Verify**: AWS credentials configured
- **Review**: zappa_settings.json syntax

**5. Logs Not Showing**
- **Command**: `zappa tail production`
- **AWS Console**: Check CloudWatch Logs directly

---

## Future Enhancements

### Phase 1: Database Migration
- Migrate from SQLite to **DynamoDB**
- Benefits:
  - Persistent writes
  - Unlimited scalability
  - No file size limits
  - Better for serverless

### Phase 2: Monitoring
- CloudWatch Dashboard
- Custom metrics
- Error alerting
- Performance tracking

### Phase 3: Custom Domain
- Register domain: `students.wmu.edu`
- SSL certificate via ACM
- Route53 DNS configuration
- Cleaner API URLs

### Phase 4: CI/CD
- GitHub Actions workflow
- Automated testing
- Auto-deploy on push to main
- Rollback on failure

---

## Contact & Support

**Developer**: Victor Tabuni
**GitHub**: @rfldn0
**Email**: [Your email]
**Repository**: https://github.com/rfldn0/WMUStudentsUpdate

---

**Last Updated**: October 8, 2025
**Document Version**: 1.0

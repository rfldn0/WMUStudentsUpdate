# DynamoDB Migration Guide

## Overview

Migrating from SQLite to DynamoDB for persistent, serverless storage.

**Benefits:**
- ✅ Fully persistent (data survives Lambda restarts)
- ✅ Serverless (no server management)
- ✅ Auto-scaling
- ✅ Free tier: 25GB storage, 200M requests/month
- ✅ Perfect for Lambda

---

## Step-by-Step Migration

### **Step 1: Install boto3**

```bash
# Activate virtual environment
.\env\Scripts\activate

# Install boto3
pip install boto3
```

---

### **Step 2: Create DynamoDB Table**

```bash
python create_dynamodb_table.py
```

**What this does:**
- Creates table: `wmu-students`
- Primary key: `idn` (Number)
- Global Secondary Index: `nama-index` (for name lookups)
- Billing: Pay-per-request (on-demand)
- Region: us-east-1

**Expected output:**
```
Creating table 'wmu-students'...
✅ Table 'wmu-students' created successfully!
```

---

### **Step 3: Migrate Data from SQLite**

```bash
python migrate_to_dynamodb.py
```

**What this does:**
- Reads all students from `backend/students.db`
- Uploads to DynamoDB table
- Verifies count matches

**Expected output:**
```
Migrating 57 students to DynamoDB...
✅ Migrated: John Doe (IDN: 1)
✅ Migrated: Jane Smith (IDN: 2)
...
✅ Migration complete!
Successful: 57
Failed: 0
```

---

### **Step 4: Switch to DynamoDB Backend**

Replace the old main.py with DynamoDB version:

```bash
# Backup old version
cp backend/main.py backend/main_sqlite.py

# Replace with DynamoDB version
cp backend/main_dynamodb.py backend/main.py
```

Or manually edit `zappa_settings.json`:

```json
{
    "production": {
        "app_function": "backend.main_dynamodb.app",
        ...
    }
}
```

---

### **Step 5: Update Lambda IAM Role**

Your Lambda function needs DynamoDB permissions.

**Option A: Via AWS Console (Easy)**

1. Go to: https://console.aws.amazon.com/iam/
2. Search for role: `wmu-students-update-production-ZappaLambdaExecutionRole`
3. Click **"Add permissions"** → **"Attach policies"**
4. Search: `AmazonDynamoDBFullAccess`
5. Check it → **"Attach policy"**

**Option B: Via AWS CLI**

```bash
aws iam attach-role-policy \
  --role-name wmu-students-update-production-ZappaLambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
```

---

### **Step 6: Deploy to Lambda**

```bash
# Update Lambda function
zappa update production

# Check logs
zappa tail production
```

---

### **Step 7: Test the Application**

1. Visit: https://rfldn0.github.io/WMUStudentsUpdate/
2. Submit a test student
3. Should see: "Successfully added new record"
4. Check DynamoDB in AWS Console to verify

---

## Verify DynamoDB Table

### Via AWS Console

1. Go to: https://console.aws.amazon.com/dynamodbv2/
2. Click **"Tables"** → **"wmu-students"**
3. Click **"Explore table items"**
4. See all students

### Via AWS CLI

```bash
# Count items
aws dynamodb scan --table-name wmu-students --select COUNT --region us-east-1

# List first 10 students
aws dynamodb scan --table-name wmu-students --max-items 10 --region us-east-1
```

### Via Python Script

```python
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('wmu-students')

response = table.scan(Select='COUNT')
print(f"Total students: {response['Count']}")
```

---

## DynamoDB Table Structure

### Primary Key
- **idn** (Number) - Partition key, unique student ID

### Attributes
- **nama** (String) - Student name
- **jurusan** (String) - Major
- **university** (String) - University name
- **year** (String) - Academic year
- **provinsi** (String) - Province
- **created_at** (String) - ISO timestamp
- **updated_at** (String) - ISO timestamp

### Global Secondary Index
- **nama-index** - For fast name lookups

---

## Cost Analysis

### Free Tier (Permanent)
- **Storage**: 25 GB FREE
- **Read requests**: 25 WCU FREE
- **Write requests**: 25 RCU FREE
- **On-demand**: First 2.5M reads + 1M writes FREE/month

### Expected Usage
- **Students**: 100
- **Data size**: ~50 KB
- **Reads/month**: ~500
- **Writes/month**: ~100
- **Cost**: **$0.00** (well within free tier)

### After Free Tier
- **On-demand reads**: $0.25 per million
- **On-demand writes**: $1.25 per million
- **Storage**: $0.25 per GB/month
- **Estimated cost**: ~$0.10/year

**Compare to SQLite in /tmp:**
- SQLite /tmp: Data lost on Lambda restart
- DynamoDB: Fully persistent, $0/year with free tier

---

## Rollback Plan

If something goes wrong, rollback to SQLite:

```bash
# Restore old main.py
cp backend/main_sqlite.py backend/main.py

# Deploy
zappa update production
```

---

## Troubleshooting

### Error: "Table already exists"
The table was created previously. Check AWS Console or run:
```bash
aws dynamodb describe-table --table-name wmu-students --region us-east-1
```

### Error: "AccessDeniedException"
Lambda doesn't have DynamoDB permissions. Follow Step 5 to add permissions.

### Error: "ResourceNotFoundException"
Table doesn't exist. Run `create_dynamodb_table.py`.

### Data not showing in DynamoDB
Check logs: `zappa tail production`
Verify migration: `python migrate_to_dynamodb.py`

---

## Cleanup (Optional)

After successful migration, you can remove SQLite files:

```bash
# Keep as backup for now
mv backend/students.db backend/students_backup.db

# Update .gitignore to include DynamoDB scripts
```

---

## Next Steps

After migration:
1. ✅ Test form submission thoroughly
2. ✅ Test student updates
3. ✅ Verify data persistence after Lambda cold start
4. ✅ Update documentation
5. ✅ Commit changes to GitHub

---

**Last Updated**: October 8, 2025
**Migration Status**: Ready to deploy

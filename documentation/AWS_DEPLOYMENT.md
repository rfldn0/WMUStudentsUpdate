# AWS Lambda Deployment Guide

## Prerequisites

### 1. Install AWS CLI

**Windows:**
Download and install from: https://aws.amazon.com/cli/

**Verify installation:**
```bash
aws --version
```

### 2. Create AWS Account
1. Go to https://aws.amazon.com
2. Sign up for free account
3. You'll need a credit card (but won't be charged for free tier)

### 3. Create IAM User with Programmatic Access

1. **Log into AWS Console** → https://console.aws.amazon.com
2. **Go to IAM** (Identity and Access Management)
3. **Click "Users"** → **"Add users"**
4. **User details:**
   - Username: `wmu-zappa-deploy`
   - Access type: ✅ Programmatic access
5. **Set permissions:**
   - Click "Attach existing policies directly"
   - Search and select: **AdministratorAccess** (for simplicity)
   - *(In production, use more restrictive policies)*
6. **Review and Create**
7. **Important**: Save the credentials:
   - Access Key ID
   - Secret Access Key
   - ⚠️ You can only see the Secret Key once!

### 4. Configure AWS CLI

```bash
aws configure
```

Enter when prompted:
```
AWS Access Key ID: [paste your access key]
AWS Secret Access Key: [paste your secret key]
Default region name: us-east-1
Default output format: json
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Zappa

```bash
pip install zappa
```

## Deployment Steps

### 1. Initialize Zappa (Already Done)

The `zappa_settings.json` file is already configured.

### 2. Deploy to AWS Lambda

**First deployment:**
```bash
zappa deploy production
```

You'll see output like:
```
Deploying API Gateway...
Deployment complete!
Your endpoint: https://abc123xyz.execute-api.us-east-1.amazonaws.com/production
```

**Copy the endpoint URL** - this is your API URL!

### 3. Update Frontend

Update `docs/index.html` line 219:
```javascript
const API_URL = 'https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/production';
```

Replace with your actual endpoint from step 2.

### 4. Push to GitHub

```bash
git add docs/index.html
git commit -m "Update API endpoint to AWS Lambda"
git push
```

## Future Updates

After making code changes:

```bash
zappa update production
```

This updates your Lambda function without recreating everything.

## Useful Commands

**Check deployment status:**
```bash
zappa status production
```

**View logs:**
```bash
zappa tail production
```

**Undeploy (delete everything):**
```bash
zappa undeploy production
```

**Test locally before deploying:**
```bash
python main.py
```

## Troubleshooting

### Error: "No module named 'zappa'"
```bash
pip install zappa
```

### Error: "Unable to locate credentials"
Run `aws configure` again with your credentials

### Error: "Bucket already exists"
Change `s3_bucket` name in `zappa_settings.json` to something unique:
```json
"s3_bucket": "zappa-wmu-students-YOUR-NAME-HERE"
```

### Database not found
Make sure `students.db` exists in your project directory before deploying

### CORS errors
Already configured in `main.py` with flask-cors

## Cost Estimate

**AWS Lambda Free Tier (every month):**
- 1 million requests FREE
- 400,000 GB-seconds of compute time FREE

**For 100 students × 12 months = 1,200 requests/year:**
- Cost: **$0.00** (well within free tier)

**API Gateway Free Tier (first 12 months):**
- 1 million requests FREE

**After 12 months:**
- API Gateway: $3.50 per million requests
- Your cost: ~$0.004/year (less than half a cent!)

## Architecture

```
User Browser
    ↓
GitHub Pages (docs/index.html)
    ↓
API Gateway (HTTPS)
    ↓
AWS Lambda (main.py)
    ↓
SQLite Database (bundled with Lambda)
```

## Notes

- **Cold starts**: First request after inactivity may take 1-2 seconds
- **Warm requests**: Subsequent requests are fast (<100ms)
- **Database**: SQLite is bundled with the Lambda function
- **Scalability**: Handles up to 1,000 concurrent requests automatically

## Security Best Practices

1. **Use environment variables** for sensitive data
2. **Enable CloudWatch logs** for monitoring
3. **Set up API key** for API Gateway (optional)
4. **Use IAM roles** instead of AdministratorAccess in production

## Support

If you encounter issues:
1. Check logs: `zappa tail production`
2. Review AWS CloudWatch Logs
3. Test locally first: `python main.py`

---

**You're all set! Your app will run on AWS Lambda with nearly zero cost!** 🚀

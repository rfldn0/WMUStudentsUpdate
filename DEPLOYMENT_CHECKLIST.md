# Deployment Checklist - Secure Production Deployment

**IMPORTANT**: Follow this checklist BEFORE deploying to production.

## Pre-Deployment Steps

### 1. Install New Dependencies
```bash
# Activate virtual environment
.\env\Scripts\activate

# Install Flask-Limiter
pip install Flask-Limiter==3.5.0

# Verify installation
pip list | findstr Flask-Limiter
```

### 2. Generate Secure API Key
```bash
# Generate a cryptographically secure random key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Example output: xK3mP9vQw2Zr8LnBfY4TcJh6Xs1NpVg5Ud7RaGe0
# SAVE THIS KEY - You'll need it for steps 3 and 4
```

### 3. Configure AWS Lambda Environment Variables
```bash
# Deploy/update Lambda first
zappa update production

# Then in AWS Console:
# 1. Go to: https://console.aws.amazon.com/lambda
# 2. Select function: wmu-students-update
# 3. Configuration → Environment variables → Edit
# 4. Add these variables:

API_KEY = <paste your key from step 2>
ENVIRONMENT = production
```

### 4. Update Frontend with API Key

**Option A: Manual Update (Quick but less secure)**
```bash
# Edit docs/script.js line 12
# Replace: const API_KEY = 'YOUR_API_KEY_HERE';
# With:    const API_KEY = 'xK3mP9vQw2Zr8LnBfY4TcJh6Xs1NpVg5Ud7RaGe0';

# IMPORTANT: DO NOT COMMIT THIS CHANGE TO GIT
# Keep it local only or use .gitignore
```

**Option B: Build Script (More secure - Recommended)**
```bash
# Create a local file: docs/script.js.production
# Copy docs/script.js and update line 12 with real key
# Use this file for deployment, keep original in Git

# Deploy the production version to GitHub Pages manually
```

### 5. Test Locally First
```bash
# Set environment variable for local testing
set API_KEY=your_generated_key
set ENVIRONMENT=development

# Run Flask app
python backend/main.py

# Test in browser: http://localhost:5000
# Verify rate limiting works
# Verify API key is required for /submit
```

## Deployment

### 6. Deploy Backend to AWS Lambda
```bash
# Make sure you're in project root
cd C:\Users\tabun\OneDrive - Western Michigan University\Desktop\WMUStudentsUpdate

# Activate virtual environment
.\env\Scripts\activate

# Deploy to Lambda
zappa update production

# Monitor deployment
zappa status production
```

### 7. Deploy Frontend to GitHub Pages
```bash
# Only commit non-sensitive files
git add backend/main.py
git add requirements.txt
git add README.md
git add SECURITY_SETUP.md
git add SECURITY_AUDIT_SUMMARY.md
git add DEPLOYMENT_CHECKLIST.md
git add .gitignore

# DO NOT add docs/script.js if it contains real API key
# Commit
git commit -m "Security hardening: Add rate limiting, API auth, input validation"

# Push to GitHub
git push origin main

# GitHub Pages will auto-deploy from /docs folder
```

### 8. Update Frontend API Key (If using Option A)
```bash
# After backend is deployed and working:
# 1. Manually update docs/script.js with real API key
# 2. Commit ONLY this file in a separate commit
# 3. Push to GitHub

git add docs/script.js
git commit -m "Update API key"
git push origin main

# OR better: Use environment variable injection at build time
```

## Post-Deployment Verification

### 9. Test Security Measures

#### Test 1: Rate Limiting
```bash
# Send multiple requests quickly
for /L %i in (1,1,15) do curl https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production/

# Expected: After 10 requests, should get 429 error
```

#### Test 2: API Key Required
```bash
# Try to submit without API key (should fail)
curl -X POST https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production/submit ^
  -H "Content-Type: application/json" ^
  -d "{\"nama\":\"Test Student\"}"

# Expected: 401 Unauthorized
```

#### Test 3: API Key Working
```bash
# Submit with valid API key (should succeed)
curl -X POST https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production/submit ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: your_api_key_here" ^
  -d "{\"nama\":\"Test Student\",\"jurusan\":\"Computer Science\",\"university\":\"WMU\",\"year\":\"Junior\",\"provinsi\":\"Papua\"}"

# Expected: 200 OK with success message
```

#### Test 4: CORS Protection
```bash
# Try from unauthorized origin (should fail)
curl -H "Origin: https://malicious-site.com" ^
  https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production/

# Expected: CORS error or blocked
```

#### Test 5: Input Validation
```bash
# Try with invalid characters (should fail)
curl -X POST https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production/submit ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: your_api_key_here" ^
  -d "{\"nama\":\"<script>alert('xss')</script>\"}"

# Expected: 400 Bad Request with validation error
```

#### Test 6: Security Headers
```bash
# Check response headers
curl -I https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production/

# Expected headers:
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
# X-XSS-Protection: 1; mode=block
# Strict-Transport-Security: max-age=31536000
```

### 10. Monitor Logs
```bash
# View real-time logs
zappa tail production

# Look for:
# - Successful requests (200)
# - Rate limit hits (429)
# - Unauthorized attempts (401)
# - Any errors (500)
```

### 11. Test Frontend Form
1. Go to: https://rfldn0.github.io/WMUStudentsUpdate/
2. Fill out the form with test data
3. Submit
4. Verify success message appears
5. Check DynamoDB to confirm data was saved

## Troubleshooting

### Error: "Module 'flask_limiter' not found"
```bash
# Solution: Install Flask-Limiter
pip install Flask-Limiter==3.5.0
zappa update production
```

### Error: "401 Unauthorized" on submit
```bash
# Solution: Check API key is set correctly
# In Lambda: Configuration → Environment variables
# In Frontend: docs/script.js line 12
```

### Error: "429 Too Many Requests"
```bash
# Solution: This is normal if testing rapidly
# Wait a few minutes and try again
# Or adjust rate limits in backend/main.py
```

### Error: CORS blocked
```bash
# Solution: Verify frontend is served from:
# https://rfldn0.github.io/WMUStudentsUpdate/
# Not localhost or other domains
```

### Error: "Invalid content type"
```bash
# Solution: Ensure Content-Type header is set
# For JSON: Content-Type: application/json
# For forms: Content-Type: multipart/form-data
```

## Security Checklist

After deployment, verify:

- [ ] API key is set in Lambda environment variables
- [ ] API key is NOT committed to Git
- [ ] Frontend has working API key
- [ ] Rate limiting is active (test with 15 quick requests)
- [ ] POST /submit requires API key
- [ ] CORS only allows GitHub Pages domain
- [ ] Security headers present in responses
- [ ] Input validation blocks invalid data
- [ ] Error messages don't leak sensitive info
- [ ] Debug mode is disabled (ENVIRONMENT=production)
- [ ] HTTPS is enforced
- [ ] CloudWatch logs are accessible
- [ ] No CSV files with student data in repo
- [ ] No AWS console links in README
- [ ] .gitignore excludes .env files

## Maintenance Schedule

### Daily
- Monitor CloudWatch logs for errors

### Weekly
- Review rate limit violations (429 errors)
- Check for unauthorized access attempts (401 errors)
- Verify backup/export functionality

### Monthly
- Review and rotate logs
- Update dependencies if security patches available
- Test disaster recovery procedures

### Quarterly (Every 90 days)
- **Rotate API key** (critical security practice)
- Review and update rate limits based on usage
- Audit user access patterns
- Review security configurations

### Annually
- Full security audit
- Penetration testing (if budget allows)
- Review and update security policies
- Disaster recovery drill

## Emergency Procedures

### If API key is compromised:
1. Immediately generate new key
2. Update Lambda environment variable
3. Update frontend
4. Deploy both simultaneously
5. Review logs for suspicious activity
6. Check DynamoDB for unauthorized changes

### If under DDoS attack:
1. Check rate limiting is working
2. If overwhelmed, temporarily disable endpoints:
   ```bash
   # Comment out routes in backend/main.py
   # Deploy: zappa update production
   ```
3. Review CloudWatch metrics
4. Consider adding AWS WAF
5. Contact AWS support if needed

### If data breach suspected:
1. Preserve logs immediately
2. Review all recent changes in DynamoDB
3. Identify affected records
4. Notify affected students (FERPA requirement)
5. Rotate all credentials
6. Conduct forensic analysis
7. Patch vulnerability
8. Document incident

## Support

For deployment issues:
- Check [SECURITY_SETUP.md](SECURITY_SETUP.md)
- Check [SECURITY_AUDIT_SUMMARY.md](SECURITY_AUDIT_SUMMARY.md)
- Review CloudWatch logs: `zappa tail production`

For security concerns:
- Contact: Victor Tabuni
- **DO NOT** post security issues publicly on GitHub

---

**Last Updated**: October 12, 2025
**Next Review**: January 12, 2026 (90 days)

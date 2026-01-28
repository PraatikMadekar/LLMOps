# ECS Deployment Fix Guide

## Issues Fixed

### 1. ✅ Dockerfile - Removed Development Mode
**Problem:** Dockerfile used `--reload` flag which is for development only
**Fix:** Changed to production mode with 2 workers:
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
```

### 2. ✅ Added Health Check
**Problem:** No health check configured, ECS couldn't verify container health
**Fix:** Added health check that calls `/health` endpoint:
```json
"healthCheck": {
  "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
  "interval": 30,
  "timeout": 5,
  "retries": 3,
  "startPeriod": 60
}
```

### 3. ⚠️ AWS Secrets Manager Configuration (ACTION REQUIRED)

**Problem:** Your app expects these environment variables:
- `GROQ_API_KEY`
- `GOOGLE_API_KEY`
- `LLM_PROVIDER`

But your Secrets Manager secret needs to store them properly.

## Required: Update Your AWS Secrets Manager Secret

You have two options:

### Option A: Store as JSON (Recommended)

1. Go to AWS Secrets Manager Console (us-east-2 region)
2. Find secret: `apikeyliveclassTest-q1PGdB`
3. Click "Retrieve secret value" → "Edit"
4. Change to **Plaintext** and paste this JSON structure:

```json
{
  "GROQ_API_KEY": "your-actual-groq-api-key-here",
  "GOOGLE_API_KEY": "your-actual-google-api-key-here"
}
```

5. Save the secret

This matches the task definition I created which references:
```json
"secrets": [
  {
    "name": "GROQ_API_KEY",
    "valueFrom": "arn:aws:secretsmanager:us-east-2:339712993834:secret:apikeyliveclassTest-q1PGdB:GROQ_API_KEY::"
  },
  {
    "name": "GOOGLE_API_KEY",
    "valueFrom": "arn:aws:secretsmanager:us-east-2:339712993834:secret:apikeyliveclassTest-q1PGdB:GOOGLE_API_KEY::"
  }
]
```

### Option B: Create Separate Secrets

Alternatively, create two separate secrets:
1. `groq-api-key-live` → store your Groq API key
2. `google-api-key-live` → store your Google API key

Then update task_definition.json:
```json
"secrets": [
  {
    "name": "GROQ_API_KEY",
    "valueFrom": "arn:aws:secretsmanager:us-east-2:339712993834:secret:groq-api-key-live"
  },
  {
    "name": "GOOGLE_API_KEY",
    "valueFrom": "arn:aws:secretsmanager:us-east-2:339712993834:secret:google-api-key-live"
  }
]
```

## Deployment Steps

1. **Update Secrets Manager** (see above)

2. **Verify IAM Role Permissions**
   
   Make sure `ecsTaskExecutionRole` has permission to read the secret:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "secretsmanager:GetSecretValue"
         ],
         "Resource": "arn:aws:secretsmanager:us-east-2:339712993834:secret:apikeyliveclassTest-q1PGdB*"
       }
     ]
   }
   ```

3. **Commit and Push**
   ```bash
   git add Dockerfile .github/workflows/task_definition.json
   git commit -m "Fix ECS deployment: add health check, fix secrets, remove reload flag"
   git push origin master
   ```

4. **Monitor Deployment**
   - Go to ECS Console → Clusters → llmopslive-cluster → llmops-live-service
   - Watch the "Events" tab for deployment progress
   - Check CloudWatch Logs: `/ecs/llmopstdlive` in us-east-2

## How to Check CloudWatch Logs

If deployment still fails:

1. Go to CloudWatch Console (us-east-2 region)
2. Navigate to: Logs → Log groups → `/ecs/llmopstdlive`
3. Click on the most recent log stream
4. Look for error messages showing why the container is failing

Common errors to look for:
- `ModuleNotFoundError` - missing Python package
- `KeyError` or environment variable errors - secrets not configured
- `Address already in use` - port conflict
- Connection errors - health check failing

## Testing Locally

Before deploying, test the Docker image locally:

```bash
# Build the image
docker build -t llmops-test .

# Run with environment variables
docker run -p 8080:8080 \
  -e GROQ_API_KEY="your-key" \
  -e GOOGLE_API_KEY="your-key" \
  -e LLM_PROVIDER="groq" \
  llmops-test

# Test health endpoint
curl http://localhost:8080/health
```

## Troubleshooting

### If deployment still times out:

1. **Check ECS Service Events**
   - Look for "service llmops-live-service was unable to place a task"
   - Check if there are resource constraints

2. **Check Task Stopped Reason**
   - Go to ECS → Clusters → Tasks (show stopped tasks)
   - Click on stopped task to see the reason

3. **Increase Health Check Grace Period**
   - If app takes longer to start, increase `startPeriod` to 120 seconds

4. **Reduce Workers**
   - Change Dockerfile workers from 2 to 1 if memory is tight

### Common Fixes:

**Out of Memory:**
- Increase memory in task_definition.json to "10240" (10GB)

**Slow Startup:**
- Increase health check `startPeriod` to 120 or 180 seconds

**Port Issues:**
- Verify your app listens on 0.0.0.0:8080, not localhost

## Next Steps After This Fix

1. Update your Secrets Manager secret with the correct JSON structure
2. Verify IAM permissions
3. Commit and push the changes
4. Monitor the deployment in ECS Console
5. Check CloudWatch logs if it fails again

The most critical step is #1 - updating Secrets Manager!

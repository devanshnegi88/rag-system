# Deployment Guide for Render

This guide explains how to deploy the RAG system to Render.com for free or with paid plans.

## Prerequisites

- GitHub account with the repository pushed
- Render account (free tier available)
- CSV file with conversation data

## Step-by-Step Deployment

### 1. Prepare Your Repository

Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit: RAG system"
git branch -M main
git remote add origin https://github.com/yourusername/rag-system.git
git push -u origin main
```

### 2. Create Render.yaml (Optional but Recommended)

Create a `render.yaml` file in the root directory:

```yaml
services:
  - type: web
    name: rag-system
    env: python
    region: oregon
    plan: free
    
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
    
    startCommand: |
      gunicorn -w 1 -b 0.0.0.0:$PORT \
        "chatbot.api:ChatbotAPI(RAGIndexer(), PersonaExtractor()).get_app()"
    
    envVars:
      - key: PYTHON_VERSION
        value: "3.9"
      - key: PORT
        value: "5000"
    
    autoDeploy: true
```

### 3. Connect to Render

1. Go to https://render.com
2. Sign up or log in
3. Click "New" → "Web Service"
4. Connect your GitHub account
5. Select your repository
6. Configure:
   - **Name**: rag-system
   - **Environment**: Python 3
   - **Region**: Leave default
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py --csv data/conversations.csv --host 0.0.0.0 --port $PORT`

### 4. Handle Data Files

**Option A: Upload CSV to Render (Simple)**
1. In Render dashboard, go to Files
2. Upload your CSV file
3. Reference it in start command: `/etc/render/data/conversations.csv`

**Option B: Use Environment Variables**
1. Store CSV content in Render environment variables (for small files)
2. Or, use an external data service (S3, GitHub raw files, etc.)

**Option C: Git LFS (Recommended for Large Files)**
1. Install Git LFS: `git lfs install`
2. Track CSV: `git lfs track "*.csv"`
3. Commit and push
4. Render will automatically handle LFS files

### 5. Set Environment Variables in Render

Go to Dashboard → Select your service → Environment:

```
PYTHON_VERSION=3.9
PORT=5000
```

### 6. Configure Disk Space (If Needed)

The free tier includes 0.5 GB ephemeral disk. For larger models:
- Upgrade to paid plan
- Or, use model caching strategies

### 7. Deploy

Click "Deploy" or enable autoDeploy.

Render will:
1. Clone your repository
2. Install dependencies
3. Start the Flask app
4. Assign a public URL

## Accessing Your Service

After deployment, Render provides a URL:
```
https://rag-system.onrender.com
```

Test it:
```bash
curl https://rag-system.onrender.com/health
```

## Production Considerations

### 1. Use WSGI Server (Gunicorn)

Flask development server isn't production-ready. Use Gunicorn:

```bash
pip install gunicorn
```

Update start command:
```bash
gunicorn -w 1 -b 0.0.0.0:$PORT -t 0 "main:app"
```

Note: `-w 1` because Render free tier has limited resources.

### 2. Add Error Handling

Create an app wrapper `app.py`:
```python
import logging
from main import main
from chatbot.api import ChatbotAPI
from rag.indexing import RAGIndexer
from persona.extractor import PersonaExtractor

# Setup on startup
indexer = RAGIndexer()
persona_extractor = PersonaExtractor()
chatbot = ChatbotAPI(indexer, persona_extractor)

app = chatbot.get_app()

if __name__ == '__main__':
    app.run()
```

### 3. Model Caching

To speed up deployments, cache downloaded models:

```python
import os
os.environ['TRANSFORMERS_CACHE'] = '/app/models_cache'
os.environ['SENTENCE_TRANSFORMERS_HOME'] = '/app/sentence_transformers'
```

### 4. Memory Optimization

For free tier (512 MB RAM):
- Reduce batch sizes
- Use smaller models: `all-MiniLM-L6-v2` (recommended, already in use)
- Disable GPU: Done by default with `torch` CPU

### 5. Timeout Configuration

Set longer timeout for initial model loading:

```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Request timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(300)  # 5 minute timeout
```

## Monitoring and Logs

1. **View logs in Render dashboard**: Logs tab
2. **Set up alerts**: Render provides email notifications
3. **Monitor performance**: Resource usage shown in dashboard

## Scaling

As traffic increases:
1. Upgrade from free to paid plan
2. Add more worker processes: `gunicorn -w 4`
3. Enable Redis caching for results
4. Use a database instead of JSON files

## Cost Estimation (as of 2024)

| Plan | Price | Resources | Best For |
|------|-------|-----------|----------|
| Free | $0 | 0.5 GB RAM, 0.5 GB disk, 750 hrs/month | Testing, demo |
| Starter | $7/month | 1 GB RAM, 10 GB disk | Small production |
| Standard | $12/month | 2 GB RAM, 20 GB disk | Medium usage |

## Troubleshooting

### 1. Build fails: "ModuleNotFoundError"
- Check requirements.txt
- Ensure all imports are included
- Run `pip freeze > requirements.txt` locally first

### 2. Service keeps restarting
- Check logs for errors
- Increase timeout: `gunicorn --timeout 120`
- Reduce memory usage

### 3. CSV file not found
- Verify CSV path in start command
- Use absolute paths: `/etc/render/data/file.csv`
- Test locally first

### 4. Slow responses
- First request takes time (models loading)
- Add caching for repeated queries
- Upgrade plan for more resources

## Example: Complete Deployment

```bash
# 1. Prepare repo
git init
git add -A
git commit -m "RAG system ready for deployment"

# 2. Test locally
python main.py --csv example_data.csv --port 5000

# 3. Push to GitHub
git remote add origin https://github.com/yourusername/rag-system.git
git push -u origin main

# 4. Go to Render.com, create web service
# - Select repository
# - Build: pip install -r requirements.txt
# - Start: python main.py --csv data/conversations.csv --host 0.0.0.0 --port $PORT
# - Add environment variable: PORT=5000
# - Deploy

# 5. Test deployed service
curl https://your-service.onrender.com/health
```

## Next Steps

1. Add authentication (API keys)
2. Set up database for persistent storage
3. Implement request rate limiting
4. Add CORS for frontend
5. Create admin dashboard

## Support

For Render-specific issues:
- Render docs: docs.render.com
- Support: support@render.com

For application issues:
- Check README.md
- Review logs in Render dashboard
- Test locally first

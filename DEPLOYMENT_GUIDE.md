# 🚀 Free Deployment Guide

## Free Hosting Options for Your RAG API

### ⭐ Best Free Options

| Platform | Free Tier | Best For | Limitations |
|----------|-----------|----------|-------------|
| **Render** | 750 hrs/month | Easy deployment | Sleeps after 15 min inactivity |
| **Railway** | $5 credit/month | Docker support | Limited credits |
| **Fly.io** | 3 VMs free | Global deployment | 256MB RAM per VM |
| **Hugging Face Spaces** | Unlimited | ML apps | Public by default |
| **Google Cloud Run** | 2M requests/month | Scalable | Requires credit card |
| **Replit** | Free tier | Quick start | Public code |

## 🏆 Recommended: Render (Easiest!)

### Why Render?
- ✅ Completely free (750 hours/month)
- ✅ Easy deployment from GitHub
- ✅ Automatic HTTPS
- ✅ No credit card required
- ✅ Good for APIs
- ⚠️ Sleeps after 15 min (wakes on request)

### Step-by-Step Deployment on Render

#### 1. Prepare Your Code

Create `render.yaml`:
```yaml
services:
  - type: web
    name: docling-rag-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GROQ_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

Create `Procfile`:
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

#### 2. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/docling-rag.git
git push -u origin main
```

#### 3. Deploy on Render
1. Go to https://render.com/
2. Sign up (free, no credit card)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: docling-rag-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
6. Add environment variable:
   - **Key**: `GROQ_API_KEY`
   - **Value**: Your Groq API key
7. Click "Create Web Service"

#### 4. Access Your API
Your API will be available at:
```
https://docling-rag-api.onrender.com
```

**Note**: First request after sleep takes ~30 seconds to wake up.

## 🚂 Option 2: Railway

### Why Railway?
- ✅ $5 free credit/month
- ✅ Easy deployment
- ✅ No sleep mode
- ✅ Good performance
- ⚠️ Requires credit card (not charged)

### Deploy on Railway

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

#### 2. Login and Deploy
```bash
railway login
railway init
railway up
```

#### 3. Add Environment Variables
```bash
railway variables set GROQ_API_KEY=your_key_here
```

#### 4. Access Your API
```bash
railway domain
# Your API URL will be shown
```

## ✈️ Option 3: Fly.io

### Why Fly.io?
- ✅ 3 free VMs
- ✅ Global deployment
- ✅ No sleep mode
- ✅ Good for APIs
- ⚠️ Limited RAM (256MB)

### Deploy on Fly.io

#### 1. Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

#### 2. Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### 3. Create fly.toml
```toml
app = "docling-rag-api"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

#### 4. Deploy
```bash
fly auth login
fly launch
fly secrets set GROQ_API_KEY=your_key_here
fly deploy
```

## 🤗 Option 4: Hugging Face Spaces

### Why Hugging Face?
- ✅ Unlimited free tier
- ✅ Perfect for ML apps
- ✅ Easy deployment
- ✅ Good community
- ⚠️ Public by default

### Deploy on Hugging Face Spaces

#### 1. Create Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose "Gradio" or "Docker"
4. Name: docling-rag-api

#### 2. Create app.py (for Gradio)
```python
import gradio as gr
from main import DoclingRAGSystem

rag = DoclingRAGSystem()

def query_rag(question):
    result = rag.query(question, verbose=False)
    return result["answer"]

def upload_file(file):
    rag.ingest_documents([file.name])
    return "File uploaded successfully!"

with gr.Blocks() as demo:
    gr.Markdown("# Docling RAG System")
    
    with gr.Tab("Upload"):
        file_input = gr.File(label="Upload Document")
        upload_btn = gr.Button("Upload")
        upload_output = gr.Textbox(label="Status")
        upload_btn.click(upload_file, inputs=file_input, outputs=upload_output)
    
    with gr.Tab("Query"):
        question_input = gr.Textbox(label="Ask a question")
        query_btn = gr.Button("Ask")
        answer_output = gr.Textbox(label="Answer")
        query_btn.click(query_rag, inputs=question_input, outputs=answer_output)

demo.launch()
```

#### 3. Push to Space
```bash
git clone https://huggingface.co/spaces/yourusername/docling-rag-api
cd docling-rag-api
# Copy your files
git add .
git commit -m "Initial commit"
git push
```

## 🌐 Option 5: Google Cloud Run

### Why Google Cloud Run?
- ✅ 2M requests/month free
- ✅ Scales to zero
- ✅ Fast cold starts
- ✅ Production-ready
- ⚠️ Requires credit card (not charged in free tier)

### Deploy on Cloud Run

#### 1. Install Google Cloud SDK
Download from: https://cloud.google.com/sdk/docs/install

#### 2. Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

CMD exec uvicorn api:app --host 0.0.0.0 --port $PORT
```

#### 3. Deploy
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy docling-rag-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=your_key_here
```

## 🎯 Comparison & Recommendation

### For Beginners: Render
- Easiest to set up
- No credit card needed
- Good free tier
- Perfect for testing

### For Production: Railway or Fly.io
- Better performance
- No sleep mode
- More reliable
- Worth the small cost

### For ML Community: Hugging Face
- Unlimited free
- Great for sharing
- ML-focused community
- Public by default

### For Scale: Google Cloud Run
- Best scalability
- Pay per use
- Production-ready
- Requires credit card

## 📝 Deployment Checklist

### Before Deployment
- [ ] Test locally: `python api.py`
- [ ] Create `.env` file with GROQ_API_KEY
- [ ] Test all endpoints
- [ ] Check requirements.txt is complete
- [ ] Add .gitignore (don't commit .env!)

### For Deployment
- [ ] Choose hosting platform
- [ ] Create account
- [ ] Push code to GitHub (if needed)
- [ ] Configure environment variables
- [ ] Deploy application
- [ ] Test deployed API
- [ ] Share API URL!

## 🔒 Security Tips

### Environment Variables
```bash
# Never commit these!
GROQ_API_KEY=your_key_here
```

### .gitignore
```
.env
*.env
__pycache__/
vector_db/
docs/
*.pyc
```

### API Security (Optional)
Add authentication to your API:
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/query", dependencies=[Depends(security)])
async def query_documents(request: QueryRequest):
    # Protected endpoint
    pass
```

## 🚀 Quick Deploy Commands

### Render
```bash
# Just push to GitHub and connect on Render.com
git push origin main
```

### Railway
```bash
railway login
railway init
railway up
railway variables set GROQ_API_KEY=your_key
```

### Fly.io
```bash
fly auth login
fly launch
fly secrets set GROQ_API_KEY=your_key
fly deploy
```

### Hugging Face
```bash
git clone https://huggingface.co/spaces/user/space
# Copy files
git push
```

## 📊 Cost Comparison

| Platform | Free Tier | After Free | Best For |
|----------|-----------|------------|----------|
| Render | 750 hrs/month | $7/month | Testing |
| Railway | $5 credit | $0.000463/GB-s | Development |
| Fly.io | 3 VMs | $1.94/VM/month | Production |
| HF Spaces | Unlimited | Paid tiers available | Sharing |
| Cloud Run | 2M requests | Pay per use | Scale |

## 🎉 Recommended Setup

### For You (Free & Easy)
1. **Start with Render**
   - Free, no credit card
   - Easy deployment
   - Good for testing

2. **If you need better performance**
   - Upgrade to Railway ($5/month)
   - Or use Fly.io (3 free VMs)

3. **For sharing with community**
   - Use Hugging Face Spaces
   - Unlimited free tier
   - Great for demos

## 📞 Support

### Render
- Docs: https://render.com/docs
- Community: https://community.render.com/

### Railway
- Docs: https://docs.railway.app/
- Discord: https://discord.gg/railway

### Fly.io
- Docs: https://fly.io/docs/
- Community: https://community.fly.io/

### Hugging Face
- Docs: https://huggingface.co/docs/hub/spaces
- Forum: https://discuss.huggingface.co/

## ✅ Summary

**Best Free Options:**
1. **Render** - Easiest, no credit card
2. **Hugging Face** - Unlimited, for ML apps
3. **Fly.io** - No sleep, good performance

**Recommended Path:**
1. Deploy on Render (free, easy)
2. Test your API
3. Share with others
4. Upgrade if needed

**Start now:**
```bash
# Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push

# Deploy on Render.com
# Connect GitHub repo
# Add GROQ_API_KEY
# Deploy!
```

**Your API will be live at:**
```
https://your-app-name.onrender.com
```

**Free, easy, and ready to use! 🚀**

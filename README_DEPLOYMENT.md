# 🌐 Deploy Your RAG API for Free!

## 🎯 Quick Answer

**Best Free Option: Render.com**
- ✅ Completely free (no credit card)
- ✅ Easy 5-minute deployment
- ✅ Automatic HTTPS
- ✅ 750 hours/month free

## 🚀 Deploy in 5 Minutes

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Deploy RAG API"
git remote add origin https://github.com/YOUR_USERNAME/docling-rag.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to **https://render.com/**
2. **Sign up** (free, no credit card!)
3. Click **"New +"** → **"Web Service"**
4. **Connect** your GitHub repository
5. Render auto-detects settings
6. Add environment variable:
   - **Key**: `GROQ_API_KEY`
   - **Value**: Your Groq API key
7. Click **"Create Web Service"**

### Step 3: Done! 🎉
Your API is live at:
```
https://your-app-name.onrender.com
```

## 🌟 Free Hosting Options

| Platform | Free Tier | Sleep Mode | Credit Card | Best For |
|----------|-----------|------------|-------------|----------|
| **Render** | 750 hrs/month | Yes (15 min) | No | Easiest |
| **Railway** | $5 credit | No | Yes | Better performance |
| **Fly.io** | 3 VMs | No | No | Production |
| **HF Spaces** | Unlimited | No | No | ML apps |

## 📚 Documentation

- **[DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md)** - 5-minute guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete guide with all options

## 🔧 Files Included

All deployment files are ready:
- ✅ `render.yaml` - Render configuration
- ✅ `Dockerfile` - Docker configuration
- ✅ `Procfile` - Process configuration
- ✅ `runtime.txt` - Python version
- ✅ `.dockerignore` - Docker ignore
- ✅ `.gitignore` - Git ignore (updated)

## 🎯 Recommended Path

### For Beginners
1. **Deploy on Render** (free, easy)
2. Test your API
3. Share with others

### For Better Performance
1. Start with Render
2. If you need no-sleep mode:
   - Upgrade to Railway ($5/month)
   - Or use Fly.io (3 free VMs)

### For ML Community
- Deploy on Hugging Face Spaces
- Unlimited free tier
- Great for sharing demos

## 🧪 Test Your Deployed API

### Web Interface
```
https://your-app-name.onrender.com
```

### API Documentation
```
https://your-app-name.onrender.com/docs
```

### Python Code
```python
import requests

BASE_URL = "https://your-app-name.onrender.com"

# Upload document
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    print(response.json())

# Ask question
data = {'question': 'What is this about?'}
response = requests.post(f"{BASE_URL}/query", json=data)
print(response.json()['answer'])
```

## ⚠️ Important Notes

### Render Free Tier
- Sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month (enough for most use)
- Automatic HTTPS included

### Keep It Awake (Optional)
Use UptimeRobot to ping every 14 minutes:
1. Go to https://uptimerobot.com/
2. Add monitor
3. URL: `https://your-app-name.onrender.com/health`
4. Interval: 14 minutes

## 🔒 Security

### Before Deploying
1. **Never commit `.env` file**
   - Already in `.gitignore`
   - Add secrets on hosting platform

2. **Set environment variables on platform**
   - `GROQ_API_KEY` - Your Groq API key
   - Other settings as needed

3. **Review `.gitignore`**
   - Excludes sensitive files
   - Excludes user documents
   - Includes deployment files

## 🎉 Summary

**You can deploy for FREE on:**
1. **Render.com** - Easiest, no credit card
2. **Fly.io** - 3 free VMs, no sleep
3. **Hugging Face** - Unlimited, for ML apps

**Deployment files included:**
- All configuration files ready
- Just push to GitHub
- Connect on hosting platform
- Add GROQ_API_KEY
- Deploy!

**Your API will be live at:**
```
https://your-app-name.onrender.com
```

**Start now:**
```bash
git push origin main
# Then deploy on Render.com
```

**Free, easy, and ready to share! 🚀**

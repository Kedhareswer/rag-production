# 🚀 Deploy in 5 Minutes (Free!)

## Easiest Way: Render.com

### Step 1: Push to GitHub (2 minutes)
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/docling-rag.git
git push -u origin main
```

### Step 2: Deploy on Render (3 minutes)
1. Go to https://render.com/
2. Sign up (free, no credit card!)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render auto-detects settings from `render.yaml`
6. Add environment variable:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
7. Click "Create Web Service"

### Step 3: Done! 🎉
Your API is live at:
```
https://your-app-name.onrender.com
```

## Test Your Deployed API

### Using Browser
```
https://your-app-name.onrender.com/docs
```

### Using Python
```python
import requests

BASE_URL = "https://your-app-name.onrender.com"

# Upload
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    print(response.json())

# Query
data = {'question': 'What is this about?'}
response = requests.post(f"{BASE_URL}/query", json=data)
print(response.json()['answer'])
```

### Using cURL
```bash
# Upload
curl -X POST "https://your-app-name.onrender.com/upload" \
  -F "file=@document.pdf"

# Query
curl -X POST "https://your-app-name.onrender.com/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?"}'
```

## Important Notes

### Free Tier Limitations
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ First request after sleep takes ~30 seconds
- ✅ 750 hours/month free (enough for most use)
- ✅ Automatic HTTPS
- ✅ No credit card required

### Keep It Awake (Optional)
Use a service like UptimeRobot to ping your API every 14 minutes:
1. Go to https://uptimerobot.com/
2. Add monitor
3. URL: `https://your-app-name.onrender.com/health`
4. Interval: 14 minutes

## Alternative: Railway (No Sleep!)

### If you want no sleep mode:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
railway variables set GROQ_API_KEY=your_key_here

# Get URL
railway domain
```

**Cost**: $5 credit/month (free to start)

## Files Included for Deployment

✅ `render.yaml` - Render configuration
✅ `Procfile` - Process configuration
✅ `Dockerfile` - Docker configuration
✅ `runtime.txt` - Python version
✅ `.dockerignore` - Docker ignore rules
✅ `.gitignore` - Git ignore rules (updated)

## Troubleshooting

### Build fails?
- Check `requirements.txt` is complete
- Verify Python version in `runtime.txt`

### API not responding?
- Wait 30 seconds (cold start)
- Check logs on Render dashboard
- Verify GROQ_API_KEY is set

### Out of memory?
- Reduce chunk size in `.env`
- Use smaller embedding model
- Upgrade to paid tier

## Summary

**Fastest deployment:**
1. Push to GitHub
2. Connect on Render.com
3. Add GROQ_API_KEY
4. Deploy!

**Your API is now live and free! 🎉**

For more options, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

# 🚀 Deploy Backend to Render (Step-by-Step Guide)

## Prerequisites
- GitHub account with your repo pushed
- Groq API Key (from https://console.groq.com/keys)
- Render account (free tier at https://render.com)

---

## Step 1: Push Your Code to GitHub

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

---

## Step 2: Create a Render Account & Login

1. Go to **https://render.com**
2. Click **Sign Up** (or login if you already have account)
3. Choose **GitHub** as signup method
4. Authorize Render to access your GitHub repos

---

## Step 3: Create a New Web Service

1. On Render dashboard, click **New +** → **Web Service**
2. Select your **Enterprise RAG** repository
3. Fill in the configuration:

| Field | Value |
|-------|-------|
| **Name** | `enterprise-rag-backend` |
| **Environment** | `Python 3` |
| **Region** | Select closest to you (e.g., `Oregon`, `Frankfurt`) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python flask_api.py` |
| **Plan** | `Free` (or Paid for better uptime) |

---

## Step 4: Add Environment Variables

1. Scroll down to **Environment** section
2. Click **Add Environment Variable**
3. Add these variables:

| Key | Value |
|-----|-------|
| `GROQ_API_KEY` | *Your API key from https://console.groq.com/keys* |
| `ENVIRONMENT` | `production` |
| `PYTHON_VERSION` | `3.9.18` |

---

## Step 5: Deploy

1. Click **Create Web Service**
2. Wait for deployment (usually 3-5 minutes)
3. Once deployed, you'll see a live URL like:
   ```
   https://enterprise-rag-backend.onrender.com
   ```

---

## Step 6: Test Your Backend

Copy your Render URL and test it:

```bash
# Test health endpoint
curl https://your-backend-name.onrender.com/api/health

# Should return:
# {
#   "status": "ok",
#   "message": "Enterprise RAG System is running",
#   "timestamp": "2026-05-28T...",
#   "system_ready": true
# }
```

---

## Step 7: Update Frontend HTML

Update the frontend with your backend URL:

1. Open `ui_standalone.html`
2. Find this line (around line 988):
   ```javascript
   const API_URL_PRODUCTION = 'https://enterprise-rag-api.onrender.com/api';
   ```
3. Replace with your actual Render URL:
   ```javascript
   const API_URL_PRODUCTION = 'https://your-backend-name.onrender.com/api';
   ```
4. Redeploy frontend to Vercel

---

## Step 8: Test on Phone

1. Update your Vercel frontend
2. Go to your Vercel app URL on your phone
3. The app should now connect to your backend! ✅

---

## Troubleshooting

### "Network error: Load failed" still appears
- ✅ Check your Render URL is correct
- ✅ Verify GROQ_API_KEY is set in Render environment
- ✅ Check that Flask app shows "✅ RAG System initialized successfully"
- ✅ Wait 2-3 minutes after deployment for cold start

### Backend build fails
- ✅ Check `requirements.txt` exists
- ✅ Verify all imports are in requirements.txt
- ✅ Check Render logs for specific errors

### Deployment takes too long
- Free tier Render services spin down after 15 minutes of inactivity
- Consider upgrading to **Paid tier** for always-on service

---

## Important Notes

⚠️ **First deployment may take 5-10 minutes** - Render installs all dependencies

⚠️ **Free tier limitations:**
- Services spin down after 15 minutes of inactivity
- Limited to 750 hours/month
- Recommended to upgrade to paid tier for production

✅ **Keep your Groq API Key safe!** - Don't commit it to GitHub

---

## Need Help?

- Render Docs: https://render.com/docs
- Groq API: https://console.groq.com
- Check Render logs in dashboard for errors

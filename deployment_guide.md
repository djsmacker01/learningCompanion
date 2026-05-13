# Learning Companion - Deployment Guide

## 🚀 Multiple Deployment Options

### Option 1: Railway (Recommended)
**Best for Python Flask apps with databases**

1. **Go to [railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select your `learningCompanion` repository**
5. **Railway will auto-detect Python and install dependencies**
6. **Add environment variables:**
   ```
   SECRET_KEY=your-secret-key
   SUPABASE_URL=https://rrhudaxhqhpiaezrfvnl.supabase.co
   SUPABASE_KEY=your-supabase-key
   OPENAI_API_KEY=your-openai-key
   FLASK_ENV=production
   ```
7. **Deploy!** (Usually takes 2-3 minutes)

### Option 2: Render
**Good alternative with free tier**

1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New" → "Web Service"**
4. **Connect your GitHub repository**
5. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
6. **Add environment variables** (same as Railway)
7. **Deploy!**

### Option 3: Heroku
**Classic platform, requires credit card for free tier**

1. **Install Heroku CLI**
2. **Login:** `heroku login`
3. **Create app:** `heroku create learning-companion-app`
4. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set SUPABASE_URL=https://rrhudaxhqhpiaezrfvnl.supabase.co
   heroku config:set SUPABASE_KEY=your-supabase-key
   heroku config:set OPENAI_API_KEY=your-openai-key
   heroku config:set FLASK_ENV=production
   ```
5. **Deploy:** `git push heroku main`

### Option 4: DigitalOcean App Platform
**Good for production apps**

1. **Go to [cloud.digitalocean.com](https://cloud.digitalocean.com)**
2. **Create App Platform project**
3. **Connect GitHub repository**
4. **Configure build and run commands**
5. **Add environment variables**
6. **Deploy!**

## 🔧 Pre-Deployment Checklist

### 1. Environment Variables
Make sure you have these ready:
- `SECRET_KEY` - Flask secret key
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase service role key
- `OPENAI_API_KEY` - Your OpenAI API key
- `FLASK_ENV=production`

### 2. Database Setup
1. **Run your SQL migrations** on Supabase
2. **Test database connection**
3. **Verify all tables exist**

### 3. Test Locally
```bash
# Test with production settings
export FLASK_ENV=production
python run.py
```

## 📋 Post-Deployment Steps

1. **Test your live URL**
2. **Check all features work:**
   - User registration/login
   - Topic creation
   - Quiz functionality
   - AI features
   - Analytics dashboard
3. **Monitor logs** for any errors
4. **Set up custom domain** (optional)

## 🎯 Recommended: Railway

**Why Railway is best for your app:**
- ✅ **Excellent Python support**
- ✅ **Automatic dependency detection**
- ✅ **Built-in database support**
- ✅ **Free tier available**
- ✅ **Easy environment variable management**
- ✅ **Automatic deployments on git push**

## 🚀 Quick Start with Railway

1. **Commit and push your code:**
   ```bash
   git add .
   git commit -m "Add deployment configurations"
   git push origin main
   ```

2. **Go to [railway.app](https://railway.app)**

3. **Connect your GitHub repository**

4. **Add environment variables**

5. **Deploy!**

Your app will be live at: `https://your-app-name.railway.app`

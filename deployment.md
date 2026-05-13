# Learning Companion - Vercel Deployment Guide

## 🚀 Deploying to Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier available)
- Your application code in a GitHub repository

### Step 1: Prepare Your Repository
1. Make sure all your code is committed to GitHub
2. Ensure your repository is private (for security)

### Step 2: Set Up Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with your GitHub account
3. Click "New Project"
4. Import your `learningCompanion` repository

### Step 3: Configure Environment Variables
In Vercel dashboard, go to your project settings and add these environment variables:

```
SECRET_KEY=your-secret-key-here
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
OPENAI_API_KEY=your-openai-api-key
FLASK_ENV=production
```

### Step 4: Deploy
1. Click "Deploy" in Vercel
2. Wait for deployment to complete
3. Your app will be available at `https://your-project-name.vercel.app`

### Step 5: Configure Database
1. Run your SQL migrations on your Supabase database
2. Ensure all tables are created
3. Test the connection

### Step 6: Test Your Deployment
1. Visit your Vercel URL
2. Test user registration/login
3. Test core functionality
4. Check analytics and AI features

## 🔧 Troubleshooting

### Common Issues:
- **Environment variables not set**: Check Vercel project settings
- **Database connection issues**: Verify Supabase credentials
- **Static files not loading**: Check file paths in templates
- **Session issues**: Ensure SECRET_KEY is set

### Support:
- Check Vercel logs in dashboard
- Verify environment variables
- Test locally with production settings

## 📝 Notes
- Vercel provides free hosting for personal projects
- Automatic deployments on git push
- Built-in SSL certificates
- Global CDN for fast loading

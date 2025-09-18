# Supabase Setup Instructions

## Quick Start Guide

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - **Name**: `learning-companion`
   - **Database Password**: Generate a strong password
   - **Region**: Choose closest to your users
5. Click "Create new project"
6. Wait for project initialization (2-3 minutes)

### 2. Get Project Credentials
1. Go to **Settings** → **API**
2. Copy the following values:
   - **Project URL**: `https://your-project.supabase.co`
   - **anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - **service_role secret key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### 3. Run Database Migrations
1. Go to **SQL Editor** in your Supabase dashboard
2. Create a new query
3. Copy and paste each migration file in order:
   ```
   001_create_users_table.sql
   002_create_topics_table.sql
   003_create_study_sessions_table.sql
   004_create_user_analytics_table.sql
   005_additional_indexes_and_optimizations.sql
   006_sample_data.sql
   ```
4. Run each query by clicking "Run"

### 4. Configure Authentication
1. Go to **Authentication** → **Settings**
2. Enable **Email** provider
3. Configure **Site URL**: `http://localhost:5000` (for development)
4. Set **Redirect URLs**: `http://localhost:5000/**`
5. Customize email templates if desired

### 5. Set Up Environment Variables
Create a `.env` file in your Flask project root:
```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### 6. Test the Setup
1. Go to **Table Editor** in Supabase dashboard
2. Verify all tables are created:
   - `users`
   - `topics`
   - `study_sessions`
   - `user_analytics`
3. Check that sample data is present
4. Test authentication by going to **Authentication** → **Users**

## Advanced Configuration

### Row Level Security (RLS)
RLS is automatically enabled on all tables. Users can only access their own data.

### Real-time Subscriptions
To enable real-time updates in your Flask app:
```python
from supabase import create_client

supabase = create_client(url, key)
supabase.table('user_analytics').on('UPDATE', handle_analytics_update).subscribe()
```

### Storage Setup (Optional)
If you want to add user avatars:
1. Go to **Storage** in Supabase dashboard
2. Create a bucket named `avatars`
3. Set it to public
4. Run the storage policies from `config.sql`

## Troubleshooting

### Common Issues

**Migration fails with "relation already exists"**
- Drop existing tables first or use `CREATE TABLE IF NOT EXISTS`

**RLS policies not working**
- Ensure user is authenticated
- Check that `auth.uid()` returns the correct user ID

**Sample data not showing**
- Verify foreign key relationships
- Check that user IDs match between tables

**Authentication not working**
- Verify Site URL and Redirect URLs are correct
- Check that email provider is enabled

### Getting Help
- Check Supabase documentation: [supabase.com/docs](https://supabase.com/docs)
- Join the Supabase Discord community
- Review the SQL logs in your project dashboard

## Next Steps
1. Update your Flask app to use Supabase client
2. Implement authentication endpoints
3. Create CRUD operations for topics and sessions
4. Build the AI recommendation algorithms
5. Test with the sample data

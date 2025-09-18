# Supabase Database Setup for Learning Companion

## Overview
This directory contains the complete Supabase database setup for the AI-Powered Personal Learning Companion application. The database is designed to support user authentication, topic management, study session tracking, and AI-powered analytics.

## Database Schema

### Tables Created
1. **users** - User accounts with Supabase Auth integration
2. **topics** - Learning topics/subjects for each user
3. **study_sessions** - Individual study sessions with progress tracking
4. **user_analytics** - AI-powered analytics and recommendations

### Key Features
- ✅ Row Level Security (RLS) on all tables
- ✅ Automatic user_id population via triggers
- ✅ Performance-optimized indexes
- ✅ Data integrity constraints
- ✅ AI algorithm support functions
- ✅ Sample data for testing

## Setup Instructions

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

### 2. Run Migrations
Execute the migration files in order:
```bash
# In Supabase SQL Editor or via CLI
001_create_users_table.sql
002_create_topics_table.sql
003_create_study_sessions_table.sql
004_create_user_analytics_table.sql
005_additional_indexes_and_optimizations.sql
006_sample_data.sql
```

### 3. Configure Authentication
1. Go to Authentication > Settings in Supabase Dashboard
2. Enable email/password authentication
3. Configure email templates if needed

### 4. Environment Variables
Add to your Flask app's `.env` file:
```env
SUPABASE_URL=your_project_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## Database Relationships

```
users (1) ──→ topics (many)
  │                │
  │                └──→ study_sessions (many)
  │
  └──→ user_analytics (many)
```

## AI Algorithm Support

The database includes functions for:
- **Spaced Repetition**: `calculate_next_review_date()`
- **Streak Tracking**: `calculate_streak()`
- **Progress Analytics**: Automatic analytics updates via triggers

## Security Features

- Row Level Security ensures users only access their own data
- Automatic user_id population prevents data leakage
- Input validation through CHECK constraints
- Secure password hashing via Supabase Auth

## Performance Optimizations

- Composite indexes for complex queries
- Partial indexes for active records
- Optimized views for dashboard analytics
- Efficient trigger-based analytics updates

## Testing

The sample data includes:
- 3 test users with different activity levels
- 6 topics across various difficulty levels
- 10 study sessions with realistic progress data
- Complete analytics records for testing AI features

## Next Steps

1. Run the migrations in your Supabase project
2. Update your Flask app configuration
3. Test the sample data
4. Implement the AI recommendation algorithms
5. Build the frontend dashboard

# Learning Companion Setup Instructions

## 🚀 Quick Start

### 1. Environment Variables Setup

Create a `.env` file in the root directory with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# OpenAI Configuration (Optional - for AI Chat features)
OPENAI_API_KEY=your_openai_api_key

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### 2. Database Setup

Run the following migrations in your Supabase SQL Editor in order:

1. `001_create_users_table.sql`
2. `002_create_topics_table.sql`
3. `003_create_study_sessions_table.sql`
4. `004_create_user_analytics_table.sql`
5. `005_additional_indexes_and_optimizations.sql`
6. `006_sample_data.sql`
7. `007_create_quiz_system_tables.sql`
8. `008_create_gamification_tables.sql`
9. `009_create_reminder_system_tables.sql`
10. `010_create_authentication_tables.sql`
11. `011_add_topic_sharing.sql`
12. `012_add_content_management.sql`
13. `013_add_social_features.sql`
14. `014_add_mobile_accessibility.sql`
15. `015_add_ai_chat_tables.sql`
16. `016_add_advanced_analytics.sql`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

### 5. Access the Application

Open your browser and go to: `http://localhost:5000`

## 🔧 Features Available

### ✅ Core Features
- User Authentication & Registration
- Topic Management
- Study Sessions Tracking
- Analytics Dashboard
- Quiz System
- Gamification (Badges, Points, Leaderboards)
- Reminder System
- AI Recommendations

### ✅ Advanced Features (Epic 12)
- **Learning Velocity Tracking**: Measure how fast you learn
- **Knowledge Retention Curves**: Track what you remember over time
- **Learning Efficiency Metrics**: Time spent vs. knowledge gained
- **Personalized Learning Paths**: AI-generated study roadmaps
- **Knowledge Gap Detection**: Identify weaknesses automatically
- **Predictive Analytics**: Success probability, optimal study times
- **Burnout Risk Assessment**: Prevent overworking
- **Goal Achievement Forecasting**: Predict when you'll reach goals

### ✅ Social Features (Epic 10)
- Friend Connections
- Study Groups
- Social Challenges
- Achievement Sharing
- Activity Feed

### ✅ Mobile & Accessibility (Epic 11)
- Responsive Design
- Offline Access
- Cross-device Sync
- Screen Reader Support
- Keyboard Navigation
- High Contrast Mode
- Adjustable Text Size

### ✅ AI Chat Assistant
- ChatGPT-like interface
- Topic-specific conversations
- Summarization and explanations
- Question generation

## 🎯 Getting Started

1. **Register/Login**: Create your account
2. **Create Topics**: Add subjects you want to study
3. **Start Study Sessions**: Track your learning time
4. **Take Quizzes**: Test your knowledge
5. **View Analytics**: See your progress and insights
6. **Use AI Chat**: Get help with your studies
7. **Explore Advanced Analytics**: Deep insights into your learning

## 🔑 API Keys Setup

### OpenAI API Key (Optional)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. Add it to your `.env` file as `OPENAI_API_KEY=your_key_here`
4. This enables AI Chat features

### Supabase Setup
1. Go to [Supabase](https://supabase.com/)
2. Create a new project
3. Get your project URL and API keys
4. Add them to your `.env` file

## 🚨 Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not set"**: Add your OpenAI API key to `.env` file
2. **Database connection errors**: Check your Supabase credentials
3. **Migration errors**: Run migrations in the correct order
4. **Import errors**: Make sure all dependencies are installed

### Getting Help

- Check the console output for error messages
- Verify all environment variables are set
- Ensure database migrations are completed
- Check that all dependencies are installed

## 🎉 You're Ready!

Your Learning Companion is now set up with advanced analytics, social features, mobile accessibility, and AI chat capabilities. Start learning and let the platform help you achieve your goals!

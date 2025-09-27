# Learning Companion 🎓

> An intelligent personal learning assistant that helps you organize, track, and optimize your educational journey.

Learning Companion is a comprehensive study management platform built with modern web technologies. Whether you're a student, professional, or lifelong learner, this tool helps you stay organized, track your progress, and achieve your learning goals more effectively.

## ✨ What Makes It Special

- **Smart Organization**: Create and manage study topics with rich descriptions and categorization
- **Progress Tracking**: Monitor your learning journey with detailed analytics and insights
- **User-Friendly**: Clean, intuitive interface that works seamlessly across all devices
- **Secure & Private**: Your data is protected with industry-standard security practices
- **Extensible**: Built with a modular architecture that's easy to customize and extend

## 🚀 Current Features

### Core Functionality
- **📚 Topic Management**: Create, edit, and organize your study materials
- **🔐 User Authentication**: Secure login and registration system
- **📱 Responsive Design**: Beautiful interface that works on desktop, tablet, and mobile
- **📊 Dashboard**: Comprehensive overview of your learning progress
- **✅ Form Validation**: Smart input validation with helpful error messages
- **🛡️ Security**: User-specific data isolation and CSRF protection
- **💬 Real-time Feedback**: Instant notifications for all your actions

### Planned Features
- **⏱️ Study Sessions**: Track study time and monitor productivity
- **🤖 AI Recommendations**: Intelligent suggestions based on your learning patterns
- **📈 Progress Visualization**: Interactive charts and detailed analytics
- **🧠 Quiz System**: Practice questions and knowledge assessments
- **🔔 Smart Reminders**: Intelligent scheduling and study notifications

## 🛠️ Built With

| Technology | Purpose | Version |
|------------|---------|---------|
| **Flask** | Web framework | 2.3.3 |
| **Supabase** | Database & backend services | 1.2.0 |
| **Bootstrap 5** | Frontend styling | Latest |
| **Flask-WTF** | Form handling & CSRF protection | 1.1.1 |
| **Flask-Login** | User authentication | 0.6.3 |
| **pytest** | Testing framework | 7.4.2 |
| **WTForms** | Form validation | 3.0.1 |

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads)
- **Supabase Account** - [Sign up here](https://supabase.com/)
- **Code Editor** (optional) - VS Code, PyCharm, or your preferred editor

## 🚀 Quick Start

Follow these steps to get Learning Companion up and running on your machine:

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd learningCompanion
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

> 💡 **Tip**: Generate a secure secret key using: `python -c "import secrets; print(secrets.token_hex(32))"`

### 5. Set Up Supabase Database
Run the following SQL commands in your Supabase SQL editor:

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Topics table
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);
```

### 6. Launch the Application
```bash
python run.py
```

### 7. Start Learning! 🎉
Open your browser and visit: **http://localhost:5000**

## 🧪 Testing

Learning Companion includes a comprehensive test suite to ensure reliability:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_topics.py -v

# Run with coverage report
pytest tests/ --cov=app
```

## 📁 Project Structure

```
learningCompanion/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory & configuration
│   ├── forms/                   # WTForms definitions
│   │   ├── __init__.py
│   │   ├── auth_forms.py        # Authentication forms
│   │   ├── quiz_forms.py        # Quiz-related forms
│   │   └── session_forms.py     # Study session forms
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── auth.py              # User authentication models
│   │   ├── gamification.py      # Gamification models
│   │   ├── quiz.py              # Quiz system models
│   │   ├── reminders.py         # Reminder system models
│   │   └── study_session.py     # Study session models
│   ├── routes/                  # Route handlers
│   │   ├── __init__.py
│   │   ├── ai_recommendations.py # AI recommendation routes
│   │   ├── analytics.py         # Analytics routes
│   │   ├── auth_routes.py       # Authentication routes
│   │   ├── gamification.py      # Gamification routes
│   │   ├── main.py              # Main dashboard routes
│   │   ├── quizzes.py           # Quiz system routes
│   │   ├── reminders.py         # Reminder routes
│   │   ├── sessions.py          # Study session routes
│   │   └── topics.py            # Topic management routes
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   │   └── style.css        # Custom styles
│   │   ├── js/
│   │   │   └── app.js           # Frontend JavaScript
│   │   └── images/              # Image assets
│   ├── templates/               # Jinja2 templates
│   │   ├── ai/                  # AI recommendation templates
│   │   ├── analytics/           # Analytics templates
│   │   ├── auth/                # Authentication templates
│   │   ├── dashboard/           # Dashboard templates
│   │   ├── gamification/        # Gamification templates
│   │   ├── quizzes/             # Quiz system templates
│   │   ├── reminders/           # Reminder templates
│   │   ├── sessions/            # Study session templates
│   │   ├── topics/              # Topic management templates
│   │   └── base.html            # Base template
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── ai_algorithms.py     # AI recommendation algorithms
│       ├── question_generator.py # Question generation utilities
│       ├── reminder_delivery.py # Reminder delivery system
│       └── smart_scheduling.py  # Smart scheduling algorithms
├── supabase/                    # Database configuration
│   ├── config.sql              # Database configuration
│   ├── migrations/             # Database migrations
│   ├── queries/                # SQL queries
│   └── README.md               # Database setup instructions
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_sessions.py        # Study session tests
│   └── test_topics.py          # Topic management tests
├── config.py                   # Application configuration
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── README.md                   # This file
```

## 🎯 How to Use Learning Companion

### Getting Started
1. **Register/Login**: Create your account or sign in to access your personalized dashboard
2. **Explore Dashboard**: Get familiar with the overview of your learning progress
3. **Create Your First Topic**: Start by adding a study topic you want to focus on

### Managing Study Topics

#### Creating Topics
1. Navigate to **Topics** in the main menu
2. Click the **"New Topic"** button
3. Fill in the form with:
   - **Title**: A clear, descriptive name for your topic
   - **Description**: Detailed information about what you want to learn
4. Click **"Save Topic"** to create your topic

#### Organizing Your Topics
- **📖 View Details**: Click on any topic to see its full information
- **✏️ Edit**: Use the edit button to update topic information
- **🗑️ Delete**: Remove topics you no longer need (soft delete)
- **🔍 Search**: Use the search bar to quickly find specific topics

### Dashboard Overview

Your dashboard provides a comprehensive view of your learning journey:

- **📊 Quick Stats**: Total topics, study sessions, and overall progress
- **📚 Recent Topics**: Your latest topics with quick action buttons
- **⚡ Quick Actions**: Fast access to common tasks like creating new topics
- **📈 Progress Tracking**: Visual indicators of your learning progress

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `FLASK_ENV` | Flask environment mode | ✅ Yes | `development` or `production` |
| `SECRET_KEY` | Secret key for session security | ✅ Yes | `your-super-secret-key-here` |
| `SUPABASE_URL` | Your Supabase project URL | ✅ Yes | `https://xyz.supabase.co` |
| `SUPABASE_KEY` | Your Supabase anon/public key | ✅ Yes | `eyJhbGciOiJIUzI1NiIs...` |

### Database Setup

Learning Companion uses **Supabase** as its backend database. Here's what you need to configure:

1. **Create Supabase Project**: Sign up at [supabase.com](https://supabase.com) and create a new project
2. **Set Up Tables**: Run the SQL commands provided in the installation section
3. **Configure RLS**: Set up Row Level Security policies for data protection
4. **Authentication**: Configure user authentication settings in Supabase dashboard

### Security Considerations

- **Secret Key**: Use a strong, randomly generated secret key
- **Environment Variables**: Never commit sensitive data to version control
- **Database Access**: Use appropriate RLS policies to protect user data
- **HTTPS**: Always use HTTPS in production environments

## 🚀 Deployment

### Local Development
```bash
# Start the development server
python run.py

# The app will be available at http://localhost:5000
```

### Production Deployment

For production deployment, follow these steps:

#### 1. Prepare Production Environment
```bash
# Install production dependencies
pip install gunicorn

# Set production environment variables
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export SUPABASE_URL=your-production-supabase-url
export SUPABASE_KEY=your-production-supabase-key
```

#### 2. Deploy with Gunicorn
```bash
# Start the production server
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Or with additional configuration
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --keep-alive 2 run:app
```

#### 3. Production Checklist
- [ ] Set up a reverse proxy (nginx recommended)
- [ ] Configure SSL certificates
- [ ] Set up monitoring and logging
- [ ] Configure database backups
- [ ] Set up error tracking
- [ ] Configure CDN for static assets
- [ ] Set up automated deployments

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute
1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-amazing-feature`
3. **Make your changes** and test them thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to your branch**: `git push origin feature/your-amazing-feature`
6. **Open a Pull Request** with a clear description of your changes

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Help

### Getting Help
- **📚 Documentation**: Check this README and inline code comments
- **🐛 Bug Reports**: Open an issue with detailed information
- **💡 Feature Requests**: Suggest new features via GitHub issues
- **❓ Questions**: Ask questions in the discussions section

### Reporting Issues
When reporting issues, please include:
- **Environment details** (OS, Python version, etc.)
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Error messages** and logs
- **Screenshots** if applicable

## 🎉 Acknowledgments

Special thanks to the amazing open-source community:

- **Flask Team** - For the excellent web framework
- **Supabase Team** - For the powerful backend-as-a-service platform
- **Bootstrap Team** - For the responsive CSS framework
- **All Contributors** - For making this project better
- **Users** - For feedback and suggestions

---

<div align="center">

**🎓 Happy Learning with Learning Companion! 🎓**

*Made with ❤️ for learners everywhere*

</div>


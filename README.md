# Learning Companion

An AI-powered personal learning assistant built with Flask and Supabase. Organize your study topics, track learning progress, and get intelligent recommendations for your educational journey.

## 🚀 Features

### ✅ Implemented Features

- **Topic Management**: Complete CRUD operations for study topics
- **User Authentication**: Secure login and registration system
- **Responsive Design**: Modern, mobile-friendly interface
- **Dashboard**: Overview of learning progress and recent topics
- **Form Validation**: Robust input validation with user feedback
- **Security**: User-specific data isolation and CSRF protection
- **Flash Messages**: Real-time user feedback for all actions

### 🔄 Coming Soon

- **Study Sessions**: Log study time and track progress
- **AI Algorithms**: Smart recommendations and spaced repetition
- **Progress Visualization**: Charts and analytics
- **Quiz System**: Practice questions and assessments
- **Study Reminders**: Intelligent scheduling and notifications

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Testing**: pytest

## 📋 Prerequisites

- Python 3.8 or higher
- Supabase account and project
- Git

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd learningCompanion
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   SUPABASE_URL=your-supabase-project-url
   SUPABASE_KEY=your-supabase-anon-key
   ```

5. **Set up Supabase Database**
   
   Create the following tables in your Supabase project:

   **Users Table:**
   ```sql
   CREATE TABLE users (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       email VARCHAR(255) UNIQUE NOT NULL,
       name VARCHAR(255),
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
       updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );
   ```

   **Topics Table:**
   ```sql
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

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_topics.py -v
```

## 📁 Project Structure

```
learningCompanion/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── forms/               # WTForms definitions
│   │   └── __init__.py
│   ├── models/              # Database models
│   │   └── __init__.py
│   ├── routes/              # Route handlers
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── main.py          # Main dashboard routes
│   │   └── topics.py        # Topic management routes
│   ├── static/              # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── app.js
│   │   └── images/
│   ├── templates/           # Jinja2 templates
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── topics/
│   │   └── base.html
│   └── utils/               # Utility functions
│       └── __init__.py
├── tests/                   # Test files
│   ├── __init__.py
│   └── test_topics.py
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── run.py                 # Application entry point
└── README.md              # This file
```

## 🎯 Usage Guide

### Creating Topics

1. **Navigate to Topics**: Click "Topics" in the navigation menu
2. **Create New Topic**: Click "New Topic" button
3. **Fill Form**: Enter a descriptive title and detailed description
4. **Save**: Click "Save Topic" to create your topic

### Managing Topics

- **View**: Click on any topic to see its details
- **Edit**: Use the edit button to modify topic information
- **Delete**: Use the delete button to remove topics (soft delete)
- **Search**: Use the search bar to find specific topics

### Dashboard Features

- **Quick Stats**: View your total topics, study sessions, and progress
- **Recent Topics**: See your latest topics with quick actions
- **Quick Actions**: Fast access to common tasks

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FLASK_ENV` | Flask environment (development/production) | Yes |
| `SECRET_KEY` | Secret key for session management | Yes |
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_KEY` | Your Supabase anon/public key | Yes |

### Database Configuration

The application uses Supabase as the backend database. Make sure to:

1. Create a Supabase project
2. Set up the required tables (see installation section)
3. Configure Row Level Security (RLS) policies
4. Set up authentication if needed

## 🚀 Deployment

### Local Development
```bash
python run.py
```

### Production Deployment

1. **Set environment variables** for production
2. **Use a production WSGI server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

3. **Set up a reverse proxy** (nginx recommended)
4. **Configure SSL certificates**
5. **Set up monitoring and logging**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🎉 Acknowledgments

- Flask community for the excellent web framework
- Supabase team for the amazing backend-as-a-service
- Bootstrap team for the responsive CSS framework
- All contributors and users of this project

---

**Happy Learning! 🎓**


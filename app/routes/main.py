from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from app.models import Topic, User
from app.models.study_session import StudySession

main = Blueprint('main', __name__)

from app.routes.topics import mock_user

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
def dashboard():
    try:
        print(f"Loading dashboard for user: {mock_user.id}")
        
        topics = Topic.get_all_by_user(mock_user.id, limit=6)
        print(f"Found {len(topics)} topics for dashboard")
        
        try:
            session_stats = StudySession.get_session_stats(mock_user.id, days=30)
            print(f"Session stats: {session_stats}")
        except Exception as e:
            print(f"Error getting session stats: {e}")
            session_stats = {'total_sessions': 0, 'total_time_hours': 0, 'total_time_minutes': 0}
        
        try:
            recent_sessions = StudySession.get_user_sessions(mock_user.id, limit=5)
            print(f"Found {len(recent_sessions)} recent sessions")
        except Exception as e:
            print(f"Error getting recent sessions: {e}")
            recent_sessions = []
        
        try:
            study_streak = StudySession.get_session_streak(mock_user.id)
            print(f"Study streak: {study_streak}")
        except Exception as e:
            print(f"Error getting study streak: {e}")
            study_streak = 0
        
        try:
            weekly_study_time = StudySession.get_weekly_study_time(mock_user.id)
            print(f"Weekly study time: {weekly_study_time}")
        except Exception as e:
            print(f"Error getting weekly study time: {e}")
            weekly_study_time = 0
        
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        topics = []
        session_stats = {'total_sessions': 0, 'total_time_hours': 0, 'total_time_minutes': 0}
        recent_sessions = []
        study_streak = 0
        weekly_study_time = 0
    
    return render_template('dashboard/index.html', 
                         topics=topics,
                         session_stats=session_stats,
                         recent_sessions=recent_sessions,
                         study_streak=study_streak,
                         weekly_study_time=weekly_study_time)

@main.route('/api/dashboard-stats')
def dashboard_stats():
    try:
        topics = Topic.get_all_by_user(mock_user.id)
        topic_count = len(topics)
        
        try:
            session_stats = StudySession.get_session_stats(mock_user.id, days=30)
            session_count = session_stats.get('total_sessions', 0)
            total_time = session_stats.get('total_time_hours', 0)
        except:
            session_count = 0
            total_time = 0
        
        try:
            study_streak = StudySession.get_session_streak(mock_user.id)
        except:
            study_streak = 0
        
        return {
            'topic_count': topic_count,
            'session_count': session_count,
            'total_time_hours': total_time,
            'study_streak': study_streak
        }
    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        return {
            'topic_count': 0,
            'session_count': 0,
            'total_time_hours': 0,
            'study_streak': 0
        }

@main.route('/test')
def test():
    return "Learning Companion is working! You can now test the topic functionality."
from flask import Flask
from flask_login import LoginManager
from config import config
from dotenv import load_dotenv
import os

load_dotenv()

print(f"=== FLASK APP INITIALIZATION ===")
print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"SUPABASE_SERVICE_ROLE_KEY: {os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'Not set')[:20]}...")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'Not set')[:20]}...")

login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.auth import AuthUser
        return AuthUser.get_by_id(user_id)
    
    
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        if text is None:
            return ''
        return text.replace('\n', '<br>')
    
    @app.template_filter('safe_date')
    def safe_date_filter(date_obj, format_str='%B %d, %Y'):
        """Safely format a date, handling both datetime objects and strings"""
        if date_obj is None:
            return 'N/A'
        if isinstance(date_obj, str):
            return date_obj
        try:
            return date_obj.strftime(format_str)
        except (AttributeError, TypeError):
            return str(date_obj)
    
    
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.routes.auth_routes import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.routes.topics import topics as topics_blueprint
    app.register_blueprint(topics_blueprint)
    
    from app.routes.sessions import sessions as sessions_blueprint
    app.register_blueprint(sessions_blueprint)
    
    from app.routes.analytics import analytics as analytics_blueprint
    app.register_blueprint(analytics_blueprint)
    
    from app.routes.ai_recommendations import ai_recommendations as ai_blueprint
    app.register_blueprint(ai_blueprint)
    
    from app.routes.quizzes import quizzes as quizzes_blueprint
    app.register_blueprint(quizzes_blueprint)
    
    from app.routes.gamification import gamification as gamification_blueprint
    app.register_blueprint(gamification_blueprint)
    
    from app.routes.reminders import reminders_bp as reminders_blueprint
    app.register_blueprint(reminders_blueprint)
    
    from app.routes.social import social as social_blueprint
    app.register_blueprint(social_blueprint)
    
    from app.routes.mobile_accessibility import mobile_accessibility as mobile_accessibility_blueprint
    app.register_blueprint(mobile_accessibility_blueprint)

    from app.routes.support import support as support_blueprint
    app.register_blueprint(support_blueprint)

    from app.routes.ai_chat import ai_chat as ai_chat_blueprint
    app.register_blueprint(ai_chat_blueprint)

    from app.routes.advanced_analytics import advanced_analytics_bp as advanced_analytics_blueprint
    app.register_blueprint(advanced_analytics_blueprint)

    from app.routes.gcse import gcse as gcse_blueprint
    app.register_blueprint(gcse_blueprint)

    from app.routes.gcse_past_papers import gcse_past_papers as gcse_past_papers_blueprint
    app.register_blueprint(gcse_past_papers_blueprint)

    from app.routes.gcse_grading import gcse_grading as gcse_grading_blueprint
    app.register_blueprint(gcse_grading_blueprint)

    from app.routes.gcse_scheduling import gcse_scheduling as gcse_scheduling_blueprint
    app.register_blueprint(gcse_scheduling_blueprint)

    from app.routes.gcse_techniques import gcse_techniques as gcse_techniques_blueprint
    app.register_blueprint(gcse_techniques_blueprint)

    from app.routes.gcse_analytics import gcse_analytics as gcse_analytics_blueprint
    app.register_blueprint(gcse_analytics_blueprint)

    from app.routes.gcse_resources import gcse_resources as gcse_resources_blueprint
    app.register_blueprint(gcse_resources_blueprint)

    return app


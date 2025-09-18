from flask import Flask
from flask_login import LoginManager
from config import config
from dotenv import load_dotenv
import os

load_dotenv()

print(f"=== FLASK APP INITIALIZATION ===")
print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"SUPABASE_SERVICE_ROLE_KEY: {os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'Not set')[:20]}...")

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
    
    return app
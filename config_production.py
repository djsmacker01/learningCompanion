import os
from dotenv import load_dotenv

load_dotenv()

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'prod-secret-key-change-this'
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

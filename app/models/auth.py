

import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv


load_dotenv()


from app.models import get_supabase_client


SUPABASE_AVAILABLE = bool(os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_SERVICE_ROLE_KEY'))


class UserProfile:
    
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.avatar_url = data.get('avatar_url')
        self.bio = data.get('bio')
        self.timezone = data.get('timezone', 'UTC')
        self.language = data.get('language', 'en')
        self.email_notifications = data.get('email_notifications', True)
        self.sms_notifications = data.get('sms_notifications', False)
        self.study_reminders = data.get('study_reminders', True)
        self.privacy_level = data.get('privacy_level', 'private')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
    
    @property
    def full_name(self) -> str:
        
        if hasattr(self, 'first_name') and hasattr(self, 'last_name'):
            if self.first_name and self.last_name:
                return f"{self.first_name} {self.last_name}"
            elif self.first_name:
                return self.first_name
            elif self.last_name:
                return self.last_name
        return self.email or "Anonymous User"
    
    @classmethod
    def get_by_user_id(cls, user_id: str) -> Optional['UserProfile']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
            
            if response.data:
                return cls(response.data[0])
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    @classmethod
    def create_profile(cls, user_id: str, **kwargs) -> Optional['UserProfile']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            profile_data = {
                'user_id': user_id,
                'first_name': kwargs.get('first_name'),
                'last_name': kwargs.get('last_name'),
                'bio': kwargs.get('bio'),
                'timezone': kwargs.get('timezone', 'UTC'),
                'language': kwargs.get('language', 'en'),
                'email_notifications': kwargs.get('email_notifications', True),
                'sms_notifications': kwargs.get('sms_notifications', False),
                'study_reminders': kwargs.get('study_reminders', True),
                'privacy_level': kwargs.get('privacy_level', 'private')
            }
            
            response = supabase.table('user_profiles').insert(profile_data).execute()
            
            if response.data:
                return cls(response.data[0])
            return None
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return None
    
    def get_learning_style(self):
        """Get the user's saved learning style"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('ai_learning_styles').select('*').eq('user_id', self.user_id).execute()
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error getting learning style: {e}")
            return None

    def update_profile(self, **kwargs) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
        
        try:
            supabase = get_supabase_client()
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            
            response = supabase.table('user_profiles').update(update_data).eq('id', self.id).execute()
            
            if response.data:
                
                for key, value in update_data.items():
                    setattr(self, key, value)
                return True
            return False
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False


class UserSession:
    
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.session_token = data.get('session_token')
        self.ip_address = data.get('ip_address')
        self.user_agent = data.get('user_agent')
        self.is_active = data.get('is_active', True)
        self.expires_at = data.get('expires_at')
        self.created_at = data.get('created_at')
        self.last_accessed = data.get('last_accessed')
    
    @classmethod
    def create_session(cls, user_id: str, ip_address: str = None, user_agent: str = None, 
                      duration_hours: int = 24) -> Optional['UserSession']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            
            
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=duration_hours)
            
            session_data = {
                'user_id': user_id,
                'session_token': session_token,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'expires_at': expires_at.isoformat(),
                'is_active': True
            }
            
            response = supabase.table('user_sessions').insert(session_data).execute()
            
            if response.data:
                return cls(response.data[0])
            return None
        except Exception as e:
            print(f"Error creating user session: {e}")
            return None
    
    @classmethod
    def get_by_token(cls, session_token: str) -> Optional['UserSession']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('user_sessions').select('*').eq('session_token', session_token).eq('is_active', True).execute()
            
            if response.data:
                session = cls(response.data[0])
                
                if datetime.fromisoformat(session.expires_at.replace('Z', '+00:00')) < datetime.now():
                    session.deactivate()
                    return None
                return session
            return None
        except Exception as e:
            print(f"Error getting session by token: {e}")
            return None
    
    def deactivate(self) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('user_sessions').update({'is_active': False}).eq('id', self.id).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error deactivating session: {e}")
            return False
    
    def update_last_accessed(self) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('user_sessions').update({'last_accessed': datetime.now().isoformat()}).eq('id', self.id).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error updating last accessed: {e}")
            return False
    
    @classmethod
    def cleanup_expired_sessions(cls) -> int:
        
        if not SUPABASE_AVAILABLE:
            return 0
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('user_sessions').delete().lt('expires_at', datetime.now().isoformat()).execute()
            return len(response.data) if response.data else 0
        except Exception as e:
            print(f"Error cleaning up expired sessions: {e}")
            return 0


class PasswordResetToken:
    
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.token = data.get('token')
        self.expires_at = data.get('expires_at')
        self.used = data.get('used', False)
        self.created_at = data.get('created_at')
    
    @classmethod
    def create_token(cls, user_id: str, duration_hours: int = 1) -> Optional['PasswordResetToken']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            
            
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=duration_hours)
            
            token_data = {
                'user_id': user_id,
                'token': token,
                'expires_at': expires_at.isoformat(),
                'used': False
            }
            
            response = supabase.table('password_reset_tokens').insert(token_data).execute()
            
            if response.data:
                return cls(response.data[0])
            return None
        except Exception as e:
            print(f"Error creating password reset token: {e}")
            return None
    
    @classmethod
    def get_by_token(cls, token: str) -> Optional['PasswordResetToken']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('password_reset_tokens').select('*').eq('token', token).eq('used', False).execute()
            
            if response.data:
                reset_token = cls(response.data[0])
                
                if datetime.fromisoformat(reset_token.expires_at.replace('Z', '+00:00')) < datetime.now():
                    return None
                return reset_token
            return None
        except Exception as e:
            print(f"Error getting password reset token: {e}")
            return None
    
    def mark_as_used(self) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('password_reset_tokens').update({'used': True}).eq('id', self.id).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error marking token as used: {e}")
            return False


class LoginAttempt:
    
    
    @classmethod
    def record_attempt(cls, email: str, ip_address: str = None, user_agent: str = None, 
                      success: bool = False, failure_reason: str = None) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
        
        try:
            supabase = get_supabase_client()
            
            attempt_data = {
                'email': email,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'success': success,
                'failure_reason': failure_reason
            }
            
            response = supabase.table('login_attempts').insert(attempt_data).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error recording login attempt: {e}")
            return False
    
    @classmethod
    def get_recent_attempts(cls, email: str, hours: int = 1) -> List[Dict[str, Any]]:
        
        if not SUPABASE_AVAILABLE:
            return []
        
        try:
            supabase = get_supabase_client()
            since = datetime.now() - timedelta(hours=hours)
            
            response = supabase.table('login_attempts').select('*').eq('email', email).gte('created_at', since.isoformat()).order('created_at', desc=True).execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting recent login attempts: {e}")
            return []
    
    @classmethod
    def is_account_locked(cls, email: str, max_attempts: int = 5, lockout_hours: int = 1) -> bool:
        
        recent_attempts = cls.get_recent_attempts(email, lockout_hours)
        failed_attempts = [attempt for attempt in recent_attempts if not attempt.get('success')]
        
        return len(failed_attempts) >= max_attempts


class AuthUser:
    
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.email = data.get('email')
        self.password_hash = data.get('password_hash')
        self.is_active = data.get('is_active', True)
        self.username = data.get('username')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.last_login = data.get('last_login')
        
        
        self.profile = None
        if self.id:
            try:
                # Use the auth UserProfile which has privacy_level and other profile fields
                self.profile = UserProfile.get_by_user_id(self.id)
                if not self.profile:
                    # Create a default profile if none exists
                    self.profile = UserProfile.create_profile(self.id)
            except Exception as e:
                print(f"Warning: Could not load profile: {e}")
    
    @property
    def is_authenticated(self) -> bool:
        
        return self.is_active and self.id is not None
    
    @property
    def is_anonymous(self) -> bool:
        
        return not self.is_authenticated
    
    @property
    def full_name(self) -> str:
        
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.email or "Anonymous User"
    
    def get_id(self) -> str:
        
        return str(self.id) if self.id else None
    
    def get_gamification_profile(self):
        """Get the gamification profile for XP, levels, etc."""
        if not self.id:
            return None
        try:
            from app.models.gamification import UserProfile as GamificationProfile
            return GamificationProfile.get_or_create_profile(self.id)
        except Exception as e:
            print(f"Warning: Could not load gamification profile: {e}")
            return None
    
    def check_password(self, password: str) -> bool:
        
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password: str) -> None:
        
        self.password_hash = generate_password_hash(password)
    
    @classmethod
    def get_by_email(cls, email: str) -> Optional['AuthUser']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('users').select('*').eq('email', email).execute()
            
            if response.data:
                return cls(response.data[0])
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    @classmethod
    def get_by_username(cls, username: str) -> Optional['AuthUser']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('users').select('*').eq('username', username).execute()
            
            if response.data:
                return cls(response.data[0])
            return None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
    
    @classmethod
    def get_by_username_or_email(cls, identifier: str) -> Optional['AuthUser']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            
            # Try username first
            response = supabase.table('users').select('*').eq('username', identifier).execute()
            if response.data:
                return cls(response.data[0])
            
            # Try email
            response = supabase.table('users').select('*').eq('email', identifier).execute()
            if response.data:
                return cls(response.data[0])
            
            return None
        except Exception as e:
            print(f"Error getting user by username or email: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, user_id: str) -> Optional['AuthUser']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('users').select('*').eq('id', user_id).execute()
            
            if response.data:
                return cls(response.data[0])
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    @classmethod
    def create_user(cls, email: str, password: str, **kwargs) -> Optional['AuthUser']:
        
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            
            
            existing_user = cls.get_by_email(email)
            if existing_user:
                return None
            
            
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            
            
            while True:
                existing_user = supabase.table('users').select('id').eq('username', username).execute()
                if not existing_user.data:
                    break
                username = f"{base_username}_{counter}"
                counter += 1
                if counter > 1000:  
                    username = f"{base_username}_{secrets.token_hex(4)}"
                    break
            
            
            user_data = {
                'email': email,
                'password_hash': generate_password_hash(password),
                'is_active': kwargs.get('is_active', True),
                'username': username,
                'first_name': kwargs.get('first_name', ''),
                'last_name': kwargs.get('last_name', '')
            }
            
            response = supabase.table('users').insert(user_data).execute()
            
            if response.data:
                user = cls(response.data[0])
                
                
                try:
                    from app.models.gamification import UserProfile as GamificationProfile
                    GamificationProfile.create_profile(user.id)
                except Exception as e:
                    print(f"Warning: Could not create gamification profile: {e}")
                
                return user
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def update_last_login(self) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('users').update({'last_login': datetime.now().isoformat()}).eq('id', self.id).execute()
            
            if response.data:
                self.last_login = response.data[0].get('last_login')
                return True
            return False
        except Exception as e:
            print(f"Error updating last login: {e}")
            return False
    
    def update_password(self, new_password: str) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('users').update({'password_hash': generate_password_hash(new_password)}).eq('id', self.id).execute()
            
            if response.data:
                self.password_hash = response.data[0].get('password_hash')
                return True
            return False
        except Exception as e:
            print(f"Error updating password: {e}")
            return False


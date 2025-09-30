"""
Authentication models for user management, sessions, and security
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Supabase client
from app.models import get_supabase_client

# Check if Supabase is available
SUPABASE_AVAILABLE = bool(os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_SERVICE_ROLE_KEY'))


class UserProfile:
    """User profile model for extended user information"""
    
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
        """Get the user's full name"""
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
        """Get user profile by user ID"""
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
        """Create a new user profile"""
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
    
    def update_profile(self, **kwargs) -> bool:
        """Update user profile"""
        if not SUPABASE_AVAILABLE:
            return False
        
        try:
            supabase = get_supabase_client()
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            
            response = supabase.table('user_profiles').update(update_data).eq('id', self.id).execute()
            
            if response.data:
                # Update local attributes
                for key, value in update_data.items():
                    setattr(self, key, value)
                return True
            return False
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False


class UserSession:
    """User session model for session management"""
    
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
        """Create a new user session"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            
            # Generate secure session token
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
        """Get session by token"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('user_sessions').select('*').eq('session_token', session_token).eq('is_active', True).execute()
            
            if response.data:
                session = cls(response.data[0])
                # Check if session is expired
                if datetime.fromisoformat(session.expires_at.replace('Z', '+00:00')) < datetime.now():
                    session.deactivate()
                    return None
                return session
            return None
        except Exception as e:
            print(f"Error getting session by token: {e}")
            return None
    
    def deactivate(self) -> bool:
        """Deactivate the session"""
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
        """Update last accessed timestamp"""
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
        """Clean up expired sessions"""
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
    """Password reset token model"""
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.token = data.get('token')
        self.expires_at = data.get('expires_at')
        self.used = data.get('used', False)
        self.created_at = data.get('created_at')
    
    @classmethod
    def create_token(cls, user_id: str, duration_hours: int = 1) -> Optional['PasswordResetToken']:
        """Create a new password reset token"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            
            # Generate secure token
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
        """Get token by value"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            response = supabase.table('password_reset_tokens').select('*').eq('token', token).eq('used', False).execute()
            
            if response.data:
                reset_token = cls(response.data[0])
                # Check if token is expired
                if datetime.fromisoformat(reset_token.expires_at.replace('Z', '+00:00')) < datetime.now():
                    return None
                return reset_token
            return None
        except Exception as e:
            print(f"Error getting password reset token: {e}")
            return None
    
    def mark_as_used(self) -> bool:
        """Mark token as used"""
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
    """Login attempt tracking model"""
    
    @classmethod
    def record_attempt(cls, email: str, ip_address: str = None, user_agent: str = None, 
                      success: bool = False, failure_reason: str = None) -> bool:
        """Record a login attempt"""
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
        """Get recent login attempts for an email"""
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
        """Check if account is locked due to too many failed attempts"""
        recent_attempts = cls.get_recent_attempts(email, lockout_hours)
        failed_attempts = [attempt for attempt in recent_attempts if not attempt.get('success')]
        
        return len(failed_attempts) >= max_attempts


class AuthUser:
    """Enhanced user model with authentication capabilities"""
    
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
        
        # Load profile if available (using gamification profile for now)
        self.profile = None
        if self.id:
            try:
                from app.models.gamification import UserProfile as GamificationProfile
                self.profile = GamificationProfile.get_or_create_profile(self.id)
            except Exception as e:
                print(f"Warning: Could not load profile: {e}")
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.is_active and self.id is not None
    
    @property
    def is_anonymous(self) -> bool:
        """Check if user is anonymous"""
        return not self.is_authenticated
    
    @property
    def full_name(self) -> str:
        """Get the user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.email or "Anonymous User"
    
    def get_id(self) -> str:
        """Get user ID for Flask-Login"""
        return str(self.id) if self.id else None
    
    def check_password(self, password: str) -> bool:
        """Check if provided password is correct"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password: str) -> None:
        """Set user password"""
        self.password_hash = generate_password_hash(password)
    
    @classmethod
    def get_by_email(cls, email: str) -> Optional['AuthUser']:
        """Get user by email"""
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
    def get_by_id(cls, user_id: str) -> Optional['AuthUser']:
        """Get user by ID"""
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
        """Create a new user"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase_client()
            
            # Check if user already exists
            existing_user = cls.get_by_email(email)
            if existing_user:
                return None
            
            # Generate unique username
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            
            # Check if username exists and generate unique one
            while True:
                existing_user = supabase.table('users').select('id').eq('username', username).execute()
                if not existing_user.data:
                    break
                username = f"{base_username}_{counter}"
                counter += 1
                if counter > 1000:  # Safety limit
                    username = f"{base_username}_{secrets.token_hex(4)}"
                    break
            
            # Create user data
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
                
                # Create gamification profile (basic profile)
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
        """Update last login timestamp"""
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
        """Update user password"""
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

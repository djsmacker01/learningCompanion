

import json
from datetime import datetime, time, timedelta
from typing import List, Dict, Optional, Any
from app.models import get_supabase_client, SUPABASE_AVAILABLE


class StudyReminderPreferences:
    
    
    def __init__(self, id=None, user_id=None, is_enabled=True, reminder_methods=None, 
                 preferred_times=None, timezone='UTC', frequency='daily', 
                 days_of_week=None, study_goal_minutes=30, advance_notice_minutes=15,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.is_enabled = is_enabled
        self.reminder_methods = reminder_methods or ['email']
        self.preferred_times = preferred_times or ['09:00', '18:00']
        self.timezone = timezone
        self.frequency = frequency
        self.days_of_week = days_of_week or [1, 2, 3, 4, 5]  
        self.study_goal_minutes = study_goal_minutes
        self.advance_notice_minutes = advance_notice_minutes
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_or_create_preferences(cls, user_id: str):
        
        if not SUPABASE_AVAILABLE:
            return cls(user_id=user_id)
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('study_reminder_preferences').select('*').eq('user_id', user_id).execute()
            if result.data:
                data = result.data[0]
                return cls(**data)
            else:
                
                preferences = cls(user_id=user_id)
                return preferences.save()
        except Exception as e:
            print(f"Error getting reminder preferences: {e}")
            
            return cls(user_id=user_id)

    def save(self):
        
        if not SUPABASE_AVAILABLE:
            return self
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'user_id': self.user_id,
                'is_enabled': self.is_enabled,
                'reminder_methods': self.reminder_methods,
                'preferred_times': self.preferred_times,
                'timezone': self.timezone,
                'frequency': self.frequency,
                'days_of_week': self.days_of_week,
                'study_goal_minutes': self.study_goal_minutes,
                'advance_notice_minutes': self.advance_notice_minutes,
                'updated_at': datetime.now().isoformat()
            }
            
            if self.id:
                
                result = supabase.table('study_reminder_preferences').update(data).eq('id', self.id).execute()
            else:
                
                data['created_at'] = datetime.now().isoformat()
                result = supabase.table('study_reminder_preferences').insert(data).execute()
                
            if result.data:
                data = result.data[0]
                self.id = data['id']
                self.created_at = data['created_at']
                self.updated_at = data['updated_at']
                
        except Exception as e:
            print(f"Error saving reminder preferences: {e}")
            
        return self


class StudyReminder:
    
    
    def __init__(self, id=None, user_id=None, title=None, message=None, 
                 scheduled_time=None, reminder_type='study', reminder_method='email',
                 status='pending', topic_id=None, session_type=None, priority='medium',
                 is_recurring=False, recurrence_pattern=None, sent_at=None,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.scheduled_time = scheduled_time
        self.reminder_type = reminder_type
        self.reminder_method = reminder_method
        self.status = status
        self.topic_id = topic_id
        self.session_type = session_type
        self.priority = priority
        self.is_recurring = is_recurring
        self.recurrence_pattern = recurrence_pattern or {}
        self.sent_at = sent_at
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_reminder(cls, user_id: str, title: str, scheduled_time: datetime, 
                       message: str = None, reminder_type: str = 'study',
                       reminder_method: str = 'email', topic_id: str = None,
                       session_type: str = None, priority: str = 'medium'):
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'user_id': user_id,
                'title': title,
                'message': message,
                'scheduled_time': scheduled_time.isoformat(),
                'reminder_type': reminder_type,
                'reminder_method': reminder_method,
                'status': 'pending',
                'topic_id': topic_id,
                'session_type': session_type,
                'priority': priority,
                'is_recurring': False,
                'recurrence_pattern': {},
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            result = supabase.table('study_reminders').insert(data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error creating reminder: {e}")
            
        return None

    @classmethod
    def get_user_reminders(cls, user_id: str, status: str = None, limit: int = 50):
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('study_reminders').select('*').eq('user_id', user_id)
            if status:
                query = query.eq('status', status)
            query = query.order('scheduled_time').limit(limit)
            
            result = query.execute()
            return [cls(**reminder) for reminder in result.data]
        except Exception as e:
            print(f"Error getting user reminders: {e}")
            
            return []

    @classmethod
    def get_pending_reminders(cls, before_time: datetime = None):
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('study_reminders').select('*').eq('status', 'pending')
            if before_time:
                query = query.lte('scheduled_time', before_time.isoformat())
            else:
                query = query.lte('scheduled_time', datetime.now().isoformat())
                
            result = query.order('scheduled_time').execute()
            return [cls(**reminder) for reminder in result.data]
        except Exception as e:
            print(f"Error getting pending reminders: {e}")
            return []

    def mark_as_sent(self):
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'status': 'sent',
                'sent_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            result = supabase.table('study_reminders').update(data).eq('id', self.id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error marking reminder as sent: {e}")
            return False

    def cancel(self):
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'status': 'cancelled',
                'updated_at': datetime.now().isoformat()
            }
            
            result = supabase.table('study_reminders').update(data).eq('id', self.id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error cancelling reminder: {e}")
            return False


class StudySchedule:
    
    
    def __init__(self, id=None, user_id=None, title=None, description=None,
                 scheduled_start=None, scheduled_end=None, topic_id=None,
                 session_type='review', priority='medium', is_recurring=False,
                 recurrence_pattern=None, status='scheduled', actual_start=None,
                 actual_end=None, notes=None, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.scheduled_start = scheduled_start
        self.scheduled_end = scheduled_end
        self.topic_id = topic_id
        self.session_type = session_type
        self.priority = priority
        self.is_recurring = is_recurring
        self.recurrence_pattern = recurrence_pattern or {}
        self.status = status
        self.actual_start = actual_start
        self.actual_end = actual_end
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_schedule(cls, user_id: str, title: str, scheduled_start: datetime,
                       scheduled_end: datetime, topic_id: str = None,
                       session_type: str = 'review', description: str = None,
                       priority: str = 'medium'):
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'user_id': user_id,
                'title': title,
                'description': description,
                'scheduled_start': scheduled_start.isoformat(),
                'scheduled_end': scheduled_end.isoformat(),
                'topic_id': topic_id,
                'session_type': session_type,
                'priority': priority,
                'is_recurring': False,
                'recurrence_pattern': {},
                'status': 'scheduled',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            result = supabase.table('study_schedules').insert(data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error creating schedule: {e}")
            
        return None

    @classmethod
    def get_user_schedules(cls, user_id: str, start_date: datetime = None,
                          end_date: datetime = None, status: str = None):
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('study_schedules').select('*').eq('user_id', user_id)
            
            if start_date:
                query = query.gte('scheduled_start', start_date.isoformat())
            if end_date:
                query = query.lte('scheduled_start', end_date.isoformat())
            if status:
                query = query.eq('status', status)
                
            result = query.order('scheduled_start').execute()
            return [cls(**schedule) for schedule in result.data]
        except Exception as e:
            print(f"Error getting user schedules: {e}")
            
            return []

    def start_session(self):
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'status': 'in_progress',
                'actual_start': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            result = supabase.table('study_schedules').update(data).eq('id', self.id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error starting schedule: {e}")
            return False

    def complete_session(self):
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'status': 'completed',
                'actual_end': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            result = supabase.table('study_schedules').update(data).eq('id', self.id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error completing schedule: {e}")
            return False


class OptimalStudyTime:
    
    
    def __init__(self, id=None, user_id=None, suggested_time=None, confidence_score=0.5,
                 reasoning=None, factors=None, topic_id=None, session_type='review',
                 is_accepted=False, accepted_at=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.suggested_time = suggested_time
        self.confidence_score = confidence_score
        self.reasoning = reasoning
        self.factors = factors or {}
        self.topic_id = topic_id
        self.session_type = session_type
        self.is_accepted = is_accepted
        self.accepted_at = accepted_at
        self.created_at = created_at

    @classmethod
    def create_suggestion(cls, user_id: str, suggested_time: datetime,
                         confidence_score: float, reasoning: str,
                         factors: Dict[str, Any] = None, topic_id: str = None,
                         session_type: str = 'review'):
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'user_id': user_id,
                'suggested_time': suggested_time.isoformat(),
                'confidence_score': confidence_score,
                'reasoning': reasoning,
                'factors': factors or {},
                'topic_id': topic_id,
                'session_type': session_type,
                'is_accepted': False,
                'created_at': datetime.now().isoformat()
            }
            
            result = supabase.table('optimal_study_times').insert(data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error creating optimal study time suggestion: {e}")
            
        return None

    @classmethod
    def get_user_suggestions(cls, user_id: str, limit: int = 10):
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('optimal_study_times').select('*').eq('user_id', user_id).order('confidence_score', desc=True).limit(limit).execute()
            return [cls(**suggestion) for suggestion in result.data]
        except Exception as e:
            print(f"Error getting optimal study time suggestions: {e}")
            
            return []

    def accept(self):
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'is_accepted': True,
                'accepted_at': datetime.now().isoformat()
            }
            
            result = supabase.table('optimal_study_times').update(data).eq('id', self.id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error accepting optimal study time: {e}")
            return False


class StudyPattern:
    
    
    def __init__(self, id=None, user_id=None, pattern_type=None, pattern_data=None,
                 confidence_score=0.5, sample_size=1, last_updated=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.pattern_type = pattern_type
        self.pattern_data = pattern_data or {}
        self.confidence_score = confidence_score
        self.sample_size = sample_size
        self.last_updated = last_updated
        self.created_at = created_at

    @classmethod
    def get_user_patterns(cls, user_id: str, pattern_type: str = None):
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('study_patterns').select('*').eq('user_id', user_id)
            if pattern_type:
                query = query.eq('pattern_type', pattern_type)
                
            result = query.order('confidence_score', desc=True).execute()
            return [cls(**pattern) for pattern in result.data]
        except Exception as e:
            print(f"Error getting study patterns: {e}")
            return []

    @classmethod
    def update_pattern(cls, user_id: str, pattern_type: str, pattern_data: Dict[str, Any],
                      confidence_score: float, sample_size: int):
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            
            existing = supabase.table('study_patterns').select('id').eq('user_id', user_id).eq('pattern_type', pattern_type).execute()
            
            data = {
                'user_id': user_id,
                'pattern_type': pattern_type,
                'pattern_data': pattern_data,
                'confidence_score': confidence_score,
                'sample_size': sample_size,
                'last_updated': datetime.now().isoformat()
            }
            
            if existing.data:
                
                result = supabase.table('study_patterns').update(data).eq('id', existing.data[0]['id']).execute()
            else:
                
                data['created_at'] = datetime.now().isoformat()
                result = supabase.table('study_patterns').insert(data).execute()
                
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error updating study pattern: {e}")
            
        return None


from datetime import datetime, timedelta
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import uuid

_in_memory_sessions = []
_next_session_id = 1

class StudySession:
    def __init__(self, id, topic_id, user_id, session_date, duration_minutes, 
                 confidence_before, confidence_after, notes, session_type, 
                 completed, created_at=None):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.session_date = session_date
        self.duration_minutes = duration_minutes
        self.confidence_before = confidence_before
        self.confidence_after = confidence_after
        self.notes = notes
        self.session_type = session_type
        self.completed = completed
        self.created_at = created_at or datetime.utcnow()
    
    @staticmethod
    def create_session(user_id, topic_id, session_date, duration_minutes, 
                      confidence_before, confidence_after, notes, session_type, completed=True):
        # Get Supabase client dynamically
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            raise Exception("Supabase not available - cannot create session")
        
        try:
            data = {
                'topic_id': topic_id,
                'user_id': user_id,
                'session_date': session_date.isoformat() if isinstance(session_date, datetime) else session_date,
                'duration_minutes': duration_minutes,
                'confidence_before': confidence_before,
                'confidence_after': confidence_after,
                'notes': notes or '',
                'session_type': session_type,
                'completed': completed,
                'created_at': datetime.utcnow().isoformat()
            }
            response = client.table('study_sessions').insert(data).execute()
            if response.data:
                session_data = response.data[0]
                print(f"✅ Created session in Supabase: {session_data['session_type']} (ID: {session_data['id']})")
                return StudySession(
                    session_data['id'],
                    session_data['topic_id'],
                    session_data['user_id'],
                    datetime.fromisoformat(session_data['session_date']),
                    session_data['duration_minutes'],
                    session_data['confidence_before'],
                    session_data['confidence_after'],
                    session_data['notes'],
                    session_data['session_type'],
                    session_data['completed'],
                    datetime.fromisoformat(session_data['created_at'])
                )
            return None
        except Exception as e:
            print(f" Error creating session in Supabase: {e}")
            raise Exception(f"Failed to create session: {e}")
    
    @staticmethod
    def get_user_sessions(user_id, limit=None):
        """Get user's sessions (recent first)"""
      
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            raise Exception("Supabase not available - cannot retrieve sessions")
        
        try:
            query = client.table('study_sessions').select('*').eq('user_id', user_id).order('session_date', desc=True)
            if limit:
                query = query.limit(limit)
            response = query.execute()
            
            sessions = []
            for session_data in response.data:
                session = StudySession(
                    session_data['id'],
                    session_data['topic_id'],
                    session_data['user_id'],
                    datetime.fromisoformat(session_data['session_date']),
                    session_data['duration_minutes'],
                    session_data['confidence_before'],
                    session_data['confidence_after'],
                    session_data['notes'],
                    session_data['session_type'],
                    session_data['completed'],
                    datetime.fromisoformat(session_data['created_at'])
                )
                sessions.append(session)
            print(f" Retrieved {len(sessions)} sessions from Supabase for user {user_id}")
            return sessions
        except Exception as e:
            print(f" Error getting sessions from Supabase: {e}")
            raise Exception(f"Failed to retrieve sessions: {e}")
    
    @staticmethod
    def get_topic_sessions(topic_id, user_id):
        """Get all sessions for a specific topic"""
        # Get Supabase client dynamically
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            raise Exception("Supabase not available - cannot retrieve sessions")
        
        try:
            response = client.table('study_sessions').select('*').eq('topic_id', topic_id).eq('user_id', user_id).order('session_date', desc=True).execute()
            
            sessions = []
            for session_data in response.data:
                session = StudySession(
                    session_data['id'],
                    session_data['topic_id'],
                    session_data['user_id'],
                    datetime.fromisoformat(session_data['session_date']),
                    session_data['duration_minutes'],
                    session_data['confidence_before'],
                    session_data['confidence_after'],
                    session_data['notes'],
                    session_data['session_type'],
                    session_data['completed'],
                    datetime.fromisoformat(session_data['created_at'])
                )
                sessions.append(session)
            return sessions
        except Exception as e:
            print(f"Error getting topic sessions from Supabase: {e}")
            raise Exception(f"Failed to retrieve sessions: {e}")
    
    @staticmethod
    def get_session_by_id(session_id, user_id):
        """Get single session with user validation"""
        
        client = get_supabase_client()
        if SUPABASE_AVAILABLE and client:
            try:
                response = client.table('study_sessions').select('*').eq('id', session_id).eq('user_id', user_id).execute()
                if response.data:
                    session_data = response.data[0]
                    return StudySession(
                        session_data['id'],
                        session_data['topic_id'],
                        session_data['user_id'],
                        datetime.fromisoformat(session_data['session_date']),
                        session_data['duration_minutes'],
                        session_data['confidence_before'],
                        session_data['confidence_after'],
                        session_data['notes'],
                        session_data['session_type'],
                        session_data['completed'],
                        datetime.fromisoformat(session_data['created_at'])
                    )
                return None
            except Exception as e:
                print(f"Error getting session from Supabase: {e}")
            
                pass
        
       
        for session in _in_memory_sessions:
            if session.id == session_id and session.user_id == user_id:
                return session
        return None
    
    def update_session(self, **kwargs):
        """Update session"""
       
        client = get_supabase_client()
        if SUPABASE_AVAILABLE and client:
            try:
                data = {}
                for key, value in kwargs.items():
                    if key == 'session_date':
                        if isinstance(value, datetime):
                            data[key] = value.isoformat()
                        elif hasattr(value, 'isoformat'):  # Handle date objects
                            data[key] = value.isoformat()
                        else:
                            data[key] = value
                    else:
                        data[key] = value
                
                response = client.table('study_sessions').update(data).eq('id', self.id).eq('user_id', self.user_id).execute()
                if response.data:
                    session_data = response.data[0]
                  
                    for key, value in kwargs.items():
                        if key == 'session_date' and isinstance(value, datetime):
                            setattr(self, key, value)
                        else:
                            setattr(self, key, value)
                    return True
                return False
            except Exception as e:
                print(f"Error updating session in Supabase: {e}")
            
                pass
        
        
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            return True
        except Exception as e:
            print(f"Error updating session in memory: {e}")
            return False
    
    @staticmethod
    def delete_session(session_id, user_id):
        """Delete session"""
        
        client = get_supabase_client()
        if SUPABASE_AVAILABLE and client:
            try:
                response = client.table('study_sessions').delete().eq('id', session_id).eq('user_id', user_id).execute()
                return len(response.data) > 0
            except Exception as e:
                print(f"Error deleting session from Supabase: {e}")
                return False
        else:
            
            try:
                global _in_memory_sessions
                _in_memory_sessions = [session for session in _in_memory_sessions 
                                     if not (session.id == session_id and session.user_id == user_id)]
                return True
            except Exception as e:
                print(f"Error deleting session from memory: {e}")
                return False
    
    @staticmethod
    def get_session_stats(user_id, days=30):
        """Get session statistics for period"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        sessions = StudySession.get_user_sessions(user_id)
        period_sessions = []
        for s in sessions:
            try:
                
                session_date = s.session_date
                if isinstance(session_date, str):
                    if session_date:
                        session_date = datetime.fromisoformat(session_date).date()
                    else:
                        continue
                elif isinstance(session_date, datetime):
                    session_date = session_date.date()
                elif hasattr(session_date, 'date') and not isinstance(session_date, datetime.date):
                    session_date = session_date.date()
                
                # Convert start_date and end_date to date objects for comparison
                if isinstance(start_date, datetime):
                    start_date = start_date.date()
                if isinstance(end_date, datetime):
                    end_date = end_date.date()
                
                if session_date >= start_date and session_date <= end_date:
                    period_sessions.append(s)
            except Exception as e:
                print(f"Error processing session date: {e}")
                continue
        
        if not period_sessions:
            return {
                'total_sessions': 0,
                'total_time_minutes': 0,
                'total_time_hours': 0,
                'avg_duration': 0,
                'avg_confidence_gain': 0,
                'sessions_by_type': {},
                'confidence_trend': []
            }
        
        total_time = sum(s.duration_minutes for s in period_sessions)
        confidence_gains = [s.confidence_after - s.confidence_before for s in period_sessions if s.confidence_after and s.confidence_before]
        
        sessions_by_type = {}
        for session in period_sessions:
            sessions_by_type[session.session_type] = sessions_by_type.get(session.session_type, 0) + 1
        
        return {
            'total_sessions': len(period_sessions),
            'total_time_minutes': total_time,
            'total_time_hours': round(total_time / 60, 1),
            'avg_duration': round(total_time / len(period_sessions), 1),
            'avg_confidence_gain': round(sum(confidence_gains) / len(confidence_gains), 1) if confidence_gains else 0,
            'sessions_by_type': sessions_by_type,
            'confidence_trend': [(s.session_date.strftime('%Y-%m-%d') if hasattr(s.session_date, 'strftime') else str(s.session_date), s.confidence_after - s.confidence_before) 
                               for s in period_sessions if s.confidence_after and s.confidence_before]
        }
    
    @staticmethod
    def get_topic_progress(topic_id, user_id):
        """Calculate topic progress metrics"""
        sessions = StudySession.get_topic_sessions(topic_id, user_id)
        
        if not sessions:
            return {
                'total_sessions': 0,
                'total_time_minutes': 0,
                'total_time_hours': 0,
                'confidence_improvement': 0,
                'last_session_date': None,
                'avg_session_duration': 0,
                'completion_rate': 0
            }
        
        total_time = sum(s.duration_minutes for s in sessions)
        completed_sessions = [s for s in sessions if s.completed]
        confidence_improvements = [s.confidence_after - s.confidence_before for s in completed_sessions 
                                 if s.confidence_after and s.confidence_before]
        
        return {
            'total_sessions': len(sessions),
            'total_time_minutes': total_time,
            'total_time_hours': round(total_time / 60, 1),
            'confidence_improvement': sum(confidence_improvements) if confidence_improvements else 0,
            'last_session_date': max(s.session_date for s in sessions),
            'avg_session_duration': round(total_time / len(sessions), 1),
            'completion_rate': round(len(completed_sessions) / len(sessions) * 100, 1)
        }
    
    def calculate_confidence_gain(self):
        """Calculate confidence gain for this session"""
        if self.confidence_after and self.confidence_before:
            return self.confidence_after - self.confidence_before
        return 0
    
    @staticmethod
    def get_session_streak(user_id):
        """Calculate current study streak"""
        sessions = StudySession.get_user_sessions(user_id)
        if not sessions:
            return 0
        
        # Sort by date descending
        sessions.sort(key=lambda x: x.session_date, reverse=True)
        
        streak = 0
        current_date = datetime.utcnow().date()
        
        for session in sessions:
           
            session_date = session.session_date
            if isinstance(session_date, str):
                try:
                    session_date = datetime.fromisoformat(session_date).date()
                except:
                    continue
            elif isinstance(session_date, datetime):
                session_date = session_date.date()
            elif hasattr(session_date, 'date'):
                session_date = session_date.date()
            
            if session_date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif session_date < current_date:
                break
        
        return streak
    
    @staticmethod
    def get_weekly_study_time(user_id):
        """Get total study time this week"""
        now = datetime.utcnow()
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        sessions = StudySession.get_user_sessions(user_id)
        week_sessions = [s for s in sessions if s.session_date >= week_start]
        
        return sum(s.duration_minutes for s in week_sessions)

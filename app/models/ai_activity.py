"""
AI Activity Model for tracking user AI interactions
"""

from datetime import datetime
from typing import Dict, List, Optional
from app.models import supabase


class AIActivity:
    """Model for tracking AI activity"""
    
    def __init__(self, id: str = None, user_id: str = None, activity_type: str = None, 
                 topic_id: str = None, activity_data: Dict = None, 
                 result_summary: str = None, created_at: datetime = None):
        self.id = id
        self.user_id = user_id
        self.activity_type = activity_type
        self.topic_id = topic_id
        self.activity_data = activity_data or {}
        self.result_summary = result_summary
        self.created_at = created_at or datetime.now()
    
    @classmethod
    def create_activity(cls, user_id: str, activity_type: str, topic_id: str = None, 
                       activity_data: Dict = None, result_summary: str = None) -> 'AIActivity':
        """Create a new AI activity record"""
        try:
            activity = {
                'user_id': user_id,
                'activity_type': activity_type,
                'topic_id': topic_id,
                'activity_data': activity_data or {},
                'result_summary': result_summary
            }
            
            result = supabase.table('ai_activity').insert(activity).execute()
            
            if result.data:
                activity_data = result.data[0]
                return cls(
                    id=activity_data['id'],
                    user_id=activity_data['user_id'],
                    activity_type=activity_data['activity_type'],
                    topic_id=activity_data.get('topic_id'),
                    activity_data=activity_data.get('activity_data', {}),
                    result_summary=activity_data.get('result_summary'),
                    created_at=datetime.fromisoformat(activity_data['created_at'].replace('Z', '+00:00'))
                )
            return None
            
        except Exception as e:
            print(f"Error creating AI activity: {e}")
            return None
    
    @classmethod
    def get_recent_activity(cls, user_id: str, limit: int = 10) -> List['AIActivity']:
        """Get recent AI activity for a user"""
        try:
            result = supabase.table('ai_activity')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            activities = []
            for activity_data in result.data:
                activity = cls(
                    id=activity_data['id'],
                    user_id=activity_data['user_id'],
                    activity_type=activity_data['activity_type'],
                    topic_id=activity_data.get('topic_id'),
                    activity_data=activity_data.get('activity_data', {}),
                    result_summary=activity_data.get('result_summary'),
                    created_at=datetime.fromisoformat(activity_data['created_at'].replace('Z', '+00:00'))
                )
                activities.append(activity)
            
            return activities
            
        except Exception as e:
            print(f"Error getting recent AI activity: {e}")
            return []
    
    @classmethod
    def get_activity_by_type(cls, user_id: str, activity_type: str, limit: int = 5) -> List['AIActivity']:
        """Get AI activity by type"""
        try:
            result = supabase.table('ai_activity')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('activity_type', activity_type)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            activities = []
            for activity_data in result.data:
                activity = cls(
                    id=activity_data['id'],
                    user_id=activity_data['user_id'],
                    activity_type=activity_data['activity_type'],
                    topic_id=activity_data.get('topic_id'),
                    activity_data=activity_data.get('activity_data', {}),
                    result_summary=activity_data.get('result_summary'),
                    created_at=datetime.fromisoformat(activity_data['created_at'].replace('Z', '+00:00'))
                )
                activities.append(activity)
            
            return activities
            
        except Exception as e:
            print(f"Error getting AI activity by type: {e}")
            return []
    
    def get_activity_icon(self) -> str:
        """Get icon for activity type"""
        icons = {
            'grade_prediction': 'fas fa-crystal-ball',
            'study_plan': 'fas fa-calendar-alt',
            'concept_explanation': 'fas fa-lightbulb',
            'adaptive_quiz': 'fas fa-question-circle',
            'chat': 'fas fa-comments'
        }
        return icons.get(self.activity_type, 'fas fa-robot')
    
    def get_activity_color(self) -> str:
        """Get color for activity type"""
        colors = {
            'grade_prediction': 'text-primary',
            'study_plan': 'text-success',
            'concept_explanation': 'text-warning',
            'adaptive_quiz': 'text-info',
            'chat': 'text-secondary'
        }
        return colors.get(self.activity_type, 'text-muted')
    
    def get_activity_title(self) -> str:
        """Get title for activity type"""
        titles = {
            'grade_prediction': 'Grade Prediction',
            'study_plan': 'Study Plan Generated',
            'concept_explanation': 'Concept Explained',
            'adaptive_quiz': 'Quiz Recommendations',
            'chat': 'AI Chat'
        }
        return titles.get(self.activity_type, 'AI Activity')
    
    def get_time_ago(self) -> str:
        """Get human-readable time ago"""
        from datetime import timezone
        now = datetime.now(timezone.utc)
        if self.created_at.tzinfo is None:
            # If created_at is naive, assume it's UTC
            created_at = self.created_at.replace(tzinfo=timezone.utc)
        else:
            created_at = self.created_at
        diff = now - created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"

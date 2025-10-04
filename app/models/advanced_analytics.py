

from app.models import get_supabase_client
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json

class LearningVelocity:
    
    
    def __init__(self, user_id: str, topic_id: str = None, velocity_score: float = 0.0, 
                 learning_rate: float = 0.0, time_to_mastery: int = None, 
                 difficulty_level: str = 'beginner'):
        self.user_id = user_id
        self.topic_id = topic_id
        self.velocity_score = velocity_score
        self.learning_rate = learning_rate
        self.time_to_mastery = time_to_mastery
        self.difficulty_level = difficulty_level
        self.measurement_period_start = datetime.now() - timedelta(days=30)
        self.measurement_period_end = datetime.now()
    
    @classmethod
    def create(cls, user_id: str, topic_id: str = None, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'user_id': user_id,
            'topic_id': topic_id,
            'velocity_score': kwargs.get('velocity_score', 0.0),
            'learning_rate': kwargs.get('learning_rate', 0.0),
            'time_to_mastery': kwargs.get('time_to_mastery'),
            'difficulty_level': kwargs.get('difficulty_level', 'beginner'),
            'measurement_period_start': kwargs.get('measurement_period_start', datetime.now() - timedelta(days=30)),
            'measurement_period_end': kwargs.get('measurement_period_end', datetime.now())
        }
        
        result = client.table('learning_velocity').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def get_user_velocity(cls, user_id: str, topic_id: str = None) -> List['LearningVelocity']:
        
        client = get_supabase_client()
        
        query = client.table('learning_velocity').select('*').eq('user_id', user_id)
        if topic_id:
            query = query.eq('topic_id', topic_id)
        
        result = query.order('created_at', desc=True).execute()
        return [cls(**item) for item in result.data] if result.data else []
    
    @classmethod
    def calculate_velocity(cls, user_id: str, topic_id: str, days_back: int = 30) -> float:
        
        client = get_supabase_client()
        
        
        start_date = datetime.now() - timedelta(days=days_back)
        result = client.table('study_sessions').select('*').eq('user_id', user_id).eq('topic_id', topic_id).gte('created_at', start_date.isoformat()).execute()
        
        if not result.data:
            return 0.0
        
        total_sessions = len(result.data)
        total_time = sum(session.get('duration_minutes', 0) for session in result.data)
        avg_progress = sum(session.get('progress_percentage', 0) for session in result.data) / total_sessions
        
        if total_time == 0:
            return 0.0
        
        
        velocity = (avg_progress * 60.0) / total_time
        return min(velocity, 100.0)  

class KnowledgeRetention:
    
    
    def __init__(self, user_id: str, topic_id: str = None, retention_score: float = 0.0,
                 forgetting_curve_slope: float = 0.0, retention_period_days: int = 7,
                 last_reviewed: datetime = None, next_review_due: datetime = None,
                 mastery_level: str = 'novice'):
        self.user_id = user_id
        self.topic_id = topic_id
        self.retention_score = retention_score
        self.forgetting_curve_slope = forgetting_curve_slope
        self.retention_period_days = retention_period_days
        self.last_reviewed = last_reviewed
        self.next_review_due = next_review_due
        self.mastery_level = mastery_level
    
    @classmethod
    def create(cls, user_id: str, topic_id: str = None, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'user_id': user_id,
            'topic_id': topic_id,
            'retention_score': kwargs.get('retention_score', 0.0),
            'forgetting_curve_slope': kwargs.get('forgetting_curve_slope', -0.1),
            'retention_period_days': kwargs.get('retention_period_days', 7),
            'last_reviewed': kwargs.get('last_reviewed', datetime.now()),
            'next_review_due': kwargs.get('next_review_due', datetime.now() + timedelta(days=7)),
            'mastery_level': kwargs.get('mastery_level', 'novice')
        }
        
        result = client.table('knowledge_retention').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def get_user_retention(cls, user_id: str, topic_id: str = None) -> List['KnowledgeRetention']:
        
        client = get_supabase_client()
        
        query = client.table('knowledge_retention').select('*').eq('user_id', user_id)
        if topic_id:
            query = query.eq('topic_id', topic_id)
        
        result = query.order('created_at', desc=True).execute()
        return [cls(**item) for item in result.data] if result.data else []
    
    @classmethod
    def calculate_retention(cls, user_id: str, topic_id: str) -> float:
        
        client = get_supabase_client()
        
        
        result = client.table('study_sessions').select('created_at').eq('user_id', user_id).eq('topic_id', topic_id).order('created_at', desc=True).limit(1).execute()
        
        if not result.data:
            return 0.0
        
        last_review = datetime.fromisoformat(result.data[0]['created_at'].replace('Z', '+00:00'))
        days_since_review = (datetime.now() - last_review).days
        
        
        
        forgetting_factor = 2.718281828 ** (-days_since_review / 7.0)
        retention_score = forgetting_factor * 100.0
        
        return max(retention_score, 0.0)

class LearningEfficiency:
    
    
    def __init__(self, user_id: str, topic_id: str = None, efficiency_score: float = 0.0,
                 time_invested_minutes: int = 0, knowledge_gained_score: float = 0.0,
                 focus_score: float = 0.0, distraction_count: int = 0,
                 session_quality: float = 0.0, measurement_date: datetime = None):
        self.user_id = user_id
        self.topic_id = topic_id
        self.efficiency_score = efficiency_score
        self.time_invested_minutes = time_invested_minutes
        self.knowledge_gained_score = knowledge_gained_score
        self.focus_score = focus_score
        self.distraction_count = distraction_count
        self.session_quality = session_quality
        self.measurement_date = measurement_date or datetime.now()
    
    @classmethod
    def create(cls, user_id: str, topic_id: str = None, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'user_id': user_id,
            'topic_id': topic_id,
            'efficiency_score': kwargs.get('efficiency_score', 0.0),
            'time_invested_minutes': kwargs.get('time_invested_minutes', 0),
            'knowledge_gained_score': kwargs.get('knowledge_gained_score', 0.0),
            'focus_score': kwargs.get('focus_score', 0.0),
            'distraction_count': kwargs.get('distraction_count', 0),
            'session_quality': kwargs.get('session_quality', 0.0),
            'measurement_date': kwargs.get('measurement_date', datetime.now())
        }
        
        result = client.table('learning_efficiency').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def calculate_efficiency(cls, user_id: str, topic_id: str, session_id: str) -> float:
        
        client = get_supabase_client()
        
        
        result = client.table('study_sessions').select('*').eq('id', session_id).eq('user_id', user_id).execute()
        
        if not result.data:
            return 0.0
        
        session = result.data[0]
        duration = session.get('duration_minutes', 0)
        progress = session.get('progress_percentage', 0)
        focus_score = session.get('focus_score', 50.0)
        
        if duration == 0:
            return 0.0
        
        
        efficiency = (progress * focus_score) / duration
        return min(efficiency, 100.0)  

class LearningPath:
    
    
    def __init__(self, user_id: str, path_name: str, path_description: str = None,
                 target_skill_level: str = 'intermediate', estimated_duration_days: int = 30,
                 current_step: int = 0, total_steps: int = 10, completion_percentage: float = 0.0,
                 is_active: bool = True, ai_generated: bool = False):
        self.user_id = user_id
        self.path_name = path_name
        self.path_description = path_description
        self.target_skill_level = target_skill_level
        self.estimated_duration_days = estimated_duration_days
        self.current_step = current_step
        self.total_steps = total_steps
        self.completion_percentage = completion_percentage
        self.is_active = is_active
        self.ai_generated = ai_generated
    
    @classmethod
    def create(cls, user_id: str, path_name: str, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'user_id': user_id,
            'path_name': path_name,
            'path_description': kwargs.get('path_description'),
            'target_skill_level': kwargs.get('target_skill_level', 'intermediate'),
            'estimated_duration_days': kwargs.get('estimated_duration_days', 30),
            'current_step': kwargs.get('current_step', 0),
            'total_steps': kwargs.get('total_steps', 10),
            'completion_percentage': kwargs.get('completion_percentage', 0.0),
            'is_active': kwargs.get('is_active', True),
            'ai_generated': kwargs.get('ai_generated', False)
        }
        
        result = client.table('learning_paths').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def get_user_paths(cls, user_id: str, active_only: bool = True) -> List['LearningPath']:
        
        client = get_supabase_client()
        
        query = client.table('learning_paths').select('*').eq('user_id', user_id)
        if active_only:
            query = query.eq('is_active', True)
        
        result = query.order('created_at', desc=True).execute()
        return [cls(**item) for item in result.data] if result.data else []

class LearningPathStep:
    
    
    def __init__(self, path_id: str, step_order: int, step_title: str,
                 step_description: str = None, step_type: str = 'study',
                 topic_id: str = None, estimated_time_minutes: int = 30,
                 difficulty_level: str = 'beginner', prerequisites: List[str] = None,
                 is_completed: bool = False, completed_at: datetime = None):
        self.path_id = path_id
        self.step_order = step_order
        self.step_title = step_title
        self.step_description = step_description
        self.step_type = step_type
        self.topic_id = topic_id
        self.estimated_time_minutes = estimated_time_minutes
        self.difficulty_level = difficulty_level
        self.prerequisites = prerequisites or []
        self.is_completed = is_completed
        self.completed_at = completed_at
    
    @classmethod
    def create(cls, path_id: str, step_order: int, step_title: str, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'path_id': path_id,
            'step_order': step_order,
            'step_title': step_title,
            'step_description': kwargs.get('step_description'),
            'step_type': kwargs.get('step_type', 'study'),
            'topic_id': kwargs.get('topic_id'),
            'estimated_time_minutes': kwargs.get('estimated_time_minutes', 30),
            'difficulty_level': kwargs.get('difficulty_level', 'beginner'),
            'prerequisites': kwargs.get('prerequisites', []),
            'is_completed': kwargs.get('is_completed', False),
            'completed_at': kwargs.get('completed_at')
        }
        
        result = client.table('learning_path_steps').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def get_path_steps(cls, path_id: str) -> List['LearningPathStep']:
        
        client = get_supabase_client()
        
        result = client.table('learning_path_steps').select('*').eq('path_id', path_id).order('step_order').execute()
        return [cls(**item) for item in result.data] if result.data else []

class KnowledgeGap:
    
    
    def __init__(self, user_id: str, topic_id: str = None, gap_type: str = 'conceptual',
                 gap_severity: str = 'medium', gap_description: str = '',
                 detected_through: str = 'quiz', confidence_score: float = 0.0,
                 suggested_remediation: str = None, is_resolved: bool = False,
                 resolved_at: datetime = None):
        self.user_id = user_id
        self.topic_id = topic_id
        self.gap_type = gap_type
        self.gap_severity = gap_severity
        self.gap_description = gap_description
        self.detected_through = detected_through
        self.confidence_score = confidence_score
        self.suggested_remediation = suggested_remediation
        self.is_resolved = is_resolved
        self.resolved_at = resolved_at
    
    @classmethod
    def create(cls, user_id: str, topic_id: str = None, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'user_id': user_id,
            'topic_id': topic_id,
            'gap_type': kwargs.get('gap_type', 'conceptual'),
            'gap_severity': kwargs.get('gap_severity', 'medium'),
            'gap_description': kwargs.get('gap_description', ''),
            'detected_through': kwargs.get('detected_through', 'quiz'),
            'confidence_score': kwargs.get('confidence_score', 0.0),
            'suggested_remediation': kwargs.get('suggested_remediation'),
            'is_resolved': kwargs.get('is_resolved', False),
            'resolved_at': kwargs.get('resolved_at')
        }
        
        result = client.table('knowledge_gaps').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def detect_gaps(cls, user_id: str, topic_id: str) -> List['KnowledgeGap']:
        
        client = get_supabase_client()
        
        
        quiz_result = client.table('quiz_attempts').select('score').eq('user_id', user_id).execute()
        if not quiz_result.data:
            return []
        
        avg_score = sum(attempt['score'] for attempt in quiz_result.data) / len(quiz_result.data)
        
        
        if avg_score < 40:
            gap_severity = 'critical'
            gap_type = 'conceptual'
            gap_description = 'Critical knowledge gaps detected. Immediate remediation needed.'
        elif avg_score < 60:
            gap_severity = 'high'
            gap_type = 'practical'
            gap_description = 'Significant knowledge gaps. Focused study required.'
        elif avg_score < 80:
            gap_severity = 'medium'
            gap_type = 'theoretical'
            gap_description = 'Minor knowledge gaps. Review recommended.'
        else:
            return []  
        
        gap = cls(
            user_id=user_id,
            topic_id=topic_id,
            gap_type=gap_type,
            gap_severity=gap_severity,
            gap_description=gap_description,
            detected_through='quiz',
            confidence_score=0.8 if len(quiz_result.data) >= 3 else 0.6,
            suggested_remediation=f"Focus on {gap_type} understanding. Practice more {gap_type} problems."
        )
        
        return [gap]

class PredictiveAnalytics:
    
    
    def __init__(self, user_id: str, topic_id: str = None, prediction_type: str = 'success_probability',
                 prediction_value: float = 0.0, confidence_level: float = 0.0,
                 prediction_horizon_days: int = 7, factors_considered: List[str] = None,
                 prediction_date: datetime = None, actual_outcome: float = None,
                 accuracy_score: float = None):
        self.user_id = user_id
        self.topic_id = topic_id
        self.prediction_type = prediction_type
        self.prediction_value = prediction_value
        self.confidence_level = confidence_level
        self.prediction_horizon_days = prediction_horizon_days
        self.factors_considered = factors_considered or []
        self.prediction_date = prediction_date or datetime.now()
        self.actual_outcome = actual_outcome
        self.accuracy_score = accuracy_score
    
    @classmethod
    def create(cls, user_id: str, topic_id: str = None, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'user_id': user_id,
            'topic_id': topic_id,
            'prediction_type': kwargs.get('prediction_type', 'success_probability'),
            'prediction_value': kwargs.get('prediction_value', 0.0),
            'confidence_level': kwargs.get('confidence_level', 0.0),
            'prediction_horizon_days': kwargs.get('prediction_horizon_days', 7),
            'factors_considered': kwargs.get('factors_considered', []),
            'prediction_date': kwargs.get('prediction_date', datetime.now()),
            'actual_outcome': kwargs.get('actual_outcome'),
            'accuracy_score': kwargs.get('accuracy_score')
        }
        
        result = client.table('predictive_analytics').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def predict_success_probability(cls, user_id: str, topic_id: str, exam_date: datetime) -> float:
        
        client = get_supabase_client()
        
        
        progress_result = client.table('study_sessions').select('progress_percentage').eq('user_id', user_id).eq('topic_id', topic_id).gte('created_at', (datetime.now() - timedelta(days=7)).isoformat()).execute()
        
        if not progress_result.data:
            return 20.0  
        
        current_progress = sum(session['progress_percentage'] for session in progress_result.data) / len(progress_result.data)
        
        
        velocity = LearningVelocity.calculate_velocity(user_id, topic_id, 14)
        
        
        days_remaining = (exam_date - datetime.now()).days
        
        if days_remaining <= 0:
            return 90.0 if current_progress >= 80 else 20.0
        
        
        required_velocity = (80.0 - current_progress) / days_remaining
        
        
        if velocity >= required_velocity:
            success_probability = 85.0 + (velocity - required_velocity) * 2
        else:
            success_probability = 20.0 + (velocity / required_velocity) * 60
        
        return max(min(success_probability, 95.0), 5.0)

class StudyTimeOptimization:
    
    
    def __init__(self, user_id: str, optimal_hour: int = 9, optimal_day_of_week: int = 1,
                 productivity_score: float = 0.0, focus_duration_minutes: int = 25,
                 break_duration_minutes: int = 5, session_frequency_per_week: int = 3,
                 measurement_period_days: int = 30):
        self.user_id = user_id
        self.optimal_hour = optimal_hour
        self.optimal_day_of_week = optimal_day_of_week
        self.productivity_score = productivity_score
        self.focus_duration_minutes = focus_duration_minutes
        self.break_duration_minutes = break_duration_minutes
        self.session_frequency_per_week = session_frequency_per_week
        self.measurement_period_days = measurement_period_days
    
    @classmethod
    def create(cls, user_id: str, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'user_id': user_id,
            'optimal_hour': kwargs.get('optimal_hour', 9),
            'optimal_day_of_week': kwargs.get('optimal_day_of_week', 1),
            'productivity_score': kwargs.get('productivity_score', 0.0),
            'focus_duration_minutes': kwargs.get('focus_duration_minutes', 25),
            'break_duration_minutes': kwargs.get('break_duration_minutes', 5),
            'session_frequency_per_week': kwargs.get('session_frequency_per_week', 3),
            'measurement_period_days': kwargs.get('measurement_period_days', 30)
        }
        
        result = client.table('study_time_optimization').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def get_user_optimization(cls, user_id: str) -> Optional['StudyTimeOptimization']:
        
        client = get_supabase_client()
        
        result = client.table('study_time_optimization').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(1).execute()
        return cls(**result.data[0]) if result.data else None

class BurnoutRisk:
    
    
    def __init__(self, user_id: str, risk_level: str = 'low', risk_score: float = 0.0,
                 contributing_factors: List[str] = None, study_intensity_score: float = 0.0,
                 rest_adequacy_score: float = 0.0, stress_indicators: List[str] = None,
                 recommended_actions: List[str] = None, is_monitored: bool = True,
                 last_assessment: datetime = None):
        self.user_id = user_id
        self.risk_level = risk_level
        self.risk_score = risk_score
        self.contributing_factors = contributing_factors or []
        self.study_intensity_score = study_intensity_score
        self.rest_adequacy_score = rest_adequacy_score
        self.stress_indicators = stress_indicators or []
        self.recommended_actions = recommended_actions or []
        self.is_monitored = is_monitored
        self.last_assessment = last_assessment or datetime.now()
    
    @classmethod
    def create(cls, user_id: str, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'user_id': user_id,
            'risk_level': kwargs.get('risk_level', 'low'),
            'risk_score': kwargs.get('risk_score', 0.0),
            'contributing_factors': kwargs.get('contributing_factors', []),
            'study_intensity_score': kwargs.get('study_intensity_score', 0.0),
            'rest_adequacy_score': kwargs.get('rest_adequacy_score', 0.0),
            'stress_indicators': kwargs.get('stress_indicators', []),
            'recommended_actions': kwargs.get('recommended_actions', []),
            'is_monitored': kwargs.get('is_monitored', True),
            'last_assessment': kwargs.get('last_assessment', datetime.now())
        }
        
        result = client.table('burnout_risk').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def assess_risk(cls, user_id: str) -> 'BurnoutRisk':
        
        client = get_supabase_client()
        
        
        recent_sessions = client.table('study_sessions').select('*').eq('user_id', user_id).gte('created_at', (datetime.now() - timedelta(days=7)).isoformat()).execute()
        
        if not recent_sessions.data:
            return cls(user_id=user_id, risk_level='low', risk_score=10.0)
        
        
        total_time = sum(session['duration_minutes'] for session in recent_sessions.data)
        avg_session_length = total_time / len(recent_sessions.data)
        
        
        rest_score = 100.0 - (total_time / 60.0)  
        
        
        if avg_session_length > 120 and total_time > 20 * 60:  
            risk_level = 'high'
            risk_score = 80.0
            contributing_factors = ['long_study_sessions', 'high_weekly_hours']
            stress_indicators = ['fatigue', 'decreased_focus']
            recommended_actions = ['take_breaks', 'reduce_session_length', 'get_adequate_sleep']
        elif avg_session_length > 90 or total_time > 15 * 60:  
            risk_level = 'medium'
            risk_score = 50.0
            contributing_factors = ['moderate_intensity']
            stress_indicators = ['occasional_fatigue']
            recommended_actions = ['monitor_stress', 'take_regular_breaks']
        else:
            risk_level = 'low'
            risk_score = 20.0
            contributing_factors = []
            stress_indicators = []
            recommended_actions = ['maintain_current_pace']
        
        return cls(
            user_id=user_id,
            risk_level=risk_level,
            risk_score=risk_score,
            contributing_factors=contributing_factors,
            study_intensity_score=min(avg_session_length / 2, 100.0),
            rest_adequacy_score=max(rest_score, 0.0),
            stress_indicators=stress_indicators,
            recommended_actions=recommended_actions
        )

class GoalForecasting:
    
    
    def __init__(self, user_id: str, goal_id: str = None, goal_description: str = '',
                 target_completion_date: datetime = None, predicted_completion_date: datetime = None,
                 confidence_percentage: float = 0.0, current_progress_percentage: float = 0.0,
                 required_velocity: float = 0.0, current_velocity: float = 0.0,
                 is_on_track: bool = True, risk_factors: List[str] = None,
                 mitigation_strategies: List[str] = None):
        self.user_id = user_id
        self.goal_id = goal_id
        self.goal_description = goal_description
        self.target_completion_date = target_completion_date
        self.predicted_completion_date = predicted_completion_date
        self.confidence_percentage = confidence_percentage
        self.current_progress_percentage = current_progress_percentage
        self.required_velocity = required_velocity
        self.current_velocity = current_velocity
        self.is_on_track = is_on_track
        self.risk_factors = risk_factors or []
        self.mitigation_strategies = mitigation_strategies or []
    
    @classmethod
    def create(cls, user_id: str, goal_description: str, target_completion_date: datetime, **kwargs):
        
        client = get_supabase_client()
        
        data = {
            'user_id': user_id,
            'goal_id': kwargs.get('goal_id'),
            'goal_description': goal_description,
            'target_completion_date': target_completion_date,
            'predicted_completion_date': kwargs.get('predicted_completion_date'),
            'confidence_percentage': kwargs.get('confidence_percentage', 0.0),
            'current_progress_percentage': kwargs.get('current_progress_percentage', 0.0),
            'required_velocity': kwargs.get('required_velocity', 0.0),
            'current_velocity': kwargs.get('current_velocity', 0.0),
            'is_on_track': kwargs.get('is_on_track', True),
            'risk_factors': kwargs.get('risk_factors', []),
            'mitigation_strategies': kwargs.get('mitigation_strategies', [])
        }
        
        result = client.table('goal_forecasting').insert(data).execute()
        return cls(**data) if result.data else None
    
    @classmethod
    def forecast_goal_achievement(cls, user_id: str, goal_description: str, target_date: datetime) -> 'GoalForecasting':
        
        client = get_supabase_client()
        
        
        current_progress = 30.0  
        
        
        days_remaining = (target_date - datetime.now()).days
        
        if days_remaining <= 0:
            return cls(
                user_id=user_id,
                goal_description=goal_description,
                target_completion_date=target_date,
                predicted_completion_date=datetime.now(),
                confidence_percentage=100.0,
                current_progress_percentage=current_progress,
                is_on_track=False
            )
        
        
        required_velocity = (100.0 - current_progress) / days_remaining
        
        
        current_velocity = 2.0  
        
        
        if current_velocity > 0:
            predicted_days = (100.0 - current_progress) / current_velocity
            predicted_date = datetime.now() + timedelta(days=predicted_days)
        else:
            predicted_date = target_date + timedelta(days=30)  
        
        
        is_on_track = predicted_date <= target_date
        
        
        confidence = 80.0 if is_on_track else 40.0
        
        
        risk_factors = []
        if not is_on_track:
            risk_factors.append('insufficient_velocity')
        if days_remaining < 7:
            risk_factors.append('short_timeframe')
        
        
        mitigation_strategies = []
        if not is_on_track:
            mitigation_strategies.extend(['increase_study_time', 'improve_focus', 'seek_help'])
        
        return cls(
            user_id=user_id,
            goal_description=goal_description,
            target_completion_date=target_date,
            predicted_completion_date=predicted_date,
            confidence_percentage=confidence,
            current_progress_percentage=current_progress,
            required_velocity=required_velocity,
            current_velocity=current_velocity,
            is_on_track=is_on_track,
            risk_factors=risk_factors,
            mitigation_strategies=mitigation_strategies
        )


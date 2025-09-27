"""
AI Algorithms and Analytics for Learning Companion

This module contains algorithms for:
- Study pattern analysis
- Spaced repetition recommendations
- Confidence trend analysis
- Optimal session timing
- Topic mastery calculation
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Tuple, Optional
from app.models import Topic
from app.models.study_session import StudySession

class LearningAnalytics:
    """Main class for learning analytics and AI algorithms"""
    
    @staticmethod
    def calculate_study_streak(user_id: str) -> int:
        """Calculate current consecutive study days"""
        sessions = StudySession.get_user_sessions(user_id)
        if not sessions:
            return 0
        
        # Sort by date descending
        sessions.sort(key=lambda x: x.session_date, reverse=True)
        
        streak = 0
        current_date = datetime.utcnow().date()
        
        for session in sessions:
            session_date = session.session_date.date() if isinstance(session.session_date, datetime) else session.session_date
            if session_date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif session_date < current_date:
                break
        
        return streak
    
    @staticmethod
    def get_optimal_session_length(user_id: str, topic_id: int) -> int:
        """Suggest ideal session duration based on past performance"""
        sessions = StudySession.get_topic_sessions(topic_id, user_id)
        if not sessions:
            return 25  # Default Pomodoro time
        
        # Analyze past session durations and confidence gains
        effective_sessions = []
        for session in sessions:
            if session.completed and session.confidence_after and session.confidence_before:
                confidence_gain = session.confidence_after - session.confidence_before
                if confidence_gain > 0:  # Only consider sessions with positive gains
                    effective_sessions.append({
                        'duration': session.duration_minutes,
                        'confidence_gain': confidence_gain,
                        'efficiency': confidence_gain / session.duration_minutes
                    })
        
        if not effective_sessions:
            return 25
        
        # Find the duration with highest average efficiency
        duration_efficiency = {}
        for session in effective_sessions:
            duration = session['duration']
            if duration not in duration_efficiency:
                duration_efficiency[duration] = []
            duration_efficiency[duration].append(session['efficiency'])
        

        best_duration = 25
        best_efficiency = 0
        
        for duration, efficiencies in duration_efficiency.items():
            avg_efficiency = sum(efficiencies) / len(efficiencies)
            if avg_efficiency > best_efficiency:
                best_efficiency = avg_efficiency
                best_duration = duration
        
        
        if best_duration <= 15:
            return 15
        elif best_duration <= 25:
            return 25
        elif best_duration <= 45:
            return 45
        else:
            return 60
    
    @staticmethod
    def calculate_confidence_trends(user_id: str, topic_id: int) -> Dict:
        """Track confidence improvement over time"""
        sessions = StudySession.get_topic_sessions(topic_id, user_id)
        if not sessions:
            return {
                'trend': 'stable',
                'improvement_rate': 0,
                'data_points': [],
                'prediction': 'insufficient_data'
            }
        
        
        sessions.sort(key=lambda x: x.session_date)
        
        confidence_data = []
        for session in sessions:
            if session.completed and session.confidence_after:
                confidence_data.append({
                    'date': session.session_date,
                    'confidence': session.confidence_after,
                    'session_type': session.session_type
                })
        
        if len(confidence_data) < 2:
            return {
                'trend': 'stable',
                'improvement_rate': 0,
                'data_points': confidence_data,
                'prediction': 'insufficient_data'
            }
        
        # Calculate trend
        first_confidence = confidence_data[0]['confidence']
        last_confidence = confidence_data[-1]['confidence']
        total_improvement = last_confidence - first_confidence
        
        # Calculate improvement rate (confidence points per session)
        improvement_rate = total_improvement / len(confidence_data)
        
        # Determine trend
        if improvement_rate > 0.5:
            trend = 'improving'
        elif improvement_rate < -0.5:
            trend = 'declining'
        else:
            trend = 'stable'
        
        # Predict next confidence level
        if trend == 'improving' and len(confidence_data) >= 3:
            recent_improvement = (confidence_data[-1]['confidence'] - confidence_data[-3]['confidence']) / 2
            predicted_confidence = min(10, confidence_data[-1]['confidence'] + recent_improvement)
        elif trend == 'declining':
            predicted_confidence = max(1, confidence_data[-1]['confidence'] - 0.5)
        else:
            predicted_confidence = confidence_data[-1]['confidence']
        
        return {
            'trend': trend,
            'improvement_rate': round(improvement_rate, 2),
            'data_points': confidence_data,
            'prediction': round(predicted_confidence, 1),
            'total_improvement': total_improvement
        }
    
    @staticmethod
    def get_study_pattern_insights(user_id: str) -> Dict:
        """Analyze when user studies most effectively"""
        sessions = StudySession.get_user_sessions(user_id)
        if not sessions:
            return {
                'best_time': 'insufficient_data',
                'best_day': 'insufficient_data',
                'productivity_pattern': 'insufficient_data',
                'recommendations': []
            }
        
        # Analyze by time of day
        time_analysis = {}
        day_analysis = {}
        
        for session in sessions:
            if session.completed and session.confidence_after and session.confidence_before:
                session_date = session.session_date
                if isinstance(session_date, str):
                    session_date = datetime.fromisoformat(session_date)
                
                hour = session_date.hour
                day_of_week = session_date.strftime('%A')
                
                confidence_gain = session.confidence_after - session.confidence_before
                
                # Time analysis
                if hour not in time_analysis:
                    time_analysis[hour] = {'total_gain': 0, 'count': 0}
                time_analysis[hour]['total_gain'] += confidence_gain
                time_analysis[hour]['count'] += 1
                
                # Day analysis
                if day_of_week not in day_analysis:
                    day_analysis[day_of_week] = {'total_gain': 0, 'count': 0}
                day_analysis[day_of_week]['total_gain'] += confidence_gain
                day_analysis[day_of_week]['count'] += 1
        
        # Find best time
        best_time = 'insufficient_data'
        best_time_score = -999
        
        for hour, data in time_analysis.items():
            if data['count'] >= 2:  # Need at least 2 sessions for reliability
                avg_gain = data['total_gain'] / data['count']
                if avg_gain > best_time_score:
                    best_time_score = avg_gain
                    if hour < 12:
                        best_time = f"{hour}:00 AM"
                    else:
                        best_time = f"{hour-12}:00 PM" if hour > 12 else "12:00 PM"
        
        # Find best day
        best_day = 'insufficient_data'
        best_day_score = -999
        
        for day, data in day_analysis.items():
            if data['count'] >= 2:
                avg_gain = data['total_gain'] / data['count']
                if avg_gain > best_day_score:
                    best_day_score = avg_gain
                    best_day = day
        
        # Generate recommendations
        recommendations = []
        if best_time != 'insufficient_data':
            recommendations.append(f"Schedule study sessions around {best_time} for optimal learning")
        if best_day != 'insufficient_data':
            recommendations.append(f"Focus intensive study on {best_day}s")
        
        if not recommendations:
            recommendations.append("Continue studying regularly to identify your optimal learning patterns")
        
        return {
            'best_time': best_time,
            'best_day': best_day,
            'productivity_pattern': 'morning' if best_time != 'insufficient_data' and 'AM' in best_time else 'evening',
            'recommendations': recommendations,
            'time_analysis': time_analysis,
            'day_analysis': day_analysis
        }
    
    @staticmethod
    def recommend_next_session_date(topic_id: int, user_id: str) -> datetime:
        """Spaced repetition algorithm to recommend next study date"""
        sessions = StudySession.get_topic_sessions(topic_id, user_id)
        if not sessions:
            return datetime.utcnow() + timedelta(days=1)
        
        # Sort sessions by date
        sessions.sort(key=lambda x: x.session_date, reverse=True)
        last_session = sessions[0]
        
        # Calculate confidence level from last session
        if last_session.confidence_after:
            confidence_level = last_session.confidence_after
        else:
            confidence_level = 5  # Default
        
        # Spaced repetition intervals based on confidence
        if confidence_level >= 8:
            # High confidence - review in 1 week
            interval_days = 7
        elif confidence_level >= 6:
            # Medium confidence - review in 3 days
            interval_days = 3
        elif confidence_level >= 4:
            # Low confidence - review tomorrow
            interval_days = 1
        else:
            # Very low confidence - review today or tomorrow
            interval_days = 0
        
        # Calculate next session date
        last_session_date = last_session.session_date
        if isinstance(last_session_date, str):
            last_session_date = datetime.fromisoformat(last_session_date)
        
        next_session_date = last_session_date + timedelta(days=interval_days)
        
        # Don't recommend past dates
        if next_session_date.date() < datetime.utcnow().date():
            next_session_date = datetime.utcnow() + timedelta(days=1)
        
        return next_session_date
    
    @staticmethod
    def get_topic_mastery_level(topic_id: int, user_id: str) -> Dict:
        """Calculate current mastery level (1-5) for a topic"""
        sessions = StudySession.get_topic_sessions(topic_id, user_id)
        if not sessions:
            return {
                'level': 1,
                'description': 'Beginner',
                'progress_percentage': 0,
                'next_milestone': 'Complete your first study session'
            }
        
        # Calculate mastery based on multiple factors
        total_sessions = len(sessions)
        completed_sessions = len([s for s in sessions if s.completed])
        total_study_time = sum(s.duration_minutes for s in sessions if s.completed)
        
        # Get latest confidence level
        latest_confidence = 1
        if sessions:
            latest_session = max(sessions, key=lambda x: x.session_date)
            if latest_session.confidence_after:
                latest_confidence = latest_session.confidence_after
        
        # Calculate mastery score (0-100)
        session_score = min(40, (completed_sessions * 4))  # Max 40 points for sessions
        time_score = min(30, (total_study_time / 10))  # Max 30 points for time (300+ minutes = 30 points)
        confidence_score = min(30, (latest_confidence * 3))  # Max 30 points for confidence
        
        mastery_score = session_score + time_score + confidence_score
        
        # Determine mastery level
        if mastery_score >= 80:
            level = 5
            description = 'Expert'
            next_milestone = 'Maintain expertise with regular reviews'
        elif mastery_score >= 60:
            level = 4
            description = 'Advanced'
            next_milestone = 'Focus on advanced applications'
        elif mastery_score >= 40:
            level = 3
            description = 'Intermediate'
            next_milestone = 'Practice with real-world examples'
        elif mastery_score >= 20:
            level = 2
            description = 'Novice'
            next_milestone = 'Build foundational understanding'
        else:
            level = 1
            description = 'Beginner'
            next_milestone = 'Complete more study sessions'
        
        return {
            'level': level,
            'description': description,
            'progress_percentage': min(100, mastery_score),
            'next_milestone': next_milestone,
            'mastery_score': mastery_score,
            'factors': {
                'sessions': session_score,
                'time': time_score,
                'confidence': confidence_score
            }
        }
    
    @staticmethod
    def get_learning_recommendations(user_id: str) -> List[Dict]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        # Get all user topics
        topics = Topic.get_all_by_user(user_id)
        if not topics:
            recommendations.append({
                'type': 'setup',
                'priority': 'high',
                'title': 'Create Your First Topic',
                'description': 'Start your learning journey by creating a topic to study',
                'action': 'create_topic'
            })
            return recommendations
        
        # Analyze each topic
        for topic in topics:
            mastery = LearningAnalytics.get_topic_mastery_level(topic.id, user_id)
            next_session_date = LearningAnalytics.recommend_next_session_date(topic.id, user_id)
            confidence_trend = LearningAnalytics.calculate_confidence_trends(user_id, topic.id)
            
            # Generate topic-specific recommendations
            if mastery['level'] == 1:
                recommendations.append({
                    'type': 'study',
                    'priority': 'high',
                    'title': f'Start Learning {topic.title}',
                    'description': f'Begin your journey with {topic.title}. {mastery["next_milestone"]}',
                    'action': 'start_session',
                    'topic_id': topic.id
                })
            elif mastery['level'] <= 3 and confidence_trend['trend'] == 'declining':
                recommendations.append({
                    'type': 'review',
                    'priority': 'high',
                    'title': f'Review {topic.title}',
                    'description': f'Your confidence in {topic.title} is declining. Time for a review session!',
                    'action': 'start_session',
                    'topic_id': topic.id
                })
            elif next_session_date.date() <= datetime.utcnow().date():
                recommendations.append({
                    'type': 'spaced_repetition',
                    'priority': 'medium',
                    'title': f'Review {topic.title}',
                    'description': f'Based on spaced repetition, it\'s time to review {topic.title}',
                    'action': 'start_session',
                    'topic_id': topic.id
                })
        
        # Add general recommendations
        study_streak = LearningAnalytics.calculate_study_streak(user_id)
        if study_streak == 0:
            recommendations.append({
                'type': 'motivation',
                'priority': 'high',
                'title': 'Start Your Study Streak',
                'description': 'Begin a daily study habit to build momentum',
                'action': 'start_session'
            })
        elif study_streak < 7:
            recommendations.append({
                'type': 'motivation',
                'priority': 'medium',
                'title': f'Keep Your {study_streak}-Day Streak Going',
                'description': f'Great job! You\'ve studied for {study_streak} days in a row. Keep it up!',
                'action': 'start_session'
            })
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return recommendations[:5]      
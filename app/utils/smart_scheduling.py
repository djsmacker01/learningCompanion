"""
Smart Study Scheduling and Reminder Engine
"""

import json
from datetime import datetime, time, timedelta
from typing import List, Dict, Optional, Any, Tuple
from app.models.reminders import (
    StudyReminderPreferences, StudyReminder, StudySchedule, 
    OptimalStudyTime, StudyPattern
)
from app.models.study_session import StudySession
from app.models import Topic


class SmartSchedulingEngine:
    """Engine for intelligent study scheduling and reminders"""
    
    def __init__(self):
        self.timezone = 'UTC'  # Default timezone
    
    def analyze_study_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's study patterns to provide insights"""
        try:
            # Get user's study sessions
            sessions = StudySession.get_user_sessions(user_id, limit=100)
            
            if not sessions:
                return self._get_default_patterns()
            
            # Analyze patterns
            patterns = {
                'peak_hours': self._analyze_peak_hours(sessions),
                'best_days': self._analyze_best_days(sessions),
                'session_duration': self._analyze_session_duration(sessions),
                'topic_preferences': self._analyze_topic_preferences(sessions),
                'confidence_trends': self._analyze_confidence_trends(sessions),
                'study_consistency': self._analyze_study_consistency(sessions)
            }
            
            # Update patterns in database
            for pattern_type, pattern_data in patterns.items():
                StudyPattern.update_pattern(
                    user_id=user_id,
                    pattern_type=pattern_type,
                    pattern_data=pattern_data,
                    confidence_score=pattern_data.get('confidence', 0.5),
                    sample_size=len(sessions)
                )
            
            return patterns
            
        except Exception as e:
            print(f"Error analyzing study patterns: {e}")
            return self._get_default_patterns()
    
    def suggest_optimal_study_times(self, user_id: str, days_ahead: int = 7) -> List[OptimalStudyTime]:
        """Suggest optimal study times for the next few days"""
        try:
            # Get user's study patterns
            patterns = self.analyze_study_patterns(user_id)
            
            # Get user's preferences
            preferences = StudyReminderPreferences.get_or_create_preferences(user_id)
            
            suggestions = []
            current_date = datetime.now().date()
            
            for day_offset in range(days_ahead):
                target_date = current_date + timedelta(days=day_offset)
                
                # Skip if it's not a preferred day
                if not self._is_preferred_day(target_date, preferences):
                    continue
                
                # Get optimal times for this day
                day_suggestions = self._get_optimal_times_for_day(
                    user_id, target_date, patterns, preferences
                )
                suggestions.extend(day_suggestions)
            
            # Sort by confidence score
            suggestions.sort(key=lambda x: x.confidence_score, reverse=True)
            
            return suggestions[:10]  # Return top 10 suggestions
            
        except Exception as e:
            print(f"Error suggesting optimal study times: {e}")
            return []
    
    def create_smart_reminders(self, user_id: str, study_goal_minutes: int = 30) -> List[StudyReminder]:
        """Create smart reminders based on user patterns and preferences"""
        try:
            # Get user preferences
            preferences = StudyReminderPreferences.get_or_create_preferences(user_id)
            
            if not preferences.is_enabled:
                return []
            
            # Get optimal study times
            optimal_times = self.suggest_optimal_study_times(user_id, days_ahead=7)
            
            reminders = []
            
            for optimal_time in optimal_times[:5]:  # Create reminders for top 5 suggestions
                # Create reminder 15 minutes before optimal time
                reminder_time = optimal_time.suggested_time - timedelta(minutes=preferences.advance_notice_minutes)
                
                # Skip if reminder time is in the past
                if reminder_time <= datetime.now():
                    continue
                
                # Create reminder
                reminder = StudyReminder.create_reminder(
                    user_id=user_id,
                    title=f"Study Time: {optimal_time.session_type.title()}",
                    scheduled_time=reminder_time,
                    message=f"Optimal study time detected! {optimal_time.reasoning}",
                    reminder_type='study',
                    reminder_method=preferences.reminder_methods[0] if preferences.reminder_methods else 'email',
                    topic_id=optimal_time.topic_id,
                    session_type=optimal_time.session_type,
                    priority='medium'
                )
                
                if reminder:
                    reminders.append(reminder)
            
            return reminders
            
        except Exception as e:
            print(f"Error creating smart reminders: {e}")
            return []
    
    def schedule_study_session(self, user_id: str, topic_id: str = None, 
                             session_type: str = 'review', duration_minutes: int = 30) -> StudySchedule:
        """Schedule a study session at an optimal time"""
        try:
            # Get optimal study times
            optimal_times = self.suggest_optimal_study_times(user_id, days_ahead=3)
            
            if not optimal_times:
                # Fallback to next available time
                start_time = datetime.now() + timedelta(hours=1)
                end_time = start_time + timedelta(minutes=duration_minutes)
            else:
                # Use the best optimal time
                best_time = optimal_times[0]
                start_time = best_time.suggested_time
                end_time = start_time + timedelta(minutes=duration_minutes)
            
            # Get topic title
            topic_title = "General Study"
            if topic_id:
                topic = Topic.get_by_id(topic_id)
                if topic:
                    topic_title = topic.title
            
            # Create schedule
            schedule = StudySchedule.create_schedule(
                user_id=user_id,
                title=f"{session_type.title()} Session: {topic_title}",
                scheduled_start=start_time,
                scheduled_end=end_time,
                topic_id=topic_id,
                session_type=session_type,
                description=f"Scheduled {session_type} session for {duration_minutes} minutes",
                priority='medium'
            )
            
            return schedule
            
        except Exception as e:
            print(f"Error scheduling study session: {e}")
            return None
    
    def _analyze_peak_hours(self, sessions: List) -> Dict[str, Any]:
        """Analyze when user is most productive"""
        if not sessions:
            return {'peak_hours': [9, 14, 20], 'confidence': 0.3}
        
        hour_counts = {}
        total_sessions = len(sessions)
        
        for session in sessions:
            if hasattr(session, 'created_at') and session.created_at:
                try:
                    if isinstance(session.created_at, str):
                        session_time = datetime.fromisoformat(session.created_at.replace('Z', '+00:00'))
                    else:
                        session_time = session.created_at
                    
                    hour = session_time.hour
                    hour_counts[hour] = hour_counts.get(hour, 0) + 1
                except:
                    continue
        
        if not hour_counts:
            return {'peak_hours': [9, 14, 20], 'confidence': 0.3}
        
        # Find peak hours (hours with most sessions)
        sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        peak_hours = [hour for hour, count in sorted_hours[:3]]
        
        # Calculate confidence based on data distribution
        max_count = max(hour_counts.values())
        confidence = min(0.9, max_count / total_sessions * 3)
        
        return {
            'peak_hours': peak_hours,
            'hour_distribution': hour_counts,
            'confidence': confidence
        }
    
    def _analyze_best_days(self, sessions: List) -> Dict[str, Any]:
        """Analyze which days user studies most effectively"""
        if not sessions:
            return {'best_days': ['Monday', 'Wednesday', 'Friday'], 'confidence': 0.3}
        
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = {day: 0 for day in day_names}
        day_confidence = {day: [] for day in day_names}
        
        for session in sessions:
            if hasattr(session, 'created_at') and session.created_at:
                try:
                    if isinstance(session.created_at, str):
                        session_time = datetime.fromisoformat(session.created_at.replace('Z', '+00:00'))
                    else:
                        session_time = session.created_at
                    
                    day_name = day_names[session_time.weekday()]
                    day_counts[day_name] += 1
                    
                    # Track confidence gains for each day
                    if hasattr(session, 'confidence_after') and session.confidence_after:
                        day_confidence[day_name].append(session.confidence_after)
                except:
                    continue
        
        # Find best days based on session count and average confidence
        day_scores = {}
        for day in day_names:
            count = day_counts[day]
            avg_confidence = sum(day_confidence[day]) / len(day_confidence[day]) if day_confidence[day] else 0
            day_scores[day] = count * (1 + avg_confidence / 10)  # Weight by confidence
        
        sorted_days = sorted(day_scores.items(), key=lambda x: x[1], reverse=True)
        best_days = [day for day, score in sorted_days[:3] if score > 0]
        
        if not best_days:
            best_days = ['Monday', 'Wednesday', 'Friday']
        
        confidence = min(0.9, len([s for s in sessions if s]) / 10)
        
        return {
            'best_days': best_days,
            'day_distribution': day_counts,
            'day_confidence': {day: sum(conf) / len(conf) if conf else 0 for day, conf in day_confidence.items()},
            'confidence': confidence
        }
    
    def _analyze_session_duration(self, sessions: List) -> Dict[str, Any]:
        """Analyze optimal session duration"""
        if not sessions:
            return {'optimal_duration': 30, 'confidence': 0.3}
        
        durations = []
        for session in sessions:
            if hasattr(session, 'duration_minutes') and session.duration_minutes:
                durations.append(session.duration_minutes)
        
        if not durations:
            return {'optimal_duration': 30, 'confidence': 0.3}
        
        # Calculate optimal duration (median of successful sessions)
        durations.sort()
        optimal_duration = durations[len(durations) // 2]
        
        # Confidence based on consistency
        avg_duration = sum(durations) / len(durations)
        variance = sum((d - avg_duration) ** 2 for d in durations) / len(durations)
        confidence = max(0.3, 1 - (variance / (avg_duration ** 2)))
        
        return {
            'optimal_duration': optimal_duration,
            'average_duration': avg_duration,
            'duration_range': [min(durations), max(durations)],
            'confidence': confidence
        }
    
    def _analyze_topic_preferences(self, sessions: List) -> Dict[str, Any]:
        """Analyze which topics user studies most effectively"""
        if not sessions:
            return {'preferred_topics': [], 'confidence': 0.3}
        
        topic_performance = {}
        
        for session in sessions:
            if hasattr(session, 'topic_id') and session.topic_id:
                topic_id = session.topic_id
                if topic_id not in topic_performance:
                    topic_performance[topic_id] = {
                        'sessions': 0,
                        'total_confidence': 0,
                        'total_duration': 0
                    }
                
                topic_performance[topic_id]['sessions'] += 1
                if hasattr(session, 'confidence_after') and session.confidence_after:
                    topic_performance[topic_id]['total_confidence'] += session.confidence_after
                if hasattr(session, 'duration_minutes') and session.duration_minutes:
                    topic_performance[topic_id]['total_duration'] += session.duration_minutes
        
        # Calculate topic scores
        topic_scores = {}
        for topic_id, data in topic_performance.items():
            avg_confidence = data['total_confidence'] / data['sessions'] if data['sessions'] > 0 else 0
            avg_duration = data['total_duration'] / data['sessions'] if data['sessions'] > 0 else 0
            topic_scores[topic_id] = data['sessions'] * (1 + avg_confidence / 10) * (1 + avg_duration / 60)
        
        # Get top topics
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        preferred_topics = [topic_id for topic_id, score in sorted_topics[:5]]
        
        confidence = min(0.9, len(sessions) / 20)
        
        return {
            'preferred_topics': preferred_topics,
            'topic_scores': topic_scores,
            'confidence': confidence
        }
    
    def _analyze_confidence_trends(self, sessions: List) -> Dict[str, Any]:
        """Analyze confidence improvement trends"""
        if not sessions:
            return {'trend': 'stable', 'confidence': 0.3}
        
        confidence_gains = []
        for session in sessions:
            if (hasattr(session, 'confidence_before') and session.confidence_before and
                hasattr(session, 'confidence_after') and session.confidence_after):
                gain = session.confidence_after - session.confidence_before
                confidence_gains.append(gain)
        
        if not confidence_gains:
            return {'trend': 'stable', 'confidence': 0.3}
        
        avg_gain = sum(confidence_gains) / len(confidence_gains)
        
        if avg_gain > 0.5:
            trend = 'improving'
        elif avg_gain < -0.5:
            trend = 'declining'
        else:
            trend = 'stable'
        
        confidence = min(0.9, len(confidence_gains) / 10)
        
        return {
            'trend': trend,
            'average_gain': avg_gain,
            'confidence': confidence
        }
    
    def _analyze_study_consistency(self, sessions: List) -> Dict[str, Any]:
        """Analyze study consistency patterns"""
        if not sessions:
            return {'consistency_score': 0.3, 'confidence': 0.3}
        
        # Calculate study streak
        current_streak = 0
        max_streak = 0
        last_study_date = None
        
        for session in sessions:
            if hasattr(session, 'created_at') and session.created_at:
                try:
                    if isinstance(session.created_at, str):
                        session_date = datetime.fromisoformat(session.created_at.replace('Z', '+00:00')).date()
                    else:
                        session_date = session.created_at.date()
                    
                    if last_study_date is None:
                        current_streak = 1
                    elif (session_date - last_study_date).days == 1:
                        current_streak += 1
                    elif (session_date - last_study_date).days > 1:
                        max_streak = max(max_streak, current_streak)
                        current_streak = 1
                    
                    last_study_date = session_date
                except:
                    continue
        
        max_streak = max(max_streak, current_streak)
        
        # Calculate consistency score
        total_days = (datetime.now().date() - min(session.created_at.date() for session in sessions if hasattr(session, 'created_at'))).days + 1
        study_days = len(set(session.created_at.date() for session in sessions if hasattr(session, 'created_at')))
        consistency_score = study_days / total_days if total_days > 0 else 0
        
        confidence = min(0.9, len(sessions) / 20)
        
        return {
            'consistency_score': consistency_score,
            'current_streak': current_streak,
            'max_streak': max_streak,
            'study_days': study_days,
            'total_days': total_days,
            'confidence': confidence
        }
    
    def _get_default_patterns(self) -> Dict[str, Any]:
        """Get default patterns when no data is available"""
        return {
            'peak_hours': {'peak_hours': [9, 14, 20], 'confidence': 0.3},
            'best_days': {'best_days': ['Monday', 'Wednesday', 'Friday'], 'confidence': 0.3},
            'session_duration': {'optimal_duration': 30, 'confidence': 0.3},
            'topic_preferences': {'preferred_topics': [], 'confidence': 0.3},
            'confidence_trends': {'trend': 'stable', 'confidence': 0.3},
            'study_consistency': {'consistency_score': 0.3, 'confidence': 0.3}
        }
    
    def _is_preferred_day(self, target_date, preferences) -> bool:
        """Check if a date is a preferred study day"""
        if not preferences.days_of_week:
            return True
        
        # Convert date to weekday (1=Monday, 7=Sunday)
        weekday = target_date.weekday() + 1
        return weekday in preferences.days_of_week
    
    def _get_optimal_times_for_day(self, user_id: str, target_date, patterns: Dict[str, Any], 
                                  preferences) -> List[OptimalStudyTime]:
        """Get optimal study times for a specific day"""
        suggestions = []
        
        # Get peak hours from patterns
        peak_hours = patterns.get('peak_hours', {}).get('peak_hours', [9, 14, 20])
        confidence = patterns.get('peak_hours', {}).get('confidence', 0.5)
        
        # Get user's topics for context
        topics = Topic.get_all_by_user(user_id)
        
        for hour in peak_hours:
            # Create datetime for this hour
            suggested_time = datetime.combine(target_date, time(hour, 0))
            
            # Skip if time is in the past
            if suggested_time <= datetime.now():
                continue
            
            # Create reasoning
            reasoning = f"Based on your study patterns, {hour}:00 is one of your most productive hours."
            
            # Create factors
            factors = {
                'peak_hour': hour,
                'pattern_confidence': confidence,
                'day_of_week': target_date.strftime('%A'),
                'preferred_time': hour in [9, 14, 20]
            }
            
            # Create suggestion for each topic (if any)
            if topics:
                for topic in topics[:3]:  # Limit to top 3 topics
                    suggestion = OptimalStudyTime.create_suggestion(
                        user_id=user_id,
                        suggested_time=suggested_time,
                        confidence_score=confidence,
                        reasoning=reasoning,
                        factors=factors,
                        topic_id=topic.id,
                        session_type='review'
                    )
                    if suggestion:
                        suggestions.append(suggestion)
            else:
                # Create general suggestion
                suggestion = OptimalStudyTime.create_suggestion(
                    user_id=user_id,
                    suggested_time=suggested_time,
                    confidence_score=confidence,
                    reasoning=reasoning,
                    factors=factors,
                    session_type='review'
                )
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions

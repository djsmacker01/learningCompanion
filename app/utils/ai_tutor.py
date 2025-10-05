"""
Advanced AI Tutor System
Enhanced AI-powered study companion with personalized recommendations
"""

import openai
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
from app.models.quiz import QuizAttempt
from app.models import Topic
from dotenv import load_dotenv

load_dotenv()

class AITutor:
    """Advanced AI-powered study companion"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.client = self._get_openai_client()
        self.supabase = get_supabase_client() if SUPABASE_AVAILABLE else None
    
    def _get_openai_client(self):
        """Get OpenAI client with error handling"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return None
        try:
            return openai.OpenAI(api_key=api_key)
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            return None
    
    def get_personalized_study_recommendations(self) -> Dict:
        """Get personalized study recommendations based on user's learning patterns"""
        try:
            # Get user's learning data
            learning_data = self._get_user_learning_data()
            
            if not learning_data:
                return self._get_default_recommendations()
            
            # Build personalized prompt
            prompt = self._build_recommendation_prompt(learning_data)
            
            # Get AI recommendations
            recommendations = self._call_ai_for_recommendations(prompt)
            
            # Save recommendations for tracking
            self._save_recommendations(recommendations)
            
            return {
                'recommendations': recommendations,
                'data_analysis': learning_data['summary'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting personalized recommendations: {e}")
            return self._get_default_recommendations()
    
    def generate_study_plan(self, topic_id: str, target_grade: str = None, time_available: int = None) -> Dict:
        """Generate a personalized study plan for a specific topic"""
        try:
            # Get topic information
            topic = Topic.get_topic_by_id(topic_id, self.user_id)
            if not topic:
                return {'error': 'Topic not found'}
            
            # Get user's performance on this topic
            topic_performance = self._get_topic_performance(topic_id)
            
            # Build study plan prompt
            prompt = self._build_study_plan_prompt(topic, topic_performance, target_grade, time_available)
            
            # Get AI-generated study plan
            study_plan = self._call_ai_for_study_plan(prompt)
            
            # Save study plan
            self._save_study_plan(topic_id, study_plan)
            
            return {
                'study_plan': study_plan,
                'topic': {
                    'id': topic.id,
                    'title': topic.title,
                    'description': topic.description
                },
                'performance': topic_performance,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating study plan: {e}")
            return {'error': 'Failed to generate study plan'}
    
    def explain_concept_with_ai(self, concept: str, topic_id: str = None, explanation_level: str = 'intermediate') -> Dict:
        """Enhanced concept explanation with adaptive difficulty"""
        try:
            # Get topic context if provided
            topic_context = ""
            if topic_id:
                topic = Topic.get_topic_by_id(topic_id, self.user_id)
                if topic:
                    topic_context = f"Topic: {topic.title}\nDescription: {topic.description}"
            
            # Get user's learning style and preferences
            learning_profile = self._get_user_learning_profile()
            
            # Build explanation prompt
            prompt = self._build_explanation_prompt(concept, topic_context, explanation_level, learning_profile)
            
            # Get AI explanation
            explanation = self._call_ai_for_explanation(prompt)
            
            # Save explanation for future reference
            self._save_explanation(concept, explanation, topic_id)
            
            return {
                'concept': concept,
                'explanation': explanation,
                'level': explanation_level,
                'learning_style': learning_profile.get('preferred_style', 'visual'),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error explaining concept: {e}")
            return {'error': 'Failed to explain concept'}
    
    def predict_grade(self, topic_id: str, exam_date: str = None) -> Dict:
        """Predict user's likely grade based on current performance"""
        try:
            # Get topic performance data
            performance_data = self._get_topic_performance(topic_id)
            
            # Get recent quiz scores
            recent_scores = self._get_recent_quiz_scores(topic_id)
            
            # Calculate learning velocity
            learning_velocity = self._calculate_learning_velocity(topic_id)
            
            # Build prediction prompt
            prompt = self._build_grade_prediction_prompt(performance_data, recent_scores, learning_velocity, exam_date)
            
            # Get AI prediction
            prediction = self._call_ai_for_prediction(prompt)
            
            # Save prediction for tracking
            self._save_grade_prediction(topic_id, prediction, exam_date)
            
            return {
                'topic_id': topic_id,
                'predicted_grade': prediction.get('grade', 'Unknown'),
                'confidence': prediction.get('confidence', 0),
                'recommendations': prediction.get('recommendations', []),
                'performance_analysis': performance_data,
                'learning_velocity': learning_velocity,
                'exam_date': exam_date,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error predicting grade: {e}")
            return {'error': 'Failed to predict grade'}
    
    def detect_learning_style(self) -> Dict:
        """Detect user's learning style based on their study patterns"""
        try:
            # Analyze user's study patterns
            study_patterns = self._analyze_study_patterns()
            
            # Build learning style detection prompt
            prompt = self._build_learning_style_prompt(study_patterns)
            
            # Get AI analysis
            learning_style = self._call_ai_for_learning_style(prompt)
            
            # Save learning style
            self._save_learning_style(learning_style)
            
            return {
                'learning_style': learning_style,
                'confidence': learning_style.get('confidence', 0),
                'recommendations': learning_style.get('recommendations', []),
                'study_patterns': study_patterns,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error detecting learning style: {e}")
            return {'error': 'Failed to detect learning style'}
    
    def get_adaptive_quiz_recommendations(self, topic_id: str) -> Dict:
        """Get adaptive quiz recommendations based on user's performance"""
        try:
            # Get topic performance
            performance = self._get_topic_performance(topic_id)
            
            # Get weak areas
            weak_areas = self._identify_weak_areas(topic_id)
            
            # Build adaptive recommendations prompt
            prompt = self._build_adaptive_quiz_prompt(performance, weak_areas)
            
            # Get AI recommendations
            recommendations = self._call_ai_for_adaptive_quiz(prompt)
            
            return {
                'topic_id': topic_id,
                'recommendations': recommendations,
                'weak_areas': weak_areas,
                'performance': performance,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting adaptive quiz recommendations: {e}")
            return {'error': 'Failed to get quiz recommendations'}
    
    # Helper methods
    def _get_user_learning_data(self) -> Dict:
        """Get comprehensive user learning data"""
        if not self.supabase:
            return None
        
        try:
            # Get recent study sessions
            sessions = self.supabase.table('study_sessions').select('*').eq('user_id', self.user_id).gte('session_date', (datetime.now() - timedelta(days=30)).isoformat()).execute()
            
            # Get quiz attempts
            quiz_attempts = self.supabase.table('quiz_attempts').select('*').eq('user_id', self.user_id).gte('created_at', (datetime.now() - timedelta(days=30)).isoformat()).execute()
            
            # Get topics
            topics = self.supabase.table('topics').select('*').eq('user_id', self.user_id).eq('is_active', True).execute()
            
            return {
                'sessions': sessions.data if sessions.data else [],
                'quiz_attempts': quiz_attempts.data if quiz_attempts.data else [],
                'topics': topics.data if topics.data else [],
                'summary': self._analyze_learning_data(sessions.data, quiz_attempts.data, topics.data)
            }
            
        except Exception as e:
            print(f"Error getting user learning data: {e}")
            return None
    
    def _analyze_learning_data(self, sessions: List, quiz_attempts: List, topics: List) -> Dict:
        """Analyze learning data to extract insights"""
        total_study_time = sum(session.get('duration_minutes', 0) for session in sessions)
        avg_session_length = total_study_time / len(sessions) if sessions else 0
        total_quizzes = len(quiz_attempts)
        avg_quiz_score = sum(attempt.get('score', 0) for attempt in quiz_attempts) / total_quizzes if quiz_attempts else 0
        
        return {
            'total_study_time_hours': round(total_study_time / 60, 2),
            'avg_session_length_minutes': round(avg_session_length, 2),
            'total_quizzes_taken': total_quizzes,
            'avg_quiz_score': round(avg_quiz_score, 2),
            'total_topics': len(topics),
            'study_consistency': self._calculate_study_consistency(sessions)
        }
    
    def _calculate_study_consistency(self, sessions: List) -> str:
        """Calculate study consistency rating"""
        if not sessions:
            return "No data"
        
        # Count days with study sessions in the last 30 days
        study_days = set()
        for session in sessions:
            if session.get('session_date'):
                study_days.add(session['session_date'][:10])  # Get date part
        
        consistency_ratio = len(study_days) / 30
        if consistency_ratio >= 0.8:
            return "Excellent"
        elif consistency_ratio >= 0.6:
            return "Good"
        elif consistency_ratio >= 0.4:
            return "Fair"
        else:
            return "Needs improvement"
    
    def _get_default_recommendations(self) -> Dict:
        """Get default recommendations when no data is available"""
        return {
            'recommendations': {
                'study_schedule': "Try to study for 30-45 minutes daily",
                'quiz_practice': "Take regular quizzes to test your knowledge",
                'topic_review': "Review previous topics to reinforce learning",
                'break_tips': "Take 5-10 minute breaks every 45 minutes"
            },
            'data_analysis': {'message': 'Not enough data for personalized recommendations yet'},
            'timestamp': datetime.now().isoformat()
        }
    
    def _build_recommendation_prompt(self, learning_data: Dict) -> str:
        """Build prompt for personalized recommendations"""
        data = learning_data['summary']
        
        prompt = f"""
        As an AI study tutor, analyze this student's learning data and provide personalized recommendations:
        
        Study Data:
        - Total study time: {data['total_study_time_hours']} hours
        - Average session length: {data['avg_session_length_minutes']} minutes
        - Quizzes taken: {data['total_quizzes_taken']}
        - Average quiz score: {data['avg_quiz_score']}%
        - Study consistency: {data['study_consistency']}
        - Topics studied: {data['total_topics']}
        
        Provide specific, actionable recommendations in JSON format:
        {{
            "study_schedule": "recommendation for when to study",
            "quiz_practice": "recommendation for quiz frequency",
            "topic_review": "recommendation for reviewing topics",
            "improvement_areas": ["specific areas to focus on"],
            "motivation_tips": ["encouraging tips"],
            "next_steps": ["immediate actions to take"]
        }}
        """
        return prompt
    
    def _call_ai_for_recommendations(self, prompt: str) -> Dict:
        """Call AI for personalized recommendations"""
        if not self.client:
            return self._get_default_recommendations()['recommendations']
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert AI study tutor. Provide personalized, actionable study recommendations based on learning data. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            return json.loads(content)
            
        except Exception as e:
            print(f"Error calling AI for recommendations: {e}")
            return self._get_default_recommendations()['recommendations']
    
    def _save_recommendations(self, recommendations: Dict):
        """Save recommendations to database"""
        if not self.supabase:
            return
        
        try:
            self.supabase.table('ai_recommendations').insert({
                'user_id': self.user_id,
                'recommendations': json.dumps(recommendations),
                'created_at': datetime.now().isoformat()
            }).execute()
        except Exception as e:
            print(f"Error saving recommendations: {e}")
    
    # Additional helper methods would be implemented here...
    def _get_topic_performance(self, topic_id: str) -> Dict:
        """Get performance data for a specific topic"""
        # Implementation would analyze quiz scores, study time, etc.
        return {'score': 75, 'time_spent': 120, 'difficulty': 'medium'}
    
    def _build_study_plan_prompt(self, topic, performance, target_grade, time_available) -> str:
        """Build prompt for study plan generation"""
        # Implementation would create detailed study plan prompts
        return f"Create a study plan for {topic.title}"
    
    def _call_ai_for_study_plan(self, prompt: str) -> Dict:
        """Call AI for study plan generation"""
        # Implementation would call OpenAI API
        return {'plan': 'Study plan generated by AI'}
    
    def _save_study_plan(self, topic_id: str, study_plan: Dict):
        """Save study plan to database"""
        # Implementation would save to database
        pass
    
    def _get_user_learning_profile(self) -> Dict:
        """Get user's learning profile"""
        return {'preferred_style': 'visual', 'difficulty_preference': 'medium'}
    
    def _build_explanation_prompt(self, concept, topic_context, level, profile) -> str:
        """Build explanation prompt"""
        return f"Explain {concept} at {level} level"
    
    def _call_ai_for_explanation(self, prompt: str) -> str:
        """Call AI for explanation"""
        return "AI explanation of the concept"
    
    def _save_explanation(self, concept: str, explanation: str, topic_id: str):
        """Save explanation to database"""
        pass
    
    def _get_recent_quiz_scores(self, topic_id: str) -> List:
        """Get recent quiz scores for topic"""
        return [75, 80, 85, 78]
    
    def _calculate_learning_velocity(self, topic_id: str) -> float:
        """Calculate learning velocity"""
        return 1.2
    
    def _build_grade_prediction_prompt(self, performance, scores, velocity, exam_date) -> str:
        """Build grade prediction prompt"""
        return "Predict grade based on performance data"
    
    def _call_ai_for_prediction(self, prompt: str) -> Dict:
        """Call AI for grade prediction"""
        return {'grade': 'A', 'confidence': 85, 'recommendations': ['Study more']}
    
    def _save_grade_prediction(self, topic_id: str, prediction: Dict, exam_date: str):
        """Save grade prediction"""
        pass
    
    def _analyze_study_patterns(self) -> Dict:
        """Analyze user's study patterns"""
        return {'pattern': 'evening_study', 'duration': '45_min'}
    
    def _build_learning_style_prompt(self, patterns) -> str:
        """Build learning style detection prompt"""
        return "Detect learning style from patterns"
    
    def _call_ai_for_learning_style(self, prompt: str) -> Dict:
        """Call AI for learning style detection"""
        return {'style': 'visual', 'confidence': 80}
    
    def _save_learning_style(self, style: Dict):
        """Save learning style"""
        pass
    
    def _identify_weak_areas(self, topic_id: str) -> List:
        """Identify weak areas in topic"""
        return ['algebra', 'geometry']
    
    def _build_adaptive_quiz_prompt(self, performance, weak_areas) -> str:
        """Build adaptive quiz prompt"""
        return "Recommend quiz adaptations"
    
    def _call_ai_for_adaptive_quiz(self, prompt: str) -> Dict:
        """Call AI for adaptive quiz recommendations"""
        return {'recommendations': ['Focus on algebra', 'More geometry practice']}

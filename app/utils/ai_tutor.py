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
            
            # Track AI activity
            self._track_ai_activity('study_plan', topic_id, {
                'target_grade': target_grade,
                'time_available': time_available,
                'topic_title': topic.title
            }, f"Generated personalized study plan for {topic.title}")
            
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
            
            # Track AI activity
            self._track_ai_activity('concept_explanation', topic_id, {
                'concept': concept,
                'level': explanation_level,
                'topic_title': topic.title if topic else 'General'
            }, f"Explained concept '{concept}' at {explanation_level} level")
            
            return {
                'concept': concept,
                'explanation': explanation.get('explanation', ''),
                'examples': explanation.get('examples', ''),
                'related_concepts': explanation.get('related_concepts', []),
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
            
            # Track AI activity
            self._track_ai_activity('grade_prediction', topic_id, {
                'predicted_grade': prediction.get('grade', 'Unknown'),
                'confidence': prediction.get('confidence', 0),
                'exam_date': exam_date
            }, f"Predicted grade {prediction.get('grade', 'Unknown')} with {prediction.get('confidence', 0)}% confidence")
            
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
            print(f"Adaptive Quiz Debug - Starting recommendations for topic: {topic_id}")
            
            # Get actual topic information
            print(f"Adaptive Quiz Debug - Fetching topic information...")
            from app.models import Topic
            topic = Topic.get_by_id(topic_id, self.user_id)
            if not topic:
                print(f"Adaptive Quiz Debug - Topic not found, using fallback")
                topic = None
            else:
                print(f"Adaptive Quiz Debug - Topic found: {topic.title}")
            
            # Get topic performance
            print(f"Adaptive Quiz Debug - Getting topic performance...")
            performance = self._get_topic_performance(topic_id)
            print(f"Adaptive Quiz Debug - Performance: {performance}")
            
            # Get weak areas
            print(f"Adaptive Quiz Debug - Identifying weak areas...")
            weak_areas = self._identify_weak_areas(topic_id)
            print(f"Adaptive Quiz Debug - Weak areas: {weak_areas}")
            
            # Build adaptive recommendations prompt
            print(f"Adaptive Quiz Debug - Building prompt...")
            prompt = self._build_adaptive_quiz_prompt(performance, weak_areas, topic)
            print(f"Adaptive Quiz Debug - Prompt length: {len(prompt)}")
            
            # Get AI recommendations
            print(f"Adaptive Quiz Debug - Calling AI...")
            recommendations = self._call_ai_for_adaptive_quiz(prompt)
            print(f"Adaptive Quiz Debug - AI response type: {type(recommendations)}")
            print(f"Adaptive Quiz Debug - AI response keys: {list(recommendations.keys()) if isinstance(recommendations, dict) else 'Not dict'}")
            
            # Safely extract recommendations
            if isinstance(recommendations, dict) and 'recommendations' in recommendations:
                rec_list = recommendations['recommendations']
            else:
                print(f"Adaptive Quiz Debug - No recommendations found, creating fallback")
                rec_list = [{
                    'quiz_type': 'General Practice',
                    'recommendation': 'Focus on fundamental concepts and practice problems',
                    'difficulty': 'medium',
                    'estimated_time': 15
                }]
            
            result = {
                'topic_id': topic_id,
                'recommendations': rec_list,
                'weak_areas': weak_areas,
                'performance': performance,
                'timestamp': datetime.now().isoformat()
            }
            
            # Track AI activity
            self._track_ai_activity('adaptive_quiz', topic_id, {
                'recommendations_count': len(rec_list),
                'topic_title': topic.title if topic else 'Unknown Topic'
            }, f"Generated {len(rec_list)} quiz recommendations for {topic.title if topic else 'selected topic'}")
            
            print(f"Adaptive Quiz Debug - Final result: {result}")
            return result
            
        except Exception as e:
            print(f"Error getting adaptive quiz recommendations: {e}")
            import traceback
            traceback.print_exc()
            return {'error': f'Failed to get quiz recommendations: {str(e)}'}
    
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
        try:
            from app.models import Topic
            topic = Topic.get_by_id(topic_id, self.user_id)
            if topic:
                # Generate topic-specific performance data
                topic_lower = topic.title.lower()
                if 'math' in topic_lower or 'algebra' in topic_lower:
                    return {
                        'score': 75, 
                        'time_spent': 120, 
                        'difficulty': 'medium',
                        'subject': 'Mathematics',
                        'focus_areas': ['problem solving', 'calculations', 'formulas']
                    }
                elif 'science' in topic_lower or 'physics' in topic_lower:
                    return {
                        'score': 80, 
                        'time_spent': 90, 
                        'difficulty': 'medium',
                        'subject': 'Science',
                        'focus_areas': ['experiments', 'theories', 'applications']
                    }
                elif 'history' in topic_lower:
                    return {
                        'score': 70, 
                        'time_spent': 150, 
                        'difficulty': 'medium',
                        'subject': 'History',
                        'focus_areas': ['timeline', 'analysis', 'causes and effects']
                    }
                elif 'english' in topic_lower or 'literature' in topic_lower:
                    return {
                        'score': 85, 
                        'time_spent': 100, 
                        'difficulty': 'medium',
                        'subject': 'English',
                        'focus_areas': ['comprehension', 'analysis', 'writing']
                    }
                else:
                    return {
                        'score': 75, 
                        'time_spent': 120, 
                        'difficulty': 'medium',
                        'subject': 'General',
                        'focus_areas': ['understanding', 'application', 'retention']
                    }
            else:
                return {'score': 75, 'time_spent': 120, 'difficulty': 'medium'}
        except Exception as e:
            print(f"Error getting topic performance: {e}")
            return {'score': 75, 'time_spent': 120, 'difficulty': 'medium'}
    
    def _build_study_plan_prompt(self, topic, performance, target_grade, time_available) -> str:
        """Build prompt for study plan generation"""
        prompt = f"""
Create a comprehensive, personalized study plan for the topic: "{topic.title}"

Topic Description: {topic.description[:200]}...

Current Performance: {performance}
Target Grade: {target_grade if target_grade else 'Not specified'}
Time Available: {time_available} hours per week

Please create a detailed study plan that includes:
1. Weekly study schedule with specific time allocations
2. Learning objectives and milestones
3. Study methods and techniques
4. Practice activities and exercises
5. Assessment and review strategies
6. Timeline for achieving the target grade

Format the response as a structured study plan with clear sections and actionable steps.
"""
        return prompt
    
    def _call_ai_for_study_plan(self, prompt: str) -> Dict:
        """Call AI for study plan generation"""
        if not self.client:
            return {
                'plan': 'AI service not available. Please check your OpenAI API key.',
                'error': 'OpenAI client not initialized'
            }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational tutor specializing in creating personalized study plans. Provide detailed, actionable study plans with specific activities, timelines, and learning strategies."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse the AI response into structured format
            return self._parse_study_plan_response(ai_response)
            
        except Exception as e:
            print(f"Error calling AI for study plan: {e}")
            return {
                'plan': f'Error generating study plan: {str(e)}',
                'error': str(e)
            }
    
    def _parse_study_plan_response(self, ai_response: str) -> Dict:
        """Parse AI response into structured study plan"""
        try:
            # Split the response into sections
            lines = ai_response.split('\n')
            structured_plan = {
                'overview': '',
                'weekly_schedule': [],
                'learning_objectives': [],
                'study_methods': [],
                'practice_activities': [],
                'assessment_strategies': [],
                'timeline': '',
                'full_text': ai_response
            }
            
            current_section = 'overview'
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Detect section headers
                if any(keyword in line.lower() for keyword in ['weekly', 'schedule', 'timetable']):
                    current_section = 'weekly_schedule'
                elif any(keyword in line.lower() for keyword in ['objective', 'goal', 'milestone']):
                    current_section = 'learning_objectives'
                elif any(keyword in line.lower() for keyword in ['method', 'technique', 'approach']):
                    current_section = 'study_methods'
                elif any(keyword in line.lower() for keyword in ['practice', 'exercise', 'activity']):
                    current_section = 'practice_activities'
                elif any(keyword in line.lower() for keyword in ['assessment', 'review', 'test']):
                    current_section = 'assessment_strategies'
                elif any(keyword in line.lower() for keyword in ['timeline', 'schedule', 'deadline']):
                    current_section = 'timeline'
                else:
                    # Add content to current section
                    if current_section == 'weekly_schedule':
                        structured_plan['weekly_schedule'].append(line)
                    elif current_section == 'learning_objectives':
                        structured_plan['learning_objectives'].append(line)
                    elif current_section == 'study_methods':
                        structured_plan['study_methods'].append(line)
                    elif current_section == 'practice_activities':
                        structured_plan['practice_activities'].append(line)
                    elif current_section == 'assessment_strategies':
                        structured_plan['assessment_strategies'].append(line)
                    elif current_section == 'timeline':
                        structured_plan['timeline'] += line + '\n'
                    else:
                        structured_plan['overview'] += line + '\n'
            
            return structured_plan
            
        except Exception as e:
            print(f"Error parsing study plan response: {e}")
            return {
                'full_text': ai_response,
                'overview': ai_response,
                'error': f'Error parsing response: {str(e)}'
            }
    
    def _save_study_plan(self, topic_id: str, study_plan: Dict):
        """Save study plan to database"""
        # Implementation would save to database
        pass
    
    def _get_user_learning_profile(self) -> Dict:
        """Get user's learning profile"""
        return {'preferred_style': 'visual', 'difficulty_preference': 'medium'}
    
    def _build_explanation_prompt(self, concept, topic_context, level, profile) -> str:
        """Build explanation prompt"""
        prompt = f"""
Explain the concept "{concept}" in detail.

Context: {topic_context if topic_context else 'No specific topic context provided'}

Explanation Level: {level}
- Beginner: Use simple language, basic examples, and fundamental concepts
- Intermediate: Include some technical terms, practical examples, and connections to other concepts
- Advanced: Use precise terminology, complex examples, and deep theoretical understanding

Please provide:
1. A clear, comprehensive explanation of the concept
2. Practical examples that illustrate the concept
3. Related concepts that connect to this topic
4. Analogies or comparisons to help understanding

Make the explanation engaging and educational, suitable for the {level} level.
"""
        return prompt
    
    def _call_ai_for_explanation(self, prompt: str) -> Dict:
        """Call AI for explanation"""
        if not self.client:
            return {
                'explanation': 'AI service not available. Please check your OpenAI API key.',
                'examples': '',
                'related_concepts': [],
                'error': 'OpenAI client not initialized'
            }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational tutor specializing in explaining complex concepts in simple, understandable terms. Provide clear explanations with examples, analogies, and related concepts. Structure your response to be educational and engaging."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse the AI response into structured format
            return self._parse_explanation_response(ai_response)
            
        except Exception as e:
            print(f"Error calling AI for explanation: {e}")
            return {
                'explanation': f'Error generating explanation: {str(e)}',
                'examples': '',
                'related_concepts': [],
                'error': str(e)
            }
    
    def _parse_explanation_response(self, ai_response: str) -> Dict:
        """Parse AI response into structured explanation"""
        try:
            # Split the response into sections
            lines = ai_response.split('\n')
            structured_explanation = {
                'explanation': '',
                'examples': '',
                'related_concepts': [],
                'full_text': ai_response
            }
            
            current_section = 'explanation'
            examples_section = []
            related_concepts = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Detect section headers
                if any(keyword in line.lower() for keyword in ['example', 'for instance', 'such as', 'like']):
                    current_section = 'examples'
                elif any(keyword in line.lower() for keyword in ['related', 'connected', 'similar', 'associated']):
                    current_section = 'related'
                else:
                    # Add content to appropriate section
                    if current_section == 'examples':
                        examples_section.append(line)
                    elif current_section == 'related':
                        # Extract concept names from the line
                        if ':' in line:
                            concepts = line.split(':')[1].strip()
                            related_concepts.extend([c.strip() for c in concepts.split(',') if c.strip()])
                        else:
                            related_concepts.append(line)
                    else:
                        structured_explanation['explanation'] += line + '\n'
            
            # Clean up examples
            if examples_section:
                structured_explanation['examples'] = '\n'.join(examples_section)
            
            # Clean up related concepts
            if related_concepts:
                structured_explanation['related_concepts'] = [c for c in related_concepts if len(c) > 2]
            
            # If no structured data, use full text
            if not structured_explanation['explanation']:
                structured_explanation['explanation'] = ai_response
            
            return structured_explanation
            
        except Exception as e:
            print(f"Error parsing explanation response: {e}")
            return {
                'explanation': ai_response,
                'examples': '',
                'related_concepts': [],
                'full_text': ai_response,
                'error': f'Error parsing response: {str(e)}'
            }
    
    def _save_explanation(self, concept: str, explanation: Dict, topic_id: str):
        """Save explanation to database"""
        pass
    
    def _parse_adaptive_quiz_response(self, ai_response: str) -> Dict:
        """Parse AI response into structured quiz recommendations"""
        try:
            # Split the response into lines
            lines = ai_response.split('\n')
            recommendations = []
            
            current_recommendation = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    if current_recommendation:
                        recommendations.append(current_recommendation)
                        current_recommendation = {}
                    continue
                
                # Detect recommendation headers
                if any(keyword in line.lower() for keyword in ['recommendation', 'suggestion', 'quiz', 'practice']):
                    if current_recommendation:
                        recommendations.append(current_recommendation)
                    current_recommendation = {
                        'quiz_type': 'Adaptive Quiz',
                        'recommendation': line,
                        'difficulty': 'medium',
                        'estimated_time': 15
                    }
                elif current_recommendation:
                    # Add details to current recommendation
                    if 'difficulty' in line.lower():
                        current_recommendation['difficulty'] = line.split(':')[-1].strip() if ':' in line else 'medium'
                    elif 'time' in line.lower():
                        time_match = line.split(':')[-1].strip() if ':' in line else '15'
                        try:
                            # Extract numbers from time string safely
                            digits = ''.join(filter(str.isdigit, time_match))
                            current_recommendation['estimated_time'] = int(digits) if digits else 15
                        except (ValueError, TypeError):
                            current_recommendation['estimated_time'] = 15
                    else:
                        current_recommendation['recommendation'] += f" {line}"
            
            # Add the last recommendation
            if current_recommendation:
                recommendations.append(current_recommendation)
            
            # If no structured recommendations found, create a general one
            if not recommendations:
                recommendations = [{
                    'quiz_type': 'General Practice',
                    'recommendation': ai_response,
                    'difficulty': 'medium',
                    'estimated_time': 15
                }]
            
            return {
                'recommendations': recommendations
            }
            
        except Exception as e:
            print(f"Error parsing adaptive quiz response: {e}")
            return {
                'recommendations': [{
                    'quiz_type': 'General Practice',
                    'recommendation': ai_response,
                    'difficulty': 'medium',
                    'estimated_time': 15
                }]
            }
    
    def _track_ai_activity(self, activity_type: str, topic_id: str = None, 
                          activity_data: Dict = None, result_summary: str = None):
        """Track AI activity for the user"""
        try:
            print(f"AI Activity Debug - Tracking activity: {activity_type} for user {self.user_id}")
            print(f"AI Activity Debug - Topic ID: {topic_id}")
            print(f"AI Activity Debug - Activity data: {activity_data}")
            print(f"AI Activity Debug - Result summary: {result_summary}")
            
            from app.models import AIActivity
            result = AIActivity.create_activity(
                user_id=self.user_id,
                activity_type=activity_type,
                topic_id=topic_id,
                activity_data=activity_data,
                result_summary=result_summary
            )
            
            if result:
                print(f"AI Activity Debug - Activity created successfully: {result.id}")
            else:
                print(f"AI Activity Debug - Activity creation returned None")
                
            print(f"AI Activity tracked: {activity_type} for user {self.user_id}")
        except Exception as e:
            print(f"Error tracking AI activity: {e}")
            import traceback
            traceback.print_exc()
    
    def _enhanced_chat(self, message: str, context: str = '', topic_id: str = None) -> str:
        """Enhanced AI chat with learning context"""
        try:
            if not self.client:
                return "I'm sorry, but I'm currently unavailable. Please check your OpenAI API key configuration."
            
            # Get topic context if provided
            topic_context = ""
            if topic_id:
                from app.models import Topic
                topic = Topic.get_by_id(topic_id, self.user_id)
                if topic:
                    topic_context = f"Topic: {topic.title}\nDescription: {topic.description}\n"
            
            # Build enhanced prompt
            prompt = f"""
You are an expert AI tutor specializing in personalized education. Help the student with their question.

{topic_context}
Previous conversation context: {context}

Student's question: {message}

Please provide a helpful, educational response that:
1. Directly answers their question
2. Provides additional learning insights
3. Suggests related topics or follow-up questions
4. Uses appropriate difficulty level for the student
5. Encourages further learning

Keep your response conversational and supportive.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert AI tutor specializing in personalized education. Provide helpful, educational responses that encourage learning."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Track chat activity
            self._track_ai_activity('chat', topic_id, {
                'message': message[:100],  # First 100 chars
                'topic_title': topic.title if topic_id and 'topic' in locals() else 'General'
            }, f"Chat interaction: {message[:50]}...")
            
            return ai_response
            
        except Exception as e:
            print(f"Error in enhanced chat: {e}")
            return "I'm sorry, I encountered an error while processing your message. Please try again."
    
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
        try:
            from app.models import Topic
            topic = Topic.get_by_id(topic_id, self.user_id)
            if topic:
                # Generate topic-specific weak areas based on the topic content
                topic_lower = topic.title.lower()
                if 'math' in topic_lower or 'algebra' in topic_lower:
                    return ['basic operations', 'equation solving', 'word problems']
                elif 'science' in topic_lower or 'physics' in topic_lower:
                    return ['formulas', 'calculations', 'concept application']
                elif 'history' in topic_lower:
                    return ['dates', 'causes and effects', 'historical analysis']
                elif 'english' in topic_lower or 'literature' in topic_lower:
                    return ['comprehension', 'analysis', 'critical thinking']
                elif 'chemistry' in topic_lower:
                    return ['chemical equations', 'periodic table', 'reactions']
                elif 'biology' in topic_lower:
                    return ['cell structure', 'processes', 'classification']
                else:
                    # Generic weak areas based on common learning challenges
                    return ['fundamental concepts', 'application', 'problem solving']
            else:
                return ['fundamental concepts', 'application', 'problem solving']
        except Exception as e:
            print(f"Error identifying weak areas: {e}")
            return ['fundamental concepts', 'application', 'problem solving']
    
    def _build_adaptive_quiz_prompt(self, performance, weak_areas, topic=None) -> str:
        """Build adaptive quiz prompt"""
        # Get topic information if available
        topic_context = ""
        if topic:
            topic_context = f"""
Topic: {topic.title}
Description: {topic.description}
Subject Area: {getattr(topic, 'subject', 'General')}
"""
        
        prompt = f"""
Analyze this student's learning data and provide personalized quiz recommendations for their specific topic:

{topic_context}
Current Performance: {performance}
Identified Weak Areas: {weak_areas}

Please provide specific quiz recommendations that are directly related to the topic above. Include:
1. Quiz type and focus area (specific to the topic)
2. Difficulty level
3. Estimated time required
4. Learning objectives (topic-specific)
5. Specific subtopics within the main topic to focus on

Make sure all recommendations are directly relevant to the topic: {topic.title if topic else 'the selected topic'}.

Format your response as structured recommendations that will help the student improve their understanding of this specific topic.
"""
        return prompt
    
    def _call_ai_for_adaptive_quiz(self, prompt: str) -> Dict:
        """Call AI for adaptive quiz recommendations"""
        if not self.client:
            return {
                'recommendations': [{
                    'quiz_type': 'General Practice',
                    'recommendation': 'AI service not available. Please check your OpenAI API key.',
                    'difficulty': 'medium',
                    'estimated_time': 15
                }],
                'error': 'OpenAI client not initialized'
            }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational tutor specializing in creating personalized quiz recommendations. Analyze student performance data and provide specific, actionable quiz recommendations with difficulty levels, time estimates, and learning objectives."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse the AI response into structured recommendations
            return self._parse_adaptive_quiz_response(ai_response)
            
        except Exception as e:
            print(f"Error calling AI for adaptive quiz: {e}")
            return {
                'recommendations': [{
                    'quiz_type': 'Error',
                    'recommendation': f'Error generating recommendations: {str(e)}',
                    'difficulty': 'medium',
                    'estimated_time': 15
                }],
                'error': str(e)
            }
    
    def _analyze_study_patterns(self) -> Dict:
        """Analyze user's study patterns for learning style detection"""
        try:
            if not self.supabase:
                return {
                    'total_sessions': 0,
                    'average_duration': 30,
                    'preferred_times': ['morning'],
                    'content_preferences': ['text'],
                    'performance_patterns': 'stable',
                    'study_consistency': 'low'
                }
            
            # Get study sessions data
            sessions_res = self.supabase.table('study_sessions').select('*').eq('user_id', self.user_id).execute()
            sessions = sessions_res.data if sessions_res.data else []
            
            # Get quiz attempts (quiz results are stored in quiz_attempts table)
            quiz_res = self.supabase.table('quiz_attempts').select('*').eq('user_id', self.user_id).execute()
            quiz_results = quiz_res.data if quiz_res.data else []
            
            # Get topics for additional context
            topics_res = self.supabase.table('topics').select('*').eq('user_id', self.user_id).execute()
            topics = topics_res.data if topics_res.data else []
            
            # Analyze patterns
            study_patterns = {
                'total_sessions': len(sessions),
                'average_duration': sum(s.get('duration_minutes', 0) for s in sessions) / max(len(sessions), 1),
                'preferred_times': self._analyze_study_times(sessions),
                'content_preferences': self._analyze_content_preferences(sessions),
                'performance_patterns': self._analyze_performance_patterns(quiz_results),
                'study_consistency': self._analyze_study_consistency(sessions),
                'total_topics': len(topics),
                'session_types': self._analyze_session_types(sessions),
                'confidence_trends': self._analyze_confidence_trends(sessions)
            }
            
            return study_patterns
            
        except Exception as e:
            print(f"Error analyzing study patterns: {e}")
            import traceback
            traceback.print_exc()
            return {
                'total_sessions': 0,
                'average_duration': 30,
                'preferred_times': ['morning'],
                'content_preferences': ['text'],
                'performance_patterns': 'stable',
                'study_consistency': 'low',
                'total_topics': 0,
                'session_types': ['study'],
                'confidence_trends': 'stable'
            }
    
    def _analyze_study_times(self, sessions: List[Dict]) -> List[str]:
        """Analyze preferred study times"""
        if not sessions:
            return ['morning']
        
        time_preferences = []
        for session in sessions:
            created_at = session.get('created_at', '')
            if created_at:
                # Simple time analysis (would be more sophisticated in production)
                hour = int(created_at.split('T')[1].split(':')[0]) if 'T' in created_at else 9
                if 6 <= hour < 12:
                    time_preferences.append('morning')
                elif 12 <= hour < 18:
                    time_preferences.append('afternoon')
                else:
                    time_preferences.append('evening')
        
        # Return most common time
        from collections import Counter
        return [Counter(time_preferences).most_common(1)[0][0]] if time_preferences else ['morning']
    
    def _analyze_content_preferences(self, sessions: List[Dict]) -> List[str]:
        """Analyze content type preferences"""
        if not sessions:
            return ['text']
        
        content_types = []
        for session in sessions:
            content_type = session.get('content_type', 'text')
            content_types.append(content_type)
        
        # Return most common content types
        from collections import Counter
        return [item[0] for item in Counter(content_types).most_common(2)]
    
    def _analyze_performance_patterns(self, quiz_results: List[Dict]) -> str:
        """Analyze performance patterns"""
        if not quiz_results:
            return 'stable'
        
        # Use score field from quiz_attempts table
        scores = [r.get('score', 0) for r in quiz_results if r.get('score') is not None]
        if len(scores) < 2:
            return 'stable'
        
        # Simple trend analysis
        if scores[-1] > scores[0]:
            return 'improving'
        elif scores[-1] < scores[0]:
            return 'declining'
        else:
            return 'stable'
    
    def _analyze_study_consistency(self, sessions: List[Dict]) -> str:
        """Analyze study consistency"""
        if len(sessions) < 3:
            return 'low'
        
        # Simple consistency check based on frequency
        if len(sessions) >= 10:
            return 'high'
        elif len(sessions) >= 5:
            return 'medium'
        else:
            return 'low'
    
    def _analyze_session_types(self, sessions: List[Dict]) -> List[str]:
        """Analyze session types"""
        if not sessions:
            return ['study']
        
        session_types = []
        for session in sessions:
            session_type = session.get('session_type', 'study')
            session_types.append(session_type)
        
        # Return most common session types
        from collections import Counter
        return [item[0] for item in Counter(session_types).most_common(3)]
    
    def _analyze_confidence_trends(self, sessions: List[Dict]) -> str:
        """Analyze confidence trends"""
        if len(sessions) < 2:
            return 'stable'
        
        # Get confidence before and after for trend analysis
        confidence_gains = []
        for session in sessions:
            confidence_before = session.get('confidence_before', 5)
            confidence_after = session.get('confidence_after', 5)
            gain = confidence_after - confidence_before
            confidence_gains.append(gain)
        
        if not confidence_gains:
            return 'stable'
        
        # Calculate average gain
        avg_gain = sum(confidence_gains) / len(confidence_gains)
        
        if avg_gain > 0.5:
            return 'improving'
        elif avg_gain < -0.5:
            return 'declining'
        else:
            return 'stable'
    
    def _build_learning_style_prompt(self, study_patterns: Dict) -> str:
        """Build prompt for learning style detection"""
        prompt = f"""
        Analyze the following study patterns to determine the user's learning style:
        
        Study Patterns:
        - Total Sessions: {study_patterns.get('total_sessions', 0)}
        - Total Topics: {study_patterns.get('total_topics', 0)}
        - Average Duration: {study_patterns.get('average_duration', 30):.1f} minutes
        - Preferred Study Times: {', '.join(study_patterns.get('preferred_times', ['morning']))}
        - Content Preferences: {', '.join(study_patterns.get('content_preferences', ['text']))}
        - Session Types: {', '.join(study_patterns.get('session_types', ['study']))}
        - Performance Patterns: {study_patterns.get('performance_patterns', 'stable')}
        - Confidence Trends: {study_patterns.get('confidence_trends', 'stable')}
        - Study Consistency: {study_patterns.get('study_consistency', 'low')}
        
        Based on this data, determine the primary learning style and provide:
        1. Primary learning style (visual, auditory, kinesthetic, reading_writing, or multimodal)
        2. Confidence level (0-100%)
        3. 3-5 personalized study recommendations
        4. Brief explanation of why this style was chosen
        
        Return the response in JSON format with keys: style, confidence, recommendations, explanation.
        """
        return prompt
    
    def _call_ai_for_learning_style(self, prompt: str) -> Dict:
        """Call OpenAI API for learning style analysis"""
        if not self.client:
            return {
                'style': 'visual',
                'confidence': 75,
                'recommendations': [
                    'Use visual aids like diagrams and charts',
                    'Create mind maps for complex topics',
                    'Watch educational videos',
                    'Use color coding in your notes',
                    'Practice with visual flashcards'
                ],
                'explanation': 'Based on your study patterns, you appear to be a visual learner who benefits from visual representations of information.'
            }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in learning psychology and cognitive science. Analyze study patterns to determine learning styles and provide personalized recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                import json
                return json.loads(ai_response)
            except:
                # Fallback parsing if JSON is not returned
                return self._parse_learning_style_response(ai_response)
                
        except Exception as e:
            print(f"Error calling AI for learning style: {e}")
            return {
                'style': 'visual',
                'confidence': 70,
                'recommendations': [
                    'Use visual learning materials',
                    'Create diagrams and charts',
                    'Watch educational videos',
                    'Use color coding in notes'
                ],
                'explanation': 'Based on your study patterns, you appear to be a visual learner.'
            }
    
    def _parse_learning_style_response(self, response: str) -> Dict:
        """Parse AI response for learning style"""
        # Extract style from response
        style = 'visual'
        if 'auditory' in response.lower():
            style = 'auditory'
        elif 'kinesthetic' in response.lower():
            style = 'kinesthetic'
        elif 'reading' in response.lower() or 'writing' in response.lower():
            style = 'reading_writing'
        elif 'multimodal' in response.lower():
            style = 'multimodal'
        
        # Extract confidence
        import re
        confidence_match = re.search(r'(\d+)%', response)
        confidence = int(confidence_match.group(1)) if confidence_match else 75
        
        # Extract recommendations
        recommendations = [
            'Use visual learning materials',
            'Create study diagrams',
            'Watch educational videos',
            'Use color coding in notes'
        ]
        
        return {
            'style': style,
            'confidence': confidence,
            'recommendations': recommendations,
            'explanation': 'Based on your study patterns, you appear to be a ' + style + ' learner.'
        }
    
    def _save_learning_style(self, learning_style: Dict):
        """Save learning style to database"""
        try:
            if not self.supabase:
                return
            
            # Save to learning styles table (using correct column names)
            style_data = {
                'user_id': self.user_id,
                'learning_style': learning_style.get('style', 'visual'),
                'confidence_score': learning_style.get('confidence', 75),
                'recommendations': learning_style.get('recommendations', []),
                'study_patterns': learning_style.get('study_patterns', {}),
                'created_at': datetime.now().isoformat()
            }
            
            # Use upsert to update existing record or create new one
            self.supabase.table('ai_learning_styles').upsert(style_data).execute()
            
        except Exception as e:
            print(f"Error saving learning style: {e}")

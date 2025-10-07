"""
GCSE-Specific AI Enhancement System
Advanced AI features tailored specifically for GCSE students and curriculum
"""

import openai
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from app.models import get_supabase_client, SUPABASE_AVAILABLE
from app.models import Topic
from app.utils.ai_tutor import AITutor
from app.utils.predictive_analytics import PredictiveAnalytics
from app.utils.smart_content_generator import SmartContentGenerator
from dotenv import load_dotenv

load_dotenv()

class GCSEAIEnhancement:
    """GCSE-specific AI enhancement system"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.client = self._get_openai_client()
        self.supabase = get_supabase_client() if SUPABASE_AVAILABLE else None
        self.ai_tutor = AITutor(user_id)
        self.analytics = PredictiveAnalytics(user_id)
        self.content_generator = SmartContentGenerator(user_id)
    
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
    
    def generate_gcse_study_plan(self, subject: str, exam_board: str, target_grade: str, exam_date: str) -> Dict:
        """Generate comprehensive GCSE study plan with exam board alignment"""
        try:
            # Get subject-specific curriculum data
            curriculum_data = self._get_gcse_curriculum_data(subject, exam_board)
            
            # Calculate study timeline
            exam_date_obj = datetime.fromisoformat(exam_date.replace('Z', '+00:00'))
            days_until_exam = (exam_date_obj - datetime.now()).days
            
            # Get user's current performance
            user_performance = self._get_user_gcse_performance(subject)
            
            # Generate AI-powered study plan
            study_plan = self._create_gcse_study_plan(curriculum_data, target_grade, days_until_exam, user_performance, exam_board)
            
            # Save study plan
            self._save_gcse_study_plan(subject, exam_board, target_grade, study_plan)
            
            return {
                'subject': subject,
                'exam_board': exam_board,
                'target_grade': target_grade,
                'exam_date': exam_date,
                'days_until_exam': days_until_exam,
                'study_plan': study_plan,
                'curriculum_alignment': curriculum_data,
                'user_performance': user_performance,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating GCSE study plan: {e}")
            return {'error': 'Failed to generate GCSE study plan'}
    
    def generate_gcse_past_paper_analysis(self, subject: str, exam_board: str, paper_type: str = 'recent') -> Dict:
        """Generate AI analysis of GCSE past papers"""
        try:
            # Get past paper data
            past_paper_data = self._get_gcse_past_papers(subject, exam_board, paper_type)
            
            # Analyze question patterns
            question_analysis = self._analyze_gcse_question_patterns(past_paper_data)
            
            # Generate topic importance rankings
            topic_importance = self._calculate_topic_importance(past_paper_data)
            
            # Create exam strategy recommendations
            exam_strategies = self._generate_gcse_exam_strategies(question_analysis, topic_importance)
            
            # Generate practice recommendations
            practice_recommendations = self._generate_gcse_practice_recommendations(question_analysis)
            
            return {
                'subject': subject,
                'exam_board': exam_board,
                'paper_type': paper_type,
                'question_analysis': question_analysis,
                'topic_importance': topic_importance,
                'exam_strategies': exam_strategies,
                'practice_recommendations': practice_recommendations,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error analyzing GCSE past papers: {e}")
            return {'error': 'Failed to analyze past papers'}
    
    def generate_gcse_grade_boundary_predictions(self, subject: str, exam_board: str, current_performance: Dict) -> Dict:
        """Predict GCSE grade boundaries and student performance"""
        try:
            print(f"Starting grade boundary prediction for {subject}")
            
            # Get historical grade boundaries
            grade_boundaries = self._get_gcse_grade_boundaries(subject, exam_board)
            print(f"Grade boundaries retrieved: {grade_boundaries}")
            
            # Analyze current performance trends
            performance_trends = self._analyze_gcse_performance_trends(current_performance)
            print(f"Performance trends: {performance_trends}")
            
            # Predict grade boundaries for current year
            predicted_boundaries = self._predict_grade_boundaries(grade_boundaries, performance_trends)
            print(f"Predicted boundaries: {predicted_boundaries}")
            
            # Calculate student's predicted grade
            predicted_grade = self._calculate_predicted_grade(current_performance, predicted_boundaries)
            print(f"Predicted grade: {predicted_grade}")
            
            # Generate improvement recommendations
            improvement_plan = self._generate_gcse_improvement_plan(current_performance, predicted_grade, predicted_boundaries)
            print(f"Improvement plan generated: {improvement_plan.keys() if isinstance(improvement_plan, dict) else type(improvement_plan)}")
            
            result = {
                'subject': subject,
                'exam_board': exam_board,
                'current_performance': current_performance,
                'historical_boundaries': grade_boundaries,
                'predicted_boundaries': predicted_boundaries,
                'predicted_grade': predicted_grade,
                'improvement_plan': improvement_plan,
                'prediction_confidence': self._calculate_prediction_confidence(performance_trends),
                'generated_at': datetime.now().isoformat()
            }
            
            print(f"Returning prediction result with keys: {result.keys()}")
            return result
            
        except Exception as e:
            print(f"Error predicting GCSE grade boundaries: {e}")
            import traceback
            traceback.print_exc()
            return {'error': f'Failed to predict grade boundaries: {str(e)}'}
    
    def generate_gcse_revision_schedule(self, subjects: List[str], exam_dates: Dict[str, str], target_grades: Dict[str, str]) -> Dict:
        """Generate comprehensive GCSE revision schedule across multiple subjects"""
        try:
            # Get exam dates and priorities
            exam_schedule = self._organize_exam_schedule(exam_dates)
            
            # Calculate subject priorities
            subject_priorities = self._calculate_subject_priorities(subjects, target_grades, exam_schedule)
            
            # Generate daily revision schedule
            daily_schedule = self._generate_daily_revision_schedule(subject_priorities, exam_schedule)
            
            # Create subject-specific revision plans
            subject_plans = {}
            for subject in subjects:
                subject_plans[subject] = self._generate_subject_revision_plan(subject, exam_dates[subject], target_grades[subject])
            
            # Generate stress management and well-being recommendations
            well_being_plan = self._generate_gcse_wellbeing_plan(exam_schedule)
            
            return {
                'subjects': subjects,
                'exam_dates': exam_dates,
                'target_grades': target_grades,
                'exam_schedule': exam_schedule,
                'subject_priorities': subject_priorities,
                'daily_schedule': daily_schedule,
                'subject_plans': subject_plans,
                'wellbeing_plan': well_being_plan,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating GCSE revision schedule: {e}")
            return {'error': 'Failed to generate revision schedule'}
    
    def generate_gcse_exam_techniques(self, subject: str, exam_board: str, question_types: List[str]) -> Dict:
        """Generate GCSE-specific exam techniques and strategies"""
        try:
            # Get exam format information
            exam_format = self._get_gcse_exam_format(subject, exam_board)
            
            # Generate question-specific techniques
            question_techniques = self._generate_question_specific_techniques(question_types, exam_format)
            
            # Create time management strategies
            time_management = self._generate_gcse_time_management_strategies(exam_format)
            
            # Generate marking scheme insights
            marking_insights = self._generate_gcse_marking_insights(subject, exam_board)
            
            # Create common mistake avoidance guide
            mistake_avoidance = self._generate_gcse_mistake_avoidance_guide(subject, exam_board)
            
            return {
                'subject': subject,
                'exam_board': exam_board,
                'exam_format': exam_format,
                'question_techniques': question_techniques,
                'time_management': time_management,
                'marking_insights': marking_insights,
                'mistake_avoidance': mistake_avoidance,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating GCSE exam techniques: {e}")
            return {'error': 'Failed to generate exam techniques'}
    
    def generate_gcse_personalized_content(self, subject: str, topic: str, learning_style: str, difficulty_level: str) -> Dict:
        """Generate GCSE-specific personalized content"""
        try:
            # Get GCSE curriculum requirements
            curriculum_requirements = self._get_gcse_topic_requirements(subject, topic)
            
            # Generate content based on learning style
            if learning_style == 'visual':
                content = self._generate_gcse_visual_content(subject, topic, curriculum_requirements)
            elif learning_style == 'auditory':
                content = self._generate_gcse_auditory_content(subject, topic, curriculum_requirements)
            elif learning_style == 'kinesthetic':
                content = self._generate_gcse_kinesthetic_content(subject, topic, curriculum_requirements)
            else:
                content = self._generate_gcse_multi_modal_content(subject, topic, curriculum_requirements)
            
            # Adapt content to difficulty level
            adapted_content = self._adapt_content_to_difficulty(content, difficulty_level, curriculum_requirements)
            
            # Add GCSE-specific exam preparation elements
            exam_prep_content = self._add_gcse_exam_preparation(adapted_content, subject, topic)
            
            # Flatten the structure - merge exam_prep_content with metadata
            result = {
                'subject': subject,
                'topic': topic,
                'learning_style': learning_style,
                'difficulty_level': difficulty_level,
                'curriculum_requirements': exam_prep_content.get('curriculum_requirements', []),
                'generated_at': datetime.now().isoformat()
            }
            
            # Add all the content fields from exam_prep_content
            result.update(exam_prep_content)
            
            return result
            
        except Exception as e:
            print(f"Error generating GCSE personalized content: {e}")
            return {'error': 'Failed to generate personalized content'}
    
    def analyze_gcse_performance_gaps(self, subject: str, user_performance: Dict) -> Dict:
        """Analyze GCSE performance gaps and provide targeted improvement strategies"""
        try:
            # Get subject curriculum standards
            curriculum_standards = self._get_gcse_curriculum_standards(subject)
            
            # Identify performance gaps
            performance_gaps = self._identify_gcse_performance_gaps(user_performance, curriculum_standards)
            
            # Prioritize gaps by impact
            prioritized_gaps = self._prioritize_performance_gaps(performance_gaps)
            
            # Generate targeted improvement strategies
            improvement_strategies = self._generate_targeted_improvement_strategies(prioritized_gaps, subject)
            
            # Create practice recommendations
            practice_recommendations = self._generate_gcse_practice_recommendations_for_gaps(prioritized_gaps)
            
            # Generate progress tracking plan
            progress_tracking = self._generate_gcse_progress_tracking_plan(prioritized_gaps)
            
            return {
                'subject': subject,
                'user_performance': user_performance,
                'curriculum_standards': curriculum_standards,
                'performance_gaps': performance_gaps,
                'prioritized_gaps': prioritized_gaps,
                'improvement_strategies': improvement_strategies,
                'practice_recommendations': practice_recommendations,
                'progress_tracking': progress_tracking,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error analyzing GCSE performance gaps: {e}")
            return {'error': 'Failed to analyze performance gaps'}
    
    # Helper methods for GCSE-specific functionality
    def _get_gcse_curriculum_data(self, subject: str, exam_board: str) -> Dict:
        """Get GCSE curriculum data for specific subject and exam board"""
        if not self.supabase:
            return self._get_default_gcse_curriculum(subject, exam_board)
        
        try:
            # Query GCSE curriculum data
            curriculum = self.supabase.table('gcse_curriculum').select('*').eq('subject', subject).eq('exam_board', exam_board).execute()
            
            if curriculum.data:
                return curriculum.data[0]
            else:
                return self._get_default_gcse_curriculum(subject, exam_board)
                
        except Exception as e:
            print(f"Error getting GCSE curriculum data: {e}")
            return self._get_default_gcse_curriculum(subject, exam_board)
    
    def _get_default_gcse_curriculum(self, subject: str, exam_board: str) -> Dict:
        """Get default GCSE curriculum structure"""
        return {
            'subject': subject,
            'exam_board': exam_board,
            'topics': [],
            'assessment_objectives': [],
            'grade_descriptors': {}
        }
    
    def _get_user_gcse_performance(self, subject: str) -> Dict:
        """Get user's GCSE performance data for a subject"""
        if not self.supabase:
            return {'current_grade': 'Unknown', 'strengths': [], 'weaknesses': []}
        
        try:
            # Get user's topics for this subject
            topics = self.supabase.table('topics').select('*').eq('user_id', self.user_id).eq('gcse_subject', subject).execute()
            
            # Get quiz performance
            quiz_scores = []
            for topic in topics.data:
                quizzes = self.supabase.table('quiz_attempts').select('score').eq('user_id', self.user_id).eq('quiz_id', topic['id']).execute()
                quiz_scores.extend([q['score'] for q in quizzes.data])
            
            # Calculate average performance
            avg_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
            
            return {
                'current_grade': self._score_to_gcse_grade(avg_score),
                'average_score': avg_score,
                'total_topics': len(topics.data),
                'total_quizzes': len(quiz_scores),
                'strengths': [],
                'weaknesses': []
            }
            
        except Exception as e:
            print(f"Error getting user GCSE performance: {e}")
            return {'current_grade': 'Unknown', 'strengths': [], 'weaknesses': []}
    
    def _score_to_gcse_grade(self, score: float) -> str:
        """Convert numerical score to GCSE grade (9-1)"""
        if score >= 90:
            return '9'
        elif score >= 80:
            return '8'
        elif score >= 70:
            return '7'
        elif score >= 60:
            return '6'
        elif score >= 50:
            return '5'
        elif score >= 40:
            return '4'
        elif score >= 30:
            return '3'
        elif score >= 20:
            return '2'
        else:
            return '1'
    
    def _create_gcse_study_plan(self, curriculum_data: Dict, target_grade: str, days_until_exam: int, user_performance: Dict, exam_board: str) -> Dict:
        """Create comprehensive GCSE study plan"""
        if not self.client:
            return {'error': 'AI study plan generation unavailable'}
        
        try:
            # Get subject from curriculum_data or use a default
            subject = curriculum_data.get('subject', 'the subject') if curriculum_data else 'the subject'
            current_grade = user_performance.get('current_grade', 'unknown') if user_performance else 'unknown'
            
            prompt = f"""
            Create a comprehensive GCSE study plan for {subject} (Exam Board: {exam_board}).
            
            Current Performance: Grade {current_grade} (Target: Grade {target_grade})
            Days until exam: {days_until_exam}
            
            IMPORTANT: Return ONLY valid JSON. Do not include any text before or after the JSON.
            
            Create a detailed study plan with the following structure:
            {{
                "GCSE_{subject}_Study_Plan": {{
                    "Weekly_Study_Schedule": {{
                        "Monday": "Topic to study",
                        "Tuesday": "Topic to study",
                        "Wednesday": "Topic to study",
                        "Thursday": "Topic to study",
                        "Friday": "Revision",
                        "Saturday": "Practice Questions",
                        "Sunday": "Rest/Review"
                    }},
                    "Exam_Preparation_Timeline": {{
                        "Months_1-3": "Phase 1 description",
                        "Months_3-6": "Phase 2 description",
                        "Months_6-12": "Phase 3 description"
                    }},
                    "Topic_Prioritization": {{
                        "Priority_1": "Most important topic",
                        "Priority_2": "Second priority",
                        "Priority_3": "Third priority",
                        "Priority_4": "Fourth priority"
                    }},
                    "Practice_Exam_Schedule": {{
                        "Month_1": "Practice activity",
                        "Month_2": "Practice activity",
                        "Month_3": "Practice activity",
                        "Month_4": "Practice activity"
                    }},
                    "Revision_Techniques": {{
                        "1. Flashcards": "Description",
                        "2. Mind Maps": "Description",
                        "3. Practice Problems": "Description",
                        "4. Teaching Others": "Description",
                        "5. Regular Reviews": "Description"
                    }}
                }}
            }}
            
            Make it specific to {subject} GCSE curriculum and suitable for achieving Grade {target_grade}.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert GCSE tutor. Create detailed, practical study plans in valid JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            # Parse JSON with error handling
            content = response.choices[0].message.content.strip()
            
            # Clean up markdown fences
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            
            # Find JSON in content
            start_idx = content.find('{')
            if start_idx != -1:
                content = content[start_idx:]
            
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            print(f"Error parsing GCSE study plan JSON: {e}")
            import traceback
            traceback.print_exc()
            return {'error': 'Failed to parse study plan'}
        except Exception as e:
            print(f"Error creating GCSE study plan: {e}")
            import traceback
            traceback.print_exc()
            return {'error': 'Failed to create study plan'}
    
    def _save_gcse_study_plan(self, subject: str, exam_board: str, target_grade: str, study_plan: Dict):
        """Save GCSE study plan to database"""
        if not self.supabase:
            return
        
        try:
            plan_data = {
                'user_id': self.user_id,
                'subject': subject,
                'exam_board': exam_board,
                'target_grade': target_grade,
                'study_plan': json.dumps(study_plan),
                'created_at': datetime.now().isoformat()
            }
            
            self.supabase.table('gcse_study_plans').insert(plan_data).execute()
            
        except Exception as e:
            print(f"Error saving GCSE study plan: {e}")
    
    # Additional helper methods would be implemented here...
    def _get_gcse_past_papers(self, subject: str, exam_board: str, paper_type: str) -> List[Dict]:
        """Get GCSE past papers data"""
        # Since we don't have a past papers database, return metadata for AI to work with
        return [{'subject': subject, 'exam_board': exam_board, 'paper_type': paper_type}]
    
    def _analyze_gcse_question_patterns(self, past_paper_data: List[Dict]) -> Dict:
        """Analyze GCSE question patterns using AI"""
        if not self.client or not past_paper_data:
            return {'patterns': ['Common question patterns analysis unavailable'], 'frequency': {}}
        
        try:
            subject = past_paper_data[0].get('subject', 'the subject')
            exam_board = past_paper_data[0].get('exam_board', 'exam board')
            
            prompt = f"""
            Analyze common question patterns in GCSE {subject} past papers for {exam_board}.
            
            List 5-7 common question types or patterns that frequently appear.
            
            Return as a simple list of patterns.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE exam expert. Provide concise, practical analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            # Parse response into list
            content = response.choices[0].message.content.strip()
            patterns = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return {'patterns': patterns[:7], 'frequency': {}}
            
        except Exception as e:
            print(f"Error analyzing question patterns: {e}")
            return {'patterns': ['Question pattern analysis in progress'], 'frequency': {}}
    
    def _calculate_topic_importance(self, past_paper_data: List[Dict]) -> Dict:
        """Calculate topic importance from past papers using AI"""
        if not self.client or not past_paper_data:
            return {'topics': ['Topic importance analysis unavailable'], 'importance_scores': {}}
        
        try:
            subject = past_paper_data[0].get('subject', 'the subject')
            
            prompt = f"""
            List the 6 most important topics for GCSE {subject} based on their frequency in past papers.
            
            Return just the topic names, one per line, in order of importance.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE curriculum expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            topics = [line.strip().lstrip('1234567890.-) ') for line in content.split('\n') if line.strip()]
            
            return {'topics': topics[:6], 'importance_scores': {}}
            
        except Exception as e:
            print(f"Error calculating topic importance: {e}")
            return {'topics': ['Topic analysis in progress'], 'importance_scores': {}}
    
    def _generate_gcse_exam_strategies(self, question_analysis: Dict, topic_importance: Dict) -> List[str]:
        """Generate GCSE exam strategies using AI"""
        if not self.client:
            return ['Exam strategies: AI generation unavailable']
        
        try:
            prompt = """
            Provide 5 practical exam strategies for GCSE students.
            
            Focus on:
            - Time management
            - Question technique
            - Mark allocation
            - Common mistakes to avoid
            
            Return as a numbered list.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE exam coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            strategies = [line.strip().lstrip('1234567890.-) ') for line in content.split('\n') if line.strip() and len(line.strip()) > 10]
            
            return strategies[:5]
            
        except Exception as e:
            print(f"Error generating exam strategies: {e}")
            return ['Exam strategies generation in progress']
    
    def _generate_gcse_practice_recommendations(self, question_analysis: Dict) -> List[str]:
        """Generate GCSE practice recommendations using AI"""
        if not self.client:
            return ['Practice recommendations: AI generation unavailable']
        
        try:
            prompt = """
            Provide 5 specific practice recommendations for GCSE students preparing for exams.
            
            Focus on:
            - What to practice
            - How often
            - Which resources to use
            - Practice techniques
            
            Return as a numbered list.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE study advisor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            recommendations = [line.strip().lstrip('1234567890.-) ') for line in content.split('\n') if line.strip() and len(line.strip()) > 10]
            
            return recommendations[:5]
            
        except Exception as e:
            print(f"Error generating practice recommendations: {e}")
            return ['Practice recommendations generation in progress']
    
    def _get_gcse_grade_boundaries(self, subject: str, exam_board: str) -> Dict:
        """Get historical GCSE grade boundaries"""
        return {'boundaries': {}, 'trends': []}
    
    def _analyze_gcse_performance_trends(self, current_performance: Dict) -> Dict:
        """Analyze GCSE performance trends"""
        return {'trend': 'stable', 'velocity': 0}
    
    def _predict_grade_boundaries(self, grade_boundaries: Dict, performance_trends: Dict) -> Dict:
        """Predict grade boundaries for current year"""
        # Generate realistic grade boundaries (typical GCSE boundaries)
        return {
            '9': 85,
            '8': 75,
            '7': 65,
            '6': 55,
            '5': 45,
            '4': 35,
            '3': 25,
            '2': 15,
            '1': 5
        }
    
    def _calculate_predicted_grade(self, current_performance: Dict, predicted_boundaries: Dict) -> str:
        """Calculate predicted grade for student"""
        # Get current score/grade
        current_grade = current_performance.get('current_grade', 5)
        average_score = current_performance.get('average_score', 50)
        
        # If we have a numeric grade, use it
        if isinstance(current_grade, (int, float)):
            return str(int(current_grade))
        
        # If we have a score, calculate grade from boundaries
        if predicted_boundaries and 'predicted_boundaries' in predicted_boundaries:
            boundaries = predicted_boundaries['predicted_boundaries']
        else:
            boundaries = predicted_boundaries
        
        # Match score to grade
        for grade in ['9', '8', '7', '6', '5', '4', '3', '2', '1']:
            if average_score >= boundaries.get(grade, 0):
                return grade
        
        return '4'  # Default to grade 4
    
    def _generate_gcse_improvement_plan(self, current_performance: Dict, predicted_grade: str, predicted_boundaries: Dict) -> Dict:
        """Generate GCSE improvement plan using AI"""
        if not self.client:
            return {
                'plan': ['Improvement plan: AI generation unavailable'],
                'recommendations': ['Set up OpenAI API key for personalized recommendations']
            }
        
        try:
            current_grade = current_performance.get('current_grade', 'unknown')
            weak_areas = current_performance.get('weak_areas', [])
            
            prompt = f"""
            Create an improvement plan for a GCSE student.
            
            Current Grade: {current_grade}
            Predicted Grade: {predicted_grade}
            Weak Areas: {', '.join(weak_areas) if weak_areas else 'General improvement needed'}
            
            Provide:
            1. 3-5 specific action steps to improve
            2. 3-5 study recommendations
            
            Format as simple lists.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE academic advisor providing practical improvement plans."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            lines = [line.strip().lstrip('1234567890.-) ') for line in content.split('\n') if line.strip() and len(line.strip()) > 10]
            
            # Split into plan and recommendations
            mid_point = len(lines) // 2
            plan = lines[:mid_point] if mid_point > 0 else lines[:3]
            recommendations = lines[mid_point:] if mid_point > 0 else lines[3:]
            
            return {
                'plan': plan[:5],
                'recommendations': recommendations[:5] if recommendations else ['Continue regular study', 'Practice past papers', 'Seek teacher feedback']
            }
            
        except Exception as e:
            print(f"Error generating improvement plan: {e}")
            return {
                'plan': ['Review weak topics regularly', 'Practice exam questions', 'Seek additional help'],
                'recommendations': ['Stay consistent', 'Track progress', 'Ask questions']
            }
    
    def _calculate_prediction_confidence(self, performance_trends: Dict) -> float:
        """Calculate prediction confidence"""
        # Return a realistic confidence level
        trend = performance_trends.get('trend', 'stable')
        if trend == 'improving':
            return 85.0
        elif trend == 'declining':
            return 65.0
        else:
            return 75.0
    
    def _organize_exam_schedule(self, exam_dates: Dict[str, str]) -> List[Dict]:
        """Organize exam schedule by priority"""
        return []
    
    def _calculate_subject_priorities(self, subjects: List[str], target_grades: Dict[str, str], exam_schedule: List[Dict]) -> Dict:
        """Calculate subject priorities"""
        return {'priorities': {}}
    
    def _generate_daily_revision_schedule(self, subject_priorities: Dict, exam_schedule: List[Dict]) -> Dict:
        """Generate daily revision schedule"""
        return {'schedule': []}
    
    def _generate_subject_revision_plan(self, subject: str, exam_date: str, target_grade: str) -> Dict:
        """Generate subject-specific revision plan"""
        return {'plan': []}
    
    def _generate_gcse_wellbeing_plan(self, exam_schedule: List[Dict]) -> Dict:
        """Generate GCSE wellbeing and stress management plan"""
        return {'wellbeing': []}
    
    def _get_gcse_exam_format(self, subject: str, exam_board: str) -> Dict:
        """Get GCSE exam format information"""
        return {'format': {}}
    
    def _generate_question_specific_techniques(self, question_types: List[str], exam_format: Dict) -> List[str]:
        """Generate question-specific techniques using AI"""
        try:
            prompt = f"""Generate specific exam techniques for these GCSE question types: {', '.join(question_types)}.
            
For each question type, provide practical, actionable techniques that students can apply.
Focus on:
- How to approach each question type
- Common pitfalls to avoid
- Marking scheme awareness
- Time-saving strategies

Return ONLY a list of clear, specific techniques (5-7 techniques).
Format: Just the list of techniques as strings, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE exam technique expert. Provide clear, practical advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse into list
            techniques = [line.strip('- ').strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return techniques if techniques else [
                "Read all questions carefully before starting",
                "Allocate time based on marks available",
                "Show all your working clearly",
                "Check your answers if time permits",
                "Answer the question that's asked, not what you wish was asked"
            ]
            
        except Exception as e:
            print(f"Error generating question techniques: {e}")
            return [
                "Read all questions carefully before starting",
                "Allocate time based on marks available",
                "Show all your working clearly"
            ]
    
    def _generate_gcse_time_management_strategies(self, exam_format: Dict) -> List[str]:
        """Generate GCSE time management strategies using AI"""
        try:
            prompt = f"""Generate time management strategies for a GCSE exam.
            
Provide practical time management tips that help students:
- Allocate time efficiently
- Pace themselves through the exam
- Handle time pressure
- Prioritize questions

Return ONLY a list of 5-7 specific time management strategies.
Format: Just the list as strings, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE exam strategy expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse into list
            strategies = [line.strip('- ').strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return strategies if strategies else [
                "Spend roughly 1 minute per mark",
                "Allocate 5 minutes at the start to read all questions",
                "Leave 10 minutes at the end for checking",
                "If stuck on a question, move on and return later"
            ]
            
        except Exception as e:
            print(f"Error generating time management strategies: {e}")
            return [
                "Spend roughly 1 minute per mark",
                "Leave time for checking at the end"
            ]
    
    def _generate_gcse_marking_insights(self, subject: str, exam_board: str) -> List[str]:
        """Generate GCSE marking scheme insights"""
        try:
            prompt = f"""Generate marking scheme insights for GCSE {subject} ({exam_board}).
            
Provide insights about:
- What examiners look for
- How marks are awarded
- Common marking criteria
- Key assessment objectives

Return ONLY a list of 5-7 specific insights about marking.
Format: Just the list as strings, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE marking expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse into list
            insights = [line.strip('- ').strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return insights if insights else [
                "Examiners award marks for method as well as answers",
                "Quality of written communication can gain extra marks",
                "Technical terminology is often required for full marks"
            ]
            
        except Exception as e:
            print(f"Error generating marking insights: {e}")
            return [
                "Show your working to gain method marks",
                "Use subject-specific terminology"
            ]
    
    def _generate_gcse_mistake_avoidance_guide(self, subject: str, exam_board: str) -> List[str]:
        """Generate GCSE mistake avoidance guide"""
        try:
            prompt = f"""Generate common mistakes to avoid in GCSE {subject} exams ({exam_board}).
            
Provide practical advice about:
- Common student errors
- Misconceptions to avoid
- Technical mistakes
- Answer presentation issues

Return ONLY a list of 5-7 specific mistakes to avoid.
Format: Just the list as strings, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE exam expert who helps students avoid common mistakes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse into list
            mistakes = [line.strip('- ').strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return mistakes if mistakes else [
                "Don't forget to include units in your final answer",
                "Avoid rounding too early in calculations",
                "Always check the number of marks to guide answer length"
            ]
            
        except Exception as e:
            print(f"Error generating mistake avoidance guide: {e}")
            return [
                "Read questions carefully",
                "Check your working"
            ]
    
    def _get_gcse_topic_requirements(self, subject: str, topic: str) -> Dict:
        """Get GCSE topic requirements"""
        return {'requirements': []}
    
    def _generate_gcse_visual_content(self, subject: str, topic: str, requirements: Dict) -> Dict:
        """Generate GCSE visual content using AI"""
        try:
            prompt = f"""Generate visual learning content for GCSE {subject} on the topic: {topic}

Create content optimized for VISUAL learners including:
1. Descriptions of diagrams, charts, or mind maps to create
2. Visual patterns or relationships to recognize
3. Color-coding or highlighting strategies
4. Visual mnemonics or memory aids
5. Graph or table interpretations

Provide 5-7 visual learning strategies.
Format: Just the list, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE teacher specializing in visual learning methods."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            content_text = response.choices[0].message.content.strip()
            learning_points = [line.strip('- ').strip() for line in content_text.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return {
                'content': content_text,
                'learning_points': learning_points
            }
            
        except Exception as e:
            print(f"Error generating visual content: {e}")
            return {
                'content': f"Visual learners should create diagrams and mind maps for {topic}.",
                'learning_points': [f"Create visual diagrams for {topic}", "Use color coding", "Draw mind maps"]
            }
    
    def _generate_gcse_auditory_content(self, subject: str, topic: str, requirements: Dict) -> Dict:
        """Generate GCSE auditory content using AI"""
        try:
            prompt = f"""Generate auditory learning content for GCSE {subject} on the topic: {topic}

Create content optimized for AUDITORY learners including:
1. Discussion points and verbal explanations
2. Memory rhymes or songs
3. Teaching points (explain to others)
4. Audio-based study techniques
5. Verbal repetition strategies

Provide 5-7 auditory learning strategies.
Format: Just the list, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE teacher specializing in auditory learning methods."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            content_text = response.choices[0].message.content.strip()
            learning_points = [line.strip('- ').strip() for line in content_text.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return {
                'content': content_text,
                'learning_points': learning_points
            }
            
        except Exception as e:
            print(f"Error generating auditory content: {e}")
            return {
                'content': f"Auditory learners should discuss and explain {topic} verbally.",
                'learning_points': [f"Explain {topic} to others", "Record and listen to notes", "Use mnemonics"]
            }
    
    def _generate_gcse_kinesthetic_content(self, subject: str, topic: str, requirements: Dict) -> Dict:
        """Generate GCSE kinesthetic content using AI"""
        try:
            prompt = f"""Generate kinesthetic learning content for GCSE {subject} on the topic: {topic}

Create content optimized for KINESTHETIC learners including:
1. Hands-on activities or experiments
2. Physical models or manipulatives to create
3. Movement-based memory techniques
4. Practical applications
5. Active learning exercises

Provide 5-7 kinesthetic learning strategies.
Format: Just the list, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE teacher specializing in kinesthetic learning methods."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            content_text = response.choices[0].message.content.strip()
            learning_points = [line.strip('- ').strip() for line in content_text.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return {
                'content': content_text,
                'learning_points': learning_points
            }
            
        except Exception as e:
            print(f"Error generating kinesthetic content: {e}")
            return {
                'content': f"Kinesthetic learners should engage with {topic} through hands-on activities.",
                'learning_points': [f"Build models related to {topic}", "Conduct experiments", "Use flashcards with movement"]
            }
    
    def _generate_gcse_multi_modal_content(self, subject: str, topic: str, requirements: Dict) -> Dict:
        """Generate comprehensive GCSE content using AI"""
        try:
            prompt = f"""Generate comprehensive GCSE {subject} content for the topic: {topic}

Create detailed learning content suitable for GCSE students including:
1. Core concepts and definitions (3-5 key points)
2. Detailed explanations with examples
3. Important formulas or rules (if applicable)
4. Common misconceptions to avoid
5. Links to related topics

Make it clear, educational, and appropriate for GCSE level.
Return the content as structured information."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert GCSE teacher creating educational content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            content_text = response.choices[0].message.content.strip()
            
            # Split into learning points
            lines = [line.strip() for line in content_text.split('\n') if line.strip()]
            learning_points = [line.strip('- ').strip() for line in lines if line.strip() and not line.strip().startswith('#')]
            
            return {
                'content': content_text,
                'learning_points': learning_points[:10] if learning_points else []
            }
            
        except Exception as e:
            print(f"Error generating multi-modal content: {e}")
            return {
                'content': f"Study {topic} by understanding the core concepts, practicing problems, and reviewing examples.",
                'learning_points': [f"Understand the fundamental principles of {topic}", "Practice regularly", "Review examples"]
            }
    
    def _adapt_content_to_difficulty(self, content: Dict, difficulty_level: str, requirements: Dict) -> Dict:
        """Adapt content to difficulty level - return enhanced content"""
        # Content is already generated, just pass through with added metadata
        content['difficulty_level'] = difficulty_level
        return content
    
    def _add_gcse_exam_preparation(self, content: Dict, subject: str, topic: str) -> Dict:
        """Add GCSE exam preparation elements using AI"""
        try:
            # Generate practice questions
            questions_prompt = f"""Generate 3 GCSE {subject} exam-style questions about {topic}.

For each question:
- Make it realistic for GCSE exams
- Include mark allocation [X marks]
- Add a helpful tip for answering

Format each question clearly."""

            questions_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE examiner creating practice questions."},
                    {"role": "user", "content": questions_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            questions_text = questions_response.choices[0].message.content.strip()
            questions = []
            
            # Parse questions
            for line in questions_text.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    questions.append(line.strip())
            
            # Generate examples
            examples_prompt = f"""Provide 2 worked examples for GCSE {subject} on {topic}.

Make each example:
- Clear and step-by-step
- Appropriate for GCSE level
- Show the complete solution process

Keep each example concise but complete."""

            examples_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE teacher creating worked examples."},
                    {"role": "user", "content": examples_prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            examples_text = examples_response.choices[0].message.content.strip()
            examples = [ex.strip() for ex in examples_text.split('\n\n') if ex.strip()]
            
            # Generate study recommendations
            recs_prompt = f"""Provide 5 specific study recommendations for GCSE students learning about {topic} in {subject}.

Each recommendation should be:
- Practical and actionable
- Specific to this topic
- Helpful for exam preparation"""

            recs_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE study advisor."},
                    {"role": "user", "content": recs_prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            recs_text = recs_response.choices[0].message.content.strip()
            recommendations = [line.strip('- ').strip() for line in recs_text.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            # Add to content
            content['practice_questions'] = questions[:3] if questions else [
                f"Explain the key concepts of {topic}. [4 marks]",
                f"Apply {topic} to solve a problem. [6 marks]"
            ]
            content['examples'] = examples[:2] if examples else [
                f"Work through a basic example of {topic}",
                f"Solve a more complex problem involving {topic}"
            ]
            content['study_recommendations'] = recommendations[:5] if recommendations else [
                f"Practice problems related to {topic}",
                "Review past paper questions",
                "Create summary notes"
            ]
            content['curriculum_requirements'] = [
                f"Understanding of {topic}",
                f"Application of {topic} to problems",
                "Exam technique and answer structure"
            ]
            
            return content
            
        except Exception as e:
            print(f"Error adding exam preparation: {e}")
            content['practice_questions'] = [f"Practice questions for {topic}"]
            content['examples'] = [f"Example problems for {topic}"]
            content['study_recommendations'] = ["Practice regularly", "Review notes"]
            return content
    
    def _get_gcse_curriculum_standards(self, subject: str) -> Dict:
        """Get GCSE curriculum standards"""
        return {'standards': []}
    
    def _identify_gcse_performance_gaps(self, user_performance: Dict, curriculum_standards: Dict) -> List[str]:
        """Identify GCSE performance gaps using AI"""
        try:
            current_grade = user_performance.get('current_grade', 5)
            target_grade = user_performance.get('target_grade', 7)
            gap = target_grade - current_grade
            
            if gap <= 0:
                return []
            
            prompt = f"""Identify specific performance gaps for a GCSE student who is currently at Grade {current_grade} and aiming for Grade {target_grade}.

Based on this {gap} grade gap, identify 5-7 specific areas where the student is likely underperforming:
- Knowledge gaps
- Skill deficiencies
- Common weak points for students at this level
- Areas that typically need improvement to reach the target grade

Return ONLY a list of specific performance gaps.
Format: Just the list as strings, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE performance assessment expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            gaps = [line.strip('- ').strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return gaps if gaps else [
                "Understanding of core concepts needs strengthening",
                "Exam technique and answer structure could be improved",
                "Time management during exams",
                "Application of knowledge to unfamiliar contexts"
            ]
            
        except Exception as e:
            print(f"Error identifying performance gaps: {e}")
            return ["Core concept understanding", "Exam technique", "Time management"]
    
    def _prioritize_performance_gaps(self, performance_gaps: List[str]) -> List[str]:
        """Prioritize performance gaps - return as-is since AI already prioritizes"""
        return performance_gaps
    
    def _generate_targeted_improvement_strategies(self, prioritized_gaps: List[str], subject: str) -> List[str]:
        """Generate targeted improvement strategies using AI"""
        try:
            gaps_text = '\n'.join(f"- {gap}" for gap in prioritized_gaps[:5])
            
            prompt = f"""Generate specific improvement strategies for a GCSE {subject} student with these performance gaps:

{gaps_text}

Provide 6-8 targeted, actionable strategies that directly address these gaps.
Each strategy should be:
- Specific and practical
- Directly addressing one or more gaps
- Achievable for a GCSE student
- Results-oriented

Return ONLY a list of improvement strategies.
Format: Just the list as strings, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE study strategy expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            content = response.choices[0].message.content.strip()
            strategies = [line.strip('- ').strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return strategies if strategies else [
                "Create detailed revision notes for each topic",
                "Practice past papers under timed conditions",
                "Focus on understanding 'why' not just 'how'",
                "Seek feedback from teachers on practice work"
            ]
            
        except Exception as e:
            print(f"Error generating improvement strategies: {e}")
            return ["Review core concepts", "Practice regularly", "Seek help when needed"]
    
    def _generate_gcse_practice_recommendations_for_gaps(self, prioritized_gaps: List[str]) -> List[str]:
        """Generate GCSE practice recommendations using AI"""
        try:
            gaps_text = '\n'.join(f"- {gap}" for gap in prioritized_gaps[:5])
            
            prompt = f"""Generate specific practice recommendations for a GCSE student with these gaps:

{gaps_text}

Provide 5-7 specific practice activities or resources that will help address these gaps.
Include:
- Specific types of questions to practice
- Topics to focus on
- Practice techniques
- Resources to use

Return ONLY a list of practice recommendations.
Format: Just the list as strings, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE practice and revision expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            recommendations = [line.strip('- ').strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return recommendations if recommendations else [
                "Complete 2-3 past papers per week",
                "Create and test yourself with flashcards",
                "Practice answering exam-style questions",
                "Review mark schemes to understand requirements"
            ]
            
        except Exception as e:
            print(f"Error generating practice recommendations: {e}")
            return ["Practice past papers", "Review mark schemes"]
    
    def _generate_gcse_progress_tracking_plan(self, prioritized_gaps: List[str]) -> List[str]:
        """Generate GCSE progress tracking plan using AI"""
        try:
            prompt = f"""Generate a progress tracking plan for a GCSE student working to improve their grade.

Provide 5-7 specific ways the student can track their progress and measure improvement:
- Regular assessment methods
- Self-monitoring techniques
- Milestone setting
- Progress indicators to watch for

Return ONLY a list of progress tracking methods.
Format: Just the list as strings, no extra explanation."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GCSE progress monitoring expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            tracking = [line.strip('- ').strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            
            return tracking if tracking else [
                "Complete weekly practice tests and track scores",
                "Keep a progress journal noting improvements",
                "Review past papers monthly to measure progress",
                "Set weekly goals and review achievement"
            ]
            
        except Exception as e:
            print(f"Error generating progress tracking plan: {e}")
            return ["Track test scores", "Review progress weekly"]

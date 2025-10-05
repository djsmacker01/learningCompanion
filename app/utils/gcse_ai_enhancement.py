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
            # Get historical grade boundaries
            grade_boundaries = self._get_gcse_grade_boundaries(subject, exam_board)
            
            # Analyze current performance trends
            performance_trends = self._analyze_gcse_performance_trends(current_performance)
            
            # Predict grade boundaries for current year
            predicted_boundaries = self._predict_grade_boundaries(grade_boundaries, performance_trends)
            
            # Calculate student's predicted grade
            predicted_grade = self._calculate_predicted_grade(current_performance, predicted_boundaries)
            
            # Generate improvement recommendations
            improvement_plan = self._generate_gcse_improvement_plan(current_performance, predicted_grade, predicted_boundaries)
            
            return {
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
            
        except Exception as e:
            print(f"Error predicting GCSE grade boundaries: {e}")
            return {'error': 'Failed to predict grade boundaries'}
    
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
            
            return {
                'subject': subject,
                'topic': topic,
                'learning_style': learning_style,
                'difficulty_level': difficulty_level,
                'curriculum_requirements': curriculum_requirements,
                'content': exam_prep_content,
                'generated_at': datetime.now().isoformat()
            }
            
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
            prompt = f"""
            Create a comprehensive GCSE study plan for {curriculum_data['subject']} (Exam Board: {exam_board}).
            
            Current Performance: {user_performance['current_grade']} (Target: {target_grade})
            Days until exam: {days_until_exam}
            
            Include:
            1. Weekly study schedule
            2. Topic prioritization
            3. Practice exam schedule
            4. Revision techniques
            5. Exam preparation timeline
            
            Format as structured JSON with daily/weekly breakdowns.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert GCSE tutor. Create detailed, practical study plans."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content.strip())
            
        except Exception as e:
            print(f"Error creating GCSE study plan: {e}")
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
        return []
    
    def _analyze_gcse_question_patterns(self, past_paper_data: List[Dict]) -> Dict:
        """Analyze GCSE question patterns"""
        return {'patterns': [], 'frequency': {}}
    
    def _calculate_topic_importance(self, past_paper_data: List[Dict]) -> Dict:
        """Calculate topic importance from past papers"""
        return {'topics': [], 'importance_scores': {}}
    
    def _generate_gcse_exam_strategies(self, question_analysis: Dict, topic_importance: Dict) -> List[str]:
        """Generate GCSE exam strategies"""
        return ['Strategy 1', 'Strategy 2']
    
    def _generate_gcse_practice_recommendations(self, question_analysis: Dict) -> List[str]:
        """Generate GCSE practice recommendations"""
        return ['Practice 1', 'Practice 2']
    
    def _get_gcse_grade_boundaries(self, subject: str, exam_board: str) -> Dict:
        """Get historical GCSE grade boundaries"""
        return {'boundaries': {}, 'trends': []}
    
    def _analyze_gcse_performance_trends(self, current_performance: Dict) -> Dict:
        """Analyze GCSE performance trends"""
        return {'trend': 'stable', 'velocity': 0}
    
    def _predict_grade_boundaries(self, grade_boundaries: Dict, performance_trends: Dict) -> Dict:
        """Predict grade boundaries for current year"""
        return {'predicted_boundaries': {}}
    
    def _calculate_predicted_grade(self, current_performance: Dict, predicted_boundaries: Dict) -> str:
        """Calculate predicted grade for student"""
        return '5'
    
    def _generate_gcse_improvement_plan(self, current_performance: Dict, predicted_grade: str, predicted_boundaries: Dict) -> Dict:
        """Generate GCSE improvement plan"""
        return {'plan': [], 'recommendations': []}
    
    def _calculate_prediction_confidence(self, performance_trends: Dict) -> float:
        """Calculate prediction confidence"""
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
    
    def _generate_question_specific_techniques(self, question_types: List[str], exam_format: Dict) -> Dict:
        """Generate question-specific techniques"""
        return {'techniques': {}}
    
    def _generate_gcse_time_management_strategies(self, exam_format: Dict) -> Dict:
        """Generate GCSE time management strategies"""
        return {'strategies': []}
    
    def _generate_gcse_marking_insights(self, subject: str, exam_board: str) -> Dict:
        """Generate GCSE marking scheme insights"""
        return {'insights': []}
    
    def _generate_gcse_mistake_avoidance_guide(self, subject: str, exam_board: str) -> Dict:
        """Generate GCSE mistake avoidance guide"""
        return {'mistakes': []}
    
    def _get_gcse_topic_requirements(self, subject: str, topic: str) -> Dict:
        """Get GCSE topic requirements"""
        return {'requirements': []}
    
    def _generate_gcse_visual_content(self, subject: str, topic: str, requirements: Dict) -> Dict:
        """Generate GCSE visual content"""
        return {'visual_content': []}
    
    def _generate_gcse_auditory_content(self, subject: str, topic: str, requirements: Dict) -> Dict:
        """Generate GCSE auditory content"""
        return {'auditory_content': []}
    
    def _generate_gcse_kinesthetic_content(self, subject: str, topic: str, requirements: Dict) -> Dict:
        """Generate GCSE kinesthetic content"""
        return {'kinesthetic_content': []}
    
    def _generate_gcse_multi_modal_content(self, subject: str, topic: str, requirements: Dict) -> Dict:
        """Generate GCSE multi-modal content"""
        return {'multi_modal_content': []}
    
    def _adapt_content_to_difficulty(self, content: Dict, difficulty_level: str, requirements: Dict) -> Dict:
        """Adapt content to difficulty level"""
        return content
    
    def _add_gcse_exam_preparation(self, content: Dict, subject: str, topic: str) -> Dict:
        """Add GCSE exam preparation elements"""
        return content
    
    def _get_gcse_curriculum_standards(self, subject: str) -> Dict:
        """Get GCSE curriculum standards"""
        return {'standards': []}
    
    def _identify_gcse_performance_gaps(self, user_performance: Dict, curriculum_standards: Dict) -> List[Dict]:
        """Identify GCSE performance gaps"""
        return []
    
    def _prioritize_performance_gaps(self, performance_gaps: List[Dict]) -> List[Dict]:
        """Prioritize performance gaps"""
        return performance_gaps
    
    def _generate_targeted_improvement_strategies(self, prioritized_gaps: List[Dict], subject: str) -> Dict:
        """Generate targeted improvement strategies"""
        return {'strategies': []}
    
    def _generate_gcse_practice_recommendations_for_gaps(self, prioritized_gaps: List[Dict]) -> List[str]:
        """Generate GCSE practice recommendations for gaps"""
        return []
    
    def _generate_gcse_progress_tracking_plan(self, prioritized_gaps: List[Dict]) -> Dict:
        """Generate GCSE progress tracking plan"""
        return {'tracking': []}

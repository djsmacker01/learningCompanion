"""
Smart Content Generation System
AI-powered content creation for study materials, summaries, and interactive learning
"""

import openai
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from app.models import get_supabase_client, SUPABASE_AVAILABLE
from app.models import Topic
from dotenv import load_dotenv

load_dotenv()

class SmartContentGenerator:
    """AI-powered content generation system"""
    
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
    
    def generate_study_notes(self, topic_id: str, content_type: str = 'comprehensive') -> Dict:
        """Generate AI-powered study notes for a topic"""
        try:
            # Get topic information
            topic = Topic.get_by_id(topic_id, self.user_id)
            if not topic:
                return {'error': 'Topic not found'}
            
            # Get existing content and performance data
            content_context = self._get_topic_content_context(topic_id)
            
            # Generate notes based on type
            if content_type == 'comprehensive':
                notes = self._generate_comprehensive_notes(topic, content_context)
            elif content_type == 'summary':
                notes = self._generate_summary_notes(topic, content_context)
            elif content_type == 'key_points':
                notes = self._generate_key_points(topic, content_context)
            elif content_type == 'exam_focused':
                notes = self._generate_exam_focused_notes(topic, content_context)
            else:
                notes = self._generate_comprehensive_notes(topic, content_context)
            
            # Save generated content
            self._save_generated_content(topic_id, 'study_notes', notes, content_type)
            
            return {
                'topic_id': topic_id,
                'content_type': content_type,
                'notes': notes,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating study notes: {e}")
            return {'error': 'Failed to generate study notes'}
    
    def generate_interactive_content(self, topic_id: str, content_type: str = 'quiz') -> Dict:
        """Generate interactive learning content"""
        try:
            topic = Topic.get_by_id(topic_id, self.user_id)
            if not topic:
                return {'error': 'Topic not found'}
            
            content_context = self._get_topic_content_context(topic_id)
            
            if content_type == 'quiz':
                content = self._generate_interactive_quiz(topic, content_context)
            elif content_type == 'flashcards':
                content = self._generate_flashcards(topic, content_context)
            elif content_type == 'scenarios':
                content = self._generate_learning_scenarios(topic, content_context)
            elif content_type == 'exercises':
                content = self._generate_practice_exercises(topic, content_context)
            else:
                content = self._generate_interactive_quiz(topic, content_context)
            
            self._save_generated_content(topic_id, 'interactive_content', content, content_type)
            
            return {
                'topic_id': topic_id,
                'content_type': content_type,
                'content': content,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating interactive content: {e}")
            return {'error': 'Failed to generate interactive content'}
    
    def generate_visual_learning_aids(self, topic_id: str, visual_type: str = 'mind_map') -> Dict:
        """Generate visual learning aids"""
        try:
            topic = Topic.get_by_id(topic_id, self.user_id)
            if not topic:
                return {'error': 'Topic not found'}
            
            content_context = self._get_topic_content_context(topic_id)
            
            if visual_type == 'mind_map':
                visual = self._generate_mind_map(topic, content_context)
            elif visual_type == 'diagram':
                visual = self._generate_diagram(topic, content_context)
            elif visual_type == 'timeline':
                visual = self._generate_timeline(topic, content_context)
            elif visual_type == 'flowchart':
                visual = self._generate_flowchart(topic, content_context)
            else:
                visual = self._generate_mind_map(topic, content_context)
            
            self._save_generated_content(topic_id, 'visual_aids', visual, visual_type)
            
            return {
                'topic_id': topic_id,
                'visual_type': visual_type,
                'visual': visual,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating visual aids: {e}")
            return {'error': 'Failed to generate visual aids'}
    
    def generate_personalized_content(self, topic_id: str, learning_style: str = 'visual') -> Dict:
        """Generate personalized content based on learning style"""
        try:
            topic = Topic.get_by_id(topic_id, self.user_id)
            if not topic:
                return {'error': 'Topic not found'}
            
            content_context = self._get_topic_content_context(topic_id)
            user_profile = self._get_user_learning_profile()
            
            # Generate content adapted to learning style
            if learning_style == 'visual':
                content = self._generate_visual_content(topic, content_context, user_profile)
            elif learning_style == 'auditory':
                content = self._generate_auditory_content(topic, content_context, user_profile)
            elif learning_style == 'kinesthetic':
                content = self._generate_kinesthetic_content(topic, content_context, user_profile)
            elif learning_style == 'reading':
                content = self._generate_reading_content(topic, content_context, user_profile)
            else:
                content = self._generate_multi_modal_content(topic, content_context, user_profile)
            
            self._save_generated_content(topic_id, 'personalized_content', content, learning_style)
            
            return {
                'topic_id': topic_id,
                'learning_style': learning_style,
                'content': content,
                'user_profile': user_profile,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating personalized content: {e}")
            return {'error': 'Failed to generate personalized content'}
    
    def generate_content_summary(self, topic_id: str, summary_type: str = 'overview') -> Dict:
        """Generate various types of content summaries"""
        try:
            topic = Topic.get_by_id(topic_id, self.user_id)
            if not topic:
                return {'error': 'Topic not found'}
            
            content_context = self._get_topic_content_context(topic_id)
            
            if summary_type == 'overview':
                summary = self._generate_topic_overview(topic, content_context)
            elif summary_type == 'key_concepts':
                summary = self._generate_key_concepts_summary(topic, content_context)
            elif summary_type == 'exam_summary':
                summary = self._generate_exam_summary(topic, content_context)
            elif summary_type == 'quick_reference':
                summary = self._generate_quick_reference(topic, content_context)
            else:
                summary = self._generate_topic_overview(topic, content_context)
            
            self._save_generated_content(topic_id, 'summary', summary, summary_type)
            
            return {
                'topic_id': topic_id,
                'summary_type': summary_type,
                'summary': summary,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating content summary: {e}")
            return {'error': 'Failed to generate content summary'}
    
    def generate_learning_path(self, topic_id: str, difficulty_level: str = 'intermediate') -> Dict:
        """Generate a structured learning path for a topic"""
        try:
            topic = Topic.get_by_id(topic_id, self.user_id)
            if not topic:
                return {'error': 'Topic not found'}
            
            content_context = self._get_topic_content_context(topic_id)
            user_progress = self._get_user_progress(topic_id)
            
            learning_path = self._generate_structured_learning_path(topic, content_context, user_progress, difficulty_level)
            
            self._save_generated_content(topic_id, 'learning_path', learning_path, difficulty_level)
            
            return {
                'topic_id': topic_id,
                'difficulty_level': difficulty_level,
                'learning_path': learning_path,
                'user_progress': user_progress,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating learning path: {e}")
            return {'error': 'Failed to generate learning path'}
    
    # Helper methods for content generation
    def _get_topic_content_context(self, topic_id: str) -> Dict:
        """Get comprehensive context about the topic"""
        if not self.supabase:
            return {}
        
        try:
            # Get topic details
            topic = self.supabase.table('topics').select('*').eq('id', topic_id).execute()
            
            # Get study sessions
            sessions = self.supabase.table('study_sessions').select('*').eq('topic_id', topic_id).eq('user_id', self.user_id).execute()
            
            # Get quiz attempts
            quizzes = self.supabase.table('quiz_attempts').select('*').eq('quiz_id', topic_id).eq('user_id', self.user_id).execute()
            
            return {
                'topic': topic.data[0] if topic.data else None,
                'sessions': sessions.data if sessions.data else [],
                'quizzes': quizzes.data if quizzes.data else []
            }
            
        except Exception as e:
            print(f"Error getting topic context: {e}")
            return {}
    
    def _get_user_learning_profile(self) -> Dict:
        """Get user's learning profile and preferences"""
        if not self.supabase:
            return {'learning_style': 'visual', 'difficulty_preference': 'intermediate'}
        
        try:
            # Get learning style from AI learning styles table
            learning_style = self.supabase.table('ai_learning_styles').select('*').eq('user_id', self.user_id).execute()
            
            if learning_style.data:
                return {
                    'learning_style': learning_style.data[0].get('learning_style', 'visual'),
                    'confidence': learning_style.data[0].get('confidence_score', 50),
                    'recommendations': learning_style.data[0].get('recommendations', [])
                }
            else:
                return {'learning_style': 'visual', 'difficulty_preference': 'intermediate'}
                
        except Exception as e:
            print(f"Error getting learning profile: {e}")
            return {'learning_style': 'visual', 'difficulty_preference': 'intermediate'}
    
    def _get_user_progress(self, topic_id: str) -> Dict:
        """Get user's progress on the topic"""
        if not self.supabase:
            return {'progress': 0, 'confidence': 50}
        
        try:
            # Get recent quiz scores
            recent_quizzes = self.supabase.table('quiz_attempts').select('score').eq('quiz_id', topic_id).eq('user_id', self.user_id).order('created_at', desc=True).limit(5).execute()
            
            # Get study session data
            recent_sessions = self.supabase.table('study_sessions').select('confidence_after').eq('topic_id', topic_id).eq('user_id', self.user_id).order('session_date', desc=True).limit(5).execute()
            
            scores = [q['score'] for q in recent_quizzes.data] if recent_quizzes.data else []
            confidence_levels = [s['confidence_after'] for s in recent_sessions.data] if recent_sessions.data else []
            
            avg_score = sum(scores) / len(scores) if scores else 0
            avg_confidence = sum(confidence_levels) / len(confidence_levels) if confidence_levels else 50
            
            return {
                'progress': min(100, avg_score),
                'confidence': avg_confidence,
                'recent_scores': scores,
                'recent_confidence': confidence_levels
            }
            
        except Exception as e:
            print(f"Error getting user progress: {e}")
            return {'progress': 0, 'confidence': 50}
    
    def _save_generated_content(self, topic_id: str, content_type: str, content: Any, subtype: str):
        """Save generated content to database"""
        if not self.supabase:
            return
        
        try:
            content_data = {
                'user_id': self.user_id,
                'topic_id': topic_id,
                'content_type': content_type,
                'content_subtype': subtype,
                'content_data': json.dumps(content),
                'generated_at': datetime.now().isoformat()
            }
            
            self.supabase.table('generated_content').insert(content_data).execute()
            
        except Exception as e:
            print(f"Error saving generated content: {e}")
    
    # Content generation methods
    def _generate_comprehensive_notes(self, topic: Any, context: Dict) -> str:
        """Generate comprehensive study notes"""
        if not self.client:
            return "AI content generation unavailable. Please set up OpenAI API key."
        
        try:
            prompt = f"""
            Generate comprehensive study notes for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Create detailed, well-structured study notes that include:
            1. Key concepts and definitions
            2. Important facts and details
            3. Examples and applications
            4. Common questions and answers
            5. Study tips and mnemonics
            
            Format the notes in clear sections with headings.
            Make them suitable for GCSE-level study.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator. Create comprehensive, well-structured study notes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating comprehensive notes: {e}")
            return "Error generating study notes. Please try again."
    
    def _generate_summary_notes(self, topic: Any, context: Dict) -> str:
        """Generate summary notes"""
        if not self.client:
            return "AI content generation unavailable."
        
        try:
            prompt = f"""
            Create a concise summary of the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Include:
            - Main points in bullet format
            - Key definitions
            - Essential facts
            - Quick reference information
            
            Keep it concise but comprehensive.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating concise educational summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary notes: {e}")
            return "Error generating summary. Please try again."
    
    def _generate_key_points(self, topic: Any, context: Dict) -> List[str]:
        """Generate key points for the topic"""
        if not self.client:
            return ["AI content generation unavailable."]
        
        try:
            prompt = f"""
            Extract the key points for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Provide 5-8 key points that are essential for understanding this topic.
            Format as a simple list.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at identifying key learning points."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Parse response into list
            content = response.choices[0].message.content.strip()
            points = [point.strip() for point in content.split('\n') if point.strip()]
            return points
            
        except Exception as e:
            print(f"Error generating key points: {e}")
            return ["Error generating key points. Please try again."]
    
    def _generate_exam_focused_notes(self, topic: Any, context: Dict) -> str:
        """Generate exam-focused study notes"""
        if not self.client:
            return "AI content generation unavailable."
        
        try:
            prompt = f"""
            Create exam-focused study notes for: "{topic.title}"
            
            Description: {topic.description}
            
            Focus on:
            - Exam-style questions and answers
            - Common exam topics
            - Key formulas and concepts
            - Revision tips
            - Past paper insights
            
            Make it practical for exam preparation.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert exam preparation tutor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating exam notes: {e}")
            return "Error generating exam notes. Please try again."
    
    # Additional content generation methods would be implemented here...
    def _generate_interactive_quiz(self, topic: Any, context: Dict) -> Dict:
        """Generate interactive quiz content"""
        return {'questions': [], 'type': 'interactive_quiz'}
    
    def _generate_flashcards(self, topic: Any, context: Dict) -> List[Dict]:
        """Generate flashcard content"""
        return [{'front': 'Question', 'back': 'Answer'}]
    
    def _generate_learning_scenarios(self, topic: Any, context: Dict) -> List[Dict]:
        """Generate learning scenarios"""
        return [{'scenario': 'Example scenario', 'questions': []}]
    
    def _generate_practice_exercises(self, topic: Any, context: Dict) -> List[Dict]:
        """Generate practice exercises"""
        return [{'exercise': 'Practice problem', 'solution': 'Answer'}]
    
    def _generate_mind_map(self, topic: Any, context: Dict) -> Dict:
        """Generate mind map structure"""
        return {'nodes': [], 'connections': []}
    
    def _generate_diagram(self, topic: Any, context: Dict) -> Dict:
        """Generate diagram content"""
        return {'elements': [], 'layout': 'default'}
    
    def _generate_timeline(self, topic: Any, context: Dict) -> List[Dict]:
        """Generate timeline content"""
        return [{'date': '2024', 'event': 'Example event'}]
    
    def _generate_flowchart(self, topic: Any, context: Dict) -> Dict:
        """Generate flowchart content"""
        return {'steps': [], 'flow': 'linear'}
    
    def _generate_visual_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate visual learning content"""
        return {'visual_elements': [], 'type': 'visual'}
    
    def _generate_auditory_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate auditory learning content"""
        return {'audio_elements': [], 'type': 'auditory'}
    
    def _generate_kinesthetic_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate kinesthetic learning content"""
        return {'interactive_elements': [], 'type': 'kinesthetic'}
    
    def _generate_reading_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate reading-based content"""
        return {'text_elements': [], 'type': 'reading'}
    
    def _generate_multi_modal_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate multi-modal content"""
        return {'mixed_elements': [], 'type': 'multi_modal'}
    
    def _generate_topic_overview(self, topic: Any, context: Dict) -> str:
        """Generate topic overview"""
        return f"Overview of {topic.title}"
    
    def _generate_key_concepts_summary(self, topic: Any, context: Dict) -> Dict:
        """Generate key concepts summary"""
        return {'concepts': [], 'definitions': {}}
    
    def _generate_exam_summary(self, topic: Any, context: Dict) -> str:
        """Generate exam summary"""
        return f"Exam summary for {topic.title}"
    
    def _generate_quick_reference(self, topic: Any, context: Dict) -> Dict:
        """Generate quick reference guide"""
        return {'quick_facts': [], 'formulas': []}
    
    def _generate_structured_learning_path(self, topic: Any, context: Dict, progress: Dict, difficulty: str) -> Dict:
        """Generate structured learning path"""
        return {'steps': [], 'difficulty': difficulty, 'estimated_time': '2 hours'}

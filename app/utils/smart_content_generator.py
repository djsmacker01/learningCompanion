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
                'is_active': True
                # created_at and updated_at are auto-generated by database
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
        if not self.client:
            return {
                'questions': [
                    {
                        'question': 'AI content generation unavailable. Please set up OpenAI API key.',
                        'options': ['Please check your API configuration'],
                        'correct_answer': 0,
                        'explanation': 'This is a placeholder question.'
                    }
                ],
                'type': 'interactive_quiz',
                'title': f'Quiz: {topic.title}',
                'description': 'Interactive quiz for the selected topic'
            }
        
        try:
            prompt = f"""
            Create an interactive quiz for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate 5-7 multiple choice questions that test understanding of key concepts.
            For each question, provide:
            1. A clear, well-written question
            2. Four plausible answer options (A, B, C, D)
            3. The correct answer (0-3 index)
            4. A brief explanation of why the answer is correct
            
            Make the questions appropriate for GCSE level students.
            Focus on the most important concepts from this topic.
            
            IMPORTANT: Return ONLY valid JSON. Do not include any text before or after the JSON.
            The JSON must be properly formatted and parseable.
            
            Format your response as a JSON object with this structure:
            {{
                "title": "Quiz Title",
                "description": "Brief description",
                "questions": [
                    {{
                        "question": "Question text here?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": 0,
                        "explanation": "Explanation of correct answer"
                    }}
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational quiz creator. Create engaging, educational multiple choice questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            # Try to parse JSON response
            import json
            try:
                content = response.choices[0].message.content.strip()
                
                # Clean up the content - remove any text before/after JSON
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                # Try to find JSON in the content
                start_idx = content.find('{')
                if start_idx != -1:
                    content = content[start_idx:]
                
                quiz_data = json.loads(content)
                return quiz_data
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response from text
                import re
                content = response.choices[0].message.content.strip()
                
                # Try to extract questions from the text content
                questions = []
                lines = content.split('\n')
                current_question = None
                
                for line in lines:
                    line = line.strip()
                    if line and ('?' in line or line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.'))):
                        # This looks like a question
                        if current_question:
                            questions.append(current_question)
                        current_question = {
                            'question': re.sub(r'^\d+\.\s*', '', line),
                            'options': [],
                            'correct_answer': 0,
                            'explanation': 'This question was generated from AI content.'
                        }
                    elif line and (line.startswith(('A.', 'B.', 'C.', 'D.', 'a)', 'b)', 'c)', 'd)')) or 
                                   (len(line) > 10 and not line.startswith(('Question', 'Answer', 'Explanation')))):
                        # This looks like an option
                        if current_question and len(current_question['options']) < 4:
                            option_text = re.sub(r'^[A-D]\.\s*', '', line)
                            option_text = re.sub(r'^[a-d]\)\s*', '', option_text)
                            current_question['options'].append(option_text)
                
                # Add the last question
                if current_question and current_question['options']:
                    questions.append(current_question)
                
                # If no questions were extracted, create a fallback
                if not questions:
                    questions = [
                        {
                            'question': f'What is the main concept of {topic.title}?',
                            'options': [
                                'A key topic in the subject area',
                                'An important concept to understand',
                                'A fundamental principle',
                                'All of the above'
                            ],
                            'correct_answer': 3,
                            'explanation': f'This is a general question about {topic.title}. The correct answer covers all aspects of the topic.'
                        }
                    ]
                
                return {
                    'title': f'Quiz: {topic.title}',
                    'description': f'Interactive quiz for {topic.title}',
                    'questions': questions
                }
            
        except Exception as e:
            print(f"Error generating interactive quiz: {e}")
            return {
                'questions': [
                    {
                        'question': f'Error generating quiz for {topic.title}',
                        'options': ['Please try again', 'Check your internet connection', 'Contact support', 'Use a different topic'],
                        'correct_answer': 0,
                        'explanation': 'There was an error generating the quiz content. Please try again.'
                    }
                ],
                'type': 'interactive_quiz',
                'title': f'Quiz: {topic.title}',
                'error': str(e)
            }
    
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
        if not self.client:
            return {
                'title': f'Mind Map: {topic.title}',
                'description': 'AI content generation unavailable. Please set up OpenAI API key.',
                'nodes': [
                    {'id': 'center', 'label': topic.title, 'type': 'central', 'x': 0, 'y': 0},
                    {'id': 'placeholder', 'label': 'Please set up API key', 'type': 'branch', 'x': 100, 'y': 0}
                ],
                'connections': [{'from': 'center', 'to': 'placeholder'}]
            }
        
        try:
            prompt = f"""
            Create a mind map structure for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate a hierarchical mind map with:
            1. A central node (the main topic) at position (0, 0)
            2. 3-5 main branches (major concepts) arranged in a circle around the center
            3. 2-3 sub-branches for each main branch (sub-concepts) positioned near their parent
            4. Connections between nodes
            
            IMPORTANT: Use organized positioning:
            - Central node: (0, 0)
            - Main branches: Arrange in a circle around center, 150px radius
            - Sub-branches: Position 100px from their parent node
            
            Format your response as a JSON object with this structure:
            {{
                "title": "Mind Map Title",
                "description": "Brief description of the mind map",
                "nodes": [
                    {{"id": "center", "label": "{topic.title}", "type": "central", "x": 0, "y": 0}},
                    {{"id": "branch1", "label": "Main Concept 1", "type": "main", "x": -150, "y": -100}},
                    {{"id": "branch2", "label": "Main Concept 2", "type": "main", "x": 150, "y": -100}},
                    {{"id": "branch3", "label": "Main Concept 3", "type": "main", "x": 0, "y": -150}},
                    {{"id": "sub1", "label": "Sub-concept", "type": "sub", "x": -250, "y": -150}}
                ],
                "connections": [
                    {{"from": "center", "to": "branch1"}},
                    {{"from": "center", "to": "branch2"}},
                    {{"from": "branch1", "to": "sub1"}}
                ]
            }}
            
            Make it educational and suitable for GCSE level students.
            Ensure nodes are well-organized and not scattered.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating educational mind maps. Create clear, hierarchical structures that help students understand topics."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Try to parse JSON response
            import json
            try:
                mind_map_data = json.loads(response.choices[0].message.content.strip())
                return mind_map_data
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                content = response.choices[0].message.content.strip()
                return {
                    'title': f'Mind Map: {topic.title}',
                    'description': f'Visual mind map for {topic.title}',
                    'nodes': [
                        {'id': 'center', 'label': topic.title, 'type': 'central', 'x': 0, 'y': 0},
                        {'id': 'concept1', 'label': 'Key Concept 1', 'type': 'main', 'x': -120, 'y': -80},
                        {'id': 'concept2', 'label': 'Key Concept 2', 'type': 'main', 'x': 120, 'y': -80},
                        {'id': 'concept3', 'label': 'Key Concept 3', 'type': 'main', 'x': 0, 'y': -120},
                        {'id': 'concept4', 'label': 'Key Concept 4', 'type': 'main', 'x': 0, 'y': 120},
                        {'id': 'sub1', 'label': 'Sub-concept 1', 'type': 'sub', 'x': -200, 'y': -120},
                        {'id': 'sub2', 'label': 'Sub-concept 2', 'type': 'sub', 'x': 200, 'y': -120},
                        {'id': 'sub3', 'label': 'Sub-concept 3', 'type': 'sub', 'x': 0, 'y': -200}
                    ],
                    'connections': [
                        {'from': 'center', 'to': 'concept1'},
                        {'from': 'center', 'to': 'concept2'},
                        {'from': 'center', 'to': 'concept3'},
                        {'from': 'center', 'to': 'concept4'},
                        {'from': 'concept1', 'to': 'sub1'},
                        {'from': 'concept2', 'to': 'sub2'},
                        {'from': 'concept3', 'to': 'sub3'}
                    ],
                    'raw_content': content
                }
            
        except Exception as e:
            print(f"Error generating mind map: {e}")
            return {
                'title': f'Mind Map: {topic.title}',
                'description': f'Visual representation of {topic.title}',
                'nodes': [
                    {'id': 'center', 'label': topic.title, 'type': 'central', 'x': 0, 'y': 0},
                    {'id': 'error', 'label': 'Error generating content', 'type': 'main', 'x': 0, 'y': 100}
                ],
                'connections': [{'from': 'center', 'to': 'error'}],
                'error': str(e)
            }
    
    def _generate_diagram(self, topic: Any, context: Dict) -> Dict:
        """Generate diagram content"""
        if not self.client:
            return {
                'title': f'Diagram: {topic.title}',
                'description': 'AI content generation unavailable. Please set up OpenAI API key.',
                'elements': [
                    {'id': 'main', 'type': 'box', 'label': topic.title, 'x': 100, 'y': 100, 'width': 200, 'height': 100}
                ],
                'layout': 'default'
            }
        
        try:
            prompt = f"""
            Create a diagram structure for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate a visual diagram with:
            1. Main elements (boxes, circles, etc.)
            2. Labels and text
            3. Connections between elements
            4. Positioning with x,y coordinates
            
            CRITICAL REQUIREMENTS:
            - Return ONLY valid JSON (no markdown, no extra text)
            - Each element MUST have x, y, width, and height values
            - Use "box" for main concepts/containers
            - Use "circle" for roles/people/entities
            - Arrange elements in a clear layout (grid or hierarchy)
            
            Format your response as a JSON object with this EXACT structure:
            {{
                "title": "Diagram Title",
                "description": "Brief description of the diagram",
                "elements": [
                    {{"id": "element1", "type": "box", "label": "Main Topic", "x": 200, "y": 50, "width": 150, "height": 80}},
                    {{"id": "element2", "type": "circle", "label": "Sub Item 1", "x": 50, "y": 200, "width": 100, "height": 100}},
                    {{"id": "element3", "type": "circle", "label": "Sub Item 2", "x": 250, "y": 200, "width": 100, "height": 100}}
                ],
                "connections": [
                    {{"from": "element1", "to": "element2", "label": "relates to"}},
                    {{"from": "element1", "to": "element3", "label": "includes"}}
                ],
                "layout": "hierarchy"
            }}
            
            Make it educational and suitable for GCSE level students.
            Include 5-10 elements with proper x,y positioning in a grid or hierarchical layout.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating educational diagrams. Create clear, visual representations that help students understand concepts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Try to parse JSON response
            import json
            try:
                content = response.choices[0].message.content.strip()
                
                # Clean up the content - remove any text before/after JSON
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                # Try to find JSON in the content
                start_idx = content.find('{')
                if start_idx != -1:
                    content = content[start_idx:]
                
                diagram_data = json.loads(content)
                
                # Post-process: Add coordinates if missing
                if 'elements' in diagram_data:
                    for i, element in enumerate(diagram_data['elements']):
                        if 'x' not in element or 'y' not in element:
                            # Arrange elements in a grid layout
                            col = i % 3  # 3 columns
                            row = i // 3
                            element['x'] = col * 200
                            element['y'] = row * 150
                        if 'width' not in element:
                            element['width'] = 150
                        if 'height' not in element:
                            element['height'] = element.get('type') == 'circle' and 100 or 80
                
                return diagram_data
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                content = response.choices[0].message.content.strip()
                return {
                    'title': f'Diagram: {topic.title}',
                    'description': f'Visual diagram for {topic.title}',
                    'elements': [
                        {'id': 'main', 'type': 'box', 'label': topic.title, 'x': 100, 'y': 100, 'width': 200, 'height': 100},
                        {'id': 'concept1', 'type': 'box', 'label': 'Key Concept 1', 'x': 50, 'y': 250, 'width': 150, 'height': 80},
                        {'id': 'concept2', 'type': 'box', 'label': 'Key Concept 2', 'x': 250, 'y': 250, 'width': 150, 'height': 80}
                    ],
                    'connections': [
                        {'from': 'main', 'to': 'concept1', 'label': 'includes'},
                        {'from': 'main', 'to': 'concept2', 'label': 'includes'}
                    ],
                    'layout': 'hierarchy',
                    'raw_content': content
                }
            
        except Exception as e:
            print(f"Error generating diagram: {e}")
            return {
                'title': f'Diagram: {topic.title}',
                'description': f'Visual representation of {topic.title}',
                'elements': [
                    {'id': 'main', 'type': 'box', 'label': topic.title, 'x': 100, 'y': 100, 'width': 200, 'height': 100},
                    {'id': 'error', 'type': 'box', 'label': 'Error generating content', 'x': 100, 'y': 250, 'width': 200, 'height': 80}
                ],
                'connections': [{'from': 'main', 'to': 'error', 'label': 'error'}],
                'layout': 'default',
                'error': str(e)
            }
    
    def _generate_timeline(self, topic: Any, context: Dict) -> Dict:
        """Generate timeline content"""
        if not self.client:
            return {
                'title': f'Timeline: {topic.title}',
                'description': 'AI content generation unavailable. Please set up OpenAI API key.',
                'events': [
                    {'date': '2024', 'event': 'Please set up API key', 'description': 'This is a placeholder event.'}
                ]
            }
        
        try:
            prompt = f"""
            Create a timeline for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate a chronological timeline with:
            1. Important dates or periods
            2. Key events or developments
            3. Brief descriptions for each event
            4. Logical chronological order
            
            IMPORTANT: Return ONLY valid JSON. Do not include any text before or after the JSON.
            The JSON must be properly formatted and parseable.
            
            Format your response as a JSON object with this structure:
            {{
                "title": "Timeline Title",
                "description": "Brief description of the timeline",
                "events": [
                    {{"date": "Year or date", "event": "Event title", "description": "Brief description of the event"}},
                    {{"date": "Year or date", "event": "Event title", "description": "Brief description of the event"}}
                ]
            }}
            
            Make it educational and suitable for GCSE level students.
            Include 5-8 key events if applicable to the topic.
            Ensure the JSON is valid and properly formatted.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating educational timelines. Create clear, chronological sequences that help students understand historical or process developments."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Try to parse JSON response
            import json
            try:
                content = response.choices[0].message.content.strip()
                
                # Clean up the content - remove any text before/after JSON
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                # Try to find JSON in the content
                start_idx = content.find('{')
                if start_idx != -1:
                    content = content[start_idx:]
                
                timeline_data = json.loads(content)
                return timeline_data
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                content = response.choices[0].message.content.strip()
                return {
                    'title': f'Timeline: {topic.title}',
                    'description': f'Chronological timeline for {topic.title}',
                    'events': [
                        {'date': 'Start', 'event': 'Introduction', 'description': 'Beginning of the topic'},
                        {'date': 'Development', 'event': 'Key Concepts', 'description': 'Main concepts and ideas'},
                        {'date': 'Conclusion', 'event': 'Summary', 'description': 'Key takeaways and conclusions'}
                    ],
                    'raw_content': content
                }
            
        except Exception as e:
            print(f"Error generating timeline: {e}")
            return {
                'title': f'Timeline: {topic.title}',
                'description': f'Chronological sequence for {topic.title}',
                'events': [
                    {'date': 'Error', 'event': 'Error generating content', 'description': 'There was an error generating the timeline content. Please try again.'}
                ],
                'error': str(e)
            }
    
    def _generate_flowchart(self, topic: Any, context: Dict) -> Dict:
        """Generate flowchart content"""
        if not self.client:
            return {
                'title': f'Flowchart: {topic.title}',
                'description': 'AI content generation unavailable. Please set up OpenAI API key.',
                'steps': [
                    {'id': 'start', 'type': 'start', 'label': 'Start', 'x': 100, 'y': 50},
                    {'id': 'process', 'type': 'process', 'label': 'Please set up API key', 'x': 100, 'y': 150}
                ],
                'connections': [{'from': 'start', 'to': 'process'}],
                'flow': 'linear'
            }
        
        try:
            prompt = f"""
            Create a flowchart for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate a process flowchart with:
            1. Start and end points
            2. Process steps or decisions
            3. Decision points (if applicable)
            4. Logical flow connections
            
            IMPORTANT: Return ONLY valid JSON. Do not include any text before or after the JSON.
            The JSON must be properly formatted and parseable.
            
            Format your response as a JSON object with this structure:
            {{
                "title": "Flowchart Title",
                "description": "Brief description of the flowchart",
                "steps": [
                    {{"id": "unique_id", "type": "start|process|decision|end", "label": "Step text", "x": 100, "y": 50}},
                    {{"id": "unique_id", "type": "start|process|decision|end", "label": "Step text", "x": 100, "y": 150}}
                ],
                "connections": [
                    {{"from": "step_id_1", "to": "step_id_2", "label": "Connection label"}}
                ],
                "flow": "linear|branching|circular"
            }}
            
            Make it educational and suitable for GCSE level students.
            Include 4-8 steps if applicable to the topic.
            Ensure the JSON is valid and properly formatted.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating educational flowcharts. Create clear, logical process flows that help students understand procedures or concepts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Try to parse JSON response
            import json
            try:
                content = response.choices[0].message.content.strip()
                
                # Clean up the content - remove any text before/after JSON
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                # Try to find JSON in the content
                start_idx = content.find('{')
                if start_idx != -1:
                    content = content[start_idx:]
                
                flowchart_data = json.loads(content)
                return flowchart_data
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                content = response.choices[0].message.content.strip()
                return {
                    'title': f'Flowchart: {topic.title}',
                    'description': f'Process flowchart for {topic.title}',
                    'steps': [
                        {'id': 'start', 'type': 'start', 'label': f'Begin {topic.title}', 'x': 200, 'y': 50},
                        {'id': 'step1', 'type': 'process', 'label': f'Understand {topic.title}', 'x': 200, 'y': 150},
                        {'id': 'step2', 'type': 'process', 'label': 'Apply Knowledge', 'x': 200, 'y': 250},
                        {'id': 'step3', 'type': 'process', 'label': 'Practice Examples', 'x': 200, 'y': 350},
                        {'id': 'end', 'type': 'end', 'label': 'Complete', 'x': 200, 'y': 450}
                    ],
                    'connections': [
                        {'from': 'start', 'to': 'step1', 'label': 'Start Learning'},
                        {'from': 'step1', 'to': 'step2', 'label': 'Apply Concepts'},
                        {'from': 'step2', 'to': 'step3', 'label': 'Practice'},
                        {'from': 'step3', 'to': 'end', 'label': 'Finish'}
                    ],
                    'flow': 'linear',
                    'raw_content': content
                }
            
        except Exception as e:
            print(f"Error generating flowchart: {e}")
            return {
                'title': f'Flowchart: {topic.title}',
                'description': f'Process flowchart for {topic.title}',
                'steps': [
                    {'id': 'start', 'type': 'start', 'label': 'Start', 'x': 100, 'y': 50},
                    {'id': 'error', 'type': 'process', 'label': 'Error generating content', 'x': 100, 'y': 150},
                    {'id': 'end', 'type': 'end', 'label': 'End', 'x': 100, 'y': 250}
                ],
                'connections': [
                    {'from': 'start', 'to': 'error'},
                    {'from': 'error', 'to': 'end'}
                ],
                'flow': 'linear',
                'error': str(e)
            }
    
    def _generate_visual_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate visual learning content"""
        if not self.client:
            return {
                'type': 'visual',
                'title': f'Visual Content: {topic.title}',
                'visual_elements': [
                    {'type': 'placeholder', 'content': 'Visual content requires OpenAI API configuration.'}
                ]
            }
        
        try:
            prompt = f"""
            Create visual-focused learning content for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate content optimized for visual learners that includes:
            1. Diagrams and charts descriptions
            2. Color-coded information
            3. Spatial relationships and layouts
            4. Visual metaphors and analogies
            5. Infographic-style summaries
            
            IMPORTANT: Return ONLY valid JSON.
            
            Format your response as:
            {{
                "title": "Visual Learning Guide",
                "visual_summary": "Brief visual description",
                "visual_elements": [
                    {{
                        "type": "diagram",
                        "title": "Main Concept Diagram",
                        "description": "Visual representation description",
                        "elements": ["Element 1", "Element 2"]
                    }},
                    {{
                        "type": "color_coding",
                        "title": "Color-Coded Categories",
                        "categories": [
                            {{"color": "blue", "label": "Category 1", "description": "..."}},
                            {{"color": "green", "label": "Category 2", "description": "..."}}
                        ]
                    }},
                    {{
                        "type": "visual_metaphor",
                        "title": "Think of it as...",
                        "metaphor": "Descriptive visual comparison"
                    }}
                ],
                "visual_summary_points": ["Visual point 1", "Visual point 2"]
            }}
            
            Focus on visual descriptions, spatial relationships, and imagery.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating visual learning content. Focus on diagrams, colors, spatial relationships, and visual metaphors."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            import json
            try:
                content = response.choices[0].message.content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                start_idx = content.find('{')
                if start_idx != -1:
                    content = content[start_idx:]
                
                visual_data = json.loads(content)
                visual_data['type'] = 'visual'
                return visual_data
                
            except json.JSONDecodeError:
                return {
                    'type': 'visual',
                    'title': f'Visual Content: {topic.title}',
                    'visual_summary': f'Visual learning content for {topic.title}',
                    'visual_elements': [
                        {'type': 'diagram', 'title': 'Main Concepts', 'description': response.choices[0].message.content.strip()}
                    ]
                }
        
        except Exception as e:
            print(f"Error generating visual content: {e}")
            return {
                'type': 'visual',
                'title': f'Visual Content: {topic.title}',
                'visual_elements': [
                    {'type': 'diagram', 'title': 'Overview', 'description': f'Visual overview of {topic.title}'}
                ],
                'error': str(e)
            }
    
    def _generate_auditory_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate auditory learning content"""
        if not self.client:
            return {
                'type': 'auditory',
                'title': f'Auditory Content: {topic.title}',
                'audio_elements': [
                    {'type': 'placeholder', 'content': 'Auditory content requires OpenAI API configuration.'}
                ]
            }
        
        try:
            prompt = f"""
            Create auditory-focused learning content for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate content optimized for auditory learners that includes:
            1. Verbal explanations and descriptions
            2. Mnemonics and rhymes
            3. Discussion points and dialogue
            4. Listening activities and instructions
            5. Sound-based analogies
            
            IMPORTANT: Return ONLY valid JSON.
            
            Format your response as:
            {{
                "title": "Auditory Learning Guide",
                "audio_introduction": "Spoken introduction",
                "audio_elements": [
                    {{
                        "type": "explanation",
                        "title": "Main Concept",
                        "script": "Verbal explanation as if speaking to someone"
                    }},
                    {{
                        "type": "mnemonic",
                        "title": "Memory Aid",
                        "phrase": "Memorable phrase or rhyme"
                    }},
                    {{
                        "type": "discussion",
                        "title": "Discussion Points",
                        "questions": ["Question 1?", "Question 2?"]
                    }}
                ],
                "listening_activities": ["Activity 1", "Activity 2"],
                "key_phrases": ["Important phrase 1", "Important phrase 2"]
            }}
            
            Focus on verbal explanations, rhythm, and spoken content.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating auditory learning content. Focus on verbal explanations, mnemonics, rhythm, and spoken language."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            import json
            try:
                content = response.choices[0].message.content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                start_idx = content.find('{')
                if start_idx != -1:
                    content = content[start_idx:]
                
                auditory_data = json.loads(content)
                auditory_data['type'] = 'auditory'
                return auditory_data
                
            except json.JSONDecodeError:
                return {
                    'type': 'auditory',
                    'title': f'Auditory Content: {topic.title}',
                    'audio_introduction': f'Listen and learn about {topic.title}',
                    'audio_elements': [
                        {'type': 'explanation', 'title': 'Overview', 'script': response.choices[0].message.content.strip()}
                    ]
                }
        
        except Exception as e:
            print(f"Error generating auditory content: {e}")
            return {
                'type': 'auditory',
                'title': f'Auditory Content: {topic.title}',
                'audio_elements': [
                    {'type': 'explanation', 'title': 'Overview', 'script': f'Verbal overview of {topic.title}'}
                ],
                'error': str(e)
            }
    
    def _generate_kinesthetic_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate kinesthetic learning content"""
        if not self.client:
            return {
                'type': 'kinesthetic',
                'title': f'Kinesthetic Content: {topic.title}',
                'interactive_elements': [
                    {'type': 'placeholder', 'content': 'Kinesthetic content requires OpenAI API configuration.'}
                ]
            }
        
        try:
            prompt = f"""
            Create kinesthetic-focused learning content for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate content optimized for kinesthetic/hands-on learners that includes:
            1. Physical activities and experiments
            2. Interactive exercises
            3. Building or creating tasks
            4. Movement-based learning
            5. Tactile and practical applications
            
            IMPORTANT: Return ONLY valid JSON.
            
            Format your response as:
            {{
                "title": "Hands-On Learning Guide",
                "introduction": "Engaging hands-on introduction",
                "interactive_elements": [
                    {{
                        "type": "activity",
                        "title": "Practical Activity",
                        "instructions": ["Step 1", "Step 2", "Step 3"],
                        "materials": ["Material 1", "Material 2"]
                    }},
                    {{
                        "type": "experiment",
                        "title": "Hands-On Experiment",
                        "purpose": "What you'll learn",
                        "procedure": ["Step 1", "Step 2"]
                    }},
                    {{
                        "type": "practice",
                        "title": "Practice Exercise",
                        "task": "Detailed practice task description"
                    }}
                ],
                "physical_activities": ["Activity 1", "Activity 2"],
                "real_world_applications": ["Application 1", "Application 2"]
            }}
            
            Focus on doing, building, moving, and hands-on practice.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating kinesthetic learning content. Focus on hands-on activities, experiments, physical tasks, and practical applications."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            import json
            try:
                content = response.choices[0].message.content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                start_idx = content.find('{')
                if start_idx != -1:
                    content = content[start_idx:]
                
                kinesthetic_data = json.loads(content)
                kinesthetic_data['type'] = 'kinesthetic'
                return kinesthetic_data
                
            except json.JSONDecodeError:
                return {
                    'type': 'kinesthetic',
                    'title': f'Kinesthetic Content: {topic.title}',
                    'introduction': f'Learn {topic.title} through hands-on practice',
                    'interactive_elements': [
                        {'type': 'activity', 'title': 'Practice Activity', 'instructions': [response.choices[0].message.content.strip()]}
                    ]
                }
        
        except Exception as e:
            print(f"Error generating kinesthetic content: {e}")
            return {
                'type': 'kinesthetic',
                'title': f'Kinesthetic Content: {topic.title}',
                'interactive_elements': [
                    {'type': 'activity', 'title': 'Hands-On Practice', 'instructions': [f'Practice exercises for {topic.title}']}
                ],
                'error': str(e)
            }
    
    def _generate_reading_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate reading-based content"""
        if not self.client:
            return {
                'type': 'reading',
                'title': f'Reading Content: {topic.title}',
                'content': 'AI content generation unavailable. Please set up OpenAI API key.',
                'text_elements': [
                    {'type': 'paragraph', 'content': 'Reading content requires OpenAI API configuration.'}
                ]
            }
        
        try:
            prompt = f"""
            Create comprehensive reading/writing learning content for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate detailed written content that includes:
            1. Clear, well-structured paragraphs explaining the topic
            2. Key definitions and terminology
            3. Examples with explanations
            4. Practice writing prompts or discussion questions
            5. Summary points for note-taking
            
            IMPORTANT: Return ONLY valid JSON. Do not include any text before or after the JSON.
            
            Format your response as a JSON object with this structure:
            {{
                "title": "Content Title",
                "introduction": "Engaging introduction paragraph",
                "sections": [
                    {{
                        "heading": "Section Title",
                        "content": "Detailed explanation with multiple paragraphs. Use \\n\\n to separate paragraphs.",
                        "key_points": ["Key point 1", "Key point 2", "Key point 3"]
                    }}
                ],
                "definitions": [
                    {{"term": "Important Term", "definition": "Clear definition"}},
                    {{"term": "Another Term", "definition": "Clear definition"}}
                ],
                "examples": [
                    {{
                        "title": "Example 1",
                        "description": "Detailed example with explanation"
                    }}
                ],
                "writing_prompts": [
                    "Write a paragraph explaining...",
                    "Compare and contrast...",
                    "Summarize in your own words..."
                ],
                "summary": "Concise summary of the main points"
            }}
            
            Make it educational, comprehensive, and suitable for GCSE level students.
            Focus on clear, readable text that promotes understanding through reading and writing.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educator creating clear, comprehensive written content. Focus on thorough explanations, proper structure, and engaging reading material that promotes deep understanding."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            # Parse JSON response
            import json
            try:
                content = response.choices[0].message.content.strip()
                
                # Clean up the content - remove markdown fences
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                # Find JSON in content
                start_idx = content.find('{')
                if start_idx != -1:
                    content = content[start_idx:]
                
                reading_data = json.loads(content)
                reading_data['type'] = 'reading'
                
                # Build text_elements for backward compatibility
                text_elements = []
                if 'introduction' in reading_data:
                    text_elements.append({
                        'type': 'introduction',
                        'content': reading_data['introduction']
                    })
                if 'sections' in reading_data:
                    for section in reading_data['sections']:
                        text_elements.append({
                            'type': 'section',
                            'heading': section.get('heading', ''),
                            'content': section.get('content', '')
                        })
                
                reading_data['text_elements'] = text_elements
                return reading_data
                
            except json.JSONDecodeError:
                # Fallback: create structured content from text
                raw_content = response.choices[0].message.content.strip()
                return {
                    'type': 'reading',
                    'title': f'Reading Content: {topic.title}',
                    'introduction': f'This content covers the topic of {topic.title}.',
                    'sections': [
                        {
                            'heading': topic.title,
                            'content': raw_content,
                            'key_points': ['Review the content carefully', 'Take notes on key concepts', 'Practice explaining in your own words']
                        }
                    ],
                    'text_elements': [
                        {'type': 'paragraph', 'content': raw_content}
                    ],
                    'summary': f'Study material for {topic.title}'
                }
        
        except Exception as e:
            print(f"Error generating reading content: {e}")
            return {
                'type': 'reading',
                'title': f'Reading Content: {topic.title}',
                'introduction': f'Learn about {topic.title}',
                'sections': [
                    {
                        'heading': 'Overview',
                        'content': f'This section covers important aspects of {topic.title}. Study the material carefully and take notes on key concepts.',
                        'key_points': ['Understand the main concepts', 'Practice explaining in writing', 'Review regularly']
                    }
                ],
                'text_elements': [
                    {'type': 'paragraph', 'content': f'Study material for {topic.title}'}
                ],
                'error': str(e)
            }
    
    def _generate_multi_modal_content(self, topic: Any, context: Dict, profile: Dict) -> Dict:
        """Generate multi-modal content combining multiple learning styles"""
        if not self.client:
            return {
                'type': 'multi_modal',
                'title': f'Multi-Modal Content: {topic.title}',
                'mixed_elements': [
                    {'type': 'placeholder', 'content': 'Multi-modal content requires OpenAI API configuration.'}
                ]
            }
        
        try:
            prompt = f"""
            Create comprehensive multi-modal learning content for the topic: "{topic.title}"
            
            Description: {topic.description}
            
            Generate content that combines multiple learning styles:
            1. Visual elements (diagrams, charts)
            2. Auditory elements (explanations, mnemonics)
            3. Reading/writing (detailed text)
            4. Kinesthetic elements (activities, experiments)
            
            IMPORTANT: Return ONLY valid JSON.
            
            Format your response as:
            {{
                "title": "Comprehensive Learning Guide",
                "overview": "Brief overview",
                "mixed_elements": [
                    {{
                        "style": "visual",
                        "type": "diagram",
                        "title": "Visual Overview",
                        "content": "Diagram description"
                    }},
                    {{
                        "style": "auditory",
                        "type": "explanation",
                        "title": "Verbal Explanation",
                        "content": "Spoken-style explanation"
                    }},
                    {{
                        "style": "reading",
                        "type": "text",
                        "title": "Detailed Reading",
                        "content": "Comprehensive text explanation"
                    }},
                    {{
                        "style": "kinesthetic",
                        "type": "activity",
                        "title": "Hands-On Practice",
                        "instructions": ["Step 1", "Step 2"]
                    }}
                ],
                "summary": "Multi-modal summary"
            }}
            
            Combine all learning styles for maximum engagement.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating multi-modal learning content. Combine visual, auditory, reading/writing, and kinesthetic elements for comprehensive learning."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            import json
            try:
                content = response.choices[0].message.content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                start_idx = content.find('{')
                if start_idx != -1:
                    content = content[start_idx:]
                
                multimodal_data = json.loads(content)
                multimodal_data['type'] = 'multi_modal'
                return multimodal_data
                
            except json.JSONDecodeError:
                return {
                    'type': 'multi_modal',
                    'title': f'Multi-Modal Content: {topic.title}',
                    'overview': f'Comprehensive learning content for {topic.title}',
                    'mixed_elements': [
                        {'style': 'reading', 'type': 'text', 'title': 'Content', 'content': response.choices[0].message.content.strip()}
                    ]
                }
        
        except Exception as e:
            print(f"Error generating multi-modal content: {e}")
            return {
                'type': 'multi_modal',
                'title': f'Multi-Modal Content: {topic.title}',
                'mixed_elements': [
                    {'style': 'reading', 'type': 'text', 'title': 'Overview', 'content': f'Comprehensive content for {topic.title}'}
                ],
                'error': str(e)
            }
    
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



from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import json

class GCSEPastPaper:
    
    
    def __init__(self, id=None, subject_id=None, paper_title=None, exam_year=None,
                 exam_month=None, paper_number=None, exam_board=None, 
                 specification_code=None, difficulty_level='Both', total_marks=None,
                 duration_minutes=None, file_url=None, mark_scheme_url=None,
                 is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.subject_id = subject_id
        self.paper_title = paper_title
        self.exam_year = exam_year
        self.exam_month = exam_month
        self.paper_number = paper_number
        self.exam_board = exam_board
        self.specification_code = specification_code
        self.difficulty_level = difficulty_level
        self.total_marks = total_marks
        self.duration_minutes = duration_minutes
        self.file_url = file_url
        self.mark_scheme_url = mark_scheme_url
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
        self.questions = []  

    @classmethod
    def create_past_paper(cls, subject_id: str, paper_title: str, exam_year: int,
                         exam_month: str, paper_number: int = None, exam_board: str = None,
                         specification_code: str = None, difficulty_level: str = 'Both',
                         total_marks: int = None, duration_minutes: int = None,
                         file_url: str = None, mark_scheme_url: str = None) -> 'GCSEPastPaper':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        paper_data = {
            'subject_id': subject_id,
            'paper_title': paper_title,
            'exam_year': exam_year,
            'exam_month': exam_month,
            'paper_number': paper_number,
            'exam_board': exam_board,
            'specification_code': specification_code,
            'difficulty_level': difficulty_level,
            'total_marks': total_marks,
            'duration_minutes': duration_minutes,
            'file_url': file_url,
            'mark_scheme_url': mark_scheme_url,
            'is_active': True
        }
        
        try:
            result = supabase.table('gcse_past_papers').insert(paper_data).execute()
            if result.data:
                paper_data = result.data[0]
                return cls(**paper_data)
        except Exception as e:
            print(f"Error creating past paper: {e}")
            
        return None

    @classmethod
    def get_past_papers_by_subject(cls, subject_id: str, exam_board: str = None,
                                  exam_year: int = None, difficulty_level: str = None) -> List['GCSEPastPaper']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_past_papers(subject_id)
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('gcse_past_papers').select('*').eq('subject_id', subject_id).eq('is_active', True)
            
            if exam_board:
                query = query.eq('exam_board', exam_board)
            if exam_year:
                query = query.eq('exam_year', exam_year)
            if difficulty_level:
                query = query.eq('difficulty_level', difficulty_level)
            
            result = query.order('exam_year', desc=True).order('exam_month').execute()
            papers = [cls(**paper) for paper in result.data]
            
            
            for paper in papers:
                paper.questions = GCSEPastPaperQuestion.get_questions_by_paper(paper.id)
                
            return papers
        except Exception as e:
            print(f"Error getting past papers: {e}")
            return cls._get_default_past_papers(subject_id)

    @classmethod
    def get_past_paper_by_id(cls, paper_id: str) -> Optional['GCSEPastPaper']:
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_past_papers').select('*').eq('id', paper_id).eq('is_active', True).execute()
            if result.data:
                paper_data = result.data[0]
                paper = cls(**paper_data)
                paper.questions = GCSEPastPaperQuestion.get_questions_by_paper(paper.id)
                return paper
        except Exception as e:
            print(f"Error getting past paper by ID: {e}")
            
        return None

    @classmethod
    def _get_default_past_papers(cls, subject_id: str) -> List['GCSEPastPaper']:
        
        
        if subject_id == "1":
            return [
                cls(
                    id="1",
                    subject_id="1",
                    paper_title="Mathematics Foundation Paper 1",
                    exam_year=2023,
                    exam_month="June",
                    paper_number=1,
                    exam_board="AQA",
                    specification_code="8300",
                    difficulty_level="Foundation",
                    total_marks=80,
                    duration_minutes=90
                ),
                cls(
                    id="2",
                    subject_id="1",
                    paper_title="Mathematics Foundation Paper 2",
                    exam_year=2023,
                    exam_month="June",
                    paper_number=2,
                    exam_board="AQA",
                    specification_code="8300",
                    difficulty_level="Foundation",
                    total_marks=80,
                    duration_minutes=90
                ),
                cls(
                    id="3",
                    subject_id="1",
                    paper_title="Mathematics Foundation Paper 3",
                    exam_year=2023,
                    exam_month="June",
                    paper_number=3,
                    exam_board="AQA",
                    specification_code="8300",
                    difficulty_level="Foundation",
                    total_marks=80,
                    duration_minutes=90
                )
            ]
        return []


class GCSEPastPaperQuestion:
    
    
    def __init__(self, id=None, past_paper_id=None, question_number=None, question_text=None,
                 question_type=None, marks=None, difficulty_level='Both', topic_tags=None,
                 correct_answer=None, mark_scheme=None, is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.past_paper_id = past_paper_id
        self.question_number = question_number
        self.question_text = question_text
        self.question_type = question_type
        self.marks = marks
        self.difficulty_level = difficulty_level
        self.topic_tags = topic_tags or []  
        self.correct_answer = correct_answer
        self.mark_scheme = mark_scheme
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_question(cls, past_paper_id: str, question_number: str, question_text: str,
                       question_type: str, marks: int, difficulty_level: str = 'Both',
                       topic_tags: List[str] = None, correct_answer: str = None,
                       mark_scheme: str = None) -> 'GCSEPastPaperQuestion':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        question_data = {
            'past_paper_id': past_paper_id,
            'question_number': question_number,
            'question_text': question_text,
            'question_type': question_type,
            'marks': marks,
            'difficulty_level': difficulty_level,
            'topic_tags': json.dumps(topic_tags) if topic_tags else None,
            'correct_answer': correct_answer,
            'mark_scheme': mark_scheme,
            'is_active': True
        }
        
        try:
            result = supabase.table('gcse_past_paper_questions').insert(question_data).execute()
            if result.data:
                question_data = result.data[0]
                if question_data.get('topic_tags'):
                    question_data['topic_tags'] = json.loads(question_data['topic_tags'])
                return cls(**question_data)
        except Exception as e:
            print(f"Error creating past paper question: {e}")
            
        return None

    @classmethod
    def get_questions_by_paper(cls, past_paper_id: str) -> List['GCSEPastPaperQuestion']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_questions(past_paper_id)
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_past_paper_questions').select('*').eq('past_paper_id', past_paper_id).eq('is_active', True).order('question_number').execute()
            questions = []
            for question_data in result.data:
                if question_data.get('topic_tags'):
                    question_data['topic_tags'] = json.loads(question_data['topic_tags'])
                questions.append(cls(**question_data))
            return questions
        except Exception as e:
            print(f"Error getting past paper questions: {e}")
            return cls._get_default_questions(past_paper_id)

    @classmethod
    def _get_default_questions(cls, past_paper_id: str) -> List['GCSEPastPaperQuestion']:
        
        
        if past_paper_id in ["1", "2", "3"]:
            return [
                cls(
                    id="1",
                    past_paper_id=past_paper_id,
                    question_number="1",
                    question_text="Calculate 12 + 8 × 3",
                    question_type="short_answer",
                    marks=2,
                    difficulty_level="Foundation",
                    topic_tags=["1"],  
                    correct_answer="36",
                    mark_scheme="M1 for 8 × 3 = 24, A1 for 12 + 24 = 36"
                ),
                cls(
                    id="2",
                    past_paper_id=past_paper_id,
                    question_number="2",
                    question_text="Solve 2x + 5 = 13",
                    question_type="short_answer",
                    marks=2,
                    difficulty_level="Foundation",
                    topic_tags=["2"],  
                    correct_answer="x = 4",
                    mark_scheme="M1 for 2x = 8, A1 for x = 4"
                ),
                cls(
                    id="3",
                    past_paper_id=past_paper_id,
                    question_number="3",
                    question_text="A rectangle has length 8 cm and width 5 cm. Calculate its area.",
                    question_type="short_answer",
                    marks=2,
                    difficulty_level="Foundation",
                    topic_tags=["4"],  
                    correct_answer="40 cm²",
                    mark_scheme="M1 for 8 × 5, A1 for 40 cm²"
                )
            ]
        return []


class GCSEExamPractice:
    
    
    def __init__(self, id=None, user_id=None, past_paper_id=None, started_at=None,
                 completed_at=None, time_taken_minutes=None, total_marks=None,
                 achieved_marks=None, grade=None, difficulty_level=None,
                 status='in_progress', created_at=None):
        self.id = id
        self.user_id = user_id
        self.past_paper_id = past_paper_id
        self.started_at = started_at
        self.completed_at = completed_at
        self.time_taken_minutes = time_taken_minutes
        self.total_marks = total_marks
        self.achieved_marks = achieved_marks
        self.grade = grade
        self.difficulty_level = difficulty_level
        self.status = status
        self.created_at = created_at
        self.answers = []  

    @classmethod
    def start_practice_session(cls, user_id: str, past_paper_id: str, difficulty_level: str = 'Both') -> 'GCSEExamPractice':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        practice_data = {
            'user_id': user_id,
            'past_paper_id': past_paper_id,
            'started_at': datetime.now().isoformat(),
            'difficulty_level': difficulty_level,
            'status': 'in_progress'
        }
        
        try:
            result = supabase.table('gcse_exam_practice').insert(practice_data).execute()
            if result.data:
                practice_data = result.data[0]
                return cls(**practice_data)
        except Exception as e:
            print(f"Error starting exam practice session: {e}")
            
        return None

    @classmethod
    def get_practice_session_by_id(cls, session_id: str, user_id: str) -> Optional['GCSEExamPractice']:
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_exam_practice').select('*').eq('id', session_id).eq('user_id', user_id).execute()
            if result.data:
                practice_data = result.data[0]
                practice = cls(**practice_data)
                practice.answers = GCSEExamPracticeAnswer.get_answers_by_session(session_id)
                return practice
        except Exception as e:
            print(f"Error getting practice session: {e}")
            
        return None

    @classmethod
    def get_user_practice_sessions(cls, user_id: str, limit: int = 10) -> List['GCSEExamPractice']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_exam_practice').select('*').eq('user_id', user_id).order('started_at', desc=True).limit(limit).execute()
            sessions = []
            for session_data in result.data:
                session = cls(**session_data)
                session.answers = GCSEExamPracticeAnswer.get_answers_by_session(session.id)
                sessions.append(session)
            return sessions
        except Exception as e:
            print(f"Error getting user practice sessions: {e}")
            return []

    def submit_answer(self, question_id: str, user_answer: str, time_spent_seconds: int = 0) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            question = GCSEPastPaperQuestion.get_question_by_id(question_id)
            if not question:
                return False
            
            
            is_correct = False
            if question.correct_answer:
                is_correct = str(user_answer).strip().lower() == str(question.correct_answer).strip().lower()
            
            answer_data = {
                'practice_session_id': self.id,
                'question_id': question_id,
                'user_answer': user_answer,
                'is_correct': is_correct,
                'time_spent_seconds': time_spent_seconds,
                'submitted_at': datetime.now().isoformat()
            }
            
            result = supabase.table('gcse_exam_practice_answers').insert(answer_data).execute()
            if result.data:
                
                answer = GCSEExamPracticeAnswer(**result.data[0])
                self.answers.append(answer)
                return True
        except Exception as e:
            print(f"Error submitting answer: {e}")
            
        return False

    def complete_practice_session(self) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            total_marks = sum(answer.marks_achieved for answer in self.answers)
            achieved_marks = sum(answer.marks_achieved for answer in self.answers if answer.is_correct)
            
            
            percentage = (achieved_marks / total_marks * 100) if total_marks > 0 else 0
            
            
            if percentage >= 90:
                grade = "9"
            elif percentage >= 80:
                grade = "8"
            elif percentage >= 70:
                grade = "7"
            elif percentage >= 60:
                grade = "6"
            elif percentage >= 50:
                grade = "5"
            elif percentage >= 40:
                grade = "4"
            else:
                grade = "U"
            
            
            if self.started_at:
                started = datetime.fromisoformat(self.started_at.replace('Z', '+00:00'))
                time_taken = datetime.now() - started
                time_taken_minutes = int(time_taken.total_seconds() / 60)
            else:
                time_taken_minutes = 0
            
            update_data = {
                'completed_at': datetime.now().isoformat(),
                'time_taken_minutes': time_taken_minutes,
                'total_marks': total_marks,
                'achieved_marks': achieved_marks,
                'grade': grade,
                'status': 'completed'
            }
            
            result = supabase.table('gcse_exam_practice').update(update_data).eq('id', self.id).execute()
            if result.data:
                
                self.completed_at = update_data['completed_at']
                self.time_taken_minutes = time_taken_minutes
                self.total_marks = total_marks
                self.achieved_marks = achieved_marks
                self.grade = grade
                self.status = 'completed'
                return True
        except Exception as e:
            print(f"Error completing practice session: {e}")
            
        return False


class GCSEExamPracticeAnswer:
    
    
    def __init__(self, id=None, practice_session_id=None, question_id=None,
                 user_answer=None, is_correct=False, marks_achieved=None,
                 time_spent_seconds=0, submitted_at=None):
        self.id = id
        self.practice_session_id = practice_session_id
        self.question_id = question_id
        self.user_answer = user_answer
        self.is_correct = is_correct
        self.marks_achieved = marks_achieved
        self.time_spent_seconds = time_spent_seconds
        self.submitted_at = submitted_at

    @classmethod
    def get_answers_by_session(cls, session_id: str) -> List['GCSEExamPracticeAnswer']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_exam_practice_answers').select('*').eq('practice_session_id', session_id).order('submitted_at').execute()
            return [cls(**answer) for answer in result.data]
        except Exception as e:
            print(f"Error getting practice answers: {e}")
            return []

    @staticmethod
    def get_question_by_id(question_id: str) -> Optional['GCSEPastPaperQuestion']:
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_past_paper_questions').select('*').eq('id', question_id).eq('is_active', True).execute()
            if result.data:
                question_data = result.data[0]
                if question_data.get('topic_tags'):
                    question_data['topic_tags'] = json.loads(question_data['topic_tags'])
                return GCSEPastPaperQuestion(**question_data)
        except Exception as e:
            print(f"Error getting question by ID: {e}")
            
        return None


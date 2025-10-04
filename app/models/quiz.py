

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import json
import uuid


class Quiz:
    
    
    def __init__(self, id=None, topic_id=None, user_id=None, title=None, 
                 description=None, quiz_type=None, difficulty_level='medium',
                 time_limit_minutes=None, passing_score=70, is_active=True,
                 created_at=None, updated_at=None):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.quiz_type = quiz_type  
        self.difficulty_level = difficulty_level
        self.time_limit_minutes = time_limit_minutes
        self.passing_score = passing_score
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_quiz(cls, topic_id: str, user_id: str, title: str, 
                   description: str = None, quiz_type: str = 'multiple_choice',
                   difficulty_level: str = 'medium', time_limit_minutes: int = None,
                   passing_score: int = 70) -> 'Quiz':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        quiz_data = {
            'topic_id': topic_id,
            'user_id': user_id,
            'title': title,
            'description': description,
            'quiz_type': quiz_type,
            'difficulty_level': difficulty_level,
            'time_limit_minutes': time_limit_minutes,
            'passing_score': passing_score,
            'is_active': True
        }
        
        try:
            result = supabase.table('quizzes').insert(quiz_data).execute()
            if result.data:
                quiz_data = result.data[0]
                return cls(**quiz_data)
        except Exception as e:
            print(f"Error creating quiz: {e}")
            
        return None

    @classmethod
    def get_quizzes_by_topic(cls, topic_id: str, user_id: str) -> List['Quiz']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('quizzes').select('*').eq('topic_id', topic_id).eq('user_id', user_id).eq('is_active', True).order('created_at', desc=True).execute()
            return [cls(**quiz) for quiz in result.data]
        except Exception as e:
            print(f"Error getting quizzes by topic: {e}")
            return []

    @classmethod
    def get_quiz_by_id(cls, quiz_id: str, user_id: str) -> Optional['Quiz']:
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('quizzes').select('*').eq('id', quiz_id).eq('user_id', user_id).eq('is_active', True).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error getting quiz by ID: {e}")
            
        return None

    def update_quiz(self, **kwargs) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('quizzes').update(kwargs).eq('id', self.id).execute()
            if result.data:
                
                for key, value in kwargs.items():
                    setattr(self, key, value)
                return True
        except Exception as e:
            print(f"Error updating quiz: {e}")
            
        return False

    def delete_quiz(self) -> bool:
        
        return self.update_quiz(is_active=False)


class QuizQuestion:
    
    
    def __init__(self, id=None, quiz_id=None, question_text=None, question_type=None,
                 correct_answer=None, explanation=None, points=1, order_index=0,
                 is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.quiz_id = quiz_id
        self.question_text = question_text
        self.question_type = question_type
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.points = points
        self.order_index = order_index
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
        self.options = []  

    @classmethod
    def create_question(cls, quiz_id: str, question_text: str, question_type: str,
                       correct_answer: str, explanation: str = None, points: int = 1,
                       order_index: int = 0) -> 'QuizQuestion':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        question_data = {
            'quiz_id': quiz_id,
            'question_text': question_text,
            'question_type': question_type,
            'correct_answer': correct_answer,
            'explanation': explanation,
            'points': points,
            'order_index': order_index,
            'is_active': True
        }
        
        try:
            result = supabase.table('quiz_questions').insert(question_data).execute()
            if result.data:
                question_data = result.data[0]
                return cls(**question_data)
        except Exception as e:
            print(f"Error creating quiz question: {e}")
            
        return None

    @classmethod
    def get_questions_by_quiz(cls, quiz_id: str) -> List['QuizQuestion']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('quiz_questions').select('*').eq('quiz_id', quiz_id).eq('is_active', True).order('order_index').execute()
            questions = [cls(**question) for question in result.data]
            
            
            for question in questions:
                question.options = QuizQuestionOption.get_options_by_question(question.id)
                
            return questions
        except Exception as e:
            print(f"Error getting questions by quiz: {e}")
            return []

    def add_option(self, option_text: str, is_correct: bool = False, order_index: int = 0) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        option_data = {
            'question_id': self.id,
            'option_text': option_text,
            'is_correct': is_correct,
            'order_index': order_index
        }
        
        try:
            result = supabase.table('quiz_question_options').insert(option_data).execute()
            if result.data:
                
                option = QuizQuestionOption(**result.data[0])
                self.options.append(option)
                return True
        except Exception as e:
            print(f"Error adding question option: {e}")
            
        return False


class QuizQuestionOption:
    
    
    def __init__(self, id=None, question_id=None, option_text=None, 
                 is_correct=False, order_index=0, created_at=None):
        self.id = id
        self.question_id = question_id
        self.option_text = option_text
        self.is_correct = is_correct
        self.order_index = order_index
        self.created_at = created_at

    @classmethod
    def get_options_by_question(cls, question_id: str) -> List['QuizQuestionOption']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('quiz_question_options').select('*').eq('question_id', question_id).order('order_index').execute()
            return [cls(**option) for option in result.data]
        except Exception as e:
            print(f"Error getting options by question: {e}")
            return []


class QuizAttempt:
    
    
    def __init__(self, id=None, quiz_id=None, user_id=None, started_at=None,
                 completed_at=None, score=0, total_questions=0, correct_answers=0,
                 time_taken_minutes=0, status='in_progress', created_at=None):
        self.id = id
        self.quiz_id = quiz_id
        self.user_id = user_id
        self.started_at = started_at
        self.completed_at = completed_at
        self.score = score
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.time_taken_minutes = time_taken_minutes
        self.status = status
        self.created_at = created_at
        self.answers = []  

    @classmethod
    def start_attempt(cls, quiz_id: str, user_id: str) -> 'QuizAttempt':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        attempt_data = {
            'quiz_id': quiz_id,
            'user_id': user_id,
            'started_at': datetime.now().isoformat(),
            'status': 'in_progress'
        }
        
        try:
            result = supabase.table('quiz_attempts').insert(attempt_data).execute()
            if result.data:
                attempt_data = result.data[0]
                return cls(**attempt_data)
        except Exception as e:
            print(f"Error starting quiz attempt: {e}")
            
        return None

    @classmethod
    def get_attempt_by_id(cls, attempt_id: str, user_id: str) -> Optional['QuizAttempt']:
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('quiz_attempts').select('*').eq('id', attempt_id).eq('user_id', user_id).execute()
            if result.data:
                attempt_data = result.data[0]
                attempt = cls(**attempt_data)
                
                attempt.answers = QuizAttemptAnswer.get_answers_by_attempt(attempt_id)
                return attempt
        except Exception as e:
            print(f"Error getting attempt by ID: {e}")
            
        return None

    def submit_answer(self, question_id: str, user_answer: str, time_spent_seconds: int = 0) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        
        try:
            question_result = supabase.table('quiz_questions').select('correct_answer').eq('id', question_id).execute()
            if not question_result.data:
                return False
                
            correct_answer = question_result.data[0]['correct_answer']
            is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
            
            answer_data = {
                'attempt_id': self.id,
                'question_id': question_id,
                'user_answer': user_answer,
                'is_correct': is_correct,
                'time_spent_seconds': time_spent_seconds,
                'answered_at': datetime.now().isoformat()
            }
            
            result = supabase.table('quiz_attempt_answers').insert(answer_data).execute()
            if result.data:
                
                answer = QuizAttemptAnswer(**result.data[0])
                self.answers.append(answer)
                return True
        except Exception as e:
            print(f"Error submitting answer: {e}")
            
        return False

    def complete_attempt(self) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            total_questions = len(self.answers)
            correct_answers = sum(1 for answer in self.answers if answer.is_correct)
            score = int((correct_answers / total_questions * 100)) if total_questions > 0 else 0
            
            
            if self.started_at:
                started = datetime.fromisoformat(self.started_at.replace('Z', '+00:00'))
                time_taken = datetime.now() - started
                time_taken_minutes = int(time_taken.total_seconds() / 60)
            else:
                time_taken_minutes = 0
            
            update_data = {
                'completed_at': datetime.now().isoformat(),
                'score': score,
                'total_questions': total_questions,
                'correct_answers': correct_answers,
                'time_taken_minutes': time_taken_minutes,
                'status': 'completed'
            }
            
            result = supabase.table('quiz_attempts').update(update_data).eq('id', self.id).execute()
            if result.data:
                
                self.completed_at = update_data['completed_at']
                self.score = score
                self.total_questions = total_questions
                self.correct_answers = correct_answers
                self.time_taken_minutes = time_taken_minutes
                self.status = 'completed'
                return True
        except Exception as e:
            print(f"Error completing attempt: {e}")
            
        return False


class QuizAttemptAnswer:
    
    
    def __init__(self, id=None, attempt_id=None, question_id=None, user_answer=None,
                 is_correct=False, time_spent_seconds=0, answered_at=None):
        self.id = id
        self.attempt_id = attempt_id
        self.question_id = question_id
        self.user_answer = user_answer
        self.is_correct = is_correct
        self.time_spent_seconds = time_spent_seconds
        self.answered_at = answered_at

    @classmethod
    def get_answers_by_attempt(cls, attempt_id: str) -> List['QuizAttemptAnswer']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('quiz_attempt_answers').select('*').eq('attempt_id', attempt_id).order('answered_at').execute()
            return [cls(**answer) for answer in result.data]
        except Exception as e:
            print(f"Error getting answers by attempt: {e}")
            return []


class FlashcardProgress:
    
    
    def __init__(self, id=None, user_id=None, question_id=None, ease_factor=2.5,
                 interval_days=1, repetitions=0, next_review_date=None,
                 last_reviewed_at=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.question_id = question_id
        self.ease_factor = ease_factor
        self.interval_days = interval_days
        self.repetitions = repetitions
        self.next_review_date = next_review_date
        self.last_reviewed_at = last_reviewed_at
        self.created_at = created_at

    @classmethod
    def get_due_flashcards(cls, user_id: str, limit: int = 20) -> List['FlashcardProgress']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            today = date.today().isoformat()
            result = supabase.table('flashcard_progress').select('*').eq('user_id', user_id).lte('next_review_date', today).order('next_review_date').limit(limit).execute()
            return [cls(**progress) for progress in result.data]
        except Exception as e:
            print(f"Error getting due flashcards: {e}")
            return []

    def update_progress(self, quality: int) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            if quality >= 3:  
                if self.repetitions == 0:
                    self.interval_days = 1
                elif self.repetitions == 1:
                    self.interval_days = 6
                else:
                    self.interval_days = int(self.interval_days * self.ease_factor)
                
                self.repetitions += 1
            else:  
                self.repetitions = 0
                self.interval_days = 1
            
            
            self.ease_factor = max(1.3, self.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            
            
            self.next_review_date = (date.today() + timedelta(days=self.interval_days)).isoformat()
            self.last_reviewed_at = datetime.now().isoformat()
            
            update_data = {
                'ease_factor': self.ease_factor,
                'interval_days': self.interval_days,
                'repetitions': self.repetitions,
                'next_review_date': self.next_review_date,
                'last_reviewed_at': self.last_reviewed_at
            }
            
            result = supabase.table('flashcard_progress').update(update_data).eq('id', self.id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error updating flashcard progress: {e}")
            return False

    @classmethod
    def create_or_update_progress(cls, user_id: str, question_id: str, quality: int) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            result = supabase.table('flashcard_progress').select('*').eq('user_id', user_id).eq('question_id', question_id).execute()
            
            if result.data:
                
                progress = cls(**result.data[0])
                return progress.update_progress(quality)
            else:
                
                progress = cls(
                    user_id=user_id,
                    question_id=question_id,
                    ease_factor=2.5,
                    interval_days=1,
                    repetitions=0,
                    next_review_date=date.today().isoformat()
                )
                
                insert_data = {
                    'user_id': user_id,
                    'question_id': question_id,
                    'ease_factor': progress.ease_factor,
                    'interval_days': progress.interval_days,
                    'repetitions': progress.repetitions,
                    'next_review_date': progress.next_review_date
                }
                
                result = supabase.table('flashcard_progress').insert(insert_data).execute()
                if result.data:
                    progress_data = result.data[0]
                    progress.id = progress_data['id']
                    return progress.update_progress(quality)
        except Exception as e:
            print(f"Error creating/updating flashcard progress: {e}")
            
        return False




from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import json

class GCSEExamSchedule:
    
    
    def __init__(self, id=None, user_id=None, subject_id=None, exam_name=None, 
                 exam_date=None, paper_number=None, duration_minutes=None,
                 exam_board=None, specification_code=None, is_active=True,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.subject_id = subject_id
        self.exam_name = exam_name
        self.exam_date = exam_date
        self.paper_number = paper_number
        self.duration_minutes = duration_minutes
        self.exam_board = exam_board
        self.specification_code = specification_code
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_exam_schedule(cls, user_id: str, subject_id: str, exam_name: str,
                           exam_date: date, paper_number: int = None,
                           duration_minutes: int = None, exam_board: str = None,
                           specification_code: str = None) -> 'GCSEExamSchedule':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        schedule_data = {
            'user_id': user_id,
            'subject_id': subject_id,
            'exam_name': exam_name,
            'exam_date': exam_date.isoformat() if isinstance(exam_date, date) else exam_date,
            'paper_number': paper_number,
            'duration_minutes': duration_minutes,
            'exam_board': exam_board,
            'specification_code': specification_code,
            'is_active': True
        }
        
        try:
            result = supabase.table('gcse_exam_schedules').insert(schedule_data).execute()
            if result.data:
                schedule_data = result.data[0]
                return cls(**schedule_data)
        except Exception as e:
            print(f"Error creating exam schedule: {e}")
            
        return None

    @classmethod
    def get_user_exam_schedules(cls, user_id: str, days_ahead: int = 365) -> List['GCSEExamSchedule']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            
            end_date = (datetime.now() + timedelta(days=days_ahead)).date().isoformat()
            result = supabase.table('gcse_exam_schedules').select('*').eq('user_id', user_id).gte('exam_date', datetime.now().date().isoformat()).lte('exam_date', end_date).eq('is_active', True).order('exam_date').execute()
            return [cls(**exam) for exam in result.data]
        except Exception as e:
            print(f"Error getting exam schedules: {e}")
            return []

    @classmethod
    def get_exam_countdown(cls, exam_date: date) -> Dict[str, any]:
        
        today = date.today()
        days_until = (exam_date - today).days
        
        if days_until < 0:
            return {"days": 0, "weeks": 0, "months": 0, "status": "past", "urgency": "none"}
        elif days_until == 0:
            return {"days": 0, "weeks": 0, "months": 0, "status": "today", "urgency": "critical"}
        elif days_until <= 7:
            return {"days": days_until, "weeks": 0, "months": 0, "status": "urgent", "urgency": "high"}
        elif days_until <= 30:
            weeks = days_until // 7
            remaining_days = days_until % 7
            return {"days": remaining_days, "weeks": weeks, "months": 0, "status": "soon", "urgency": "medium"}
        else:
            months = days_until // 30
            remaining_days = days_until % 30
            weeks = remaining_days // 7
            final_days = remaining_days % 7
            return {"days": final_days, "weeks": weeks, "months": months, "status": "upcoming", "urgency": "low"}


class GCSERevisionSchedule:
    
    
    def __init__(self, id=None, user_id=None, subject_id=None, topic_id=None,
                 revision_date=None, duration_minutes=None, revision_type=None,
                 priority_level=None, completed=False, notes=None,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.subject_id = subject_id
        self.topic_id = topic_id
        self.revision_date = revision_date
        self.duration_minutes = duration_minutes
        self.revision_type = revision_type  
        self.priority_level = priority_level  
        self.completed = completed
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_revision_schedule(cls, user_id: str, subject_id: str, topic_id: str,
                                revision_date: date, duration_minutes: int,
                                revision_type: str, priority_level: str = 'medium',
                                notes: str = None) -> 'GCSERevisionSchedule':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        schedule_data = {
            'user_id': user_id,
            'subject_id': subject_id,
            'topic_id': topic_id,
            'revision_date': revision_date.isoformat() if isinstance(revision_date, date) else revision_date,
            'duration_minutes': duration_minutes,
            'revision_type': revision_type,
            'priority_level': priority_level,
            'completed': False,
            'notes': notes
        }
        
        try:
            result = supabase.table('gcse_revision_schedules').insert(schedule_data).execute()
            if result.data:
                schedule_data = result.data[0]
                return cls(**schedule_data)
        except Exception as e:
            print(f"Error creating revision schedule: {e}")
            
        return None

    @classmethod
    def get_user_revision_schedule(cls, user_id: str, days_ahead: int = 30) -> List['GCSERevisionSchedule']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            end_date = (datetime.now() + timedelta(days=days_ahead)).date().isoformat()
            result = supabase.table('gcse_revision_schedules').select('*').eq('user_id', user_id).gte('revision_date', datetime.now().date().isoformat()).lte('revision_date', end_date).order('revision_date').order('priority_level').execute()
            return [cls(**schedule) for schedule in result.data]
        except Exception as e:
            print(f"Error getting revision schedule: {e}")
            return []


class GCSERevisionPlanner:
    
    
    @staticmethod
    def generate_smart_revision_plan(user_id: str, subject_id: str, exam_date: date,
                                    study_hours_per_week: int = 5) -> List[Dict]:
        
        
        today = date.today()
        days_until_exam = (exam_date - today).days
        
        if days_until_exam <= 0:
            return [{"error": "Exam date is in the past"}]
        
        
        total_study_hours = (days_until_exam / 7) * study_hours_per_week
        
        
        if days_until_exam <= 7:
            
            phases = [
                {
                    "phase": "intensive",
                    "duration_days": days_until_exam,
                    "study_hours_per_day": min(4, total_study_hours / days_until_exam),
                    "focus": "exam technique and quick review",
                    "revision_types": ["past_paper", "flashcards", "quick_review"]
                }
            ]
        elif days_until_exam <= 30:
            
            intensive_days = 7
            focused_days = days_until_exam - intensive_days
            focused_hours = total_study_hours - (intensive_days * 3)
            
            phases = [
                {
                    "phase": "focused",
                    "duration_days": focused_days,
                    "study_hours_per_day": min(2, focused_hours / focused_days),
                    "focus": "topic review and practice",
                    "revision_types": ["practice", "review", "flashcards"]
                },
                {
                    "phase": "intensive",
                    "duration_days": intensive_days,
                    "study_hours_per_day": 3,
                    "focus": "exam technique and final review",
                    "revision_types": ["past_paper", "flashcards", "quick_review"]
                }
            ]
        else:
            
            intensive_days = 7
            focused_days = 21
            comprehensive_days = days_until_exam - intensive_days - focused_days
            comprehensive_hours = total_study_hours - (intensive_days * 3) - (focused_days * 2)
            
            phases = [
                {
                    "phase": "comprehensive",
                    "duration_days": comprehensive_days,
                    "study_hours_per_day": min(1.5, comprehensive_hours / comprehensive_days),
                    "focus": "deep understanding and foundation",
                    "revision_types": ["review", "practice", "concept_mapping"]
                },
                {
                    "phase": "focused",
                    "duration_days": focused_days,
                    "study_hours_per_day": 2,
                    "focus": "topic consolidation and practice",
                    "revision_types": ["practice", "review", "flashcards"]
                },
                {
                    "phase": "intensive",
                    "duration_days": intensive_days,
                    "study_hours_per_day": 3,
                    "focus": "exam technique and final review",
                    "revision_types": ["past_paper", "flashcards", "quick_review"]
                }
            ]
        
        return phases

    @staticmethod
    def schedule_revision_sessions(user_id: str, subject_id: str, exam_date: date,
                                  study_hours_per_week: int = 5) -> List['GCSERevisionSchedule']:
        
        
        phases = GCSERevisionPlanner.generate_smart_revision_plan(
            user_id, subject_id, exam_date, study_hours_per_week
        )
        
        if phases and "error" in phases[0]:
            return []
        
        scheduled_sessions = []
        current_date = date.today()
        
        for phase in phases:
            phase_duration = phase["duration_days"]
            study_hours_per_day = phase["study_hours_per_day"]
            revision_types = phase["revision_types"]
            
            
            for day in range(phase_duration):
                session_date = current_date + timedelta(days=day)
                
                
                sessions_per_day = max(1, int(study_hours_per_day))
                session_duration = int((study_hours_per_day * 60) / sessions_per_day)
                
                for session_num in range(sessions_per_day):
                    
                    revision_type = revision_types[session_num % len(revision_types)]
                    
                    
                    days_until_exam = (exam_date - session_date).days
                    if days_until_exam <= 7:
                        priority = "high"
                    elif days_until_exam <= 30:
                        priority = "medium"
                    else:
                        priority = "low"
                    
                    
                    schedule = GCSERevisionSchedule.create_revision_schedule(
                        user_id=user_id,
                        subject_id=subject_id,
                        topic_id=None,  
                        revision_date=session_date,
                        duration_minutes=session_duration,
                        revision_type=revision_type,
                        priority_level=priority,
                        notes=f"{phase['phase'].title()} revision - {phase['focus']}"
                    )
                    
                    if schedule:
                        scheduled_sessions.append(schedule)
        
        return scheduled_sessions

    @staticmethod
    def get_daily_revision_schedule(user_id: str, target_date: date = None) -> Dict:
        
        
        if target_date is None:
            target_date = date.today()
        
        
        revision_sessions = GCSERevisionSchedule.get_user_revision_schedule(user_id, 1)
        daily_sessions = [s for s in revision_sessions if s.revision_date == target_date]
        
        
        exam_schedules = GCSEExamSchedule.get_user_exam_schedules(user_id, 90)
        upcoming_exams = [e for e in exam_schedules if e.exam_date >= target_date]
        
        
        total_study_time = sum(s.duration_minutes for s in daily_sessions)
        
        
        high_priority = [s for s in daily_sessions if s.priority_level == "high"]
        medium_priority = [s for s in daily_sessions if s.priority_level == "medium"]
        low_priority = [s for s in daily_sessions if s.priority_level == "low"]
        
        return {
            "date": target_date,
            "total_sessions": len(daily_sessions),
            "total_study_time_minutes": total_study_time,
            "total_study_time_hours": round(total_study_time / 60, 1),
            "sessions": {
                "high_priority": high_priority,
                "medium_priority": medium_priority,
                "low_priority": low_priority
            },
            "upcoming_exams": upcoming_exams[:3],  
            "study_intensity": "high" if total_study_time >= 180 else "medium" if total_study_time >= 60 else "light"
        }


class GCSEStudyReminder:
    
    
    def __init__(self, id=None, user_id=None, reminder_type=None, subject_id=None,
                 reminder_date=None, reminder_time=None, message=None,
                 is_active=True, created_at=None):
        self.id = id
        self.user_id = user_id
        self.reminder_type = reminder_type  
        self.subject_id = subject_id
        self.reminder_date = reminder_date
        self.reminder_time = reminder_time
        self.message = message
        self.is_active = is_active
        self.created_at = created_at

    @classmethod
    def create_reminder(cls, user_id: str, reminder_type: str, subject_id: str,
                       reminder_date: date, reminder_time: str, message: str) -> 'GCSEStudyReminder':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        reminder_data = {
            'user_id': user_id,
            'reminder_type': reminder_type,
            'subject_id': subject_id,
            'reminder_date': reminder_date.isoformat() if isinstance(reminder_date, date) else reminder_date,
            'reminder_time': reminder_time,
            'message': message,
            'is_active': True
        }
        
        try:
            result = supabase.table('gcse_study_reminders').insert(reminder_data).execute()
            if result.data:
                reminder_data = result.data[0]
                return cls(**reminder_data)
        except Exception as e:
            print(f"Error creating study reminder: {e}")
            
        return None

    @classmethod
    def get_user_reminders(cls, user_id: str, days_ahead: int = 7) -> List['GCSEStudyReminder']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            end_date = (datetime.now() + timedelta(days=days_ahead)).date().isoformat()
            result = supabase.table('gcse_study_reminders').select('*').eq('user_id', user_id).gte('reminder_date', datetime.now().date().isoformat()).lte('reminder_date', end_date).eq('is_active', True).order('reminder_date').order('reminder_time').execute()
            return [cls(**reminder) for reminder in result.data]
        except Exception as e:
            print(f"Error getting study reminders: {e}")
            return []

    @staticmethod
    def create_exam_countdown_reminders(user_id: str, exam_schedules: List['GCSEExamSchedule']) -> List['GCSEStudyReminder']:
        
        
        reminders = []
        today = date.today()
        
        for exam in exam_schedules:
            if not exam.exam_date:
                continue
                
            exam_date = exam.exam_date
            if isinstance(exam_date, str):
                exam_date = datetime.strptime(exam_date, '%Y-%m-%d').date()
            
            
            reminder_intervals = [30, 14, 7, 3, 1]  
            
            for days_before in reminder_intervals:
                reminder_date = exam_date - timedelta(days=days_before)
                
                if reminder_date >= today:
                    if days_before == 1:
                        message = f"🚨 {exam.exam_name} is TOMORROW! Final preparation time."
                    elif days_before <= 3:
                        message = f"⚠️ {exam.exam_name} is in {days_before} days. Focus on exam technique!"
                    elif days_before <= 7:
                        message = f"📚 {exam.exam_name} is in {days_before} days. Time for intensive revision!"
                    elif days_before <= 14:
                        message = f"⏰ {exam.exam_name} is in {days_before} days. Keep up the revision momentum!"
                    else:
                        message = f"📅 {exam.exam_name} is in {days_before} days. Plan your revision strategy!"
                    
                    reminder = GCSEStudyReminder.create_reminder(
                        user_id=user_id,
                        reminder_type="exam_countdown",
                        subject_id=exam.subject_id,
                        reminder_date=reminder_date,
                        reminder_time="09:00",
                        message=message
                    )
                    
                    if reminder:
                        reminders.append(reminder)
        
        return reminders


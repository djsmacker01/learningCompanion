

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import json

class GCSESubject:
    
    
    def __init__(self, id=None, subject_name=None, exam_board=None, specification_code=None,
                 subject_code=None, is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.subject_name = subject_name
        self.exam_board = exam_board  
        self.specification_code = specification_code
        self.subject_code = subject_code
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
        self.topics = []  

    @classmethod
    def create_subject(cls, subject_name: str, exam_board: str, 
                      specification_code: str = None, subject_code: str = None) -> 'GCSESubject':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        subject_data = {
            'subject_name': subject_name,
            'exam_board': exam_board,
            'specification_code': specification_code,
            'subject_code': subject_code,
            'is_active': True
        }
        
        try:
            result = supabase.table('gcse_subjects').insert(subject_data).execute()
            if result.data:
                subject_data = result.data[0]
                return cls(**subject_data)
        except Exception as e:
            print(f"Error creating GCSE subject: {e}")
            
        return None

    @classmethod
    def get_all_subjects(cls) -> List['GCSESubject']:
        
        print(f"DEBUG: Getting GCSE subjects... SUPABASE_AVAILABLE={SUPABASE_AVAILABLE}")
        
        if not SUPABASE_AVAILABLE:
            print("DEBUG: Supabase not available, returning default subjects")
            defaults = cls._get_default_subjects()
            print(f"DEBUG: Returning {len(defaults)} default subjects")
            return defaults
            
        supabase = get_supabase_client()
        
        try:
            print("DEBUG: Querying gcse_subjects table...")
            result = supabase.table('gcse_subjects').select('*').eq('is_active', True).order('subject_name').execute()
            print(f"DEBUG: Query returned {len(result.data)} subjects from database")
            
            if not result.data or len(result.data) == 0:
                print("DEBUG: No subjects in database, falling back to defaults")
                return cls._get_default_subjects()
            
            subjects = [cls(**subject) for subject in result.data]
            
            
            for subject in subjects:
                subject.topics = GCSETopic.get_topics_by_subject(subject.id)
                
            return subjects
        except Exception as e:
            print(f"ERROR getting GCSE subjects from database: {e}")
            import traceback
            traceback.print_exc()
            print("DEBUG: Exception occurred, falling back to default subjects")
            return cls._get_default_subjects()

    @classmethod
    def get_subject_by_id(cls, subject_id: str) -> Optional['GCSESubject']:
        
        if not SUPABASE_AVAILABLE:

            default_subjects = cls._get_default_subjects()
            for subject in default_subjects:
                if subject.id == subject_id:
                    subject.topics = GCSETopic.get_topics_by_subject(subject.id)
                    return subject
            return None
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_subjects').select('*').eq('id', subject_id).eq('is_active', True).execute()
            if result.data:
                subject = cls(**result.data[0])
                subject.topics = GCSETopic.get_topics_by_subject(subject.id)
                return subject
        except Exception as e:
            print(f"Error getting GCSE subject by ID: {e}")

            default_subjects = cls._get_default_subjects()
            for subject in default_subjects:
                if subject.id == subject_id:
                    subject.topics = GCSETopic.get_topics_by_subject(subject.id)
                    return subject
            
        return None

    @classmethod
    def _get_default_subjects(cls) -> List['GCSESubject']:
        
        return [

            cls(
                id="1",
                subject_name="Mathematics",
                exam_board="AQA",
                specification_code="8300",
                subject_code="MATHS"
            ),
            cls(
                id="2", 
                subject_name="English Language",
                exam_board="AQA",
                specification_code="8700",
                subject_code="ENGLANG"
            ),
            cls(
                id="3",
                subject_name="English Literature", 
                exam_board="AQA",
                specification_code="8702",
                subject_code="ENGLIT"
            ),
            cls(
                id="4",
                subject_name="Biology",
                exam_board="AQA", 
                specification_code="8461",
                subject_code="BIO"
            ),
            cls(
                id="5",
                subject_name="Chemistry",
                exam_board="AQA",
                specification_code="8462", 
                subject_code="CHEM"
            ),

            cls(
                id="6",
                subject_name="Physics",
                exam_board="Edexcel",
                specification_code="1PH0",
                subject_code="PHYS"
            ),
            cls(
                id="7",
                subject_name="History",
                exam_board="Edexcel",
                specification_code="1HI0",
                subject_code="HIST"
            ),
            cls(
                id="8",
                subject_name="Geography", 
                exam_board="Edexcel",
                specification_code="1GA0",
                subject_code="GEOG"
            ),
            cls(
                id="9",
                subject_name="French",
                exam_board="Edexcel",
                specification_code="1FR0",
                subject_code="FRENCH"
            ),

            cls(
                id="10",
                subject_name="Spanish",
                exam_board="OCR",
                specification_code="J732",
                subject_code="SPANISH"
            ),
            cls(
                id="11",
                subject_name="German",
                exam_board="OCR",
                specification_code="J732",
                subject_code="GERMAN"
            ),
            cls(
                id="12",
                subject_name="Computer Science",
                exam_board="OCR",
                specification_code="J277",
                subject_code="COMPSCI"
            ),
            cls(
                id="13",
                subject_name="Business Studies",
                exam_board="OCR",
                specification_code="J204",
                subject_code="BUSINESS"
            ),

            cls(
                id="14",
                subject_name="Economics",
                exam_board="WJEC",
                specification_code="C700U",
                subject_code="ECONOMICS"
            ),
            cls(
                id="15",
                subject_name="Psychology",
                exam_board="WJEC",
                specification_code="C860U",
                subject_code="PSYCHOLOGY"
            ),
            cls(
                id="16",
                subject_name="Sociology",
                exam_board="WJEC",
                specification_code="C690U",
                subject_code="SOCIOLOGY"
            ),
            cls(
                id="17",
                subject_name="Art & Design",
                exam_board="WJEC",
                specification_code="C650U",
                subject_code="ART"
            ),

            cls(
                id="18",
                subject_name="Music",
                exam_board="Edexcel",
                specification_code="1MU0",
                subject_code="MUSIC"
            ),
            cls(
                id="19",
                subject_name="Drama",
                exam_board="OCR",
                specification_code="J316",
                subject_code="DRAMA"
            ),
            cls(
                id="20",
                subject_name="Physical Education",
                exam_board="AQA",
                specification_code="8582",
                subject_code="PE"
            )
        ]


class GCSETopic:
    
    
    def __init__(self, id=None, subject_id=None, topic_name=None, topic_number=None,
                 topic_description=None, learning_objectives=None, exam_weight=None,
                 difficulty_level=None, is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.subject_id = subject_id
        self.topic_name = topic_name
        self.topic_number = topic_number
        self.topic_description = topic_description
        self.learning_objectives = learning_objectives  
        self.exam_weight = exam_weight  
        self.difficulty_level = difficulty_level  
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_topic(cls, subject_id: str, topic_name: str, topic_number: str,
                    topic_description: str = None, learning_objectives: List[str] = None,
                    exam_weight: float = None, difficulty_level: str = 'Both') -> 'GCSETopic':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        topic_data = {
            'subject_id': subject_id,
            'topic_name': topic_name,
            'topic_number': topic_number,
            'topic_description': topic_description,
            'learning_objectives': json.dumps(learning_objectives) if learning_objectives else None,
            'exam_weight': exam_weight,
            'difficulty_level': difficulty_level,
            'is_active': True
        }
        
        try:
            result = supabase.table('gcse_topics').insert(topic_data).execute()
            if result.data:
                topic_data = result.data[0]
                if topic_data.get('learning_objectives'):
                    topic_data['learning_objectives'] = json.loads(topic_data['learning_objectives'])
                return cls(**topic_data)
        except Exception as e:
            print(f"Error creating GCSE topic: {e}")
            
        return None

    @classmethod
    def get_topics_by_subject(cls, subject_id: str) -> List['GCSETopic']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_topics(subject_id)
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_topics').select('*').eq('subject_id', subject_id).eq('is_active', True).order('topic_number').execute()
            topics = []
            for topic_data in result.data:
                if topic_data.get('learning_objectives'):
                    topic_data['learning_objectives'] = json.loads(topic_data['learning_objectives'])
                topics.append(cls(**topic_data))
            return topics
        except Exception as e:
            print(f"Error getting GCSE topics: {e}")
            return cls._get_default_topics(subject_id)

    @classmethod
    def _get_default_topics(cls, subject_id: str) -> List['GCSETopic']:
        
        default_topics = {
            "1": [
                cls(id="1", subject_id="1", topic_name="Number", topic_number="1", 
                    topic_description="Basic number operations, fractions, decimals, percentages",
                    exam_weight=25.0, difficulty_level="Both"),
                cls(id="2", subject_id="1", topic_name="Algebra", topic_number="2",
                    topic_description="Expressions, equations, sequences, graphs",
                    exam_weight=30.0, difficulty_level="Both"),
                cls(id="3", subject_id="1", topic_name="Ratio, Proportion & Rates of Change", topic_number="3",
                    topic_description="Ratios, proportions, percentages, rates",
                    exam_weight=15.0, difficulty_level="Both"),
                cls(id="4", subject_id="1", topic_name="Geometry & Measures", topic_number="4",
                    topic_description="Shapes, angles, area, volume, transformations",
                    exam_weight=20.0, difficulty_level="Both"),
                cls(id="5", subject_id="1", topic_name="Probability & Statistics", topic_number="5",
                    topic_description="Data handling, probability, statistics",
                    exam_weight=10.0, difficulty_level="Both")
            ],
            "2": [
                cls(id="6", subject_id="2", topic_name="Reading Skills", topic_number="1",
                    topic_description="Comprehension, analysis, evaluation",
                    exam_weight=40.0, difficulty_level="Both"),
                cls(id="7", subject_id="2", topic_name="Writing Skills", topic_number="2",
                    topic_description="Creative writing, transactional writing",
                    exam_weight=40.0, difficulty_level="Both"),
                cls(id="8", subject_id="2", topic_name="Spoken Language", topic_number="3",
                    topic_description="Speaking and listening skills",
                    exam_weight=20.0, difficulty_level="Both")
            ],
            "4": [
                cls(id="9", subject_id="4", topic_name="Cell Biology", topic_number="1",
                    topic_description="Cell structure, transport, division",
                    exam_weight=15.0, difficulty_level="Both"),
                cls(id="10", subject_id="4", topic_name="Organisation", topic_number="2",
                    topic_description="Organ systems, digestive system, circulatory system",
                    exam_weight=20.0, difficulty_level="Both"),
                cls(id="11", subject_id="4", topic_name="Infection & Response", topic_number="3",
                    topic_description="Pathogens, immune system, vaccination",
                    exam_weight=15.0, difficulty_level="Both"),
                cls(id="12", subject_id="4", topic_name="Bioenergetics", topic_number="4",
                    topic_description="Photosynthesis, respiration",
                    exam_weight=15.0, difficulty_level="Both"),
                cls(id="13", subject_id="4", topic_name="Homeostasis & Response", topic_number="5",
                    topic_description="Nervous system, endocrine system, homeostasis",
                    exam_weight=15.0, difficulty_level="Both"),
                cls(id="14", subject_id="4", topic_name="Inheritance, Variation & Evolution", topic_number="6",
                    topic_description="Genetics, evolution, natural selection",
                    exam_weight=20.0, difficulty_level="Both")
            ],
            "5": [
                cls(id="15", subject_id="5", topic_name="Atomic Structure", topic_number="1",
                    topic_description="Atoms, elements, compounds, mixtures",
                    exam_weight=20.0, difficulty_level="Both"),
                cls(id="16", subject_id="5", topic_name="Bonding & Structure", topic_number="2",
                    topic_description="Ionic, covalent, metallic bonding",
                    exam_weight=20.0, difficulty_level="Both"),
                cls(id="17", subject_id="5", topic_name="Quantitative Chemistry", topic_number="3",
                    topic_description="Moles, calculations, equations",
                    exam_weight=15.0, difficulty_level="Both"),
                cls(id="18", subject_id="5", topic_name="Chemical Changes", topic_number="4",
                    topic_description="Acids, bases, electrolysis, redox",
                    exam_weight=20.0, difficulty_level="Both"),
                cls(id="19", subject_id="5", topic_name="Energy Changes", topic_number="5",
                    topic_description="Exothermic, endothermic reactions",
                    exam_weight=15.0, difficulty_level="Both"),
                cls(id="20", subject_id="5", topic_name="Rate & Extent of Change", topic_number="6",
                    topic_description="Reaction rates, equilibrium",
                    exam_weight=10.0, difficulty_level="Both")
            ],
            "6": [
                cls(id="21", subject_id="6", topic_name="Energy", topic_number="1",
                    topic_description="Energy stores, transfers, efficiency",
                    exam_weight=20.0, difficulty_level="Both"),
                cls(id="22", subject_id="6", topic_name="Electricity", topic_number="2",
                    topic_description="Current, voltage, resistance, circuits",
                    exam_weight=20.0, difficulty_level="Both"),
                cls(id="23", subject_id="6", topic_name="Particle Model", topic_number="3",
                    topic_description="States of matter, pressure, gas laws",
                    exam_weight=15.0, difficulty_level="Both"),
                cls(id="24", subject_id="6", topic_name="Atomic Structure", topic_number="4",
                    topic_description="Radioactivity, nuclear fission, fusion",
                    exam_weight=15.0, difficulty_level="Both"),
                cls(id="25", subject_id="6", topic_name="Forces", topic_number="5",
                    topic_description="Motion, forces, pressure, moments",
                    exam_weight=20.0, difficulty_level="Both"),
                cls(id="26", subject_id="6", topic_name="Waves", topic_number="6",
                    topic_description="Properties of waves, electromagnetic spectrum",
                    exam_weight=10.0, difficulty_level="Both")
            ]
        }
        return default_topics.get(subject_id, [])


class GCSESpecification:
    
    
    @staticmethod
    def get_exam_boards() -> List[str]:
        
        return ["AQA", "Edexcel", "OCR", "WJEC", "CCEA"]

    @staticmethod
    def get_subject_specifications(subject_name: str) -> Dict[str, Dict]:
        
        specifications = {
            "Mathematics": {
                "AQA": {"code": "8300", "name": "Mathematics", "papers": 3, "duration": "90min each"},
                "Edexcel": {"code": "1MA1", "name": "Mathematics", "papers": 3, "duration": "90min each"},
                "OCR": {"code": "J560", "name": "Mathematics", "papers": 3, "duration": "90min each"}
            },
            "Biology": {
                "AQA": {"code": "8461", "name": "Biology", "papers": 2, "duration": "105min each"},
                "Edexcel": {"code": "1BI0", "name": "Biology", "papers": 2, "duration": "110min each"},
                "OCR": {"code": "J257", "name": "Biology", "papers": 2, "duration": "105min each"}
            },
            "Chemistry": {
                "AQA": {"code": "8462", "name": "Chemistry", "papers": 2, "duration": "105min each"},
                "Edexcel": {"code": "1CH0", "name": "Chemistry", "papers": 2, "duration": "110min each"},
                "OCR": {"code": "J258", "name": "Chemistry", "papers": 2, "duration": "105min each"}
            },
            "Physics": {
                "AQA": {"code": "8463", "name": "Physics", "papers": 2, "duration": "105min each"},
                "Edexcel": {"code": "1PH0", "name": "Physics", "papers": 2, "duration": "110min each"},
                "OCR": {"code": "J259", "name": "Physics", "papers": 2, "duration": "105min each"}
            }
        }
        return specifications.get(subject_name, {})

    @staticmethod
    def get_grade_boundaries(exam_board: str, subject_code: str, year: int = 2023) -> Dict[str, Dict]:
        
        
        mock_boundaries = {
            "AQA": {
                "8300": {  
                    "Foundation": {"5": 77, "4": 65, "3": 53},
                    "Higher": {"9": 214, "8": 186, "7": 158, "6": 130, "5": 102, "4": 74}
                },
                "8461": {  
                    "Foundation": {"5": 69, "4": 58, "3": 47},
                    "Higher": {"9": 131, "8": 119, "7": 107, "6": 95, "5": 83, "4": 71}
                }
            }
        }
        return mock_boundaries.get(exam_board, {}).get(subject_code, {})


class GCSEExam:
    
    
    def __init__(self, id=None, subject_id=None, exam_name=None, exam_date=None,
                 paper_number=None, duration_minutes=None, total_marks=None,
                 exam_board=None, specification_code=None, user_id=None, is_active=True,
                 created_at=None, updated_at=None):
        self.id = id
        self.subject_id = subject_id
        self.exam_name = exam_name
        self.exam_date = exam_date
        self.paper_number = paper_number
        self.duration_minutes = duration_minutes
        self.total_marks = total_marks
        self.exam_board = exam_board
        self.specification_code = specification_code
        self.user_id = user_id
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_exam(cls, user_id: str, subject_id: str, exam_name: str, exam_date: date,
                   paper_number: int = None, duration_minutes: int = None,
                   total_marks: int = None, exam_board: str = None,
                   specification_code: str = None) -> 'GCSEExam':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        exam_data = {
            'user_id': str(user_id),
            'subject_id': str(subject_id),
            'exam_name': exam_name,
            'exam_date': exam_date.isoformat() if isinstance(exam_date, date) else exam_date,
            'paper_number': paper_number,
            'duration_minutes': duration_minutes,
            'total_marks': total_marks,
            'exam_board': exam_board,
            'specification_code': specification_code,
            'is_active': True
        }
        
        try:
            result = supabase.table('gcse_exams').insert(exam_data).execute()
            if result.data:
                exam_data = result.data[0]
                return cls(**exam_data)
            else:
                print(f"No data returned from insert: {result}")
        except Exception as e:
            print(f"Error creating GCSE exam: {e}")
            import traceback
            traceback.print_exc()
            
        return None

    @classmethod
    def get_upcoming_exams(cls, user_id: str = None, days_ahead: int = 365) -> List['GCSEExam']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            end_date = (datetime.now() + timedelta(days=days_ahead)).date().isoformat()
            query = supabase.table('gcse_exams').select('*').gte('exam_date', datetime.now().date().isoformat()).lte('exam_date', end_date).eq('is_active', True)
            

            if user_id:
                query = query.eq('user_id', str(user_id))
            
            result = query.order('exam_date').execute()
            return [cls(**exam) for exam in result.data]
        except Exception as e:
            print(f"Error getting upcoming exams: {e}")
            import traceback
            traceback.print_exc()
            return []

    @staticmethod
    def get_exam_countdown(exam_date: date) -> Dict[str, int]:
        
        today = date.today()
        days_until = (exam_date - today).days
        
        if days_until < 0:
            return {"days": 0, "weeks": 0, "months": 0, "status": "past"}
        elif days_until == 0:
            return {"days": 0, "weeks": 0, "months": 0, "status": "today"}
        elif days_until <= 7:
            return {"days": days_until, "weeks": 0, "months": 0, "status": "urgent"}
        elif days_until <= 30:
            weeks = days_until // 7
            remaining_days = days_until % 7
            return {"days": remaining_days, "weeks": weeks, "months": 0, "status": "soon"}
        else:
            months = days_until // 30
            remaining_days = days_until % 30
            weeks = remaining_days // 7
            final_days = remaining_days % 7
            return {"days": final_days, "weeks": weeks, "months": months, "status": "upcoming"}


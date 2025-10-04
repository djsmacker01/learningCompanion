

from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import json

class GCSEStudyTechnique:
    
    
    def __init__(self, id=None, technique_name=None, category=None, subject_applicability=None,
                 difficulty_level=None, time_required=None, effectiveness_rating=None,
                 description=None, step_by_step_guide=None, tips_and_tricks=None,
                 when_to_use=None, examples=None, is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.technique_name = technique_name
        self.category = category  
        self.subject_applicability = subject_applicability  
        self.difficulty_level = difficulty_level  
        self.time_required = time_required  
        self.effectiveness_rating = effectiveness_rating  
        self.description = description
        self.step_by_step_guide = step_by_step_guide
        self.tips_and_tricks = tips_and_tricks
        self.when_to_use = when_to_use
        self.examples = examples
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_all_techniques(cls, category=None, subject=None, difficulty=None) -> List['GCSEStudyTechnique']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_techniques()
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('gcse_study_techniques').select('*').eq('is_active', True)
            
            if category:
                query = query.eq('category', category)
            if subject:
                
                query = query.or_(f'subject_applicability.eq.all,subject_applicability.eq.{subject}')
            if difficulty:
                query = query.eq('difficulty_level', difficulty)
            
            result = query.order('effectiveness_rating', desc=True).order('technique_name').execute()
            return [cls(**technique) for technique in result.data]
        except Exception as e:
            print(f"Error getting study techniques: {e}")
            return cls._get_default_techniques()

    @classmethod
    def get_technique_by_id(cls, technique_id: str) -> Optional['GCSEStudyTechnique']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_technique_by_id(technique_id)
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_study_techniques').select('*').eq('id', technique_id).eq('is_active', True).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error getting study technique: {e}")
            
        return cls._get_default_technique_by_id(technique_id)

    @classmethod
    def _get_default_techniques(cls) -> List['GCSEStudyTechnique']:
        
        return [
            cls(
                id="1",
                technique_name="Active Recall",
                category="memorization",
                subject_applicability="all",
                difficulty_level="intermediate",
                time_required="medium",
                effectiveness_rating=5,
                description="Test yourself on information without looking at notes to strengthen memory",
                step_by_step_guide=[
                    "Write down everything you remember about a topic",
                    "Check against your notes for accuracy",
                    "Identify gaps in your knowledge",
                    "Focus study time on the gaps",
                    "Repeat the process regularly"
                ],
                tips_and_tricks=[
                    "Use flashcards for quick active recall",
                    "Try to explain concepts out loud",
                    "Test yourself at increasing intervals",
                    "Don't just re-read notes - actively test knowledge"
                ],
                when_to_use="Best for memorizing facts, formulas, and key concepts",
                examples=["Testing yourself on biology definitions", "Recalling mathematical formulas", "Remembering historical dates"]
            ),
            cls(
                id="2",
                technique_name="Spaced Repetition",
                category="memorization",
                subject_applicability="all",
                difficulty_level="beginner",
                time_required="long",
                effectiveness_rating=5,
                description="Review information at increasing intervals to improve long-term retention",
                step_by_step_guide=[
                    "Learn new material thoroughly",
                    "Review after 1 day",
                    "Review after 3 days",
                    "Review after 1 week",
                    "Review after 2 weeks",
                    "Review after 1 month"
                ],
                tips_and_tricks=[
                    "Use apps like Anki for automated scheduling",
                    "Be consistent with review sessions",
                    "Adjust intervals based on difficulty",
                    "Focus more time on difficult material"
                ],
                when_to_use="Perfect for long-term retention of facts and concepts",
                examples=["Learning vocabulary", "Memorizing scientific formulas", "Remembering historical facts"]
            ),
            cls(
                id="3",
                technique_name="Mind Mapping",
                category="understanding",
                subject_applicability="all",
                difficulty_level="beginner",
                time_required="medium",
                effectiveness_rating=4,
                description="Create visual diagrams to organize and connect information",
                step_by_step_guide=[
                    "Start with main topic in center",
                    "Add major subtopics as branches",
                    "Add details to each branch",
                    "Use colors and symbols",
                    "Review and refine connections"
                ],
                tips_and_tricks=[
                    "Use different colors for different topics",
                    "Keep branches short with key words",
                    "Add images and symbols for visual memory",
                    "Review maps regularly to reinforce connections"
                ],
                when_to_use="Great for understanding relationships between concepts",
                examples=["Biology: ecosystem relationships", "History: causes of World War I", "Literature: character relationships"]
            ),
            cls(
                id="4",
                technique_name="Past Paper Practice",
                category="practice",
                subject_applicability="all",
                difficulty_level="intermediate",
                time_required="long",
                effectiveness_rating=5,
                description="Practice with real exam questions under timed conditions",
                step_by_step_guide=[
                    "Complete past paper under exam conditions",
                    "Mark your answers honestly",
                    "Identify areas of weakness",
                    "Study weak areas thoroughly",
                    "Repeat with different past papers"
                ],
                tips_and_tricks=[
                    "Time yourself to practice exam technique",
                    "Focus on question command words",
                    "Practice different question types",
                    "Review mark schemes for key points"
                ],
                when_to_use="Essential for exam preparation and technique",
                examples=["Math: solving equations under time pressure", "English: essay writing practice", "Science: practical questions"]
            ),
            cls(
                id="5",
                technique_name="Feynman Technique",
                category="understanding",
                subject_applicability="sciences",
                difficulty_level="advanced",
                time_required="medium",
                effectiveness_rating=4,
                description="Explain complex concepts in simple terms to deepen understanding",
                step_by_step_guide=[
                    "Choose a concept to learn",
                    "Explain it in simple terms",
                    "Identify gaps in your explanation",
                    "Return to source material",
                    "Simplify and clarify",
                    "Teach someone else"
                ],
                tips_and_tricks=[
                    "Use analogies and examples",
                    "Avoid jargon and technical terms",
                    "Focus on the 'why' not just the 'what'",
                    "Practice explaining to different audiences"
                ],
                when_to_use="Best for understanding complex scientific concepts",
                examples=["Physics: explaining gravity", "Chemistry: understanding chemical bonds", "Biology: explaining photosynthesis"]
            ),
            cls(
                id="6",
                technique_name="Pomodoro Technique",
                category="exam_technique",
                subject_applicability="all",
                difficulty_level="beginner",
                time_required="quick",
                effectiveness_rating=4,
                description="Study in focused 25-minute intervals with short breaks",
                step_by_step_guide=[
                    "Set timer for 25 minutes",
                    "Focus entirely on one task",
                    "Take 5-minute break",
                    "Repeat cycle 4 times",
                    "Take longer 15-30 minute break"
                ],
                tips_and_tricks=[
                    "Eliminate distractions during focus time",
                    "Use breaks for physical movement",
                    "Track completed pomodoros",
                    "Adjust intervals based on attention span"
                ],
                when_to_use="Great for maintaining focus during long study sessions",
                examples=["Reading textbooks", "Writing essays", "Solving math problems", "Reviewing notes"]
            )
        ]

    @classmethod
    def _get_default_technique_by_id(cls, technique_id: str) -> Optional['GCSEStudyTechnique']:
        
        techniques = cls._get_default_techniques()
        for technique in techniques:
            if technique.id == technique_id:
                return technique
        return None


class GCSEExamStrategy:
    
    
    def __init__(self, id=None, strategy_name=None, exam_type=None, subject_applicability=None,
                 strategy_type=None, description=None, step_by_step_guide=None,
                 time_management_tips=None, common_mistakes=None, success_tips=None,
                 is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.strategy_name = strategy_name
        self.exam_type = exam_type  
        self.subject_applicability = subject_applicability
        self.strategy_type = strategy_type  
        self.description = description
        self.step_by_step_guide = step_by_step_guide
        self.time_management_tips = time_management_tips
        self.common_mistakes = common_mistakes
        self.success_tips = success_tips
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_strategies_by_type(cls, strategy_type=None, exam_type=None, subject=None) -> List['GCSEExamStrategy']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_strategies()
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('gcse_exam_strategies').select('*').eq('is_active', True)
            
            if strategy_type:
                query = query.eq('strategy_type', strategy_type)
            if exam_type:
                query = query.eq('exam_type', exam_type)
            if subject:
                query = query.or_(f'subject_applicability.eq.all,subject_applicability.eq.{subject}')
            
            result = query.order('strategy_name').execute()
            return [cls(**strategy) for strategy in result.data]
        except Exception as e:
            print(f"Error getting exam strategies: {e}")
            return cls._get_default_strategies()

    @classmethod
    def _get_default_strategies(cls) -> List['GCSEExamStrategy']:
        
        return [
            cls(
                id="1",
                strategy_name="Read All Questions First",
                exam_type="all",
                subject_applicability="all",
                strategy_type="question_approach",
                description="Read through all questions before starting to plan your time effectively",
                step_by_step_guide=[
                    "Quickly scan all questions in the paper",
                    "Identify easy questions you can answer quickly",
                    "Note difficult questions that need more time",
                    "Allocate time based on marks per question",
                    "Start with questions you're most confident about"
                ],
                time_management_tips=[
                    "Spend 5-10 minutes reading through the paper",
                    "Allocate 1.5-2 minutes per mark",
                    "Leave 10-15 minutes at the end for checking",
                    "Don't spend too long on any single question"
                ],
                common_mistakes=[
                    "Starting with the first question without planning",
                    "Spending too much time on difficult questions early",
                    "Running out of time for easier questions",
                    "Not leaving time for checking answers"
                ],
                success_tips=[
                    "Answer easy questions first to build confidence",
                    "Show your working even for simple calculations",
                    "If stuck, move on and return later",
                    "Use the full time allocated"
                ]
            ),
            cls(
                id="2",
                strategy_name="Command Word Recognition",
                exam_type="all",
                subject_applicability="all",
                strategy_type="question_approach",
                description="Understand what each command word requires to answer questions correctly",
                step_by_step_guide=[
                    "Identify the command word in the question",
                    "Understand what the command word requires",
                    "Structure your answer accordingly",
                    "Check you've addressed the command word",
                    "Ensure your answer matches the mark allocation"
                ],
                time_management_tips=[
                    "Command words indicate time needed: 'explain' needs more time than 'state'",
                    "Higher mark questions usually need more detailed answers",
                    "Plan your answer structure before writing"
                ],
                common_mistakes=[
                    "Confusing 'describe' with 'explain'",
                    "Not providing enough detail for 'evaluate' questions",
                    "Listing when asked to 'compare'",
                    "Not addressing all parts of multi-part questions"
                ],
                success_tips=[
                    "Learn command word meanings thoroughly",
                    "Practice identifying command words in past papers",
                    "Structure answers to match command requirements",
                    "Use command words in your answer structure"
                ]
            ),
            cls(
                id="3",
                strategy_name="Show Your Working",
                exam_type="calculation",
                subject_applicability="maths",
                strategy_type="question_approach",
                description="Always show clear working for mathematical and scientific calculations",
                step_by_step_guide=[
                    "Write down the formula or equation you're using",
                    "Substitute values clearly",
                    "Show each step of your calculation",
                    "Write your final answer clearly",
                    "Check your answer makes sense"
                ],
                time_management_tips=[
                    "Don't rush calculations - accuracy is more important",
                    "Use rough working space effectively",
                    "Double-check calculations before moving on"
                ],
                common_mistakes=[
                    "Not showing working steps",
                    "Using incorrect units",
                    "Rounding errors",
                    "Not checking if answer is reasonable"
                ],
                success_tips=[
                    "Even if you get the wrong answer, you can get marks for correct method",
                    "Use standard mathematical notation",
                    "Check units are consistent",
                    "Estimate answers to check reasonableness"
                ]
            ),
            cls(
                id="4",
                strategy_name="PEEL Paragraph Structure",
                exam_type="essay",
                subject_applicability="humanities",
                strategy_type="question_approach",
                description="Use Point, Evidence, Explanation, Link structure for essay questions",
                step_by_step_guide=[
                    "Make a clear Point in your opening sentence",
                    "Provide Evidence to support your point",
                    "Explain how the evidence supports your point",
                    "Link back to the question or next point",
                    "Repeat for each paragraph"
                ],
                time_management_tips=[
                    "Plan your essay structure before writing",
                    "Allocate time per paragraph based on marks",
                    "Leave time for introduction and conclusion"
                ],
                common_mistakes=[
                    "Making points without evidence",
                    "Not explaining how evidence supports the point",
                    "Writing in a narrative style instead of analytical",
                    "Not linking paragraphs together"
                ],
                success_tips=[
                    "Use specific examples and evidence",
                    "Analyze rather than just describe",
                    "Link each paragraph to the question",
                    "Use topic sentences to introduce each point"
                ]
            ),
            cls(
                id="5",
                strategy_name="Elimination Method",
                exam_type="multiple_choice",
                subject_applicability="all",
                strategy_type="question_approach",
                description="Use process of elimination for multiple choice questions",
                step_by_step_guide=[
                    "Read the question carefully",
                    "Identify obviously wrong answers",
                    "Consider each remaining option",
                    "Use knowledge to eliminate incorrect choices",
                    "Make an educated guess if necessary"
                ],
                time_management_tips=[
                    "Don't spend too long on difficult multiple choice questions",
                    "Answer all questions - there's no penalty for wrong answers",
                    "Mark difficult questions to return to later"
                ],
                common_mistakes=[
                    "Not reading all options before choosing",
                    "Getting distracted by similar-sounding options",
                    "Changing correct answers unnecessarily",
                    "Leaving questions blank"
                ],
                success_tips=[
                    "Read questions and options carefully",
                    "Use elimination to narrow down choices",
                    "Trust your first instinct unless you have a good reason to change",
                    "Answer all questions even if unsure"
                ]
            )
        ]


class GCSEStudyPlanGenerator:
    
    
    @staticmethod
    def generate_study_plan(user_id: str, subject_id: str, exam_date: date,
                           study_hours_per_week: int, learning_style: str = "mixed",
                           weak_areas: List[str] = None) -> Dict:
        
        
        if weak_areas is None:
            weak_areas = []
        
        days_until_exam = (exam_date - date.today()).days
        
        
        if days_until_exam <= 7:
            phases = GCSEStudyPlanGenerator._generate_intensive_phase(days_until_exam, study_hours_per_week)
        elif days_until_exam <= 30:
            phases = GCSEStudyPlanGenerator._generate_focused_phase(days_until_exam, study_hours_per_week)
        else:
            phases = GCSEStudyPlanGenerator._generate_comprehensive_phase(days_until_exam, study_hours_per_week)
        
        
        recommended_techniques = GCSEStudyPlanGenerator._select_techniques_for_plan(
            learning_style, weak_areas, subject_id
        )
        
        
        weekly_schedule = GCSEStudyPlanGenerator._generate_weekly_schedule(
            study_hours_per_week, recommended_techniques
        )
        
        return {
            "phases": phases,
            "recommended_techniques": recommended_techniques,
            "weekly_schedule": weekly_schedule,
            "weak_area_focus": weak_areas,
            "learning_style": learning_style,
            "total_study_hours": (days_until_exam / 7) * study_hours_per_week
        }

    @staticmethod
    def _generate_intensive_phase(days: int, hours_per_week: int) -> List[Dict]:
        
        hours_per_day = (hours_per_week / 7) * 1.5  
        
        return [{
            "phase_name": "Intensive Revision",
            "duration_days": days,
            "focus": "Exam technique and quick review",
            "techniques": ["Past Paper Practice", "Active Recall", "Quick Review"],
            "study_hours_per_day": min(6, hours_per_day),
            "priority": "high"
        }]

    @staticmethod
    def _generate_focused_phase(days: int, hours_per_week: int) -> List[Dict]:
        
        intensive_days = 7
        focused_days = days - intensive_days
        
        return [
            {
                "phase_name": "Focused Revision",
                "duration_days": focused_days,
                "focus": "Topic review and practice",
                "techniques": ["Past Paper Practice", "Mind Mapping", "Active Recall"],
                "study_hours_per_day": hours_per_week / 7,
                "priority": "medium"
            },
            {
                "phase_name": "Intensive Revision",
                "duration_days": intensive_days,
                "focus": "Exam technique and final review",
                "techniques": ["Past Paper Practice", "Active Recall", "Quick Review"],
                "study_hours_per_day": min(4, (hours_per_week / 7) * 1.5),
                "priority": "high"
            }
        ]

    @staticmethod
    def _generate_comprehensive_phase(days: int, hours_per_week: int) -> List[Dict]:
        
        intensive_days = 7
        focused_days = 21
        comprehensive_days = days - intensive_days - focused_days
        
        return [
            {
                "phase_name": "Comprehensive Study",
                "duration_days": comprehensive_days,
                "focus": "Deep understanding and foundation",
                "techniques": ["Feynman Technique", "Mind Mapping", "Spaced Repetition"],
                "study_hours_per_day": hours_per_week / 7,
                "priority": "low"
            },
            {
                "phase_name": "Focused Revision",
                "duration_days": focused_days,
                "focus": "Topic consolidation and practice",
                "techniques": ["Past Paper Practice", "Mind Mapping", "Active Recall"],
                "study_hours_per_day": hours_per_week / 7,
                "priority": "medium"
            },
            {
                "phase_name": "Intensive Revision",
                "duration_days": intensive_days,
                "focus": "Exam technique and final review",
                "techniques": ["Past Paper Practice", "Active Recall", "Quick Review"],
                "study_hours_per_day": min(4, (hours_per_week / 7) * 1.5),
                "priority": "high"
            }
        ]

    @staticmethod
    def _select_techniques_for_plan(learning_style: str, weak_areas: List[str], subject_id: str) -> List[str]:
        
        
        
        base_techniques = ["Past Paper Practice", "Active Recall"]
        
        
        if learning_style == "visual":
            style_techniques = ["Mind Mapping", "Visual Notes"]
        elif learning_style == "auditory":
            style_techniques = ["Study Groups", "Recorded Notes"]
        elif learning_style == "kinesthetic":
            style_techniques = ["Hands-on Practice", "Movement-based Learning"]
        else:  
            style_techniques = ["Mind Mapping", "Spaced Repetition"]
        
        
        weak_area_techniques = []
        if "memorization" in weak_areas:
            weak_area_techniques.extend(["Spaced Repetition", "Flashcards"])
        if "understanding" in weak_areas:
            weak_area_techniques.extend(["Feynman Technique", "Concept Mapping"])
        if "application" in weak_areas:
            weak_area_techniques.extend(["Practice Problems", "Real-world Examples"])
        
        
        all_techniques = base_techniques + style_techniques + weak_area_techniques
        return list(set(all_techniques))

    @staticmethod
    def _generate_weekly_schedule(hours_per_week: int, techniques: List[str]) -> Dict:
        
        
        days_per_week = 5  
        hours_per_day = hours_per_week / days_per_week
        
        
        weekly_schedule = {}
        
        for day in range(days_per_week):
            day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][day]
            
            
            day_techniques = techniques[day % len(techniques):(day % len(techniques)) + 2]
            if len(day_techniques) < 2:
                day_techniques.extend(techniques[:2-len(day_techniques)])
            
            weekly_schedule[day_name] = {
                "study_hours": hours_per_day,
                "techniques": day_techniques,
                "focus": "Mixed revision and practice"
            }
        
        return weekly_schedule


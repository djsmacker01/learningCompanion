

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import json

class GCSELearningResource:
    
    
    def __init__(self, id=None, title=None, resource_type=None, subject_id=None, topic_area=None,
                 difficulty_level=None, format_type=None, description=None, content_url=None,
                 thumbnail_url=None, duration_minutes=None, file_size_mb=None, tags=None,
                 author=None, publisher=None, year_published=None, is_free=None, price=None,
                 rating=None, review_count=None, download_count=None, is_active=True,
                 created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.resource_type = resource_type  
        self.subject_id = subject_id
        self.topic_area = topic_area
        self.difficulty_level = difficulty_level  
        self.format_type = format_type  
        self.description = description
        self.content_url = content_url
        self.thumbnail_url = thumbnail_url
        self.duration_minutes = duration_minutes
        self.file_size_mb = file_size_mb
        self.tags = tags or []
        self.author = author
        self.publisher = publisher
        self.year_published = year_published
        self.is_free = is_free
        self.price = price
        self.rating = rating
        self.review_count = review_count
        self.download_count = download_count
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_resources_by_subject(cls, subject_id: str, resource_type: str = None, 
                                difficulty: str = None, free_only: bool = False) -> List['GCSELearningResource']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_resources()
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('gcse_learning_resources').select('*').eq('subject_id', subject_id).eq('is_active', True)
            
            if resource_type:
                query = query.eq('resource_type', resource_type)
            if difficulty:
                query = query.eq('difficulty_level', difficulty)
            if free_only:
                query = query.eq('is_free', True)
            
            result = query.order('rating', desc=True).order('download_count', desc=True).execute()
            return [cls(**resource) for resource in result.data]
        except Exception as e:
            print(f"Error getting learning resources: {e}")
            return cls._get_default_resources()

    @classmethod
    def get_resource_by_id(cls, resource_id: str) -> Optional['GCSELearningResource']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_resource_by_id(resource_id)
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('gcse_learning_resources').select('*').eq('id', resource_id).eq('is_active', True).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error getting learning resource: {e}")
            
        return cls._get_default_resource_by_id(resource_id)

    @classmethod
    def search_resources(cls, search_term: str, subject_id: str = None, 
                        resource_type: str = None) -> List['GCSELearningResource']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_resources()
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('gcse_learning_resources').select('*').eq('is_active', True)
            
            
            query = query.or_(f'title.ilike.%{search_term}%,description.ilike.%{search_term}%,tags.cs.{{"{search_term}"}}')
            
            if subject_id:
                query = query.eq('subject_id', subject_id)
            if resource_type:
                query = query.eq('resource_type', resource_type)
            
            result = query.order('rating', desc=True).execute()
            return [cls(**resource) for resource in result.data]
        except Exception as e:
            print(f"Error searching learning resources: {e}")
            return []

    @classmethod
    def _get_default_resources(cls) -> List['GCSELearningResource']:
        
        return [
            cls(
                id="1",
                title="GCSE Biology: Cell Structure and Function",
                resource_type="video",
                subject_id="biology_8461",
                topic_area="Cell Biology",
                difficulty_level="intermediate",
                format_type="mp4",
                description="Comprehensive video explaining cell structure, organelles, and their functions. Perfect for GCSE Biology revision.",
                content_url="https://example.com/biology/cell-structure.mp4",
                thumbnail_url="https://example.com/thumbnails/cell-structure.jpg",
                duration_minutes=15,
                tags=["cells", "organelles", "biology", "revision"],
                author="GCSE Biology Tutor",
                publisher="EduVideos",
                year_published=2023,
                is_free=True,
                rating=4.8,
                review_count=156,
                download_count=2340
            ),
            cls(
                id="2",
                title="GCSE Mathematics: Quadratic Equations",
                resource_type="interactive",
                subject_id="mathematics_8300",
                topic_area="Algebra",
                difficulty_level="intermediate",
                format_type="html",
                description="Interactive tutorial with step-by-step solutions for quadratic equations. Includes practice problems with instant feedback.",
                content_url="https://example.com/maths/quadratic-equations.html",
                thumbnail_url="https://example.com/thumbnails/quadratic.jpg",
                duration_minutes=25,
                tags=["algebra", "quadratic", "equations", "interactive"],
                author="Maths Master",
                publisher="Interactive Learning",
                year_published=2023,
                is_free=True,
                rating=4.6,
                review_count=89,
                download_count=1876
            ),
            cls(
                id="3",
                title="GCSE English Literature: Macbeth Analysis",
                resource_type="document",
                subject_id="english_literature_8702",
                topic_area="Shakespeare",
                difficulty_level="advanced",
                format_type="pdf",
                description="Detailed analysis of Macbeth including themes, characters, and key quotes. Perfect for essay preparation.",
                content_url="https://example.com/english/macbeth-analysis.pdf",
                thumbnail_url="https://example.com/thumbnails/macbeth.jpg",
                duration_minutes=45,
                file_size_mb=2.3,
                tags=["macbeth", "shakespeare", "literature", "analysis"],
                author="English Literature Expert",
                publisher="Literary Guides",
                year_published=2023,
                is_free=False,
                price=4.99,
                rating=4.9,
                review_count=203,
                download_count=892
            )
        ]

    @classmethod
    def _get_default_resource_by_id(cls, resource_id: str) -> Optional['GCSELearningResource']:
        
        resources = cls._get_default_resources()
        for resource in resources:
            if resource.id == resource_id:
                return resource
        return None


class GCSERevisionMaterial:
    
    
    def __init__(self, id=None, title=None, material_type=None, subject_id=None, topic_area=None,
                 exam_board=None, specification_code=None, difficulty_level=None, 
                 content_summary=None, key_points=None, revision_notes=None,
                 practice_questions=None, mark_scheme=None, tips_and_tricks=None,
                 estimated_study_time=None, is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.material_type = material_type  
        self.subject_id = subject_id
        self.topic_area = topic_area
        self.exam_board = exam_board
        self.specification_code = specification_code
        self.difficulty_level = difficulty_level
        self.content_summary = content_summary
        self.key_points = key_points or []
        self.revision_notes = revision_notes
        self.practice_questions = practice_questions or []
        self.mark_scheme = mark_scheme
        self.tips_and_tricks = tips_and_tricks or []
        self.estimated_study_time = estimated_study_time
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_materials_by_subject(cls, subject_id: str, material_type: str = None) -> List['GCSERevisionMaterial']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_materials()
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('gcse_revision_materials').select('*').eq('subject_id', subject_id).eq('is_active', True)
            
            if material_type:
                query = query.eq('material_type', material_type)
            
            result = query.order('title').execute()
            return [cls(**material) for material in result.data]
        except Exception as e:
            print(f"Error getting revision materials: {e}")
            return cls._get_default_materials()

    @classmethod
    def _get_default_materials(cls) -> List['GCSERevisionMaterial']:
        
        return [
            cls(
                id="1",
                title="Biology Cell Structure Revision Guide",
                material_type="revision_guide",
                subject_id="biology_8461",
                topic_area="Cell Biology",
                exam_board="AQA",
                specification_code="8461",
                difficulty_level="intermediate",
                content_summary="Complete revision guide covering all aspects of cell structure and function for GCSE Biology.",
                key_points=[
                    "Plant and animal cells have different organelles",
                    "Mitochondria are the powerhouse of the cell",
                    "Chloroplasts contain chlorophyll for photosynthesis",
                    "Cell membrane controls what enters and leaves the cell"
                ],
                tips_and_tricks=[
                    "Use diagrams to remember organelle locations",
                    "Compare plant vs animal cells in a table",
                    "Practice labeling cell diagrams",
                    "Remember functions with acronyms"
                ],
                estimated_study_time=60
            ),
            cls(
                id="2",
                title="Mathematics Algebra Summary Sheet",
                material_type="summary_sheet",
                subject_id="mathematics_8300",
                topic_area="Algebra",
                exam_board="AQA",
                specification_code="8300",
                difficulty_level="intermediate",
                content_summary="Essential formulas and methods for GCSE Algebra topics.",
                key_points=[
                    "Linear equations: y = mx + c",
                    "Quadratic formula: x = (-b ± √(b²-4ac)) / 2a",
                    "Factorising: find common factors",
                    "Simultaneous equations: substitution or elimination"
                ],
                tips_and_tricks=[
                    "Always check your answers by substituting back",
                    "Draw graphs to visualize linear equations",
                    "Practice with negative numbers",
                    "Use calculator efficiently for complex calculations"
                ],
                estimated_study_time=45
            )
        ]


class GCSEEducationalContent:
    
    
    def __init__(self, id=None, content_title=None, content_type=None, subject_id=None,
                 learning_objective=None, prerequisite_knowledge=None, content_body=None,
                 examples=None, exercises=None, assessment_criteria=None, 
                 estimated_completion_time=None, difficulty_progression=None,
                 related_topics=None, is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.content_title = content_title
        self.content_type = content_type  
        self.subject_id = subject_id
        self.learning_objective = learning_objective
        self.prerequisite_knowledge = prerequisite_knowledge
        self.content_body = content_body
        self.examples = examples or []
        self.exercises = exercises or []
        self.assessment_criteria = assessment_criteria
        self.estimated_completion_time = estimated_completion_time
        self.difficulty_progression = difficulty_progression  
        self.related_topics = related_topics or []
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_content_by_subject(cls, subject_id: str, content_type: str = None) -> List['GCSEEducationalContent']:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_content()
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('gcse_educational_content').select('*').eq('subject_id', subject_id).eq('is_active', True)
            
            if content_type:
                query = query.eq('content_type', content_type)
            
            result = query.order('content_title').execute()
            return [cls(**content) for content in result.data]
        except Exception as e:
            print(f"Error getting educational content: {e}")
            return cls._get_default_content()

    @classmethod
    def _get_default_content(cls) -> List['GCSEEducationalContent']:
        
        return [
            cls(
                id="1",
                content_title="Understanding Photosynthesis",
                content_type="lesson",
                subject_id="biology_8461",
                learning_objective="Students will understand the process of photosynthesis and its importance in ecosystems",
                prerequisite_knowledge="Basic understanding of plant cells and energy",
                content_body="Photosynthesis is the process by which plants convert light energy into chemical energy...",
                examples=[
                    "Green plants in sunlight produce oxygen",
                    "Leaves change color in autumn due to chlorophyll breakdown"
                ],
                exercises=[
                    "Label the parts of a leaf involved in photosynthesis",
                    "Explain why plants need sunlight",
                    "Calculate the rate of photosynthesis from given data"
                ],
                estimated_completion_time=30
            ),
            cls(
                id="2",
                content_title="Solving Linear Equations",
                content_type="tutorial",
                subject_id="mathematics_8300",
                learning_objective="Students will be able to solve linear equations with one unknown",
                prerequisite_knowledge="Basic arithmetic and algebraic manipulation",
                content_body="Linear equations are equations where the highest power of the variable is 1...",
                examples=[
                    "2x + 3 = 7 → x = 2",
                    "3y - 5 = 10 → y = 5"
                ],
                exercises=[
                    "Solve: 4x + 2 = 14",
                    "Solve: 2y - 3 = 7",
                    "Solve: 3z + 1 = 10"
                ],
                estimated_completion_time=25
            )
        ]


class GCSEResourceRecommendationEngine:
    
    
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_personalized_recommendations(self, subject_id: str = None, 
                                       learning_style: str = None,
                                       weak_areas: List[str] = None) -> Dict:
        
        
        if not subject_id:
            
            user_subjects = self._get_user_gcse_subjects()
            all_recommendations = {}
            
            for subject in user_subjects:
                recommendations = self._get_subject_recommendations(
                    subject.id, learning_style, weak_areas
                )
                all_recommendations[subject.name] = recommendations
            
            return {
                "recommendations_by_subject": all_recommendations,
                "overall_recommendations": self._get_overall_recommendations(learning_style)
            }
        
        return self._get_subject_recommendations(subject_id, learning_style, weak_areas)

    def _get_subject_recommendations(self, subject_id: str, learning_style: str, 
                                   weak_areas: List[str]) -> Dict:
        
        
        
        if learning_style == "visual":
            preferred_types = ["video", "interactive", "image"]
        elif learning_style == "auditory":
            preferred_types = ["audio", "video"]
        elif learning_style == "kinesthetic":
            preferred_types = ["interactive", "document"]
        else:
            preferred_types = ["video", "document", "interactive"]
        
        
        recommendations = {}
        for resource_type in preferred_types:
            resources = GCSELearningResource.get_resources_by_subject(
                subject_id, resource_type=resource_type, free_only=True
            )
            recommendations[resource_type] = resources[:3]  
        
        
        revision_materials = GCSERevisionMaterial.get_materials_by_subject(subject_id)
        recommendations["revision_materials"] = revision_materials[:3]
        
        
        educational_content = GCSEEducationalContent.get_content_by_subject(subject_id)
        recommendations["educational_content"] = educational_content[:3]
        
        return {
            "subject_id": subject_id,
            "recommendations": recommendations,
            "weak_area_focus": weak_areas or [],
            "learning_style": learning_style or "mixed"
        }

    def _get_overall_recommendations(self, learning_style: str) -> List[Dict]:
        
        
        general_recommendations = [
            {
                "title": "GCSE Study Techniques Guide",
                "type": "document",
                "description": "Comprehensive guide to effective GCSE study methods",
                "rating": 4.8,
                "is_free": True
            },
            {
                "title": "Exam Strategy Masterclass",
                "type": "video",
                "description": "Learn proven strategies for different exam question types",
                "rating": 4.7,
                "is_free": True
            },
            {
                "title": "Time Management for GCSE Students",
                "type": "interactive",
                "description": "Interactive tool to help plan your revision schedule",
                "rating": 4.6,
                "is_free": True
            }
        ]
        
        return general_recommendations

    def _get_user_gcse_subjects(self) -> List:
        
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('topics').select('gcse_subject_id').eq('user_id', self.user_id).eq('is_gcse', True).execute()
            subject_ids = [t['gcse_subject_id'] for t in result.data if t['gcse_subject_id']]
            
            
            subjects = []
            for subject_id in subject_ids:
                subjects.append(type('Subject', (), {'id': subject_id, 'name': f'Subject {subject_id}'})())
            
            return subjects
        except Exception as e:
            print(f"Error getting user GCSE subjects: {e}")
            return []


class GCSEResourceTracker:
    
    
    def __init__(self, user_id: str):
        self.user_id = user_id

    def track_resource_access(self, resource_id: str, resource_type: str, 
                            action: str, duration_seconds: int = None) -> bool:
        
        
        if not SUPABASE_AVAILABLE:
            return True
            
        supabase = get_supabase_client()
        
        try:
            tracking_data = {
                'user_id': self.user_id,
                'resource_id': resource_id,
                'resource_type': resource_type,
                'action': action,  
                'duration_seconds': duration_seconds,
                'accessed_at': datetime.utcnow().isoformat()
            }
            
            supabase.table('gcse_resource_tracking').insert(tracking_data).execute()
            return True
        except Exception as e:
            print(f"Error tracking resource access: {e}")
            return False

    def get_user_resource_history(self, days_back: int = 30) -> List[Dict]:
        
        
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        start_date = (datetime.now() - timedelta(days=days_back)).date().isoformat()
        
        try:
            result = supabase.table('gcse_resource_tracking').select('*').eq('user_id', self.user_id).gte('accessed_at', start_date).order('accessed_at', desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Error getting resource history: {e}")
            return []

    def get_recommended_resources(self, subject_id: str = None) -> List[Dict]:
        
        
        
        history = self.get_user_resource_history()
        
        
        recommendations = []
        
        
        accessed_types = set(item['resource_type'] for item in history)
        
        if 'video' in accessed_types:
            recommendations.append({
                "type": "video",
                "reason": "You frequently watch educational videos",
                "resources": GCSELearningResource.get_resources_by_subject(
                    subject_id, resource_type="video", free_only=True
                )[:2]
            })
        
        if 'document' in accessed_types:
            recommendations.append({
                "type": "document",
                "reason": "You often use study documents",
                "resources": GCSELearningResource.get_resources_by_subject(
                    subject_id, resource_type="document", free_only=True
                )[:2]
            })
        
        return recommendations


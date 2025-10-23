from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import json

class GCSEGradeBoundary:
    
    def __init__(self, id=None, exam_board=None, subject_code=None, exam_year=None,
                 exam_month=None, tier=None, grade=None, raw_mark=None,
                 percentage_mark=None, is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.exam_board = exam_board
        self.subject_code = subject_code
        self.exam_year = exam_year
        self.exam_month = exam_month
        self.tier = tier
        self.grade = grade
        self.raw_mark = raw_mark
        self.percentage_mark = percentage_mark
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_grade_boundaries(cls, exam_board: str, subject_code: str, 
                           exam_year: int = None, tier: str = None) -> Dict[str, Dict]:
        
        if not SUPABASE_AVAILABLE:
            return cls._get_default_boundaries(exam_board, subject_code)
            
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('gcse_grade_boundaries').select('*').eq('exam_board', exam_board).eq('subject_code', subject_code).eq('is_active', True)
            
            if exam_year:
                query = query.eq('exam_year', exam_year)
            if tier:
                query = query.eq('tier', tier)
            
            result = query.order('exam_year', desc=True).order('raw_mark', desc=True).execute()
            
            
            boundaries = {}
            for boundary_data in result.data:
                boundary = cls(**boundary_data)
                tier_key = boundary.tier or 'single'
                
                if tier_key not in boundaries:
                    boundaries[tier_key] = {}
                
                boundaries[tier_key][boundary.grade] = {
                    'raw_mark': boundary.raw_mark,
                    'percentage_mark': boundary.percentage_mark,
                    'exam_year': boundary.exam_year,
                    'exam_month': boundary.exam_month
                }
            
            return boundaries
        except Exception as e:
            print(f"Error getting grade boundaries: {e}")
            return cls._get_default_boundaries(exam_board, subject_code)

    @classmethod
    def _get_default_boundaries(cls, exam_board: str, subject_code: str) -> Dict[str, Dict]:
        
        
        if exam_board == "AQA" and subject_code == "8300":
            return {
                "Foundation": {
                    "5": {"raw_mark": 77, "percentage_mark": 77.0},
                    "4": {"raw_mark": 65, "percentage_mark": 65.0},
                    "3": {"raw_mark": 53, "percentage_mark": 53.0}
                },
                "Higher": {
                    "9": {"raw_mark": 214, "percentage_mark": 89.2},
                    "8": {"raw_mark": 186, "percentage_mark": 77.5},
                    "7": {"raw_mark": 158, "percentage_mark": 65.8},
                    "6": {"raw_mark": 130, "percentage_mark": 54.2},
                    "5": {"raw_mark": 102, "percentage_mark": 42.5},
                    "4": {"raw_mark": 74, "percentage_mark": 30.8}
                }
            }
        
        elif exam_board == "AQA" and subject_code == "8461":
            return {
                "Foundation": {
                    "5": {"raw_mark": 69, "percentage_mark": 69.0},
                    "4": {"raw_mark": 58, "percentage_mark": 58.0},
                    "3": {"raw_mark": 47, "percentage_mark": 47.0}
                },
                "Higher": {
                    "9": {"raw_mark": 131, "percentage_mark": 87.3},
                    "8": {"raw_mark": 119, "percentage_mark": 79.3},
                    "7": {"raw_mark": 107, "percentage_mark": 71.3},
                    "6": {"raw_mark": 95, "percentage_mark": 63.3},
                    "5": {"raw_mark": 83, "percentage_mark": 55.3},
                    "4": {"raw_mark": 71, "percentage_mark": 47.3}
                }
            }
        return {}


class GCSEGradeCalculator:
    
    
    @staticmethod
    def calculate_grade(achieved_marks: int, total_marks: int, exam_board: str, 
                       subject_code: str, tier: str = None, exam_year: int = None) -> Dict:
        
        
        
        percentage = (achieved_marks / total_marks * 100) if total_marks > 0 else 0
        
        
        boundaries = GCSEGradeBoundary.get_grade_boundaries(exam_board, subject_code, exam_year, tier)
        
        print(f"DEBUG: Grade calculation - Board: {exam_board}, Code: {subject_code}, Tier: {tier}")
        print(f"DEBUG: Boundaries found: {list(boundaries.keys()) if boundaries else 'None'}")
        
        
        if not tier:
            if "Foundation" in boundaries and "Higher" in boundaries:
                
                tier = "Foundation" if percentage < 50 else "Higher"
            elif "Foundation" in boundaries:
                tier = "Foundation"
            elif "Higher" in boundaries:
                tier = "Higher"
            else:
                tier = "single"
        
        
        tier_boundaries = boundaries.get(tier, {})
        
        print(f"DEBUG: Selected tier: {tier}")
        print(f"DEBUG: Tier boundaries: {tier_boundaries}")
        
        
        grade = "U"
        grade_info = {
            "grade": "U", 
            "description": "Ungraded", 
            "percentage": percentage,
            "raw_mark": achieved_marks,
            "total_mark": total_marks,
            "tier": tier if tier else "Not specified",
            "exam_board": exam_board,
            "subject_code": subject_code
        }
        
        if tier_boundaries:
            
            sorted_grades = sorted(tier_boundaries.items(), 
                                 key=lambda x: x[1]["raw_mark"], reverse=True)
            
            for grade_num, boundary_info in sorted_grades:
                if achieved_marks >= boundary_info["raw_mark"]:
                    grade = grade_num
                    grade_info = {
                        "grade": grade_num,
                        "description": GCSEGradeCalculator._get_grade_description(grade_num),
                        "percentage": percentage,
                        "raw_mark": achieved_marks,
                        "total_mark": total_marks,
                        "boundary_mark": boundary_info["raw_mark"],
                        "tier": tier,
                        "exam_board": exam_board,
                        "subject_code": subject_code
                    }
                    break
        
        return grade_info

    @staticmethod
    def predict_grade(current_performance: List[Dict], target_grade: str, 
                     exam_board: str, subject_code: str, tier: str = None) -> Dict:
        
        
        if not current_performance:
            return {
                "prediction": "insufficient_data",
                "message": "Not enough performance data to make a prediction",
                "confidence": 0
            }
        
        
        total_marks = sum(p["total_marks"] for p in current_performance)
        achieved_marks = sum(p["achieved_marks"] for p in current_performance)
        average_percentage = (achieved_marks / total_marks * 100) if total_marks > 0 else 0
        
        
        boundaries = GCSEGradeBoundary.get_grade_boundaries(exam_board, subject_code, tier=tier)
        
        
        if not tier:
            if "Foundation" in boundaries and "Higher" in boundaries:
                tier = "Foundation" if average_percentage < 50 else "Higher"
            elif "Foundation" in boundaries:
                tier = "Foundation"
            elif "Higher" in boundaries:
                tier = "Higher"
            else:
                tier = "single"
        
        tier_boundaries = boundaries.get(tier, {})
        
        if target_grade not in tier_boundaries:
            return {
                "prediction": "invalid_target",
                "message": f"Target grade {target_grade} not available for {tier} tier",
                "confidence": 0
            }
        
        
        target_boundary = tier_boundaries[target_grade]
        target_percentage = target_boundary["percentage_mark"]
        
        
        improvement_needed = target_percentage - average_percentage
        
        
        recent_performance = current_performance[-5:] if len(current_performance) >= 5 else current_performance
        if len(recent_performance) >= 2:
            recent_avg = sum(p["achieved_marks"] / p["total_marks"] * 100 for p in recent_performance) / len(recent_performance)
            earlier_performance = current_performance[:-5] if len(current_performance) > 5 else []
            
            if earlier_performance:
                earlier_avg = sum(p["achieved_marks"] / p["total_marks"] * 100 for p in earlier_performance) / len(earlier_performance)
                trend = "improving" if recent_avg > earlier_avg else "declining" if recent_avg < earlier_avg else "stable"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        
        if improvement_needed <= 5:
            prediction = "likely"
            confidence = 85
            message = f"You're very close to achieving grade {target_grade}. Keep up the good work!"
        elif improvement_needed <= 15:
            if trend == "improving":
                prediction = "possible"
                confidence = 70
                message = f"With continued improvement, grade {target_grade} is achievable. You're on the right track!"
            else:
                prediction = "challenging"
                confidence = 45
                message = f"Grade {target_grade} will require significant improvement. Consider targeted revision."
        elif improvement_needed <= 25:
            if trend == "improving":
                prediction = "challenging"
                confidence = 40
                message = f"Grade {target_grade} is challenging but possible with dedicated effort and improvement."
            else:
                prediction = "unlikely"
                confidence = 20
                message = f"Grade {target_grade} will require substantial improvement. Focus on foundation topics first."
        else:
            prediction = "unlikely"
            confidence = 10
            message = f"Grade {target_grade} is very challenging. Consider setting a more achievable target first."
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "message": message,
            "current_percentage": round(average_percentage, 1),
            "target_percentage": target_percentage,
            "improvement_needed": round(improvement_needed, 1),
            "trend": trend,
            "target_grade": target_grade,
            "tier": tier
        }

    @staticmethod
    def get_grade_requirements(target_grade: str, exam_board: str, subject_code: str,
                              tier: str = None) -> Dict:
        
        
        boundaries = GCSEGradeBoundary.get_grade_boundaries(exam_board, subject_code, tier=tier)
        
        
        if not tier:
            if "Foundation" in boundaries and "Higher" in boundaries:
                tier = "Higher"  
            elif "Foundation" in boundaries:
                tier = "Foundation"
            elif "Higher" in boundaries:
                tier = "Higher"
            else:
                tier = "single"
        
        tier_boundaries = boundaries.get(tier, {})
        
        if target_grade not in tier_boundaries:
            return {
                "error": f"Grade {target_grade} not available for {tier} tier",
                "available_grades": list(tier_boundaries.keys())
            }
        
        target_boundary = tier_boundaries[target_grade]
        
        
        available_grades = list(tier_boundaries.keys())
        available_grades.sort(key=lambda x: int(x) if x.isdigit() else 0, reverse=True)
        
        
        current_index = available_grades.index(target_grade)
        next_grade_up = available_grades[current_index - 1] if current_index > 0 else None
        next_grade_down = available_grades[current_index + 1] if current_index < len(available_grades) - 1 else None
        
        return {
            "target_grade": target_grade,
            "grade_description": GCSEGradeCalculator._get_grade_description(target_grade),
            "required_percentage": target_boundary["percentage_mark"],
            "tier": tier,
            "exam_board": exam_board,
            "subject_code": subject_code,
            "available_grades": available_grades,
            "next_grade_up": next_grade_up,
            "next_grade_down": next_grade_down,
            "grade_boundary": target_boundary
        }

    @staticmethod
    def _get_grade_description(grade: str) -> str:
        
        grade_descriptions = {
            "9": "Exceptional (A* equivalent)",
            "8": "Excellent (A* equivalent)",
            "7": "Very Good (A equivalent)",
            "6": "Good (B equivalent)",
            "5": "Strong Pass (B/C equivalent)",
            "4": "Standard Pass (C equivalent)",
            "3": "Below Standard Pass (D equivalent)",
            "2": "Poor (E equivalent)",
            "1": "Very Poor (F equivalent)",
            "U": "Ungraded"
        }
        return grade_descriptions.get(grade, "Unknown")


class GCSEGradeTracker:
    
    
    @staticmethod
    def track_grade_progression(user_id: str, subject_id: str, exam_board: str, 
                               subject_code: str) -> Dict:
        
        
        if not SUPABASE_AVAILABLE:
            return {"error": "Database not available"}
        
        supabase = get_supabase_client()
        
        try:
            
            performance_result = supabase.table('gcse_performance').select('*').eq('user_id', user_id).eq('subject_id', subject_id).order('completed_at', desc=True).execute()
            
            if not performance_result.data:
                return {
                    "error": "No performance data found",
                    "recommendation": "Start practicing with quizzes and past papers to build a performance history"
                }
            
            performance_data = performance_result.data
            
            
            grades = []
            percentages = []
            dates = []
            
            for record in performance_data:
                if record['grade'] and record['grade'] != 'U':
                    grades.append(int(record['grade']) if record['grade'].isdigit() else 0)
                    percentages.append(record['score'])
                    dates.append(record['completed_at'])
            
            if not grades:
                return {
                    "error": "No valid grades found",
                    "recommendation": "Complete more assessments to track your progress"
                }
            
            
            recent_grades = grades[:5] if len(grades) >= 5 else grades
            older_grades = grades[5:] if len(grades) > 5 else []
            
            if older_grades:
                recent_avg = sum(recent_grades) / len(recent_grades)
                older_avg = sum(older_grades) / len(older_grades)
                trend = "improving" if recent_avg > older_avg else "declining" if recent_avg < older_avg else "stable"
            else:
                trend = "insufficient_data"
            
            
            avg_grade = sum(grades) / len(grades)
            avg_percentage = sum(percentages) / len(percentages)
            
            
            boundaries = GCSEGradeBoundary.get_grade_boundaries(exam_board, subject_code)
            
            
            tier = "Higher" if avg_percentage >= 50 else "Foundation"
            tier_boundaries = boundaries.get(tier, {})
            
            
            current_grade = "U"
            for grade_num, boundary_info in tier_boundaries.items():
                if avg_percentage >= boundary_info["percentage_mark"]:
                    current_grade = grade_num
                    break
            
            
            recommendations = []
            if trend == "declining":
                recommendations.append("Focus on areas where you're struggling and seek additional help")
            elif trend == "improving":
                recommendations.append("Great progress! Continue with your current study methods")
            else:
                recommendations.append("Try different study techniques to improve your performance")
            
            if avg_percentage < 40:
                recommendations.append("Focus on foundation topics and basic concepts first")
            elif avg_percentage < 70:
                recommendations.append("Practice more past papers and exam-style questions")
            else:
                recommendations.append("Aim for higher grades by tackling more challenging questions")
            
            return {
                "current_grade": current_grade,
                "current_percentage": round(avg_percentage, 1),
                "average_grade": round(avg_grade, 1),
                "trend": trend,
                "total_assessments": len(grades),
                "recent_performance": recent_grades[:3],
                "recommendations": recommendations,
                "grade_history": list(zip(dates[:10], grades[:10], percentages[:10])),  
                "tier": tier
            }
            
        except Exception as e:
            print(f"Error tracking grade progression: {e}")
            return {"error": "Failed to track grade progression"}

    @staticmethod
    def get_grade_target_recommendations(user_id: str, subject_id: str, 
                                        exam_board: str, subject_code: str) -> List[Dict]:
        
        
        progression = GCSEGradeTracker.track_grade_progression(user_id, subject_id, exam_board, subject_code)
        
        if "error" in progression:
            return [{
                "target_grade": "4",
                "description": "Start with a standard pass target",
                "confidence": "low",
                "reasoning": "Build a performance history first"
            }]
        
        current_percentage = progression["current_percentage"]
        trend = progression["trend"]
        
        recommendations = []
        
        
        if current_percentage >= 70:
            recommendations.append({
                "target_grade": "7",
                "description": "Very Good (A equivalent)",
                "confidence": "high",
                "reasoning": f"Current performance ({current_percentage}%) suggests this is achievable"
            })
        elif current_percentage >= 60:
            recommendations.append({
                "target_grade": "6",
                "description": "Good (B equivalent)",
                "confidence": "high",
                "reasoning": f"Current performance ({current_percentage}%) suggests this is achievable"
            })
        elif current_percentage >= 50:
            recommendations.append({
                "target_grade": "5",
                "description": "Strong Pass (B/C equivalent)",
                "confidence": "high",
                "reasoning": f"Current performance ({current_percentage}%) suggests this is achievable"
            })
        else:
            recommendations.append({
                "target_grade": "4",
                "description": "Standard Pass (C equivalent)",
                "confidence": "medium",
                "reasoning": f"Focus on reaching standard pass level first"
            })
        
        
        if current_percentage >= 60 and trend == "improving":
            recommendations.append({
                "target_grade": "8",
                "description": "Excellent (A* equivalent)",
                "confidence": "medium",
                "reasoning": "Improving trend suggests this could be achievable with continued effort"
            })
        elif current_percentage >= 50:
            recommendations.append({
                "target_grade": "7",
                "description": "Very Good (A equivalent)",
                "confidence": "medium",
                "reasoning": "Could be achievable with targeted improvement"
            })
        elif current_percentage >= 40:
            recommendations.append({
                "target_grade": "6",
                "description": "Good (B equivalent)",
                "confidence": "medium",
                "reasoning": "Would require significant improvement but is possible"
            })
        
        
        if current_percentage >= 70:
            recommendations.append({
                "target_grade": "9",
                "description": "Exceptional (A* equivalent)",
                "confidence": "low",
                "reasoning": "Very challenging but worth aiming for if you're consistently high-performing"
            })
        
        return recommendations


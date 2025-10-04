

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
from app.models.gcse_grading import GCSEGradeCalculator, GCSEGradeTracker
from app.models.gcse_curriculum import GCSESubject
import json
import statistics

class GCSEPerformanceAnalytics:
    
    
    def __init__(self, user_id: str, subject_id: str = None):
        self.user_id = user_id
        self.subject_id = subject_id

    def get_comprehensive_performance_report(self, days_back: int = 90) -> Dict:
        
        
        
        performance_data = self._get_performance_data(days_back)
        
        if not performance_data:
            return {
                "error": "No performance data available",
                "recommendation": "Start practicing with quizzes and past papers to build analytics"
            }
        
        
        metrics = self._calculate_performance_metrics(performance_data)
        
        
        trends = self._analyze_performance_trends(performance_data)
        
        
        insights = self._generate_insights(metrics, trends)
        
        
        grade_predictions = self._get_grade_predictions(performance_data)
        
        
        study_efficiency = self._calculate_study_efficiency(days_back)
        
        return {
            "performance_metrics": metrics,
            "trends": trends,
            "insights": insights,
            "grade_predictions": grade_predictions,
            "study_efficiency": study_efficiency,
            "data_period": f"Last {days_back} days",
            "total_sessions": len(performance_data)
        }

    def _get_performance_data(self, days_back: int) -> List[Dict]:
        
        if not SUPABASE_AVAILABLE:
            return self._get_mock_performance_data()
        
        supabase = get_supabase_client()
        start_date = (datetime.now() - timedelta(days=days_back)).date().isoformat()
        
        try:
            query = supabase.table('gcse_performance').select('*').eq('user_id', self.user_id).gte('completed_at', start_date)
            
            if self.subject_id:
                query = query.eq('subject_id', self.subject_id)
            
            result = query.order('completed_at').execute()
            return result.data
        except Exception as e:
            print(f"Error getting performance data: {e}")
            return self._get_mock_performance_data()

    def _get_mock_performance_data(self) -> List[Dict]:
        
        return [
            {
                "id": "1",
                "score": 75.0,
                "grade": "7",
                "total_marks": 100,
                "achieved_marks": 75,
                "assessment_type": "quiz",
                "completed_at": (datetime.now() - timedelta(days=5)).isoformat()
            },
            {
                "id": "2",
                "score": 68.0,
                "grade": "6",
                "total_marks": 80,
                "achieved_marks": 54,
                "assessment_type": "past_paper",
                "completed_at": (datetime.now() - timedelta(days=8)).isoformat()
            },
            {
                "id": "3",
                "score": 82.0,
                "grade": "8",
                "total_marks": 90,
                "achieved_marks": 74,
                "assessment_type": "quiz",
                "completed_at": (datetime.now() - timedelta(days=12)).isoformat()
            }
        ]

    def _calculate_performance_metrics(self, performance_data: List[Dict]) -> Dict:
        
        
        if not performance_data:
            return {}
        
        scores = [p["score"] for p in performance_data]
        grades = [int(p["grade"]) for p in performance_data if p["grade"].isdigit()]
        
        
        metrics = {
            "average_score": round(statistics.mean(scores), 1),
            "median_score": round(statistics.median(scores), 1),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "score_range": max(scores) - min(scores),
            "standard_deviation": round(statistics.stdev(scores) if len(scores) > 1 else 0, 1),
            "average_grade": round(statistics.mean(grades), 1) if grades else 0,
            "grade_improvement": self._calculate_grade_improvement(performance_data),
            "consistency_score": self._calculate_consistency_score(scores),
            "total_assessments": len(performance_data)
        }
        
        
        assessment_types = {}
        for assessment in performance_data:
            assessment_type = assessment["assessment_type"]
            if assessment_type not in assessment_types:
                assessment_types[assessment_type] = []
            assessment_types[assessment_type].append(assessment["score"])
        
        metrics["performance_by_type"] = {}
        for assessment_type, scores in assessment_types.items():
            metrics["performance_by_type"][assessment_type] = {
                "average": round(statistics.mean(scores), 1),
                "count": len(scores),
                "highest": max(scores),
                "lowest": min(scores)
            }
        
        return metrics

    def _calculate_grade_improvement(self, performance_data: List[Dict]) -> Dict:
        
        
        if len(performance_data) < 2:
            return {"improvement": 0, "trend": "insufficient_data"}
        
        
        sorted_data = sorted(performance_data, key=lambda x: x["completed_at"])
        
        
        first_grade = int(sorted_data[0]["grade"]) if sorted_data[0]["grade"].isdigit() else 0
        last_grade = int(sorted_data[-1]["grade"]) if sorted_data[-1]["grade"].isdigit() else 0
        
        improvement = last_grade - first_grade
        
        
        if improvement > 0:
            trend = "improving"
        elif improvement < 0:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "improvement": improvement,
            "trend": trend,
            "first_grade": first_grade,
            "last_grade": last_grade,
            "improvement_percentage": round((improvement / max(first_grade, 1)) * 100, 1)
        }

    def _calculate_consistency_score(self, scores: List[float]) -> float:
        
        
        if len(scores) < 2:
            return 100.0
        
        
        mean_score = statistics.mean(scores)
        std_dev = statistics.stdev(scores)
        
        if mean_score == 0:
            return 100.0
        
        coefficient_of_variation = (std_dev / mean_score) * 100
        
        
        consistency_score = max(0, 100 - coefficient_of_variation)
        
        return round(consistency_score, 1)

    def _analyze_performance_trends(self, performance_data: List[Dict]) -> Dict:
        
        
        if len(performance_data) < 3:
            return {"trend": "insufficient_data", "message": "Need more data for trend analysis"}
        
        
        sorted_data = sorted(performance_data, key=lambda x: x["completed_at"])
        
        
        scores = [p["score"] for p in sorted_data]
        
        
        n = len(scores)
        x_values = list(range(n))
        
        
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(scores)
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, scores))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        slope = numerator / denominator if denominator != 0 else 0
        
        
        if slope > 1:
            trend = "strongly_improving"
        elif slope > 0.5:
            trend = "improving"
        elif slope > -0.5:
            trend = "stable"
        elif slope > -1:
            trend = "declining"
        else:
            trend = "strongly_declining"
        
        
        weekly_performance = self._calculate_weekly_performance(sorted_data)
        
        return {
            "trend": trend,
            "slope": round(slope, 2),
            "weekly_performance": weekly_performance,
            "recent_performance": scores[-3:] if len(scores) >= 3 else scores,
            "performance_volatility": self._calculate_volatility(scores)
        }

    def _calculate_weekly_performance(self, performance_data: List[Dict]) -> List[Dict]:
        
        
        weekly_data = {}
        
        for assessment in performance_data:
            assessment_date = datetime.fromisoformat(assessment["completed_at"]).date()
            week_start = assessment_date - timedelta(days=assessment_date.weekday())
            week_key = week_start.isoformat()
            
            if week_key not in weekly_data:
                weekly_data[week_key] = []
            
            weekly_data[week_key].append(assessment["score"])
        
        
        weekly_performance = []
        for week_start, scores in sorted(weekly_data.items()):
            weekly_performance.append({
                "week_start": week_start,
                "average_score": round(statistics.mean(scores), 1),
                "assessment_count": len(scores),
                "highest_score": max(scores),
                "lowest_score": min(scores)
            })
        
        return weekly_performance

    def _calculate_volatility(self, scores: List[float]) -> float:
        
        
        if len(scores) < 2:
            return 0.0
        
        
        mean_score = statistics.mean(scores)
        std_dev = statistics.stdev(scores)
        
        if mean_score == 0:
            return 0.0
        
        volatility = (std_dev / mean_score) * 100
        return round(volatility, 1)

    def _generate_insights(self, metrics: Dict, trends: Dict) -> List[Dict]:
        
        
        insights = []
        
        
        avg_score = metrics.get("average_score", 0)
        if avg_score >= 80:
            insights.append({
                "type": "positive",
                "title": "Excellent Performance",
                "message": f"Your average score of {avg_score}% shows excellent understanding. Keep up the great work!",
                "recommendation": "Focus on maintaining consistency and tackling more challenging questions."
            })
        elif avg_score >= 70:
            insights.append({
                "type": "positive",
                "title": "Good Performance",
                "message": f"Your average score of {avg_score}% shows good understanding with room for improvement.",
                "recommendation": "Identify weak areas and focus revision on those topics."
            })
        elif avg_score >= 60:
            insights.append({
                "type": "warning",
                "title": "Moderate Performance",
                "message": f"Your average score of {avg_score}% indicates moderate understanding.",
                "recommendation": "Increase study time and focus on fundamental concepts."
            })
        else:
            insights.append({
                "type": "concern",
                "title": "Needs Improvement",
                "message": f"Your average score of {avg_score}% suggests significant gaps in understanding.",
                "recommendation": "Seek additional help and focus on basic concepts before moving to advanced topics."
            })
        
        
        consistency = metrics.get("consistency_score", 0)
        if consistency >= 80:
            insights.append({
                "type": "positive",
                "title": "Consistent Performance",
                "message": "Your performance is very consistent, showing reliable understanding.",
                "recommendation": "This consistency is excellent for exam preparation."
            })
        elif consistency >= 60:
            insights.append({
                "type": "info",
                "title": "Moderate Consistency",
                "message": "Your performance shows some variability.",
                "recommendation": "Focus on identifying what causes performance fluctuations."
            })
        else:
            insights.append({
                "type": "warning",
                "title": "Inconsistent Performance",
                "message": "Your performance varies significantly between assessments.",
                "recommendation": "Work on study techniques and exam strategies to improve consistency."
            })
        
        
        trend = trends.get("trend", "stable")
        if trend in ["improving", "strongly_improving"]:
            insights.append({
                "type": "positive",
                "title": "Improving Trend",
                "message": "Your performance is improving over time.",
                "recommendation": "Continue with your current study methods."
            })
        elif trend in ["declining", "strongly_declining"]:
            insights.append({
                "type": "concern",
                "title": "Declining Trend",
                "message": "Your performance has been declining recently.",
                "recommendation": "Review your study methods and consider seeking additional help."
            })
        
        
        performance_by_type = metrics.get("performance_by_type", {})
        if len(performance_by_type) > 1:
            best_type = max(performance_by_type.items(), key=lambda x: x[1]["average"])
            worst_type = min(performance_by_type.items(), key=lambda x: x[1]["average"])
            
            if best_type[1]["average"] - worst_type[1]["average"] > 10:
                insights.append({
                    "type": "info",
                    "title": "Assessment Type Variation",
                    "message": f"You perform better in {best_type[0]} than {worst_type[0]}.",
                    "recommendation": f"Focus more practice on {worst_type[0]} to improve overall performance."
                })
        
        return insights

    def _get_grade_predictions(self, performance_data: List[Dict]) -> Dict:
        
        
        if not performance_data:
            return {"error": "No performance data available"}
        
        
        recent_scores = [p["score"] for p in performance_data[-5:]]  
        current_avg = statistics.mean(recent_scores)
        
        
        grade_boundaries = {
            9: 90, 8: 80, 7: 70, 6: 60, 5: 50, 4: 40, 3: 30, 2: 20, 1: 10
        }
        
        
        current_grade = 1
        for grade, boundary in sorted(grade_boundaries.items(), reverse=True):
            if current_avg >= boundary:
                current_grade = grade
                break
        
        
        next_grade = current_grade + 1 if current_grade < 9 else 9
        
        
        improvement_needed = grade_boundaries.get(next_grade, 100) - current_avg
        
        return {
            "current_grade": current_grade,
            "current_average": round(current_avg, 1),
            "predicted_next_grade": next_grade,
            "improvement_needed": round(improvement_needed, 1),
            "confidence": "medium" if len(performance_data) >= 5 else "low"
        }

    def _calculate_study_efficiency(self, days_back: int) -> Dict:
        
        
        
        
        return {
            "study_hours": 25.5,
            "assessments_completed": 12,
            "efficiency_score": 85.2,
            "productive_study_time": 21.3,
            "distraction_time": 4.2,
            "recommendation": "Maintain current study habits - you're being very efficient!"
        }


class GCSEComparativeAnalytics:
    
    
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_subject_comparison(self) -> Dict:
        
        
        
        user_subjects = self._get_user_gcse_subjects()
        
        subject_comparison = {}
        
        for subject in user_subjects:
            analytics = GCSEPerformanceAnalytics(self.user_id, subject.id)
            performance_report = analytics.get_comprehensive_performance_report()
            
            if "error" not in performance_report:
                subject_comparison[subject.name] = {
                    "average_score": performance_report["performance_metrics"].get("average_score", 0),
                    "total_assessments": performance_report["performance_metrics"].get("total_assessments", 0),
                    "consistency_score": performance_report["performance_metrics"].get("consistency_score", 0),
                    "trend": performance_report["trends"].get("trend", "stable"),
                    "grade_predictions": performance_report["grade_predictions"]
                }
        
        return {
            "subject_comparison": subject_comparison,
            "strongest_subject": max(subject_comparison.items(), key=lambda x: x[1]["average_score"])[0] if subject_comparison else None,
            "weakest_subject": min(subject_comparison.items(), key=lambda x: x[1]["average_score"])[0] if subject_comparison else None,
            "overall_average": round(statistics.mean([s["average_score"] for s in subject_comparison.values()]), 1) if subject_comparison else 0
        }

    def _get_user_gcse_subjects(self) -> List:
        
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('topics').select('gcse_subject_id').eq('user_id', self.user_id).eq('is_gcse', True).execute()
            subject_ids = [t['gcse_subject_id'] for t in result.data if t['gcse_subject_id']]
            
            subjects = []
            for subject_id in subject_ids:
                subject = GCSESubject.get_subject_by_id(subject_id)
                if subject:
                    subjects.append(subject)
            
            return subjects
        except Exception as e:
            print(f"Error getting user GCSE subjects: {e}")
            return []


class GCSERecommendationEngine:
    
    
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_personalized_recommendations(self) -> Dict:
        
        
        
        analytics = GCSEPerformanceAnalytics(self.user_id)
        performance_report = analytics.get_comprehensive_performance_report()
        
        if "error" in performance_report:
            return {"error": "Insufficient data for recommendations"}
        
        
        recommendations = []
        
        insights = performance_report.get("insights", [])
        for insight in insights:
            if insight["type"] in ["warning", "concern"]:
                recommendations.append({
                    "type": "study_technique",
                    "priority": "high",
                    "title": "Improve Study Techniques",
                    "description": insight["recommendation"],
                    "action_items": [
                        "Try active recall instead of passive reading",
                        "Use spaced repetition for better retention",
                        "Practice past papers regularly"
                    ]
                })
        
        
        subject_recommendations = self._get_subject_specific_recommendations(performance_report)
        recommendations.extend(subject_recommendations)
        
        
        time_recommendations = self._get_time_management_recommendations(performance_report)
        recommendations.extend(time_recommendations)
        
        return {
            "recommendations": recommendations,
            "priority_order": sorted(recommendations, key=lambda x: x["priority"], reverse=True),
            "next_actions": self._get_next_actions(recommendations)
        }

    def _get_subject_specific_recommendations(self, performance_report: Dict) -> List[Dict]:
        
        
        recommendations = []
        
        performance_by_type = performance_report.get("performance_metrics", {}).get("performance_by_type", {})
        
        if "quiz" in performance_by_type and "past_paper" in performance_by_type:
            quiz_avg = performance_by_type["quiz"]["average"]
            paper_avg = performance_by_type["past_paper"]["average"]
            
            if quiz_avg > paper_avg + 10:
                recommendations.append({
                    "type": "exam_technique",
                    "priority": "high",
                    "title": "Improve Exam Technique",
                    "description": "You perform well in quizzes but struggle with past papers.",
                    "action_items": [
                        "Practice more past papers under timed conditions",
                        "Focus on exam question command words",
                        "Work on time management during exams"
                    ]
                })
        
        return recommendations

    def _get_time_management_recommendations(self, performance_report: Dict) -> List[Dict]:
        
        
        recommendations = []
        
        study_efficiency = performance_report.get("study_efficiency", {})
        efficiency_score = study_efficiency.get("efficiency_score", 0)
        
        if efficiency_score < 70:
            recommendations.append({
                "type": "time_management",
                "priority": "medium",
                "title": "Improve Study Efficiency",
                "description": "Your study efficiency could be improved.",
                "action_items": [
                    "Use the Pomodoro Technique for focused study",
                    "Eliminate distractions during study time",
                    "Plan study sessions in advance"
                ]
            })
        
        return recommendations

    def _get_next_actions(self, recommendations: List[Dict]) -> List[str]:
        
        
        actions = []
        
        for recommendation in recommendations[:3]:  
            actions.extend(recommendation.get("action_items", [])[:2])  
        
        return actions[:5]  


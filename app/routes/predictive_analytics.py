"""
Predictive Analytics API Routes
Advanced analytics and prediction endpoints
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.routes.topics import get_current_user
from app.utils.predictive_analytics import PredictiveAnalytics
from datetime import datetime
import json

predictive_analytics = Blueprint('predictive_analytics', __name__, url_prefix='/analytics')

@predictive_analytics.route('/')
@login_required
def analytics_dashboard():
    """Predictive Analytics Dashboard"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        # Get performance trends across all topics
        performance_trends = analytics.analyze_performance_trends(days_back=90)
        
        return render_template('analytics/predictive_dashboard.html', 
                             performance_trends=performance_trends,
                             user=user)
    
    except Exception as e:
        print(f"Error loading analytics dashboard: {e}")
        return jsonify({'error': 'Failed to load dashboard'}), 500

@predictive_analytics.route('/grade-prediction/<topic_id>')
@login_required
def predict_grade(topic_id):
    """Predict exam grade for a specific topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        # Get optional parameters
        exam_date = request.args.get('exam_date')
        target_grade = request.args.get('target_grade')
        
        prediction = analytics.predict_exam_grade(topic_id, exam_date, target_grade)
        
        return jsonify(prediction)
    
    except Exception as e:
        print(f"Error predicting grade: {e}")
        return jsonify({'error': 'Failed to predict grade'}), 500

@predictive_analytics.route('/trajectory/<topic_id>')
@login_required
def analyze_trajectory(topic_id):
    """Analyze learning trajectory for a topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        # Get optional days back parameter
        days_back = request.args.get('days_back', 30, type=int)
        
        trajectory = analytics.analyze_learning_trajectory(topic_id, days_back)
        
        return jsonify(trajectory)
    
    except Exception as e:
        print(f"Error analyzing trajectory: {e}")
        return jsonify({'error': 'Failed to analyze trajectory'}), 500

@predictive_analytics.route('/efficiency/<topic_id>')
@login_required
def predict_efficiency(topic_id):
    """Predict study efficiency for a topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        # Get study time parameter
        study_time = request.args.get('study_time', 60, type=int)
        
        efficiency = analytics.predict_study_efficiency(topic_id, study_time)
        
        return jsonify(efficiency)
    
    except Exception as e:
        print(f"Error predicting efficiency: {e}")
        return jsonify({'error': 'Failed to predict efficiency'}), 500

@predictive_analytics.route('/risk-assessment/<topic_id>')
@login_required
def assess_risks(topic_id):
    """Assess risk factors for a topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        risk_assessment = analytics.identify_risk_factors(topic_id)
        
        return jsonify(risk_assessment)
    
    except Exception as e:
        print(f"Error assessing risks: {e}")
        return jsonify({'error': 'Failed to assess risks'}), 500

@predictive_analytics.route('/revision-schedule/<topic_id>')
@login_required
def predict_revision_schedule(topic_id):
    """Predict optimal revision schedule"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        # Get required parameters
        exam_date = request.args.get('exam_date')
        target_grade = request.args.get('target_grade')
        
        if not exam_date:
            return jsonify({'error': 'Exam date is required'}), 400
        
        revision_schedule = analytics.predict_optimal_revision_schedule(topic_id, exam_date, target_grade)
        
        return jsonify(revision_schedule)
    
    except Exception as e:
        print(f"Error predicting revision schedule: {e}")
        return jsonify({'error': 'Failed to predict revision schedule'}), 500

@predictive_analytics.route('/performance-trends')
@login_required
def get_performance_trends():
    """Get performance trends across all topics"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        # Get optional days back parameter
        days_back = request.args.get('days_back', 90, type=int)
        
        trends = analytics.analyze_performance_trends(days_back=days_back)
        
        return jsonify(trends)
    
    except Exception as e:
        print(f"Error getting performance trends: {e}")
        return jsonify({'error': 'Failed to get performance trends'}), 500

@predictive_analytics.route('/comprehensive-report/<topic_id>')
@login_required
def get_comprehensive_report(topic_id):
    """Get comprehensive analytics report for a topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        # Get optional parameters
        exam_date = request.args.get('exam_date')
        target_grade = request.args.get('target_grade')
        days_back = request.args.get('days_back', 30, type=int)
        
        # Generate comprehensive report
        report = {
            'topic_id': topic_id,
            'grade_prediction': analytics.predict_exam_grade(topic_id, exam_date, target_grade),
            'learning_trajectory': analytics.analyze_learning_trajectory(topic_id, days_back),
            'risk_assessment': analytics.identify_risk_factors(topic_id),
            'study_efficiency': analytics.predict_study_efficiency(topic_id, 60),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add revision schedule if exam date provided
        if exam_date:
            report['revision_schedule'] = analytics.predict_optimal_revision_schedule(topic_id, exam_date, target_grade)
        
        return jsonify(report)
    
    except Exception as e:
        print(f"Error generating comprehensive report: {e}")
        return jsonify({'error': 'Failed to generate comprehensive report'}), 500

@predictive_analytics.route('/insights')
@login_required
def get_insights():
    """Get personalized learning insights"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        # Get performance trends
        trends = analytics.analyze_performance_trends(days_back=90)
        
        # Generate insights
        insights = {
            'performance_trends': trends,
            'key_insights': [
                'Your learning velocity is improving',
                'Focus on consistent study patterns',
                'Consider increasing quiz frequency'
            ],
            'recommendations': [
                'Study daily for better retention',
                'Take practice quizzes regularly',
                'Review weak areas more frequently'
            ],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(insights)
    
    except Exception as e:
        print(f"Error getting insights: {e}")
        return jsonify({'error': 'Failed to get insights'}), 500

@predictive_analytics.route('/comparison')
@login_required
def compare_performance():
    """Compare performance across topics"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        analytics = PredictiveAnalytics(user.id)
        
        # Get performance trends
        trends = analytics.analyze_performance_trends(days_back=90)
        
        # Generate comparison data
        comparison = {
            'topics_analyzed': trends.get('total_topics_analyzed', 0),
            'cross_topic_trends': trends.get('cross_topic_trends', {}),
            'strengths_weaknesses': trends.get('strengths_weaknesses', {}),
            'recommendations': [
                'Focus on weaker subjects',
                'Maintain strength in strong areas',
                'Balance study time across topics'
            ],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(comparison)
    
    except Exception as e:
        print(f"Error comparing performance: {e}")
        return jsonify({'error': 'Failed to compare performance'}), 500

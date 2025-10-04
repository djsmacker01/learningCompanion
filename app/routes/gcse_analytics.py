

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.gcse_analytics import (
    GCSEPerformanceAnalytics, GCSEComparativeAnalytics, GCSERecommendationEngine
)
from app.models.gcse_curriculum import GCSESubject
from app.models import Topic
from app.routes.topics import get_current_user
from datetime import datetime, date, timedelta
import json

gcse_analytics = Blueprint('gcse_analytics', __name__, url_prefix='/gcse/analytics')

@gcse_analytics.route('/')
@login_required
def analytics_dashboard():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        performance_analytics = GCSEPerformanceAnalytics(user.id)
        performance_report = performance_analytics.get_comprehensive_performance_report()
        
        
        comparative_analytics = GCSEComparativeAnalytics(user.id)
        subject_comparison = comparative_analytics.get_subject_comparison()
        
        
        recommendation_engine = GCSERecommendationEngine(user.id)
        recommendations = recommendation_engine.get_personalized_recommendations()
        
        return render_template('gcse/analytics/dashboard.html',
                             user_gcse_topics=user_gcse_topics,
                             performance_report=performance_report,
                             subject_comparison=subject_comparison,
                             recommendations=recommendations)
    
    except Exception as e:
        flash('Error loading analytics dashboard.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_analytics.route('/performance')
@login_required
def performance_analytics():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.args.get('subject_id')
        days_back = request.args.get('days_back', 90, type=int)
        
        
        performance_analytics = GCSEPerformanceAnalytics(user.id, subject_id)
        performance_report = performance_analytics.get_comprehensive_performance_report(days_back)
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/analytics/performance.html',
                             performance_report=performance_report,
                             user_gcse_topics=user_gcse_topics,
                             selected_subject_id=subject_id,
                             selected_days_back=days_back)
    
    except Exception as e:
        flash('Error loading performance analytics.', 'error')
        return redirect(url_for('gcse_analytics.analytics_dashboard'))

@gcse_analytics.route('/comparison')
@login_required
def subject_comparison():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        comparative_analytics = GCSEComparativeAnalytics(user.id)
        subject_comparison = comparative_analytics.get_subject_comparison()
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/analytics/comparison.html',
                             subject_comparison=subject_comparison,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading subject comparison.', 'error')
        return redirect(url_for('gcse_analytics.analytics_dashboard'))

@gcse_analytics.route('/recommendations')
@login_required
def recommendations():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        recommendation_engine = GCSERecommendationEngine(user.id)
        recommendations = recommendation_engine.get_personalized_recommendations()
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/analytics/recommendations.html',
                             recommendations=recommendations,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading recommendations.', 'error')
        return redirect(url_for('gcse_analytics.analytics_dashboard'))

@gcse_analytics.route('/trends')
@login_required
def performance_trends():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.args.get('subject_id')
        days_back = request.args.get('days_back', 180, type=int)
        
        
        performance_analytics = GCSEPerformanceAnalytics(user.id, subject_id)
        performance_report = performance_analytics.get_comprehensive_performance_report(days_back)
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/analytics/trends.html',
                             performance_report=performance_report,
                             user_gcse_topics=user_gcse_topics,
                             selected_subject_id=subject_id,
                             selected_days_back=days_back)
    
    except Exception as e:
        flash('Error loading performance trends.', 'error')
        return redirect(url_for('gcse_analytics.analytics_dashboard'))

@gcse_analytics.route('/efficiency')
@login_required
def study_efficiency():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        days_back = request.args.get('days_back', 30, type=int)
        
        
        performance_analytics = GCSEPerformanceAnalytics(user.id)
        performance_report = performance_analytics.get_comprehensive_performance_report(days_back)
        
        
        study_efficiency = performance_report.get("study_efficiency", {})
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/analytics/efficiency.html',
                             study_efficiency=study_efficiency,
                             user_gcse_topics=user_gcse_topics,
                             selected_days_back=days_back)
    
    except Exception as e:
        flash('Error loading study efficiency analytics.', 'error')
        return redirect(url_for('gcse_analytics.analytics_dashboard'))

@gcse_analytics.route('/reports')
@login_required
def performance_reports():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.args.get('subject_id')
        report_type = request.args.get('report_type', 'comprehensive')
        days_back = request.args.get('days_back', 90, type=int)
        
        
        performance_analytics = GCSEPerformanceAnalytics(user.id, subject_id)
        performance_report = performance_analytics.get_comprehensive_performance_report(days_back)
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        if report_type == 'comprehensive':
            report_data = performance_report
        elif report_type == 'trends':
            report_data = {
                "trends": performance_report.get("trends", {}),
                "performance_metrics": performance_report.get("performance_metrics", {})
            }
        elif report_type == 'recommendations':
            recommendation_engine = GCSERecommendationEngine(user.id)
            report_data = recommendation_engine.get_personalized_recommendations()
        else:
            report_data = performance_report
        
        return render_template('gcse/analytics/reports.html',
                             report_data=report_data,
                             report_type=report_type,
                             user_gcse_topics=user_gcse_topics,
                             selected_subject_id=subject_id,
                             selected_days_back=days_back)
    
    except Exception as e:
        flash('Error loading performance reports.', 'error')
        return redirect(url_for('gcse_analytics.analytics_dashboard'))


@gcse_analytics.route('/api/performance-data')
@login_required
def api_get_performance_data():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        subject_id = request.args.get('subject_id')
        days_back = request.args.get('days_back', 90, type=int)
        
        
        performance_analytics = GCSEPerformanceAnalytics(user.id, subject_id)
        performance_report = performance_analytics.get_comprehensive_performance_report(days_back)
        
        
        chart_data = {
            "weekly_performance": performance_report.get("trends", {}).get("weekly_performance", []),
            "performance_by_type": performance_report.get("performance_metrics", {}).get("performance_by_type", {}),
            "grade_predictions": performance_report.get("grade_predictions", {}),
            "study_efficiency": performance_report.get("study_efficiency", {})
        }
        
        return jsonify({
            'success': True,
            'chart_data': chart_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_analytics.route('/api/subject-comparison')
@login_required
def api_get_subject_comparison():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        comparative_analytics = GCSEComparativeAnalytics(user.id)
        subject_comparison = comparative_analytics.get_subject_comparison()
        
        return jsonify({
            'success': True,
            'subject_comparison': subject_comparison
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_analytics.route('/api/recommendations')
@login_required
def api_get_recommendations():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        recommendation_engine = GCSERecommendationEngine(user.id)
        recommendations = recommendation_engine.get_personalized_recommendations()
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_analytics.route('/api/export-report', methods=['POST'])
@login_required
def api_export_report():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        subject_id = data.get('subject_id')
        report_type = data.get('report_type', 'comprehensive')
        days_back = data.get('days_back', 90)
        
        
        performance_analytics = GCSEPerformanceAnalytics(user.id, subject_id)
        performance_report = performance_analytics.get_comprehensive_performance_report(days_back)
        
        
        export_data = {
            "report_type": report_type,
            "generated_at": datetime.now().isoformat(),
            "data_period": f"Last {days_back} days",
            "performance_data": performance_report
        }
        
        return jsonify({
            'success': True,
            'export_data': export_data,
            'filename': f'gcse_performance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


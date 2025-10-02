"""
Advanced Analytics Routes for Learning Companion
Epic 12: Smart Learning Analytics & Predictive Learning
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.advanced_analytics import (
    LearningVelocity, KnowledgeRetention, LearningEfficiency, 
    LearningPath, LearningPathStep, KnowledgeGap, PredictiveAnalytics,
    StudyTimeOptimization, BurnoutRisk, GoalForecasting
)
from app.models import get_supabase_client
from datetime import datetime, timedelta
import json

advanced_analytics_bp = Blueprint('advanced_analytics', __name__)

@advanced_analytics_bp.route('/analytics/advanced')
@login_required
def advanced_dashboard():
    """Advanced analytics dashboard"""
    try:
        user_id = current_user.id
        
        # Get learning velocity data
        velocity_data = LearningVelocity.get_user_velocity(user_id)
        
        # Get knowledge retention data
        retention_data = KnowledgeRetention.get_user_retention(user_id)
        
        # Get learning efficiency data
        client = get_supabase_client()
        efficiency_result = client.table('learning_efficiency').select('*').eq('user_id', user_id).order('measurement_date', desc=True).limit(10).execute()
        efficiency_data = efficiency_result.data if efficiency_result.data else []
        
        # Get learning paths
        learning_paths = LearningPath.get_user_paths(user_id)
        
        # Get knowledge gaps
        gaps_result = client.table('knowledge_gaps').select('*').eq('user_id', user_id).eq('is_resolved', False).execute()
        knowledge_gaps = gaps_result.data if gaps_result.data else []
        
        # Get predictive analytics
        predictive_result = client.table('predictive_analytics').select('*').eq('user_id', user_id).order('prediction_date', desc=True).limit(5).execute()
        predictive_data = predictive_result.data if predictive_result.data else []
        
        # Get study time optimization
        study_optimization = StudyTimeOptimization.get_user_optimization(user_id)
        
        # Get burnout risk
        burnout_result = client.table('burnout_risk').select('*').eq('user_id', user_id).order('last_assessment', desc=True).limit(1).execute()
        burnout_data = burnout_result.data[0] if burnout_result.data else None
        
        # Get goal forecasting
        goals_result = client.table('goal_forecasting').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(3).execute()
        goal_forecasts = goals_result.data if goals_result.data else []
        
        return render_template('analytics/advanced_dashboard.html',
                             velocity_data=velocity_data,
                             retention_data=retention_data,
                             efficiency_data=efficiency_data,
                             learning_paths=learning_paths,
                             knowledge_gaps=knowledge_gaps,
                             predictive_data=predictive_data,
                             study_optimization=study_optimization,
                             burnout_data=burnout_data,
                             goal_forecasts=goal_forecasts)
    
    except Exception as e:
        flash(f'Error loading advanced analytics: {str(e)}', 'error')
        return redirect(url_for('analytics.dashboard'))

@advanced_analytics_bp.route('/analytics/velocity')
@login_required
def learning_velocity():
    """Learning velocity analysis"""
    try:
        user_id = current_user.id
        topic_id = request.args.get('topic_id')
        
        # Get velocity data
        velocity_data = LearningVelocity.get_user_velocity(user_id, topic_id)
        
        # Get topics for filter
        client = get_supabase_client()
        topics_result = client.table('topics').select('id, title').eq('user_id', user_id).execute()
        topics = topics_result.data if topics_result.data else []
        
        return render_template('analytics/learning_velocity.html',
                             velocity_data=velocity_data,
                             topics=topics,
                             selected_topic_id=topic_id)
    
    except Exception as e:
        flash(f'Error loading learning velocity: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.advanced_dashboard'))

@advanced_analytics_bp.route('/analytics/retention')
@login_required
def knowledge_retention():
    """Knowledge retention analysis"""
    try:
        user_id = current_user.id
        topic_id = request.args.get('topic_id')
        
        # Get retention data
        retention_data = KnowledgeRetention.get_user_retention(user_id, topic_id)
        
        # Get topics for filter
        client = get_supabase_client()
        topics_result = client.table('topics').select('id, title').eq('user_id', user_id).execute()
        topics = topics_result.data if topics_result.data else []
        
        return render_template('analytics/knowledge_retention.html',
                             retention_data=retention_data,
                             topics=topics,
                             selected_topic_id=topic_id)
    
    except Exception as e:
        flash(f'Error loading knowledge retention: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.advanced_dashboard'))

@advanced_analytics_bp.route('/analytics/efficiency')
@login_required
def learning_efficiency():
    """Learning efficiency analysis"""
    try:
        user_id = current_user.id
        topic_id = request.args.get('topic_id')
        
        # Get efficiency data
        client = get_supabase_client()
        query = client.table('learning_efficiency').select('*').eq('user_id', user_id)
        if topic_id:
            query = query.eq('topic_id', topic_id)
        
        efficiency_result = query.order('measurement_date', desc=True).execute()
        efficiency_data = efficiency_result.data if efficiency_result.data else []
        
        # Get topics for filter
        topics_result = client.table('topics').select('id, title').eq('user_id', user_id).execute()
        topics = topics_result.data if topics_result.data else []
        
        return render_template('analytics/learning_efficiency.html',
                             efficiency_data=efficiency_data,
                             topics=topics,
                             selected_topic_id=topic_id)
    
    except Exception as e:
        flash(f'Error loading learning efficiency: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.advanced_dashboard'))

@advanced_analytics_bp.route('/analytics/paths')
@login_required
def learning_paths():
    """Learning paths management"""
    try:
        user_id = current_user.id
        
        # Get learning paths
        learning_paths = LearningPath.get_user_paths(user_id)
        
        # Get topics for path creation
        client = get_supabase_client()
        topics_result = client.table('topics').select('id, title').eq('user_id', user_id).execute()
        topics = topics_result.data if topics_result.data else []
        
        return render_template('analytics/learning_paths.html',
                             learning_paths=learning_paths,
                             topics=topics)
    
    except Exception as e:
        flash(f'Error loading learning paths: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.advanced_dashboard'))

@advanced_analytics_bp.route('/analytics/paths/create', methods=['GET', 'POST'])
@login_required
def create_learning_path():
    """Create new learning path"""
    if request.method == 'POST':
        try:
            user_id = current_user.id
            
            # Get form data
            path_name = request.form.get('path_name')
            path_description = request.form.get('path_description')
            target_skill_level = request.form.get('target_skill_level', 'intermediate')
            estimated_duration_days = int(request.form.get('estimated_duration_days', 30))
            ai_generated = request.form.get('ai_generated') == 'on'
            
            # Create learning path
            learning_path = LearningPath.create(
                user_id=user_id,
                path_name=path_name,
                path_description=path_description,
                target_skill_level=target_skill_level,
                estimated_duration_days=estimated_duration_days,
                ai_generated=ai_generated
            )
            
            if learning_path:
                flash('Learning path created successfully!', 'success')
                return redirect(url_for('advanced_analytics.learning_paths'))
            else:
                flash('Error creating learning path', 'error')
        
        except Exception as e:
            flash(f'Error creating learning path: {str(e)}', 'error')
    
    return render_template('analytics/create_learning_path.html')

@advanced_analytics_bp.route('/analytics/paths/<path_id>')
@login_required
def learning_path_detail(path_id):
    """Learning path detail view"""
    try:
        user_id = current_user.id
        
        # Get learning path
        client = get_supabase_client()
        path_result = client.table('learning_paths').select('*').eq('id', path_id).eq('user_id', user_id).execute()
        
        if not path_result.data:
            flash('Learning path not found', 'error')
            return redirect(url_for('advanced_analytics.learning_paths'))
        
        learning_path = path_result.data[0]
        
        # Get path steps
        steps_result = client.table('learning_path_steps').select('*').eq('path_id', path_id).order('step_order').execute()
        path_steps = steps_result.data if steps_result.data else []
        
        return render_template('analytics/learning_path_detail.html',
                             learning_path=learning_path,
                             path_steps=path_steps)
    
    except Exception as e:
        flash(f'Error loading learning path: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.learning_paths'))

@advanced_analytics_bp.route('/analytics/gaps')
@login_required
def knowledge_gaps():
    """Knowledge gaps analysis"""
    try:
        user_id = current_user.id
        topic_id = request.args.get('topic_id')
        
        # Get knowledge gaps
        client = get_supabase_client()
        query = client.table('knowledge_gaps').select('*').eq('user_id', user_id).eq('is_resolved', False)
        if topic_id:
            query = query.eq('topic_id', topic_id)
        
        gaps_result = query.order('created_at', desc=True).execute()
        knowledge_gaps = gaps_result.data if gaps_result.data else []
        
        # Get topics for filter
        topics_result = client.table('topics').select('id, title').eq('user_id', user_id).execute()
        topics = topics_result.data if topics_result.data else []
        
        return render_template('analytics/knowledge_gaps.html',
                             knowledge_gaps=knowledge_gaps,
                             topics=topics,
                             selected_topic_id=topic_id)
    
    except Exception as e:
        flash(f'Error loading knowledge gaps: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.advanced_dashboard'))

@advanced_analytics_bp.route('/analytics/gaps/detect', methods=['POST'])
@login_required
def detect_knowledge_gaps():
    """Detect knowledge gaps for user"""
    try:
        user_id = current_user.id
        topic_id = request.form.get('topic_id')
        
        if topic_id:
            # Detect gaps for specific topic
            gaps = KnowledgeGap.detect_gaps(user_id, topic_id)
            
            # Save detected gaps
            for gap in gaps:
                KnowledgeGap.create(
                    user_id=user_id,
                    topic_id=topic_id,
                    gap_type=gap.gap_type,
                    gap_severity=gap.gap_severity,
                    gap_description=gap.gap_description,
                    detected_through='ai_analysis',
                    confidence_score=gap.confidence_score,
                    suggested_remediation=gap.suggested_remediation
                )
            
            flash(f'Detected {len(gaps)} knowledge gaps', 'success')
        else:
            flash('Please select a topic to analyze', 'error')
        
        return redirect(url_for('advanced_analytics.knowledge_gaps'))
    
    except Exception as e:
        flash(f'Error detecting knowledge gaps: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.knowledge_gaps'))

@advanced_analytics_bp.route('/analytics/predictive')
@login_required
def predictive_analytics():
    """Predictive analytics dashboard"""
    try:
        user_id = current_user.id
        
        # Get predictive analytics data
        client = get_supabase_client()
        predictive_result = client.table('predictive_analytics').select('*').eq('user_id', user_id).order('prediction_date', desc=True).execute()
        predictive_data = predictive_result.data if predictive_result.data else []
        
        # Get study time optimization
        study_optimization = StudyTimeOptimization.get_user_optimization(user_id)
        
        # Get burnout risk
        burnout_result = client.table('burnout_risk').select('*').eq('user_id', user_id).order('last_assessment', desc=True).limit(1).execute()
        burnout_data = burnout_result.data[0] if burnout_result.data else None
        
        # Get goal forecasts
        goals_result = client.table('goal_forecasting').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        goal_forecasts = goals_result.data if goals_result.data else []
        
        return render_template('analytics/predictive_analytics.html',
                             predictive_data=predictive_data,
                             study_optimization=study_optimization,
                             burnout_data=burnout_data,
                             goal_forecasts=goal_forecasts)
    
    except Exception as e:
        flash(f'Error loading predictive analytics: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.advanced_dashboard'))

@advanced_analytics_bp.route('/analytics/optimization')
@login_required
def study_optimization():
    """Study time optimization"""
    try:
        user_id = current_user.id
        
        # Get study optimization data
        study_optimization = StudyTimeOptimization.get_user_optimization(user_id)
        
        # Get recent study sessions for analysis
        client = get_supabase_client()
        sessions_result = client.table('study_sessions').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(20).execute()
        recent_sessions = sessions_result.data if sessions_result.data else []
        
        return render_template('analytics/study_optimization.html',
                             study_optimization=study_optimization,
                             recent_sessions=recent_sessions)
    
    except Exception as e:
        flash(f'Error loading study optimization: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.advanced_dashboard'))

@advanced_analytics_bp.route('/analytics/burnout')
@login_required
def burnout_analysis():
    """Burnout risk analysis"""
    try:
        user_id = current_user.id
        
        # Assess current burnout risk
        burnout_assessment = BurnoutRisk.assess_risk(user_id)
        
        # Save assessment
        BurnoutRisk.create(
            user_id=user_id,
            risk_level=burnout_assessment.risk_level,
            risk_score=burnout_assessment.risk_score,
            contributing_factors=burnout_assessment.contributing_factors,
            study_intensity_score=burnout_assessment.study_intensity_score,
            rest_adequacy_score=burnout_assessment.rest_adequacy_score,
            stress_indicators=burnout_assessment.stress_indicators,
            recommended_actions=burnout_assessment.recommended_actions
        )
        
        # Get historical burnout data
        client = get_supabase_client()
        burnout_result = client.table('burnout_risk').select('*').eq('user_id', user_id).order('last_assessment', desc=True).limit(10).execute()
        burnout_history = burnout_result.data if burnout_result.data else []
        
        return render_template('analytics/burnout_analysis.html',
                             current_assessment=burnout_assessment,
                             burnout_history=burnout_history)
    
    except Exception as e:
        flash(f'Error analyzing burnout risk: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.advanced_dashboard'))

@advanced_analytics_bp.route('/analytics/goals')
@login_required
def goal_forecasting():
    """Goal achievement forecasting"""
    try:
        user_id = current_user.id
        
        # Get goal forecasts
        client = get_supabase_client()
        goals_result = client.table('goal_forecasting').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        goal_forecasts = goals_result.data if goals_result.data else []
        
        return render_template('analytics/goal_forecasting.html',
                             goal_forecasts=goal_forecasts)
    
    except Exception as e:
        flash(f'Error loading goal forecasting: {str(e)}', 'error')
        return redirect(url_for('advanced_analytics.advanced_dashboard'))

@advanced_analytics_bp.route('/analytics/goals/create', methods=['GET', 'POST'])
@login_required
def create_goal_forecast():
    """Create goal forecast"""
    if request.method == 'POST':
        try:
            user_id = current_user.id
            
            # Get form data
            goal_description = request.form.get('goal_description')
            target_date_str = request.form.get('target_date')
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
            
            # Create goal forecast
            goal_forecast = GoalForecasting.forecast_goal_achievement(
                user_id=user_id,
                goal_description=goal_description,
                target_date=target_date
            )
            
            # Save forecast
            GoalForecasting.create(
                user_id=user_id,
                goal_description=goal_description,
                target_completion_date=target_date,
                predicted_completion_date=goal_forecast.predicted_completion_date,
                confidence_percentage=goal_forecast.confidence_percentage,
                current_progress_percentage=goal_forecast.current_progress_percentage,
                required_velocity=goal_forecast.required_velocity,
                current_velocity=goal_forecast.current_velocity,
                is_on_track=goal_forecast.is_on_track,
                risk_factors=goal_forecast.risk_factors,
                mitigation_strategies=goal_forecast.mitigation_strategies
            )
            
            flash('Goal forecast created successfully!', 'success')
            return redirect(url_for('advanced_analytics.goal_forecasting'))
        
        except Exception as e:
            flash(f'Error creating goal forecast: {str(e)}', 'error')
    
    return render_template('analytics/create_goal_forecast.html')

# API endpoints for AJAX requests
@advanced_analytics_bp.route('/api/analytics/velocity/<topic_id>')
@login_required
def api_learning_velocity(topic_id):
    """API endpoint for learning velocity data"""
    try:
        user_id = current_user.id
        velocity = LearningVelocity.calculate_velocity(user_id, topic_id)
        
        return jsonify({
            'velocity': velocity,
            'topic_id': topic_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_analytics_bp.route('/api/analytics/retention/<topic_id>')
@login_required
def api_knowledge_retention(topic_id):
    """API endpoint for knowledge retention data"""
    try:
        user_id = current_user.id
        retention = KnowledgeRetention.calculate_retention(user_id, topic_id)
        
        return jsonify({
            'retention': retention,
            'topic_id': topic_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_analytics_bp.route('/api/analytics/efficiency/<session_id>')
@login_required
def api_learning_efficiency(session_id):
    """API endpoint for learning efficiency data"""
    try:
        user_id = current_user.id
        efficiency = LearningEfficiency.calculate_efficiency(user_id, None, session_id)
        
        return jsonify({
            'efficiency': efficiency,
            'session_id': session_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_analytics_bp.route('/api/analytics/predict-success', methods=['POST'])
@login_required
def api_predict_success():
    """API endpoint for success probability prediction"""
    try:
        user_id = current_user.id
        data = request.get_json()
        
        topic_id = data.get('topic_id')
        exam_date_str = data.get('exam_date')
        exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d')
        
        success_probability = PredictiveAnalytics.predict_success_probability(
            user_id, topic_id, exam_date
        )
        
        return jsonify({
            'success_probability': success_probability,
            'exam_date': exam_date_str,
            'topic_id': topic_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@advanced_analytics_bp.route('/api/analytics/burnout-assessment')
@login_required
def api_burnout_assessment():
    """API endpoint for burnout risk assessment"""
    try:
        user_id = current_user.id
        burnout_assessment = BurnoutRisk.assess_risk(user_id)
        
        return jsonify({
            'risk_level': burnout_assessment.risk_level,
            'risk_score': burnout_assessment.risk_score,
            'contributing_factors': burnout_assessment.contributing_factors,
            'study_intensity_score': burnout_assessment.study_intensity_score,
            'rest_adequacy_score': burnout_assessment.rest_adequacy_score,
            'stress_indicators': burnout_assessment.stress_indicators,
            'recommended_actions': burnout_assessment.recommended_actions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

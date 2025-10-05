"""
AI Tutor API Routes
Enhanced AI-powered study companion endpoints
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.routes.topics import get_current_user
from app.utils.ai_tutor import AITutor
from datetime import datetime
import json

ai_tutor = Blueprint('ai_tutor', __name__, url_prefix='/ai-tutor')

@ai_tutor.route('/')
@login_required
def tutor_dashboard():
    """AI Tutor dashboard"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        tutor = AITutor(user.id)
        
        # Get personalized recommendations
        recommendations = tutor.get_personalized_study_recommendations()
        
        return render_template('ai_tutor/dashboard.html', 
                             recommendations=recommendations,
                             user=user)
    
    except Exception as e:
        print(f"Error loading AI tutor dashboard: {e}")
        return jsonify({'error': 'Failed to load dashboard'}), 500

@ai_tutor.route('/api/recommendations')
@login_required
def get_recommendations():
    """Get personalized study recommendations"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        tutor = AITutor(user.id)
        recommendations = tutor.get_personalized_study_recommendations()
        
        return jsonify(recommendations)
    
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return jsonify({'error': 'Failed to get recommendations'}), 500

@ai_tutor.route('/api/study-plan/<topic_id>')
@login_required
def generate_study_plan(topic_id):
    """Generate personalized study plan for a topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        tutor = AITutor(user.id)
        
        # Get optional parameters
        target_grade = request.args.get('target_grade')
        time_available = request.args.get('time_available', type=int)
        
        study_plan = tutor.generate_study_plan(topic_id, target_grade, time_available)
        
        return jsonify(study_plan)
    
    except Exception as e:
        print(f"Error generating study plan: {e}")
        return jsonify({'error': 'Failed to generate study plan'}), 500

@ai_tutor.route('/api/explain', methods=['POST'])
@login_required
def explain_concept():
    """Enhanced concept explanation with adaptive difficulty"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        concept = data.get('concept', '').strip()
        topic_id = data.get('topic_id')
        explanation_level = data.get('level', 'intermediate')
        
        if not concept:
            return jsonify({'error': 'Concept is required'}), 400
        
        tutor = AITutor(user.id)
        explanation = tutor.explain_concept_with_ai(concept, topic_id, explanation_level)
        
        return jsonify(explanation)
    
    except Exception as e:
        print(f"Error explaining concept: {e}")
        return jsonify({'error': 'Failed to explain concept'}), 500

@ai_tutor.route('/api/predict-grade/<topic_id>')
@login_required
def predict_grade(topic_id):
    """Predict user's likely grade for a topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        tutor = AITutor(user.id)
        
        # Get optional exam date
        exam_date = request.args.get('exam_date')
        
        prediction = tutor.predict_grade(topic_id, exam_date)
        
        return jsonify(prediction)
    
    except Exception as e:
        print(f"Error predicting grade: {e}")
        return jsonify({'error': 'Failed to predict grade'}), 500

@ai_tutor.route('/api/learning-style')
@login_required
def detect_learning_style():
    """Detect user's learning style"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        tutor = AITutor(user.id)
        learning_style = tutor.detect_learning_style()
        
        return jsonify(learning_style)
    
    except Exception as e:
        print(f"Error detecting learning style: {e}")
        return jsonify({'error': 'Failed to detect learning style'}), 500

@ai_tutor.route('/api/adaptive-quiz/<topic_id>')
@login_required
def get_adaptive_quiz_recommendations(topic_id):
    """Get adaptive quiz recommendations"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        tutor = AITutor(user.id)
        recommendations = tutor.get_adaptive_quiz_recommendations(topic_id)
        
        return jsonify(recommendations)
    
    except Exception as e:
        print(f"Error getting adaptive quiz recommendations: {e}")
        return jsonify({'error': 'Failed to get quiz recommendations'}), 500

@ai_tutor.route('/chat')
@login_required
def tutor_chat():
    """Enhanced AI tutor chat interface"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        return render_template('ai_tutor/chat.html', user=user)
    
    except Exception as e:
        print(f"Error loading tutor chat: {e}")
        return jsonify({'error': 'Failed to load chat interface'}), 500

@ai_tutor.route('/api/chat', methods=['POST'])
@login_required
def tutor_chat_api():
    """Enhanced AI tutor chat API"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        message = data.get('message', '').strip()
        context = data.get('context', '')
        topic_id = data.get('topic_id')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        tutor = AITutor(user.id)
        
        # Enhanced chat with learning context
        response = tutor._enhanced_chat(message, context, topic_id)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error in tutor chat: {e}")
        return jsonify({'error': 'Failed to process chat message'}), 500

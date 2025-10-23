"""
AI Tutor API Routes
Enhanced AI-powered study companion endpoints
"""

from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
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

@ai_tutor.route('/api/topics')
@login_required
def get_topics():
    """Get user's topics for AI Tutor features"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        from app.models import Topic
        topics = Topic.get_all_by_user(user.id)
        
        return jsonify({
            'topics': [{'id': topic.id, 'title': topic.title} for topic in topics]
        })
    
    except Exception as e:
        print(f"Error getting topics: {e}")
        return jsonify({'error': 'Failed to get topics'}), 500

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
        

        target_grade = request.args.get('target_grade')
        time_available = request.args.get('time_available', type=int)
        
        print(f"Study Plan Debug - Calling generate_study_plan for topic: {topic_id}")
        study_plan = tutor.generate_study_plan(topic_id, target_grade, time_available)
        print(f"Study Plan Debug - Study plan generated: {type(study_plan)}")
        
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
        print(f"Concept Explainer Debug - Request data: {data}")
        
        concept = data.get('concept', '').strip()
        topic_id = data.get('topic_id')
        explanation_level = data.get('level', 'intermediate')
        
        print(f"Concept Explainer Debug - Concept: '{concept}', Topic ID: {topic_id}, Level: {explanation_level}")
        
        if not concept:
            return jsonify({'error': 'Concept is required'}), 400
        
        tutor = AITutor(user.id)
        print(f"Concept Explainer Debug - Calling explain_concept_with_ai...")
        explanation = tutor.explain_concept_with_ai(concept, topic_id, explanation_level)
        print(f"Concept Explainer Debug - Result: {type(explanation)}, Keys: {list(explanation.keys()) if isinstance(explanation, dict) else 'Not dict'}")
        print(f"Concept Explainer Debug - Activity tracking should have been called")
        
        return jsonify(explanation)
    
    except Exception as e:
        print(f"Error explaining concept: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to explain concept: {str(e)}'}), 500

@ai_tutor.route('/api/predict-grade/<topic_id>')
@login_required
def predict_grade(topic_id):
    """Predict user's likely grade for a topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        tutor = AITutor(user.id)
        

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
        
        print(f"Adaptive Quiz Debug - Topic ID: {topic_id}, User: {user.id}")
        
        tutor = AITutor(user.id)
        recommendations = tutor.get_adaptive_quiz_recommendations(topic_id)
        
        print(f"Adaptive Quiz Debug - Result type: {type(recommendations)}")
        print(f"Adaptive Quiz Debug - Result keys: {list(recommendations.keys()) if isinstance(recommendations, dict) else 'Not dict'}")
        if 'recommendations' in recommendations:
            print(f"Adaptive Quiz Debug - Recommendations count: {len(recommendations['recommendations'])}")
            if recommendations['recommendations']:
                print(f"Adaptive Quiz Debug - First recommendation: {recommendations['recommendations'][0]}")
        
        return jsonify(recommendations)
    
    except Exception as e:
        print(f"Error getting adaptive quiz recommendations: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to get quiz recommendations: {str(e)}'}), 500

@ai_tutor.route('/api/activity')
@login_required
def get_ai_activity():
    """Get recent AI activity for the user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        print(f"AI Activity Debug - User ID: {user.id}")
        
        from app.models import AIActivity
        activities = AIActivity.get_recent_activity(user.id, limit=10)
        
        print(f"AI Activity Debug - Retrieved {len(activities)} activities")
        
        # Convert activities to JSON-serializable format
        activity_data = []
        for activity in activities:
            try:
                activity_data.append({
                    'id': activity.id,
                    'activity_type': activity.activity_type,
                    'topic_id': activity.topic_id,
                    'result_summary': activity.result_summary,
                    'created_at': activity.created_at.isoformat(),
                    'icon': activity.get_activity_icon(),
                    'color': activity.get_activity_color(),
                    'title': activity.get_activity_title(),
                    'time_ago': activity.get_time_ago()
                })
            except Exception as activity_error:
                print(f"Error processing activity {activity.id}: {activity_error}")
                continue
        
        print(f"AI Activity Debug - Returning {len(activity_data)} processed activities")
        
        return jsonify({
            'activities': activity_data,
            'count': len(activity_data)
        })
    
    except Exception as e:
        print(f"Error getting AI activity: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to get AI activity: {str(e)}'}), 500

@ai_tutor.route('/chat')
@login_required
def tutor_chat():
    """Enhanced AI tutor chat interface"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        return render_template('ai_tutor/chat.html', user=user)
    
    except Exception as e:
        print(f"Error loading chat interface: {e}")
        import traceback
        traceback.print_exc()
        flash('Error loading chat interface. Please try again.', 'error')
        return redirect(url_for('ai_tutor.tutor_dashboard'))

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

@ai_tutor.route('/api/save-learning-style', methods=['POST'])
@login_required
def save_learning_style():
    """Save learning style to user profile"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        

        learning_style = data.get('learning_style', 'visual')
        confidence = data.get('confidence', 75)
        recommendations = data.get('recommendations', [])
        saved_at = data.get('saved_at', datetime.now().isoformat())
        

        from app.models import get_supabase_client
        supabase = get_supabase_client()
        
        if not supabase:
            return jsonify({'error': 'Database connection failed'}), 500
        

        style_data = {
            'user_id': user.id,
            'learning_style': learning_style,
            'confidence_score': confidence,
            'recommendations': recommendations,
            'study_patterns': {
                'saved_at': saved_at,
                'source': 'ai_detection'
            },
            'created_at': datetime.now().isoformat()
        }
        


        existing = supabase.table('ai_learning_styles').select('id').eq('user_id', user.id).execute()
        
        if existing.data and len(existing.data) > 0:

            result = supabase.table('ai_learning_styles').update({
                'learning_style': learning_style,
                'confidence_score': confidence,
                'recommendations': recommendations,
                'study_patterns': {
                    'saved_at': saved_at,
                    'source': 'ai_detection'
                },
                'updated_at': datetime.now().isoformat()
            }).eq('user_id', user.id).execute()
        else:

            result = supabase.table('ai_learning_styles').insert(style_data).execute()
        
        if result.data:
            return jsonify({
                'success': True,
                'message': 'Learning style saved successfully',
                'learning_style': learning_style,
                'confidence': confidence
            })
        else:
            return jsonify({'error': 'Failed to save learning style'}), 500
    
    except Exception as e:
        print(f"Error saving learning style: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to save learning style: {str(e)}'}), 500

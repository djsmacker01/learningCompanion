"""
GCSE AI Enhancement API Routes
GCSE-specific AI features and integration endpoints
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.routes.topics import get_current_user
from app.utils.gcse_ai_enhancement import GCSEAIEnhancement
from datetime import datetime
import json

gcse_ai = Blueprint('gcse_ai', __name__, url_prefix='/gcse-ai')

@gcse_ai.route('/')
@login_required
def gcse_ai_dashboard():
    """GCSE AI Enhancement Dashboard"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        return render_template('gcse_ai/dashboard.html', user=user)
    
    except Exception as e:
        print(f"Error loading GCSE AI dashboard: {e}")
        return jsonify({'error': 'Failed to load dashboard'}), 500

@gcse_ai.route('/api/study-plan')
@login_required
def generate_gcse_study_plan():
    """Generate comprehensive GCSE study plan"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get required parameters
        subject = request.args.get('subject')
        exam_board = request.args.get('exam_board')
        target_grade = request.args.get('target_grade')
        exam_date = request.args.get('exam_date')
        
        if not all([subject, exam_board, target_grade, exam_date]):
            return jsonify({'error': 'Missing required parameters: subject, exam_board, target_grade, exam_date'}), 400
        
        study_plan = enhancement.generate_gcse_study_plan(subject, exam_board, target_grade, exam_date)
        
        return jsonify(study_plan)
    
    except Exception as e:
        print(f"Error generating GCSE study plan: {e}")
        return jsonify({'error': 'Failed to generate study plan'}), 500

@gcse_ai.route('/api/past-paper-analysis')
@login_required
def analyze_gcse_past_papers():
    """Analyze GCSE past papers for patterns and insights"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get parameters
        subject = request.args.get('subject')
        exam_board = request.args.get('exam_board')
        paper_type = request.args.get('paper_type', 'recent')
        
        if not all([subject, exam_board]):
            return jsonify({'error': 'Missing required parameters: subject, exam_board'}), 400
        
        analysis = enhancement.generate_gcse_past_paper_analysis(subject, exam_board, paper_type)
        
        return jsonify(analysis)
    
    except Exception as e:
        print(f"Error analyzing GCSE past papers: {e}")
        return jsonify({'error': 'Failed to analyze past papers'}), 500

@gcse_ai.route('/api/grade-boundary-predictions')
@login_required
def predict_gcse_grade_boundaries():
    """Predict GCSE grade boundaries and student performance"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get parameters
        subject = request.args.get('subject')
        exam_board = request.args.get('exam_board')
        
        if not all([subject, exam_board]):
            return jsonify({'error': 'Missing required parameters: subject, exam_board'}), 400
        
        # Get current performance from request body
        current_performance = request.get_json() or {}
        
        predictions = enhancement.generate_gcse_grade_boundary_predictions(subject, exam_board, current_performance)
        
        return jsonify(predictions)
    
    except Exception as e:
        print(f"Error predicting GCSE grade boundaries: {e}")
        return jsonify({'error': 'Failed to predict grade boundaries'}), 500

@gcse_ai.route('/api/revision-schedule', methods=['POST'])
@login_required
def generate_gcse_revision_schedule():
    """Generate comprehensive GCSE revision schedule across multiple subjects"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get data from request body
        data = request.get_json()
        
        subjects = data.get('subjects', [])
        exam_dates = data.get('exam_dates', {})
        target_grades = data.get('target_grades', {})
        
        if not subjects:
            return jsonify({'error': 'At least one subject is required'}), 400
        
        revision_schedule = enhancement.generate_gcse_revision_schedule(subjects, exam_dates, target_grades)
        
        return jsonify(revision_schedule)
    
    except Exception as e:
        print(f"Error generating GCSE revision schedule: {e}")
        return jsonify({'error': 'Failed to generate revision schedule'}), 500

@gcse_ai.route('/api/exam-techniques')
@login_required
def generate_gcse_exam_techniques():
    """Generate GCSE-specific exam techniques and strategies"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get parameters
        subject = request.args.get('subject')
        exam_board = request.args.get('exam_board')
        question_types = request.args.getlist('question_types') or ['multiple_choice', 'short_answer', 'essay']
        
        if not all([subject, exam_board]):
            return jsonify({'error': 'Missing required parameters: subject, exam_board'}), 400
        
        techniques = enhancement.generate_gcse_exam_techniques(subject, exam_board, question_types)
        
        return jsonify(techniques)
    
    except Exception as e:
        print(f"Error generating GCSE exam techniques: {e}")
        return jsonify({'error': 'Failed to generate exam techniques'}), 500

@gcse_ai.route('/api/personalized-content')
@login_required
def generate_gcse_personalized_content():
    """Generate GCSE-specific personalized content"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get parameters
        subject = request.args.get('subject')
        topic = request.args.get('topic')
        learning_style = request.args.get('learning_style', 'visual')
        difficulty_level = request.args.get('difficulty_level', 'intermediate')
        
        if not all([subject, topic]):
            return jsonify({'error': 'Missing required parameters: subject, topic'}), 400
        
        content = enhancement.generate_gcse_personalized_content(subject, topic, learning_style, difficulty_level)
        
        return jsonify(content)
    
    except Exception as e:
        print(f"Error generating GCSE personalized content: {e}")
        return jsonify({'error': 'Failed to generate personalized content'}), 500

@gcse_ai.route('/api/performance-gap-analysis', methods=['POST'])
@login_required
def analyze_gcse_performance_gaps():
    """Analyze GCSE performance gaps and provide improvement strategies"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get data from request body
        data = request.get_json()
        
        subject = data.get('subject')
        user_performance = data.get('user_performance', {})
        
        if not subject:
            return jsonify({'error': 'Subject is required'}), 400
        
        analysis = enhancement.analyze_gcse_performance_gaps(subject, user_performance)
        
        return jsonify(analysis)
    
    except Exception as e:
        print(f"Error analyzing GCSE performance gaps: {e}")
        return jsonify({'error': 'Failed to analyze performance gaps'}), 500

@gcse_ai.route('/api/subjects')
@login_required
def get_gcse_subjects():
    """Get available GCSE subjects"""
    try:
        subjects = [
            {'name': 'Mathematics', 'code': 'maths', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'English Language', 'code': 'english_lang', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'English Literature', 'code': 'english_lit', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Biology', 'code': 'biology', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Chemistry', 'code': 'chemistry', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Physics', 'code': 'physics', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'History', 'code': 'history', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Geography', 'code': 'geography', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'French', 'code': 'french', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Spanish', 'code': 'spanish', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'German', 'code': 'german', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Computer Science', 'code': 'computer_science', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Business Studies', 'code': 'business', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Economics', 'code': 'economics', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Psychology', 'code': 'psychology', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Sociology', 'code': 'sociology', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Art & Design', 'code': 'art', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Music', 'code': 'music', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Drama', 'code': 'drama', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Physical Education', 'code': 'pe', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']}
        ]
        
        return jsonify({'subjects': subjects})
    
    except Exception as e:
        print(f"Error getting GCSE subjects: {e}")
        return jsonify({'error': 'Failed to get GCSE subjects'}), 500

@gcse_ai.route('/api/grade-boundaries/<subject>/<exam_board>')
@login_required
def get_gcse_grade_boundaries(subject, exam_board):
    """Get GCSE grade boundaries for a subject and exam board"""
    try:
        # This would typically fetch from a database or external API
        # For now, return sample data
        grade_boundaries = {
            'subject': subject,
            'exam_board': exam_board,
            'boundaries': {
                '2023': {'9': 85, '8': 75, '7': 65, '6': 55, '5': 45, '4': 35, '3': 25, '2': 15, '1': 5},
                '2022': {'9': 83, '8': 73, '7': 63, '6': 53, '5': 43, '4': 33, '3': 23, '2': 13, '1': 3},
                '2021': {'9': 87, '8': 77, '7': 67, '6': 57, '5': 47, '4': 37, '3': 27, '2': 17, '1': 7}
            },
            'trends': {
                'increasing_grades': ['9', '8'],
                'stable_grades': ['7', '6', '5'],
                'decreasing_grades': ['4', '3', '2', '1']
            }
        }
        
        return jsonify(grade_boundaries)
    
    except Exception as e:
        print(f"Error getting GCSE grade boundaries: {e}")
        return jsonify({'error': 'Failed to get grade boundaries'}), 500

@gcse_ai.route('/comprehensive-analysis')
@login_required
def comprehensive_gcse_analysis():
    """Comprehensive GCSE analysis page"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        return render_template('gcse_ai/comprehensive_analysis.html', user=user)
    
    except Exception as e:
        print(f"Error loading comprehensive GCSE analysis: {e}")
        return jsonify({'error': 'Failed to load comprehensive analysis'}), 500



from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.gcse_grading import GCSEGradeBoundary, GCSEGradeCalculator, GCSEGradeTracker
from app.models.gcse_curriculum import GCSESubject, GCSESpecification
from app.models import Topic
from app.routes.topics import get_current_user
from datetime import datetime, date
import json

gcse_grading = Blueprint('gcse_grading', __name__, url_prefix='/gcse/grading')

@gcse_grading.route('/')
@login_required
def grade_calculator():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        subjects = GCSESubject.get_all_subjects()
        exam_boards = GCSESpecification.get_exam_boards()
        
        return render_template('gcse/grading/calculator.html',
                             user_gcse_topics=user_gcse_topics,
                             subjects=subjects,
                             exam_boards=exam_boards)
    
    except Exception as e:
        flash('Error loading grade calculator.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_grading.route('/calculate', methods=['POST'])
@login_required
def calculate_grade():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        achieved_marks = data.get('achieved_marks', type=int)
        total_marks = data.get('total_marks', type=int)
        exam_board = data.get('exam_board')
        subject_code = data.get('subject_code')
        tier = data.get('tier')
        
        if not all([achieved_marks, total_marks, exam_board, subject_code]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        
        grade_result = GCSEGradeCalculator.calculate_grade(
            achieved_marks, total_marks, exam_board, subject_code, tier
        )
        
        return jsonify({
            'success': True,
            'grade_result': grade_result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_grading.route('/predict')
@login_required
def grade_predictor():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        subjects = GCSESubject.get_all_subjects()
        exam_boards = GCSESpecification.get_exam_boards()
        
        return render_template('gcse/grading/predictor.html',
                             user_gcse_topics=user_gcse_topics,
                             subjects=subjects,
                             exam_boards=exam_boards)
    
    except Exception as e:
        flash('Error loading grade predictor.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_grading.route('/predict/<subject_id>')
@login_required
def predict_subject_grade(subject_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject = GCSESubject.get_subject_by_id(subject_id)
        if not subject:
            flash('GCSE subject not found.', 'error')
            return redirect(url_for('gcse_grading.grade_predictor'))
        
        target_grade = request.args.get('target_grade', '5')
        
        
        
        current_performance = []  
        
        
        prediction = GCSEGradeCalculator.predict_grade(
            current_performance, target_grade, subject.exam_board, subject.specification_code
        )
        
        
        requirements = GCSEGradeCalculator.get_grade_requirements(
            target_grade, subject.exam_board, subject.specification_code
        )
        
        return render_template('gcse/grading/subject_prediction.html',
                             subject=subject,
                             target_grade=target_grade,
                             prediction=prediction,
                             requirements=requirements)
    
    except Exception as e:
        flash('Error generating grade prediction.', 'error')
        return redirect(url_for('gcse_grading.grade_predictor'))

@gcse_grading.route('/tracker')
@login_required
def grade_tracker():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        subject_progressions = []
        for topic in user_gcse_topics:
            if topic.gcse_subject_id and topic.gcse_exam_board and topic.gcse_specification_code:
                progression = GCSEGradeTracker.track_grade_progression(
                    user.id, topic.gcse_subject_id, topic.gcse_exam_board, topic.gcse_specification_code
                )
                
                if "error" not in progression:
                    subject_progressions.append({
                        'topic': topic,
                        'progression': progression
                    })
        
        return render_template('gcse/grading/tracker.html',
                             subject_progressions=subject_progressions)
    
    except Exception as e:
        flash('Error loading grade tracker.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_grading.route('/requirements/<subject_id>')
@login_required
def grade_requirements(subject_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject = GCSESubject.get_subject_by_id(subject_id)
        if not subject:
            flash('GCSE subject not found.', 'error')
            return redirect(url_for('gcse.gcse_dashboard'))
        
        
        boundaries = GCSEGradeBoundary.get_grade_boundaries(
            subject.exam_board, subject.specification_code
        )
        
        
        grade_requirements = {}
        for tier, tier_boundaries in boundaries.items():
            grade_requirements[tier] = {}
            for grade in tier_boundaries.keys():
                requirements = GCSEGradeCalculator.get_grade_requirements(
                    grade, subject.exam_board, subject.specification_code, tier
                )
                grade_requirements[tier][grade] = requirements
        
        return render_template('gcse/grading/requirements.html',
                             subject=subject,
                             boundaries=boundaries,
                             grade_requirements=grade_requirements)
    
    except Exception as e:
        flash('Error loading grade requirements.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_grading.route('/targets')
@login_required
def grade_targets():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        subject_targets = []
        for topic in user_gcse_topics:
            if topic.gcse_subject_id and topic.gcse_exam_board and topic.gcse_specification_code:
                targets = GCSEGradeTracker.get_grade_target_recommendations(
                    user.id, topic.gcse_subject_id, topic.gcse_exam_board, topic.gcse_specification_code
                )
                
                subject_targets.append({
                    'topic': topic,
                    'targets': targets
                })
        
        return render_template('gcse/grading/targets.html',
                             subject_targets=subject_targets)
    
    except Exception as e:
        flash('Error loading grade targets.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))


@gcse_grading.route('/api/boundaries/<exam_board>/<subject_code>')
@login_required
def api_get_grade_boundaries(exam_board, subject_code):
    
    try:
        tier = request.args.get('tier')
        exam_year = request.args.get('exam_year', type=int)
        
        boundaries = GCSEGradeBoundary.get_grade_boundaries(exam_board, subject_code, exam_year, tier)
        
        return jsonify({
            'exam_board': exam_board,
            'subject_code': subject_code,
            'boundaries': boundaries
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_grading.route('/api/calculate', methods=['POST'])
@login_required
def api_calculate_grade():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        
        # Convert string values to appropriate types
        try:
            achieved_marks = int(data.get('achieved_marks'))
            total_marks = int(data.get('total_marks'))
        except (ValueError, TypeError) as e:
            return jsonify({'error': 'Invalid marks values - must be numbers'}), 400
        
        exam_board = data.get('exam_board')
        subject_code = data.get('subject_code')
        tier = data.get('tier') if data.get('tier') else None
        
        if not all([achieved_marks, total_marks, exam_board, subject_code]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        
        grade_result = GCSEGradeCalculator.calculate_grade(
            achieved_marks, total_marks, exam_board, subject_code, tier
        )
        
        return jsonify({
            'success': True,
            'grade_result': grade_result
        })
    
    except Exception as e:
        print(f"Error calculating grade: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@gcse_grading.route('/api/predict', methods=['POST'])
@login_required
def api_predict_grade():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        subject_id = data.get('subject_id')
        target_grade = data.get('target_grade')
        
        if not all([subject_id, target_grade]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        
        subject = GCSESubject.get_subject_by_id(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        
        
        current_performance = []  
        
        
        prediction = GCSEGradeCalculator.predict_grade(
            current_performance, target_grade, subject.exam_board, subject.specification_code
        )
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_grading.route('/api/track/<subject_id>')
@login_required
def api_track_progression(subject_id):
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        subject = GCSESubject.get_subject_by_id(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        
        progression = GCSEGradeTracker.track_grade_progression(
            user.id, subject_id, subject.exam_board, subject.specification_code
        )
        
        return jsonify({
            'success': True,
            'progression': progression
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


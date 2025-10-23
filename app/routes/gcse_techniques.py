

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.gcse_study_techniques import (
    GCSEStudyTechnique, GCSEExamStrategy, GCSEStudyPlanGenerator
)
from app.models.gcse_curriculum import GCSESubject
from app.models import Topic
from app.routes.topics import get_current_user
from datetime import datetime, date, timedelta
import json

gcse_techniques = Blueprint('gcse_techniques', __name__, url_prefix='/gcse/techniques')

@gcse_techniques.route('/')
@login_required
def techniques_dashboard():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        popular_techniques = GCSEStudyTechnique.get_all_techniques()[:6]
        
        
        time_management_strategies = GCSEExamStrategy.get_strategies_by_type(strategy_type="time_management")[:3]
        question_approach_strategies = GCSEExamStrategy.get_strategies_by_type(strategy_type="question_approach")[:3]
        
        return render_template('gcse/techniques/dashboard.html',
                             user_gcse_topics=user_gcse_topics,
                             popular_techniques=popular_techniques,
                             time_management_strategies=time_management_strategies,
                             question_approach_strategies=question_approach_strategies)
    
    except Exception as e:
        print(f"Error loading techniques dashboard: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error loading techniques dashboard: {str(e)}', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_techniques.route('/study-techniques')
@login_required
def study_techniques():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        category = request.args.get('category')
        subject = request.args.get('subject')
        difficulty = request.args.get('difficulty')
        
        
        techniques = GCSEStudyTechnique.get_all_techniques(category, subject, difficulty)
        
        
        categories = ["memorization", "understanding", "practice", "exam_technique"]
        subjects = ["all", "sciences", "humanities", "languages", "maths"]
        difficulties = ["beginner", "intermediate", "advanced"]
        
        return render_template('gcse/techniques/study_techniques.html',
                             techniques=techniques,
                             categories=categories,
                             subjects=subjects,
                             difficulties=difficulties,
                             selected_category=category,
                             selected_subject=subject,
                             selected_difficulty=difficulty)
    
    except Exception as e:
        flash('Error loading study techniques.', 'error')
        return redirect(url_for('gcse_techniques.techniques_dashboard'))

@gcse_techniques.route('/study-techniques/<technique_id>')
@login_required
def study_technique_detail(technique_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        technique = GCSEStudyTechnique.get_technique_by_id(technique_id)
        if not technique:
            flash('Study technique not found.', 'error')
            return redirect(url_for('gcse_techniques.study_techniques'))
        
        
        related_techniques = GCSEStudyTechnique.get_all_techniques(
            category=technique.category
        )[:4]
        
        related_techniques = [t for t in related_techniques if t.id != technique_id]
        
        return render_template('gcse/techniques/technique_detail.html',
                             technique=technique,
                             related_techniques=related_techniques)
    
    except Exception as e:
        flash('Error loading technique details.', 'error')
        return redirect(url_for('gcse_techniques.study_techniques'))

@gcse_techniques.route('/exam-strategies')
@login_required
def exam_strategies():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        strategy_type = request.args.get('strategy_type')
        exam_type = request.args.get('exam_type')
        subject = request.args.get('subject')
        
        
        strategies = GCSEExamStrategy.get_strategies_by_type(strategy_type, exam_type, subject)
        
        
        strategy_types = ["time_management", "question_approach", "revision"]
        exam_types = ["multiple_choice", "essay", "practical", "calculation", "all"]
        subjects = ["all", "sciences", "humanities", "languages", "maths"]
        
        return render_template('gcse/techniques/exam_strategies.html',
                             strategies=strategies,
                             strategy_types=strategy_types,
                             exam_types=exam_types,
                             subjects=subjects,
                             selected_strategy_type=strategy_type,
                             selected_exam_type=exam_type,
                             selected_subject=subject)
    
    except Exception as e:
        flash('Error loading exam strategies.', 'error')
        return redirect(url_for('gcse_techniques.techniques_dashboard'))

@gcse_techniques.route('/study-planner')
@login_required
def study_planner():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        subjects = GCSESubject.get_all_subjects()
        
        return render_template('gcse/techniques/study_planner.html',
                             user_gcse_topics=user_gcse_topics,
                             subjects=subjects)
    
    except Exception as e:
        flash('Error loading study planner.', 'error')
        return redirect(url_for('gcse_techniques.techniques_dashboard'))

@gcse_techniques.route('/study-planner/generate', methods=['POST'])
@login_required
def generate_study_plan():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.form.get('subject_id')
        exam_date_str = request.form.get('exam_date')
        study_hours_per_week = request.form.get('study_hours_per_week', 5, type=int)
        learning_style = request.form.get('learning_style', 'mixed')
        weak_areas = request.form.getlist('weak_areas')
        
        if not all([subject_id, exam_date_str]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('gcse_techniques.study_planner'))
        
        try:
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid exam date format.', 'error')
            return redirect(url_for('gcse_techniques.study_planner'))
        
        
        subject = GCSESubject.get_subject_by_id(subject_id)
        if not subject:
            flash('Subject not found.', 'error')
            return redirect(url_for('gcse_techniques.study_planner'))
        
        
        study_plan = GCSEStudyPlanGenerator.generate_study_plan(
            user.id, subject_id, exam_date, study_hours_per_week, learning_style, weak_areas
        )
        
        return render_template('gcse/techniques/study_plan_result.html',
                             subject=subject,
                             study_plan=study_plan,
                             exam_date=exam_date)
    
    except Exception as e:
        flash('Error generating study plan.', 'error')
        return redirect(url_for('gcse_techniques.study_planner'))

@gcse_techniques.route('/learning-style-quiz')
@login_required
def learning_style_quiz():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        quiz_questions = [
            {
                "id": 1,
                "question": "When learning new information, I prefer to:",
                "options": [
                    {"text": "See diagrams, charts, and visual representations", "style": "visual"},
                    {"text": "Listen to explanations or discuss with others", "style": "auditory"},
                    {"text": "Try hands-on activities and experiments", "style": "kinesthetic"}
                ]
            },
            {
                "id": 2,
                "question": "I remember information best when I:",
                "options": [
                    {"text": "See it written down or in pictures", "style": "visual"},
                    {"text": "Hear it explained or repeat it aloud", "style": "auditory"},
                    {"text": "Do something with it or practice it", "style": "kinesthetic"}
                ]
            },
            {
                "id": 3,
                "question": "When studying, I find it most helpful to:",
                "options": [
                    {"text": "Create mind maps and visual notes", "style": "visual"},
                    {"text": "Read aloud or listen to recordings", "style": "auditory"},
                    {"text": "Take breaks and move around", "style": "kinesthetic"}
                ]
            },
            {
                "id": 4,
                "question": "In a classroom, I learn best when:",
                "options": [
                    {"text": "The teacher uses visual aids and diagrams", "style": "visual"},
                    {"text": "The teacher explains things clearly and discusses", "style": "auditory"},
                    {"text": "I can participate in activities and experiments", "style": "kinesthetic"}
                ]
            },
            {
                "id": 5,
                "question": "When solving problems, I typically:",
                "options": [
                    {"text": "Draw diagrams or write out the problem", "style": "visual"},
                    {"text": "Talk through the problem step by step", "style": "auditory"},
                    {"text": "Try different approaches until one works", "style": "kinesthetic"}
                ]
            }
        ]
        
        return render_template('gcse/techniques/learning_style_quiz.html',
                             quiz_questions=quiz_questions)
    
    except Exception as e:
        flash('Error loading learning style quiz.', 'error')
        return redirect(url_for('gcse_techniques.techniques_dashboard'))

@gcse_techniques.route('/learning-style-quiz/result', methods=['POST'])
@login_required
def learning_style_result():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        responses = []
        for i in range(1, 6):  
            response = request.form.get(f'question_{i}')
            if response:
                responses.append(response)
        
        if len(responses) != 5:
            flash('Please answer all questions.', 'error')
            return redirect(url_for('gcse_techniques.learning_style_quiz'))
        
        
        style_scores = {"visual": 0, "auditory": 0, "kinesthetic": 0}
        for response in responses:
            style_scores[response] += 1
        
        
        primary_style = max(style_scores, key=style_scores.get)
        
        
        if primary_style == "visual":
            recommended_techniques = ["Mind Mapping", "Visual Notes", "Diagrams", "Color Coding"]
            description = "You learn best through visual aids, diagrams, and spatial representations."
        elif primary_style == "auditory":
            recommended_techniques = ["Study Groups", "Recorded Notes", "Verbal Repetition", "Discussion"]
            description = "You learn best through listening, speaking, and auditory processing."
        else:  
            recommended_techniques = ["Hands-on Practice", "Movement-based Learning", "Experiments", "Role Playing"]
            description = "You learn best through physical activities, hands-on experiences, and movement."
        
        
        matching_techniques = GCSEStudyTechnique.get_all_techniques()
        
        filtered_techniques = []
        for technique in matching_techniques:
            if (primary_style == "visual" and technique.category in ["understanding"]) or \
               (primary_style == "auditory" and technique.category in ["memorization"]) or \
               (primary_style == "kinesthetic" and technique.category in ["practice"]):
                filtered_techniques.append(technique)
        
        return render_template('gcse/techniques/learning_style_result.html',
                             primary_style=primary_style,
                             style_scores=style_scores,
                             description=description,
                             recommended_techniques=recommended_techniques,
                             matching_techniques=filtered_techniques[:4])
    
    except Exception as e:
        flash('Error processing learning style quiz.', 'error')
        return redirect(url_for('gcse_techniques.learning_style_quiz'))


@gcse_techniques.route('/api/techniques')
@login_required
def api_get_techniques():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        category = request.args.get('category')
        subject = request.args.get('subject')
        difficulty = request.args.get('difficulty')
        
        
        techniques = GCSEStudyTechnique.get_all_techniques(category, subject, difficulty)
        
        
        techniques_data = []
        for technique in techniques:
            techniques_data.append({
                'id': technique.id,
                'technique_name': technique.technique_name,
                'category': technique.category,
                'subject_applicability': technique.subject_applicability,
                'difficulty_level': technique.difficulty_level,
                'time_required': technique.time_required,
                'effectiveness_rating': technique.effectiveness_rating,
                'description': technique.description
            })
        
        return jsonify({
            'success': True,
            'techniques': techniques_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_techniques.route('/api/strategies')
@login_required
def api_get_strategies():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        strategy_type = request.args.get('strategy_type')
        exam_type = request.args.get('exam_type')
        subject = request.args.get('subject')
        
        
        strategies = GCSEExamStrategy.get_strategies_by_type(strategy_type, exam_type, subject)
        
        
        strategies_data = []
        for strategy in strategies:
            strategies_data.append({
                'id': strategy.id,
                'strategy_name': strategy.strategy_name,
                'exam_type': strategy.exam_type,
                'subject_applicability': strategy.subject_applicability,
                'strategy_type': strategy.strategy_type,
                'description': strategy.description
            })
        
        return jsonify({
            'success': True,
            'strategies': strategies_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_techniques.route('/api/generate-plan', methods=['POST'])
@login_required
def api_generate_study_plan():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        subject_id = data.get('subject_id')
        exam_date_str = data.get('exam_date')
        study_hours_per_week = data.get('study_hours_per_week', 5)
        learning_style = data.get('learning_style', 'mixed')
        weak_areas = data.get('weak_areas', [])
        
        if not all([subject_id, exam_date_str]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid exam date format'}), 400
        
        
        study_plan = GCSEStudyPlanGenerator.generate_study_plan(
            user.id, subject_id, exam_date, study_hours_per_week, learning_style, weak_areas
        )
        
        return jsonify({
            'success': True,
            'study_plan': study_plan
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


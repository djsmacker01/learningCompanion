

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.gcse_curriculum import GCSESubject, GCSETopic, GCSESpecification, GCSEExam
from app.models import Topic, get_supabase_client
from app.routes.topics import get_current_user
from datetime import datetime, date, timedelta
import json

gcse = Blueprint('gcse', __name__, url_prefix='/gcse')

@gcse.route('/')
@login_required
def gcse_dashboard():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subjects = GCSESubject.get_all_subjects()
        
        
        upcoming_exams = GCSEExam.get_upcoming_exams(user.id, days_ahead=365)
        
        
        exam_countdowns = []
        for exam in upcoming_exams:
            if exam.exam_date:
                exam_date = datetime.strptime(exam.exam_date, '%Y-%m-%d').date() if isinstance(exam.exam_date, str) else exam.exam_date
                countdown = GCSEExam.get_exam_countdown(exam_date)
                exam_countdowns.append({
                    'exam': exam,
                    'countdown': countdown
                })
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/dashboard.html',
                             subjects=subjects,
                             upcoming_exams=upcoming_exams,
                             exam_countdowns=exam_countdowns,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading GCSE dashboard.', 'error')
        return redirect(url_for('main.dashboard'))

@gcse.route('/subjects')
@login_required
def subjects_list():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        subjects = GCSESubject.get_all_subjects()
        exam_boards = GCSESpecification.get_exam_boards()
        
        return render_template('gcse/subjects.html',
                             subjects=subjects,
                             exam_boards=exam_boards)
    
    except Exception as e:
        flash('Error loading GCSE subjects.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse.route('/subjects/<subject_id>')
@login_required
def subject_detail(subject_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        subject = GCSESubject.get_subject_by_id(subject_id)
        if not subject:
            flash('GCSE subject not found.', 'error')
            return redirect(url_for('gcse.subjects_list'))
        
        
        specifications = GCSESpecification.get_subject_specifications(subject.subject_name)
        
        
        grade_boundaries = GCSESpecification.get_grade_boundaries(subject.exam_board, subject.specification_code)
        
        
        existing_topic = Topic.get_topic_by_gcse_subject(user.id, subject_id)
        
        return render_template('gcse/subject_detail.html',
                             subject=subject,
                             specifications=specifications,
                             grade_boundaries=grade_boundaries,
                             existing_topic=existing_topic)
    
    except Exception as e:
        flash('Error loading subject details.', 'error')
        return redirect(url_for('gcse.subjects_list'))

@gcse.route('/subjects/<subject_id>/create-topic', methods=['POST'])
@login_required
def create_subject_topic(subject_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        subject = GCSESubject.get_subject_by_id(subject_id)
        if not subject:
            flash('GCSE subject not found.', 'error')
            return redirect(url_for('gcse.subjects_list'))
        
        
        topic = Topic.create_topic(
            user_id=user.id,
            title=f"{subject.subject_name} ({subject.exam_board})",
            description=f"GCSE {subject.subject_name} revision for {subject.exam_board} specification {subject.specification_code}",
            is_gcse=True,
            gcse_subject_id=subject_id,
            gcse_exam_board=subject.exam_board,
            gcse_specification_code=subject.specification_code
        )
        
        if topic:
            
            for gcse_topic in subject.topics:
                Topic.create_topic(
                    user_id=user.id,
                    title=gcse_topic.topic_name,
                    description=gcse_topic.topic_description,
                    parent_topic_id=topic.id,
                    is_gcse=True,
                    gcse_topic_id=gcse_topic.id,
                    exam_weight=gcse_topic.exam_weight
                )
            
            flash(f'GCSE {subject.subject_name} topic created successfully!', 'success')
            return redirect(url_for('topics.topic_detail', topic_id=topic.id))
        else:
            flash('Error creating GCSE topic.', 'error')
            return redirect(url_for('gcse.subject_detail', subject_id=subject_id))
    
    except Exception as e:
        flash('Error creating GCSE topic.', 'error')
        return redirect(url_for('gcse.subject_detail', subject_id=subject_id))

@gcse.route('/exams')
@login_required
def exams_list():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        upcoming_exams = GCSEExam.get_upcoming_exams(user.id, days_ahead=365)
        
        
        exams_by_subject = {}
        for exam in upcoming_exams:
            subject_id = exam.subject_id
            if subject_id not in exams_by_subject:
                exams_by_subject[subject_id] = []
            
            
            if exam.exam_date:
                exam_date = datetime.strptime(exam.exam_date, '%Y-%m-%d').date() if isinstance(exam.exam_date, str) else exam.exam_date
                countdown = GCSEExam.get_exam_countdown(exam_date)
                exam.countdown = countdown
            
            exams_by_subject[subject_id].append(exam)
        
        return render_template('gcse/exams.html',
                             exams_by_subject=exams_by_subject,
                             total_exams=len(upcoming_exams))
    
    except Exception as e:
        flash('Error loading GCSE exams.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse.route('/exams/create', methods=['GET', 'POST'])
@login_required
def create_exam():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            subject_id = request.form.get('subject_id')
            exam_name = request.form.get('exam_name')
            exam_date_str = request.form.get('exam_date')
            paper_number = request.form.get('paper_number', type=int)
            duration_minutes = request.form.get('duration_minutes', type=int)
            total_marks = request.form.get('total_marks', type=int)
            exam_board = request.form.get('exam_board')
            specification_code = request.form.get('specification_code')
            
            if not all([subject_id, exam_name, exam_date_str]):
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('gcse.create_exam'))
            
            try:
                exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid exam date format.', 'error')
                return redirect(url_for('gcse.create_exam'))
            
            exam = GCSEExam.create_exam(
                subject_id=subject_id,
                exam_name=exam_name,
                exam_date=exam_date,
                paper_number=paper_number,
                duration_minutes=duration_minutes,
                total_marks=total_marks,
                exam_board=exam_board,
                specification_code=specification_code
            )
            
            if exam:
                flash('GCSE exam created successfully!', 'success')
                return redirect(url_for('gcse.exams_list'))
            else:
                flash('Error creating GCSE exam.', 'error')
        
        
        subjects = GCSESubject.get_all_subjects()
        exam_boards = GCSESpecification.get_exam_boards()
        
        return render_template('gcse/create_exam.html',
                             subjects=subjects,
                             exam_boards=exam_boards)
    
    except Exception as e:
        flash('Error loading exam creation page.', 'error')
        return redirect(url_for('gcse.exams_list'))

@gcse.route('/revision-schedule')
@login_required
def revision_schedule():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        upcoming_exams = GCSEExam.get_upcoming_exams(user.id, days_ahead=90)
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        revision_plan = []
        for exam in upcoming_exams:
            if exam.exam_date:
                exam_date = datetime.strptime(exam.exam_date, '%Y-%m-%d').date() if isinstance(exam.exam_date, str) else exam.exam_date
                days_until = (exam_date - date.today()).days
                
                if days_until > 0:
                    
                    matching_topic = None
                    for topic in user_gcse_topics:
                        if topic.gcse_subject_id == exam.subject_id:
                            matching_topic = topic
                            break
                    
                    if matching_topic:
                        
                        if days_until <= 7:
                            intensity = "intensive"
                            sessions_per_week = 7
                        elif days_until <= 30:
                            intensity = "moderate"
                            sessions_per_week = 5
                        else:
                            intensity = "light"
                            sessions_per_week = 3
                        
                        revision_plan.append({
                            'exam': exam,
                            'topic': matching_topic,
                            'days_until': days_until,
                            'intensity': intensity,
                            'sessions_per_week': sessions_per_week,
                            'recommended_session_length': 45 if intensity == "intensive" else 60
                        })
        
        
        revision_plan.sort(key=lambda x: x['days_until'])
        
        return render_template('gcse/revision_schedule.html',
                             revision_plan=revision_plan,
                             total_exams=len(upcoming_exams))
    
    except Exception as e:
        flash('Error loading revision schedule.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse.route('/grade-calculator')
@login_required
def grade_calculator():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        subjects = GCSESubject.get_all_subjects()
        subject_map = {subject.id: subject for subject in subjects}
        
        topic_performance = []
        for topic in user_gcse_topics:
            if topic.gcse_subject_id in subject_map:
                subject = subject_map[topic.gcse_subject_id]
                
                
                grade_boundaries = GCSESpecification.get_grade_boundaries(
                    subject.exam_board, subject.specification_code
                )
                
                
                
                predicted_grade = "TBD"  
                
                topic_performance.append({
                    'topic': topic,
                    'subject': subject,
                    'grade_boundaries': grade_boundaries,
                    'predicted_grade': predicted_grade
                })
        
        return render_template('gcse/grade_calculator.html',
                             topic_performance=topic_performance)
    
    except Exception as e:
        flash('Error loading grade calculator.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))


@gcse.route('/api/subjects/<subject_id>/topics')
@login_required
def api_get_subject_topics(subject_id):
    
    try:
        subject = GCSESubject.get_subject_by_id(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        topics_data = []
        for topic in subject.topics:
            topics_data.append({
                'id': topic.id,
                'name': topic.topic_name,
                'description': topic.topic_description,
                'exam_weight': topic.exam_weight,
                'difficulty_level': topic.difficulty_level,
                'learning_objectives': topic.learning_objectives
            })
        
        return jsonify({
            'subject': {
                'id': subject.id,
                'name': subject.subject_name,
                'exam_board': subject.exam_board,
                'specification_code': subject.specification_code
            },
            'topics': topics_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse.route('/api/exams/upcoming')
@login_required
def api_upcoming_exams():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        upcoming_exams = GCSEExam.get_upcoming_exams(user.id, days_ahead=365)
        
        exams_data = []
        for exam in upcoming_exams:
            if exam.exam_date:
                exam_date = datetime.strptime(exam.exam_date, '%Y-%m-%d').date() if isinstance(exam.exam_date, str) else exam.exam_date
                countdown = GCSEExam.get_exam_countdown(exam_date)
                
                exams_data.append({
                    'id': exam.id,
                    'exam_name': exam.exam_name,
                    'exam_date': exam.exam_date,
                    'paper_number': exam.paper_number,
                    'duration_minutes': exam.duration_minutes,
                    'total_marks': exam.total_marks,
                    'exam_board': exam.exam_board,
                    'countdown': countdown
                })
        
        return jsonify({'exams': exams_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse.route('/api/grade-boundaries/<exam_board>/<subject_code>')
@login_required
def api_grade_boundaries(exam_board, subject_code):
    
    try:
        grade_boundaries = GCSESpecification.get_grade_boundaries(exam_board, subject_code)
        return jsonify({
            'exam_board': exam_board,
            'subject_code': subject_code,
            'boundaries': grade_boundaries
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


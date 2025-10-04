

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.gcse_exam_scheduling import (
    GCSEExamSchedule, GCSERevisionSchedule, GCSERevisionPlanner, 
    GCSEStudyReminder
)
from app.models.gcse_curriculum import GCSESubject
from app.models import Topic
from app.routes.topics import get_current_user
from datetime import datetime, date, timedelta
import json

gcse_scheduling = Blueprint('gcse_scheduling', __name__, url_prefix='/gcse/scheduling')

@gcse_scheduling.route('/')
@login_required
def scheduling_dashboard():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        exam_schedules = GCSEExamSchedule.get_user_exam_schedules(user.id, days_ahead=365)
        
        
        exam_countdowns = []
        for exam in exam_schedules:
            if exam.exam_date:
                exam_date = datetime.strptime(exam.exam_date, '%Y-%m-%d').date() if isinstance(exam.exam_date, str) else exam.exam_date
                countdown = GCSEExamSchedule.get_exam_countdown(exam_date)
                exam_countdowns.append({
                    'exam': exam,
                    'countdown': countdown
                })
        
        
        exam_countdowns.sort(key=lambda x: x['countdown']['days'] if x['countdown']['status'] != 'past' else 9999)
        
        
        today_schedule = GCSERevisionPlanner.get_daily_revision_schedule(user.id, date.today())
        
        
        upcoming_revisions = GCSERevisionSchedule.get_user_revision_schedule(user.id, days_ahead=7)
        
        
        study_reminders = GCSEStudyReminder.get_user_reminders(user.id, days_ahead=7)
        
        return render_template('gcse/scheduling/dashboard.html',
                             exam_countdowns=exam_countdowns,
                             today_schedule=today_schedule,
                             upcoming_revisions=upcoming_revisions,
                             study_reminders=study_reminders)
    
    except Exception as e:
        flash('Error loading scheduling dashboard.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_scheduling.route('/exams')
@login_required
def exam_schedules():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        exam_schedules = GCSEExamSchedule.get_user_exam_schedules(user.id, days_ahead=365)
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/scheduling/exam_schedules.html',
                             exam_schedules=exam_schedules,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading exam schedules.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_scheduling.route('/exams/create', methods=['GET', 'POST'])
@login_required
def create_exam_schedule():
    
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
            exam_board = request.form.get('exam_board')
            specification_code = request.form.get('specification_code')
            
            if not all([subject_id, exam_name, exam_date_str]):
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('gcse_scheduling.create_exam_schedule'))
            
            try:
                exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid exam date format.', 'error')
                return redirect(url_for('gcse_scheduling.create_exam_schedule'))
            
            exam_schedule = GCSEExamSchedule.create_exam_schedule(
                user_id=user.id,
                subject_id=subject_id,
                exam_name=exam_name,
                exam_date=exam_date,
                paper_number=paper_number,
                duration_minutes=duration_minutes,
                exam_board=exam_board,
                specification_code=specification_code
            )
            
            if exam_schedule:
                
                reminders = GCSEStudyReminder.create_exam_countdown_reminders(user.id, [exam_schedule])
                
                flash(f'Exam schedule created successfully! {len(reminders)} reminders added.', 'success')
                return redirect(url_for('gcse_scheduling.exam_schedules'))
            else:
                flash('Error creating exam schedule.', 'error')
        
        
        subjects = GCSESubject.get_all_subjects()
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/scheduling/create_exam_schedule.html',
                             subjects=subjects,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading exam schedule creation page.', 'error')
        return redirect(url_for('gcse_scheduling.exam_schedules'))

@gcse_scheduling.route('/revision')
@login_required
def revision_schedule():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        exam_schedules = GCSEExamSchedule.get_user_exam_schedules(user.id, days_ahead=180)
        
        
        revision_schedule = GCSERevisionSchedule.get_user_revision_schedule(user.id, days_ahead=30)
        
        
        revisions_by_date = {}
        for revision in revision_schedule:
            revision_date = revision.revision_date
            if isinstance(revision_date, str):
                revision_date = datetime.strptime(revision_date, '%Y-%m-%d').date()
            
            if revision_date not in revisions_by_date:
                revisions_by_date[revision_date] = []
            revisions_by_date[revision_date].append(revision)
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/scheduling/revision_schedule.html',
                             exam_schedules=exam_schedules,
                             revisions_by_date=revisions_by_date,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading revision schedule.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_scheduling.route('/revision/generate', methods=['POST'])
@login_required
def generate_revision_plan():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        subject_id = request.form.get('subject_id')
        exam_date_str = request.form.get('exam_date')
        study_hours_per_week = request.form.get('study_hours_per_week', 5, type=int)
        
        if not all([subject_id, exam_date_str]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('gcse_scheduling.revision_schedule'))
        
        try:
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid exam date format.', 'error')
            return redirect(url_for('gcse_scheduling.revision_schedule'))
        
        
        revision_phases = GCSERevisionPlanner.generate_smart_revision_plan(
            user.id, subject_id, exam_date, study_hours_per_week
        )
        
        
        scheduled_sessions = GCSERevisionPlanner.schedule_revision_sessions(
            user.id, subject_id, exam_date, study_hours_per_week
        )
        
        flash(f'Revision plan generated successfully! {len(scheduled_sessions)} sessions scheduled.', 'success')
        return redirect(url_for('gcse_scheduling.revision_schedule'))
    
    except Exception as e:
        flash('Error generating revision plan.', 'error')
        return redirect(url_for('gcse_scheduling.revision_schedule'))

@gcse_scheduling.route('/daily/<date_str>')
@login_required
def daily_schedule(date_str):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'error')
            return redirect(url_for('gcse_scheduling.scheduling_dashboard'))
        
        
        daily_schedule = GCSERevisionPlanner.get_daily_revision_schedule(user.id, target_date)
        
        
        prev_date = target_date - timedelta(days=1)
        next_date = target_date + timedelta(days=1)
        
        return render_template('gcse/scheduling/daily_schedule.html',
                             daily_schedule=daily_schedule,
                             target_date=target_date,
                             prev_date=prev_date,
                             next_date=next_date)
    
    except Exception as e:
        flash('Error loading daily schedule.', 'error')
        return redirect(url_for('gcse_scheduling.scheduling_dashboard'))

@gcse_scheduling.route('/reminders')
@login_required
def study_reminders():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        study_reminders = GCSEStudyReminder.get_user_reminders(user.id, days_ahead=30)
        
        
        reminders_by_date = {}
        for reminder in study_reminders:
            reminder_date = reminder.reminder_date
            if isinstance(reminder_date, str):
                reminder_date = datetime.strptime(reminder_date, '%Y-%m-%d').date()
            
            if reminder_date not in reminders_by_date:
                reminders_by_date[reminder_date] = []
            reminders_by_date[reminder_date].append(reminder)
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/scheduling/study_reminders.html',
                             reminders_by_date=reminders_by_date,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading study reminders.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_scheduling.route('/reminders/create', methods=['POST'])
@login_required
def create_study_reminder():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        reminder_type = request.form.get('reminder_type')
        subject_id = request.form.get('subject_id')
        reminder_date_str = request.form.get('reminder_date')
        reminder_time = request.form.get('reminder_time')
        message = request.form.get('message')
        
        if not all([reminder_type, subject_id, reminder_date_str, reminder_time, message]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('gcse_scheduling.study_reminders'))
        
        try:
            reminder_date = datetime.strptime(reminder_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid reminder date format.', 'error')
            return redirect(url_for('gcse_scheduling.study_reminders'))
        
        reminder = GCSEStudyReminder.create_reminder(
            user_id=user.id,
            reminder_type=reminder_type,
            subject_id=subject_id,
            reminder_date=reminder_date,
            reminder_time=reminder_time,
            message=message
        )
        
        if reminder:
            flash('Study reminder created successfully!', 'success')
        else:
            flash('Error creating study reminder.', 'error')
        
        return redirect(url_for('gcse_scheduling.study_reminders'))
    
    except Exception as e:
        flash('Error creating study reminder.', 'error')
        return redirect(url_for('gcse_scheduling.study_reminders'))


@gcse_scheduling.route('/api/countdown/<exam_id>')
@login_required
def api_exam_countdown(exam_id):
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        exam_schedules = GCSEExamSchedule.get_user_exam_schedules(user.id, days_ahead=365)
        exam = next((e for e in exam_schedules if e.id == exam_id), None)
        
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if exam.exam_date:
            exam_date = datetime.strptime(exam.exam_date, '%Y-%m-%d').date() if isinstance(exam.exam_date, str) else exam.exam_date
            countdown = GCSEExamSchedule.get_exam_countdown(exam_date)
            
            return jsonify({
                'success': True,
                'exam_id': exam_id,
                'exam_name': exam.exam_name,
                'exam_date': exam.exam_date,
                'countdown': countdown
            })
        
        return jsonify({'error': 'Invalid exam date'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_scheduling.route('/api/daily-schedule/<date_str>')
@login_required
def api_daily_schedule(date_str):
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        
        daily_schedule = GCSERevisionPlanner.get_daily_revision_schedule(user.id, target_date)
        
        return jsonify({
            'success': True,
            'daily_schedule': daily_schedule
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_scheduling.route('/api/generate-plan', methods=['POST'])
@login_required
def api_generate_revision_plan():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        subject_id = data.get('subject_id')
        exam_date_str = data.get('exam_date')
        study_hours_per_week = data.get('study_hours_per_week', 5)
        
        if not all([subject_id, exam_date_str]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid exam date format'}), 400
        
        
        phases = GCSERevisionPlanner.generate_smart_revision_plan(
            user.id, subject_id, exam_date, study_hours_per_week
        )
        
        return jsonify({
            'success': True,
            'phases': phases
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


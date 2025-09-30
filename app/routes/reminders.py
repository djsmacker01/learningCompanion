"""
Routes for Study Reminders and Scheduling System
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, make_response
from flask_login import login_required
from datetime import datetime, timedelta
import uuid
from app.models.reminders import (
    StudyReminderPreferences, StudyReminder, StudySchedule, 
    OptimalStudyTime, StudyPattern
)
from app.utils.smart_scheduling import SmartSchedulingEngine
from app.utils.calendar_integration import GoogleCalendarIntegration, CalendarWidget
from app.utils.reminder_delivery import ReminderScheduler
from app.routes.topics import get_current_user

reminders_bp = Blueprint('reminders', __name__)


@reminders_bp.route('/reminders')
@login_required
def reminders_dashboard():
    """Main reminders dashboard"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Get user's reminder preferences
        preferences = StudyReminderPreferences.get_or_create_preferences(user.id)
        
        # Get upcoming reminders
        upcoming_reminders = StudyReminder.get_user_reminders(
            user.id, 
            status='pending',
            limit=10
        )
        
        # Get upcoming schedules
        upcoming_schedules = StudySchedule.get_user_schedules(
            user.id,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=7)
        )
        
        # Get recent optimal study time suggestions
        optimal_times = OptimalStudyTime.get_user_suggestions(user.id, limit=5)
        
        return render_template('reminders/dashboard.html',
                             preferences=preferences,
                             upcoming_reminders=upcoming_reminders,
                             upcoming_schedules=upcoming_schedules,
                             optimal_times=optimal_times)
        
    except Exception as e:
        print(f"Error loading reminders dashboard: {e}")
        flash('Error loading reminders dashboard', 'error')
        return redirect(url_for('main.dashboard'))


@reminders_bp.route('/reminders/preferences', methods=['GET', 'POST'])
def reminder_preferences():
    """Manage reminder preferences"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('main.dashboard'))
        
        preferences = StudyReminderPreferences.get_or_create_preferences(user.id)
        
        if request.method == 'POST':
            # Update preferences
            preferences.is_enabled = request.form.get('is_enabled') == 'on'
            preferences.reminder_methods = request.form.getlist('reminder_methods')
            preferences.frequency = request.form.get('frequency', 'daily')
            preferences.study_goal_minutes = int(request.form.get('study_goal_minutes', 30))
            preferences.advance_notice_minutes = int(request.form.get('advance_notice_minutes', 15))
            preferences.timezone = request.form.get('timezone', 'UTC')
            
            # Handle days of week
            days_of_week = []
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                if request.form.get(f'day_{day}') == 'on':
                    days_of_week.append(['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(day) + 1)
            preferences.days_of_week = days_of_week
            
            # Handle preferred times
            preferred_times = []
            for time_input in ['morning_time', 'afternoon_time', 'evening_time']:
                time_value = request.form.get(time_input)
                if time_value:
                    preferred_times.append(time_value)
            preferences.preferred_times = preferred_times
            
            # Save preferences
            preferences.save()
            flash('Reminder preferences updated successfully!', 'success')
            return redirect(url_for('reminders.reminder_preferences'))
        
        return render_template('reminders/preferences.html', preferences=preferences)
        
    except Exception as e:
        print(f"Error managing reminder preferences: {e}")
        flash('Error managing reminder preferences. Database tables may not be created yet.', 'error')
        return redirect(url_for('reminders.reminders_dashboard'))


@reminders_bp.route('/reminders/schedule')
def schedule_reminders():
    """Schedule new reminders"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Get user's topics for scheduling
        from app.models import Topic
        topics = Topic.get_all_by_user(user.id)
        
        # Add current datetime for template
        from datetime import datetime, timedelta
        now = datetime.now()
        
        return render_template('reminders/schedule.html', 
                             topics=topics, 
                             now=now,
                             timedelta=timedelta)
        
    except Exception as e:
        print(f"Error loading schedule page: {e}")
        import traceback
        traceback.print_exc()
        flash('Error loading schedule page. Database tables may not be created yet.', 'error')
        return redirect(url_for('reminders.reminders_dashboard'))


@reminders_bp.route('/reminders/schedule', methods=['POST'])
def create_scheduled_reminder():
    """Create a new scheduled reminder"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Get form data
        title = request.form.get('title', 'Study Reminder')
        message = request.form.get('message', 'Time for your study session!')
        scheduled_date = request.form.get('scheduled_date')
        scheduled_time = request.form.get('scheduled_time')
        reminder_type = request.form.get('reminder_type', 'study')
        reminder_method = request.form.get('reminder_method', 'email')
        topic_id = request.form.get('topic_id')
        session_type = request.form.get('session_type', 'review')
        priority = request.form.get('priority', 'medium')
        
        # Parse scheduled time
        scheduled_datetime = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%Y-%m-%d %H:%M")
        
        # Create reminder
        reminder = StudyReminder.create_reminder(
            user_id=mock_user.id,
            title=title,
            scheduled_time=scheduled_datetime,
            message=message,
            reminder_type=reminder_type,
            reminder_method=reminder_method,
            topic_id=topic_id if topic_id else None,
            session_type=session_type,
            priority=priority
        )
        
        if reminder:
            flash('Reminder scheduled successfully!', 'success')
            return jsonify({'success': True, 'message': 'Reminder scheduled successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to schedule reminder'})
        
    except Exception as e:
        print(f"Error creating scheduled reminder: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@reminders_bp.route('/reminders/smart-schedule')
def smart_schedule():
    """Smart scheduling based on AI analysis"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Get smart scheduling suggestions
        scheduling_engine = SmartSchedulingEngine()
        optimal_times = scheduling_engine.suggest_optimal_study_times(user.id, days_ahead=7)
        
        # Get user's topics
        from app.models import Topic
        topics = Topic.get_all_by_user(user.id)
        
        # Get study patterns
        patterns = scheduling_engine.analyze_study_patterns(user.id)
        
        return render_template('reminders/smart_schedule.html',
                             optimal_times=optimal_times,
                             topics=topics,
                             patterns=patterns)
        
    except Exception as e:
        print(f"Error loading smart schedule: {e}")
        flash('Error loading smart schedule. Database tables may not be created yet.', 'error')
        return redirect(url_for('reminders.reminders_dashboard'))


@reminders_bp.route('/reminders/smart-schedule', methods=['POST'])
def create_smart_schedule():
    """Create a smart scheduled session"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Get form data
        topic_id = request.form.get('topic_id')
        session_type = request.form.get('session_type', 'review')
        duration_minutes = int(request.form.get('duration_minutes', 30))
        
        # Create smart schedule
        scheduling_engine = SmartSchedulingEngine()
        schedule = scheduling_engine.schedule_study_session(
            user_id=mock_user.id,
            topic_id=topic_id if topic_id else None,
            session_type=session_type,
            duration_minutes=duration_minutes
        )
        
        if schedule:
            flash('Smart schedule created successfully!', 'success')
            return jsonify({
                'success': True, 
                'message': 'Smart schedule created successfully!',
                'schedule_id': schedule.id,
                'scheduled_time': schedule.scheduled_start.isoformat()
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to create smart schedule'})
        
    except Exception as e:
        print(f"Error creating smart schedule: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@reminders_bp.route('/reminders/accept-suggestion/<suggestion_id>')
def accept_optimal_suggestion(suggestion_id):
    """Accept an optimal study time suggestion"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Get the suggestion
        optimal_times = OptimalStudyTime.get_user_suggestions(user.id, limit=100)
        suggestion = next((s for s in optimal_times if s.id == suggestion_id), None)
        
        if not suggestion:
            flash('Suggestion not found', 'error')
            return redirect(url_for('reminders.smart_schedule'))
        
        # Accept the suggestion
        if suggestion.accept():
            # Create a schedule for this time
            schedule = StudySchedule.create_schedule(
                user_id=mock_user.id,
                title=f"Study Session: {suggestion.session_type.title()}",
                scheduled_start=suggestion.suggested_time,
                scheduled_end=suggestion.suggested_time + timedelta(minutes=30),
                topic_id=suggestion.topic_id,
                session_type=suggestion.session_type,
                description=f"Accepted optimal study time suggestion: {suggestion.reasoning}"
            )
            
            if schedule:
                flash('Optimal study time accepted and scheduled!', 'success')
            else:
                flash('Suggestion accepted but failed to create schedule', 'warning')
        else:
            flash('Failed to accept suggestion', 'error')
        
        return redirect(url_for('reminders.smart_schedule'))
        
    except Exception as e:
        print(f"Error accepting optimal suggestion: {e}")
        flash('Error accepting suggestion', 'error')
        return redirect(url_for('reminders.smart_schedule'))


@reminders_bp.route('/reminders/cancel/<reminder_id>')
def cancel_reminder(reminder_id):
    """Cancel a reminder"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Get the reminder
        reminders = StudyReminder.get_user_reminders(user.id, limit=100)
        reminder = next((r for r in reminders if r.id == reminder_id), None)
        
        if not reminder:
            flash('Reminder not found', 'error')
            return redirect(url_for('reminders.reminders_dashboard'))
        
        # Cancel the reminder
        if reminder.cancel():
            flash('Reminder cancelled successfully!', 'success')
        else:
            flash('Failed to cancel reminder', 'error')
        
        return redirect(url_for('reminders.reminders_dashboard'))
        
    except Exception as e:
        print(f"Error cancelling reminder: {e}")
        flash('Error cancelling reminder', 'error')
        return redirect(url_for('reminders.reminders_dashboard'))


# API Routes
@reminders_bp.route('/api/reminders/process')
def process_reminders_api():
    """API endpoint to process pending reminders"""
    try:
        scheduler = ReminderScheduler()
        results = scheduler.process_pending_reminders()
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        print(f"Error processing reminders: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        })


@reminders_bp.route('/api/reminders/patterns/<user_id>')
def get_study_patterns_api(user_id):
    """API endpoint to get study patterns"""
    try:
        scheduling_engine = SmartSchedulingEngine()
        patterns = scheduling_engine.analyze_study_patterns(user_id)
        
        return jsonify({
            'success': True,
            'patterns': patterns
        })
        
    except Exception as e:
        print(f"Error getting study patterns: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        })


@reminders_bp.route('/api/reminders/optimal-times/<user_id>')
def get_optimal_times_api(user_id):
    """API endpoint to get optimal study times"""
    try:
        scheduling_engine = SmartSchedulingEngine()
        optimal_times = scheduling_engine.suggest_optimal_study_times(user_id, days_ahead=7)
        
        # Convert to JSON-serializable format
        times_data = []
        for time_suggestion in optimal_times:
            times_data.append({
                'id': time_suggestion.id,
                'suggested_time': time_suggestion.suggested_time.isoformat(),
                'confidence_score': time_suggestion.confidence_score,
                'reasoning': time_suggestion.reasoning,
                'factors': time_suggestion.factors,
                'topic_id': time_suggestion.topic_id,
                'session_type': time_suggestion.session_type,
                'is_accepted': time_suggestion.is_accepted
            })
        
        return jsonify({
            'success': True,
            'optimal_times': times_data
        })
        
    except Exception as e:
        print(f"Error getting optimal study times: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        })


@reminders_bp.route('/api/reminders/create-daily/<user_id>')
def create_daily_reminders_api(user_id):
    """API endpoint to create daily reminders"""
    try:
        scheduler = ReminderScheduler()
        reminders = scheduler.create_daily_reminders(user_id)
        
        return jsonify({
            'success': True,
            'reminders_created': len(reminders),
            'reminder_ids': [r.id for r in reminders]
        })
        
    except Exception as e:
        print(f"Error creating daily reminders: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        })


@reminders_bp.route('/reminders/export/ical')
@login_required
def export_schedule_ical():
    """Export study schedule as iCal file"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('reminders.reminders_dashboard'))
        
        # Get user's study schedules
        schedules = StudySchedule.get_user_schedules(user.id)
        
        # Generate iCal content
        ical_content = generate_ical_content(schedules, user.id)
        
        # Create response
        response = make_response(ical_content)
        response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=study_schedule_{datetime.now().strftime("%Y%m%d_%H%M%S")}.ics'
        
        return response
    
    except Exception as e:
        flash('Error exporting schedule. Please try again.', 'error')
        return redirect(url_for('reminders.reminders_dashboard'))


def generate_ical_content(schedules, user_id):
    """Generate iCal content from study schedules"""
    ical_lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Learning Companion//Study Schedule//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH'
    ]
    
    for schedule in schedules:
        # Format dates for iCal
        start_dt = schedule.scheduled_start.strftime('%Y%m%dT%H%M%SZ')
        end_dt = schedule.scheduled_end.strftime('%Y%m%dT%H%M%SZ')
        created_dt = schedule.created_at.strftime('%Y%m%dT%H%M%SZ') if schedule.created_at else datetime.now().strftime('%Y%m%dT%H%M%SZ')
        
        # Generate unique ID
        uid = f"{schedule.id}@learningcompanion.app"
        
        ical_lines.extend([
            'BEGIN:VEVENT',
            f'UID:{uid}',
            f'DTSTART:{start_dt}',
            f'DTEND:{end_dt}',
            f'DTSTAMP:{created_dt}',
            f'SUMMARY:{schedule.title}',
            f'DESCRIPTION:{schedule.description or "Study session"}',
            f'STATUS:CONFIRMED',
            f'SEQUENCE:0',
            'END:VEVENT'
        ])
    
    ical_lines.append('END:VCALENDAR')
    
    return '\r\n'.join(ical_lines)


@reminders_bp.route('/reminders/google-calendar/auth')
@login_required
def google_calendar_auth():
    """Initiate Google Calendar OAuth flow"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('reminders.reminders_dashboard'))
        
        # Generate state for security
        state = str(uuid.uuid4())
        
        # Store state in session (in production, use proper session storage)
        # For now, we'll skip state validation
        
        # Get Google Calendar integration
        gcal = GoogleCalendarIntegration()
        auth_url = gcal.get_auth_url(state=state)
        
        return redirect(auth_url)
    
    except Exception as e:
        flash('Error initiating Google Calendar authentication.', 'error')
        return redirect(url_for('reminders.reminders_dashboard'))


@reminders_bp.route('/reminders/google-calendar/callback')
@login_required
def google_calendar_callback():
    """Handle Google Calendar OAuth callback"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        
        if not code:
            flash('Authorization failed. Please try again.', 'error')
            return redirect(url_for('reminders.reminders_dashboard'))
        
        # Exchange code for tokens
        gcal = GoogleCalendarIntegration()
        token_data = gcal.exchange_code_for_token(code)
        
        if 'error' in token_data:
            flash(f'Authentication failed: {token_data.get("error_description", "Unknown error")}', 'error')
            return redirect(url_for('reminders.reminders_dashboard'))
        
        # Store tokens (in production, store in database)
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        
        # Get user's study schedules
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        schedules = StudySchedule.get_user_schedules(user.id)
        
        # Sync schedules to Google Calendar
        created_events = gcal.sync_study_schedule(access_token, schedules)
        
        flash(f'Successfully synced {len(created_events)} study sessions to Google Calendar!', 'success')
        return redirect(url_for('reminders.reminders_dashboard'))
    
    except Exception as e:
        flash('Error syncing with Google Calendar.', 'error')
        return redirect(url_for('reminders.reminders_dashboard'))


@reminders_bp.route('/reminders/calendar-widget')
@login_required
def calendar_widget():
    """Get calendar widget data"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get study schedules for current month
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = datetime(now.year, now.month + 1, 1) - timedelta(days=1)
        
        schedules = StudySchedule.get_user_schedules(
            user.id, 
            start_date=start_of_month, 
            end_date=end_of_month
        )
        
        # Convert to calendar widget format
        events = []
        for schedule in schedules:
            events.append({
                'id': schedule.id,
                'title': schedule.title,
                'start': {
                    'dateTime': schedule.scheduled_start.isoformat()
                },
                'end': {
                    'dateTime': schedule.scheduled_end.isoformat()
                },
                'description': schedule.description
            })
        
        # Generate calendar HTML
        calendar_html = CalendarWidget.generate_calendar_html(events, now.month, now.year)
        
        return jsonify({
            'calendar_html': calendar_html,
            'events': events,
            'month': now.month,
            'year': now.year
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

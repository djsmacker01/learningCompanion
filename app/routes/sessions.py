from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify, make_response
from flask_login import current_user, login_required
from app.models import Topic, User
from app.models.study_session import StudySession
from app.forms.session_forms import StartSessionForm, CompleteSessionForm, EditSessionForm, SessionFilterForm
from app.models.gamification import GamificationEngine
from datetime import datetime, date, timedelta
import csv
import io
import json

sessions = Blueprint('sessions', __name__)


from app.routes.topics import get_current_user

@sessions.route('/sessions/debug')
@login_required
def debug_sessions():
    
    try:
        
        from app.models.study_session import _in_memory_sessions, _next_session_id
        print(f"In-memory sessions: {len(_in_memory_sessions)}")
        print(f"Next session ID: {_next_session_id}")
        for session in _in_memory_sessions:
            print(f"Session {session.id}: {session.session_type} for user {session.user_id}")
        
        
        user = get_current_user()
        if not user:
            return "User not authenticated"
        
        user_sessions = StudySession.get_user_sessions(user.id)
        print(f"User sessions found: {len(user_sessions)}")
        
        return f"Debug info: {len(_in_memory_sessions)} sessions in memory, {len(user_sessions)} user sessions"
    except Exception as e:
        return f"Debug error: {e}"

@sessions.route('/sessions')
@login_required
def session_history():
    
    try:
        
        topic_id = request.args.get('topic_id', type=str)
        session_type = request.args.get('session_type', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        all_sessions = StudySession.get_user_sessions(user.id)
        
        
        filtered_sessions = all_sessions
        if topic_id:
            filtered_sessions = [s for s in filtered_sessions if s.topic_id == topic_id]
        if session_type:
            filtered_sessions = [s for s in filtered_sessions if s.session_type == session_type]
        if date_from:
            try:
                from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                filtered_sessions = [s for s in filtered_sessions if s.session_date.date() >= from_date]
            except ValueError:
                pass
        if date_to:
            try:
                to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                filtered_sessions = [s for s in filtered_sessions if s.session_date.date() <= to_date]
            except ValueError:
                pass
        
        
        total_sessions = len(filtered_sessions)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        sessions_page = filtered_sessions[start_idx:end_idx]
        
        
        topics = Topic.get_all_by_user(user.id)
        
        
        filter_form = SessionFilterForm(topics=topics)
        filter_form.topic_id.data = topic_id
        filter_form.session_type.data = session_type
        filter_form.date_from.data = datetime.strptime(date_from, '%Y-%m-%d').date() if date_from else None
        filter_form.date_to.data = datetime.strptime(date_to, '%Y-%m-%d').date() if date_to else None
        
        
        try:
            stats = StudySession.get_session_stats(user.id, days=30)
        except Exception as e:
            print(f"Error getting session stats: {e}")
            stats = {'total_sessions': 0, 'total_time_minutes': 0, 'total_time_hours': 0, 'confidence_improvement': 0, 'last_session_date': None, 'avg_session_duration': 0, 'completion_rate': 0}
        
        try:
            streak = StudySession.get_session_streak(user.id)
        except Exception as e:
            print(f"Error getting session streak: {e}")
            streak = 0
        
        try:
            weekly_time = StudySession.get_weekly_study_time(user.id)
        except Exception as e:
            print(f"Error getting weekly study time: {e}")
            weekly_time = 0
        
        
        has_prev = page > 1
        has_next = end_idx < total_sessions
        prev_page = page - 1 if has_prev else None
        next_page = page + 1 if has_next else None
        
        return render_template('sessions/history.html', 
                             sessions=sessions_page,
                             filter_form=filter_form,
                             stats=stats,
                             streak=streak,
                             weekly_time=weekly_time,
                             page=page,
                             has_prev=has_prev,
                             has_next=has_next,
                             prev_page=prev_page,
                             next_page=next_page,
                             total_sessions=total_sessions)
    
    except Exception as e:
        flash('Error loading session history. Please try again.', 'error')
        
        try:
            topics = Topic.get_all_by_user(user.id)
            filter_form = SessionFilterForm(topics=topics)
        except:
            filter_form = SessionFilterForm()
        return render_template('sessions/history.html', 
                             sessions=[], 
                             filter_form=filter_form,
                             stats={}, 
                             streak=0, 
                             weekly_time=0,
                             total_sessions=0)

@sessions.route('/sessions/start', methods=['GET', 'POST'])
def start_session():
    
    try:
        
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        print(f"Getting topics for user: {user.id}")
        topics = Topic.get_all_by_user(user.id)
        print(f"Found {len(topics)} topics for user")
        if not topics:
            print("No topics found, redirecting to create topic")
            flash('You need to create a topic before starting a study session.', 'warning')
            return redirect(url_for('topics.create_topic'))
        
        form = StartSessionForm(topics=topics)
        
        
        ai_recommendations = []
        try:
            from app.utils.ai_algorithms import LearningAnalytics
            ai_recommendations = LearningAnalytics.get_learning_recommendations(user.id)
        except Exception as e:
            print(f"Error getting AI recommendations: {e}")
        
        print(f"Form validation: {form.validate_on_submit()}")
        if form.errors:
            print(f"Form errors: {form.errors}")
        
        if form.validate_on_submit():
            print(f"Creating session for user: {user.id}, topic: {form.topic_id.data}")
            print(f"Form data: {form.data}")
            
            session = StudySession.create_session(
                user_id=user.id,
                topic_id=form.topic_id.data,
                session_date=datetime.now(),
                duration_minutes=form.estimated_duration.data or 25,
                confidence_before=form.confidence_before.data,
                confidence_after=form.confidence_before.data,  
                notes=form.notes.data or '',
                session_type=form.session_type.data,
                completed=False
            )
            
            print(f"Created session: {session}")
            if session:
                print(f"Session created successfully with ID: {session.id}")
                flash('Study session started! Good luck with your learning.', 'success')
                return redirect(url_for('sessions.session_detail', session_id=session.id))
            else:
                print("Session creation returned None")
                flash('Error starting session. Please try again.', 'error')
        
        return render_template('sessions/start.html', form=form, topics=topics, ai_recommendations=ai_recommendations)
    
    except Exception as e:
        flash('Error loading session start page. Please try again.', 'error')
        return redirect(url_for('sessions.session_history'))

@sessions.route('/sessions/<session_id>')
def session_detail(session_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        print(f"Looking for session ID: {session_id} for user: {user.id}")
        session = StudySession.get_session_by_id(session_id, user.id)
        print(f"Found session: {session}")
        if not session:
            flash('Session not found.', 'error')
            return redirect(url_for('sessions.session_history'))
        
        
        topic = Topic.get_by_id(session.topic_id, user.id)
        
        
        related_sessions = StudySession.get_topic_sessions(session.topic_id, user.id)
        related_sessions = [s for s in related_sessions if s.id != session_id][:5]
        
        
        topic_progress = StudySession.get_topic_progress(session.topic_id, user.id)
        
        return render_template('sessions/detail.html', 
                             session=session, 
                             topic=topic,
                             related_sessions=related_sessions,
                             topic_progress=topic_progress)
    
    except Exception as e:
        flash('Error loading session details. Please try again.', 'error')
        return redirect(url_for('sessions.session_history'))


@sessions.route('/sessions/export/csv')
@login_required
def export_sessions_csv():
    
    try:
        
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        all_sessions = StudySession.get_user_sessions(user.id)
        
        
        topics = Topic.get_all_by_user(user.id)
        topic_map = {topic.id: topic.title for topic in topics}
        
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        
        writer.writerow([
            'Session ID', 'Topic', 'Date', 'Duration (minutes)', 
            'Confidence Before', 'Confidence After', 'Session Type', 
            'Completed', 'Notes', 'Created At'
        ])
        
        
        for session in all_sessions:
            writer.writerow([
                session.id,
                topic_map.get(session.topic_id, 'Unknown Topic'),
                session.session_date.strftime('%Y-%m-%d'),
                session.duration_minutes,
                session.confidence_before,
                session.confidence_after,
                session.session_type,
                'Yes' if session.completed else 'No',
                session.notes or '',
                session.created_at.strftime('%Y-%m-%d %H:%M:%S') if session.created_at else ''
            ])
        
        
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=study_sessions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
    
    except Exception as e:
        flash('Error exporting sessions. Please try again.', 'error')
        return redirect(url_for('sessions.session_history'))


@sessions.route('/sessions/export/json')
@login_required
def export_sessions_json():
    
    try:
        
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        all_sessions = StudySession.get_user_sessions(user.id)
        
        
        topics = Topic.get_all_by_user(user.id)
        topic_map = {topic.id: topic.title for topic in topics}
        
        
        sessions_data = []
        for session in all_sessions:
            sessions_data.append({
                'id': session.id,
                'topic': topic_map.get(session.topic_id, 'Unknown Topic'),
                'topic_id': session.topic_id,
                'date': session.session_date.isoformat(),
                'duration_minutes': session.duration_minutes,
                'confidence_before': session.confidence_before,
                'confidence_after': session.confidence_after,
                'session_type': session.session_type,
                'completed': session.completed,
                'notes': session.notes,
                'created_at': session.created_at.isoformat() if session.created_at else None
            })
        
        
        response = make_response(json.dumps(sessions_data, indent=2))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Disposition'] = f'attachment; filename=study_sessions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        return response
    
    except Exception as e:
        flash('Error exporting sessions. Please try again.', 'error')
        return redirect(url_for('sessions.session_history'))


@sessions.route('/sessions/export/complete')
@login_required
def export_complete_data():
    
    try:
        
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        sessions = StudySession.get_user_sessions(user.id)
        topics = Topic.get_all_by_user(user.id)
        
        
        complete_data = {
            'export_info': {
                'exported_at': datetime.now().isoformat(),
                'user_id': user.id,
                'total_sessions': len(sessions),
                'total_topics': len(topics)
            },
            'topics': [],
            'sessions': []
        }
        
        
        for topic in topics:
            complete_data['topics'].append({
                'id': topic.id,
                'title': topic.title,
                'description': topic.description,
                'created_at': topic.created_at.isoformat() if topic.created_at else None,
                'is_active': topic.is_active,
                'is_shared': getattr(topic, 'is_shared', False),
                'share_code': getattr(topic, 'share_code', None)
            })
        
        
        for session in sessions:
            complete_data['sessions'].append({
                'id': session.id,
                'topic_id': session.topic_id,
                'date': session.session_date.isoformat(),
                'duration_minutes': session.duration_minutes,
                'confidence_before': session.confidence_before,
                'confidence_after': session.confidence_after,
                'session_type': session.session_type,
                'completed': session.completed,
                'notes': session.notes,
                'created_at': session.created_at.isoformat() if session.created_at else None
            })
        
        
        response = make_response(json.dumps(complete_data, indent=2))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Disposition'] = f'attachment; filename=complete_data_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        return response
    
    except Exception as e:
        flash('Error exporting complete data. Please try again.', 'error')
        return redirect(url_for('sessions.session_history'))


@sessions.route('/sessions/<session_id>/edit', methods=['GET', 'POST'])
def edit_session(session_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        session = StudySession.get_session_by_id(session_id, user.id)
        if not session:
            flash('Session not found.', 'error')
            return redirect(url_for('sessions.session_history'))
        
        form = EditSessionForm()
        
        if request.method == 'GET':
            
            form.session_date.data = session.session_date.date() if isinstance(session.session_date, datetime) else session.session_date
            form.duration_minutes.data = session.duration_minutes
            form.confidence_before.data = session.confidence_before
            form.confidence_after.data = session.confidence_after
            form.notes.data = session.notes
            form.session_type.data = session.session_type
        
        if form.validate_on_submit():
            print(f"Updating session {session.id} with data: {form.data}")
            
            success = session.update_session(
                session_date=form.session_date.data,
                duration_minutes=form.duration_minutes.data,
                confidence_before=form.confidence_before.data,
                confidence_after=form.confidence_after.data,
                notes=form.notes.data,
                session_type=form.session_type.data
            )
            
            print(f"Update result: {success}")
            if success:
                flash('Session updated successfully!', 'success')
                return redirect(url_for('sessions.session_detail', session_id=session.id))
            else:
                flash('Error updating session. Please try again.', 'error')
        
        return render_template('sessions/edit.html', form=form, session=session)
    
    except Exception as e:
        flash('Error loading session edit page. Please try again.', 'error')
        return redirect(url_for('sessions.session_history'))

@sessions.route('/sessions/<session_id>/complete', methods=['POST'])
def complete_session(session_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        session = StudySession.get_session_by_id(session_id, user.id)
        if not session:
            flash('Session not found.', 'error')
            return redirect(url_for('sessions.session_history'))
        
        form = CompleteSessionForm()
        
        if form.validate_on_submit():
            
            success = session.update_session(
                duration_minutes=form.duration_minutes.data,
                confidence_after=form.confidence_after.data,
                notes=form.notes.data,
                completed=form.completed.data
            )
            
            if success:
                confidence_gain = form.confidence_after.data - session.confidence_before
                
                
                rewards = GamificationEngine.process_study_session(user.id, form.duration_minutes.data)
                
                
                success_message = f'Session completed! Confidence improved by {confidence_gain} points.'
                if rewards['xp_earned'] > 0:
                    success_message += f' Earned {rewards["xp_earned"]} XP!'
                if rewards['level_up']:
                    success_message += ' 🎉 Level up!'
                if rewards['badges_earned']:
                    success_message += f' 🏆 New badges: {", ".join(rewards["badges_earned"])}'
                if rewards['achievements_unlocked']:
                    success_message += f' ⭐ New achievements: {", ".join(rewards["achievements_unlocked"])}'
                
                flash(success_message, 'success')
                return redirect(url_for('sessions.session_detail', session_id=session.id))
            else:
                flash('Error completing session. Please try again.', 'error')
        
        
        return redirect(url_for('sessions.session_detail', session_id=session_id))
    
    except Exception as e:
        flash('Error completing session. Please try again.', 'error')
        return redirect(url_for('sessions.session_history'))

@sessions.route('/sessions/<session_id>/delete', methods=['POST'])
def delete_session(session_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        session = StudySession.get_session_by_id(session_id, user.id)
        if not session:
            flash('Session not found.', 'error')
            return redirect(url_for('sessions.session_history'))
        
        success = StudySession.delete_session(session_id, user.id)
        
        if success:
            flash('Session deleted successfully.', 'success')
        else:
            flash('Error deleting session. Please try again.', 'error')
        
        return redirect(url_for('sessions.session_history'))
    
    except Exception as e:
        flash('Error deleting session. Please try again.', 'error')
        return redirect(url_for('sessions.session_history'))

@sessions.route('/sessions/timer')
@login_required
def study_timer():
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topics = Topic.get_all_by_user(user.id)
        if not topics:
            flash('You need to create a topic before using the timer.', 'warning')
            return redirect(url_for('topics.create_topic'))
        
        return render_template('sessions/timer.html', topics=topics)
    
    except Exception as e:
        flash('Error loading timer page. Please try again.', 'error')
        return redirect(url_for('sessions.session_history'))

@sessions.route('/sessions/api/start-timer', methods=['POST'])
def start_timer_session():
    try:

        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated. Please log in to use the study timer.'}), 401
        
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        topic_id = data.get('topic_id')
        session_type = data.get('session_type', 'practice')
        confidence_before = data.get('confidence_before', 5)
        
        if not topic_id:
            return jsonify({'error': 'Topic ID is required'}), 400
        
        topic = Topic.get_by_id(topic_id, user.id)
        if not topic:
            return jsonify({'error': 'Topic not found'}), 404
        
        

        try:
            session = StudySession.create_session(
                user_id=user.id,
                topic_id=topic_id,
                session_date=datetime.now(),
                duration_minutes=25,  
                confidence_before=confidence_before,
                confidence_after=confidence_before,  
                notes='',
                session_type=session_type,
                completed=False
            )
        except Exception as e:


            from datetime import timedelta
            past_date = datetime.now() - timedelta(days=730)
            
            try:
                session = StudySession.create_session(
                    user_id=user.id,
                    topic_id=topic_id,
                    session_date=past_date,
                    duration_minutes=25,  
                    confidence_before=confidence_before,
                    confidence_after=confidence_before,  
                    notes='',
                    session_type=session_type,
                    completed=False
                )
            except Exception as e2:
                print(f"Error creating session with past date: {e2}")
                session = None
        
        if session:
            return jsonify({
                'success': True,
                'session_id': session.id,
                'message': 'Timer session started'
            })
        else:

            return jsonify({
                'error': 'Database constraint prevents session creation. The next_recommended_date_future constraint is blocking session creation.',
                'details': 'To fix this issue, run the following SQL in your Supabase dashboard: ALTER TABLE user_analytics DROP CONSTRAINT IF EXISTS next_recommended_date_future;',
                'fix_required': True,
                'sql_command': 'ALTER TABLE user_analytics DROP CONSTRAINT IF EXISTS next_recommended_date_future;'
            }), 500
    
    except Exception as e:
        print(f"ERROR in start_timer_session: {e}")
        print(f"ERROR type: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'error_type': str(type(e))}), 500

@sessions.route('/sessions/api/complete-timer', methods=['POST'])
@login_required
def complete_timer_session():
    
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        duration_minutes = data.get('duration_minutes')
        confidence_after = data.get('confidence_after')
        notes = data.get('notes', '')
        
        if not all([session_id, duration_minutes, confidence_after]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        session = StudySession.get_session_by_id(session_id, user.id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        
        success = session.update_session(
            duration_minutes=duration_minutes,
            confidence_after=confidence_after,
            notes=notes,
            completed=True
        )
        
        if success:
            confidence_gain = confidence_after - session.confidence_before
            return jsonify({
                'success': True,
                'confidence_gain': confidence_gain,
                'message': 'Session completed successfully'
            })
        else:
            return jsonify({'error': 'Failed to update session'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions.route('/sessions/<session_id>/update-notes', methods=['POST'])
def update_notes(session_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        session = StudySession.get_session_by_id(session_id, user.id)
        if not session:
            flash('Session not found.', 'error')
            return redirect(url_for('sessions.session_history'))
        
        notes = request.form.get('notes', '').strip()
        
        
        success = session.update_session(notes=notes)
        
        if success:
            flash('Session notes updated successfully!', 'success')
        else:
            flash('Error updating session notes. Please try again.', 'error')
        
        return redirect(url_for('sessions.session_detail', session_id=session_id))
    
    except Exception as e:
        flash('Error updating session notes. Please try again.', 'error')
        return redirect(url_for('sessions.session_detail', session_id=session_id))


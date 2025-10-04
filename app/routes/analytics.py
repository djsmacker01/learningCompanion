from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required
from app.models import get_supabase_client, SUPABASE_AVAILABLE
from app.routes.topics import get_current_user
from datetime import datetime, timedelta
import json

analytics = Blueprint('analytics', __name__)

@analytics.route('/analytics')
@login_required
def analytics_dashboard():
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        client = get_supabase_client()
        
        if not SUPABASE_AVAILABLE or not client:
            return render_template('analytics/dashboard.html', 
                                 error="Analytics not available - Supabase connection failed")
        
        analytics_data = get_user_analytics(user.id, client)
        topic_analytics = get_topic_analytics(user.id, client)
        learning_insights = get_learning_insights(user.id, client)
        
        
        return render_template('analytics/dashboard.html',
                             analytics_data=analytics_data,
                             topic_analytics=topic_analytics,
                             learning_insights=learning_insights)
    
    except Exception as e:
        print(f"Error loading analytics: {e}")
        return render_template('analytics/dashboard.html', 
                             error="Error loading analytics data")

@analytics.route('/analytics/api/overview')
@login_required
def analytics_overview():
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        client = get_supabase_client()
        
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Analytics not available'}), 500
        
        overview_data = get_analytics_overview(user.id, client)
        return jsonify(overview_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics.route('/analytics/api/topic-progress')
@login_required
def topic_progress():
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        client = get_supabase_client()
        
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Analytics not available'}), 500
        
        
        progress_data = get_topic_progress_data(user.id, client)
        return jsonify(progress_data)
    
    except Exception as e:
        print(f"Error in topic progress API: {e}")
        return jsonify({'error': str(e)}), 500

@analytics.route('/analytics/api/learning-trends')
def learning_trends():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        client = get_supabase_client()
        
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Analytics not available'}), 500
        
        
        trends_data = get_learning_trends_data(user.id, client)
        return jsonify(trends_data)
    
    except Exception as e:
        print(f"Error in learning trends API: {e}")
        return jsonify({'error': str(e)}), 500

def get_user_analytics(user_id, client):
    try:
        
        response = client.table('user_dashboard_analytics').select('*').eq('user_id', user_id).execute()
        
        if response.data:
            return response.data[0]
        
        
        return calculate_user_analytics(user_id, client)
    
    except Exception as e:
        print(f"Error getting user analytics: {e}")
        return calculate_user_analytics(user_id, client)

def calculate_user_analytics(user_id, client):
    try:
        
        topics_response = client.table('topics').select('id').eq('user_id', user_id).eq('is_active', True).execute()
        total_topics = len(topics_response.data) if topics_response.data else 0
        
        
        sessions_response = client.table('study_sessions').select('*').eq('user_id', user_id).execute()
        all_sessions = sessions_response.data if sessions_response.data else []
        
       
        sessions = [s for s in all_sessions if s.get('duration_minutes', 0) > 0 or (s.get('confidence_before') and s.get('confidence_after'))]
        
        total_sessions = len(sessions)
        total_study_time = sum(session.get('duration_minutes', 0) for session in sessions)
        
       
        confidence_gains = []
        for session in sessions:
            if session.get('confidence_after') and session.get('confidence_before'):
                gain = session['confidence_after'] - session['confidence_before']
                confidence_gains.append(gain)
        
        avg_confidence_gain = sum(confidence_gains) / len(confidence_gains) if confidence_gains else 0
        
        
        last_study_date = None
        if sessions:
            session_dates = []
            for s in sessions:
                if s.get('session_date'):
                    try:
                        if 'T' in s['session_date']:
                            session_dates.append(datetime.fromisoformat(s['session_date']))
                        else:
                            session_dates.append(datetime.fromisoformat(s['session_date'] + 'T00:00:00'))
                    except:
                        continue
            if session_dates:
                last_study_date = max(session_dates).date()
        
      
        week_ago = datetime.now() - timedelta(days=7)
        sessions_this_week = 0
        for s in sessions:
            if s.get('session_date'):
                try:
                    if 'T' in s['session_date']:
                        session_date = datetime.fromisoformat(s['session_date'])
                    else:
                        session_date = datetime.fromisoformat(s['session_date'] + 'T00:00:00')
                    if session_date >= week_ago:
                        sessions_this_week += 1
                except:
                    continue
        
       
        days_since_last_study = None
        if last_study_date:
            days_since_last_study = (datetime.now().date() - last_study_date).days
        
        result = {
            'user_id': user_id,
            'total_topics': total_topics,
            'active_topics': total_topics,
            'total_sessions': total_sessions,
            'total_study_time': total_study_time,
            'avg_confidence_gain': round(avg_confidence_gain, 2),
            'last_study_date': last_study_date,
            'days_since_last_study': days_since_last_study,
            'sessions_this_week': sessions_this_week
        }
        
        return result
    
    except Exception as e:
        print(f"Error calculating user analytics: {e}")
        return {
            'user_id': user_id,
            'total_topics': 0,
            'active_topics': 0,
            'total_sessions': 0,
            'total_study_time': 0,
            'avg_confidence_gain': 0,
            'last_study_date': None,
            'days_since_last_study': None,
            'sessions_this_week': 0
        }

def get_topic_analytics(user_id, client):
    try:
        
        response = client.table('topic_progress_analytics').select('*').eq('user_id', user_id).execute()
        
        if response.data:
            return response.data
        
        
        return calculate_topic_analytics(user_id, client)
    
    except Exception as e:
        print(f"Error getting topic analytics: {e}")
        return calculate_topic_analytics(user_id, client)

def calculate_topic_analytics(user_id, client):
    try:
        topics_response = client.table('topics').select('*').eq('user_id', user_id).eq('is_active', True).execute()
        topics = topics_response.data if topics_response.data else []
        
        topic_analytics = []
        for topic in topics:
            sessions_response = client.table('study_sessions').select('*').eq('user_id', user_id).eq('topic_id', topic['id']).execute()
            all_topic_sessions = sessions_response.data if sessions_response.data else []
            
            sessions = [s for s in all_topic_sessions if s.get('duration_minutes', 0) > 0 or (s.get('confidence_before') and s.get('confidence_after'))]
            
            total_sessions = len(sessions)
            total_study_time = sum(session.get('duration_minutes', 0) for session in sessions)
            
            confidence_gains = []
            for session in sessions:
                if session.get('confidence_after') and session.get('confidence_before'):
                    gain = session['confidence_after'] - session['confidence_before']
                    confidence_gains.append(gain)
            
            avg_confidence_gain = sum(confidence_gains) / len(confidence_gains) if confidence_gains else 0
            
            last_session_date = None
            if sessions:
                session_dates = []
                for s in sessions:
                    if s.get('session_date'):
                        try:
                            if 'T' in s['session_date']:
                                session_dates.append(datetime.fromisoformat(s['session_date']))
                            else:
                                session_dates.append(datetime.fromisoformat(s['session_date'] + 'T00:00:00'))
                        except:
                            continue
                if session_dates:
                    last_session_date = max(session_dates).date()
            
            mastery_level = min(5, max(1, int(total_sessions / 3) + 1))
            
            target_sessions = topic.get('target_sessions_per_week', 3)
            if total_sessions >= target_sessions:
                progress_status = 'On Track'
            elif total_sessions >= target_sessions * 0.5:
                progress_status = 'Behind'
            else:
                progress_status = 'Needs Attention'
            
            topic_data = {
                'topic_id': topic['id'],
                'user_id': user_id,
                'title': topic['title'],
                'difficulty_level': topic.get('difficulty_level', 'beginner'),
                'target_sessions_per_week': target_sessions,
                'total_sessions': total_sessions,
                'total_study_time': total_study_time,
                'current_streak': 0,
                'longest_streak': 0,
                'mastery_level': mastery_level,
                'average_confidence_gain': round(avg_confidence_gain, 2),
                'last_session_date': last_session_date,
                'next_recommended_date': None,
                'progress_status': progress_status
            }
            
            topic_analytics.append(topic_data)
        return topic_analytics
    
    except Exception as e:
        print(f"Error calculating topic analytics: {e}")
        return []

def get_learning_insights(user_id, client):
    try:
        sessions_response = client.table('study_sessions').select('*').eq('user_id', user_id).order('session_date', desc=True).limit(20).execute()
        all_sessions = sessions_response.data if sessions_response.data else []
        
        sessions = [s for s in all_sessions if s.get('duration_minutes', 0) > 0 or (s.get('confidence_before') and s.get('confidence_after'))]
        
        insights = []
        
        if not sessions:
            return [{'type': 'info', 'message': 'Start studying to get personalized insights!'}]
        
        total_sessions = len(sessions)
        total_time = sum(session.get('duration_minutes', 0) for session in sessions)
        avg_duration = total_time / total_sessions if total_sessions > 0 else 0
        
        confidence_gains = []
        for session in sessions:
            if session.get('confidence_after') and session.get('confidence_before'):
                gain = session['confidence_after'] - session['confidence_before']
                confidence_gains.append(gain)
        
        avg_confidence_gain = sum(confidence_gains) / len(confidence_gains) if confidence_gains else 0
        
        if avg_confidence_gain > 2:
            insights.append({
                'type': 'success',
                'message': f'Great progress! Your confidence is improving by {avg_confidence_gain:.1f} points on average.',
                'icon': 'fas fa-trophy'
            })
        elif avg_confidence_gain < 0:
            insights.append({
                'type': 'warning',
                'message': 'Consider reviewing previous material to boost your confidence.',
                'icon': 'fas fa-exclamation-triangle'
            })
        
        if avg_duration > 45:
            insights.append({
                'type': 'info',
                'message': f'You study for {avg_duration:.0f} minutes on average. Consider shorter, focused sessions.',
                'icon': 'fas fa-clock'
            })
        elif avg_duration < 15:
            insights.append({
                'type': 'info',
                'message': f'Your sessions are {avg_duration:.0f} minutes on average. Try longer sessions for deeper learning.',
                'icon': 'fas fa-clock'
            })
        
        if total_sessions >= 10:
            insights.append({
                'type': 'success',
                'message': f'Excellent consistency! You\'ve completed {total_sessions} study sessions.',
                'icon': 'fas fa-star'
            })
        
        return insights
    
    except Exception as e:
        print(f"Error getting learning insights: {e}")
        return [{'type': 'error', 'message': 'Unable to generate insights at this time.'}]

def get_analytics_overview(user_id, client):
    analytics_data = get_user_analytics(user_id, client)
    
    return {
        'total_topics': analytics_data.get('total_topics', 0),
        'total_sessions': analytics_data.get('total_sessions', 0),
        'total_study_time': analytics_data.get('total_study_time', 0),
        'avg_confidence_gain': analytics_data.get('avg_confidence_gain', 0),
        'sessions_this_week': analytics_data.get('sessions_this_week', 0)
    }

def get_topic_progress_data(user_id, client):
    topic_analytics = get_topic_analytics(user_id, client)
    
    on_track = 0
    behind = 0
    needs_attention = 0
    
    for topic in topic_analytics:
        total_sessions = topic.get('total_sessions', 0)
        target_sessions = topic.get('target_sessions_per_week', 3)
        
        if total_sessions >= target_sessions:
            on_track += 1
        elif total_sessions >= target_sessions * 0.5:
            behind += 1
        else:
            needs_attention += 1
    
    
    return {
        'topics': topic_analytics,
        'summary': {
            'total_topics': len(topic_analytics),
            'on_track': on_track,
            'behind': behind,
            'needs_attention': needs_attention
        }
    }

def get_learning_trends_data(user_id, client):
    try:
        
        sessions_response = client.table('study_sessions').select('*').eq('user_id', user_id).order('session_date').execute()
        all_sessions = sessions_response.data if sessions_response.data else []
        
        sessions = [s for s in all_sessions if s.get('duration_minutes', 0) > 0 or (s.get('confidence_before') and s.get('confidence_after'))]
        
        
        daily_data = {}
        for session in sessions:
            session_date = session.get('session_date', '')
            if session_date:
                if 'T' in session_date:
                    date_key = session_date[:10]
                else:
                    date_key = session_date
                
                if date_key not in daily_data:
                    daily_data[date_key] = {'sessions': 0, 'time': 0, 'confidence_gain': 0}
                
                daily_data[date_key]['sessions'] += 1
                daily_data[date_key]['time'] += session.get('duration_minutes', 0)
                
                if session.get('confidence_after') and session.get('confidence_before'):
                    daily_data[date_key]['confidence_gain'] += session['confidence_after'] - session['confidence_before']
        
        trends = []
        for date, data in sorted(daily_data.items()):
            trends.append({
                'date': date,
                'sessions': data['sessions'],
                'time': data['time'],
                'confidence_gain': data['confidence_gain']
            })
        
        return {'trends': trends}
    
    except Exception as e:
        print(f"Error getting learning trends: {e}")
        return {'trends': []}


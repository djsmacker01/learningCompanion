from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import get_supabase_client, SUPABASE_AVAILABLE
from app.routes.topics import get_current_user
from datetime import datetime, timedelta
import json

analytics = Blueprint('analytics', __name__)

@analytics.route('/analytics')
@login_required
def dashboard():
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        client = get_supabase_client()
        
        if not SUPABASE_AVAILABLE or not client:
            return render_template('analytics/dashboard.html', 
                                 error="Analytics not available - Supabase connection failed")
        
        print(f"DEBUG: Loading analytics for user {user.id}")
        analytics_data = get_user_analytics(user.id, client)
        print(f"DEBUG: Analytics data: {analytics_data}")
        
        topic_analytics = get_topic_analytics(user.id, client)
        print(f"DEBUG: Topic analytics: {topic_analytics}")
        
        learning_insights = get_learning_insights(user.id, client)
        print(f"DEBUG: Learning insights: {learning_insights}")
        
        return render_template('analytics/dashboard.html',
                             analytics_data=analytics_data,
                             topic_analytics=topic_analytics,
                             learning_insights=learning_insights)
    
    except Exception as e:
        print(f"Error loading analytics: {e}")
        import traceback
        traceback.print_exc()
        return render_template('analytics/dashboard.html', 
                             error="Error loading analytics data")

@analytics.route('/analytics/api/overview')
def analytics_overview():
    try:

        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401
        
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
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


@analytics.route('/analytics/performance-trends')
def performance_trends():
    """Get performance trends analysis"""
    try:
        # Check authentication manually to return JSON error instead of redirect
        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401
        
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Analytics not available'}), 500
        
        # Get user's study sessions for analysis
        sessions_response = client.table('study_sessions').select('*').eq('user_id', user.id).order('session_date').execute()
        sessions = sessions_response.data if sessions_response.data else []
        
        if not sessions:
            return jsonify({
                'overall_trend': 'No Data',
                'total_topics_analyzed': 0,
                'analysis_period_days': 0,
                'strengths_weaknesses': {
                    'strengths': ['Start studying to see your strengths'],
                    'weaknesses': ['No weaknesses identified yet']
                }
            })
        
        # Calculate trends
        total_sessions = len(sessions)
        total_study_time = sum(session.get('duration_minutes', 0) for session in sessions)
        avg_session_length = total_study_time / total_sessions if total_sessions > 0 else 0
        
        # Calculate confidence trends
        confidence_gains = []
        for session in sessions:
            if session.get('confidence_after') and session.get('confidence_before'):
                gain = session['confidence_after'] - session['confidence_before']
                confidence_gains.append(gain)
        
        avg_confidence_gain = sum(confidence_gains) / len(confidence_gains) if confidence_gains else 0
        
        # Determine overall trend
        if avg_confidence_gain > 1:
            overall_trend = 'Improving'
        elif avg_confidence_gain > 0:
            overall_trend = 'Stable'
        else:
            overall_trend = 'Declining'
        
        # Get unique topics
        topic_ids = list(set(session.get('topic_id') for session in sessions if session.get('topic_id')))
        total_topics_analyzed = len(topic_ids)
        
        # Calculate analysis period
        if sessions:
            first_session = min(sessions, key=lambda x: x.get('session_date', ''))
            last_session = max(sessions, key=lambda x: x.get('session_date', ''))
            try:
                first_date = datetime.fromisoformat(first_session['session_date'].replace('T', ' ').split('.')[0])
                last_date = datetime.fromisoformat(last_session['session_date'].replace('T', ' ').split('.')[0])
                analysis_period_days = (last_date - first_date).days + 1
            except:
                analysis_period_days = 30
        else:
            analysis_period_days = 0
        
        # Generate strengths and weaknesses
        strengths = []
        weaknesses = []
        
        if avg_confidence_gain > 1:
            strengths.append('Strong confidence improvement')
        if total_sessions > 10:
            strengths.append('Consistent study habits')
        if avg_session_length > 30:
            strengths.append('Effective study sessions')
        
        if avg_confidence_gain < 0:
            weaknesses.append('Confidence declining')
        if total_sessions < 5:
            weaknesses.append('Need more study sessions')
        if avg_session_length < 15:
            weaknesses.append('Study sessions too short')
        
        return jsonify({
            'overall_trend': overall_trend,
            'total_topics_analyzed': total_topics_analyzed,
            'analysis_period_days': analysis_period_days,
            'strengths_weaknesses': {
                'strengths': strengths if strengths else ['Keep up the good work!'],
                'weaknesses': weaknesses if weaknesses else ['No major weaknesses identified']
            }
        })
    
    except Exception as e:
        print(f"Error getting performance trends: {e}")
        return jsonify({'error': 'Failed to get performance trends'}), 500

@analytics.route('/analytics/grade-prediction/<topic_id>')
def grade_prediction(topic_id):
    """Predict grade for a specific topic"""
    try:

        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401
        
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Analytics not available'}), 500
        

        topic_response = client.table('topics').select('*').eq('id', topic_id).eq('user_id', user.id).execute()
        if not topic_response.data:
            return jsonify({'error': 'Topic not found'}), 404
        
        topic = topic_response.data[0]
        

        sessions_response = client.table('study_sessions').select('*').eq('user_id', user.id).eq('topic_id', topic_id).execute()
        sessions = sessions_response.data if sessions_response.data else []
        
        if not sessions:
            return jsonify({
                'predictions': {
                    'ensemble': {
                        'grade': 'N/A',
                        'confidence': 0,
                        'model_count': 1
                    }
                },
                'recommendations': ['Start studying this topic to get grade predictions']
            })
        

        total_sessions = len(sessions)
        total_study_time = sum(session.get('duration_minutes', 0) for session in sessions)
        avg_session_length = total_study_time / total_sessions if total_sessions > 0 else 0
        

        confidence_gains = []
        for session in sessions:
            if session.get('confidence_after') and session.get('confidence_before'):
                gain = session['confidence_after'] - session['confidence_before']
                confidence_gains.append(gain)
        
        avg_confidence_gain = sum(confidence_gains) / len(confidence_gains) if confidence_gains else 0
        

        base_grade = 5
        

        if avg_confidence_gain > 2:
            grade_adjustment = 2
        elif avg_confidence_gain > 1:
            grade_adjustment = 1
        elif avg_confidence_gain > 0:
            grade_adjustment = 0
        else:
            grade_adjustment = -1
        

        if total_study_time > 300:
            time_adjustment = 1
        elif total_study_time > 120:
            time_adjustment = 0
        else:
            time_adjustment = -1
        

        if total_sessions > 10:
            frequency_adjustment = 1
        elif total_sessions > 5:
            frequency_adjustment = 0
        else:
            frequency_adjustment = -1
        
        predicted_grade = min(9, max(1, base_grade + grade_adjustment + time_adjustment + frequency_adjustment))
        

        confidence = min(95, max(20, 50 + (avg_confidence_gain * 10) + (total_sessions * 2)))
        

        recommendations = []
        if predicted_grade < 7:
            recommendations.append('Increase study time for this topic')
            recommendations.append('Focus on understanding core concepts')
        if total_sessions < 5:
            recommendations.append('Study this topic more frequently')
        if avg_confidence_gain < 1:
            recommendations.append('Review previous material to boost confidence')
        
        return jsonify({
            'predictions': {
                'ensemble': {
                    'grade': predicted_grade,
                    'confidence': round(confidence),
                    'model_count': 3
                }
            },
            'recommendations': recommendations
        })
    
    except Exception as e:
        print(f"Error predicting grade: {e}")
        return jsonify({'error': 'Failed to predict grade'}), 500

@analytics.route('/analytics/trajectory/<topic_id>')
def learning_trajectory(topic_id):
    """Analyze learning trajectory for a topic"""
    try:
        # Check authentication manually to return JSON error instead of redirect
        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401
        
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Analytics not available'}), 500
        
        days_back = request.args.get('days_back', 30, type=int)
        
        # Get sessions for this topic within the specified period
        cutoff_date = datetime.now() - timedelta(days=days_back)
        sessions_response = client.table('study_sessions').select('*').eq('user_id', user.id).eq('topic_id', topic_id).gte('session_date', cutoff_date.isoformat()).order('session_date').execute()
        sessions = sessions_response.data if sessions_response.data else []
        
        if not sessions:
            return jsonify({
                'data_points': 0,
                'analysis_period_days': days_back,
                'insights': ['No study sessions found for this period']
            })
        
        # Analyze trajectory
        data_points = len(sessions)
        total_study_time = sum(session.get('duration_minutes', 0) for session in sessions)
        
        # Calculate confidence progression
        confidence_progression = []
        for session in sessions:
            if session.get('confidence_after'):
                confidence_progression.append(session['confidence_after'])
        
        # Generate insights
        insights = []
        if len(confidence_progression) > 1:
            if confidence_progression[-1] > confidence_progression[0]:
                insights.append('Confidence is improving over time')
            elif confidence_progression[-1] < confidence_progression[0]:
                insights.append('Confidence has declined recently')
            else:
                insights.append('Confidence has remained stable')
        
        if total_study_time > 180:  # More than 3 hours
            insights.append('Good study time investment in this topic')
        elif total_study_time < 60:  # Less than 1 hour
            insights.append('Consider spending more time on this topic')
        
        if data_points > 5:
            insights.append('Consistent study pattern detected')
        elif data_points < 3:
            insights.append('Study sessions are infrequent')
        
        return jsonify({
            'data_points': data_points,
            'analysis_period_days': days_back,
            'insights': insights
        })
    
    except Exception as e:
        print(f"Error analyzing trajectory: {e}")
        return jsonify({'error': 'Failed to analyze trajectory'}), 500

@analytics.route('/analytics/insights')
def ai_insights():
    """Get AI-powered learning insights"""
    try:

        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401
        
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Analytics not available'}), 500
        

        sessions_response = client.table('study_sessions').select('*').eq('user_id', user.id).order('session_date', desc=True).limit(20).execute()
        sessions = sessions_response.data if sessions_response.data else []
        
        if not sessions:
            return jsonify({
                'key_insights': ['Start studying to get personalized insights'],
                'recommendations': ['Create your first topic and begin studying']
            })
        

        total_sessions = len(sessions)
        total_study_time = sum(session.get('duration_minutes', 0) for session in sessions)
        avg_session_length = total_study_time / total_sessions if total_sessions > 0 else 0
        

        confidence_gains = []
        for session in sessions:
            if session.get('confidence_after') and session.get('confidence_before'):
                gain = session['confidence_after'] - session['confidence_before']
                confidence_gains.append(gain)
        
        avg_confidence_gain = sum(confidence_gains) / len(confidence_gains) if confidence_gains else 0
        

        key_insights = []
        recommendations = []
        
        if avg_confidence_gain > 2:
            key_insights.append('Excellent learning progress - confidence is improving significantly')
            recommendations.append('Continue with your current study approach')
        elif avg_confidence_gain > 0:
            key_insights.append('Steady learning progress detected')
            recommendations.append('Consider increasing study intensity for faster progress')
        else:
            key_insights.append('Learning progress needs attention')
            recommendations.append('Review study methods and consider different approaches')
        
        if avg_session_length > 45:
            key_insights.append('Long study sessions are effective for your learning')
            recommendations.append('Maintain your current session length')
        elif avg_session_length < 20:
            key_insights.append('Short study sessions may limit deep learning')
            recommendations.append('Try extending study sessions to 25-30 minutes')
        
        if total_sessions > 15:
            key_insights.append('Consistent study habits are well established')
            recommendations.append('Keep up the regular study routine')
        elif total_sessions < 5:
            key_insights.append('Study frequency could be improved')
            recommendations.append('Aim for at least 3-4 study sessions per week')
        
        return jsonify({
            'key_insights': key_insights,
            'recommendations': recommendations
        })
    
    except Exception as e:
        print(f"Error getting AI insights: {e}")
        return jsonify({'error': 'Failed to get AI insights'}), 500

@analytics.route('/analytics/api/topics')
def analytics_topics():
    """Get user's topics for analytics dropdowns"""
    try:
        print(f"DEBUG: Analytics topics API called")
        print(f"DEBUG: current_user.is_authenticated: {current_user.is_authenticated}")
        
        # Check authentication manually to return JSON error instead of redirect
        if not current_user.is_authenticated:
            print("DEBUG: User not authenticated, returning 401")
            return jsonify({'error': 'User not authenticated'}), 401
        
        user = get_current_user()
        if not user:
            print("DEBUG: get_current_user returned None, returning 401")
            return jsonify({'error': 'User not authenticated'}), 401
        
        print(f"DEBUG: User authenticated: {user.id}")
        
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Analytics not available'}), 500
        
        # Get user's topics
        print(f"DEBUG: Querying topics for user {user.id}")
        topics_response = client.table('topics').select('id, title, description').eq('user_id', user.id).eq('is_active', True).order('title').execute()
        topics = topics_response.data if topics_response.data else []
        
        print(f"DEBUG: Found {len(topics)} topics")
        for topic in topics:
            print(f"DEBUG: Topic - {topic.get('title', 'No title')} (ID: {topic.get('id', 'No ID')})")
        
        return jsonify({
            'topics': topics
        })
    
    except Exception as e:
        print(f"Error getting topics for analytics: {e}")
        return jsonify({'error': 'Failed to get topics'}), 500


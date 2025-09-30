

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from datetime import datetime, timedelta, date
from app.models import Topic
from app.models.study_session import StudySession
from app.models import get_supabase_client, SUPABASE_AVAILABLE
from app.routes.topics import get_current_user
from app.utils.ai_algorithms import LearningAnalytics
import json

ai_recommendations = Blueprint('ai_recommendations', __name__)

@ai_recommendations.route('/ai/recommendations')
@login_required
def recommendations_dashboard():
    """AI Recommendations Dashboard"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        client = get_supabase_client()
        
        if not SUPABASE_AVAILABLE or not client:
            return render_template('ai/recommendations.html', 
                                 recommendations=[], 
                                 error="AI recommendations not available")
        

        recommendations = LearningAnalytics.get_learning_recommendations(user.id)
        
        
        study_patterns = LearningAnalytics.get_study_pattern_insights(user.id)
        
        
        topics_for_review = get_topics_for_review(user.id, client)
        
        study_schedule = get_study_schedule(user.id, client)
        
        return render_template('ai/recommendations.html',
                             recommendations=recommendations,
                             study_patterns=study_patterns,
                             topics_for_review=topics_for_review,
                             study_schedule=study_schedule)
    
    except Exception as e:
        print(f"Error loading AI recommendations: {e}")
        return render_template('ai/recommendations.html', 
                             recommendations=[], 
                             error="Error loading recommendations")

@ai_recommendations.route('/ai/api/recommendations')
def api_recommendations():
    """API endpoint for AI recommendations"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        recommendations = LearningAnalytics.get_learning_recommendations(user.id)
        return jsonify({
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_recommendations.route('/ai/api/study-patterns')
def api_study_patterns():
    """API endpoint for study pattern analysis"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        patterns = LearningAnalytics.get_study_pattern_insights(user.id)
        return jsonify(patterns)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_recommendations.route('/ai/api/topics-for-review')
def api_topics_for_review():
    """API endpoint for spaced repetition recommendations"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        client = get_supabase_client()
        
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Database not available'}), 500
        
        topics = get_topics_for_review(user.id, client)
        return jsonify({'topics': topics})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_recommendations.route('/ai/api/study-schedule')
def api_study_schedule():
    """API endpoint for optimal study schedule"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        client = get_supabase_client()
        
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Database not available'}), 500
        
        days = request.args.get('days', 7, type=int)
        schedule = get_study_schedule(user.id, client, days)
        return jsonify({'schedule': schedule})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_recommendations.route('/ai/api/topic-mastery/<topic_id>')
def api_topic_mastery(topic_id):
    """API endpoint for topic mastery analysis"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        mastery = LearningAnalytics.get_topic_mastery_level(topic_id, user.id)
        confidence_trend = LearningAnalytics.calculate_confidence_trends(user.id, topic_id)
        next_session_date = LearningAnalytics.recommend_next_session_date(topic_id, user.id)
        optimal_duration = LearningAnalytics.get_optimal_session_length(user.id, topic_id)
        
        return jsonify({
            'mastery': mastery,
            'confidence_trend': confidence_trend,
            'next_session_date': next_session_date.isoformat(),
            'optimal_duration': optimal_duration
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_topics_for_review(user_id, client):
    """Get topics that need review based on spaced repetition"""
    try:
       
        response = client.rpc('get_topics_for_review', {'p_user_id': user_id}).execute()
        
        if response.data:
            return response.data
        
       
        return calculate_topics_for_review_fallback(user_id, client)
    
    except Exception as e:
        print(f"Error getting topics for review: {e}")
        return calculate_topics_for_review_fallback(user_id, client)

def calculate_topics_for_review_fallback(user_id, client):
    """Fallback method to calculate topics for review"""
    try:
        
        topics_response = client.table('topics').select('*').eq('user_id', user_id).eq('is_active', True).execute()
        topics = topics_response.data if topics_response.data else []
        
        topics_for_review = []
        
        for topic in topics:
            
            sessions_response = client.table('study_sessions').select('*').eq('topic_id', topic['id']).eq('user_id', user_id).order('session_date', desc=True).limit(1).execute()
            
            if sessions_response.data:
                last_session = sessions_response.data[0]
                last_session_date = datetime.fromisoformat(last_session['session_date'].replace('Z', '+00:00')).date()
                days_since = (datetime.now().date() - last_session_date).days
                
            
                confidence_level = last_session.get('confidence_after', 5)
                
                # Calculate recommended interval based on confidence
                if confidence_level >= 8:
                    recommended_interval = 7
                elif confidence_level >= 6:
                    recommended_interval = 3
                elif confidence_level >= 4:
                    recommended_interval = 1
                else:
                    recommended_interval = 0
                
                # Check if review is needed
                if days_since >= recommended_interval:
                    topics_for_review.append({
                        'topic_id': topic['id'],
                        'title': topic['title'],
                        'days_since_last_session': days_since,
                        'mastery_level': min(5, max(1, int(confidence_level / 2))),
                        'recommended_interval': recommended_interval,
                        'confidence_level': confidence_level
                    })
            else:
                # No sessions yet - high priority
                topics_for_review.append({
                    'topic_id': topic['id'],
                    'title': topic['title'],
                    'days_since_last_session': 999,
                    'mastery_level': 1,
                    'recommended_interval': 0,
                    'confidence_level': 1
                })
        
        # Sort by priority (days overdue, then mastery level)
        topics_for_review.sort(key=lambda x: (x['days_since_last_session'] - x['recommended_interval'], -x['mastery_level']))
        
        return topics_for_review
    
    except Exception as e:
        print(f"Error in fallback calculation: {e}")
        return []

def get_study_schedule(user_id, client, days=7):
    """Get optimal study schedule for the next N days"""
    try:
       
        response = client.rpc('get_study_schedule', {'p_user_id': user_id, 'p_days': days}).execute()
        
        if response.data:
            return response.data
        
       
        return calculate_study_schedule_fallback(user_id, client, days)
    
    except Exception as e:
        print(f"Error getting study schedule: {e}")
        return calculate_study_schedule_fallback(user_id, client, days)

def calculate_study_schedule_fallback(user_id, client, days=7):
    """Fallback method to calculate study schedule"""
    try:
        
        topics_for_review = get_topics_for_review(user_id, client)
        
        schedule = []
        current_date = datetime.now().date()
        
        
        for i, topic in enumerate(topics_for_review[:days]):
            study_date = current_date + timedelta(days=i)
            
           
            priority_score = 100 - (topic['days_since_last_session'] - topic['recommended_interval'])
            priority_score = max(10, min(100, priority_score))
            
           
            if topic['mastery_level'] <= 2:
                recommended_duration = 45  # Longer for beginners
            elif topic['mastery_level'] <= 4:
                recommended_duration = 30  # Medium for intermediate
            else:
                recommended_duration = 20  # Shorter for advanced
            
            # Determine reason
            if topic['days_since_last_session'] > topic['recommended_interval'] * 2:
                reason = 'Overdue for review'
            elif topic['days_since_last_session'] >= topic['recommended_interval']:
                reason = 'Scheduled review'
            else:
                reason = 'Maintaining progress'
            
            schedule.append({
                'study_date': study_date.isoformat(),
                'topic_id': topic['topic_id'],
                'title': topic['title'],
                'priority_score': priority_score,
                'recommended_duration': recommended_duration,
                'reason': reason
            })
        
        return schedule
    
    except Exception as e:
        print(f"Error in fallback schedule calculation: {e}")
        return []

@ai_recommendations.route('/ai/api/learning-insights')
def api_learning_insights():
    """API endpoint for comprehensive learning insights"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        client = get_supabase_client()
        
        if not SUPABASE_AVAILABLE or not client:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get comprehensive insights
        insights = {
            'study_streak': LearningAnalytics.calculate_study_streak(user.id),
            'study_patterns': LearningAnalytics.get_study_pattern_insights(user.id),
            'topics_for_review': get_topics_for_review(user.id, client),
            'study_schedule': get_study_schedule(user.id, client, 7),
            'recommendations': LearningAnalytics.get_learning_recommendations(user.id)
        }
        
        return jsonify(insights)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

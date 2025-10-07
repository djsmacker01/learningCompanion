

from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from typing import List, Dict
from app.models.gamification import (
    UserProfile, Badge, UserBadge, Achievement, UserAchievement, 
    Leaderboard, GamificationEngine
)
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import json

gamification = Blueprint('gamification', __name__, url_prefix='/gamification')


@gamification.route('/')
@login_required
def gamification_dashboard():
    
    if not current_user.is_authenticated:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    
    profile = UserProfile.get_or_create_profile(current_user.id)
    if not profile:
        return jsonify({'error': 'Failed to load profile'}), 500
    
    
    user_badges = UserBadge.get_user_badges(current_user.id)
    user_achievements = UserAchievement.get_user_achievements(current_user.id)
    
    
    recent_xp = GamificationEngine._get_recent_xp_transactions(current_user.id, limit=10)
    
    return render_template('gamification/dashboard.html', 
                         profile=profile,
                         user_badges=user_badges,
                         user_achievements=user_achievements,
                         recent_xp=recent_xp)


@gamification.route('/badges')
def badges_page():
    
    if not current_user.is_authenticated:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    
    all_badges = Badge.get_all_badges()
    user_badges = UserBadge.get_user_badges(current_user.id)
    user_badge_ids = {badge.badge_id for badge in user_badges}
    
    
    profile = UserProfile.get_or_create_profile(current_user.id)
    
    return render_template('gamification/badges.html',
                         all_badges=all_badges,
                         user_badge_ids=user_badge_ids,
                         profile=profile)


@gamification.route('/achievements')
def achievements_page():
    
    if not current_user.is_authenticated:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    
    all_achievements = Achievement.get_all_achievements()
    user_achievements = UserAchievement.get_user_achievements(current_user.id)
    user_achievement_ids = {achievement.achievement_id for achievement in user_achievements}
    
    
    profile = UserProfile.get_or_create_profile(current_user.id)
    
    return render_template('gamification/achievements.html',
                         all_achievements=all_achievements,
                         user_achievement_ids=user_achievement_ids,
                         profile=profile)


@gamification.route('/leaderboard')
def leaderboard_page():
    
    if not current_user.is_authenticated:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    
    categories = ['total_xp', 'study_streak', 'quizzes_completed', 'study_time', 'topics_mastered']
    leaderboards = {}
    
    for category in categories:
        leaderboards[category] = Leaderboard.get_leaderboard(category, limit=10)
    
    
    user_ranks = {}
    profile = UserProfile.get_or_create_profile(current_user.id)
    
    if profile:
        for category in categories:
            user_ranks[category] = GamificationEngine._get_user_rank(user.id, category)
    
    return render_template('gamification/leaderboard.html',
                         leaderboards=leaderboards,
                         user_ranks=user_ranks,
                         profile=profile)


@gamification.route('/api/profile')
def api_user_profile():
    """Get user gamification profile data"""
    try:
        # Check authentication manually to return JSON error instead of redirect
        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401
        
        profile = UserProfile.get_or_create_profile(current_user.id)
        if not profile:
            return jsonify({'error': 'Failed to load profile'}), 500
        
        # Calculate level progress safely
        try:
            level_progress = GamificationEngine._calculate_level_progress(profile)
        except Exception as e:
            print(f"Error calculating level progress: {e}")
            level_progress = {
                'current_level': profile.current_level,
                'next_level': profile.current_level + 1,
                'progress_percentage': 0
            }
        
        # Calculate XP to next level safely
        try:
            xp_to_next = profile.get_xp_to_next_level()
        except Exception as e:
            print(f"Error calculating XP to next level: {e}")
            xp_to_next = 100  # Default fallback
        
        return jsonify({
            'user_id': profile.user_id,
            'total_xp': profile.total_xp,
            'current_level': profile.current_level,
            'study_streak': profile.study_streak,
            'longest_streak': profile.longest_streak,
            'total_study_time_minutes': profile.total_study_time_minutes,
            'badges_earned': profile.badges_earned,
            'achievements_unlocked': profile.achievements_unlocked,
            'quizzes_completed': profile.quizzes_completed,
            'topics_mastered': profile.topics_mastered,
            'xp_to_next_level': xp_to_next,
            'level_progress': level_progress
        })
    
    except Exception as e:
        print(f"Error in gamification API: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@gamification.route('/api/badges')
@login_required
def api_user_badges():
    
    user_badges = UserBadge.get_user_badges(current_user.id)
    
    badges_data = []
    for user_badge in user_badges:
        badge = Badge.get_badge_by_id(user_badge.badge_id)
        if badge:
            badges_data.append({
                'id': badge.id,
                'name': badge.name,
                'description': badge.description,
                'icon': badge.icon,
                'category': badge.category,
                'rarity': badge.rarity,
                'xp_reward': badge.xp_reward,
                'earned_at': user_badge.earned_at
            })
    
    return jsonify({'badges': badges_data})


@gamification.route('/api/achievements')
def api_user_achievements():
    
    if not current_user.is_authenticated:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    user_achievements = UserAchievement.get_user_achievements(current_user.id)
    
    achievements_data = []
    for user_achievement in user_achievements:
        achievement = Achievement.get_achievement_by_id(user_achievement.achievement_id)
        if achievement:
            achievements_data.append({
                'id': achievement.id,
                'name': achievement.name,
                'description': achievement.description,
                'icon': achievement.icon,
                'category': achievement.category,
                'xp_reward': achievement.xp_reward,
                'unlocked_at': user_achievement.unlocked_at,
                'progress': user_achievement.progress
            })
    
    return jsonify({'achievements': achievements_data})


@gamification.route('/api/leaderboard/<category>')
def api_leaderboard(category):
    
    period = request.args.get('period', 'all_time')
    limit = int(request.args.get('limit', 10))
    
    leaderboard_data = Leaderboard.get_leaderboard(category, period, limit)
    
    return jsonify({
        'category': category,
        'period': period,
        'leaderboard': leaderboard_data
    })


@gamification.route('/api/xp-history')
def api_xp_history():
    
    if not current_user.is_authenticated:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    limit = int(request.args.get('limit', 20))
    recent_xp = GamificationEngine._get_recent_xp_transactions(user.id, limit)
    
    return jsonify({'xp_transactions': recent_xp})


@gamification.route('/api/process-study-session', methods=['POST'])
def api_process_study_session():
    
    if not current_user.is_authenticated:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        data = request.get_json()
        duration_minutes = data.get('duration_minutes', 0)
        
        if duration_minutes <= 0:
            return jsonify({'error': 'Invalid duration'}), 400
        
        
        rewards = GamificationEngine.process_study_session(user.id, duration_minutes)
        
        return jsonify({
            'success': True,
            'rewards': rewards
        })
        
    except Exception as e:
        print(f"Error processing study session: {e}")
        return jsonify({'error': 'Failed to process study session'}), 500


@gamification.route('/api/process-quiz-completion', methods=['POST'])
def api_process_quiz_completion():
    
    if not current_user.is_authenticated:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        data = request.get_json()
        quiz_score = data.get('quiz_score', 0)
        time_taken_minutes = data.get('time_taken_minutes', 0)
        
        if quiz_score < 0 or quiz_score > 100:
            return jsonify({'error': 'Invalid quiz score'}), 400
        
        
        rewards = GamificationEngine.process_quiz_completion(user.id, quiz_score, time_taken_minutes)
        
        return jsonify({
            'success': True,
            'rewards': rewards
        })
        
    except Exception as e:
        print(f"Error processing quiz completion: {e}")
        return jsonify({'error': 'Failed to process quiz completion'}), 500


@gamification.route('/api/check-rewards')
def api_check_rewards():
    
    if not current_user.is_authenticated:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        
        new_badges = GamificationEngine._check_badges(user.id)
        new_achievements = GamificationEngine._check_achievements(user.id)
        
        return jsonify({
            'success': True,
            'new_badges': new_badges,
            'new_achievements': new_achievements
        })
        
    except Exception as e:
        print(f"Error checking rewards: {e}")
        return jsonify({'error': 'Failed to check rewards'}), 500



class GamificationEngine:
    
    
    @staticmethod
    def _get_recent_xp_transactions(user_id: str, limit: int = 10) -> List[Dict]:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('xp_transactions').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            print(f"Error getting XP transactions: {e}")
            return []
    
    @staticmethod
    def _get_user_rank(user_id: str, category: str, period: str = 'all_time') -> int:
        
        if not SUPABASE_AVAILABLE:
            return 0
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('leaderboards').select('rank').eq('user_id', user_id).eq('category', category).eq('period', period).execute()
            if result.data:
                return result.data[0]['rank']
        except Exception as e:
            print(f"Error getting user rank: {e}")
            
        return 0
    
    @staticmethod
    def _calculate_level_progress(profile: UserProfile) -> Dict:
        
        current_level_xp = UserProfile.get_xp_for_level(profile.current_level)
        next_level_xp = UserProfile.get_xp_for_level(profile.current_level + 1)
        
        progress_xp = profile.total_xp - current_level_xp
        total_xp_needed = next_level_xp - current_level_xp
        
        progress_percentage = (progress_xp / total_xp_needed * 100) if total_xp_needed > 0 else 100
        
        return {
            'current_xp': progress_xp,
            'total_xp_needed': total_xp_needed,
            'progress_percentage': min(100, max(0, progress_percentage))
        }


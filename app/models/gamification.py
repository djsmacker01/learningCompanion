

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import json


class UserProfile:
    
    
    def __init__(self, id=None, user_id=None, total_xp=0, current_level=1, 
                 study_streak=0, longest_streak=0, total_study_time_minutes=0,
                 badges_earned=0, achievements_unlocked=0, quizzes_completed=0,
                 topics_mastered=0, last_activity_date=None, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.total_xp = total_xp
        self.current_level = current_level
        self.study_streak = study_streak
        self.longest_streak = longest_streak
        self.total_study_time_minutes = total_study_time_minutes
        self.badges_earned = badges_earned
        self.achievements_unlocked = achievements_unlocked
        self.quizzes_completed = quizzes_completed
        self.topics_mastered = topics_mastered
        self.last_activity_date = last_activity_date
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_or_create_profile(cls, user_id: str) -> 'UserProfile':
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            

            result = supabase.table('user_profiles').select(
                'id, user_id, total_xp, current_level, study_streak, longest_streak, '
                'total_study_time_minutes, badges_earned, achievements_unlocked, '
                'quizzes_completed, topics_mastered, last_activity_date, created_at, updated_at'
            ).eq('user_id', user_id).execute()
            
            if result.data:
                profile_data = result.data[0]
                return cls(**profile_data)
            
            
            profile_data = {
                'user_id': user_id,
                'total_xp': 0,
                'current_level': 1,
                'study_streak': 0,
                'longest_streak': 0,
                'total_study_time_minutes': 0,
                'badges_earned': 0,
                'achievements_unlocked': 0,
                'quizzes_completed': 0,
                'topics_mastered': 0,
                'last_activity_date': date.today().isoformat()
            }
            
            result = supabase.table('user_profiles').insert(profile_data).execute()
            if result.data:
                profile_data = result.data[0]
                return cls(**profile_data)
        except Exception as e:
            print(f"Error getting/creating user profile: {e}")
            
        return None

    def add_xp(self, amount: int, source: str, source_id: str = None, description: str = None) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            transaction_data = {
                'user_id': self.user_id,
                'amount': amount,
                'source': source,
                'source_id': source_id,
                'description': description
            }
            
            supabase.table('xp_transactions').insert(transaction_data).execute()
            
            
            new_total_xp = self.total_xp + amount
            new_level = self.calculate_level(new_total_xp)
            
            update_data = {
                'total_xp': new_total_xp,
                'current_level': new_level
            }
            
            result = supabase.table('user_profiles').update(update_data).eq('id', self.id).execute()
            if result.data:
                self.total_xp = new_total_xp
                self.current_level = new_level
                return True
        except Exception as e:
            print(f"Error adding XP: {e}")
            
        return False

    def update_study_streak(self, new_streak: int) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            update_data = {
                'study_streak': new_streak,
                'longest_streak': max(self.longest_streak, new_streak),
                'last_activity_date': date.today().isoformat()
            }
            
            result = supabase.table('user_profiles').update(update_data).eq('id', self.id).execute()
            if result.data:
                self.study_streak = new_streak
                self.longest_streak = max(self.longest_streak, new_streak)
                self.last_activity_date = date.today()
                return True
        except Exception as e:
            print(f"Error updating study streak: {e}")
            
        return False

    def add_study_time(self, minutes: int) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            new_total_time = self.total_study_time_minutes + minutes
            
            update_data = {
                'total_study_time_minutes': new_total_time
            }
            
            result = supabase.table('user_profiles').update(update_data).eq('id', self.id).execute()
            if result.data:
                self.total_study_time_minutes = new_total_time
                return True
        except Exception as e:
            print(f"Error adding study time: {e}")
            
        return False

    @staticmethod
    def calculate_level(total_xp: int) -> int:
        
        
        return int((total_xp / 100) ** 0.5) + 1

    @staticmethod
    def get_xp_for_level(level: int) -> int:
        
        return (level - 1) ** 2 * 100

    def get_xp_to_next_level(self) -> int:
        
        next_level_xp = self.get_xp_for_level(self.current_level + 1)
        return next_level_xp - self.total_xp


class Badge:
    
    
    def __init__(self, id=None, name=None, description=None, icon=None, category=None,
                 rarity=None, xp_reward=10, requirements=None, is_active=True, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category
        self.rarity = rarity
        self.xp_reward = xp_reward
        self.requirements = requirements
        self.is_active = is_active
        self.created_at = created_at

    @classmethod
    def get_all_badges(cls) -> List['Badge']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('badges').select('*').eq('is_active', True).order('category').order('name').execute()
            return [cls(**badge) for badge in result.data]
        except Exception as e:
            print(f"Error getting badges: {e}")
            return []

    @classmethod
    def get_badge_by_id(cls, badge_id: str) -> Optional['Badge']:
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('badges').select('*').eq('id', badge_id).eq('is_active', True).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error getting badge by ID: {e}")
            
        return None

    def check_requirements(self, user_id: str) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            profile_result = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
            if not profile_result.data:
                return False
                
            profile = profile_result.data[0]
            
            
            for requirement, value in self.requirements.items():
                if requirement == 'study_sessions':
                    
                    sessions_result = supabase.table('study_sessions').select('id').eq('user_id', user_id).execute()
                    if len(sessions_result.data) < value:
                        return False
                elif requirement == 'study_streak':
                    if profile['study_streak'] < value:
                        return False
                elif requirement == 'quizzes_completed':
                    if profile['quizzes_completed'] < value:
                        return False
                elif requirement == 'topics_mastered':
                    if profile['topics_mastered'] < value:
                        return False
                elif requirement == 'quiz_score':
                    
                    attempts_result = supabase.table('quiz_attempts').select('score').eq('user_id', user_id).eq('status', 'completed').execute()
                    perfect_scores = sum(1 for attempt in attempts_result.data if attempt['score'] >= value)
                    if perfect_scores < 1:  
                        return False
                elif requirement == 'quiz_time_under':
                    
                    attempts_result = supabase.table('quiz_attempts').select('time_taken_minutes').eq('user_id', user_id).eq('status', 'completed').execute()
                    fast_completions = sum(1 for attempt in attempts_result.data if attempt['time_taken_minutes'] * 60 < value)
                    if fast_completions < 1:
                        return False
                elif requirement == 'session_duration':
                    
                    sessions_result = supabase.table('study_sessions').select('duration_minutes').eq('user_id', user_id).execute()
                    long_sessions = sum(1 for session in sessions_result.data if session['duration_minutes'] >= value)
                    if long_sessions < 1:
                        return False
                        
            return True
        except Exception as e:
            print(f"Error checking badge requirements: {e}")
            return False


class UserBadge:
    
    
    def __init__(self, id=None, user_id=None, badge_id=None, earned_at=None):
        self.id = id
        self.user_id = user_id
        self.badge_id = badge_id
        self.earned_at = earned_at

    @classmethod
    def get_user_badges(cls, user_id: str) -> List['UserBadge']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('user_badges').select('*, badges(*)').eq('user_id', user_id).order('earned_at', desc=True).execute()
            return [cls(**badge) for badge in result.data]
        except Exception as e:
            print(f"Error getting user badges: {e}")
            return []

    @classmethod
    def award_badge(cls, user_id: str, badge_id: str) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            existing = supabase.table('user_badges').select('id').eq('user_id', user_id).eq('badge_id', badge_id).execute()
            if existing.data:
                return True  
                
            
            badge_data = {
                'user_id': user_id,
                'badge_id': badge_id,
                'earned_at': datetime.now().isoformat()
            }
            
            result = supabase.table('user_badges').insert(badge_data).execute()
            if result.data:
                
                badge_count_result = supabase.table('user_badges').select('id').eq('user_id', user_id).execute()
                badge_count = len(badge_count_result.data) if badge_count_result.data else 0
                supabase.table('user_profiles').update({'badges_earned': badge_count}).eq('user_id', user_id).execute()
                return True
        except Exception as e:
            print(f"Error awarding badge: {e}")
            
        return False


class Achievement:
    
    
    def __init__(self, id=None, name=None, description=None, icon=None, category=None,
                 xp_reward=25, requirements=None, is_active=True, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category
        self.xp_reward = xp_reward
        self.requirements = requirements
        self.is_active = is_active
        self.created_at = created_at

    @classmethod
    def get_all_achievements(cls) -> List['Achievement']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('achievements').select('*').eq('is_active', True).order('category').order('name').execute()
            return [cls(**achievement) for achievement in result.data]
        except Exception as e:
            print(f"Error getting achievements: {e}")
            return []

    @classmethod
    def get_achievement_by_id(cls, achievement_id: str) -> Optional['Achievement']:
        
        if not SUPABASE_AVAILABLE:
            return None
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('achievements').select('*').eq('id', achievement_id).eq('is_active', True).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error getting achievement by ID: {e}")
            
        return None

    def check_requirements(self, user_id: str) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            profile_result = supabase.table('user_profiles').select('*').eq('user_id', user_id).execute()
            if not profile_result.data:
                return False
                
            profile = profile_result.data[0]
            
            
            for requirement, value in self.requirements.items():
                if requirement == 'consecutive_days':
                    if profile['study_streak'] < value:
                        return False
                elif requirement == 'total_hours':
                    if profile['total_study_time_minutes'] / 60 < value:
                        return False
                elif requirement == 'sessions_per_day':
                    
                    sessions_result = supabase.table('study_sessions').select('id').eq('user_id', user_id).gte('created_at', '2025-09-14').execute()
                    if len(sessions_result.data) < value:
                        return False
                elif requirement == 'high_scores':
                    
                    attempts_result = supabase.table('quiz_attempts').select('score').eq('user_id', user_id).eq('status', 'completed').execute()
                    high_scores = sum(1 for attempt in attempts_result.data if attempt['score'] >= 90)
                    if high_scores < value:
                        return False
                elif requirement == 'perfect_scores':
                    
                    attempts_result = supabase.table('quiz_attempts').select('score').eq('user_id', user_id).eq('status', 'completed').execute()
                    perfect_scores = sum(1 for attempt in attempts_result.data if attempt['score'] == 100)
                    if perfect_scores < value:
                        return False
                elif requirement == 'quizzes_per_week':
                    
                    if profile['quizzes_completed'] < value:
                        return False
                elif requirement == 'topics_mastered':
                    if profile['topics_mastered'] < value:
                        return False
                elif requirement == 'quizzes_created':
                    
                    quizzes_result = supabase.table('quizzes').select('id').eq('user_id', user_id).execute()
                    if len(quizzes_result.data) < value:
                        return False
                elif requirement == 'flashcards_reviewed':
                    
                    reviews_result = supabase.table('flashcard_progress').select('id').eq('user_id', user_id).execute()
                    if len(reviews_result.data) < value:
                        return False
                elif requirement == 'study_streak':
                    if profile['study_streak'] < value:
                        return False
                        
            return True
        except Exception as e:
            print(f"Error checking achievement requirements: {e}")
            return False


class UserAchievement:
    
    
    def __init__(self, id=None, user_id=None, achievement_id=None, unlocked_at=None, progress=None):
        self.id = id
        self.user_id = user_id
        self.achievement_id = achievement_id
        self.unlocked_at = unlocked_at
        self.progress = progress or {}

    @classmethod
    def get_user_achievements(cls, user_id: str) -> List['UserAchievement']:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('user_achievements').select('*, achievements(*)').eq('user_id', user_id).order('unlocked_at', desc=True).execute()
            return [cls(**achievement) for achievement in result.data]
        except Exception as e:
            print(f"Error getting user achievements: {e}")
            return []

    @classmethod
    def unlock_achievement(cls, user_id: str, achievement_id: str) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            existing = supabase.table('user_achievements').select('id').eq('user_id', user_id).eq('achievement_id', achievement_id).execute()
            if existing.data:
                return True  
                
            
            achievement_data = {
                'user_id': user_id,
                'achievement_id': achievement_id,
                'unlocked_at': datetime.now().isoformat(),
                'progress': {}
            }
            
            result = supabase.table('user_achievements').insert(achievement_data).execute()
            if result.data:
                
                achievement_count_result = supabase.table('user_achievements').select('id').eq('user_id', user_id).execute()
                achievement_count = len(achievement_count_result.data) if achievement_count_result.data else 0
                supabase.table('user_profiles').update({'achievements_unlocked': achievement_count}).eq('user_id', user_id).execute()
                return True
        except Exception as e:
            print(f"Error unlocking achievement: {e}")
            
        return False


class Leaderboard:
    
    
    @staticmethod
    def get_leaderboard(category: str, period: str = 'all_time', limit: int = 10) -> List[Dict]:
        
        if not SUPABASE_AVAILABLE:
            return []
            
        supabase = get_supabase_client()
        
        try:
            
            result = supabase.table('leaderboards').select('*, users(email)').eq('category', category).eq('period', period).order('rank').limit(limit).execute()
            return result.data
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []

    @staticmethod
    def update_leaderboard(user_id: str, category: str, value: int, period: str = 'all_time') -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            leaderboard_data = {
                'user_id': user_id,
                'category': category,
                'value': value,
                'period': period,
                'rank': 1,  
                'updated_at': datetime.now().isoformat()
            }
            
            
            existing = supabase.table('leaderboards').select('id').eq('user_id', user_id).eq('category', category).eq('period', period).execute()
            
            if existing.data:
                
                supabase.table('leaderboards').update(leaderboard_data).eq('id', existing.data[0]['id']).execute()
            else:
                
                supabase.table('leaderboards').insert(leaderboard_data).execute()
            
            
            Leaderboard._recalculate_ranks(category, period)
            return True
        except Exception as e:
            print(f"Error updating leaderboard: {e}")
            return False

    @staticmethod
    def _recalculate_ranks(category: str, period: str) -> bool:
        
        if not SUPABASE_AVAILABLE:
            return False
            
        supabase = get_supabase_client()
        
        try:
            
            result = supabase.table('leaderboards').select('id, value').eq('category', category).eq('period', period).order('value', desc=True).execute()
            
            
            for rank, entry in enumerate(result.data, 1):
                supabase.table('leaderboards').update({'rank': rank}).eq('id', entry['id']).execute()
                
            return True
        except Exception as e:
            print(f"Error recalculating ranks: {e}")
            return False


class GamificationEngine:
    
    
    @staticmethod
    def process_study_session(user_id: str, session_duration_minutes: int) -> Dict:
        
        rewards = {
            'xp_earned': 0,
            'badges_earned': [],
            'achievements_unlocked': [],
            'level_up': False
        }
        
        try:
            
            profile = UserProfile.get_or_create_profile(user_id)
            if not profile:
                return rewards
            
            
            xp_earned = session_duration_minutes
            old_level = profile.current_level
            
            
            if profile.add_xp(xp_earned, 'study_session', description=f'Studied for {session_duration_minutes} minutes'):
                rewards['xp_earned'] = xp_earned
                
                
                if profile.current_level > old_level:
                    rewards['level_up'] = True
                    
                    level_bonus = profile.current_level * 10
                    profile.add_xp(level_bonus, 'level_up', description=f'Leveled up to level {profile.current_level}')
                    rewards['xp_earned'] += level_bonus
            
            
            profile.add_study_time(session_duration_minutes)
            
            
            GamificationEngine._update_study_streak(profile)
            
            
            rewards['badges_earned'] = GamificationEngine._check_badges(user_id)
            rewards['achievements_unlocked'] = GamificationEngine._check_achievements(user_id)
            
            
            GamificationEngine._update_leaderboards(user_id)
            
        except Exception as e:
            print(f"Error processing study session: {e}")
            
        return rewards

    @staticmethod
    def process_quiz_completion(user_id: str, quiz_score: int, time_taken_minutes: int) -> Dict:
        
        rewards = {
            'xp_earned': 0,
            'badges_earned': [],
            'achievements_unlocked': [],
            'level_up': False
        }
        
        try:
            
            profile = UserProfile.get_or_create_profile(user_id)
            if not profile:
                return rewards
            
            
            base_xp = 20  
            score_bonus = int(quiz_score * 0.3)  
            time_bonus = max(0, 10 - time_taken_minutes)  
            
            xp_earned = base_xp + score_bonus + time_bonus
            old_level = profile.current_level
            
            
            if profile.add_xp(xp_earned, 'quiz_completion', description=f'Completed quiz with {quiz_score}% score'):
                rewards['xp_earned'] = xp_earned
                
                
                if profile.current_level > old_level:
                    rewards['level_up'] = True
            
            
            supabase = get_supabase_client()
            supabase.table('user_profiles').update({'quizzes_completed': profile.quizzes_completed + 1}).eq('user_id', user_id).execute()
            
            
            rewards['badges_earned'] = GamificationEngine._check_badges(user_id)
            rewards['achievements_unlocked'] = GamificationEngine._check_achievements(user_id)
            
            
            GamificationEngine._update_leaderboards(user_id)
            
        except Exception as e:
            print(f"Error processing quiz completion: {e}")
            
        return rewards

    @staticmethod
    def _update_study_streak(profile: UserProfile) -> None:
        
        today = date.today()
        last_activity = profile.last_activity_date
        
        if isinstance(last_activity, str):
            last_activity = datetime.fromisoformat(last_activity).date()
        
        if last_activity == today:
            
            return
        elif last_activity == today - timedelta(days=1):
            
            profile.update_study_streak(profile.study_streak + 1)
        else:
            
            profile.update_study_streak(1)

    @staticmethod
    def _check_badges(user_id: str) -> List[str]:
        
        new_badges = []
        
        try:
            badges = Badge.get_all_badges()
            user_badges = UserBadge.get_user_badges(user_id)
            user_badge_ids = {badge.badge_id for badge in user_badges}
            
            for badge in badges:
                if badge.id not in user_badge_ids and badge.check_requirements(user_id):
                    if UserBadge.award_badge(user_id, badge.id):
                        new_badges.append(badge.name)
                        
                        profile = UserProfile.get_or_create_profile(user_id)
                        if profile:
                            profile.add_xp(badge.xp_reward, 'badge_earned', badge.id, f'Earned badge: {badge.name}')
                            
        except Exception as e:
            print(f"Error checking badges: {e}")
            
        return new_badges

    @staticmethod
    def _check_achievements(user_id: str) -> List[str]:
        
        new_achievements = []
        
        try:
            achievements = Achievement.get_all_achievements()
            user_achievements = UserAchievement.get_user_achievements(user_id)
            user_achievement_ids = {achievement.achievement_id for achievement in user_achievements}
            
            for achievement in achievements:
                if achievement.id not in user_achievement_ids and achievement.check_requirements(user_id):
                    if UserAchievement.unlock_achievement(user_id, achievement.id):
                        new_achievements.append(achievement.name)
                        
                        profile = UserProfile.get_or_create_profile(user_id)
                        if profile:
                            profile.add_xp(achievement.xp_reward, 'achievement_unlocked', achievement.id, f'Unlocked achievement: {achievement.name}')
                            
        except Exception as e:
            print(f"Error checking achievements: {e}")
            
        return new_achievements

    @staticmethod
    def _update_leaderboards(user_id: str) -> None:
        
        try:
            profile = UserProfile.get_or_create_profile(user_id)
            if not profile:
                return
                
            
            Leaderboard.update_leaderboard(user_id, 'total_xp', profile.total_xp)
            Leaderboard.update_leaderboard(user_id, 'study_streak', profile.study_streak)
            Leaderboard.update_leaderboard(user_id, 'quizzes_completed', profile.quizzes_completed)
            Leaderboard.update_leaderboard(user_id, 'study_time', profile.total_study_time_minutes)
            Leaderboard.update_leaderboard(user_id, 'topics_mastered', profile.topics_mastered)
            
        except Exception as e:
            print(f"Error updating leaderboards: {e}")

    @staticmethod
    def _calculate_level_progress(profile: UserProfile) -> Dict:
        """Calculate level progress for a user profile"""
        try:
            current_level_xp = UserProfile.get_xp_for_level(profile.current_level)
            next_level_xp = UserProfile.get_xp_for_level(profile.current_level + 1)
            
            # Calculate progress within current level
            xp_in_current_level = profile.total_xp - current_level_xp
            xp_needed_for_next_level = next_level_xp - current_level_xp
            
            if xp_needed_for_next_level <= 0:
                progress_percentage = 100
            else:
                progress_percentage = min(100, (xp_in_current_level / xp_needed_for_next_level) * 100)
            
            return {
                'current_level': profile.current_level,
                'next_level': profile.current_level + 1,
                'current_level_xp': current_level_xp,
                'next_level_xp': next_level_xp,
                'xp_in_current_level': xp_in_current_level,
                'xp_needed_for_next_level': xp_needed_for_next_level,
                'progress_percentage': round(progress_percentage, 1)
            }
        except Exception as e:
            print(f"Error calculating level progress: {e}")
            return {
                'current_level': 1,
                'next_level': 2,
                'current_level_xp': 0,
                'next_level_xp': 100,
                'xp_in_current_level': 0,
                'xp_needed_for_next_level': 100,
                'progress_percentage': 0
            }


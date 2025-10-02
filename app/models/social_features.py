"""
Social Features Models
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import uuid
import json


class Friend:
    """Model for friend connections"""
    
    def __init__(self, id=None, user_id=None, friend_id=None, status='pending', 
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.friend_id = friend_id
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def send_friend_request(cls, friend_id: str):
        """Send a friend request"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            response = client.rpc('send_friend_request', {
                'p_friend_id': friend_id
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error sending friend request: {e}")
            return False
    
    @classmethod
    def accept_friend_request(cls, user_id: str):
        """Accept a friend request"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            response = client.rpc('accept_friend_request', {
                'p_user_id': user_id
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error accepting friend request: {e}")
            return False
    
    @classmethod
    def get_friends(cls, user_id: str, status: str = 'accepted'):
        """Get friends for a user"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('friends').select('*').eq('user_id', user_id).eq('status', status).execute()
            
            friends = []
            for data in response.data:
                friend = cls(
                    id=data['id'],
                    user_id=data['user_id'],
                    friend_id=data['friend_id'],
                    status=data['status'],
                    created_at=datetime.fromisoformat(data['created_at']),
                    updated_at=datetime.fromisoformat(data['updated_at'])
                )
                friends.append(friend)
            
            return friends
        except Exception as e:
            print(f"Error getting friends: {e}")
            return []
    
    @classmethod
    def get_pending_requests(cls, user_id: str):
        """Get pending friend requests for a user"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('friends').select('*').eq('friend_id', user_id).eq('status', 'pending').execute()
            
            requests = []
            for data in response.data:
                request = cls(
                    id=data['id'],
                    user_id=data['user_id'],
                    friend_id=data['friend_id'],
                    status=data['status'],
                    created_at=datetime.fromisoformat(data['created_at']),
                    updated_at=datetime.fromisoformat(data['updated_at'])
                )
                requests.append(request)
            
            return requests
        except Exception as e:
            print(f"Error getting pending requests: {e}")
            return []


class StudyGroup:
    """Model for study groups"""
    
    def __init__(self, id=None, name=None, description=None, creator_id=None,
                 is_public=True, max_members=50, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.creator_id = creator_id
        self.is_public = is_public
        self.max_members = max_members
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def create_group(cls, name: str, description: str, creator_id: str, 
                     is_public: bool = True, max_members: int = 50):
        """Create a new study group"""
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            data = {
                'name': name,
                'description': description,
                'creator_id': creator_id,
                'is_public': is_public,
                'max_members': max_members,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            result = client.table('study_groups').insert(data).execute()
            if result.data:
                group = cls(**result.data[0])
                # Add creator as admin member
                StudyGroupMember.add_member(group.id, creator_id, 'admin')
                return group
        except Exception as e:
            print(f"Error creating study group: {e}")
        
        return None
    
    @classmethod
    def get_public_groups(cls, limit: int = 20):
        """Get public study groups"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('study_groups').select('*').eq('is_public', True).order('created_at', desc=True).limit(limit).execute()
            
            groups = []
            for data in response.data:
                group = cls(
                    id=data['id'],
                    name=data['name'],
                    description=data['description'],
                    creator_id=data['creator_id'],
                    is_public=data['is_public'],
                    max_members=data['max_members'],
                    created_at=datetime.fromisoformat(data['created_at']),
                    updated_at=datetime.fromisoformat(data['updated_at'])
                )
                groups.append(group)
            
            return groups
        except Exception as e:
            print(f"Error getting public groups: {e}")
            return []
    
    @classmethod
    def get_user_groups(cls, user_id: str):
        """Get groups a user is a member of"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            # Get group IDs where user is a member
            member_response = client.table('study_group_members').select('group_id').eq('user_id', user_id).eq('status', 'active').execute()
            
            if not member_response.data:
                return []
            
            group_ids = [member['group_id'] for member in member_response.data]
            
            # Get group details
            response = client.table('study_groups').select('*').in_('id', group_ids).execute()
            
            groups = []
            for data in response.data:
                group = cls(
                    id=data['id'],
                    name=data['name'],
                    description=data['description'],
                    creator_id=data['creator_id'],
                    is_public=data['is_public'],
                    max_members=data['max_members'],
                    created_at=datetime.fromisoformat(data['created_at']),
                    updated_at=datetime.fromisoformat(data['updated_at'])
                )
                groups.append(group)
            
            return groups
        except Exception as e:
            print(f"Error getting user groups: {e}")
            return []
    
    @classmethod
    def join_group(cls, group_id: str):
        """Join a study group"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            response = client.rpc('join_study_group', {
                'p_group_id': group_id
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error joining group: {e}")
            return False


class StudyGroupMember:
    """Model for study group members"""
    
    def __init__(self, id=None, group_id=None, user_id=None, role='member',
                 joined_at=None, status='active'):
        self.id = id
        self.group_id = group_id
        self.user_id = user_id
        self.role = role
        self.joined_at = joined_at or datetime.utcnow()
        self.status = status
    
    @classmethod
    def add_member(cls, group_id: str, user_id: str, role: str = 'member'):
        """Add a member to a study group"""
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            data = {
                'group_id': group_id,
                'user_id': user_id,
                'role': role,
                'joined_at': datetime.utcnow().isoformat(),
                'status': 'active'
            }
            
            result = client.table('study_group_members').insert(data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error adding group member: {e}")
        
        return None
    
    @classmethod
    def get_group_members(cls, group_id: str):
        """Get all members of a study group"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('study_group_members').select('*').eq('group_id', group_id).eq('status', 'active').execute()
            
            members = []
            for data in response.data:
                member = cls(
                    id=data['id'],
                    group_id=data['group_id'],
                    user_id=data['user_id'],
                    role=data['role'],
                    joined_at=datetime.fromisoformat(data['joined_at']),
                    status=data['status']
                )
                members.append(member)
            
            return members
        except Exception as e:
            print(f"Error getting group members: {e}")
            return []


class SocialChallenge:
    """Model for social challenges"""
    
    def __init__(self, id=None, title=None, description=None, challenge_type=None,
                 target_value=None, target_unit=None, creator_id=None, group_id=None,
                 start_date=None, end_date=None, is_active=True, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.challenge_type = challenge_type
        self.target_value = target_value
        self.target_unit = target_unit
        self.creator_id = creator_id
        self.group_id = group_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
    
    @classmethod
    def create_challenge(cls, title: str, description: str, challenge_type: str,
                        target_value: int, target_unit: str, creator_id: str,
                        group_id: str = None, start_date: datetime = None,
                        end_date: datetime = None):
        """Create a new social challenge"""
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            if not start_date:
                start_date = datetime.utcnow()
            if not end_date:
                end_date = start_date.replace(day=start_date.day + 7)  # Default 7 days
            
            data = {
                'title': title,
                'description': description,
                'challenge_type': challenge_type,
                'target_value': target_value,
                'target_unit': target_unit,
                'creator_id': creator_id,
                'group_id': group_id,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'is_active': True,
                'created_at': datetime.utcnow().isoformat()
            }
            
            result = client.table('social_challenges').insert(data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error creating challenge: {e}")
        
        return None
    
    @classmethod
    def get_active_challenges(cls, group_id: str = None):
        """Get active challenges"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            query = client.table('social_challenges').select('*').eq('is_active', True)
            
            if group_id:
                query = query.eq('group_id', group_id)
            else:
                query = query.is_('group_id', 'null')
            
            response = query.order('created_at', desc=True).execute()
            
            challenges = []
            for data in response.data:
                challenge = cls(
                    id=data['id'],
                    title=data['title'],
                    description=data['description'],
                    challenge_type=data['challenge_type'],
                    target_value=data['target_value'],
                    target_unit=data['target_unit'],
                    creator_id=data['creator_id'],
                    group_id=data.get('group_id'),
                    start_date=datetime.fromisoformat(data['start_date']),
                    end_date=datetime.fromisoformat(data['end_date']),
                    is_active=data['is_active'],
                    created_at=datetime.fromisoformat(data['created_at'])
                )
                challenges.append(challenge)
            
            return challenges
        except Exception as e:
            print(f"Error getting active challenges: {e}")
            return []
    
    @classmethod
    def join_challenge(cls, challenge_id: str):
        """Join a challenge"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            response = client.rpc('join_challenge', {
                'p_challenge_id': challenge_id
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error joining challenge: {e}")
            return False


class ChallengeParticipant:
    """Model for challenge participants"""
    
    def __init__(self, id=None, challenge_id=None, user_id=None, joined_at=None,
                 current_progress=0, is_completed=False, completed_at=None):
        self.id = id
        self.challenge_id = challenge_id
        self.user_id = user_id
        self.joined_at = joined_at or datetime.utcnow()
        self.current_progress = current_progress
        self.is_completed = is_completed
        self.completed_at = completed_at
    
    @classmethod
    def update_progress(cls, challenge_id: str, progress: int):
        """Update challenge progress"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            response = client.rpc('update_challenge_progress', {
                'p_challenge_id': challenge_id,
                'p_progress': progress
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error updating challenge progress: {e}")
            return False
    
    @classmethod
    def get_user_participations(cls, user_id: str):
        """Get user's challenge participations"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('challenge_participants').select('*').eq('user_id', user_id).execute()
            
            participations = []
            for data in response.data:
                participation = cls(
                    id=data['id'],
                    challenge_id=data['challenge_id'],
                    user_id=data['user_id'],
                    joined_at=datetime.fromisoformat(data['joined_at']),
                    current_progress=data['current_progress'],
                    is_completed=data['is_completed'],
                    completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None
                )
                participations.append(participation)
            
            return participations
        except Exception as e:
            print(f"Error getting user participations: {e}")
            return []


class SocialAchievement:
    """Model for social achievements"""
    
    def __init__(self, id=None, user_id=None, achievement_type=None,
                 achievement_data=None, is_shared=False, shared_at=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.achievement_type = achievement_type
        self.achievement_data = achievement_data or {}
        self.is_shared = is_shared
        self.shared_at = shared_at
        self.created_at = created_at or datetime.utcnow()
    
    @classmethod
    def create_achievement(cls, user_id: str, achievement_type: str,
                          achievement_data: dict, is_shared: bool = False):
        """Create a new social achievement"""
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            data = {
                'user_id': user_id,
                'achievement_type': achievement_type,
                'achievement_data': json.dumps(achievement_data),
                'is_shared': is_shared,
                'shared_at': datetime.utcnow().isoformat() if is_shared else None,
                'created_at': datetime.utcnow().isoformat()
            }
            
            result = client.table('social_achievements').insert(data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error creating achievement: {e}")
        
        return None
    
    @classmethod
    def get_user_achievements(cls, user_id: str, is_shared: bool = None):
        """Get user's achievements"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            query = client.table('social_achievements').select('*').eq('user_id', user_id)
            
            if is_shared is not None:
                query = query.eq('is_shared', is_shared)
            
            response = query.order('created_at', desc=True).execute()
            
            achievements = []
            for data in response.data:
                achievement = cls(
                    id=data['id'],
                    user_id=data['user_id'],
                    achievement_type=data['achievement_type'],
                    achievement_data=json.loads(data['achievement_data']) if data['achievement_data'] else {},
                    is_shared=data['is_shared'],
                    shared_at=datetime.fromisoformat(data['shared_at']) if data.get('shared_at') else None,
                    created_at=datetime.fromisoformat(data['created_at'])
                )
                achievements.append(achievement)
            
            return achievements
        except Exception as e:
            print(f"Error getting user achievements: {e}")
            return []


class SocialActivity:
    """Model for social activity feed"""
    
    def __init__(self, id=None, user_id=None, activity_type=None, activity_data=None,
                 target_user_id=None, group_id=None, is_public=True, created_at=None):
        self.id = id
        self.user_id = user_id
        self.activity_type = activity_type
        self.activity_data = activity_data or {}
        self.target_user_id = target_user_id
        self.group_id = group_id
        self.is_public = is_public
        self.created_at = created_at or datetime.utcnow()
    
    @classmethod
    def get_user_activity(cls, user_id: str, limit: int = 20):
        """Get user's activity feed"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('social_activity').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
            
            activities = []
            for data in response.data:
                activity = cls(
                    id=data['id'],
                    user_id=data['user_id'],
                    activity_type=data['activity_type'],
                    activity_data=json.loads(data['activity_data']) if data['activity_data'] else {},
                    target_user_id=data.get('target_user_id'),
                    group_id=data.get('group_id'),
                    is_public=data['is_public'],
                    created_at=datetime.fromisoformat(data['created_at'])
                )
                activities.append(activity)
            
            return activities
        except Exception as e:
            print(f"Error getting user activity: {e}")
            return []

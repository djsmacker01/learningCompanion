from datetime import datetime
from flask_login import UserMixin
from supabase import create_client, Client
from config import Config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global variables for Supabase client
supabase = None
SUPABASE_AVAILABLE = False

def get_supabase_client():
    """Get Supabase client, initializing if necessary"""
    global supabase, SUPABASE_AVAILABLE
    
    if supabase is None:
        try:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
            
            if not supabase_url or not supabase_key:
                print("❌ Supabase credentials not found in environment variables")
                SUPABASE_AVAILABLE = False
                return None
            
            supabase = create_client(supabase_url, supabase_key)
            SUPABASE_AVAILABLE = True
            print("✅ Supabase connected with service role key (RLS bypassed)")
        except Exception as e:
            print(f"❌ Supabase not available: {e}")
            supabase = None
            SUPABASE_AVAILABLE = False
    
    return supabase

# Initialize Supabase client
get_supabase_client()

# In-memory storage for testing without Supabase
_in_memory_topics = []
_next_topic_id = 1

class User(UserMixin):
    def __init__(self, id, email, name=None):
        self.id = id
        self.email = email
        self.name = name
    
    @staticmethod
    def get(user_id):
        try:
            response = supabase.table('users').select('*').eq('id', user_id).execute()
            if response.data:
                user_data = response.data[0]
                return User(user_data['id'], user_data['email'], user_data.get('name'))
            return None
        except Exception as e:
            print(f"Error loading user: {e}")
            return None

class Topic:
    def __init__(self, id, title, description, user_id, created_at=None, is_active=True, 
                 share_code=None, is_shared=False, shared_at=None, notes=None, 
                 tags=None, version=1, last_modified=None):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.is_active = is_active
        self.share_code = share_code
        self.is_shared = is_shared
        self.shared_at = shared_at
        self.notes = notes
        self.tags = tags or []
        self.version = version
        self.last_modified = last_modified or datetime.utcnow()
    
    @staticmethod
    def create(title, description, user_id):
        """Create a new topic"""
        print(f"=== TOPIC.CREATE METHOD CALLED ===")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"User ID: {user_id}")
        
        # Get Supabase client dynamically
        client = get_supabase_client()
        print(f"Supabase client: {client is not None}")
        print(f"SUPABASE_AVAILABLE: {SUPABASE_AVAILABLE}")
        print(f"Environment SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
        
        if not SUPABASE_AVAILABLE or not client:
            print("❌ Supabase not available - cannot create topic")
            raise Exception("Supabase not available - cannot create topic")
        
        try:
            data = {
                'title': title,
                'description': description,
                'user_id': user_id,
                'created_at': datetime.utcnow().isoformat(),
                'is_active': True,
                'is_shared': False,
                'version': 1,
                'last_modified': datetime.utcnow().isoformat()
            }
            print(f"Attempting to insert data: {data}")
            response = client.table('topics').insert(data).execute()
            if response.data:
                topic_data = response.data[0]
                print(f"✅ Created topic in Supabase: {topic_data['title']} (ID: {topic_data['id']})")
                return Topic(
                    topic_data['id'],
                    topic_data['title'],
                    topic_data['description'],
                    topic_data['user_id'],
                    datetime.fromisoformat(topic_data['created_at']),
                    topic_data['is_active'],
                    topic_data.get('share_code'),
                    topic_data.get('is_shared', False),
                    datetime.fromisoformat(topic_data['shared_at']) if topic_data.get('shared_at') else None,
                    topic_data.get('notes'),
                    topic_data.get('tags', []),
                    topic_data.get('version', 1),
                    datetime.fromisoformat(topic_data['last_modified']) if topic_data.get('last_modified') else None
                )
            return None
        except Exception as e:
            print(f"❌ Error creating topic in Supabase: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to create topic: {e}")
    
    @staticmethod
    def get_by_id(topic_id, user_id):
        """Get a topic by ID (user-specific or shared)"""
        # Get Supabase client dynamically
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            raise Exception("Supabase not available - cannot retrieve topic")
        
        try:
            # First try to get own topic
            response = client.table('topics').select('*').eq('id', topic_id).eq('user_id', user_id).eq('is_active', True).execute()
            if response.data:
                topic_data = response.data[0]
                return Topic(
                    topic_data['id'],
                    topic_data['title'],
                    topic_data['description'],
                    topic_data['user_id'],
                    datetime.fromisoformat(topic_data['created_at']),
                    topic_data['is_active'],
                    topic_data.get('share_code'),
                    topic_data.get('is_shared', False),
                    datetime.fromisoformat(topic_data['shared_at']) if topic_data.get('shared_at') else None
                )
            
            # If not found, check if user has access through shared_topic_access
            shared_response = client.table('topics').select('*').eq('id', topic_id).eq('is_active', True).in_('id', 
                client.table('shared_topic_access').select('topic_id').eq('user_id', user_id)
            ).execute()
            
            if shared_response.data:
                topic_data = shared_response.data[0]
                return Topic(
                    topic_data['id'],
                    topic_data['title'],
                    topic_data['description'],
                    topic_data['user_id'],
                    datetime.fromisoformat(topic_data['created_at']),
                    topic_data['is_active'],
                    topic_data.get('share_code'),
                    topic_data.get('is_shared', False),
                    datetime.fromisoformat(topic_data['shared_at']) if topic_data.get('shared_at') else None
                )
            
            return None
        except Exception as e:
            print(f"❌ Error getting topic from Supabase: {e}")
            raise Exception(f"Failed to retrieve topic: {e}")
    
    @staticmethod
    def get_all_by_user(user_id, limit=None):
        """Get all topics for a user"""
        # Get Supabase client dynamically
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            raise Exception("Supabase not available - cannot retrieve topics")
        
        try:
            query = client.table('topics').select('*').eq('user_id', user_id).eq('is_active', True).order('created_at', desc=True)
            if limit:
                query = query.limit(limit)
            response = query.execute()
            
            topics = []
            for topic_data in response.data:
                topic = Topic(
                    topic_data['id'],
                    topic_data['title'],
                    topic_data['description'],
                    topic_data['user_id'],
                    datetime.fromisoformat(topic_data['created_at']),
                    topic_data['is_active'],
                    topic_data.get('share_code'),
                    topic_data.get('is_shared', False),
                    datetime.fromisoformat(topic_data['shared_at']) if topic_data.get('shared_at') else None
                )
                topics.append(topic)
            print(f"✅ Retrieved {len(topics)} topics from Supabase for user {user_id}")
            return topics
        except Exception as e:
            print(f"❌ Error getting topics from Supabase: {e}")
            raise Exception(f"Failed to retrieve topics: {e}")
    
    def update(self, title, description):
        """Update topic"""
        # Get Supabase client dynamically
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            raise Exception("Supabase not available - cannot update topic")
        
        try:
            data = {
                'title': title,
                'description': description
            }
            response = client.table('topics').update(data).eq('id', self.id).eq('user_id', self.user_id).execute()
            if response.data:
                topic_data = response.data[0]
                self.title = topic_data['title']
                self.description = topic_data['description']
                print(f"✅ Updated topic in Supabase: {self.title}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error updating topic in Supabase: {e}")
            raise Exception(f"Failed to update topic: {e}")
    
    def delete(self):
        """Soft delete topic"""
        # Get Supabase client dynamically
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            raise Exception("Supabase not available - cannot delete topic")
        
        try:
            data = {
                'is_active': False
            }
            response = client.table('topics').update(data).eq('id', self.id).eq('user_id', self.user_id).execute()
            if response.data:
                self.is_active = False
                print(f"✅ Deleted topic in Supabase: {self.title}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting topic in Supabase: {e}")
            raise Exception(f"Failed to delete topic: {e}")

    # Sharing methods
    @staticmethod
    def share_topic(topic_id, user_id, expires_at=None, max_uses=None):
        """Share a topic and return the share code"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            client = get_supabase_client()
            
            # Check if user owns the topic
            topic = Topic.get_by_id(topic_id, user_id)
            if not topic:
                return None
            
            # Call the share_topic function
            response = client.rpc('share_topic', {
                'p_topic_id': topic_id,
                'p_expires_at': expires_at.isoformat() if expires_at else None,
                'p_max_uses': max_uses
            }).execute()
            
            if response.data:
                return response.data
            return None
        except Exception as e:
            print(f"Error sharing topic: {e}")
            return None
    
    @staticmethod
    def join_topic_with_code(share_code, user_id):
        """Join a topic using a share code"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            client = get_supabase_client()
            
            # Call the join_topic_with_code function
            response = client.rpc('join_topic_with_code', {
                'p_share_code': share_code
            }).execute()
            
            if response.data:
                return response.data
            return None
        except Exception as e:
            print(f"Error joining topic: {e}")
            return None
    
    @staticmethod
    def revoke_topic_sharing(topic_id, user_id):
        """Revoke sharing for a topic"""
        if not SUPABASE_AVAILABLE:
            return False
        
        try:
            client = get_supabase_client()
            
            # Check if user owns the topic
            topic = Topic.get_by_id(topic_id, user_id)
            if not topic:
                return False
            
            # Call the revoke_topic_sharing function
            response = client.rpc('revoke_topic_sharing', {
                'p_topic_id': topic_id
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error revoking topic sharing: {e}")
            return False
    
    @staticmethod
    def get_shared_topics(user_id):
        """Get topics shared with a user"""
        if not SUPABASE_AVAILABLE:
            return []
        
        try:
            client = get_supabase_client()
            
            # Get topics where user has access through shared_topic_access
            response = client.table('topics').select('*').in_('id', 
                client.table('shared_topic_access').select('topic_id').eq('user_id', user_id)
            ).eq('is_active', True).execute()
            
            topics = []
            for topic_data in response.data:
                topic = Topic(
                    topic_data['id'],
                    topic_data['title'],
                    topic_data['description'],
                    topic_data['user_id'],
                    datetime.fromisoformat(topic_data['created_at']),
                    topic_data['is_active'],
                    topic_data.get('share_code'),
                    topic_data.get('is_shared', False),
                    datetime.fromisoformat(topic_data['shared_at']) if topic_data.get('shared_at') else None
                )
                topics.append(topic)
            
            return topics
        except Exception as e:
            print(f"Error getting shared topics: {e}")
            return []
    
    @staticmethod
    def get_all_topics_for_user(user_id, limit=None):
        """Get all topics for a user (own + shared)"""
        own_topics = Topic.get_all_by_user(user_id, limit)
        shared_topics = Topic.get_shared_topics(user_id)
        
        # Combine and deduplicate
        all_topics = own_topics.copy()
        for shared_topic in shared_topics:
            if not any(topic.id == shared_topic.id for topic in all_topics):
                all_topics.append(shared_topic)
        
        return all_topics
    
    # Content management methods
    @staticmethod
    def update_topic_content(topic_id, user_id, title=None, description=None, 
                           notes=None, tags=None):
        """Update topic content and create version"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            # Get current topic
            current = Topic.get_by_id(topic_id, user_id)
            if not current:
                return False
            
            # Prepare update data
            update_data = {'last_modified': datetime.utcnow().isoformat()}
            
            if title is not None:
                update_data['title'] = title
            if description is not None:
                update_data['description'] = description
            if notes is not None:
                update_data['notes'] = notes
            if tags is not None:
                update_data['tags'] = tags
            
            # Update topic
            client.table('topics').update(update_data).eq('id', topic_id).eq('user_id', user_id).execute()
            
            # Create version if significant changes
            if title or description or notes:
                from app.models.content_management import TopicVersion
                TopicVersion.create_version(topic_id, "Content updated")
            
            return True
        except Exception as e:
            print(f"Error updating topic content: {e}")
            return False
    
    @staticmethod
    def get_topic_attachments(topic_id, user_id):
        """Get attachments for a topic"""
        from app.models.content_management import TopicAttachment
        return TopicAttachment.get_topic_attachments(topic_id, user_id)
    
    @staticmethod
    def get_topic_notes(topic_id, user_id, note_type=None):
        """Get notes for a topic"""
        from app.models.content_management import TopicNote
        return TopicNote.get_topic_notes(topic_id, user_id, note_type)
    
    @staticmethod
    def get_topic_versions(topic_id, user_id):
        """Get version history for a topic"""
        from app.models.content_management import TopicVersion
        return TopicVersion.get_topic_versions(topic_id, user_id)
    
    @staticmethod
    def search_topics_by_tags(user_id, tags):
        """Search topics by tags"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            # Search for topics containing any of the specified tags
            response = client.table('topics').select('*').eq('user_id', user_id).eq('is_active', True).overlaps('tags', tags).execute()
            
            topics = []
            for topic_data in response.data:
                topic = Topic(
                    topic_data['id'],
                    topic_data['title'],
                    topic_data['description'],
                    topic_data['user_id'],
                    datetime.fromisoformat(topic_data['created_at']),
                    topic_data['is_active'],
                    topic_data.get('share_code'),
                    topic_data.get('is_shared', False),
                    datetime.fromisoformat(topic_data['shared_at']) if topic_data.get('shared_at') else None,
                    topic_data.get('notes'),
                    topic_data.get('tags', []),
                    topic_data.get('version', 1),
                    datetime.fromisoformat(topic_data['last_modified']) if topic_data.get('last_modified') else None
                )
                topics.append(topic)
            
            return topics
        except Exception as e:
            print(f"Error searching topics by tags: {e}")
            return []

    # Alias methods for compatibility
    @staticmethod
    def get_topics_by_user(user_id, limit=None):
        """Alias for get_all_by_user"""
        return Topic.get_all_by_user(user_id, limit)
    
    @staticmethod
    def get_topic_by_id(topic_id, user_id):
        """Alias for get_by_id"""
        return Topic.get_by_id(topic_id, user_id)

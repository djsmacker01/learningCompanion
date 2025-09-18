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
    def __init__(self, id, title, description, user_id, created_at=None, is_active=True):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.is_active = is_active
    
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
                'is_active': True
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
                    topic_data['is_active']
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
        """Get a topic by ID (user-specific)"""
        # Get Supabase client dynamically
        client = get_supabase_client()
        if not SUPABASE_AVAILABLE or not client:
            raise Exception("Supabase not available - cannot retrieve topic")
        
        try:
            response = client.table('topics').select('*').eq('id', topic_id).eq('user_id', user_id).eq('is_active', True).execute()
            if response.data:
                topic_data = response.data[0]
                return Topic(
                    topic_data['id'],
                    topic_data['title'],
                    topic_data['description'],
                    topic_data['user_id'],
                    datetime.fromisoformat(topic_data['created_at']),
                    topic_data['is_active']
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
                    topic_data['is_active']
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

    # Alias methods for compatibility
    @staticmethod
    def get_topics_by_user(user_id, limit=None):
        """Alias for get_all_by_user"""
        return Topic.get_all_by_user(user_id, limit)
    
    @staticmethod
    def get_topic_by_id(topic_id, user_id):
        """Alias for get_by_id"""
        return Topic.get_by_id(topic_id, user_id)

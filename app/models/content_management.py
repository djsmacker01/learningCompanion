"""
Content Management Models
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import uuid
import os


class TopicAttachment:
    """Model for topic file attachments"""
    
    def __init__(self, id=None, topic_id=None, user_id=None, filename=None, 
                 original_filename=None, file_path=None, file_size=None, 
                 file_type=None, mime_type=None, description=None, 
                 is_public=False, created_at=None, updated_at=None):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.filename = filename
        self.original_filename = original_filename
        self.file_path = file_path
        self.file_size = file_size
        self.file_type = file_type
        self.mime_type = mime_type
        self.description = description
        self.is_public = is_public
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def create_attachment(cls, topic_id: str, user_id: str, filename: str, 
                         original_filename: str, file_path: str, file_size: int,
                         file_type: str, mime_type: str = None, 
                         description: str = None, is_public: bool = False):
        """Create a new topic attachment"""
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            data = {
                'topic_id': topic_id,
                'user_id': user_id,
                'filename': filename,
                'original_filename': original_filename,
                'file_path': file_path,
                'file_size': file_size,
                'file_type': file_type,
                'mime_type': mime_type,
                'description': description,
                'is_public': is_public,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            result = client.table('topic_attachments').insert(data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error creating attachment: {e}")
        
        return None
    
    @classmethod
    def get_topic_attachments(cls, topic_id: str, user_id: str):
        """Get all attachments for a topic"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('topic_attachments').select('*').eq('topic_id', topic_id).eq('user_id', user_id).order('created_at', desc=True).execute()
            
            attachments = []
            for data in response.data:
                attachment = cls(
                    id=data['id'],
                    topic_id=data['topic_id'],
                    user_id=data['user_id'],
                    filename=data['filename'],
                    original_filename=data['original_filename'],
                    file_path=data['file_path'],
                    file_size=data['file_size'],
                    file_type=data['file_type'],
                    mime_type=data.get('mime_type'),
                    description=data.get('description'),
                    is_public=data.get('is_public', False),
                    created_at=datetime.fromisoformat(data['created_at']),
                    updated_at=datetime.fromisoformat(data['updated_at'])
                )
                attachments.append(attachment)
            
            return attachments
        except Exception as e:
            print(f"Error getting attachments: {e}")
            return []
    
    @classmethod
    def delete_attachment(cls, attachment_id: str, user_id: str):
        """Delete an attachment"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            # Get attachment info first
            response = client.table('topic_attachments').select('file_path').eq('id', attachment_id).eq('user_id', user_id).execute()
            
            if response.data:
                # Delete from database
                client.table('topic_attachments').delete().eq('id', attachment_id).eq('user_id', user_id).execute()
                
                # Delete file from storage (implement based on your storage solution)
                file_path = response.data[0]['file_path']
                # TODO: Implement file deletion from storage
                
                return True
        except Exception as e:
            print(f"Error deleting attachment: {e}")
        
        return False


class TopicNote:
    """Model for topic notes"""
    
    def __init__(self, id=None, topic_id=None, user_id=None, title=None, 
                 content=None, note_type='general', is_public=False, 
                 created_at=None, updated_at=None):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.note_type = note_type
        self.is_public = is_public
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def create_note(cls, topic_id: str, user_id: str, title: str, 
                    content: str, note_type: str = 'general', 
                    is_public: bool = False):
        """Create a new topic note"""
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            data = {
                'topic_id': topic_id,
                'user_id': user_id,
                'title': title,
                'content': content,
                'note_type': note_type,
                'is_public': is_public,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            result = client.table('topic_notes').insert(data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error creating note: {e}")
        
        return None
    
    @classmethod
    def get_topic_notes(cls, topic_id: str, user_id: str, note_type: str = None):
        """Get notes for a topic"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            query = client.table('topic_notes').select('*').eq('topic_id', topic_id).eq('user_id', user_id)
            
            if note_type:
                query = query.eq('note_type', note_type)
            
            response = query.order('created_at', desc=True).execute()
            
            notes = []
            for data in response.data:
                note = cls(
                    id=data['id'],
                    topic_id=data['topic_id'],
                    user_id=data['user_id'],
                    title=data['title'],
                    content=data['content'],
                    note_type=data['note_type'],
                    is_public=data.get('is_public', False),
                    created_at=datetime.fromisoformat(data['created_at']),
                    updated_at=datetime.fromisoformat(data['updated_at'])
                )
                notes.append(note)
            
            return notes
        except Exception as e:
            print(f"Error getting notes: {e}")
            return []
    
    @classmethod
    def update_note(cls, note_id: str, user_id: str, title: str = None, 
                    content: str = None, note_type: str = None):
        """Update a note"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            update_data = {'updated_at': datetime.utcnow().isoformat()}
            
            if title is not None:
                update_data['title'] = title
            if content is not None:
                update_data['content'] = content
            if note_type is not None:
                update_data['note_type'] = note_type
            
            client.table('topic_notes').update(update_data).eq('id', note_id).eq('user_id', user_id).execute()
            return True
        except Exception as e:
            print(f"Error updating note: {e}")
        
        return False
    
    @classmethod
    def delete_note(cls, note_id: str, user_id: str):
        """Delete a note"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            client.table('topic_notes').delete().eq('id', note_id).eq('user_id', user_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting note: {e}")
        
        return False


class TopicVersion:
    """Model for topic versioning"""
    
    def __init__(self, id=None, topic_id=None, user_id=None, version_number=None,
                 title=None, description=None, notes=None, tags=None,
                 change_summary=None, created_at=None):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.version_number = version_number
        self.title = title
        self.description = description
        self.notes = notes
        self.tags = tags or []
        self.change_summary = change_summary
        self.created_at = created_at or datetime.utcnow()
    
    @classmethod
    def create_version(cls, topic_id: str, change_summary: str = None):
        """Create a new version of a topic"""
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            # Call the database function
            response = client.rpc('create_topic_version', {
                'p_topic_id': topic_id,
                'p_change_summary': change_summary
            }).execute()
            
            if response.data:
                return response.data
        except Exception as e:
            print(f"Error creating version: {e}")
        
        return None
    
    @classmethod
    def get_topic_versions(cls, topic_id: str, user_id: str):
        """Get all versions of a topic"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('topic_versions').select('*').eq('topic_id', topic_id).eq('user_id', user_id).order('version_number', desc=True).execute()
            
            versions = []
            for data in response.data:
                version = cls(
                    id=data['id'],
                    topic_id=data['topic_id'],
                    user_id=data['user_id'],
                    version_number=data['version_number'],
                    title=data['title'],
                    description=data.get('description'),
                    notes=data.get('notes'),
                    tags=data.get('tags', []),
                    change_summary=data.get('change_summary'),
                    created_at=datetime.fromisoformat(data['created_at'])
                )
                versions.append(version)
            
            return versions
        except Exception as e:
            print(f"Error getting versions: {e}")
            return []
    
    @classmethod
    def restore_version(cls, topic_id: str, version_number: int):
        """Restore a topic to a specific version"""
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            # Call the database function
            response = client.rpc('restore_topic_version', {
                'p_topic_id': topic_id,
                'p_version_number': version_number
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error restoring version: {e}")
        
        return False


class TopicTag:
    """Model for topic tags"""
    
    def __init__(self, id=None, name=None, color=None, description=None,
                 usage_count=0, created_at=None):
        self.id = id
        self.name = name
        self.color = color
        self.description = description
        self.usage_count = usage_count
        self.created_at = created_at or datetime.utcnow()
    
    @classmethod
    def get_all_tags(cls):
        """Get all available tags"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('topic_tags').select('*').order('usage_count', desc=True).execute()
            
            tags = []
            for data in response.data:
                tag = cls(
                    id=data['id'],
                    name=data['name'],
                    color=data.get('color', '#3B82F6'),
                    description=data.get('description'),
                    usage_count=data.get('usage_count', 0),
                    created_at=datetime.fromisoformat(data['created_at'])
                )
                tags.append(tag)
            
            return tags
        except Exception as e:
            print(f"Error getting tags: {e}")
            return []
    
    @classmethod
    def create_tag(cls, name: str, color: str = '#3B82F6', description: str = None):
        """Create a new tag"""
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            data = {
                'name': name.lower().strip(),
                'color': color,
                'description': description,
                'usage_count': 0,
                'created_at': datetime.utcnow().isoformat()
            }
            
            result = client.table('topic_tags').insert(data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error creating tag: {e}")
        
        return None
    
    @classmethod
    def search_tags(cls, query: str):
        """Search tags by name"""
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('topic_tags').select('*').ilike('name', f'%{query}%').order('usage_count', desc=True).execute()
            
            tags = []
            for data in response.data:
                tag = cls(
                    id=data['id'],
                    name=data['name'],
                    color=data.get('color', '#3B82F6'),
                    description=data.get('description'),
                    usage_count=data.get('usage_count', 0),
                    created_at=datetime.fromisoformat(data['created_at'])
                )
                tags.append(tag)
            
            return tags
        except Exception as e:
            print(f"Error searching tags: {e}")
            return []



from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import uuid
import json


class UserAccessibilityPreferences:
    
    
    def __init__(self, id=None, user_id=None, screen_reader_enabled=False,
                 high_contrast_mode=False, text_size='medium', keyboard_navigation=True,
                 reduced_motion=False, color_blind_friendly=False, focus_indicators=True,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.screen_reader_enabled = screen_reader_enabled
        self.high_contrast_mode = high_contrast_mode
        self.text_size = text_size
        self.keyboard_navigation = keyboard_navigation
        self.reduced_motion = reduced_motion
        self.color_blind_friendly = color_blind_friendly
        self.focus_indicators = focus_indicators
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def get_user_preferences(cls, user_id: str):
        
        if not SUPABASE_AVAILABLE:
            return cls(user_id=user_id)
        
        client = get_supabase_client()
        if not client:
            return cls(user_id=user_id)
        
        try:
            response = client.rpc('get_user_accessibility_preferences', {
                'p_user_id': user_id
            }).execute()
            
            if response.data:
                prefs_data = response.data
                return cls(
                    user_id=user_id,
                    screen_reader_enabled=prefs_data.get('screen_reader_enabled', False),
                    high_contrast_mode=prefs_data.get('high_contrast_mode', False),
                    text_size=prefs_data.get('text_size', 'medium'),
                    keyboard_navigation=prefs_data.get('keyboard_navigation', True),
                    reduced_motion=prefs_data.get('reduced_motion', False),
                    color_blind_friendly=prefs_data.get('color_blind_friendly', False),
                    focus_indicators=prefs_data.get('focus_indicators', True)
                )
        except Exception as e:
            print(f"Error getting accessibility preferences: {e}")
        
        return cls(user_id=user_id)
    
    @classmethod
    def update_preferences(cls, user_id: str, **kwargs):
        
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            response = client.rpc('update_user_accessibility_preferences', {
                'p_user_id': user_id,
                'p_screen_reader_enabled': kwargs.get('screen_reader_enabled'),
                'p_high_contrast_mode': kwargs.get('high_contrast_mode'),
                'p_text_size': kwargs.get('text_size'),
                'p_keyboard_navigation': kwargs.get('keyboard_navigation'),
                'p_reduced_motion': kwargs.get('reduced_motion'),
                'p_color_blind_friendly': kwargs.get('color_blind_friendly'),
                'p_focus_indicators': kwargs.get('focus_indicators')
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error updating accessibility preferences: {e}")
        
        return False
    
    @classmethod
    def log_accessibility_action(cls, user_id: str, action_type: str, action_data: dict = None):
        
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            response = client.rpc('log_accessibility_action', {
                'p_user_id': user_id,
                'p_action_type': action_type,
                'p_action_data': json.dumps(action_data) if action_data else None
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error logging accessibility action: {e}")
        
        return False


class UserMobilePreferences:
    
    
    def __init__(self, id=None, user_id=None, offline_mode=False, auto_sync=True,
                 sync_frequency=15, data_usage_limit=100, push_notifications=True,
                 vibration_enabled=True, haptic_feedback=True, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.offline_mode = offline_mode
        self.auto_sync = auto_sync
        self.sync_frequency = sync_frequency
        self.data_usage_limit = data_usage_limit
        self.push_notifications = push_notifications
        self.vibration_enabled = vibration_enabled
        self.haptic_feedback = haptic_feedback
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def get_user_preferences(cls, user_id: str):
        
        if not SUPABASE_AVAILABLE:
            return cls(user_id=user_id)
        
        client = get_supabase_client()
        if not client:
            return cls(user_id=user_id)
        
        try:
            response = client.rpc('get_user_mobile_preferences', {
                'p_user_id': user_id
            }).execute()
            
            if response.data:
                prefs_data = response.data
                return cls(
                    user_id=user_id,
                    offline_mode=prefs_data.get('offline_mode', False),
                    auto_sync=prefs_data.get('auto_sync', True),
                    sync_frequency=prefs_data.get('sync_frequency', 15),
                    data_usage_limit=prefs_data.get('data_usage_limit', 100),
                    push_notifications=prefs_data.get('push_notifications', True),
                    vibration_enabled=prefs_data.get('vibration_enabled', True),
                    haptic_feedback=prefs_data.get('haptic_feedback', True)
                )
        except Exception as e:
            print(f"Error getting mobile preferences: {e}")
        
        return cls(user_id=user_id)
    
    @classmethod
    def update_preferences(cls, user_id: str, **kwargs):
        
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            response = client.rpc('update_user_mobile_preferences', {
                'p_user_id': user_id,
                'p_offline_mode': kwargs.get('offline_mode'),
                'p_auto_sync': kwargs.get('auto_sync'),
                'p_sync_frequency': kwargs.get('sync_frequency'),
                'p_data_usage_limit': kwargs.get('data_usage_limit'),
                'p_push_notifications': kwargs.get('push_notifications'),
                'p_vibration_enabled': kwargs.get('vibration_enabled'),
                'p_haptic_feedback': kwargs.get('haptic_feedback')
            }).execute()
            
            return response.data if response.data else False
        except Exception as e:
            print(f"Error updating mobile preferences: {e}")
        
        return False


class OfflineData:
    
    
    def __init__(self, id=None, user_id=None, data_type=None, data_id=None,
                 data_content=None, last_synced=None, is_dirty=False,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.data_type = data_type
        self.data_id = data_id
        self.data_content = data_content or {}
        self.last_synced = last_synced or datetime.utcnow()
        self.is_dirty = is_dirty
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def cache_data(cls, user_id: str, data_type: str, data_id: str, data_content: dict):
        
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            data = {
                'user_id': user_id,
                'data_type': data_type,
                'data_id': data_id,
                'data_content': json.dumps(data_content),
                'last_synced': datetime.utcnow().isoformat(),
                'is_dirty': False,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            result = client.table('offline_data').upsert(data, on_conflict='user_id,data_type,data_id').execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error caching data: {e}")
        
        return None
    
    @classmethod
    def get_cached_data(cls, user_id: str, data_type: str = None):
        
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            query = client.table('offline_data').select('*').eq('user_id', user_id)
            
            if data_type:
                query = query.eq('data_type', data_type)
            
            response = query.execute()
            
            cached_data = []
            for data in response.data:
                offline_data = cls(
                    id=data['id'],
                    user_id=data['user_id'],
                    data_type=data['data_type'],
                    data_id=data['data_id'],
                    data_content=json.loads(data['data_content']) if data['data_content'] else {},
                    last_synced=datetime.fromisoformat(data['last_synced']),
                    is_dirty=data['is_dirty'],
                    created_at=datetime.fromisoformat(data['created_at']),
                    updated_at=datetime.fromisoformat(data['updated_at'])
                )
                cached_data.append(offline_data)
            
            return cached_data
        except Exception as e:
            print(f"Error getting cached data: {e}")
            return []
    
    @classmethod
    def mark_dirty(cls, user_id: str, data_type: str, data_id: str):
        
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            client.table('offline_data').update({
                'is_dirty': True,
                'updated_at': datetime.utcnow().isoformat()
            }).eq('user_id', user_id).eq('data_type', data_type).eq('data_id', data_id).execute()
            
            return True
        except Exception as e:
            print(f"Error marking data as dirty: {e}")
        
        return False
    
    @classmethod
    def clear_cache(cls, user_id: str, data_type: str = None):
        
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            query = client.table('offline_data').delete().eq('user_id', user_id)
            
            if data_type:
                query = query.eq('data_type', data_type)
            
            query.execute()
            return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
        
        return False


class DeviceSync:
    
    
    def __init__(self, id=None, user_id=None, device_id=None, device_name=None,
                 device_type=None, last_sync=None, sync_token=None, is_active=True,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type
        self.last_sync = last_sync or datetime.utcnow()
        self.sync_token = sync_token
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def register_device(cls, user_id: str, device_id: str, device_name: str, device_type: str):
        
        if not SUPABASE_AVAILABLE:
            return None
        
        client = get_supabase_client()
        if not client:
            return None
        
        try:
            response = client.rpc('register_device', {
                'p_user_id': user_id,
                'p_device_id': device_id,
                'p_device_name': device_name,
                'p_device_type': device_type
            }).execute()
            
            if response.data:
                sync_token = response.data
                return cls(
                    user_id=user_id,
                    device_id=device_id,
                    device_name=device_name,
                    device_type=device_type,
                    sync_token=sync_token
                )
        except Exception as e:
            print(f"Error registering device: {e}")
        
        return None
    
    @classmethod
    def get_user_devices(cls, user_id: str):
        
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('device_sync').select('*').eq('user_id', user_id).eq('is_active', True).execute()
            
            devices = []
            for data in response.data:
                device = cls(
                    id=data['id'],
                    user_id=data['user_id'],
                    device_id=data['device_id'],
                    device_name=data['device_name'],
                    device_type=data['device_type'],
                    last_sync=datetime.fromisoformat(data['last_sync']),
                    sync_token=data['sync_token'],
                    is_active=data['is_active'],
                    created_at=datetime.fromisoformat(data['created_at']),
                    updated_at=datetime.fromisoformat(data['updated_at'])
                )
                devices.append(device)
            
            return devices
        except Exception as e:
            print(f"Error getting user devices: {e}")
            return []
    
    @classmethod
    def update_sync_time(cls, user_id: str, device_id: str):
        
        if not SUPABASE_AVAILABLE:
            return False
        
        client = get_supabase_client()
        if not client:
            return False
        
        try:
            client.table('device_sync').update({
                'last_sync': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }).eq('user_id', user_id).eq('device_id', device_id).execute()
            
            return True
        except Exception as e:
            print(f"Error updating sync time: {e}")
        
        return False


class AccessibilityAuditLog:
    
    
    def __init__(self, id=None, user_id=None, action_type=None, action_data=None, timestamp=None):
        self.id = id
        self.user_id = user_id
        self.action_type = action_type
        self.action_data = action_data or {}
        self.timestamp = timestamp or datetime.utcnow()
    
    @classmethod
    def get_user_audit_log(cls, user_id: str, limit: int = 50):
        
        if not SUPABASE_AVAILABLE:
            return []
        
        client = get_supabase_client()
        if not client:
            return []
        
        try:
            response = client.table('accessibility_audit_log').select('*').eq('user_id', user_id).order('timestamp', desc=True).limit(limit).execute()
            
            audit_logs = []
            for data in response.data:
                audit_log = cls(
                    id=data['id'],
                    user_id=data['user_id'],
                    action_type=data['action_type'],
                    action_data=json.loads(data['action_data']) if data['action_data'] else {},
                    timestamp=datetime.fromisoformat(data['timestamp'])
                )
                audit_logs.append(audit_log)
            
            return audit_logs
        except Exception as e:
            print(f"Error getting audit log: {e}")
            return []


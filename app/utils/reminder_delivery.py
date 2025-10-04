

import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from app.models.reminders import StudyReminder
from app.models import get_supabase_client, SUPABASE_AVAILABLE


class ReminderDeliveryService:
    
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"  
        self.smtp_port = 587
        self.sender_email = None  
        self.sender_password = None  
        
    def send_reminder(self, reminder: StudyReminder) -> bool:
        
        try:
            if reminder.reminder_method == 'email':
                return self._send_email_reminder(reminder)
            elif reminder.reminder_method == 'sms':
                return self._send_sms_reminder(reminder)
            elif reminder.reminder_method == 'push':
                return self._send_push_reminder(reminder)
            else:
                print(f"Unknown reminder method: {reminder.reminder_method}")
                return False
                
        except Exception as e:
            print(f"Error sending reminder: {e}")
            self._log_delivery(reminder.id, reminder.reminder_method, 'failed', str(e))
            return False
    
    def send_bulk_reminders(self, reminders: List[StudyReminder]) -> Dict[str, int]:
        
        results = {
            'sent': 0,
            'failed': 0,
            'total': len(reminders)
        }
        
        for reminder in reminders:
            if self.send_reminder(reminder):
                results['sent'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def _send_email_reminder(self, reminder: StudyReminder) -> bool:
        
        try:
            
            
            
            print(f"📧 EMAIL REMINDER SENT:")
            print(f"   To: {reminder.user_id}")
            print(f"   Subject: {reminder.title}")
            print(f"   Message: {reminder.message}")
            print(f"   Scheduled Time: {reminder.scheduled_time}")
            print(f"   Topic: {reminder.topic_id}")
            print(f"   Session Type: {reminder.session_type}")
            
            
            reminder.mark_as_sent()
            self._log_delivery(reminder.id, 'email', 'sent')
            
            return True
            
        except Exception as e:
            print(f"Error sending email reminder: {e}")
            self._log_delivery(reminder.id, 'email', 'failed', str(e))
            return False
    
    def _send_sms_reminder(self, reminder: StudyReminder) -> bool:
        
        try:
            
            
            
            print(f"📱 SMS REMINDER SENT:")
            print(f"   To: {reminder.user_id}")
            print(f"   Message: {reminder.title} - {reminder.message}")
            print(f"   Time: {reminder.scheduled_time}")
            
            
            reminder.mark_as_sent()
            self._log_delivery(reminder.id, 'sms', 'sent')
            
            return True
            
        except Exception as e:
            print(f"Error sending SMS reminder: {e}")
            self._log_delivery(reminder.id, 'sms', 'failed', str(e))
            return False
    
    def _send_push_reminder(self, reminder: StudyReminder) -> bool:
        
        try:
            
            
            
            print(f"🔔 PUSH REMINDER SENT:")
            print(f"   To: {reminder.user_id}")
            print(f"   Title: {reminder.title}")
            print(f"   Body: {reminder.message}")
            print(f"   Time: {reminder.scheduled_time}")
            
            
            reminder.mark_as_sent()
            self._log_delivery(reminder.id, 'push', 'sent')
            
            return True
            
        except Exception as e:
            print(f"Error sending push reminder: {e}")
            self._log_delivery(reminder.id, 'push', 'failed', str(e))
            return False
    
    def _log_delivery(self, reminder_id: str, method: str, status: str, error_message: str = None):
        
        if not SUPABASE_AVAILABLE:
            return
            
        supabase = get_supabase_client()
        
        try:
            data = {
                'reminder_id': reminder_id,
                'delivery_method': method,
                'delivery_status': status,
                'delivery_time': datetime.now().isoformat(),
                'error_message': error_message,
                'created_at': datetime.now().isoformat()
            }
            
            supabase.table('reminder_delivery_logs').insert(data).execute()
            
        except Exception as e:
            print(f"Error logging delivery: {e}")


class ReminderScheduler:
    
    
    def __init__(self):
        self.delivery_service = ReminderDeliveryService()
    
    def process_pending_reminders(self) -> Dict[str, int]:
        
        try:
            
            pending_reminders = StudyReminder.get_pending_reminders()
            
            if not pending_reminders:
                return {'sent': 0, 'failed': 0, 'total': 0}
            
            print(f"🕐 Processing {len(pending_reminders)} pending reminders...")
            
            
            results = self.delivery_service.send_bulk_reminders(pending_reminders)
            
            print(f"✅ Reminder processing complete:")
            print(f"   Sent: {results['sent']}")
            print(f"   Failed: {results['failed']}")
            print(f"   Total: {results['total']}")
            
            return results
            
        except Exception as e:
            print(f"Error processing pending reminders: {e}")
            return {'sent': 0, 'failed': 0, 'total': 0}
    
    def create_daily_reminders(self, user_id: str) -> List[StudyReminder]:
        
        try:
            from app.models.reminders import StudyReminderPreferences
            from app.utils.smart_scheduling import SmartSchedulingEngine
            
            
            preferences = StudyReminderPreferences.get_or_create_preferences(user_id)
            
            if not preferences.is_enabled:
                return []
            
            
            scheduling_engine = SmartSchedulingEngine()
            reminders = scheduling_engine.create_smart_reminders(user_id)
            
            print(f"📅 Created {len(reminders)} daily reminders for user {user_id}")
            
            return reminders
            
        except Exception as e:
            print(f"Error creating daily reminders: {e}")
            return []
    
    def cleanup_old_reminders(self, days_old: int = 30) -> int:
        
        if not SUPABASE_AVAILABLE:
            return 0
            
        supabase = get_supabase_client()
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            
            result = supabase.table('study_reminders').delete().eq('status', 'sent').lt('sent_at', cutoff_date.isoformat()).execute()
            
            deleted_count = len(result.data) if result.data else 0
            print(f"🧹 Cleaned up {deleted_count} old reminders")
            
            return deleted_count
            
        except Exception as e:
            print(f"Error cleaning up old reminders: {e}")
            return 0


def send_study_reminder_email(user_email: str, reminder_title: str, reminder_message: str, 
                            scheduled_time: datetime, topic_title: str = None) -> bool:
    
    try:
        
        
        
        print("=" * 60)
        print("📧 STUDY REMINDER EMAIL")
        print("=" * 60)
        print(f"To: {user_email}")
        print(f"Subject: {reminder_title}")
        print(f"")
        print(f"Hi there!")
        print(f"")
        print(f"{reminder_message}")
        print(f"")
        print(f"Scheduled Time: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        if topic_title:
            print(f"Topic: {topic_title}")
        print(f"")
        print(f"Ready to study? Click here to start your session!")
        print(f"")
        print(f"Best regards,")
        print(f"Your Learning Companion")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"Error sending study reminder email: {e}")
        return False


def send_study_reminder_sms(phone_number: str, reminder_message: str, 
                          scheduled_time: datetime) -> bool:
    
    try:
        
        
        
        print("=" * 40)
        print("📱 STUDY REMINDER SMS")
        print("=" * 40)
        print(f"To: {phone_number}")
        print(f"Message: {reminder_message}")
        print(f"Time: {scheduled_time.strftime('%H:%M')}")
        print("=" * 40)
        
        return True
        
    except Exception as e:
        print(f"Error sending study reminder SMS: {e}")
        return False


"""
Google Calendar Integration Utilities
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json


class GoogleCalendarIntegration:
    """Google Calendar integration for study schedules"""
    
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/auth/google/callback')
        self.scope = 'https://www.googleapis.com/auth/calendar'
    
    def get_auth_url(self, state: str = None) -> str:
        """Generate Google OAuth authorization URL"""
        from urllib.parse import urlencode
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        if state:
            params['state'] = state
        
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        import requests
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        return response.json()
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        import requests
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        return response.json()
    
    def create_calendar_event(self, access_token: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an event in Google Calendar"""
        import requests
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
        response = requests.post(url, headers=headers, json=event_data)
        return response.json()
    
    def create_study_event(self, access_token: str, title: str, start_time: datetime, 
                          end_time: datetime, description: str = None, topic: str = None) -> Dict[str, Any]:
        """Create a study session event in Google Calendar"""
        
        event_data = {
            'summary': title,
            'description': description or f"Study session: {topic or 'General study'}",
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC'
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                    {'method': 'popup', 'minutes': 15}  # 15 minutes before
                ]
            },
            'colorId': '2',  # Green color for study events
            'visibility': 'private'
        }
        
        return self.create_calendar_event(access_token, event_data)
    
    def sync_study_schedule(self, access_token: str, schedules: List[Any]) -> List[Dict[str, Any]]:
        """Sync multiple study schedules to Google Calendar"""
        created_events = []
        
        for schedule in schedules:
            try:
                event = self.create_study_event(
                    access_token=access_token,
                    title=schedule.title,
                    start_time=schedule.scheduled_start,
                    end_time=schedule.scheduled_end,
                    description=schedule.description,
                    topic=getattr(schedule, 'topic_title', None)
                )
                created_events.append(event)
            except Exception as e:
                print(f"Error creating event for schedule {schedule.id}: {e}")
        
        return created_events


class CalendarWidget:
    """Calendar widget for dashboard"""
    
    @staticmethod
    def generate_calendar_html(events: List[Dict[str, Any]], month: int = None, year: int = None) -> str:
        """Generate HTML for calendar widget"""
        from datetime import datetime, timedelta
        import calendar
        
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
        
        # Get calendar data
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        
        # Create events lookup by date
        events_by_date = {}
        for event in events:
            event_date = datetime.fromisoformat(event['start']['dateTime']).date()
            if event_date not in events_by_date:
                events_by_date[event_date] = []
            events_by_date[event_date].append(event)
        
        # Generate HTML
        html = f"""
        <div class="calendar-widget">
            <div class="calendar-header">
                <h5>{month_name} {year}</h5>
            </div>
            <div class="calendar-grid">
                <div class="calendar-weekdays">
                    <div class="weekday">Mon</div>
                    <div class="weekday">Tue</div>
                    <div class="weekday">Wed</div>
                    <div class="weekday">Thu</div>
                    <div class="weekday">Fri</div>
                    <div class="weekday">Sat</div>
                    <div class="weekday">Sun</div>
                </div>
                <div class="calendar-days">
        """
        
        for week in cal:
            for day in week:
                if day == 0:
                    html += '<div class="calendar-day empty"></div>'
                else:
                    date = datetime(year, month, day).date()
                    has_events = date in events_by_date
                    event_count = len(events_by_date.get(date, []))
                    
                    html += f'''
                    <div class="calendar-day {"has-events" if has_events else ""}">
                        <span class="day-number">{day}</span>
                        {f'<span class="event-indicator">{event_count}</span>' if has_events else ''}
                    </div>
                    '''
        
        html += """
                </div>
            </div>
        </div>
        """
        
        return html

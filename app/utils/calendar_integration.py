

import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json


class GoogleCalendarIntegration:
    
    
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/auth/google/callback')
        self.scope = 'https://www.googleapis.com/auth/calendar'
    
    def get_auth_url(self, state: str = None) -> str:
        
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
                    {'method': 'email', 'minutes': 24 * 60},  
                    {'method': 'popup', 'minutes': 15}  
                ]
            },
            'colorId': '2',  
            'visibility': 'private'
        }
        
        return self.create_calendar_event(access_token, event_data)
    
    def sync_study_schedule(self, access_token: str, schedules: List[Any]) -> List[Dict[str, Any]]:
        
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
    
    
    @staticmethod
    def generate_calendar_html(events: List[Dict[str, Any]], month: int = None, year: int = None) -> str:
        
        from datetime import datetime, timedelta
        import calendar
        
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
        
        
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        
        
        events_by_date = {}
        for event in events:
            event_date = datetime.fromisoformat(event['start']['dateTime']).date()
            if event_date not in events_by_date:
                events_by_date[event_date] = []
            events_by_date[event_date].append(event)
        
        
        html = f
        
        for week in cal:
            for day in week:
                if day == 0:
                    html += '<div class="calendar-day empty"></div>'
                else:
                    date = datetime(year, month, day).date()
                    has_events = date in events_by_date
                    event_count = len(events_by_date.get(date, []))
                    
                    html += f'<td class="calendar-day{" has-events" if has_events else ""}" data-date="{date}" data-events="{event_count}">{day}</td>'
        
        html += '</tr></tbody></table>'
        
        return html


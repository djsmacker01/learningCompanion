

import pytest
from datetime import datetime, date, timedelta
from app.models import StudySession, Topic, User
from app.forms.session_forms import StartSessionForm, CompleteSessionForm, EditSessionForm, SessionFilterForm

class TestStudySessionModel:
    
    
    def test_create_session(self):
        
        user_id = 'test-user-123'
        topic_id = 1
        
        session = StudySession.create_session(
            user_id=user_id,
            topic_id=topic_id,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='Great session!',
            session_type='study',
            completed=True
        )
        
        assert session is not None
        assert session.user_id == user_id
        assert session.topic_id == topic_id
        assert session.duration_minutes == 25
        assert session.confidence_before == 5
        assert session.confidence_after == 7
        assert session.notes == 'Great session!'
        assert session.session_type == 'study'
        assert session.completed == True
    
    def test_get_user_sessions(self):
        
        user_id = 'test-user-123'
        
        
        session1 = StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='Session 1',
            session_type='study'
        )
        
        session2 = StudySession.create_session(
            user_id=user_id,
            topic_id=2,
            session_date=date.today() - timedelta(days=1),
            duration_minutes=30,
            confidence_before=6,
            confidence_after=8,
            notes='Session 2',
            session_type='review'
        )
        
        sessions = StudySession.get_user_sessions(user_id)
        
        assert len(sessions) >= 2
        
        assert sessions[0].session_date >= sessions[1].session_date
    
    def test_get_topic_sessions(self):
        
        user_id = 'test-user-123'
        topic_id = 1
        
        
        session1 = StudySession.create_session(
            user_id=user_id,
            topic_id=topic_id,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='Topic 1 session',
            session_type='study'
        )
        
        session2 = StudySession.create_session(
            user_id=user_id,
            topic_id=2,  
            session_date=date.today(),
            duration_minutes=30,
            confidence_before=6,
            confidence_after=8,
            notes='Topic 2 session',
            session_type='review'
        )
        
        topic_sessions = StudySession.get_topic_sessions(topic_id, user_id)
        
        assert len(topic_sessions) >= 1
        for session in topic_sessions:
            assert session.topic_id == topic_id
    
    def test_get_session_by_id(self):
        
        user_id = 'test-user-123'
        
        session = StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='Test session',
            session_type='study'
        )
        
        retrieved_session = StudySession.get_session_by_id(session.id, user_id)
        
        assert retrieved_session is not None
        assert retrieved_session.id == session.id
        assert retrieved_session.user_id == user_id
    
    def test_update_session(self):
        
        user_id = 'test-user-123'
        
        session = StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='Original notes',
            session_type='study'
        )
        
        
        success = session.update_session(
            duration_minutes=30,
            notes='Updated notes',
            confidence_after=8
        )
        
        assert success == True
        assert session.duration_minutes == 30
        assert session.notes == 'Updated notes'
        assert session.confidence_after == 8
    
    def test_delete_session(self):
        
        user_id = 'test-user-123'
        
        session = StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='To be deleted',
            session_type='study'
        )
        
        session_id = session.id
        
        
        success = StudySession.delete_session(session_id, user_id)
        
        assert success == True
        
        
        deleted_session = StudySession.get_session_by_id(session_id, user_id)
        assert deleted_session is None
    
    def test_calculate_confidence_gain(self):
        
        session = StudySession(
            id=1,
            topic_id=1,
            user_id='test-user',
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=8,
            notes='Test',
            session_type='study',
            completed=True
        )
        
        gain = session.calculate_confidence_gain()
        assert gain == 3
    
    def test_get_session_stats(self):
        
        user_id = 'test-user-123'
        
        
        StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='Session 1',
            session_type='study'
        )
        
        StudySession.create_session(
            user_id=user_id,
            topic_id=2,
            session_date=date.today() - timedelta(days=1),
            duration_minutes=30,
            confidence_before=6,
            confidence_after=8,
            notes='Session 2',
            session_type='review'
        )
        
        stats = StudySession.get_session_stats(user_id, days=30)
        
        assert 'total_sessions' in stats
        assert 'total_time_minutes' in stats
        assert 'total_time_hours' in stats
        assert 'avg_duration' in stats
        assert 'avg_confidence_gain' in stats
        assert 'sessions_by_type' in stats
        assert 'confidence_trend' in stats
        
        assert stats['total_sessions'] >= 2
        assert stats['total_time_minutes'] >= 55  
        assert stats['total_time_hours'] >= 0.9  
    
    def test_get_topic_progress(self):
        
        user_id = 'test-user-123'
        topic_id = 1
        
        
        StudySession.create_session(
            user_id=user_id,
            topic_id=topic_id,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='Session 1',
            session_type='study'
        )
        
        StudySession.create_session(
            user_id=user_id,
            topic_id=topic_id,
            session_date=date.today() - timedelta(days=1),
            duration_minutes=30,
            confidence_before=6,
            confidence_after=8,
            notes='Session 2',
            session_type='review'
        )
        
        progress = StudySession.get_topic_progress(topic_id, user_id)
        
        assert 'total_sessions' in progress
        assert 'total_time_minutes' in progress
        assert 'total_time_hours' in progress
        assert 'confidence_improvement' in progress
        assert 'last_session_date' in progress
        assert 'avg_session_duration' in progress
        assert 'completion_rate' in progress
        
        assert progress['total_sessions'] >= 2
        assert progress['total_time_minutes'] >= 55
        assert progress['confidence_improvement'] >= 4  
    
    def test_get_session_streak(self):
        
        user_id = 'test-user-123'
        
        
        StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='Today',
            session_type='study'
        )
        
        StudySession.create_session(
            user_id=user_id,
            topic_id=2,
            session_date=date.today() - timedelta(days=1),
            duration_minutes=30,
            confidence_before=6,
            confidence_after=8,
            notes='Yesterday',
            session_type='review'
        )
        
        streak = StudySession.get_session_streak(user_id)
        assert streak >= 2
    
    def test_get_weekly_study_time(self):
        
        user_id = 'test-user-123'
        
        
        StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='This week',
            session_type='study'
        )
        
        StudySession.create_session(
            user_id=user_id,
            topic_id=2,
            session_date=date.today() - timedelta(days=2),
            duration_minutes=30,
            confidence_before=6,
            confidence_after=8,
            notes='This week too',
            session_type='review'
        )
        
        weekly_time = StudySession.get_weekly_study_time(user_id)
        assert weekly_time >= 55  


class TestSessionForms:
    
    
    def test_start_session_form_validation(self):
        
        form = StartSessionForm()
        
        
        assert not form.validate()
        assert 'topic_id' in form.errors
        assert 'session_type' in form.errors
        assert 'confidence_before' in form.errors
    
    def test_start_session_form_valid_data(self):
        
        form = StartSessionForm(data={
            'topic_id': 1,
            'session_type': 'study',
            'confidence_before': 5,
            'estimated_duration': 25
        })
        
        assert form.validate()
    
    def test_start_session_form_invalid_confidence(self):
        
        form = StartSessionForm(data={
            'topic_id': 1,
            'session_type': 'study',
            'confidence_before': 15,  
            'estimated_duration': 25
        })
        
        assert not form.validate()
        assert 'confidence_before' in form.errors
    
    def test_complete_session_form_validation(self):
        
        form = CompleteSessionForm()
        
        
        assert not form.validate()
        assert 'duration_minutes' in form.errors
        assert 'confidence_after' in form.errors
    
    def test_complete_session_form_valid_data(self):
        
        form = CompleteSessionForm(data={
            'duration_minutes': 25,
            'confidence_after': 7,
            'notes': 'Great session!',
            'completed': True
        })
        
        assert form.validate()
    
    def test_edit_session_form_validation(self):
        
        form = EditSessionForm()
        
        
        assert not form.validate()
        assert 'session_date' in form.errors
        assert 'duration_minutes' in form.errors
        assert 'confidence_before' in form.errors
        assert 'confidence_after' in form.errors
        assert 'session_type' in form.errors
    
    def test_edit_session_form_future_date(self):
        
        future_date = date.today() + timedelta(days=1)
        form = EditSessionForm(data={
            'session_date': future_date,
            'duration_minutes': 25,
            'confidence_before': 5,
            'confidence_after': 7,
            'session_type': 'study'
        })
        
        assert not form.validate()
        assert 'session_date' in form.errors
    
    def test_session_filter_form(self):
        
        form = SessionFilterForm()
        
        
        assert form.validate()
        
        
        form = SessionFilterForm(data={
            'topic_id': 1,
            'session_type': 'study',
            'date_from': date.today() - timedelta(days=7),
            'date_to': date.today()
        })
        
        assert form.validate()
    
    def test_session_filter_form_invalid_date_range(self):
        
        form = SessionFilterForm(data={
            'date_from': date.today(),
            'date_to': date.today() - timedelta(days=1)  
        })
        
        assert not form.validate()
        assert 'date_to' in form.errors


class TestSessionIntegration:
    
    
    def test_session_user_ownership(self):
        
        user1_id = 'user-1'
        user2_id = 'user-2'
        topic_id = 1
        
        
        session = StudySession.create_session(
            user_id=user1_id,
            topic_id=topic_id,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='User 1 session',
            session_type='study'
        )
        
        
        user1_session = StudySession.get_session_by_id(session.id, user1_id)
        assert user1_session is not None
        assert user1_session.user_id == user1_id
        
        
        user2_session = StudySession.get_session_by_id(session.id, user2_id)
        assert user2_session is None
    
    def test_session_topic_relationship(self):
        
        user_id = 'test-user-123'
        topic_id = 1
        
        
        session = StudySession.create_session(
            user_id=user_id,
            topic_id=topic_id,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='Topic session',
            session_type='study'
        )
        
        
        topic_sessions = StudySession.get_topic_sessions(topic_id, user_id)
        assert len(topic_sessions) >= 1
        assert topic_sessions[0].topic_id == topic_id
    
    def test_session_completion_workflow(self):
        
        user_id = 'test-user-123'
        topic_id = 1
        
        
        session = StudySession.create_session(
            user_id=user_id,
            topic_id=topic_id,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=None,  
            notes='',
            session_type='study',
            completed=False
        )
        
        assert not session.completed
        assert session.confidence_after is None
        
        
        success = session.update_session(
            confidence_after=7,
            notes='Completed session!',
            completed=True
        )
        
        assert success
        assert session.completed
        assert session.confidence_after == 7
        assert session.notes == 'Completed session!'


class TestSessionEdgeCases:
    
    
    def test_session_with_none_values(self):
        
        user_id = 'test-user-123'
        
        session = StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=None,
            notes=None,
            session_type='study',
            completed=False
        )
        
        assert session is not None
        assert session.confidence_after is None
        assert session.notes == ''  
    
    def test_session_with_empty_strings(self):
        
        user_id = 'test-user-123'
        
        session = StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=25,
            confidence_before=5,
            confidence_after=7,
            notes='',
            session_type='study',
            completed=True
        )
        
        assert session is not None
        assert session.notes == ''
    
    def test_session_with_extreme_values(self):
        
        user_id = 'test-user-123'
        
        session = StudySession.create_session(
            user_id=user_id,
            topic_id=1,
            session_date=date.today(),
            duration_minutes=480,  
            confidence_before=1,
            confidence_after=10,
            notes='A' * 1000,  
            session_type='study',
            completed=True
        )
        
        assert session is not None
        assert session.duration_minutes == 480
        assert session.confidence_before == 1
        assert session.confidence_after == 10
        assert len(session.notes) == 1000
    
    def test_session_stats_with_no_sessions(self):
        
        user_id = 'new-user-123'
        
        stats = StudySession.get_session_stats(user_id, days=30)
        
        assert stats['total_sessions'] == 0
        assert stats['total_time_minutes'] == 0
        assert stats['total_time_hours'] == 0
        assert stats['avg_duration'] == 0
        assert stats['avg_confidence_gain'] == 0
        assert stats['sessions_by_type'] == {}
        assert stats['confidence_trend'] == []
    
    def test_topic_progress_with_no_sessions(self):
        
        user_id = 'new-user-123'
        topic_id = 999
        
        progress = StudySession.get_topic_progress(topic_id, user_id)
        
        assert progress['total_sessions'] == 0
        assert progress['total_time_minutes'] == 0
        assert progress['total_time_hours'] == 0
        assert progress['confidence_improvement'] == 0
        assert progress['last_session_date'] is None
        assert progress['avg_session_duration'] == 0
        assert progress['completion_rate'] == 0


if __name__ == '__main__':
    pytest.main([__file__])


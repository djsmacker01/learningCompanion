import pytest
from unittest.mock import MagicMock, patch
from flask_login import UserMixin

from app import create_app

import app.models.study_session as study_session_module


class _TestLoginUser(UserMixin):
    """Minimal user for route tests (Flask-Login session without hitting Supabase)."""

    def __init__(self, user_id='test-user-id'):
        self.id = user_id
        self.email = 'test@example.com'

    @property
    def full_name(self):
        return 'Test User'


@pytest.fixture
def app():
    application = create_app('default')
    application.config['TESTING'] = True
    application.config['WTF_CSRF_ENABLED'] = False
    return application


@pytest.fixture(autouse=True)
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def _clear_in_memory_study_sessions():
    """Study sessions fall back to an in-memory store when Supabase is unavailable."""
    study_session_module._in_memory_sessions.clear()
    yield
    study_session_module._in_memory_sessions.clear()


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 'test-user-id'
    user.email = 'test@example.com'
    user.is_authenticated = True
    return user


@pytest.fixture
def logged_in_client(client):
    user = _TestLoginUser()
    with patch('app.models.auth.AuthUser.get_by_id', return_value=user):
        with client.session_transaction() as sess:
            sess['_user_id'] = user.get_id()
            sess['_fresh'] = True
        yield client

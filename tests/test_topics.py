import pytest
from app import create_app
from app.models import Topic
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    app = create_app('default')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 'test-user-id'
    user.email = 'test@example.com'
    user.is_authenticated = True
    return user

class TestTopicModel:
    
    
    @patch('app.models.supabase')
    def test_topic_creation(self, mock_supabase):
        
        mock_response = MagicMock()
        mock_response.data = [{
            'id': 1,
            'title': 'Test Topic',
            'description': 'Test Description',
            'user_id': 'test-user-id',
            'created_at': '2024-01-01T00:00:00',
            'updated_at': '2024-01-01T00:00:00',
            'is_deleted': False
        }]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        topic = Topic.create('Test Topic', 'Test Description', 'test-user-id')
        
        assert topic is not None
        assert topic.title == 'Test Topic'
        assert topic.description == 'Test Description'
        assert topic.user_id == 'test-user-id'
    
    @patch('app.models.supabase')
    def test_get_topic_by_id(self, mock_supabase):
        
        mock_response = MagicMock()
        mock_response.data = [{
            'id': 1,
            'title': 'Test Topic',
            'description': 'Test Description',
            'user_id': 'test-user-id',
            'created_at': '2024-01-01T00:00:00',
            'updated_at': '2024-01-01T00:00:00',
            'is_deleted': False
        }]
        mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value = mock_response
        
        topic = Topic.get_by_id(1, 'test-user-id')
        
        assert topic is not None
        assert topic.id == 1
        assert topic.title == 'Test Topic'
    
    @patch('app.models.supabase')
    def test_get_all_topics_by_user(self, mock_supabase):
        
        mock_response = MagicMock()
        mock_response.data = [
            {
                'id': 1,
                'title': 'Topic 1',
                'description': 'Description 1',
                'user_id': 'test-user-id',
                'created_at': '2024-01-01T00:00:00',
                'updated_at': '2024-01-01T00:00:00',
                'is_deleted': False
            },
            {
                'id': 2,
                'title': 'Topic 2',
                'description': 'Description 2',
                'user_id': 'test-user-id',
                'created_at': '2024-01-02T00:00:00',
                'updated_at': '2024-01-02T00:00:00',
                'is_deleted': False
            }
        ]
        mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.order.return_value.execute.return_value = mock_response
        
        topics = Topic.get_all_by_user('test-user-id')
        
        assert len(topics) == 2
        assert topics[0].title == 'Topic 1'
        assert topics[1].title == 'Topic 2'

class TestTopicRoutes:
    
    
    @patch('app.models.Topic')
    @patch('flask_login.current_user')
    def test_list_topics_route(self, mock_current_user, mock_topic_model, client):
        
        mock_current_user.id = 'test-user-id'
        mock_current_user.is_authenticated = True
        
        mock_topics = [
            MagicMock(id=1, title='Topic 1', description='Description 1'),
            MagicMock(id=2, title='Topic 2', description='Description 2')
        ]
        mock_topic_model.get_all_by_user.return_value = mock_topics
        
        response = client.get('/topics')
        
        assert response.status_code == 200
        assert b'Topic 1' in response.data
        assert b'Topic 2' in response.data
    
    @patch('flask_login.current_user')
    def test_create_topic_route_get(self, mock_current_user, client):
        
        mock_current_user.is_authenticated = True
        
        response = client.get('/topics/new')
        
        assert response.status_code == 200
        assert b'Create New Topic' in response.data
    
    @patch('app.models.Topic')
    @patch('flask_login.current_user')
    def test_create_topic_route_post(self, mock_current_user, mock_topic_model, client):
        
        mock_current_user.id = 'test-user-id'
        mock_current_user.is_authenticated = True
        
        mock_topic = MagicMock(id=1, title='New Topic', description='New Description')
        mock_topic_model.create.return_value = mock_topic
        
        response = client.post('/topics/new', data={
            'title': 'New Topic',
            'description': 'New Description'
        })
        
        assert response.status_code == 302  
        mock_topic_model.create.assert_called_once_with('New Topic', 'New Description', 'test-user-id')

if __name__ == '__main__':
    pytest.main([__file__])



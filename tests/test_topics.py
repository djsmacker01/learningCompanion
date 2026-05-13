import pytest
from unittest.mock import patch, MagicMock

from app.models import Topic


def _topic_row(**overrides):
    row = {
        'id': '550e8400-e29b-41d4-a716-446655440099',
        'title': 'Test Topic',
        'description': 'Test Description',
        'user_id': 'test-user-id',
        'created_at': '2024-01-01T00:00:00',
        'is_active': True,
        'share_code': None,
        'is_shared': False,
        'shared_at': None,
        'notes': None,
        'tags': [],
        'version': 1,
        'last_modified': '2024-01-01T00:00:00',
        'is_gcse': False,
        'gcse_subject_id': None,
        'gcse_topic_id': None,
        'gcse_exam_board': None,
        'gcse_specification_code': None,
        'exam_weight': None,
        'parent_topic_id': None,
    }
    row.update(overrides)
    return row


class TestTopicModel:

    @patch('app.models.SUPABASE_AVAILABLE', True)
    @patch('app.models.get_supabase_client')
    def test_topic_creation(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_response = MagicMock()
        mock_response.data = [_topic_row()]
        mock_client.table.return_value.insert.return_value.execute.return_value = mock_response

        topic = Topic.create('Test Topic', 'Test Description', 'test-user-id')

        assert topic is not None
        assert topic.title == 'Test Topic'
        assert topic.description == 'Test Description'
        assert topic.user_id == 'test-user-id'

    @patch('app.models.SUPABASE_AVAILABLE', True)
    @patch('app.models.get_supabase_client')
    def test_get_topic_by_id(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_response = MagicMock()
        mock_response.data = [_topic_row()]
        mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value = mock_response

        topic = Topic.get_by_id('550e8400-e29b-41d4-a716-446655440099', 'test-user-id')

        assert topic is not None
        assert topic.id == '550e8400-e29b-41d4-a716-446655440099'
        assert topic.title == 'Test Topic'

    @patch('app.models.SUPABASE_AVAILABLE', True)
    @patch('app.models.get_supabase_client')
    def test_get_all_topics_by_user(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_response = MagicMock()
        mock_response.data = [
            _topic_row(title='Topic 1', description='Description 1', id='660e8400-e29b-41d4-a716-446655440001'),
            _topic_row(title='Topic 2', description='Description 2', id='660e8400-e29b-41d4-a716-446655440002'),
        ]
        mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.order.return_value.execute.return_value = mock_response

        topics = Topic.get_all_by_user('test-user-id')

        assert len(topics) == 2
        assert topics[0].title == 'Topic 1'
        assert topics[1].title == 'Topic 2'


class TestTopicRoutes:

    @patch('app.routes.topics.Topic')
    def test_list_topics_route(self, mock_topic_model, logged_in_client):
        mock_topics = [
            MagicMock(id=1, title='Topic 1', description='Description 1'),
            MagicMock(id=2, title='Topic 2', description='Description 2'),
        ]
        mock_topic_model.get_all_by_user.return_value = mock_topics

        response = logged_in_client.get('/topics')

        assert response.status_code == 200
        assert b'Topic 1' in response.data
        assert b'Topic 2' in response.data

    def test_create_topic_route_get(self, logged_in_client):
        response = logged_in_client.get('/topics/new')

        assert response.status_code == 200
        assert b'Create New Topic' in response.data

    @patch('app.routes.topics.Topic')
    def test_create_topic_route_post(self, mock_topic_model, logged_in_client):
        mock_topic = MagicMock(id=1, title='New Topic', description='New Description')
        mock_topic_model.create.return_value = mock_topic

        response = logged_in_client.post('/topics/new', data={
            'title': 'New Topic',
            'description': 'New Description for the topic form.',
            'submit': 'Save Topic',
        })

        assert response.status_code == 302
        mock_topic_model.create.assert_called_once_with(
            title='New Topic',
            description='New Description for the topic form.',
            user_id='test-user-id',
        )

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models import Topic, User
from app.models.study_session import StudySession
from app.forms import TopicForm
import os

topics = Blueprint('topics', __name__)

import uuid
from app.models import get_supabase_client

def get_or_create_mock_user():
    mock_email = 'flask-test@example.com'
    
    client = get_supabase_client()
    if not client:
        print("❌ Supabase client not available for mock user creation")
        return None
    
    try:
        response = client.table('users').select('*').eq('email', mock_email).execute()
        if response.data:
            user_data = response.data[0]
            print(f"✅ Found existing mock user: {user_data['email']}")
            return User(id=user_data['id'], email=user_data['email'], name=f"{user_data['first_name']} {user_data['last_name']}")
    except Exception as e:
        print(f"Error finding existing user: {e}")
    
    try:
        import uuid
        mock_user_id = str(uuid.uuid4())
        user_data = {
            'id': mock_user_id,
            'email': mock_email,
            'username': f'testuser_{mock_user_id[:8]}',
            'password_hash': 'hashed_password',
            'first_name': 'Flask',
            'last_name': 'Test'
        }
        response = client.table('users').insert(user_data).execute()
        if response.data:
            user_data = response.data[0]
            print(f"✅ Created mock user: {user_data['email']}")
            return User(id=user_data['id'], email=user_data['email'], name=f"{user_data['first_name']} {user_data['last_name']}")
        else:
            print("❌ Failed to create mock user - no data returned")
    except Exception as e:
        print(f"❌ Error creating mock user: {e}")
    
    return User(id='12345678-1234-1234-1234-123456789012', email=mock_email, name='Flask Test')

mock_user = get_or_create_mock_user()

@topics.route('/topics')
def list_topics():
    try:
        topics_list = Topic.get_all_by_user(mock_user.id)
        return render_template('topics/list.html', topics=topics_list)
    except Exception as e:
        flash('Error loading topics. Please try again.', 'error')
        return render_template('topics/list.html', topics=[])

@topics.route('/topics/debug')
def debug_env():
    import os
    return {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'Not set')[:20] + '...' if os.getenv('SUPABASE_SERVICE_ROLE_KEY') else 'Not set',
        'SUPABASE_AVAILABLE': os.getenv('SUPABASE_AVAILABLE', 'Not set')
    }

@topics.route('/topics/new', methods=['GET', 'POST'])
def create_topic():
    form = TopicForm()
    
    if form.validate_on_submit():
        try:
            print(f"=== TOPIC CREATION REQUEST ===")
            print(f"Attempting to create topic: {form.title.data.strip()}")
            print(f"User ID: {mock_user.id}")
            print(f"Supabase URL: {os.getenv('SUPABASE_URL')}")
            print(f"Supabase Service Role Key: {os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'Not set')[:20]}...")
            print(f"Supabase Available: {os.getenv('SUPABASE_AVAILABLE', 'Not set')}")
            
            from app.models import get_supabase_client, SUPABASE_AVAILABLE
            client = get_supabase_client()
            print(f"Supabase client available: {SUPABASE_AVAILABLE}")
            print(f"Supabase client object: {client is not None}")
            
            topic = Topic.create(
                title=form.title.data.strip(),
                description=form.description.data.strip(),
                user_id=mock_user.id
            )
            
            if topic:
                flash('Topic created successfully!', 'success')
                return redirect(url_for('topics.view_topic', topic_id=topic.id))
            else:
                flash('Error creating topic. Please try again.', 'error')
        except Exception as e:
            print(f"Exception creating topic: {e}")
            flash(f'Error creating topic: {str(e)}', 'error')
    
    return render_template('topics/form.html', form=form, title='Create New Topic')

@topics.route('/topics/<topic_id>')
def view_topic(topic_id):
    try:
        print(f"=== VIEWING TOPIC ===")
        print(f"Topic ID: {topic_id}")
        print(f"User ID: {mock_user.id}")
        
        topic = Topic.get_by_id(topic_id, mock_user.id)
        print(f"Topic found: {topic is not None}")
        if topic:
            print(f"Topic title: {topic.title}")
        
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        print(f"Getting session data for topic: {topic_id}")
        try:
            topic_sessions = StudySession.get_topic_sessions(topic_id, mock_user.id)
            print(f"Got {len(topic_sessions)} sessions")
        except Exception as e:
            print(f"Error getting topic sessions: {e}")
            topic_sessions = []
        
        try:
            topic_progress = StudySession.get_topic_progress(topic_id, mock_user.id)
            print(f"Got topic progress: {topic_progress}")
        except Exception as e:
            print(f"Error getting topic progress: {e}")
            topic_progress = {}
        
        recent_sessions = topic_sessions[:5]
        
        print(f"Rendering template with topic: {topic.title}")
        return render_template('topics/view.html', 
                             topic=topic, 
                             topic_sessions=topic_sessions,
                             topic_progress=topic_progress,
                             recent_sessions=recent_sessions)
    except Exception as e:
        print(f"❌ Exception in view_topic: {e}")
        import traceback
        traceback.print_exc()
        flash('Error loading topic. Please try again.', 'error')
        return redirect(url_for('topics.list_topics'))

@topics.route('/topics/<topic_id>/edit', methods=['GET', 'POST'])
def edit_topic(topic_id):
    try:
        topic = Topic.get_by_id(topic_id, mock_user.id)
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        form = TopicForm()
        
        if request.method == 'GET':
            form.title.data = topic.title
            form.description.data = topic.description
        
        if form.validate_on_submit():
            success = topic.update(
                title=form.title.data.strip(),
                description=form.description.data.strip()
            )
            
            if success:
                flash('Topic updated successfully!', 'success')
                return redirect(url_for('topics.view_topic', topic_id=topic.id))
            else:
                flash('Error updating topic. Please try again.', 'error')
        
        return render_template('topics/form.html', form=form, topic=topic, title='Edit Topic')
    
    except Exception as e:
        flash('Error loading topic. Please try again.', 'error')
        return redirect(url_for('topics.list_topics'))

@topics.route('/topics/<topic_id>/delete', methods=['POST'])
def delete_topic(topic_id):
    try:
        topic = Topic.get_by_id(topic_id, mock_user.id)
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        success = topic.delete()
        
        if success:
            flash('Topic deleted successfully!', 'success')
        else:
            flash('Error deleting topic. Please try again.', 'error')
        
        return redirect(url_for('topics.list_topics'))
    
    except Exception as e:
        flash('Error deleting topic. Please try again.', 'error')
        return redirect(url_for('topics.list_topics'))

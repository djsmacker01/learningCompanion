

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.gcse_resources import (
    GCSELearningResource, GCSERevisionMaterial, GCSEEducationalContent,
    GCSEResourceRecommendationEngine, GCSEResourceTracker
)
from app.models.gcse_curriculum import GCSESubject
from app.models import Topic
from app.routes.topics import get_current_user
from datetime import datetime, date, timedelta
import json

gcse_resources = Blueprint('gcse_resources', __name__, url_prefix='/gcse/resources')

@gcse_resources.route('/')
@login_required
def resources_dashboard():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        
        recommendation_engine = GCSEResourceRecommendationEngine(user.id)
        recommendations = recommendation_engine.get_personalized_recommendations()
        
        
        resource_tracker = GCSEResourceTracker(user.id)
        recent_resources = resource_tracker.get_user_resource_history(days_back=7)
        
        
        featured_resources = GCSELearningResource._get_default_resources()[:4]
        
        return render_template('gcse/resources/dashboard.html',
                             user_gcse_topics=user_gcse_topics,
                             recommendations=recommendations,
                             recent_resources=recent_resources,
                             featured_resources=featured_resources)
    
    except Exception as e:
        flash('Error loading resources dashboard.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_resources.route('/browse')
@login_required
def browse_resources():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.args.get('subject_id')
        resource_type = request.args.get('resource_type')
        difficulty = request.args.get('difficulty')
        free_only = request.args.get('free_only', 'false').lower() == 'true'
        search_term = request.args.get('search')
        
        
        if search_term:
            resources = GCSELearningResource.search_resources(
                search_term, subject_id, resource_type
            )
        else:
            resources = GCSELearningResource.get_resources_by_subject(
                subject_id, resource_type, difficulty, free_only
            )
        
        
        subjects = GCSESubject.get_all_subjects()
        resource_types = ["video", "document", "interactive", "quiz", "audio", "image"]
        difficulties = ["beginner", "intermediate", "advanced"]
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/resources/browse.html',
                             resources=resources,
                             subjects=subjects,
                             resource_types=resource_types,
                             difficulties=difficulties,
                             selected_subject_id=subject_id,
                             selected_resource_type=resource_type,
                             selected_difficulty=difficulty,
                             free_only=free_only,
                             search_term=search_term,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading resource browser.', 'error')
        return redirect(url_for('gcse_resources.resources_dashboard'))

@gcse_resources.route('/resource/<resource_id>')
@login_required
def resource_detail(resource_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        resource = GCSELearningResource.get_resource_by_id(resource_id)
        if not resource:
            flash('Learning resource not found.', 'error')
            return redirect(url_for('gcse_resources.browse_resources'))
        
        
        resource_tracker = GCSEResourceTracker(user.id)
        resource_tracker.track_resource_access(
            resource_id, resource.resource_type, 'view'
        )
        
        
        related_resources = GCSELearningResource.get_resources_by_subject(
            resource.subject_id
        )[:4]
        
        related_resources = [r for r in related_resources if r.id != resource_id]
        
        return render_template('gcse/resources/resource_detail.html',
                             resource=resource,
                             related_resources=related_resources)
    
    except Exception as e:
        flash('Error loading resource details.', 'error')
        return redirect(url_for('gcse_resources.browse_resources'))

@gcse_resources.route('/revision-materials')
@login_required
def revision_materials():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.args.get('subject_id')
        material_type = request.args.get('material_type')
        
        
        materials = GCSERevisionMaterial.get_materials_by_subject(subject_id, material_type)
        
        
        subjects = GCSESubject.get_all_subjects()
        material_types = ["revision_guide", "summary_sheet", "mind_map", "flashcards", "practice_paper"]
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/resources/revision_materials.html',
                             materials=materials,
                             subjects=subjects,
                             material_types=material_types,
                             selected_subject_id=subject_id,
                             selected_material_type=material_type,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading revision materials.', 'error')
        return redirect(url_for('gcse_resources.resources_dashboard'))

@gcse_resources.route('/educational-content')
@login_required
def educational_content():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.args.get('subject_id')
        content_type = request.args.get('content_type')
        
        
        content = GCSEEducationalContent.get_content_by_subject(subject_id, content_type)
        
        
        subjects = GCSESubject.get_all_subjects()
        content_types = ["lesson", "tutorial", "case_study", "experiment", "project"]
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/resources/educational_content.html',
                             content=content,
                             subjects=subjects,
                             content_types=content_types,
                             selected_subject_id=subject_id,
                             selected_content_type=content_type,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading educational content.', 'error')
        return redirect(url_for('gcse_resources.resources_dashboard'))

@gcse_resources.route('/recommendations')
@login_required
def personalized_recommendations():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.args.get('subject_id')
        learning_style = request.args.get('learning_style')
        
        
        recommendation_engine = GCSEResourceRecommendationEngine(user.id)
        recommendations = recommendation_engine.get_personalized_recommendations(
            subject_id, learning_style
        )
        
        
        resource_tracker = GCSEResourceTracker(user.id)
        recent_resources = resource_tracker.get_user_resource_history(days_back=30)
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/resources/recommendations.html',
                             recommendations=recommendations,
                             recent_resources=recent_resources,
                             user_gcse_topics=user_gcse_topics,
                             selected_subject_id=subject_id,
                             selected_learning_style=learning_style)
    
    except Exception as e:
        flash('Error loading recommendations.', 'error')
        return redirect(url_for('gcse_resources.resources_dashboard'))

@gcse_resources.route('/my-resources')
@login_required
def my_resources():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        resource_tracker = GCSEResourceTracker(user.id)
        resource_history = resource_tracker.get_user_resource_history(days_back=90)
        
        
        recommended_resources = resource_tracker.get_recommended_resources()
        
        
        user_gcse_topics = Topic.get_topics_by_user(user.id, gcse_only=True)
        
        return render_template('gcse/resources/my_resources.html',
                             resource_history=resource_history,
                             recommended_resources=recommended_resources,
                             user_gcse_topics=user_gcse_topics)
    
    except Exception as e:
        flash('Error loading your resources.', 'error')
        return redirect(url_for('gcse_resources.resources_dashboard'))

@gcse_resources.route('/download/<resource_id>')
@login_required
def download_resource(resource_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        resource = GCSELearningResource.get_resource_by_id(resource_id)
        if not resource:
            flash('Resource not found.', 'error')
            return redirect(url_for('gcse_resources.browse_resources'))
        
        
        resource_tracker = GCSEResourceTracker(user.id)
        resource_tracker.track_resource_access(
            resource_id, resource.resource_type, 'download'
        )
        
        
        
        if resource.content_url:
            return redirect(resource.content_url)
        else:
            flash('Download link not available.', 'error')
            return redirect(url_for('gcse_resources.resource_detail', resource_id=resource_id))
    
    except Exception as e:
        flash('Error downloading resource.', 'error')
        return redirect(url_for('gcse_resources.browse_resources'))


@gcse_resources.route('/api/resources')
@login_required
def api_get_resources():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        subject_id = request.args.get('subject_id')
        resource_type = request.args.get('resource_type')
        difficulty = request.args.get('difficulty')
        free_only = request.args.get('free_only', 'false').lower() == 'true'
        search_term = request.args.get('search')
        
        
        if search_term:
            resources = GCSELearningResource.search_resources(
                search_term, subject_id, resource_type
            )
        else:
            resources = GCSELearningResource.get_resources_by_subject(
                subject_id, resource_type, difficulty, free_only
            )
        
        
        resources_data = []
        for resource in resources:
            resources_data.append({
                'id': resource.id,
                'title': resource.title,
                'resource_type': resource.resource_type,
                'subject_id': resource.subject_id,
                'topic_area': resource.topic_area,
                'difficulty_level': resource.difficulty_level,
                'description': resource.description,
                'thumbnail_url': resource.thumbnail_url,
                'duration_minutes': resource.duration_minutes,
                'rating': resource.rating,
                'is_free': resource.is_free,
                'tags': resource.tags
            })
        
        return jsonify({
            'success': True,
            'resources': resources_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_resources.route('/api/track-access', methods=['POST'])
@login_required
def api_track_resource_access():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        resource_id = data.get('resource_id')
        resource_type = data.get('resource_type')
        action = data.get('action')
        duration_seconds = data.get('duration_seconds')
        
        if not all([resource_id, resource_type, action]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        
        resource_tracker = GCSEResourceTracker(user.id)
        success = resource_tracker.track_resource_access(
            resource_id, resource_type, action, duration_seconds
        )
        
        return jsonify({
            'success': success
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_resources.route('/api/recommendations')
@login_required
def api_get_recommendations():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        subject_id = request.args.get('subject_id')
        learning_style = request.args.get('learning_style')
        
        
        recommendation_engine = GCSEResourceRecommendationEngine(user.id)
        recommendations = recommendation_engine.get_personalized_recommendations(
            subject_id, learning_style
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


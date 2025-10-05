"""
Smart Content Generation API Routes
AI-powered content creation endpoints
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.routes.topics import get_current_user
from app.utils.smart_content_generator import SmartContentGenerator
from datetime import datetime
import json

smart_content = Blueprint('smart_content', __name__, url_prefix='/content')

@smart_content.route('/')
@login_required
def content_dashboard():
    """Smart Content Generation Dashboard"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        generator = SmartContentGenerator(user.id)
        
        return render_template('smart_content/dashboard.html', user=user)
    
    except Exception as e:
        print(f"Error loading content dashboard: {e}")
        return jsonify({'error': 'Failed to load dashboard'}), 500

@smart_content.route('/api/generate-notes/<topic_id>')
@login_required
def generate_study_notes(topic_id):
    """Generate AI-powered study notes"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        generator = SmartContentGenerator(user.id)
        
        # Get optional content type parameter
        content_type = request.args.get('type', 'comprehensive')
        
        notes = generator.generate_study_notes(topic_id, content_type)
        
        return jsonify(notes)
    
    except Exception as e:
        print(f"Error generating study notes: {e}")
        return jsonify({'error': 'Failed to generate study notes'}), 500

@smart_content.route('/api/generate-interactive/<topic_id>')
@login_required
def generate_interactive_content(topic_id):
    """Generate interactive learning content"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        generator = SmartContentGenerator(user.id)
        
        # Get optional content type parameter
        content_type = request.args.get('type', 'quiz')
        
        content = generator.generate_interactive_content(topic_id, content_type)
        
        return jsonify(content)
    
    except Exception as e:
        print(f"Error generating interactive content: {e}")
        return jsonify({'error': 'Failed to generate interactive content'}), 500

@smart_content.route('/api/generate-visual/<topic_id>')
@login_required
def generate_visual_aids(topic_id):
    """Generate visual learning aids"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        generator = SmartContentGenerator(user.id)
        
        # Get optional visual type parameter
        visual_type = request.args.get('type', 'mind_map')
        
        visual = generator.generate_visual_learning_aids(topic_id, visual_type)
        
        return jsonify(visual)
    
    except Exception as e:
        print(f"Error generating visual aids: {e}")
        return jsonify({'error': 'Failed to generate visual aids'}), 500

@smart_content.route('/api/generate-personalized/<topic_id>')
@login_required
def generate_personalized_content(topic_id):
    """Generate personalized content based on learning style"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        generator = SmartContentGenerator(user.id)
        
        # Get optional learning style parameter
        learning_style = request.args.get('style', 'visual')
        
        content = generator.generate_personalized_content(topic_id, learning_style)
        
        return jsonify(content)
    
    except Exception as e:
        print(f"Error generating personalized content: {e}")
        return jsonify({'error': 'Failed to generate personalized content'}), 500

@smart_content.route('/api/generate-summary/<topic_id>')
@login_required
def generate_content_summary(topic_id):
    """Generate content summary"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        generator = SmartContentGenerator(user.id)
        
        # Get optional summary type parameter
        summary_type = request.args.get('type', 'overview')
        
        summary = generator.generate_content_summary(topic_id, summary_type)
        
        return jsonify(summary)
    
    except Exception as e:
        print(f"Error generating content summary: {e}")
        return jsonify({'error': 'Failed to generate content summary'}), 500

@smart_content.route('/api/generate-learning-path/<topic_id>')
@login_required
def generate_learning_path(topic_id):
    """Generate structured learning path"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        generator = SmartContentGenerator(user.id)
        
        # Get optional difficulty level parameter
        difficulty_level = request.args.get('difficulty', 'intermediate')
        
        learning_path = generator.generate_learning_path(topic_id, difficulty_level)
        
        return jsonify(learning_path)
    
    except Exception as e:
        print(f"Error generating learning path: {e}")
        return jsonify({'error': 'Failed to generate learning path'}), 500

@smart_content.route('/api/comprehensive-generation/<topic_id>')
@login_required
def comprehensive_content_generation(topic_id):
    """Generate comprehensive content package for a topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        generator = SmartContentGenerator(user.id)
        
        # Get optional parameters
        learning_style = request.args.get('learning_style', 'visual')
        difficulty_level = request.args.get('difficulty', 'intermediate')
        content_types = request.args.getlist('types') or ['notes', 'quiz', 'summary']
        
        # Generate multiple types of content
        content_package = {
            'topic_id': topic_id,
            'generated_at': datetime.now().isoformat(),
            'content_types': content_types,
            'learning_style': learning_style,
            'difficulty_level': difficulty_level
        }
        
        # Generate each requested content type
        if 'notes' in content_types:
            content_package['study_notes'] = generator.generate_study_notes(topic_id, 'comprehensive')
        
        if 'quiz' in content_types:
            content_package['interactive_quiz'] = generator.generate_interactive_content(topic_id, 'quiz')
        
        if 'summary' in content_types:
            content_package['summary'] = generator.generate_content_summary(topic_id, 'overview')
        
        if 'visual' in content_types:
            content_package['visual_aids'] = generator.generate_visual_learning_aids(topic_id, 'mind_map')
        
        if 'personalized' in content_types:
            content_package['personalized_content'] = generator.generate_personalized_content(topic_id, learning_style)
        
        if 'learning_path' in content_types:
            content_package['learning_path'] = generator.generate_learning_path(topic_id, difficulty_level)
        
        return jsonify(content_package)
    
    except Exception as e:
        print(f"Error generating comprehensive content: {e}")
        return jsonify({'error': 'Failed to generate comprehensive content'}), 500

@smart_content.route('/api/content-types')
@login_required
def get_content_types():
    """Get available content generation types"""
    try:
        content_types = {
            'study_notes': {
                'types': ['comprehensive', 'summary', 'key_points', 'exam_focused'],
                'description': 'AI-generated study notes in various formats'
            },
            'interactive_content': {
                'types': ['quiz', 'flashcards', 'scenarios', 'exercises'],
                'description': 'Interactive learning content'
            },
            'visual_aids': {
                'types': ['mind_map', 'diagram', 'timeline', 'flowchart'],
                'description': 'Visual learning aids and diagrams'
            },
            'personalized_content': {
                'types': ['visual', 'auditory', 'kinesthetic', 'reading'],
                'description': 'Content adapted to learning style'
            },
            'summaries': {
                'types': ['overview', 'key_concepts', 'exam_summary', 'quick_reference'],
                'description': 'Various types of content summaries'
            },
            'learning_paths': {
                'types': ['beginner', 'intermediate', 'advanced'],
                'description': 'Structured learning progression'
            }
        }
        
        return jsonify(content_types)
    
    except Exception as e:
        print(f"Error getting content types: {e}")
        return jsonify({'error': 'Failed to get content types'}), 500

@smart_content.route('/generator')
@login_required
def content_generator():
    """Interactive content generator interface"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        return render_template('smart_content/generator.html', user=user)
    
    except Exception as e:
        print(f"Error loading content generator: {e}")
        return jsonify({'error': 'Failed to load content generator'}), 500

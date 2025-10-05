"""
Learning Style Detection and Personalization API Routes
Advanced learning style analysis and adaptive learning features
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.routes.topics import get_current_user
from app.utils.learning_style_detection import LearningStyleDetector
from datetime import datetime
import json

learning_style = Blueprint('learning_style', __name__, url_prefix='/learning-style')

@learning_style.route('/')
@login_required
def learning_style_dashboard():
    """Learning Style Detection and Personalization Dashboard"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        detector = LearningStyleDetector(user.id)
        
        return render_template('learning_style/dashboard.html', user=user)
    
    except Exception as e:
        print(f"Error loading learning style dashboard: {e}")
        return jsonify({'error': 'Failed to load dashboard'}), 500

@learning_style.route('/api/analyze-learning-style', methods=['POST'])
@login_required
def analyze_learning_style():
    """Analyze user's learning style based on behavior data"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        detector = LearningStyleDetector(user.id)
        
        # Get user behavior data from request
        user_behavior_data = request.get_json() or {}
        
        # If no data provided, generate sample data for demonstration
        if not user_behavior_data:
            user_behavior_data = {
                'study_sessions': [
                    {'duration_minutes': 45, 'content_type': 'video', 'performance': 85, 'time_of_day': 'morning'},
                    {'duration_minutes': 30, 'content_type': 'text', 'performance': 78, 'time_of_day': 'afternoon'},
                    {'duration_minutes': 60, 'content_type': 'interactive', 'performance': 92, 'time_of_day': 'evening'}
                ],
                'quiz_results': [
                    {'score': 85, 'question_type': 'multiple_choice', 'time_spent': 120},
                    {'score': 78, 'question_type': 'essay', 'time_spent': 300},
                    {'score': 92, 'question_type': 'visual', 'time_spent': 90}
                ],
                'content_interactions': [
                    {'content_type': 'video', 'engagement_time': 180, 'completion_rate': 0.95},
                    {'content_type': 'text', 'engagement_time': 240, 'completion_rate': 0.80},
                    {'content_type': 'interactive', 'engagement_time': 150, 'completion_rate': 0.98}
                ]
            }
        
        analysis = detector.analyze_learning_style(user_behavior_data)
        
        return jsonify(analysis)
    
    except Exception as e:
        print(f"Error analyzing learning style: {e}")
        return jsonify({'error': 'Failed to analyze learning style'}), 500

@learning_style.route('/api/create-adaptive-learning-path', methods=['POST'])
@login_required
def create_adaptive_learning_path():
    """Create adaptive learning path based on learning style"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        detector = LearningStyleDetector(user.id)
        
        # Get parameters from request
        data = request.get_json()
        
        subject = data.get('subject')
        current_level = data.get('current_level', 'beginner')
        target_level = data.get('target_level', 'intermediate')
        learning_style = data.get('learning_style', 'visual')
        
        if not subject:
            return jsonify({'error': 'Subject is required'}), 400
        
        learning_path = detector.create_adaptive_learning_path(subject, current_level, target_level, learning_style)
        
        return jsonify(learning_path)
    
    except Exception as e:
        print(f"Error creating adaptive learning path: {e}")
        return jsonify({'error': 'Failed to create adaptive learning path'}), 500

@learning_style.route('/api/personalize-content-delivery', methods=['POST'])
@login_required
def personalize_content_delivery():
    """Personalize content delivery based on learning style"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        detector = LearningStyleDetector(user.id)
        
        # Get parameters from request
        data = request.get_json()
        
        content_id = data.get('content_id')
        user_learning_style = data.get('learning_style', 'visual')
        performance_history = data.get('performance_history', {})
        
        if not content_id:
            return jsonify({'error': 'Content ID is required'}), 400
        
        personalized_content = detector.personalize_content_delivery(content_id, user_learning_style, performance_history)
        
        return jsonify(personalized_content)
    
    except Exception as e:
        print(f"Error personalizing content delivery: {e}")
        return jsonify({'error': 'Failed to personalize content delivery'}), 500

@learning_style.route('/api/analyze-learning-progress')
@login_required
def analyze_learning_progress():
    """Analyze learning progress with style-specific insights"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        detector = LearningStyleDetector(user.id)
        
        # Get parameters
        time_period = request.args.get('time_period', '30_days')
        
        progress_analysis = detector.analyze_learning_progress(user.id, time_period)
        
        return jsonify(progress_analysis)
    
    except Exception as e:
        print(f"Error analyzing learning progress: {e}")
        return jsonify({'error': 'Failed to analyze learning progress'}), 500

@learning_style.route('/api/create-intelligent-study-schedule', methods=['POST'])
@login_required
def create_intelligent_study_schedule():
    """Create intelligent study schedule based on learning style"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        detector = LearningStyleDetector(user.id)
        
        # Get parameters from request
        data = request.get_json()
        
        user_learning_style = data.get('learning_style', 'visual')
        available_time = data.get('available_time', {
            'monday': {'morning': 60, 'afternoon': 90, 'evening': 120},
            'tuesday': {'morning': 60, 'afternoon': 90, 'evening': 120},
            'wednesday': {'morning': 60, 'afternoon': 90, 'evening': 120},
            'thursday': {'morning': 60, 'afternoon': 90, 'evening': 120},
            'friday': {'morning': 60, 'afternoon': 90, 'evening': 120},
            'saturday': {'morning': 120, 'afternoon': 180, 'evening': 90},
            'sunday': {'morning': 120, 'afternoon': 180, 'evening': 90}
        })
        subjects = data.get('subjects', ['Mathematics', 'English', 'Science'])
        priorities = data.get('priorities', {'Mathematics': 'high', 'English': 'medium', 'Science': 'low'})
        
        study_schedule = detector.create_intelligent_study_schedule(
            user_learning_style, available_time, subjects, priorities
        )
        
        return jsonify(study_schedule)
    
    except Exception as e:
        print(f"Error creating intelligent study schedule: {e}")
        return jsonify({'error': 'Failed to create intelligent study schedule'}), 500

@learning_style.route('/api/generate-learning-insights')
@login_required
def generate_learning_insights():
    """Generate comprehensive learning insights and recommendations"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        detector = LearningStyleDetector(user.id)
        
        # Get parameters
        analysis_depth = request.args.get('analysis_depth', 'comprehensive')
        
        insights = detector.generate_learning_insights(user.id, analysis_depth)
        
        return jsonify(insights)
    
    except Exception as e:
        print(f"Error generating learning insights: {e}")
        return jsonify({'error': 'Failed to generate learning insights'}), 500

@learning_style.route('/api/learning-styles')
@login_required
def get_learning_styles():
    """Get available learning styles and their characteristics"""
    try:
        learning_styles = [
            {
                'id': 'visual',
                'name': 'Visual Learner',
                'description': 'Learns best through images, diagrams, charts, and visual representations',
                'characteristics': [
                    'Prefers visual aids and diagrams',
                    'Benefits from color coding and highlighting',
                    'Likes mind maps and flowcharts',
                    'Remembers information through spatial relationships'
                ],
                'recommended_methods': [
                    'Use visual flashcards with images',
                    'Create mind maps and diagrams',
                    'Watch educational videos',
                    'Use highlighters and color coding'
                ]
            },
            {
                'id': 'auditory',
                'name': 'Auditory Learner',
                'description': 'Learns best through listening, discussions, and verbal explanations',
                'characteristics': [
                    'Prefers verbal instructions and explanations',
                    'Benefits from group discussions',
                    'Likes to read aloud and hear information',
                    'Remembers information through sound and rhythm'
                ],
                'recommended_methods': [
                    'Record lectures and explanations',
                    'Participate in study groups',
                    'Use mnemonic devices and rhymes',
                    'Read notes aloud'
                ]
            },
            {
                'id': 'kinesthetic',
                'name': 'Kinesthetic Learner',
                'description': 'Learns best through hands-on activities, movement, and physical interaction',
                'characteristics': [
                    'Prefers hands-on activities and experiments',
                    'Benefits from physical movement and touch',
                    'Likes to build and create things',
                    'Remembers information through physical experience'
                ],
                'recommended_methods': [
                    'Use hands-on activities and experiments',
                    'Take frequent breaks and move around',
                    'Use manipulatives and physical models',
                    'Study in different locations'
                ]
            },
            {
                'id': 'reading_writing',
                'name': 'Reading/Writing Learner',
                'description': 'Learns best through text-based materials, note-taking, and written exercises',
                'characteristics': [
                    'Prefers written instructions and materials',
                    'Benefits from note-taking and writing',
                    'Likes to read extensively',
                    'Remembers information through written repetition'
                ],
                'recommended_methods': [
                    'Take detailed written notes',
                    'Create written summaries and outlines',
                    'Use text-based flashcards',
                    'Write practice essays and explanations'
                ]
            },
            {
                'id': 'multimodal',
                'name': 'Multimodal Learner',
                'description': 'Combines multiple learning styles effectively and adapts to different situations',
                'characteristics': [
                    'Uses multiple learning methods',
                    'Adapts to different content types',
                    'Benefits from varied approaches',
                    'Flexible in learning preferences'
                ],
                'recommended_methods': [
                    'Combine visual, auditory, and kinesthetic methods',
                    'Use varied content formats',
                    'Adapt methods based on subject',
                    'Experiment with different approaches'
                ]
            }
        ]
        
        return jsonify({'learning_styles': learning_styles})
    
    except Exception as e:
        print(f"Error getting learning styles: {e}")
        return jsonify({'error': 'Failed to get learning styles'}), 500

@learning_style.route('/api/learning-style-assessment')
@login_required
def learning_style_assessment():
    """Get learning style assessment questions"""
    try:
        assessment_questions = [
            {
                'id': 1,
                'question': 'When learning new information, I prefer to:',
                'options': [
                    {'id': 'a', 'text': 'See diagrams, charts, or visual representations', 'style': 'visual'},
                    {'id': 'b', 'text': 'Listen to explanations or discussions', 'style': 'auditory'},
                    {'id': 'c', 'text': 'Try hands-on activities or experiments', 'style': 'kinesthetic'},
                    {'id': 'd', 'text': 'Read written materials and take notes', 'style': 'reading_writing'}
                ]
            },
            {
                'id': 2,
                'question': 'I remember information best when:',
                'options': [
                    {'id': 'a', 'text': 'I can see it in a diagram or picture', 'style': 'visual'},
                    {'id': 'b', 'text': 'I hear it explained or discussed', 'style': 'auditory'},
                    {'id': 'c', 'text': 'I physically do something with it', 'style': 'kinesthetic'},
                    {'id': 'd', 'text': 'I write it down or read about it', 'style': 'reading_writing'}
                ]
            },
            {
                'id': 3,
                'question': 'When studying, I find it most helpful to:',
                'options': [
                    {'id': 'a', 'text': 'Use highlighters and create visual summaries', 'style': 'visual'},
                    {'id': 'b', 'text': 'Read aloud or discuss with others', 'style': 'auditory'},
                    {'id': 'c', 'text': 'Take breaks and move around', 'style': 'kinesthetic'},
                    {'id': 'd', 'text': 'Take detailed notes and make lists', 'style': 'reading_writing'}
                ]
            },
            {
                'id': 4,
                'question': 'I prefer learning materials that are:',
                'options': [
                    {'id': 'a', 'text': 'Rich with images, videos, and visual aids', 'style': 'visual'},
                    {'id': 'b', 'text': 'Audio recordings or verbal explanations', 'style': 'auditory'},
                    {'id': 'c', 'text': 'Interactive and hands-on', 'style': 'kinesthetic'},
                    {'id': 'd', 'text': 'Text-based with clear written instructions', 'style': 'reading_writing'}
                ]
            },
            {
                'id': 5,
                'question': 'When solving problems, I typically:',
                'options': [
                    {'id': 'a', 'text': 'Draw diagrams or visualize the problem', 'style': 'visual'},
                    {'id': 'b', 'text': 'Talk through the problem out loud', 'style': 'auditory'},
                    {'id': 'c', 'text': 'Try different approaches physically', 'style': 'kinesthetic'},
                    {'id': 'd', 'text': 'Write out the steps and work through them', 'style': 'reading_writing'}
                ]
            },
            {
                'id': 6,
                'question': 'I learn best in environments that are:',
                'options': [
                    {'id': 'a', 'text': 'Visually organized with charts and posters', 'style': 'visual'},
                    {'id': 'b', 'text': 'Quiet for listening or with background discussion', 'style': 'auditory'},
                    {'id': 'c', 'text': 'Spacious for movement and hands-on activities', 'style': 'kinesthetic'},
                    {'id': 'd', 'text': 'Well-lit with access to books and writing materials', 'style': 'reading_writing'}
                ]
            }
        ]
        
        return jsonify({'assessment_questions': assessment_questions})
    
    except Exception as e:
        print(f"Error getting learning style assessment: {e}")
        return jsonify({'error': 'Failed to get learning style assessment'}), 500

@learning_style.route('/api/submit-assessment', methods=['POST'])
@login_required
def submit_learning_style_assessment():
    """Submit learning style assessment and get results"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        detector = LearningStyleDetector(user.id)
        
        # Get assessment responses
        responses = request.get_json()
        
        if not responses or 'answers' not in responses:
            return jsonify({'error': 'Assessment responses are required'}), 400
        
        # Process assessment responses
        style_scores = {
            'visual': 0,
            'auditory': 0,
            'kinesthetic': 0,
            'reading_writing': 0
        }
        
        for answer in responses['answers']:
            if 'style' in answer:
                style_scores[answer['style']] += 1
        
        # Determine primary learning style
        primary_style = max(style_scores, key=style_scores.get)
        
        # Create behavior data from assessment
        behavior_data = {
            'assessment_responses': responses['answers'],
            'style_scores': style_scores,
            'primary_style': primary_style
        }
        
        # Analyze learning style
        analysis = detector.analyze_learning_style(behavior_data)
        
        return jsonify({
            'assessment_results': {
                'primary_learning_style': primary_style,
                'style_scores': style_scores,
                'analysis': analysis
            }
        })
    
    except Exception as e:
        print(f"Error submitting learning style assessment: {e}")
        return jsonify({'error': 'Failed to submit assessment'}), 500

@learning_style.route('/personalization-center')
@login_required
def personalization_center():
    """Personalization Center - Advanced learning personalization"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        return render_template('learning_style/personalization_center.html', user=user)
    
    except Exception as e:
        print(f"Error loading personalization center: {e}")
        return jsonify({'error': 'Failed to load personalization center'}), 500

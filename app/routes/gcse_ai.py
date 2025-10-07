"""
GCSE AI Enhancement API Routes
GCSE-specific AI features and integration endpoints
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.routes.topics import get_current_user
from app.utils.gcse_ai_enhancement import GCSEAIEnhancement
from datetime import datetime
import json

gcse_ai = Blueprint('gcse_ai', __name__, url_prefix='/gcse-ai')

@gcse_ai.route('/')
@login_required
def gcse_ai_dashboard():
    """GCSE AI Enhancement Dashboard"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        return render_template('gcse_ai/dashboard.html', user=user)
    
    except Exception as e:
        print(f"Error loading GCSE AI dashboard: {e}")
        return jsonify({'error': 'Failed to load dashboard'}), 500

@gcse_ai.route('/api/study-plan')
@login_required
def generate_gcse_study_plan():
    """Generate comprehensive GCSE study plan"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get required parameters
        subject = request.args.get('subject')
        exam_board = request.args.get('exam_board')
        target_grade = request.args.get('target_grade')
        exam_date = request.args.get('exam_date')
        
        if not all([subject, exam_board, target_grade, exam_date]):
            return jsonify({'error': 'Missing required parameters: subject, exam_board, target_grade, exam_date'}), 400
        
        study_plan = enhancement.generate_gcse_study_plan(subject, exam_board, target_grade, exam_date)
        
        return jsonify(study_plan)
    
    except Exception as e:
        print(f"Error generating GCSE study plan: {e}")
        return jsonify({'error': 'Failed to generate study plan'}), 500

@gcse_ai.route('/api/past-paper-analysis')
@login_required
def analyze_gcse_past_papers():
    """Analyze GCSE past papers for patterns and insights"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get parameters
        subject = request.args.get('subject')
        exam_board = request.args.get('exam_board')
        paper_type = request.args.get('paper_type', 'recent')
        
        if not all([subject, exam_board]):
            return jsonify({'error': 'Missing required parameters: subject, exam_board'}), 400
        
        analysis = enhancement.generate_gcse_past_paper_analysis(subject, exam_board, paper_type)
        
        return jsonify(analysis)
    
    except Exception as e:
        print(f"Error analyzing GCSE past papers: {e}")
        return jsonify({'error': 'Failed to analyze past papers'}), 500

@gcse_ai.route('/api/grade-boundary-predictions', methods=['GET', 'POST'])
@login_required
def predict_gcse_grade_boundaries():
    """Predict GCSE grade boundaries and student performance"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get parameters
        subject = request.args.get('subject')
        exam_board = request.args.get('exam_board')
        
        if not all([subject, exam_board]):
            return jsonify({'error': 'Missing required parameters: subject, exam_board'}), 400
        
        # Get current performance from request body (POST) or default
        current_performance = request.get_json() or {}
        
        print(f"Predicting grade boundaries for {subject} ({exam_board})")
        print(f"Current performance: {current_performance}")
        
        predictions = enhancement.generate_gcse_grade_boundary_predictions(subject, exam_board, current_performance)
        
        print(f"Predictions generated: {predictions.keys() if isinstance(predictions, dict) else type(predictions)}")
        
        return jsonify(predictions)
    
    except Exception as e:
        print(f"Error predicting GCSE grade boundaries: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to predict grade boundaries: {str(e)}'}), 500

@gcse_ai.route('/api/revision-schedule', methods=['POST'])
@login_required
def generate_gcse_revision_schedule():
    """Generate comprehensive GCSE revision schedule across multiple subjects"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get data from request body
        data = request.get_json()
        
        subjects = data.get('subjects', [])
        exam_dates = data.get('exam_dates', {})
        target_grades = data.get('target_grades', {})
        
        if not subjects:
            return jsonify({'error': 'At least one subject is required'}), 400
        
        revision_schedule = enhancement.generate_gcse_revision_schedule(subjects, exam_dates, target_grades)
        
        return jsonify(revision_schedule)
    
    except Exception as e:
        print(f"Error generating GCSE revision schedule: {e}")
        return jsonify({'error': 'Failed to generate revision schedule'}), 500

@gcse_ai.route('/api/exam-techniques')
@login_required
def generate_gcse_exam_techniques():
    """Generate GCSE-specific exam techniques and strategies"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get parameters
        subject = request.args.get('subject')
        exam_board = request.args.get('exam_board')
        question_types = request.args.getlist('question_types') or ['multiple_choice', 'short_answer', 'essay']
        
        if not all([subject, exam_board]):
            return jsonify({'error': 'Missing required parameters: subject, exam_board'}), 400
        
        techniques = enhancement.generate_gcse_exam_techniques(subject, exam_board, question_types)
        
        return jsonify(techniques)
    
    except Exception as e:
        print(f"Error generating GCSE exam techniques: {e}")
        return jsonify({'error': 'Failed to generate exam techniques'}), 500

@gcse_ai.route('/api/personalized-content')
@login_required
def generate_gcse_personalized_content():
    """Generate GCSE-specific personalized content"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get parameters
        subject = request.args.get('subject')
        topic = request.args.get('topic')
        learning_style = request.args.get('learning_style', 'visual')
        difficulty_level = request.args.get('difficulty_level', 'intermediate')
        
        if not all([subject, topic]):
            return jsonify({'error': 'Missing required parameters: subject, topic'}), 400
        
        print(f"Generating personalized content: {subject}/{topic} ({learning_style}, {difficulty_level})")
        
        content = enhancement.generate_gcse_personalized_content(subject, topic, learning_style, difficulty_level)
        
        print(f"Content generated with keys: {content.keys() if isinstance(content, dict) else type(content)}")
        
        return jsonify(content)
    
    except Exception as e:
        print(f"Error generating GCSE personalized content: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate personalized content: {str(e)}'}), 500

@gcse_ai.route('/api/performance-gap-analysis', methods=['POST'])
@login_required
def analyze_gcse_performance_gaps():
    """Analyze GCSE performance gaps and provide improvement strategies"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        enhancement = GCSEAIEnhancement(user.id)
        
        # Get data from request body
        data = request.get_json()
        
        subject = data.get('subject')
        user_performance = data.get('user_performance', {})
        
        if not subject:
            return jsonify({'error': 'Subject is required'}), 400
        
        analysis = enhancement.analyze_gcse_performance_gaps(subject, user_performance)
        
        return jsonify(analysis)
    
    except Exception as e:
        print(f"Error analyzing GCSE performance gaps: {e}")
        return jsonify({'error': 'Failed to analyze performance gaps'}), 500

@gcse_ai.route('/api/save-to-topics', methods=['POST'])
@login_required
def save_gcse_content_to_topics():
    """Save GCSE personalized content as a topic"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        subject = data.get('subject')
        topic_name = data.get('topic')
        content = data.get('content')
        learning_style = data.get('learning_style')
        difficulty = data.get('difficulty')
        
        if not all([subject, topic_name, content]):
            return jsonify({'error': 'Missing required data'}), 400
        
        # Import Topic model
        from app.models import Topic
        
        # Helper function to sanitize Unicode
        def sanitize_unicode(text):
            """Replace Unicode math symbols with ASCII equivalents"""
            if not text:
                return text
            return str(text).replace('√', 'sqrt').replace('≠', '!=').replace('±', '+/-').replace('²', '^2').replace('³', '^3').replace('×', '*').replace('÷', '/')
        
        # Create topic title (sanitize Unicode)
        title = sanitize_unicode(f"{subject.title()} - {topic_name}")
        
        # Build description from content (sanitize Unicode for ALL text)
        
        description = f"Personalized GCSE content for {sanitize_unicode(topic_name)}\n\n"
        description += f"Learning Style: {learning_style}\n"
        description += f"Difficulty: {difficulty}\n\n"
        
        # Add learning points (clean any problematic Unicode)
        if content.get('learning_points'):
            description += "Key Points:\n"
            for point in content['learning_points'][:5]:
                clean_point = sanitize_unicode(point)
                description += f"• {clean_point}\n"
        
        # Create the topic
        topic = Topic.create(
            title=title,
            description=description,
            user_id=user.id,
            is_gcse=True
        )
        
        if topic:
            # Save the full content as a note
            from app.models.content_management import TopicNote
            
            # Convert to JSON with ensure_ascii=False to handle Unicode characters
            note_content = json.dumps(content, indent=2, ensure_ascii=False)
            note = TopicNote.create_note(
                topic_id=topic.id,
                user_id=user.id,
                title=f"AI-Generated Content",
                content=note_content,
                note_type='ai_generated'
            )
            
            return jsonify({
                'success': True,
                'topic_id': topic.id,
                'message': 'Content saved to topics successfully!'
            })
        else:
            return jsonify({'error': 'Failed to create topic'}), 500
    
    except Exception as e:
        # Use safe printing to avoid Unicode errors
        error_msg = str(e).encode('ascii', 'replace').decode('ascii')
        print(f"Error saving GCSE content to topics: {error_msg}")
        try:
            import traceback
            traceback.print_exc()
        except:
            pass  # Skip traceback if it has Unicode issues
        return jsonify({'error': f'Failed to save content: {error_msg}'}), 500

@gcse_ai.route('/api/export-content', methods=['POST'])
@login_required
def export_gcse_content():
    """Export GCSE personalized content as formatted document"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        subject = data.get('subject', 'GCSE Subject')
        topic = data.get('topic', 'Topic')
        content_data = data.get('content', {})
        learning_style = data.get('learning_style', 'general')
        difficulty = data.get('difficulty', 'intermediate')
        
        # Build HTML export
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{subject} - {topic}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #17a2b8 0%, #138496 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; }}
        .section {{ margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        .section h2 {{ color: #17a2b8; margin-top: 0; }}
        ul {{ line-height: 1.8; }}
        .question-box {{ background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #0d6efd; border-radius: 6px; }}
        .example-box {{ background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #28a745; border-radius: 6px; }}
        code {{ background: #f8f9fa; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{subject} - {topic}</h1>
        <p>Learning Style: {learning_style.title()} | Difficulty: {difficulty.title()}</p>
    </div>
"""
        
        # Learning points
        if content_data.get('learning_points'):
            html_content += """
    <div class="section">
        <h2>📖 Learning Content</h2>
        <ul>
"""
            for point in content_data['learning_points']:
                html_content += f"            <li>{point}</li>\n"
            html_content += "        </ul>\n    </div>\n"
        
        # Practice questions
        if content_data.get('practice_questions'):
            html_content += """
    <div class="section">
        <h2>❓ Practice Questions</h2>
"""
            for idx, q in enumerate(content_data['practice_questions'][:3], 1):
                question_text = q if isinstance(q, str) else q.get('question', q)
                html_content += f"""        <div class="question-box">
            <strong>Question {idx}:</strong><br>
            {question_text}
        </div>
"""
            html_content += "    </div>\n"
        
        # Examples
        if content_data.get('examples'):
            html_content += """
    <div class="section">
        <h2>🧪 Worked Examples</h2>
"""
            for idx, ex in enumerate(content_data['examples'][:2], 1):
                example_text = ex if isinstance(ex, str) else ex.get('description', ex)
                html_content += f"""        <div class="example-box">
            <strong>Example {idx}:</strong><br>
            <pre style="white-space: pre-wrap; font-family: monospace; margin: 10px 0;">{example_text}</pre>
        </div>
"""
            html_content += "    </div>\n"
        
        # Study recommendations
        if content_data.get('study_recommendations'):
            html_content += """
    <div class="section">
        <h2>💡 Study Recommendations</h2>
        <ul>
"""
            for rec in content_data['study_recommendations'][:5]:
                html_content += f"            <li>{rec}</li>\n"
            html_content += "        </ul>\n    </div>\n"
        
        html_content += f"""
    <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 2px solid #dee2e6; color: #6c757d;">
        <p>Generated by Learning Companion on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        <p><small>To save as PDF: Print this page and select "Save as PDF"</small></p>
    </div>
</body>
</html>
"""
        
        return jsonify({
            'success': True,
            'html': html_content,
            'filename': f"{subject}_{topic.replace(' ', '_')}.html"
        })
    
    except Exception as e:
        print(f"Error exporting GCSE content: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to export content: {str(e)}'}), 500

@gcse_ai.route('/api/subjects')
@login_required
def get_gcse_subjects():
    """Get available GCSE subjects"""
    try:
        subjects = [
            {'name': 'Mathematics', 'code': 'maths', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'English Language', 'code': 'english_lang', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'English Literature', 'code': 'english_lit', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Biology', 'code': 'biology', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Chemistry', 'code': 'chemistry', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Physics', 'code': 'physics', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'History', 'code': 'history', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Geography', 'code': 'geography', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'French', 'code': 'french', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Spanish', 'code': 'spanish', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'German', 'code': 'german', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Computer Science', 'code': 'computer_science', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Business Studies', 'code': 'business', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Economics', 'code': 'economics', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Psychology', 'code': 'psychology', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Sociology', 'code': 'sociology', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Art & Design', 'code': 'art', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Music', 'code': 'music', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Drama', 'code': 'drama', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']},
            {'name': 'Physical Education', 'code': 'pe', 'exam_boards': ['AQA', 'Edexcel', 'OCR', 'WJEC']}
        ]
        
        return jsonify({'subjects': subjects})
    
    except Exception as e:
        print(f"Error getting GCSE subjects: {e}")
        return jsonify({'error': 'Failed to get GCSE subjects'}), 500

@gcse_ai.route('/api/grade-boundaries/<subject>/<exam_board>')
@login_required
def get_gcse_grade_boundaries(subject, exam_board):
    """Get GCSE grade boundaries for a subject and exam board"""
    try:
        # This would typically fetch from a database or external API
        # For now, return sample data
        grade_boundaries = {
            'subject': subject,
            'exam_board': exam_board,
            'boundaries': {
                '2023': {'9': 85, '8': 75, '7': 65, '6': 55, '5': 45, '4': 35, '3': 25, '2': 15, '1': 5},
                '2022': {'9': 83, '8': 73, '7': 63, '6': 53, '5': 43, '4': 33, '3': 23, '2': 13, '1': 3},
                '2021': {'9': 87, '8': 77, '7': 67, '6': 57, '5': 47, '4': 37, '3': 27, '2': 17, '1': 7}
            },
            'trends': {
                'increasing_grades': ['9', '8'],
                'stable_grades': ['7', '6', '5'],
                'decreasing_grades': ['4', '3', '2', '1']
            }
        }
        
        return jsonify(grade_boundaries)
    
    except Exception as e:
        print(f"Error getting GCSE grade boundaries: {e}")
        return jsonify({'error': 'Failed to get grade boundaries'}), 500

@gcse_ai.route('/comprehensive-analysis')
@login_required
def comprehensive_gcse_analysis():
    """Comprehensive GCSE analysis page"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        return render_template('gcse_ai/comprehensive_analysis.html', user=user)
    
    except Exception as e:
        print(f"Error loading comprehensive GCSE analysis: {e}")
        return jsonify({'error': 'Failed to load comprehensive analysis'}), 500

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import get_supabase_client
from app.routes.topics import get_current_user
import openai
import os
import json
from datetime import datetime

ai_chat = Blueprint('ai_chat', __name__)

# Initialize OpenAI client with error handling
def get_openai_client():
    """Get OpenAI client, loading environment variables if needed"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("WARNING: OPENAI_API_KEY not set. AI Chat features will be disabled.")
        return None
    
    try:
        return openai.OpenAI(api_key=api_key)
    except Exception as e:
        print(f"WARNING: Failed to initialize OpenAI client: {e}")
        return None

# Initialize client
client = get_openai_client()

@ai_chat.route('/ai/chat')
@login_required
def chat_interface():
    """AI Chat interface"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        return render_template('ai/chat.html')
    except Exception as e:
        flash('Error loading AI chat interface.', 'error')
        return redirect(url_for('main.dashboard'))

@ai_chat.route('/api/ai/chat', methods=['POST'])
@login_required
def ai_chat_api():
    """API endpoint for AI chat"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        message = data.get('message', '').strip()
        topic_id = data.get('topic_id')
        context = data.get('context', '')
        settings = data.get('settings', {})
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get topic context if provided
        topic_context = ''
        if topic_id:
            topic_context = get_topic_context(topic_id, user.id)
        
        # Build the prompt
        prompt = build_prompt(message, topic_context, context, settings)
        
        # Call OpenAI API
        response = call_openai_api(prompt, settings)
        
        # Save conversation to database
        save_conversation(user.id, message, response, topic_id)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"AI Chat API Error: {e}")
        return jsonify({'error': 'Failed to process request'}), 500

@ai_chat.route('/api/ai/summarize', methods=['POST'])
@login_required
def ai_summarize():
    """API endpoint for AI summarization"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        content = data.get('content', '').strip()
        topic_id = data.get('topic_id')
        summary_type = data.get('type', 'general')  # general, key_points, detailed
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Get topic context if provided
        topic_context = ''
        if topic_id:
            topic_context = get_topic_context(topic_id, user.id)
        
        # Build summarization prompt
        prompt = build_summarization_prompt(content, topic_context, summary_type)
        
        # Call OpenAI API
        response = call_openai_api(prompt, {'response_style': 'concise'})
        
        return jsonify({
            'summary': response,
            'type': summary_type,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"AI Summarize Error: {e}")
        return jsonify({'error': 'Failed to generate summary'}), 500

@ai_chat.route('/api/ai/explain', methods=['POST'])
@login_required
def ai_explain():
    """API endpoint for AI explanation"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        concept = data.get('concept', '').strip()
        topic_id = data.get('topic_id')
        explanation_level = data.get('level', 'beginner')  # beginner, intermediate, advanced
        
        if not concept:
            return jsonify({'error': 'Concept is required'}), 400
        
        # Get topic context if provided
        topic_context = ''
        if topic_id:
            topic_context = get_topic_context(topic_id, user.id)
        
        # Build explanation prompt
        prompt = build_explanation_prompt(concept, topic_context, explanation_level)
        
        # Call OpenAI API
        response = call_openai_api(prompt, {'response_style': explanation_level})
        
        return jsonify({
            'explanation': response,
            'level': explanation_level,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"AI Explain Error: {e}")
        return jsonify({'error': 'Failed to generate explanation'}), 500

@ai_chat.route('/api/ai/questions', methods=['POST'])
@login_required
def ai_generate_questions():
    """API endpoint for generating practice questions"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        topic_id = data.get('topic_id')
        question_type = data.get('type', 'multiple_choice')  # multiple_choice, short_answer, essay
        difficulty = data.get('difficulty', 'medium')  # easy, medium, hard
        count = data.get('count', 5)
        
        if not topic_id:
            return jsonify({'error': 'Topic ID is required'}), 400
        
        # Get topic context
        topic_context = get_topic_context(topic_id, user.id)
        
        # Build questions prompt
        prompt = build_questions_prompt(topic_context, question_type, difficulty, count)
        
        # Call OpenAI API
        response = call_openai_api(prompt, {'response_style': 'detailed'})
        
        return jsonify({
            'questions': response,
            'type': question_type,
            'difficulty': difficulty,
            'count': count,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"AI Questions Error: {e}")
        return jsonify({'error': 'Failed to generate questions'}), 500

def get_topic_context(topic_id, user_id):
    """Get topic context for AI"""
    try:
        client = get_supabase_client()
        
        # Get topic details
        topic_res = client.table('topics').select('*').eq('id', topic_id).eq('user_id', user_id).execute()
        if not topic_res.data:
            return ''
        
        topic = topic_res.data[0]
        
        # Get topic notes
        notes_res = client.table('topic_notes').select('*').eq('topic_id', topic_id).execute()
        notes = notes_res.data if notes_res.data else []
        
        # Get topic attachments (file names)
        attachments_res = client.table('topic_attachments').select('*').eq('topic_id', topic_id).execute()
        attachments = attachments_res.data if attachments_res.data else []
        
        # Build context
        context = f"Topic: {topic['title']}\n"
        context += f"Description: {topic.get('description', '')}\n"
        
        if topic.get('notes'):
            context += f"Notes: {topic['notes']}\n"
        
        if notes:
            context += "Additional Notes:\n"
            for note in notes:
                context += f"- {note['note_content']}\n"
        
        if attachments:
            context += "Attachments:\n"
            for attachment in attachments:
                context += f"- {attachment['file_name']}\n"
        
        return context
        
    except Exception as e:
        print(f"Error getting topic context: {e}")
        return ''

def build_prompt(message, topic_context, conversation_context, settings):
    """Build the main chat prompt"""
    response_style = settings.get('response_style', 'concise')
    context_length = settings.get('context_length', 'medium')
    
    # Adjust prompt based on settings
    if response_style == 'concise':
        style_instruction = "Keep your response brief and to the point (2-3 sentences max)."
    elif response_style == 'detailed':
        style_instruction = "Provide a comprehensive response with examples."
    elif response_style == 'beginner':
        style_instruction = "Explain in simple terms suitable for beginners."
    else:  # advanced
        style_instruction = "Provide an advanced, technical explanation."
    
    if context_length == 'short':
        length_instruction = "Keep it very brief (1-2 sentences)."
    elif context_length == 'medium':
        length_instruction = "Provide a medium-length response (2-3 paragraphs)."
    else:  # long
        length_instruction = "Provide a detailed, comprehensive response."
    
    prompt = f"""You are an AI Study Assistant. {style_instruction} {length_instruction}

Context: {topic_context if topic_context else 'No specific topic context'}

User question: {message}

Respond directly and helpfully. Be educational but concise."""
    return prompt

def build_summarization_prompt(content, topic_context, summary_type):
    """Build summarization prompt"""
    prompt = f"""You are an AI Study Assistant. Please summarize the following content for a student:

Topic Context:
{topic_context}

Content to summarize:
{content}

Summary type: {summary_type}

Please provide a clear, concise summary that:
1. Captures the main points
2. Is appropriate for the topic context
3. Uses bullet points or numbered lists when helpful
4. Highlights key concepts and takeaways
"""
    return prompt

def build_explanation_prompt(concept, topic_context, level):
    """Build explanation prompt"""
    prompt = f"""You are an AI Study Assistant. Please explain the following concept:

Topic Context:
{topic_context}

Concept to explain: {concept}

Explanation level: {level}

Please provide an explanation that:
1. Is appropriate for the {level} level
2. Uses clear, simple language
3. Includes relevant examples
4. Connects to the broader topic context
5. Encourages understanding and retention
"""
    return prompt

def build_questions_prompt(topic_context, question_type, difficulty, count):
    """Build questions generation prompt"""
    prompt = f"""You are an AI Study Assistant. Please generate {count} practice questions for the following topic:

Topic Context:
{topic_context}

Question type: {question_type}
Difficulty: {difficulty}

Please generate questions that:
1. Test understanding of key concepts
2. Are appropriate for the {difficulty} level
3. Match the {question_type} format
4. Cover different aspects of the topic
5. Include answers/explanations when appropriate
"""
    return prompt

def call_openai_api(prompt, settings):
    """Call OpenAI API"""
    try:
        # Get fresh client instance
        current_client = get_openai_client()
        if current_client is None:
            return "AI Chat is currently unavailable. Please set up your OpenAI API key to use this feature."
        
        # Set shorter timeout and more concise parameters
        response = current_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI Study Assistant. Be concise and direct."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,  # Reduced for more concise responses
            temperature=0.7,
            timeout=30  # 30 second timeout
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "I'm sorry, I'm having trouble processing your request right now. Please try again later."

def save_conversation(user_id, user_message, ai_response, topic_id):
    """Save conversation to database"""
    try:
        client = get_supabase_client()
        
        # Save conversation
        conversation_data = {
            'user_id': user_id,
            'user_message': user_message,
            'ai_response': ai_response,
            'topic_id': topic_id,
            'created_at': datetime.now().isoformat()
        }
        
        client.table('ai_conversations').insert(conversation_data).execute()
        
    except Exception as e:
        print(f"Error saving conversation: {e}")

@ai_chat.route('/ai/conversations')
@login_required
def conversations_history():
    """View conversation history"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        # Get conversations from database
        client = get_supabase_client()
        conversations_res = client.table('ai_conversations').select('*').eq('user_id', user.id).order('created_at', desc=True).execute()
        conversations = conversations_res.data if conversations_res.data else []
        
        return render_template('ai/conversations.html', conversations=conversations)
        
    except Exception as e:
        flash('Error loading conversation history.', 'error')
        return redirect(url_for('main.dashboard'))

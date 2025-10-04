from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import get_supabase_client
from app.routes.topics import get_current_user
import openai
import os
import json
from datetime import datetime

ai_chat = Blueprint('ai_chat', __name__)


def get_openai_client():
    
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


client = get_openai_client()

@ai_chat.route('/ai/chat')
@login_required
def chat_interface():
    
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
        
        
        topic_context = ''
        if topic_id:
            topic_context = get_topic_context(topic_id, user.id)
        
        
        prompt = build_prompt(message, topic_context, context, settings)
        
        
        response = call_openai_api(prompt, settings)
        
        
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
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        content = data.get('content', '').strip()
        topic_id = data.get('topic_id')
        summary_type = data.get('type', 'general')  
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        
        topic_context = ''
        if topic_id:
            topic_context = get_topic_context(topic_id, user.id)
        
        
        prompt = build_summarization_prompt(content, topic_context, summary_type)
        
        
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
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        concept = data.get('concept', '').strip()
        topic_id = data.get('topic_id')
        explanation_level = data.get('level', 'beginner')  
        
        if not concept:
            return jsonify({'error': 'Concept is required'}), 400
        
        
        topic_context = ''
        if topic_id:
            topic_context = get_topic_context(topic_id, user.id)
        
        
        prompt = build_explanation_prompt(concept, topic_context, explanation_level)
        
        
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
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        topic_id = data.get('topic_id')
        question_type = data.get('type', 'multiple_choice')  
        difficulty = data.get('difficulty', 'medium')  
        count = data.get('count', 5)
        
        if not topic_id:
            return jsonify({'error': 'Topic ID is required'}), 400
        
        
        topic_context = get_topic_context(topic_id, user.id)
        
        
        prompt = build_questions_prompt(topic_context, question_type, difficulty, count)
        
        
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
    
    try:
        client = get_supabase_client()
        
        
        topic_res = client.table('topics').select('*').eq('id', topic_id).eq('user_id', user_id).execute()
        if not topic_res.data:
            return ''
        
        topic = topic_res.data[0]
        
        
        notes_res = client.table('topic_notes').select('*').eq('topic_id', topic_id).execute()
        notes = notes_res.data if notes_res.data else []
        
        
        attachments_res = client.table('topic_attachments').select('*').eq('topic_id', topic_id).execute()
        attachments = attachments_res.data if attachments_res.data else []
        
        
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
    
    response_style = settings.get('response_style', 'concise')
    context_length = settings.get('context_length', 'medium')
    
    
    if response_style == 'concise':
        style_instruction = "Keep your response brief and to the point (2-3 sentences max)."
    elif response_style == 'detailed':
        style_instruction = "Provide a comprehensive response with examples."
    elif response_style == 'beginner':
        style_instruction = "Explain in simple terms suitable for beginners."
    else:  
        style_instruction = "Provide an advanced, technical explanation."
    
    if context_length == 'short':
        length_instruction = "Keep it very brief (1-2 sentences)."
    elif context_length == 'medium':
        length_instruction = "Provide a medium-length response (2-3 paragraphs)."
    else:  
        length_instruction = "Provide a detailed, comprehensive response."
    
    prompt = f
    return prompt

def build_summarization_prompt(content, topic_context, summary_type):
    
    prompt = f
    return prompt

def build_explanation_prompt(concept, topic_context, level):
    
    prompt = f
    return prompt

def build_questions_prompt(topic_context, question_type, difficulty, count):
    
    prompt = f
    return prompt

def call_openai_api(prompt, settings):
    
    try:
        
        current_client = get_openai_client()
        if current_client is None:
            return "AI Chat is currently unavailable. Please set up your OpenAI API key to use this feature."
        
        
        response = current_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI Study Assistant. Be concise and direct."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,  
            temperature=0.7,
            timeout=30  
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "I'm sorry, I'm having trouble processing your request right now. Please try again later."

def save_conversation(user_id, user_message, ai_response, topic_id):
    
    try:
        client = get_supabase_client()
        
        
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
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        client = get_supabase_client()
        conversations_res = client.table('ai_conversations').select('*').eq('user_id', user.id).order('created_at', desc=True).execute()
        conversations = conversations_res.data if conversations_res.data else []
        
        return render_template('ai/conversations.html', conversations=conversations)
        
    except Exception as e:
        flash('Error loading conversation history.', 'error')
        return redirect(url_for('main.dashboard'))


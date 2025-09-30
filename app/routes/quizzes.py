"""
Quiz and Assessment Routes
Handles quiz creation, taking quizzes, and results
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required
from datetime import datetime, timedelta
from app.models import Topic
from app.models.quiz import Quiz, QuizQuestion, QuizQuestionOption, QuizAttempt, QuizAttemptAnswer, FlashcardProgress
from app.models import get_supabase_client, SUPABASE_AVAILABLE
from app.routes.topics import get_current_user
from app.forms.quiz_forms import (
    CreateQuizForm, CreateQuestionForm, MultipleChoiceOptionForm, 
    TakeQuizForm, FlashcardReviewForm, QuizSearchForm, QuizSettingsForm
)
from app.utils.question_generator import SmartQuestionGenerator
from app.models.gamification import GamificationEngine
import json

quizzes = Blueprint('quizzes', __name__, url_prefix='/quizzes')


@quizzes.route('/')
@login_required
def quiz_list():
    """Display list of all quizzes"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get all topics for the user
    topics = Topic.get_topics_by_user(user.id)
    
    # Get all quizzes for each topic
    all_quizzes = []
    for topic in topics:
        topic_quizzes = Quiz.get_quizzes_by_topic(topic.id, user.id)
        for quiz in topic_quizzes:
            quiz.topic_title = topic.title
            all_quizzes.append(quiz)
    
    # Sort by creation date
    all_quizzes.sort(key=lambda x: x.created_at, reverse=True)
    
    return render_template('quizzes/list.html', quizzes=all_quizzes, topics=topics)


@quizzes.route('/topic/<topic_id>')
@login_required
def topic_quizzes(topic_id):
    """Display quizzes for a specific topic"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get topic
    topic = Topic.get_topic_by_id(topic_id, user.id)
    if not topic:
        flash('Topic not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    # Get quizzes for this topic
    quizzes_list = Quiz.get_quizzes_by_topic(topic_id, user.id)
    
    return render_template('quizzes/topic_quizzes.html', topic=topic, quizzes=quizzes_list)


@quizzes.route('/create/<topic_id>', methods=['GET', 'POST'])
def create_quiz(topic_id):
    """Create a new quiz for a topic"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get topic
    topic = Topic.get_topic_by_id(topic_id, user.id)
    if not topic:
        flash('Topic not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    form = CreateQuizForm()
    
    if form.validate_on_submit():
        quiz = Quiz.create_quiz(
            topic_id=topic_id,
            user_id=user.id,
            title=form.title.data,
            description=form.description.data,
            quiz_type=form.quiz_type.data,
            difficulty_level=form.difficulty_level.data,
            time_limit_minutes=form.time_limit_minutes.data,
            passing_score=form.passing_score.data
        )
        
        if quiz:
            flash('Quiz created successfully!', 'success')
            return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz.id))
        else:
            flash('Error creating quiz', 'error')
    
    return render_template('quizzes/create.html', form=form, topic=topic)


@quizzes.route('/<quiz_id>')
def quiz_detail(quiz_id):
    """Display quiz details and questions"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get quiz
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    # Get topic
    topic = Topic.get_topic_by_id(quiz.topic_id, user.id)
    
    # Get questions
    questions = QuizQuestion.get_questions_by_quiz(quiz_id)
    
    return render_template('quizzes/detail.html', quiz=quiz, topic=topic, questions=questions)


@quizzes.route('/<quiz_id>/add-question', methods=['GET', 'POST'])
def add_question(quiz_id):
    """Add a question to a quiz"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get quiz
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    form = CreateQuestionForm()
    
    if form.validate_on_submit():
        # Get next order index
        existing_questions = QuizQuestion.get_questions_by_quiz(quiz_id)
        next_order = len(existing_questions)
        
        question = QuizQuestion.create_question(
            quiz_id=quiz_id,
            question_text=form.question_text.data,
            question_type=form.question_type.data,
            correct_answer=form.correct_answer.data,
            explanation=form.explanation.data,
            points=form.points.data,
            order_index=next_order
        )
        
        if question:
            flash('Question added successfully!', 'success')
            
            # If it's a multiple choice question, redirect to add options
            if form.question_type.data == 'multiple_choice':
                return redirect(url_for('quizzes.add_options', question_id=question.id))
            else:
                return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
        else:
            flash('Error adding question', 'error')
    
    return render_template('quizzes/add_question.html', form=form, quiz=quiz)


@quizzes.route('/question/<question_id>/add-options', methods=['GET', 'POST'])
def add_options(question_id):
    """Add options to a multiple choice question"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get question and verify ownership
    if not SUPABASE_AVAILABLE:
        flash('Database not available', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    supabase = get_supabase_client()
    
    try:
        result = supabase.table('quiz_questions').select('*, quizzes!inner(*)').eq('id', question_id).eq('quizzes.user_id', user.id).execute()
        if not result.data:
            flash('Question not found', 'error')
            return redirect(url_for('quizzes.quiz_list'))
        
        question_data = result.data[0]
        quiz_data = question_data['quizzes']
        
        # Get existing options
        options = QuizQuestionOption.get_options_by_question(question_id)
        
        form = MultipleChoiceOptionForm()
        
        if form.validate_on_submit():
            # Get next order index
            next_order = len(options)
            
            option = QuizQuestionOption()
            if option.add_option(question_id, form.option_text.data, form.is_correct.data, next_order):
                flash('Option added successfully!', 'success')
                return redirect(url_for('quizzes.add_options', question_id=question_id))
            else:
                flash('Error adding option', 'error')
        
        return render_template('quizzes/add_options.html', form=form, question=question_data, quiz=quiz_data, options=options)
        
    except Exception as e:
        print(f"Error in add_options: {e}")
        flash('Error loading question', 'error')
        return redirect(url_for('quizzes.quiz_list'))


@quizzes.route('/<quiz_id>/take', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    """Take a quiz"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get quiz
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    # Get questions
    questions = QuizQuestion.get_questions_by_quiz(quiz_id)
    if not questions:
        flash('No questions found in this quiz', 'error')
        return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
    
    # Check if there's an active attempt
    attempt_id = session.get(f'quiz_attempt_{quiz_id}')
    attempt = None
    
    if attempt_id:
        attempt = QuizAttempt.get_attempt_by_id(attempt_id, user.id)
        if not attempt or attempt.status != 'in_progress':
            attempt = None
            session.pop(f'quiz_attempt_{quiz_id}', None)
    
    # Start new attempt if none exists
    if not attempt:
        attempt = QuizAttempt.start_attempt(quiz_id, user.id)
        if attempt:
            session[f'quiz_attempt_{quiz_id}'] = attempt.id
        else:
            flash('Error starting quiz attempt', 'error')
            return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
    
    # Get current question index
    current_question_index = int(request.args.get('q', 0))
    
    if current_question_index >= len(questions):
        # Quiz completed
        attempt.complete_attempt()
        
        # Process gamification rewards
        if attempt.score is not None:
            time_taken_minutes = attempt.time_taken_minutes or 0
            rewards = GamificationEngine.process_quiz_completion(user.id, attempt.score, time_taken_minutes)
            
            # Store rewards in session for display in results
            session[f'quiz_rewards_{attempt.id}'] = rewards
        
        session.pop(f'quiz_attempt_{quiz_id}', None)
        return redirect(url_for('quizzes.quiz_results', attempt_id=attempt.id))
    
    current_question = questions[current_question_index]
    form = TakeQuizForm()
    
    if form.validate_on_submit():
        # Submit answer
        attempt.submit_answer(current_question.id, form.answer.data)
        
        # Move to next question
        next_index = current_question_index + 1
        if next_index < len(questions):
            return redirect(url_for('quizzes.take_quiz', quiz_id=quiz_id, q=next_index))
        else:
            # Quiz completed
            attempt.complete_attempt()
            
            # Process gamification rewards
            if attempt.score is not None:
                time_taken_minutes = attempt.time_taken_minutes or 0
                rewards = GamificationEngine.process_quiz_completion(user.id, attempt.score, time_taken_minutes)
                
                # Store rewards in session for display in results
                session[f'quiz_rewards_{attempt.id}'] = rewards
            
            session.pop(f'quiz_attempt_{quiz_id}', None)
            return redirect(url_for('quizzes.quiz_results', attempt_id=attempt.id))
    
    # Calculate progress
    progress = int((current_question_index / len(questions)) * 100)
    
    return render_template('quizzes/take.html', 
                         quiz=quiz, 
                         question=current_question, 
                         question_index=current_question_index,
                         total_questions=len(questions),
                         progress=progress,
                         form=form,
                         attempt=attempt)


@quizzes.route('/results/<attempt_id>')
def quiz_results(attempt_id):
    """Display quiz results"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get attempt
    attempt = QuizAttempt.get_attempt_by_id(attempt_id, user.id)
    if not attempt:
        flash('Quiz attempt not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    # Get quiz
    quiz = Quiz.get_quiz_by_id(attempt.quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    # Get topic
    topic = Topic.get_topic_by_id(quiz.topic_id, user.id)
    
    # Get questions and answers
    questions = QuizQuestion.get_questions_by_quiz(quiz.id)
    
    # Create question-answer mapping
    qa_mapping = {}
    for answer in attempt.answers:
        qa_mapping[answer.question_id] = answer
    
    # Determine if passed
    passed = attempt.score >= quiz.passing_score
    
    # Get gamification rewards
    rewards = session.get(f'quiz_rewards_{attempt_id}', {})
    
    return render_template('quizzes/results.html', 
                         attempt=attempt, 
                         quiz=quiz, 
                         topic=topic,
                         questions=questions,
                         qa_mapping=qa_mapping,
                         passed=passed,
                         rewards=rewards)


@quizzes.route('/flashcards/<quiz_id>')
def flashcards(quiz_id):
    """Study flashcards"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get quiz
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    # Get questions (flashcards)
    questions = QuizQuestion.get_questions_by_quiz(quiz_id)
    if not questions:
        flash('No flashcards found in this quiz', 'error')
        return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
    
    # Get current card index
    current_index = int(request.args.get('card', 0))
    
    if current_index >= len(questions):
        flash('All flashcards completed!', 'success')
        return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
    
    current_question = questions[current_index]
    form = FlashcardReviewForm()
    
    return render_template('quizzes/flashcards.html', 
                         quiz=quiz, 
                         question=current_question, 
                         card_index=current_index,
                         total_cards=len(questions),
                         form=form)


@quizzes.route('/flashcards/<quiz_id>/review', methods=['POST'])
def review_flashcard(quiz_id):
    """Review a flashcard and update progress"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    form = FlashcardReviewForm()
    
    if form.validate_on_submit():
        question_id = request.form.get('question_id')
        quality = form.quality.data
        
        # Update flashcard progress
        FlashcardProgress.create_or_update_progress(user.id, question_id, quality)
        
        # Get current card index
        current_index = int(request.form.get('card_index', 0))
        next_index = current_index + 1
        
        # Check if there are more cards
        questions = QuizQuestion.get_questions_by_quiz(quiz_id)
        if next_index < len(questions):
            return redirect(url_for('quizzes.flashcards', quiz_id=quiz_id, card=next_index))
        else:
            flash('All flashcards completed! Great job!', 'success')
            return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
    
    return redirect(url_for('quizzes.flashcards', quiz_id=quiz_id))


@quizzes.route('/api/due-flashcards')
def api_due_flashcards():
    """API endpoint to get due flashcards"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get due flashcards
    due_flashcards = FlashcardProgress.get_due_flashcards(user.id, limit=10)
    
    # Get question details for each flashcard
    flashcards_data = []
    for progress in due_flashcards:
        if not SUPABASE_AVAILABLE:
            continue
            
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('quiz_questions').select('*, quizzes!inner(title, topic_id)').eq('id', progress.question_id).execute()
            if result.data:
                question_data = result.data[0]
                quiz_data = question_data['quizzes']
                
                flashcards_data.append({
                    'id': progress.id,
                    'question_id': progress.question_id,
                    'question_text': question_data['question_text'],
                    'correct_answer': question_data['correct_answer'],
                    'explanation': question_data['explanation'],
                    'quiz_title': quiz_data['title'],
                    'topic_id': quiz_data['topic_id'],
                    'ease_factor': progress.ease_factor,
                    'interval_days': progress.interval_days,
                    'repetitions': progress.repetitions,
                    'next_review_date': progress.next_review_date
                })
        except Exception as e:
            print(f"Error getting flashcard data: {e}")
            continue
    
    return jsonify({'flashcards': flashcards_data})


@quizzes.route('/api/quiz-stats')
def api_quiz_stats():
    """API endpoint to get quiz statistics"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not SUPABASE_AVAILABLE:
        return jsonify({'error': 'Database not available'}), 500
    
    supabase = get_supabase_client()
    
    try:
        # Get total quizzes
        quizzes_result = supabase.table('quizzes').select('id').eq('user_id', user.id).eq('is_active', True).execute()
        total_quizzes = len(quizzes_result.data)
        
        # Get total attempts
        attempts_result = supabase.table('quiz_attempts').select('id, score, status').eq('user_id', user.id).execute()
        total_attempts = len(attempts_result.data)
        
        # Get completed attempts
        completed_attempts = [a for a in attempts_result.data if a['status'] == 'completed']
        completed_count = len(completed_attempts)
        
        # Calculate average score
        if completed_attempts:
            avg_score = sum(a['score'] for a in completed_attempts) / len(completed_attempts)
        else:
            avg_score = 0
        
        # Get due flashcards count
        due_flashcards = FlashcardProgress.get_due_flashcards(user.id, limit=100)
        due_count = len(due_flashcards)
        
        return jsonify({
            'total_quizzes': total_quizzes,
            'total_attempts': total_attempts,
            'completed_attempts': completed_count,
            'average_score': round(avg_score, 1),
            'due_flashcards': due_count
        })
        
    except Exception as e:
        print(f"Error getting quiz stats: {e}")
        return jsonify({'error': 'Error getting statistics'}), 500


@quizzes.route('/api/generate-questions/<topic_id>')
def api_generate_questions(topic_id):
    """API endpoint to generate smart questions for a topic"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get topic
    topic = Topic.get_topic_by_id(topic_id, user.id)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    # Get parameters
    num_questions = int(request.args.get('num_questions', 5))
    difficulty = request.args.get('difficulty', 'medium')
    question_type = request.args.get('type', 'mixed')  # mixed, multiple_choice, true_false, fill_blank, flashcards
    
    try:
        if question_type == 'flashcards':
            # Generate flashcards
            generated_questions = SmartQuestionGenerator.generate_flashcards_from_topic(
                topic.title, topic.description, num_questions
            )
        else:
            # Generate regular questions
            generated_questions = SmartQuestionGenerator.generate_questions_from_topic(
                topic.title, topic.description, num_questions, difficulty
            )
        
        return jsonify({
            'success': True,
            'topic_id': topic_id,
            'topic_title': topic.title,
            'questions': generated_questions,
            'count': len(generated_questions)
        })
        
    except Exception as e:
        print(f"Error generating questions: {e}")
        return jsonify({'error': 'Error generating questions'}), 500


@quizzes.route('/api/add-generated-questions', methods=['POST'])
def api_add_generated_questions():
    """API endpoint to add generated questions to a quiz"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        data = request.get_json()
        quiz_id = data.get('quiz_id')
        selected_questions = data.get('selected_questions', [])
        
        if not quiz_id or not selected_questions:
            return jsonify({'error': 'Missing required data'}), 400
        
        # Verify quiz ownership
        quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        added_questions = []
        
        for question_data in selected_questions:
            # Get next order index
            existing_questions = QuizQuestion.get_questions_by_quiz(quiz_id)
            next_order = len(existing_questions)
            
            # Create the question
            question = QuizQuestion.create_question(
                quiz_id=quiz_id,
                question_text=question_data['question_text'],
                question_type=question_data['question_type'],
                correct_answer=question_data['correct_answer'],
                explanation=question_data.get('explanation', ''),
                points=question_data.get('points', 1),
                order_index=next_order
            )
            
            if question:
                # Add options for multiple choice questions
                if question_data['question_type'] == 'multiple_choice' and 'options' in question_data:
                    for option_data in question_data['options']:
                        question.add_option(
                            option_data['text'],
                            option_data['is_correct'],
                            len(question.options)
                        )
                
                added_questions.append({
                    'id': question.id,
                    'question_text': question.question_text,
                    'question_type': question.question_type
                })
        
        return jsonify({
            'success': True,
            'added_questions': added_questions,
            'count': len(added_questions)
        })
        
    except Exception as e:
        print(f"Error adding generated questions: {e}")
        return jsonify({'error': 'Error adding questions'}), 500


@quizzes.route('/<quiz_id>/generate-questions')
def generate_questions_page(quiz_id):
    """Page for generating and selecting smart questions"""
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    # Get quiz
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    # Get topic
    topic = Topic.get_topic_by_id(quiz.topic_id, user.id)
    
    return render_template('quizzes/generate_questions.html', quiz=quiz, topic=topic)

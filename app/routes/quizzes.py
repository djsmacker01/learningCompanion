

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import json
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
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    
    topics = Topic.get_topics_by_user(user.id)
    
    
    all_quizzes = []
    for topic in topics:
        topic_quizzes = Quiz.get_quizzes_by_topic(topic.id, user.id)
        for quiz in topic_quizzes:
            quiz.topic_title = topic.title
            all_quizzes.append(quiz)
    
    
    all_quizzes.sort(key=lambda x: x.created_at, reverse=True)
    
    return render_template('quizzes/list.html', quizzes=all_quizzes, topics=topics)


@quizzes.route('/topic/<topic_id>')
@login_required
def topic_quizzes(topic_id):
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    
    topic = Topic.get_topic_by_id(topic_id, user.id)
    if not topic:
        flash('Topic not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    
    quizzes_list = Quiz.get_quizzes_by_topic(topic_id, user.id)
    
    return render_template('quizzes/topic_quizzes.html', topic=topic, quizzes=quizzes_list)


@quizzes.route('/create/<topic_id>', methods=['GET', 'POST'])
def create_quiz(topic_id):
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    
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
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    
    topic = Topic.get_topic_by_id(quiz.topic_id, user.id)
    
    
    questions = QuizQuestion.get_questions_by_quiz(quiz_id)
    
    return render_template('quizzes/detail.html', quiz=quiz, topic=topic, questions=questions)


@quizzes.route('/<quiz_id>/add-question', methods=['GET', 'POST'])
def add_question(quiz_id):
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    form = CreateQuestionForm()
    
    if form.validate_on_submit():
        
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
            
            
            if form.question_type.data == 'multiple_choice':
                return redirect(url_for('quizzes.add_options', question_id=question.id))
            else:
                return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
        else:
            flash('Error adding question', 'error')
    
    return render_template('quizzes/add_question.html', form=form, quiz=quiz)


@quizzes.route('/question/<question_id>/add-options', methods=['GET', 'POST'])
def add_options(question_id):
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    
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
        
        
        options = QuizQuestionOption.get_options_by_question(question_id)
        
        form = MultipleChoiceOptionForm()
        
        if form.validate_on_submit():
            
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
    print("*** QUIZ ROUTE CALLED ***")
    print(f"Method: {request.method}")
    print(f"Quiz ID: {quiz_id}")
    print(f"Request data: {dict(request.form)}")
    print("*** END QUIZ ROUTE DEBUG ***")
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    
    questions = QuizQuestion.get_questions_by_quiz(quiz_id)
    if not questions:
        flash('No questions found in this quiz', 'error')
        return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
    
    
    attempt_id = session.get(f'quiz_attempt_{quiz_id}')
    attempt = None
    
    if attempt_id:
        attempt = QuizAttempt.get_attempt_by_id(attempt_id, user.id)
        if not attempt or attempt.status != 'in_progress':
            attempt = None
            session.pop(f'quiz_attempt_{quiz_id}', None)
    
    
    if not attempt:
        attempt = QuizAttempt.start_attempt(quiz_id, user.id)
        if attempt:
            session[f'quiz_attempt_{quiz_id}'] = attempt.id
        else:
            flash('Error starting quiz attempt', 'error')
            return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
    
    
    current_question_index = int(request.args.get('q', 0))
    
    if current_question_index >= len(questions):
        
        attempt.complete_attempt()
        
        
        if attempt.score is not None:
            time_taken_minutes = attempt.time_taken_minutes or 0
            rewards = GamificationEngine.process_quiz_completion(user.id, attempt.score, time_taken_minutes)
            
            
            session[f'quiz_rewards_{attempt.id}'] = rewards
        
        session.pop(f'quiz_attempt_{quiz_id}', None)
        return redirect(url_for('quizzes.quiz_results', attempt_id=attempt.id))
    
    current_question = questions[current_question_index]
    form = TakeQuizForm()
    
    print(f"Form validation check - validate_on_submit: {form.validate_on_submit()}")
    print(f"Form errors: {form.errors}")
    print(f"Form data: {form.data}")
    
    if form.validate_on_submit():
        print(f"Form submitted - Question ID: {current_question.id}, Answer: '{form.answer.data}', Question Type: {current_question.question_type}")
        
        attempt.submit_answer(current_question.id, form.answer.data)
        
        
        next_index = current_question_index + 1
        if next_index < len(questions):
            return redirect(url_for('quizzes.take_quiz', quiz_id=quiz_id, q=next_index))
        else:
            
            attempt.complete_attempt()
            
            
            if attempt.score is not None:
                time_taken_minutes = attempt.time_taken_minutes or 0
                rewards = GamificationEngine.process_quiz_completion(user.id, attempt.score, time_taken_minutes)
                
                
                session[f'quiz_rewards_{attempt.id}'] = rewards
            
            session.pop(f'quiz_attempt_{quiz_id}', None)
            return redirect(url_for('quizzes.quiz_results', attempt_id=attempt.id))
    
    
    progress = int((current_question_index / len(questions)) * 100)
    
    return render_template('quizzes/take.html', 
                         quiz=quiz, 
                         question=current_question, 
                         question_index=current_question_index,
                         total_questions=len(questions),
                         progress=progress,
                         form=form,
                         attempt=attempt)


@quizzes.route('/debug-quiz/<quiz_id>')
def debug_quiz(quiz_id):
    """Debug route to check quiz data"""
    user = get_current_user()
    if not user:
        return "Not authenticated", 401
    
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        return f"Quiz not found for user {user.id}", 404
    
    questions = QuizQuestion.get_questions_by_quiz(quiz_id)
    
    debug_info = []
    for question in questions:
        debug_info.append({
            'id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'correct_answer': question.correct_answer,
            'options': [{'text': opt.option_text, 'is_correct': opt.is_correct} for opt in question.options]
        })
    
    return f"<pre>{json.dumps(debug_info, indent=2)}</pre>"

@quizzes.route('/results/<attempt_id>')
def quiz_results(attempt_id):
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    
    attempt = QuizAttempt.get_attempt_by_id(attempt_id, user.id)
    if not attempt:
        flash('Quiz attempt not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    
    quiz = Quiz.get_quiz_by_id(attempt.quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    
    topic = Topic.get_topic_by_id(quiz.topic_id, user.id)
    
    
    questions = QuizQuestion.get_questions_by_quiz(quiz.id)
    
    
    qa_mapping = {}
    for answer in attempt.answers:
        qa_mapping[answer.question_id] = answer
        print(f"Quiz Results Debug - Question ID: {answer.question_id}, User Answer: '{answer.user_answer}', Is Correct: {answer.is_correct}")
    
    
    passed = attempt.score >= quiz.passing_score
    
    
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
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    
    questions = QuizQuestion.get_questions_by_quiz(quiz_id)
    if not questions:
        flash('No flashcards found in this quiz', 'error')
        return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
    
    
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
        
        
        FlashcardProgress.create_or_update_progress(user.id, question_id, quality)
        
        
        current_index = int(request.form.get('card_index', 0))
        next_index = current_index + 1
        
        
        questions = QuizQuestion.get_questions_by_quiz(quiz_id)
        if next_index < len(questions):
            return redirect(url_for('quizzes.flashcards', quiz_id=quiz_id, card=next_index))
        else:
            flash('All flashcards completed! Great job!', 'success')
            return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz_id))
    
    return redirect(url_for('quizzes.flashcards', quiz_id=quiz_id))


@quizzes.route('/api/due-flashcards')
def api_due_flashcards():
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    
    due_flashcards = FlashcardProgress.get_due_flashcards(user.id, limit=10)
    
    
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
        
        quizzes_result = supabase.table('quizzes').select('id').eq('user_id', user.id).eq('is_active', True).execute()
        total_quizzes = len(quizzes_result.data)
        
        
        attempts_result = supabase.table('quiz_attempts').select('id, score, status').eq('user_id', user.id).execute()
        total_attempts = len(attempts_result.data)
        
        
        completed_attempts = [a for a in attempts_result.data if a['status'] == 'completed']
        completed_count = len(completed_attempts)
        
        
        if completed_attempts:
            avg_score = sum(a['score'] for a in completed_attempts) / len(completed_attempts)
        else:
            avg_score = 0
        
        
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
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    
    topic = Topic.get_topic_by_id(topic_id, user.id)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    
    num_questions = int(request.args.get('num_questions', 5))
    difficulty = request.args.get('difficulty', 'medium')
    question_type = request.args.get('type', 'mixed')  
    
    try:
        if question_type == 'flashcards':
            
            generated_questions = SmartQuestionGenerator.generate_flashcards_from_topic(
                topic.title, topic.description, num_questions
            )
        else:
            
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
        
        
        quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        added_questions = []
        
        for question_data in selected_questions:
            
            existing_questions = QuizQuestion.get_questions_by_quiz(quiz_id)
            next_order = len(existing_questions)
            
            
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
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    
    quiz = Quiz.get_quiz_by_id(quiz_id, user.id)
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    
    topic = Topic.get_topic_by_id(quiz.topic_id, user.id)
    
    return render_template('quizzes/generate_questions.html', quiz=quiz, topic=topic)


@quizzes.route('/auto-generate/<topic_id>', methods=['GET', 'POST'])
@login_required
def auto_generate_quiz(topic_id):
    """Auto-generate a complete quiz from topic description"""
    
    user = get_current_user()
    if not user:
        flash('User not authenticated.', 'error')
        return redirect(url_for('auth.login'))
    
    # Get the topic
    topic = Topic.get_topic_by_id(topic_id, user.id)
    if not topic:
        flash('Topic not found', 'error')
        return redirect(url_for('quizzes.quiz_list'))
    
    if request.method == 'GET':
        # Show the generation options form
        return render_template('quizzes/auto_generate.html', topic=topic)
    
    # Handle POST request - generate the quiz
    try:
        data = request.get_json() if request.is_json else request.form
        
        # Get generation parameters
        num_questions = int(data.get('num_questions', 5))
        difficulty = data.get('difficulty', 'mixed')
        question_types = data.get('question_types', ['multiple_choice', 'true_false', 'fill_blank'])
        
        # Validate parameters
        if num_questions < 1 or num_questions > 20:
            num_questions = 5
        
        if difficulty not in ['easy', 'medium', 'hard', 'mixed']:
            difficulty = 'mixed'
        
        if isinstance(question_types, str):
            question_types = [question_types]
        
        # Generate the quiz using our smart generator
        quiz_data = SmartQuestionGenerator.generate_smart_quiz_from_topic(
            topic.title, 
            topic.description or "No description available",
            num_questions, 
            difficulty, 
            question_types
        )
        
        if not quiz_data or not quiz_data.get('questions'):
            return jsonify({'error': 'Failed to generate quiz questions'}), 500
        
        # Create the quiz in the database
        quiz = Quiz.create_quiz(
            title=quiz_data['quiz_title'],
            description=quiz_data['quiz_description'],
            topic_id=topic_id,
            user_id=user.id,
            quiz_type='practice_test'
        )
        
        if not quiz:
            return jsonify({'error': 'Failed to create quiz'}), 500
        
        # Add questions to the quiz
        questions_added = 0
        for q_data in quiz_data['questions']:
            question = QuizQuestion.create_question(
                quiz_id=quiz.id,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data.get('explanation', ''),
                points=q_data.get('points', 2)
            )
            
            if question and q_data['question_type'] == 'multiple_choice':
                # Add options for multiple choice questions
                for option_data in q_data.get('options', []):
                    QuizQuestionOption.create_option(
                        question_id=question.id,
                        option_text=option_data['text'],
                        is_correct=option_data['is_correct']
                    )
            
            if question:
                questions_added += 1
        
        if questions_added == 0:
            # Delete the quiz if no questions were added
            Quiz.delete_quiz(quiz.id, user.id)
            return jsonify({'error': 'Failed to add questions to quiz'}), 500
        
        # Return success response
        response_data = {
            'success': True,
            'quiz_id': str(quiz.id),
            'quiz_title': quiz.title,
            'questions_added': questions_added,
            'generation_method': quiz_data.get('generation_method', 'unknown'),
            'redirect_url': url_for('quizzes.quiz_detail', quiz_id=quiz.id)
        }
        
        if request.is_json:
            return jsonify(response_data)
        else:
            flash(f'Successfully generated quiz "{quiz.title}" with {questions_added} questions!', 'success')
            return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz.id))
    
    except Exception as e:
        print(f"Error in auto-generate quiz: {e}")
        error_msg = f"Failed to generate quiz: {str(e)}"
        
        if request.is_json:
            return jsonify({'error': error_msg}), 500
        else:
            flash(error_msg, 'error')
            return redirect(url_for('quizzes.topic_quizzes', topic_id=topic_id))


@quizzes.route('/api/auto-generate-preview/<topic_id>')
@login_required
def api_auto_generate_preview(topic_id):
    """Generate a preview of questions without saving to database"""
    
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not authenticated'}), 401
    
    # Get the topic
    topic = Topic.get_topic_by_id(topic_id, user.id)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    try:
        # Get parameters from query string
        num_questions = int(request.args.get('num_questions', 3))
        difficulty = request.args.get('difficulty', 'medium')
        question_types = request.args.getlist('question_types') or ['multiple_choice']
        
        # Validate parameters
        if num_questions < 1 or num_questions > 10:
            num_questions = 3
        
        if difficulty not in ['easy', 'medium', 'hard', 'mixed']:
            difficulty = 'medium'
        
        # Generate preview questions
        quiz_data = SmartQuestionGenerator.generate_smart_quiz_from_topic(
            topic.title,
            topic.description or "No description available",
            num_questions,
            difficulty,
            question_types
        )
        
        if not quiz_data or not quiz_data.get('questions'):
            return jsonify({'error': 'Failed to generate preview questions'}), 500
        
        # Return only the questions data for preview
        return jsonify({
            'success': True,
            'questions': quiz_data['questions'][:num_questions],
            'generation_method': quiz_data.get('generation_method', 'unknown'),
            'quiz_title': quiz_data.get('quiz_title', f'Quiz: {topic.title}'),
            'quiz_description': quiz_data.get('quiz_description', f'Test your knowledge of {topic.title}')
        })
    
    except Exception as e:
        print(f"Error in auto-generate preview: {e}")
        return jsonify({'error': f'Failed to generate preview: {str(e)}'}), 500

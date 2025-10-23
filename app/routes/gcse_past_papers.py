

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from app.models.gcse_past_papers import GCSEPastPaper, GCSEPastPaperQuestion, GCSEExamPractice, GCSEExamPracticeAnswer
from app.models.gcse_curriculum import GCSESubject, GCSESpecification
from app.routes.topics import get_current_user
from datetime import datetime, timedelta
import json

gcse_past_papers = Blueprint('gcse_past_papers', __name__, url_prefix='/gcse/past-papers')

@gcse_past_papers.route('/')
@login_required
def past_papers_list():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.args.get('subject_id')
        exam_board = request.args.get('exam_board')
        exam_year = request.args.get('exam_year', type=int)
        difficulty_level = request.args.get('difficulty_level')
        
        
        subjects = GCSESubject.get_all_subjects()
        exam_boards = GCSESpecification.get_exam_boards()
        
        
        past_papers = []
        if subject_id:

            past_papers = GCSEPastPaper.get_past_papers_by_subject(
                subject_id, exam_board, exam_year, difficulty_level
            )
        else:

            for subject in subjects:
                subject_papers = GCSEPastPaper.get_past_papers_by_subject(
                    subject.id, exam_board, exam_year, difficulty_level
                )
                past_papers.extend(subject_papers)
            

            past_papers.sort(key=lambda p: (p.exam_year, p.subject_id), reverse=True)
        
        
        recent_sessions = GCSEExamPractice.get_user_practice_sessions(user.id, limit=5)
        
        return render_template('gcse/past_papers/list.html',
                             subjects=subjects,
                             exam_boards=exam_boards,
                             past_papers=past_papers,
                             recent_sessions=recent_sessions,
                             selected_subject_id=subject_id,
                             selected_exam_board=exam_board,
                             selected_exam_year=exam_year,
                             selected_difficulty_level=difficulty_level)
    
    except Exception as e:
        flash('Error loading past papers.', 'error')
        return redirect(url_for('gcse.gcse_dashboard'))

@gcse_past_papers.route('/subject/<subject_id>')
@login_required
def subject_past_papers(subject_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject = GCSESubject.get_subject_by_id(subject_id)
        if not subject:
            flash('GCSE subject not found.', 'error')
            return redirect(url_for('gcse_past_papers.past_papers_list'))
        
        
        past_papers = GCSEPastPaper.get_past_papers_by_subject(subject_id)
        
        
        papers_by_year = {}
        for paper in past_papers:
            year = paper.exam_year
            if year not in papers_by_year:
                papers_by_year[year] = {}
            
            month = paper.exam_month
            if month not in papers_by_year[year]:
                papers_by_year[year][month] = []
            
            papers_by_year[year][month].append(paper)
        
        
        user_sessions = GCSEExamPractice.get_user_practice_sessions(user.id, limit=20)
        subject_sessions = [s for s in user_sessions if s.past_paper_id and 
                          any(p.id == s.past_paper_id for p in past_papers)]
        
        return render_template('gcse/past_papers/subject_papers.html',
                             subject=subject,
                             papers_by_year=papers_by_year,
                             subject_sessions=subject_sessions)
    
    except Exception as e:
        flash('Error loading subject past papers.', 'error')
        return redirect(url_for('gcse_past_papers.past_papers_list'))

@gcse_past_papers.route('/paper/<paper_id>')
@login_required
def past_paper_detail(paper_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        paper = GCSEPastPaper.get_past_paper_by_id(paper_id)
        if not paper:
            flash('Past paper not found.', 'error')
            return redirect(url_for('gcse_past_papers.past_papers_list'))
        
        
        subject = GCSESubject.get_subject_by_id(paper.subject_id)
        
        
        user_sessions = GCSEExamPractice.get_user_practice_sessions(user.id, limit=50)
        paper_sessions = [s for s in user_sessions if s.past_paper_id == paper_id]
        
        
        grade_boundaries = GCSESpecification.get_grade_boundaries(
            paper.exam_board, paper.specification_code
        )
        
        return render_template('gcse/past_papers/paper_detail.html',
                             paper=paper,
                             subject=subject,
                             paper_sessions=paper_sessions,
                             grade_boundaries=grade_boundaries)
    
    except Exception as e:
        flash('Error loading past paper details.', 'error')
        return redirect(url_for('gcse_past_papers.past_papers_list'))

@gcse_past_papers.route('/paper/<paper_id>/practice', methods=['GET', 'POST'])
@login_required
def start_practice_session(paper_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        paper = GCSEPastPaper.get_past_paper_by_id(paper_id)
        if not paper:
            flash('Past paper not found.', 'error')
            return redirect(url_for('gcse_past_papers.past_papers_list'))
        
        
        active_session_id = session.get(f'practice_session_{paper_id}')
        active_session = None
        
        if active_session_id:
            active_session = GCSEExamPractice.get_practice_session_by_id(active_session_id, user.id)
            if not active_session or active_session.status != 'in_progress':
                active_session = None
                session.pop(f'practice_session_{paper_id}', None)
        
        
        if not active_session:
            active_session = GCSEExamPractice.start_practice_session(
                user.id, paper_id, paper.difficulty_level
            )
            if active_session:
                session[f'practice_session_{paper_id}'] = active_session.id
            else:
                flash('Error starting practice session.', 'error')
                return redirect(url_for('gcse_past_papers.past_paper_detail', paper_id=paper_id))
        
        
        current_question_index = int(request.args.get('q', 0))
        
        if current_question_index >= len(paper.questions):
            
            active_session.complete_practice_session()
            
            
            session.pop(f'practice_session_{paper_id}', None)
            
            
            from app.models.gamification import GamificationEngine
            rewards = GamificationEngine.process_exam_completion(
                user.id, active_session.achieved_marks, active_session.total_marks,
                active_session.time_taken_minutes
            )
            
            
            session[f'practice_rewards_{active_session.id}'] = rewards
            
            return redirect(url_for('gcse_past_papers.practice_results', session_id=active_session.id))
        
        current_question = paper.questions[current_question_index]
        
        
        user_answer = None
        for answer in active_session.answers:
            if answer.question_id == current_question.id:
                user_answer = answer.user_answer
                break
        
        
        progress = int((current_question_index / len(paper.questions)) * 100)
        
        return render_template('gcse/past_papers/practice_session.html',
                             paper=paper,
                             question=current_question,
                             question_index=current_question_index,
                             total_questions=len(paper.questions),
                             progress=progress,
                             user_answer=user_answer,
                             session=active_session)
    
    except Exception as e:
        flash('Error starting practice session.', 'error')
        return redirect(url_for('gcse_past_papers.past_paper_detail', paper_id=paper_id))

@gcse_past_papers.route('/practice/submit-answer', methods=['POST'])
@login_required
def submit_practice_answer():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        data = request.get_json()
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        user_answer = data.get('answer', '').strip()
        time_spent = data.get('time_spent', 0)
        
        if not all([session_id, question_id]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        
        practice_session = GCSEExamPractice.get_practice_session_by_id(session_id, user.id)
        if not practice_session:
            return jsonify({'error': 'Practice session not found'}), 404
        
        
        success = practice_session.submit_answer(question_id, user_answer, time_spent)
        
        if success:
            return jsonify({'success': True, 'message': 'Answer submitted successfully'})
        else:
            return jsonify({'error': 'Failed to submit answer'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_past_papers.route('/practice/results/<session_id>')
@login_required
def practice_results(session_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        practice_session = GCSEExamPractice.get_practice_session_by_id(session_id, user.id)
        if not practice_session:
            flash('Practice session not found.', 'error')
            return redirect(url_for('gcse_past_papers.past_papers_list'))
        
        
        paper = GCSEPastPaper.get_past_paper_by_id(practice_session.past_paper_id)
        if not paper:
            flash('Past paper not found.', 'error')
            return redirect(url_for('gcse_past_papers.past_papers_list'))
        
        
        subject = GCSESubject.get_subject_by_id(paper.subject_id)
        
        
        questions = paper.questions
        qa_mapping = {}
        for answer in practice_session.answers:
            qa_mapping[answer.question_id] = answer
        
        
        rewards = session.get(f'practice_rewards_{session_id}', {})
        
        
        percentage = (practice_session.achieved_marks / practice_session.total_marks * 100) if practice_session.total_marks > 0 else 0
        
        return render_template('gcse/past_papers/practice_results.html',
                             practice_session=practice_session,
                             paper=paper,
                             subject=subject,
                             questions=questions,
                             qa_mapping=qa_mapping,
                             rewards=rewards,
                             percentage=percentage)
    
    except Exception as e:
        flash('Error loading practice results.', 'error')
        return redirect(url_for('gcse_past_papers.past_papers_list'))

@gcse_past_papers.route('/practice/history')
@login_required
def practice_history():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
        subject_id = request.args.get('subject_id')
        exam_board = request.args.get('exam_board')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        
        all_sessions = GCSEExamPractice.get_user_practice_sessions(user.id, limit=100)
        
        
        filtered_sessions = all_sessions
        if subject_id:
            
            subject_papers = GCSEPastPaper.get_past_papers_by_subject(subject_id)
            subject_paper_ids = [p.id for p in subject_papers]
            filtered_sessions = [s for s in filtered_sessions if s.past_paper_id in subject_paper_ids]
        
        if exam_board:
            
            filtered_sessions = [s for s in filtered_sessions 
                               if any(p.exam_board == exam_board for p in GCSEPastPaper.get_past_papers_by_subject(s.past_paper_id) if s.past_paper_id)]
        
        
        filtered_sessions.sort(key=lambda x: x.started_at, reverse=True)
        
        
        total_sessions = len(filtered_sessions)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        sessions_page = filtered_sessions[start_idx:end_idx]
        
        
        subjects = GCSESubject.get_all_subjects()
        exam_boards = GCSESpecification.get_exam_boards()
        
        
        has_prev = page > 1
        has_next = end_idx < total_sessions
        prev_page = page - 1 if has_prev else None
        next_page = page + 1 if has_next else None
        
        return render_template('gcse/past_papers/practice_history.html',
                             sessions=sessions_page,
                             subjects=subjects,
                             exam_boards=exam_boards,
                             selected_subject_id=subject_id,
                             selected_exam_board=exam_board,
                             page=page,
                             has_prev=has_prev,
                             has_next=has_next,
                             prev_page=prev_page,
                             next_page=next_page,
                             total_sessions=total_sessions)
    
    except Exception as e:
        flash('Error loading practice history.', 'error')
        return redirect(url_for('gcse_past_papers.past_papers_list'))


@gcse_past_papers.route('/api/papers/<subject_id>')
@login_required
def api_get_papers_for_subject(subject_id):
    
    try:
        exam_board = request.args.get('exam_board')
        exam_year = request.args.get('exam_year', type=int)
        difficulty_level = request.args.get('difficulty_level')
        
        papers = GCSEPastPaper.get_past_papers_by_subject(
            subject_id, exam_board, exam_year, difficulty_level
        )
        
        papers_data = []
        for paper in papers:
            papers_data.append({
                'id': paper.id,
                'paper_title': paper.paper_title,
                'exam_year': paper.exam_year,
                'exam_month': paper.exam_month,
                'paper_number': paper.paper_number,
                'exam_board': paper.exam_board,
                'difficulty_level': paper.difficulty_level,
                'total_marks': paper.total_marks,
                'duration_minutes': paper.duration_minutes,
                'question_count': len(paper.questions)
            })
        
        return jsonify({'papers': papers_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gcse_past_papers.route('/api/practice/stats')
@login_required
def api_practice_stats():
    
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        
        sessions = GCSEExamPractice.get_user_practice_sessions(user.id, limit=20)
        
        
        total_sessions = len(sessions)
        completed_sessions = len([s for s in sessions if s.status == 'completed'])
        
        if completed_sessions > 0:
            avg_score = sum(s.achieved_marks / s.total_marks * 100 for s in sessions if s.status == 'completed') / completed_sessions
            avg_time = sum(s.time_taken_minutes for s in sessions if s.status == 'completed') / completed_sessions
        else:
            avg_score = 0
            avg_time = 0
        
        
        grade_distribution = {}
        for session in sessions:
            if session.status == 'completed' and session.grade:
                grade = session.grade
                grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
        
        return jsonify({
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'average_score': round(avg_score, 1),
            'average_time_minutes': round(avg_time, 1),
            'grade_distribution': grade_distribution
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


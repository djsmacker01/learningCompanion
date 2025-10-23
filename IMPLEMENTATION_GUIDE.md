# Implementation Guide - Priority Features

## 🎯 CRITICAL FEATURE 1: Classroom Management System

### Database Schema (Supabase Migration)

```sql
-- supabase/migrations/020_classroom_management.sql

-- Classrooms table
CREATE TABLE classrooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    teacher_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(100),
    year_group VARCHAR(50),
    class_code VARCHAR(10) UNIQUE NOT NULL,
    academic_year VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Classroom members
CREATE TABLE classroom_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    classroom_id UUID REFERENCES classrooms(id) ON DELETE CASCADE,
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    role VARCHAR(20) DEFAULT 'student', -- student, co-teacher
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(classroom_id, student_id)
);

-- Assignments
CREATE TABLE assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    classroom_id UUID REFERENCES classrooms(id) ON DELETE CASCADE,
    teacher_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    assignment_type VARCHAR(50), -- quiz, reading, practice, project
    due_date TIMESTAMP WITH TIME ZONE,
    points_possible INTEGER,
    topic_id INTEGER REFERENCES topics(id),
    quiz_id UUID REFERENCES quizzes(id),
    allow_late_submission BOOLEAN DEFAULT TRUE,
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Assignment submissions
CREATE TABLE assignment_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assignment_id UUID REFERENCES assignments(id) ON DELETE CASCADE,
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    submitted_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'assigned', -- assigned, in_progress, submitted, graded, late
    points_earned INTEGER,
    feedback TEXT,
    teacher_comments TEXT,
    graded_at TIMESTAMP WITH TIME ZONE,
    graded_by UUID REFERENCES users(id),
    UNIQUE(assignment_id, student_id)
);

-- Classroom announcements
CREATE TABLE classroom_announcements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    classroom_id UUID REFERENCES classrooms(id) ON DELETE CASCADE,
    teacher_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    is_pinned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_classroom_members_student ON classroom_members(student_id);
CREATE INDEX idx_assignments_classroom ON assignments(classroom_id);
CREATE INDEX idx_assignments_due_date ON assignments(due_date);
CREATE INDEX idx_submissions_student ON assignment_submissions(student_id);
CREATE INDEX idx_submissions_status ON assignment_submissions(status);
```

### Python Models

```python
# app/models/classroom.py

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from app.models import get_supabase_client, SUPABASE_AVAILABLE
import secrets
import string

class Classroom:
    """Teacher's classroom management"""
    
    def __init__(self, id=None, teacher_id=None, name=None, subject=None,
                 year_group=None, class_code=None, academic_year=None,
                 is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.teacher_id = teacher_id
        self.name = name
        self.subject = subject
        self.year_group = year_group
        self.class_code = class_code
        self.academic_year = academic_year
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def create_classroom(cls, teacher_id: str, name: str, subject: str = None,
                        year_group: str = None, academic_year: str = None) -> 'Classroom':
        """Teacher creates a new classroom"""
        if not SUPABASE_AVAILABLE:
            return None
        
        supabase = get_supabase_client()
        
        # Generate unique class code
        class_code = cls._generate_class_code()
        
        classroom_data = {
            'teacher_id': teacher_id,
            'name': name,
            'subject': subject,
            'year_group': year_group,
            'class_code': class_code,
            'academic_year': academic_year or cls._get_current_academic_year(),
            'is_active': True
        }
        
        try:
            result = supabase.table('classrooms').insert(classroom_data).execute()
            if result.data:
                return cls(**result.data[0])
        except Exception as e:
            print(f"Error creating classroom: {e}")
        
        return None
    
    @classmethod
    def _generate_class_code(cls) -> str:
        """Generate unique 6-character class code"""
        supabase = get_supabase_client()
        
        while True:
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            # Check if code exists
            existing = supabase.table('classrooms').select('id').eq('class_code', code).execute()
            if not existing.data:
                return code
    
    @classmethod
    def _get_current_academic_year(cls) -> str:
        """Get current academic year (e.g., 2024-2025)"""
        now = datetime.now()
        if now.month >= 9:  # September onwards
            return f"{now.year}-{now.year + 1}"
        else:
            return f"{now.year - 1}-{now.year}"
    
    @classmethod
    def join_with_code(cls, student_id: str, class_code: str) -> bool:
        """Student joins classroom with code"""
        if not SUPABASE_AVAILABLE:
            return False
        
        supabase = get_supabase_client()
        
        try:
            # Find classroom
            classroom_result = supabase.table('classrooms').select('id').eq('class_code', class_code).eq('is_active', True).execute()
            
            if not classroom_result.data:
                return False
            
            classroom_id = classroom_result.data[0]['id']
            
            # Check if already member
            existing = supabase.table('classroom_members').select('id').eq('classroom_id', classroom_id).eq('student_id', student_id).execute()
            
            if existing.data:
                return True  # Already a member
            
            # Add to classroom
            member_data = {
                'classroom_id': classroom_id,
                'student_id': student_id,
                'role': 'student',
                'is_active': True
            }
            
            result = supabase.table('classroom_members').insert(member_data).execute()
            return bool(result.data)
            
        except Exception as e:
            print(f"Error joining classroom: {e}")
            return False
    
    @classmethod
    def get_teacher_classrooms(cls, teacher_id: str) -> List['Classroom']:
        """Get all classrooms for a teacher"""
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('classrooms').select('*').eq('teacher_id', teacher_id).eq('is_active', True).order('created_at', desc=True).execute()
            return [cls(**classroom) for classroom in result.data]
        except Exception as e:
            print(f"Error getting teacher classrooms: {e}")
            return []
    
    @classmethod
    def get_student_classrooms(cls, student_id: str) -> List['Classroom']:
        """Get all classrooms a student is enrolled in"""
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        
        try:
            # Get classroom IDs
            members_result = supabase.table('classroom_members').select('classroom_id').eq('student_id', student_id).eq('is_active', True).execute()
            
            if not members_result.data:
                return []
            
            classroom_ids = [m['classroom_id'] for m in members_result.data]
            
            # Get classroom details
            classrooms_result = supabase.table('classrooms').select('*').in_('id', classroom_ids).eq('is_active', True).execute()
            
            return [cls(**classroom) for classroom in classrooms_result.data]
        except Exception as e:
            print(f"Error getting student classrooms: {e}")
            return []
    
    def get_students(self) -> List[Dict]:
        """Get all students in this classroom"""
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('classroom_members').select('*, users(id, email, name)').eq('classroom_id', self.id).eq('is_active', True).execute()
            
            return [
                {
                    'id': member['student_id'],
                    'email': member['users']['email'],
                    'name': member['users'].get('name'),
                    'joined_at': member['joined_at']
                }
                for member in result.data
            ]
        except Exception as e:
            print(f"Error getting classroom students: {e}")
            return []
    
    def get_student_count(self) -> int:
        """Get number of students in classroom"""
        if not SUPABASE_AVAILABLE:
            return 0
        
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('classroom_members').select('id', count='exact').eq('classroom_id', self.id).eq('is_active', True).execute()
            return result.count or 0
        except Exception as e:
            print(f"Error getting student count: {e}")
            return 0


class Assignment:
    """Classroom assignment"""
    
    def __init__(self, id=None, classroom_id=None, teacher_id=None, title=None,
                 description=None, assignment_type=None, due_date=None,
                 points_possible=None, topic_id=None, quiz_id=None,
                 allow_late_submission=True, is_published=False,
                 created_at=None, updated_at=None):
        self.id = id
        self.classroom_id = classroom_id
        self.teacher_id = teacher_id
        self.title = title
        self.description = description
        self.assignment_type = assignment_type
        self.due_date = due_date
        self.points_possible = points_possible
        self.topic_id = topic_id
        self.quiz_id = quiz_id
        self.allow_late_submission = allow_late_submission
        self.is_published = is_published
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def create_assignment(cls, classroom_id: str, teacher_id: str, title: str,
                         description: str = None, assignment_type: str = 'reading',
                         due_date: datetime = None, points_possible: int = 100,
                         topic_id: int = None, quiz_id: str = None,
                         auto_publish: bool = False) -> 'Assignment':
        """Teacher creates an assignment"""
        if not SUPABASE_AVAILABLE:
            return None
        
        supabase = get_supabase_client()
        
        assignment_data = {
            'classroom_id': classroom_id,
            'teacher_id': teacher_id,
            'title': title,
            'description': description,
            'assignment_type': assignment_type,
            'due_date': due_date.isoformat() if due_date else None,
            'points_possible': points_possible,
            'topic_id': topic_id,
            'quiz_id': quiz_id,
            'is_published': auto_publish
        }
        
        try:
            result = supabase.table('assignments').insert(assignment_data).execute()
            if result.data:
                assignment = cls(**result.data[0])
                
                # If published, create submissions for all students
                if auto_publish:
                    assignment._create_submissions_for_students()
                
                return assignment
        except Exception as e:
            print(f"Error creating assignment: {e}")
        
        return None
    
    def _create_submissions_for_students(self):
        """Create assignment submission records for all students in classroom"""
        if not SUPABASE_AVAILABLE:
            return
        
        supabase = get_supabase_client()
        
        try:
            # Get all students in classroom
            members_result = supabase.table('classroom_members').select('student_id').eq('classroom_id', self.classroom_id).eq('is_active', True).execute()
            
            # Create submission records
            submissions = [
                {
                    'assignment_id': self.id,
                    'student_id': member['student_id'],
                    'status': 'assigned'
                }
                for member in members_result.data
            ]
            
            if submissions:
                supabase.table('assignment_submissions').insert(submissions).execute()
        except Exception as e:
            print(f"Error creating submissions: {e}")
    
    @classmethod
    def get_classroom_assignments(cls, classroom_id: str, published_only: bool = True) -> List['Assignment']:
        """Get all assignments for a classroom"""
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('assignments').select('*').eq('classroom_id', classroom_id)
            
            if published_only:
                query = query.eq('is_published', True)
            
            result = query.order('due_date', desc=False).execute()
            return [cls(**assignment) for assignment in result.data]
        except Exception as e:
            print(f"Error getting classroom assignments: {e}")
            return []
    
    @classmethod
    def get_student_assignments(cls, student_id: str, status: str = None) -> List[Dict]:
        """Get all assignments for a student across all classrooms"""
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        
        try:
            query = supabase.table('assignment_submissions').select(
                '*, assignments(*, classrooms(name, teacher_id))'
            ).eq('student_id', student_id)
            
            if status:
                query = query.eq('status', status)
            
            result = query.order('assignments(due_date)', desc=False).execute()
            
            return [
                {
                    'submission_id': submission['id'],
                    'assignment_id': submission['assignment_id'],
                    'title': submission['assignments']['title'],
                    'classroom_name': submission['assignments']['classrooms']['name'],
                    'due_date': submission['assignments']['due_date'],
                    'status': submission['status'],
                    'points_earned': submission['points_earned'],
                    'points_possible': submission['assignments']['points_possible']
                }
                for submission in result.data
            ]
        except Exception as e:
            print(f"Error getting student assignments: {e}")
            return []
    
    def get_submission_stats(self) -> Dict:
        """Get submission statistics for this assignment"""
        if not SUPABASE_AVAILABLE:
            return {}
        
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('assignment_submissions').select('status').eq('assignment_id', self.id).execute()
            
            total = len(result.data)
            submitted = sum(1 for s in result.data if s['status'] in ['submitted', 'graded'])
            graded = sum(1 for s in result.data if s['status'] == 'graded')
            late = sum(1 for s in result.data if s['status'] == 'late')
            
            return {
                'total_students': total,
                'submitted': submitted,
                'graded': graded,
                'late': late,
                'pending': total - submitted,
                'submission_rate': round((submitted / total * 100) if total > 0 else 0, 1)
            }
        except Exception as e:
            print(f"Error getting submission stats: {e}")
            return {}


class AssignmentSubmission:
    """Student's submission for an assignment"""
    
    @classmethod
    def submit_assignment(cls, assignment_id: str, student_id: str, 
                         submission_data: Dict = None) -> bool:
        """Student submits an assignment"""
        if not SUPABASE_AVAILABLE:
            return False
        
        supabase = get_supabase_client()
        
        try:
            # Check if assignment exists and due date
            assignment_result = supabase.table('assignments').select('due_date, allow_late_submission').eq('id', assignment_id).execute()
            
            if not assignment_result.data:
                return False
            
            assignment = assignment_result.data[0]
            is_late = False
            
            if assignment['due_date']:
                due_date = datetime.fromisoformat(assignment['due_date'].replace('Z', '+00:00'))
                is_late = datetime.now() > due_date
                
                if is_late and not assignment['allow_late_submission']:
                    return False  # Late submissions not allowed
            
            # Update submission
            update_data = {
                'submitted_at': datetime.now().isoformat(),
                'status': 'late' if is_late else 'submitted'
            }
            
            result = supabase.table('assignment_submissions').update(update_data).eq('assignment_id', assignment_id).eq('student_id', student_id).execute()
            
            return bool(result.data)
        except Exception as e:
            print(f"Error submitting assignment: {e}")
            return False
    
    @classmethod
    def grade_submission(cls, submission_id: str, points_earned: int,
                        feedback: str = None, teacher_id: str = None) -> bool:
        """Teacher grades a submission"""
        if not SUPABASE_AVAILABLE:
            return False
        
        supabase = get_supabase_client()
        
        try:
            update_data = {
                'points_earned': points_earned,
                'feedback': feedback,
                'status': 'graded',
                'graded_at': datetime.now().isoformat(),
                'graded_by': teacher_id
            }
            
            result = supabase.table('assignment_submissions').update(update_data).eq('id', submission_id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error grading submission: {e}")
            return False
```

### Flask Routes

```python
# app/routes/classroom.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.classroom import Classroom, Assignment, AssignmentSubmission
from app.forms.classroom_forms import ClassroomForm, AssignmentForm
from datetime import datetime

classroom = Blueprint('classroom', __name__, url_prefix='/classroom')

@classroom.route('/dashboard')
@login_required
def dashboard():
    """Main classroom dashboard - shows different view for teachers vs students"""
    user_id = current_user.id
    
    # Check if user is a teacher (has created classrooms)
    teacher_classrooms = Classroom.get_teacher_classrooms(user_id)
    student_classrooms = Classroom.get_student_classrooms(user_id)
    
    if teacher_classrooms:
        # Teacher view
        return render_template('classroom/teacher_dashboard.html',
                             classrooms=teacher_classrooms)
    else:
        # Student view
        assignments = Assignment.get_student_assignments(user_id)
        return render_template('classroom/student_dashboard.html',
                             classrooms=student_classrooms,
                             assignments=assignments)

@classroom.route('/create', methods=['GET', 'POST'])
@login_required
def create_classroom():
    """Teacher creates a new classroom"""
    form = ClassroomForm()
    
    if form.validate_on_submit():
        classroom = Classroom.create_classroom(
            teacher_id=current_user.id,
            name=form.name.data,
            subject=form.subject.data,
            year_group=form.year_group.data
        )
        
        if classroom:
            flash(f'Classroom created! Class code: {classroom.class_code}', 'success')
            return redirect(url_for('classroom.view_classroom', classroom_id=classroom.id))
        else:
            flash('Error creating classroom', 'error')
    
    return render_template('classroom/create_classroom.html', form=form)

@classroom.route('/join', methods=['GET', 'POST'])
@login_required
def join_classroom():
    """Student joins a classroom with code"""
    if request.method == 'POST':
        class_code = request.form.get('class_code', '').upper().strip()
        
        if Classroom.join_with_code(current_user.id, class_code):
            flash(f'Successfully joined classroom!', 'success')
            return redirect(url_for('classroom.dashboard'))
        else:
            flash('Invalid class code or classroom not found', 'error')
    
    return render_template('classroom/join_classroom.html')

@classroom.route('/<classroom_id>')
@login_required
def view_classroom(classroom_id):
    """View a specific classroom"""
    # Get classroom details
    teacher_classrooms = Classroom.get_teacher_classrooms(current_user.id)
    student_classrooms = Classroom.get_student_classrooms(current_user.id)
    
    # Check access
    classroom_obj = None
    is_teacher = False
    
    for c in teacher_classrooms:
        if c.id == classroom_id:
            classroom_obj = c
            is_teacher = True
            break
    
    if not classroom_obj:
        for c in student_classrooms:
            if c.id == classroom_id:
                classroom_obj = c
                break
    
    if not classroom_obj:
        flash('Classroom not found or access denied', 'error')
        return redirect(url_for('classroom.dashboard'))
    
    # Get assignments
    assignments = Assignment.get_classroom_assignments(classroom_id)
    
    if is_teacher:
        # Teacher view - get students and stats
        students = classroom_obj.get_students()
        return render_template('classroom/classroom_teacher_view.html',
                             classroom=classroom_obj,
                             assignments=assignments,
                             students=students,
                             student_count=len(students))
    else:
        # Student view
        my_submissions = Assignment.get_student_assignments(current_user.id)
        return render_template('classroom/classroom_student_view.html',
                             classroom=classroom_obj,
                             assignments=assignments,
                             my_submissions=my_submissions)

@classroom.route('/<classroom_id>/assignment/create', methods=['GET', 'POST'])
@login_required
def create_assignment(classroom_id):
    """Teacher creates an assignment"""
    # Verify teacher owns this classroom
    teacher_classrooms = Classroom.get_teacher_classrooms(current_user.id)
    if not any(c.id == classroom_id for c in teacher_classrooms):
        flash('Access denied', 'error')
        return redirect(url_for('classroom.dashboard'))
    
    form = AssignmentForm()
    
    if form.validate_on_submit():
        assignment = Assignment.create_assignment(
            classroom_id=classroom_id,
            teacher_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            assignment_type=form.assignment_type.data,
            due_date=form.due_date.data,
            points_possible=form.points_possible.data,
            auto_publish=form.publish_now.data
        )
        
        if assignment:
            flash('Assignment created successfully!', 'success')
            return redirect(url_for('classroom.view_classroom', classroom_id=classroom_id))
        else:
            flash('Error creating assignment', 'error')
    
    return render_template('classroom/create_assignment.html',
                         form=form,
                         classroom_id=classroom_id)

@classroom.route('/assignment/<assignment_id>/submit', methods=['POST'])
@login_required
def submit_assignment(assignment_id):
    """Student submits an assignment"""
    if AssignmentSubmission.submit_assignment(assignment_id, current_user.id):
        flash('Assignment submitted successfully!', 'success')
    else:
        flash('Error submitting assignment', 'error')
    
    return redirect(url_for('classroom.dashboard'))

@classroom.route('/assignment/<assignment_id>/grade')
@login_required
def grade_assignment(assignment_id):
    """Teacher grades an assignment"""
    # Get assignment and submissions
    # (implementation details...)
    return render_template('classroom/grade_assignment.html')

@classroom.route('/api/classroom/<classroom_id>/stats')
@login_required
def classroom_stats(classroom_id):
    """API endpoint for classroom statistics"""
    # Verify access
    # Return JSON with stats
    # (implementation details...)
    pass
```

### Forms

```python
# app/forms/classroom_forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Optional

class ClassroomForm(FlaskForm):
    name = StringField('Classroom Name', validators=[DataRequired(), Length(min=3, max=100)])
    subject = SelectField('Subject', choices=[
        ('Mathematics', 'Mathematics'),
        ('English', 'English'),
        ('Science', 'Science'),
        ('History', 'History'),
        ('Geography', 'Geography'),
        ('Computer Science', 'Computer Science'),
        ('Other', 'Other')
    ])
    year_group = SelectField('Year Group', choices=[
        ('Year 7', 'Year 7'),
        ('Year 8', 'Year 8'),
        ('Year 9', 'Year 9'),
        ('Year 10', 'Year 10'),
        ('Year 11', 'Year 11')
    ])

class AssignmentForm(FlaskForm):
    title = StringField('Assignment Title', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    assignment_type = SelectField('Type', choices=[
        ('reading', 'Reading'),
        ('quiz', 'Quiz'),
        ('practice', 'Practice'),
        ('project', 'Project'),
        ('homework', 'Homework')
    ])
    due_date = DateTimeField('Due Date', validators=[Optional()], format='%Y-%m-%dT%H:%M')
    points_possible = IntegerField('Points', validators=[DataRequired()], default=100)
    publish_now = BooleanField('Publish Immediately', default=True)
```

---

## 🎯 CRITICAL FEATURE 2: Spaced Repetition System

### Algorithm Implementation

```python
# app/utils/spaced_repetition.py

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import math

class ResponseQuality(Enum):
    """Student's response quality rating (SM-2 algorithm)"""
    BLACKOUT = 0      # Complete blackout
    INCORRECT = 1     # Incorrect, felt familiar
    RECALL_HARD = 2   # Recalled with serious difficulty
    RECALL_MODERATE = 3  # Recalled with hesitation
    RECALL_EASY = 4   # Recalled with moderate ease
    PERFECT = 5       # Perfect recall, trivial

class SpacedRepetitionCard:
    """A card/topic for spaced repetition"""
    
    def __init__(self, content_id: str, content_type: str = 'topic',
                 easiness_factor: float = 2.5, interval: int = 1,
                 repetitions: int = 0, next_review: datetime = None,
                 last_reviewed: datetime = None):
        self.content_id = content_id
        self.content_type = content_type  # topic, quiz_question, flashcard
        self.easiness_factor = easiness_factor  # Default 2.5
        self.interval = interval  # Days until next review
        self.repetitions = repetitions  # Number of successful repetitions
        self.next_review = next_review or datetime.now()
        self.last_reviewed = last_reviewed
    
    def update_after_review(self, quality: ResponseQuality) -> Dict:
        """Update card parameters after a review (SM-2 algorithm)"""
        q = quality.value
        
        # Update easiness factor
        self.easiness_factor = max(1.3, self.easiness_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
        
        # Update repetitions and interval
        if q < 3:
            # Poor recall - restart
            self.repetitions = 0
            self.interval = 1
        else:
            # Good recall - increase interval
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = math.ceil(self.interval * self.easiness_factor)
            
            self.repetitions += 1
        
        # Calculate next review date
        self.last_reviewed = datetime.now()
        self.next_review = self.last_reviewed + timedelta(days=self.interval)
        
        return {
            'easiness_factor': self.easiness_factor,
            'interval': self.interval,
            'repetitions': self.repetitions,
            'next_review': self.next_review.isoformat(),
            'last_reviewed': self.last_reviewed.isoformat()
        }

class SpacedRepetitionEngine:
    """Manages spaced repetition for a user"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
    
    def get_due_cards(self, limit: int = 20) -> List[Dict]:
        """Get cards due for review"""
        from app.models import get_supabase_client, SUPABASE_AVAILABLE
        
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        
        try:
            # Get cards due for review
            result = supabase.table('spaced_repetition_cards').select(
                '*'
            ).eq('user_id', self.user_id).lte(
                'next_review', datetime.now().isoformat()
            ).order('next_review').limit(limit).execute()
            
            return result.data
        except Exception as e:
            print(f"Error getting due cards: {e}")
            return []
    
    def record_review(self, card_id: str, quality: ResponseQuality) -> bool:
        """Record a review and update card schedule"""
        from app.models import get_supabase_client, SUPABASE_AVAILABLE
        
        if not SUPABASE_AVAILABLE:
            return False
        
        supabase = get_supabase_client()
        
        try:
            # Get current card data
            card_result = supabase.table('spaced_repetition_cards').select('*').eq('id', card_id).execute()
            
            if not card_result.data:
                return False
            
            card_data = card_result.data[0]
            
            # Create card object
            card = SpacedRepetitionCard(
                content_id=card_data['content_id'],
                content_type=card_data['content_type'],
                easiness_factor=card_data['easiness_factor'],
                interval=card_data['interval'],
                repetitions=card_data['repetitions']
            )
            
            # Update after review
            update_data = card.update_after_review(quality)
            
            # Save to database
            supabase.table('spaced_repetition_cards').update(update_data).eq('id', card_id).execute()
            
            # Record review history
            history_data = {
                'card_id': card_id,
                'user_id': self.user_id,
                'quality': quality.value,
                'reviewed_at': datetime.now().isoformat()
            }
            supabase.table('spaced_repetition_history').insert(history_data).execute()
            
            return True
        except Exception as e:
            print(f"Error recording review: {e}")
            return False
    
    def add_card(self, content_id: str, content_type: str = 'topic') -> bool:
        """Add new content to spaced repetition"""
        from app.models import get_supabase_client, SUPABASE_AVAILABLE
        
        if not SUPABASE_AVAILABLE:
            return False
        
        supabase = get_supabase_client()
        
        try:
            # Check if card already exists
            existing = supabase.table('spaced_repetition_cards').select('id').eq(
                'user_id', self.user_id
            ).eq('content_id', content_id).eq('content_type', content_type).execute()
            
            if existing.data:
                return True  # Already added
            
            card_data = {
                'user_id': self.user_id,
                'content_id': content_id,
                'content_type': content_type,
                'easiness_factor': 2.5,
                'interval': 1,
                'repetitions': 0,
                'next_review': datetime.now().isoformat()
            }
            
            result = supabase.table('spaced_repetition_cards').insert(card_data).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error adding card: {e}")
            return False
    
    def get_review_stats(self) -> Dict:
        """Get user's review statistics"""
        from app.models import get_supabase_client, SUPABASE_AVAILABLE
        
        if not SUPABASE_AVAILABLE:
            return {}
        
        supabase = get_supabase_client()
        
        try:
            # Total cards
            total_result = supabase.table('spaced_repetition_cards').select('id', count='exact').eq('user_id', self.user_id).execute()
            
            # Due today
            due_result = supabase.table('spaced_repetition_cards').select('id', count='exact').eq(
                'user_id', self.user_id
            ).lte('next_review', datetime.now().isoformat()).execute()
            
            # Mastered (repetitions >= 5)
            mastered_result = supabase.table('spaced_repetition_cards').select('id', count='exact').eq(
                'user_id', self.user_id
            ).gte('repetitions', 5).execute()
            
            # Reviews this week
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            weekly_result = supabase.table('spaced_repetition_history').select('id', count='exact').eq(
                'user_id', self.user_id
            ).gte('reviewed_at', week_ago).execute()
            
            return {
                'total_cards': total_result.count or 0,
                'due_today': due_result.count or 0,
                'mastered': mastered_result.count or 0,
                'reviewed_this_week': weekly_result.count or 0
            }
        except Exception as e:
            print(f"Error getting review stats: {e}")
            return {}
```

### Database Schema

```sql
-- supabase/migrations/021_spaced_repetition.sql

CREATE TABLE spaced_repetition_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content_id TEXT NOT NULL,
    content_type VARCHAR(50) NOT NULL, -- topic, quiz_question, flashcard
    easiness_factor DECIMAL(3,2) DEFAULT 2.5,
    interval INTEGER DEFAULT 1, -- days
    repetitions INTEGER DEFAULT 0,
    next_review TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_reviewed TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, content_id, content_type)
);

CREATE TABLE spaced_repetition_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    card_id UUID REFERENCES spaced_repetition_cards(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    quality INTEGER CHECK (quality >= 0 AND quality <= 5),
    reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sr_cards_user_due ON spaced_repetition_cards(user_id, next_review);
CREATE INDEX idx_sr_history_user ON spaced_repetition_history(user_id, reviewed_at);
```

---

## 🎯 CRITICAL FEATURE 3: Parent Portal

### Database Schema

```sql
-- supabase/migrations/022_parent_portal.sql

-- Parent accounts linked to students
CREATE TABLE parent_student_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID REFERENCES users(id) ON DELETE CASCADE,
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    relationship VARCHAR(50), -- mother, father, guardian, etc.
    access_level VARCHAR(20) DEFAULT 'read_only', -- read_only, limited
    is_primary BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(parent_id, student_id)
);

-- Parent notifications preferences
CREATE TABLE parent_notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID REFERENCES users(id) ON DELETE CASCADE,
    student_id UUID REFERENCES users(id) ON DELETE CASCADE,
    weekly_report BOOLEAN DEFAULT TRUE,
    assignment_alerts BOOLEAN DEFAULT TRUE,
    grade_alerts BOOLEAN DEFAULT TRUE,
    attendance_alerts BOOLEAN DEFAULT TRUE,
    behavior_alerts BOOLEAN DEFAULT TRUE,
    email_enabled BOOLEAN DEFAULT TRUE,
    sms_enabled BOOLEAN DEFAULT FALSE,
    UNIQUE(parent_id, student_id)
);

-- Parent-teacher messages
CREATE TABLE parent_teacher_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID REFERENCES users(id),
    teacher_id UUID REFERENCES users(id),
    student_id UUID REFERENCES users(id), -- context
    subject VARCHAR(255),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    parent_to_teacher BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Python Models

```python
# app/models/parent_portal.py

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from app.models import get_supabase_client, SUPABASE_AVAILABLE

class ParentPortal:
    """Parent access to student data"""
    
    @classmethod
    def link_parent_to_student(cls, parent_id: str, student_id: str,
                               relationship: str = 'guardian') -> bool:
        """Link a parent account to a student"""
        if not SUPABASE_AVAILABLE:
            return False
        
        supabase = get_supabase_client()
        
        try:
            link_data = {
                'parent_id': parent_id,
                'student_id': student_id,
                'relationship': relationship,
                'access_level': 'read_only',
                'is_active': True
            }
            
            result = supabase.table('parent_student_links').insert(link_data).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error linking parent to student: {e}")
            return False
    
    @classmethod
    def get_parent_children(cls, parent_id: str) -> List[Dict]:
        """Get all children linked to a parent"""
        if not SUPABASE_AVAILABLE:
            return []
        
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('parent_student_links').select(
                '*, students:users!student_id(id, email, name)'
            ).eq('parent_id', parent_id).eq('is_active', True).execute()
            
            return [
                {
                    'student_id': link['student_id'],
                    'name': link['students']['name'],
                    'email': link['students']['email'],
                    'relationship': link['relationship']
                }
                for link in result.data
            ]
        except Exception as e:
            print(f"Error getting parent children: {e}")
            return []
    
    @classmethod
    def get_child_progress_summary(cls, parent_id: str, student_id: str,
                                   days: int = 30) -> Dict:
        """Get comprehensive progress summary for a child"""
        if not SUPABASE_AVAILABLE:
            return {}
        
        # Verify access
        if not cls._verify_parent_access(parent_id, student_id):
            return {'error': 'Access denied'}
        
        from app.models.study_session import StudySession
        from app.models.gamification import UserProfile
        from app.models.classroom import Assignment
        
        # Get various metrics
        study_stats = StudySession.get_session_stats(student_id, days)
        profile = UserProfile.get_or_create_profile(student_id)
        assignments = Assignment.get_student_assignments(student_id)
        
        # Calculate assignment completion rate
        total_assignments = len(assignments)
        completed_assignments = sum(1 for a in assignments if a['status'] in ['submitted', 'graded'])
        
        return {
            'student_id': student_id,
            'period_days': days,
            'study_time_hours': study_stats.get('total_time_hours', 0),
            'study_sessions': study_stats.get('total_sessions', 0),
            'study_streak': profile.study_streak if profile else 0,
            'current_level': profile.current_level if profile else 1,
            'assignments_total': total_assignments,
            'assignments_completed': completed_assignments,
            'assignments_pending': total_assignments - completed_assignments,
            'completion_rate': round((completed_assignments / total_assignments * 100) if total_assignments > 0 else 0, 1),
            'last_active': study_stats.get('last_session_date')
        }
    
    @classmethod
    def _verify_parent_access(cls, parent_id: str, student_id: str) -> bool:
        """Verify parent has access to student data"""
        if not SUPABASE_AVAILABLE:
            return False
        
        supabase = get_supabase_client()
        
        try:
            result = supabase.table('parent_student_links').select('id').eq(
                'parent_id', parent_id
            ).eq('student_id', student_id).eq('is_active', True).execute()
            
            return bool(result.data)
        except Exception as e:
            print(f"Error verifying parent access: {e}")
            return False
    
    @classmethod
    def send_weekly_report(cls, parent_id: str, student_id: str) -> bool:
        """Generate and send weekly progress report"""
        summary = cls.get_child_progress_summary(parent_id, student_id, days=7)
        
        if 'error' in summary:
            return False
        
        # Format email
        email_html = cls._format_weekly_report_email(summary)
        
        # Send email (integrate with your email service)
        # send_email(to=parent_email, subject="Weekly Progress Report", html=email_html)
        
        return True
    
    @classmethod
    def _format_weekly_report_email(cls, summary: Dict) -> str:
        """Format weekly report as HTML email"""
        return f"""
        <h2>Weekly Progress Report</h2>
        <p>Here's how your child performed this week:</p>
        <ul>
            <li><strong>Study Time:</strong> {summary['study_time_hours']} hours</li>
            <li><strong>Study Sessions:</strong> {summary['study_sessions']}</li>
            <li><strong>Current Streak:</strong> {summary['study_streak']} days</li>
            <li><strong>Assignments Completed:</strong> {summary['assignments_completed']}/{summary['assignments_total']}</li>
            <li><strong>Completion Rate:</strong> {summary['completion_rate']}%</li>
        </ul>
        <p>Keep up the great work!</p>
        """
```

---

## 📋 NEXT STEPS

1. **Implement Classroom Management** (Week 1-4)
   - Create database migrations
   - Build models and routes
   - Design teacher/student UI
   - Test with pilot teachers

2. **Add Spaced Repetition** (Week 5-7)
   - Implement SM-2 algorithm
   - Integrate with existing quiz system
   - Create review dashboard
   - A/B test effectiveness

3. **Build Parent Portal** (Week 8-9)
   - Parent account linking
   - Progress dashboards
   - Weekly reports
   - Notification system

4. **GDPR Compliance** (Week 10-11)
   - Consent management
   - Data export/deletion
   - Privacy policy
   - Audit logs

5. **Testing & Launch** (Week 12)
   - End-to-end testing
   - Teacher training
   - Student onboarding
   - Monitor metrics

This implementation guide provides the foundation for your three most critical features. Each can be built incrementally and tested with real users before moving to the next.





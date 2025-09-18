from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, TextAreaField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError, Optional
from datetime import date, datetime

class StartSessionForm(FlaskForm):
    topic_id = SelectField('Topic', coerce=str, validators=[DataRequired(message='Please select a topic')])
    session_type = SelectField('Session Type', 
                              choices=[('review', 'Review'), ('practice', 'Practice')],
                              validators=[DataRequired(message='Please select a session type')])
    confidence_before = IntegerField('Confidence Before (1-10)', 
                                   validators=[DataRequired(message='Please rate your confidence'),
                                             NumberRange(min=1, max=10, message='Confidence must be between 1 and 10')])
    estimated_duration = IntegerField('Estimated Duration (minutes)', 
                                    validators=[Optional(), 
                                              NumberRange(min=1, max=480, message='Duration must be between 1 and 480 minutes')],
                                    default=25)
    notes = TextAreaField('Initial Notes (Optional)', 
                         validators=[Optional(), 
                                   Length(max=500, message='Initial notes cannot exceed 500 characters')],
                         render_kw={'rows': 3, 'placeholder': 'Any initial thoughts or goals for this session?'})
    submit = SubmitField('Start Session')
    
    def __init__(self, topics=None, *args, **kwargs):
        super(StartSessionForm, self).__init__(*args, **kwargs)
        if topics:
            self.topic_id.choices = [(topic.id, topic.title) for topic in topics]

class CompleteSessionForm(FlaskForm):
    duration_minutes = IntegerField('Duration (minutes)', 
                                  validators=[DataRequired(message='Please enter session duration'),
                                            NumberRange(min=1, max=480, message='Duration must be between 1 and 480 minutes')])
    confidence_after = IntegerField('Confidence After (1-10)', 
                                  validators=[DataRequired(message='Please rate your confidence after the session'),
                                            NumberRange(min=1, max=10, message='Confidence must be between 1 and 10')])
    notes = TextAreaField('Session Notes', 
                         validators=[Optional(), 
                                   Length(max=1000, message='Notes cannot exceed 1000 characters')],
                         render_kw={'rows': 4, 'placeholder': 'What did you learn? Any insights or challenges?'})
    completed = BooleanField('Mark as completed', default=True)
    submit = SubmitField('Complete Session')

class EditSessionForm(FlaskForm):
    session_date = DateField('Session Date', 
                           validators=[DataRequired(message='Please select a session date')],
                           default=date.today)
    duration_minutes = IntegerField('Duration (minutes)', 
                                  validators=[DataRequired(message='Please enter session duration'),
                                            NumberRange(min=1, max=480, message='Duration must be between 1 and 480 minutes')])
    confidence_before = IntegerField('Confidence Before (1-10)', 
                                   validators=[DataRequired(message='Please rate your confidence before'),
                                             NumberRange(min=1, max=10, message='Confidence must be between 1 and 10')])
    confidence_after = IntegerField('Confidence After (1-10)', 
                                  validators=[DataRequired(message='Please rate your confidence after'),
                                            NumberRange(min=1, max=10, message='Confidence must be between 1 and 10')])
    notes = TextAreaField('Session Notes', 
                         validators=[Optional(), 
                                   Length(max=1000, message='Notes cannot exceed 1000 characters')],
                         render_kw={'rows': 4})
    session_type = SelectField('Session Type', 
                              choices=[('review', 'Review'), ('practice', 'Practice')],
                              validators=[DataRequired(message='Please select a session type')])
    submit = SubmitField('Update Session')
    
    def validate_session_date(self, field):
        """Validate that session date is not in the future"""
        if field.data and field.data > date.today():
            raise ValidationError('Session date cannot be in the future')
    
    def validate_confidence_after(self, field):
        """Validate confidence after is reasonable compared to before"""
        if hasattr(self, 'confidence_before') and self.confidence_before.data and field.data:
            # Allow some flexibility but warn about unrealistic jumps
            diff = field.data - self.confidence_before.data
            if diff > 5:
                raise ValidationError('Confidence improvement seems unrealistic. Please verify your ratings.')
            elif diff < -3:
                raise ValidationError('Large confidence drops are unusual. Please verify your ratings.')

class SessionFilterForm(FlaskForm):
    topic_id = SelectField('Filter by Topic', coerce=lambda x: x if x else None, validators=[Optional()])
    session_type = SelectField('Filter by Type', 
                              choices=[('', 'All Types'), ('review', 'Review'), ('practice', 'Practice')],
                              validators=[Optional()])
    date_from = DateField('From Date', validators=[Optional()])
    date_to = DateField('To Date', validators=[Optional()])
    submit = SubmitField('Apply Filters')
    
    def __init__(self, topics=None, *args, **kwargs):
        super(SessionFilterForm, self).__init__(*args, **kwargs)
        if topics:
            self.topic_id.choices = [('', 'All Topics')] + [(topic.id, topic.title) for topic in topics]
    
    def validate_date_to(self, field):
        """Validate date range"""
        if self.date_from.data and field.data and field.data < self.date_from.data:
            raise ValidationError('End date must be after start date')

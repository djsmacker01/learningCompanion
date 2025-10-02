from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import datetime, timedelta


class ShareTopicForm(FlaskForm):
    """Form for sharing a topic"""
    
    expires_at = DateTimeField('Expires At (Optional)', 
        validators=[Optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Leave empty for no expiration'
        }
    )
    
    max_uses = IntegerField('Maximum Uses (Optional)', 
        validators=[Optional(), NumberRange(min=1, max=1000)],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Leave empty for unlimited uses'
        }
    )
    
    submit = SubmitField('Generate Share Code', render_kw={
        'class': 'btn btn-success'
    })


class JoinTopicForm(FlaskForm):
    """Form for joining a topic with share code"""
    
    share_code = StringField('Share Code', 
        validators=[
            DataRequired(message='Share code is required'),
            Length(min=8, max=20, message='Share code must be between 8 and 20 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter the share code',
            'autocomplete': 'off'
        }
    )
    
    submit = SubmitField('Join Topic', render_kw={
        'class': 'btn btn-primary w-100'
    })

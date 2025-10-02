from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, HiddenField, IntegerField, DateTimeLocalField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Email
from wtforms.widgets import CheckboxInput


class FriendRequestForm(FlaskForm):
    """Form for sending friend requests"""
    
    friend_email = StringField('Friend\'s Email', 
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Please enter a valid email address')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter your friend\'s email address'
        }
    )
    
    submit = SubmitField('Send Friend Request', render_kw={
        'class': 'btn btn-primary'
    })


class StudyGroupForm(FlaskForm):
    """Form for creating study groups"""
    
    name = StringField('Group Name', 
        validators=[
            DataRequired(message='Group name is required'),
            Length(min=3, max=100, message='Group name must be between 3 and 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter a name for your study group'
        }
    )
    
    description = TextAreaField('Description', 
        validators=[
            DataRequired(message='Description is required'),
            Length(min=10, max=500, message='Description must be between 10 and 500 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe what this study group is about...'
        }
    )
    
    is_public = SelectField('Visibility', 
        choices=[
            (True, 'Public - Anyone can join'),
            (False, 'Private - Invite only')
        ],
        coerce=bool,
        default=True,
        render_kw={
            'class': 'form-control'
        }
    )
    
    max_members = IntegerField('Maximum Members', 
        validators=[
            DataRequired(message='Maximum members is required'),
            NumberRange(min=2, max=100, message='Maximum members must be between 2 and 100')
        ],
        default=50,
        render_kw={
            'class': 'form-control'
        }
    )
    
    submit = SubmitField('Create Study Group', render_kw={
        'class': 'btn btn-primary'
    })


class SocialChallengeForm(FlaskForm):
    """Form for creating social challenges"""
    
    title = StringField('Challenge Title', 
        validators=[
            DataRequired(message='Title is required'),
            Length(min=5, max=200, message='Title must be between 5 and 200 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter a title for your challenge'
        }
    )
    
    description = TextAreaField('Description', 
        validators=[
            DataRequired(message='Description is required'),
            Length(min=10, max=1000, message='Description must be between 10 and 1000 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe the challenge and its goals...'
        }
    )
    
    challenge_type = SelectField('Challenge Type', 
        choices=[
            ('study_time', 'Study Time - Total minutes studied'),
            ('streak', 'Study Streak - Consecutive days'),
            ('quiz_score', 'Quiz Score - Average quiz performance'),
            ('topic_completion', 'Topic Completion - Number of topics completed')
        ],
        validators=[DataRequired(message='Challenge type is required')],
        render_kw={
            'class': 'form-control'
        }
    )
    
    target_value = IntegerField('Target Value', 
        validators=[
            DataRequired(message='Target value is required'),
            NumberRange(min=1, max=10000, message='Target value must be between 1 and 10000')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter the target number'
        }
    )
    
    target_unit = StringField('Target Unit', 
        validators=[
            DataRequired(message='Target unit is required'),
            Length(min=1, max=20, message='Unit must be between 1 and 20 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'e.g., minutes, days, score, topics'
        }
    )
    
    start_date = DateTimeLocalField('Start Date', 
        validators=[DataRequired(message='Start date is required')],
        render_kw={
            'class': 'form-control'
        }
    )
    
    end_date = DateTimeLocalField('End Date', 
        validators=[DataRequired(message='End date is required')],
        render_kw={
            'class': 'form-control'
        }
    )
    
    submit = SubmitField('Create Challenge', render_kw={
        'class': 'btn btn-primary'
    })


class ShareAchievementForm(FlaskForm):
    """Form for sharing achievements"""
    
    achievement_type = SelectField('Achievement Type', 
        choices=[
            ('badge_earned', 'Badge Earned'),
            ('level_up', 'Level Up'),
            ('streak_milestone', 'Streak Milestone'),
            ('challenge_completed', 'Challenge Completed'),
            ('study_goal', 'Study Goal Achieved')
        ],
        validators=[DataRequired(message='Achievement type is required')],
        render_kw={
            'class': 'form-control'
        }
    )
    
    achievement_title = StringField('Achievement Title', 
        validators=[
            DataRequired(message='Title is required'),
            Length(min=5, max=100, message='Title must be between 5 and 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter a title for your achievement'
        }
    )
    
    achievement_description = TextAreaField('Description', 
        validators=[
            DataRequired(message='Description is required'),
            Length(min=10, max=500, message='Description must be between 10 and 500 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe your achievement...'
        }
    )
    
    share_with_friends = BooleanField('Share with Friends', 
        default=True,
        render_kw={
            'class': 'form-check-input'
        }
    )
    
    share_with_groups = BooleanField('Share with Study Groups', 
        default=False,
        render_kw={
            'class': 'form-check-input'
        }
    )
    
    submit = SubmitField('Share Achievement', render_kw={
        'class': 'btn btn-success'
    })


class StudySessionSocialForm(FlaskForm):
    """Form for sharing study sessions"""
    
    is_public = BooleanField('Make Session Public', 
        default=False,
        render_kw={
            'class': 'form-check-input'
        }
    )
    
    share_with_friends = BooleanField('Share with Friends', 
        default=True,
        render_kw={
            'class': 'form-check-input'
        }
    )
    
    share_with_groups = BooleanField('Share with Study Groups', 
        default=False,
        render_kw={
            'class': 'form-check-input'
        }
    )
    
    group_id = SelectField('Study Group', 
        choices=[],  # Will be populated dynamically
        validators=[Optional()],
        render_kw={
            'class': 'form-control'
        }
    )
    
    session_message = TextAreaField('Message', 
        validators=[
            Optional(),
            Length(max=200, message='Message must be less than 200 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Optional message about your study session...'
        }
    )
    
    submit = SubmitField('Share Session', render_kw={
        'class': 'btn btn-primary'
    })


class SocialSearchForm(FlaskForm):
    """Form for searching social content"""
    
    query = StringField('Search', 
        validators=[
            Optional(),
            Length(min=1, max=100, message='Search query must be between 1 and 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Search friends, groups, challenges...'
        }
    )
    
    search_type = SelectField('Search Type', 
        choices=[
            ('all', 'All'),
            ('friends', 'Friends'),
            ('groups', 'Study Groups'),
            ('challenges', 'Challenges')
        ],
        default='all',
        render_kw={
            'class': 'form-control'
        }
    )
    
    submit = SubmitField('Search', render_kw={
        'class': 'btn btn-primary'
    })


class GroupInviteForm(FlaskForm):
    """Form for inviting users to study groups"""
    
    invite_email = StringField('Email Address', 
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Please enter a valid email address')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter email address to invite'
        }
    )
    
    message = TextAreaField('Invitation Message', 
        validators=[
            Optional(),
            Length(max=300, message='Message must be less than 300 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional personal message...'
        }
    )
    
    submit = SubmitField('Send Invitation', render_kw={
        'class': 'btn btn-primary'
    })


class ChallengeProgressForm(FlaskForm):
    """Form for updating challenge progress"""
    
    challenge_id = HiddenField('Challenge ID')
    
    progress = IntegerField('Current Progress', 
        validators=[
            DataRequired(message='Progress is required'),
            NumberRange(min=0, message='Progress cannot be negative')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter your current progress'
        }
    )
    
    submit = SubmitField('Update Progress', render_kw={
        'class': 'btn btn-success'
    })

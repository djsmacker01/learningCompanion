from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.widgets import CheckboxInput, ListWidget


class TopicNoteForm(FlaskForm):
    """Form for creating/editing topic notes"""
    
    title = StringField('Note Title', 
        validators=[
            DataRequired(message='Title is required'),
            Length(min=1, max=255, message='Title must be between 1 and 255 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter a title for this note'
        }
    )
    
    content = TextAreaField('Note Content', 
        validators=[
            DataRequired(message='Content is required'),
            Length(min=1, message='Content cannot be empty')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Enter your note content here...'
        }
    )
    
    note_type = SelectField('Note Type', 
        choices=[
            ('general', 'General Note'),
            ('summary', 'Summary'),
            ('key_points', 'Key Points'),
            ('questions', 'Questions'),
            ('resources', 'Resources')
        ],
        default='general',
        render_kw={
            'class': 'form-control'
        }
    )
    
    is_public = SelectField('Visibility', 
        choices=[
            (False, 'Private'),
            (True, 'Public')
        ],
        coerce=bool,
        default=False,
        render_kw={
            'class': 'form-control'
        }
    )
    
    submit = SubmitField('Save Note', render_kw={
        'class': 'btn btn-primary'
    })


class TopicAttachmentForm(FlaskForm):
    """Form for uploading topic attachments"""
    
    file = FileField('File', 
        validators=[
            DataRequired(message='Please select a file'),
            FileAllowed(['pdf', 'doc', 'docx', 'txt', 'md', 'jpg', 'jpeg', 'png', 'gif', 'mp4', 'mp3', 'zip'], 
                       'Only PDF, Word, text, image, video, audio, and archive files are allowed')
        ],
        render_kw={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.txt,.md,.jpg,.jpeg,.png,.gif,.mp4,.mp3,.zip'
        }
    )
    
    description = TextAreaField('Description', 
        validators=[
            Optional(),
            Length(max=500, message='Description must be less than 500 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional description of the file'
        }
    )
    
    is_public = SelectField('Visibility', 
        choices=[
            (False, 'Private'),
            (True, 'Public')
        ],
        coerce=bool,
        default=False,
        render_kw={
            'class': 'form-control'
        }
    )
    
    submit = SubmitField('Upload File', render_kw={
        'class': 'btn btn-primary'
    })


class TopicTagForm(FlaskForm):
    """Form for managing topic tags"""
    
    tags = SelectMultipleField('Tags', 
        choices=[],  # Will be populated dynamically
        render_kw={
            'class': 'form-control',
            'multiple': True,
            'size': 8
        }
    )
    
    new_tag = StringField('Add New Tag', 
        validators=[
            Optional(),
            Length(min=1, max=50, message='Tag name must be between 1 and 50 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter new tag name'
        }
    )
    
    submit = SubmitField('Update Tags', render_kw={
        'class': 'btn btn-primary'
    })


class TopicContentForm(FlaskForm):
    """Form for updating topic content"""
    
    title = StringField('Title', 
        validators=[
            DataRequired(message='Title is required'),
            Length(min=1, max=200, message='Title must be between 1 and 200 characters')
        ],
        render_kw={
            'class': 'form-control'
        }
    )
    
    description = TextAreaField('Description', 
        validators=[
            DataRequired(message='Description is required'),
            Length(min=10, max=1000, message='Description must be between 10 and 1000 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 4
        }
    )
    
    notes = TextAreaField('Quick Notes', 
        validators=[
            Optional(),
            Length(max=2000, message='Notes must be less than 2000 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add quick notes about this topic...'
        }
    )
    
    tags = SelectMultipleField('Tags', 
        choices=[],  # Will be populated dynamically
        render_kw={
            'class': 'form-control',
            'multiple': True,
            'size': 5
        }
    )
    
    change_summary = StringField('Change Summary', 
        validators=[
            Optional(),
            Length(max=200, message='Change summary must be less than 200 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Optional: Describe what you changed'
        }
    )
    
    submit = SubmitField('Update Topic', render_kw={
        'class': 'btn btn-primary'
    })


class TopicVersionForm(FlaskForm):
    """Form for restoring topic versions"""
    
    version_number = HiddenField('Version Number')
    
    submit = SubmitField('Restore This Version', render_kw={
        'class': 'btn btn-warning',
        'onclick': 'return confirm("Are you sure you want to restore this version? This will create a new version with the restored content.")'
    })


class ContentSearchForm(FlaskForm):
    """Form for searching content"""
    
    query = StringField('Search', 
        validators=[
            Optional(),
            Length(min=1, max=100, message='Search query must be between 1 and 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Search topics, notes, and content...'
        }
    )
    
    tags = SelectMultipleField('Filter by Tags', 
        choices=[],  # Will be populated dynamically
        render_kw={
            'class': 'form-control',
            'multiple': True,
            'size': 4
        }
    )
    
    content_type = SelectField('Content Type', 
        choices=[
            ('all', 'All Content'),
            ('topics', 'Topics Only'),
            ('notes', 'Notes Only'),
            ('attachments', 'Attachments Only')
        ],
        default='all',
        render_kw={
            'class': 'form-control'
        }
    )
    
    submit = SubmitField('Search', render_kw={
        'class': 'btn btn-primary'
    })

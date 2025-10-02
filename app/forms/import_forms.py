from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length, Optional


class CSVImportForm(FlaskForm):
    """Form for importing topics from CSV"""
    
    csv_file = FileField('CSV File', 
        validators=[
            DataRequired(message='Please select a CSV file'),
            FileAllowed(['csv'], 'Only CSV files are allowed')
        ],
        render_kw={
            'class': 'form-control',
            'accept': '.csv'
        }
    )
    
    submit = SubmitField('Import Topics', render_kw={
        'class': 'btn btn-primary'
    })


class BulkTopicForm(FlaskForm):
    """Form for creating multiple topics at once"""
    
    topics_data = TextAreaField('Topics Data (one per line)', 
        validators=[
            DataRequired(message='Please enter topic data'),
            Length(min=10, message='Please enter at least one topic')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Enter topics in the format: Title|Description\nExample:\nPython Basics|Learn the fundamentals of Python programming\nData Structures|Study arrays, lists, and trees'
        }
    )
    
    submit = SubmitField('Create Topics', render_kw={
        'class': 'btn btn-success'
    })


class FileUploadForm(FlaskForm):
    """Form for uploading study materials"""
    
    file = FileField('Study Material', 
        validators=[
            DataRequired(message='Please select a file'),
            FileAllowed(['pdf', 'doc', 'docx', 'txt', 'md'], 'Only PDF, Word, text, and Markdown files are allowed')
        ],
        render_kw={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.txt,.md'
        }
    )
    
    title = StringField('Title', 
        validators=[
            DataRequired(message='Title is required'),
            Length(min=1, max=200, message='Title must be between 1 and 200 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter a title for this material'
        }
    )
    
    description = TextAreaField('Description', 
        validators=[
            Optional(),
            Length(max=1000, message='Description must be less than 1000 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional description of the material'
        }
    )
    
    submit = SubmitField('Upload Material', render_kw={
        'class': 'btn btn-primary'
    })

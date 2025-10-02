from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.widgets import TextArea

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    subject = SelectField('Subject', validators=[DataRequired()], choices=[
        ('', 'Select a subject'),
        ('general', 'General Inquiry'),
        ('technical', 'Technical Support'),
        ('billing', 'Billing Question'),
        ('feature', 'Feature Request'),
        ('bug', 'Bug Report'),
        ('account', 'Account Issue'),
        ('other', 'Other')
    ])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)], 
                          widget=TextArea(), render_kw={'rows': 6})
    attachments = FileField('Attachments (Optional)', validators=[Optional()])
    newsletter = BooleanField('Subscribe to newsletter for updates and tips')

class SupportTicketForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)], 
                          widget=TextArea(), render_kw={'rows': 6})
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('', 'Select a category'),
        ('technical', 'Technical Issue'),
        ('billing', 'Billing Question'),
        ('feature', 'Feature Request'),
        ('bug', 'Bug Report'),
        ('account', 'Account Issue'),
        ('privacy', 'Privacy Concern'),
        ('other', 'Other')
    ])

class DataExportForm(FlaskForm):
    data_types = SelectField('Data Types to Export', validators=[DataRequired()], choices=[
        ('all', 'All Data'),
        ('profile', 'Profile Information'),
        ('sessions', 'Study Sessions'),
        ('topics', 'Topics and Content'),
        ('social', 'Social Data'),
        ('analytics', 'Analytics Data')
    ])
    format = SelectField('Export Format', choices=[
        ('json', 'JSON'),
        ('csv', 'CSV'),
        ('xml', 'XML')
    ], default='json')
    include_attachments = BooleanField('Include file attachments')

class DataDeletionForm(FlaskForm):
    confirmation = BooleanField('I understand that this action cannot be undone', validators=[DataRequired()])
    reason = SelectField('Reason for Deletion', validators=[DataRequired()], choices=[
        ('', 'Select a reason'),
        ('privacy', 'Privacy concerns'),
        ('no_longer_needed', 'No longer need the service'),
        ('found_alternative', 'Found an alternative service'),
        ('technical_issues', 'Technical issues'),
        ('other', 'Other')
    ])
    feedback = TextAreaField('Additional Feedback (Optional)', 
                           widget=TextArea(), render_kw={'rows': 4})

class FeedbackForm(FlaskForm):
    rating = SelectField('Overall Rating', validators=[DataRequired()], choices=[
        ('', 'Select a rating'),
        ('5', 'Excellent'),
        ('4', 'Good'),
        ('3', 'Average'),
        ('2', 'Poor'),
        ('1', 'Very Poor')
    ])
    category = SelectField('Feedback Category', validators=[DataRequired()], choices=[
        ('', 'Select a category'),
        ('general', 'General Feedback'),
        ('feature', 'Feature Request'),
        ('bug', 'Bug Report'),
        ('ui', 'User Interface'),
        ('performance', 'Performance'),
        ('mobile', 'Mobile Experience'),
        ('accessibility', 'Accessibility')
    ])
    message = TextAreaField('Your Feedback', validators=[DataRequired(), Length(min=10, max=1000)], 
                          widget=TextArea(), render_kw={'rows': 5})
    anonymous = BooleanField('Submit anonymously')

class ReportIssueForm(FlaskForm):
    issue_type = SelectField('Issue Type', validators=[DataRequired()], choices=[
        ('', 'Select an issue type'),
        ('bug', 'Bug or Error'),
        ('performance', 'Performance Issue'),
        ('ui', 'User Interface Problem'),
        ('accessibility', 'Accessibility Issue'),
        ('security', 'Security Concern'),
        ('other', 'Other')
    ])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)], 
                              widget=TextArea(), render_kw={'rows': 5})
    steps_to_reproduce = TextAreaField('Steps to Reproduce (if applicable)', 
                                     widget=TextArea(), render_kw={'rows': 4})
    browser = StringField('Browser and Version', validators=[Optional()])
    device = StringField('Device and OS', validators=[Optional()])
    screenshots = FileField('Screenshots (Optional)', validators=[Optional()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium')


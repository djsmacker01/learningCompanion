from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class TopicForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=1, max=100, message='Title must be between 1 and 100 characters')
    ])
    
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(min=10, max=1000, message='Description must be between 10 and 1000 characters')
    ])
    
    submit = SubmitField('Save Topic')
    
    def validate_title(self, title):
        """Custom validation for title"""
        if title.data and title.data.strip() == '':
            raise ValidationError('Title cannot be empty or only whitespace')
    
    def validate_description(self, description):
        """Custom validation for description"""
        if description.data and description.data.strip() == '':
            raise ValidationError('Description cannot be empty or only whitespace')

# Import session forms
from .session_forms import StartSessionForm, CompleteSessionForm, EditSessionForm, SessionFilterForm

# Import auth forms
from .auth_forms import (
    LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm,
    ForgotPasswordForm, ResetPasswordForm
)

# Import sharing forms
from .sharing_forms import ShareTopicForm, JoinTopicForm

# Import import forms
from .import_forms import CSVImportForm, BulkTopicForm, FileUploadForm

# Import content management forms
from .content_forms import (
    TopicNoteForm, TopicAttachmentForm, TopicTagForm, 
    TopicContentForm, TopicVersionForm, ContentSearchForm
)

# Import social features forms
from .social_forms import (
    FriendRequestForm, StudyGroupForm, SocialChallengeForm, ShareAchievementForm,
    StudySessionSocialForm, SocialSearchForm, GroupInviteForm, ChallengeProgressForm
)

# Import mobile and accessibility forms
from .mobile_accessibility_forms import (
    AccessibilityPreferencesForm, MobilePreferencesForm, DeviceRegistrationForm,
    OfflineDataForm, AccessibilityTestForm, SyncStatusForm
)

# Import support forms
from .support_forms import (
    ContactForm, SupportTicketForm, DataExportForm, DataDeletionForm, 
    FeedbackForm, ReportIssueForm
)


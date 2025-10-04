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
        
        if title.data and title.data.strip() == '':
            raise ValidationError('Title cannot be empty or only whitespace')
    
    def validate_description(self, description):
        
        if description.data and description.data.strip() == '':
            raise ValidationError('Description cannot be empty or only whitespace')


from .session_forms import StartSessionForm, CompleteSessionForm, EditSessionForm, SessionFilterForm


from .auth_forms import (
    LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm,
    ForgotPasswordForm, ResetPasswordForm
)


from .sharing_forms import ShareTopicForm, JoinTopicForm


from .import_forms import CSVImportForm, BulkTopicForm, FileUploadForm


from .content_forms import (
    TopicNoteForm, TopicAttachmentForm, TopicTagForm, 
    TopicContentForm, TopicVersionForm, ContentSearchForm
)


from .social_forms import (
    FriendRequestForm, StudyGroupForm, SocialChallengeForm, ShareAchievementForm,
    StudySessionSocialForm, SocialSearchForm, GroupInviteForm, ChallengeProgressForm
)


from .mobile_accessibility_forms import (
    AccessibilityPreferencesForm, MobilePreferencesForm, DeviceRegistrationForm,
    OfflineDataForm, AccessibilityTestForm, SyncStatusForm
)


from .support_forms import (
    ContactForm, SupportTicketForm, DataExportForm, DataDeletionForm, 
    FeedbackForm, ReportIssueForm
)



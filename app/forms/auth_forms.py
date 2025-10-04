
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from wtforms.widgets import TextArea
import re


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'autocomplete': 'email'
    })
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters long')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your password',
        'autocomplete': 'current-password'
    })
    
    remember_me = BooleanField('Remember Me', render_kw={
        'class': 'form-check-input'
    })
    
    submit = SubmitField('Sign In', render_kw={
        'class': 'btn btn-primary w-100'
    })


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=255, message='Email is too long')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'autocomplete': 'email'
    })
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        Length(max=128, message='Password is too long')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Create a password',
        'autocomplete': 'new-password'
    })
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Confirm your password',
        'autocomplete': 'new-password'
    })
    
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=1, max=100, message='First name must be between 1 and 100 characters')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your first name',
        'autocomplete': 'given-name'
    })
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=1, max=100, message='Last name must be between 1 and 100 characters')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your last name',
        'autocomplete': 'family-name'
    })
    
    bio = TextAreaField('Bio (Optional)', validators=[
        Optional(),
        Length(max=500, message='Bio must be less than 500 characters')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Tell us about yourself...',
        'rows': 3
    })
    
    timezone = SelectField('Timezone', validators=[
        DataRequired(message='Please select your timezone')
    ], choices=[
        ('UTC', 'UTC (Coordinated Universal Time)'),
        ('America/New_York', 'Eastern Time (ET)'),
        ('America/Chicago', 'Central Time (CT)'),
        ('America/Denver', 'Mountain Time (MT)'),
        ('America/Los_Angeles', 'Pacific Time (PT)'),
        ('Europe/London', 'London (GMT)'),
        ('Europe/Paris', 'Paris (CET)'),
        ('Europe/Berlin', 'Berlin (CET)'),
        ('Asia/Tokyo', 'Tokyo (JST)'),
        ('Asia/Shanghai', 'Shanghai (CST)'),
        ('Asia/Kolkata', 'Mumbai (IST)'),
        ('Australia/Sydney', 'Sydney (AEST)')
    ], render_kw={
        'class': 'form-select'
    })
    
    language = SelectField('Language', validators=[
        DataRequired(message='Please select your language')
    ], choices=[
        ('en', 'English'),
        ('es', 'Español'),
        ('fr', 'Français'),
        ('de', 'Deutsch'),
        ('it', 'Italiano'),
        ('pt', 'Português'),
        ('ru', 'Русский'),
        ('ja', '日本語'),
        ('ko', '한국어'),
        ('zh', '中文')
    ], render_kw={
        'class': 'form-select'
    })
    
    email_notifications = BooleanField('Email Notifications', default=True, render_kw={
        'class': 'form-check-input'
    })
    
    study_reminders = BooleanField('Study Reminders', default=True, render_kw={
        'class': 'form-check-input'
    })
    
    submit = SubmitField('Create Account', render_kw={
        'class': 'btn btn-success w-100'
    })
    
    def validate_password(self, field):
        password = field.data
        
        weak_passwords = ['password', '123456', '123456789', 'qwerty', 'abc123', 'password123']
        if password.lower() in weak_passwords:
            raise ValidationError('This password is too common. Please choose a stronger password.')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character.')


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=1, max=100, message='First name must be between 1 and 100 characters')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your first name'
    })
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=1, max=100, message='Last name must be between 1 and 100 characters')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your last name'
    })
    
    bio = TextAreaField('Bio', validators=[
        Optional(),
        Length(max=500, message='Bio must be less than 500 characters')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Tell us about yourself...',
        'rows': 3
    })
    
    timezone = SelectField('Timezone', validators=[
        DataRequired(message='Please select your timezone')
    ], choices=[
        ('UTC', 'UTC (Coordinated Universal Time)'),
        ('America/New_York', 'Eastern Time (ET)'),
        ('America/Chicago', 'Central Time (CT)'),
        ('America/Denver', 'Mountain Time (MT)'),
        ('America/Los_Angeles', 'Pacific Time (PT)'),
        ('Europe/London', 'London (GMT)'),
        ('Europe/Paris', 'Paris (CET)'),
        ('Europe/Berlin', 'Berlin (CET)'),
        ('Asia/Tokyo', 'Tokyo (JST)'),
        ('Asia/Shanghai', 'Shanghai (CST)'),
        ('Asia/Kolkata', 'Mumbai (IST)'),
        ('Australia/Sydney', 'Sydney (AEST)')
    ], render_kw={
        'class': 'form-select'
    })
    
    language = SelectField('Language', validators=[
        DataRequired(message='Please select your language')
    ], choices=[
        ('en', 'English'),
        ('es', 'Español'),
        ('fr', 'Français'),
        ('de', 'Deutsch'),
        ('it', 'Italiano'),
        ('pt', 'Português'),
        ('ru', 'Русский'),
        ('ja', '日本語'),
        ('ko', '한국어'),
        ('zh', '中文')
    ], render_kw={
        'class': 'form-select'
    })
    
    email_notifications = BooleanField('Email Notifications', render_kw={
        'class': 'form-check-input'
    })
    
    sms_notifications = BooleanField('SMS Notifications', render_kw={
        'class': 'form-check-input'
    })
    
    study_reminders = BooleanField('Study Reminders', render_kw={
        'class': 'form-check-input'
    })
    
    privacy_level = SelectField('Privacy Level', validators=[
        DataRequired(message='Please select your privacy level')
    ], choices=[
        ('private', 'Private - Only I can see my data'),
        ('friends', 'Friends - Share with study partners'),
        ('public', 'Public - Share with everyone')
    ], render_kw={
        'class': 'form-select'
    })
    
    submit = SubmitField('Update Profile', render_kw={
        'class': 'btn btn-primary'
    })


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your current password',
        'autocomplete': 'current-password'
    })
    
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        Length(max=128, message='Password is too long')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your new password',
        'autocomplete': 'new-password'
    })
    
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'),
        EqualTo('new_password', message='Passwords must match')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Confirm your new password',
        'autocomplete': 'new-password'
    })
    
    submit = SubmitField('Change Password', render_kw={
        'class': 'btn btn-warning'
    })
    
    def validate_new_password(self, field):
        password = field.data
        
        weak_passwords = ['password', '123456', '123456789', 'qwerty', 'abc123', 'password123']
        if password.lower() in weak_passwords:
            raise ValidationError('This password is too common. Please choose a stronger password.')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character.')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
        'autocomplete': 'email'
    })
    
    submit = SubmitField('Send Reset Link', render_kw={
        'class': 'btn btn-primary w-100'
    })


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=8, message='Password must be at least 8 characters long'),
        Length(max=128, message='Password is too long')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter your new password',
        'autocomplete': 'new-password'
    })
    
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'),
        EqualTo('new_password', message='Passwords must match')
    ], render_kw={
        'class': 'form-control',
        'placeholder': 'Confirm your new password',
        'autocomplete': 'new-password'
    })
    
    submit = SubmitField('Reset Password', render_kw={
        'class': 'btn btn-success w-100'
    })
    
    def validate_new_password(self, field):
        password = field.data
        
        weak_passwords = ['password', '123456', '123456789', 'qwerty', 'abc123', 'password123']
        if password.lower() in weak_passwords:
            raise ValidationError('This password is too common. Please choose a stronger password.')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character.')


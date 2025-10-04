from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, IntegerField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Length


class AccessibilityPreferencesForm(FlaskForm):
    
    
    screen_reader_enabled = BooleanField('Enable Screen Reader Support', 
        default=False,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'screenReaderHelp'
        }
    )
    
    high_contrast_mode = BooleanField('High Contrast Mode', 
        default=False,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'highContrastHelp'
        }
    )
    
    text_size = SelectField('Text Size', 
        choices=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large'),
            ('extra-large', 'Extra Large')
        ],
        default='medium',
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'aria-describedby': 'textSizeHelp'
        }
    )
    
    keyboard_navigation = BooleanField('Enable Keyboard Navigation', 
        default=True,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'keyboardNavHelp'
        }
    )
    
    reduced_motion = BooleanField('Reduce Motion', 
        default=False,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'reducedMotionHelp'
        }
    )
    
    color_blind_friendly = BooleanField('Color Blind Friendly Mode', 
        default=False,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'colorBlindHelp'
        }
    )
    
    focus_indicators = BooleanField('Enhanced Focus Indicators', 
        default=True,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'focusIndicatorsHelp'
        }
    )
    
    submit = SubmitField('Save Accessibility Preferences', render_kw={
        'class': 'btn btn-primary'
    })


class MobilePreferencesForm(FlaskForm):
    
    
    offline_mode = BooleanField('Enable Offline Mode', 
        default=False,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'offlineModeHelp'
        }
    )
    
    auto_sync = BooleanField('Auto Sync', 
        default=True,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'autoSyncHelp'
        }
    )
    
    sync_frequency = IntegerField('Sync Frequency (minutes)', 
        validators=[
            DataRequired(message='Sync frequency is required'),
            NumberRange(min=1, max=1440, message='Sync frequency must be between 1 and 1440 minutes')
        ],
        default=15,
        render_kw={
            'class': 'form-control',
            'aria-describedby': 'syncFreqHelp'
        }
    )
    
    data_usage_limit = IntegerField('Daily Data Usage Limit (MB)', 
        validators=[
            DataRequired(message='Data usage limit is required'),
            NumberRange(min=1, max=10000, message='Data usage limit must be between 1 and 10000 MB')
        ],
        default=100,
        render_kw={
            'class': 'form-control',
            'aria-describedby': 'dataUsageHelp'
        }
    )
    
    push_notifications = BooleanField('Push Notifications', 
        default=True,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'pushNotifHelp'
        }
    )
    
    vibration_enabled = BooleanField('Vibration', 
        default=True,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'vibrationHelp'
        }
    )
    
    haptic_feedback = BooleanField('Haptic Feedback', 
        default=True,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'hapticHelp'
        }
    )
    
    submit = SubmitField('Save Mobile Preferences', render_kw={
        'class': 'btn btn-primary'
    })


class DeviceRegistrationForm(FlaskForm):
    
    
    device_name = StringField('Device Name', 
        validators=[
            DataRequired(message='Device name is required'),
            Length(min=1, max=100, message='Device name must be between 1 and 100 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter a name for this device',
            'aria-describedby': 'deviceNameHelp'
        }
    )
    
    device_type = SelectField('Device Type', 
        choices=[
            ('mobile', 'Mobile Phone'),
            ('tablet', 'Tablet'),
            ('desktop', 'Desktop Computer'),
            ('laptop', 'Laptop')
        ],
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'aria-describedby': 'deviceTypeHelp'
        }
    )
    
    submit = SubmitField('Register Device', render_kw={
        'class': 'btn btn-primary'
    })


class OfflineDataForm(FlaskForm):
    
    
    data_type = SelectField('Data Type', 
        choices=[
            ('topics', 'Topics'),
            ('sessions', 'Study Sessions'),
            ('notes', 'Notes'),
            ('attachments', 'Attachments'),
            ('all', 'All Data')
        ],
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'aria-describedby': 'dataTypeHelp'
        }
    )
    
    action = SelectField('Action', 
        choices=[
            ('download', 'Download for Offline'),
            ('clear', 'Clear Cache'),
            ('sync', 'Sync with Server')
        ],
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'aria-describedby': 'actionHelp'
        }
    )
    
    submit = SubmitField('Execute Action', render_kw={
        'class': 'btn btn-primary'
    })


class AccessibilityTestForm(FlaskForm):
    
    
    test_type = SelectField('Test Type', 
        choices=[
            ('screen_reader', 'Screen Reader Test'),
            ('keyboard_navigation', 'Keyboard Navigation Test'),
            ('color_contrast', 'Color Contrast Test'),
            ('text_scaling', 'Text Scaling Test'),
            ('focus_management', 'Focus Management Test')
        ],
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'aria-describedby': 'testTypeHelp'
        }
    )
    
    test_description = TextAreaField('Test Description', 
        validators=[
            Optional(),
            Length(max=500, message='Description must be less than 500 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe what you want to test...',
            'aria-describedby': 'testDescHelp'
        }
    )
    
    submit = SubmitField('Run Test', render_kw={
        'class': 'btn btn-warning'
    })


class SyncStatusForm(FlaskForm):
    
    
    device_id = StringField('Device ID', 
        validators=[
            DataRequired(message='Device ID is required'),
            Length(min=1, max=255, message='Device ID must be between 1 and 255 characters')
        ],
        render_kw={
            'class': 'form-control',
            'readonly': True,
            'aria-describedby': 'deviceIdHelp'
        }
    )
    
    force_sync = BooleanField('Force Sync Now', 
        default=False,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'forceSyncHelp'
        }
    )
    
    clear_cache = BooleanField('Clear Local Cache', 
        default=False,
        render_kw={
            'class': 'form-check-input',
            'aria-describedby': 'clearCacheHelp'
        }
    )
    
    submit = SubmitField('Update Sync Status', render_kw={
        'class': 'btn btn-primary'
    })


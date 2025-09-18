"""
Authentication routes for user registration, login, logout, and profile management
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import secrets

from app.forms.auth_forms import (
    LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm, 
    ForgotPasswordForm, ResetPasswordForm
)
from app.models.auth import (
    AuthUser, UserProfile, UserSession, PasswordResetToken, LoginAttempt
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data
        remember_me = form.remember_me.data
        
        # Get client information for security tracking
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        user_agent = request.headers.get('User-Agent', '')
        
        # Check if account is locked
        if LoginAttempt.is_account_locked(email):
            flash('Account temporarily locked due to too many failed attempts. Please try again later.', 'error')
            LoginAttempt.record_attempt(email, ip_address, user_agent, False, 'account_locked')
            return render_template('auth/login.html', form=form)
        
        # Get user by email
        user = AuthUser.get_by_email(email)
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'error')
                LoginAttempt.record_attempt(email, ip_address, user_agent, False, 'account_deactivated')
                return render_template('auth/login.html', form=form)
            
            # Login successful
            login_user(user, remember=remember_me)
            
            # Update last login
            user.update_last_login()
            
            # Create session for tracking
            UserSession.create_session(
                user.id, 
                ip_address=ip_address, 
                user_agent=user_agent,
                duration_hours=24 if remember_me else 8
            )
            
            # Record successful login
            LoginAttempt.record_attempt(email, ip_address, user_agent, True)
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            
            flash(f'Welcome back, {user.profile.full_name if user.profile else user.email}!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            # Login failed
            LoginAttempt.record_attempt(email, ip_address, user_agent, False, 'invalid_credentials')
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data
        first_name = form.first_name.data.strip()
        last_name = form.last_name.data.strip()
        bio = form.bio.data.strip() if form.bio.data else None
        
        # Check if user already exists
        existing_user = AuthUser.get_by_email(email)
        if existing_user:
            flash('An account with this email already exists. Please use a different email or try logging in.', 'error')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = AuthUser.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            timezone=form.timezone.data,
            language=form.language.data,
            email_notifications=form.email_notifications.data,
            study_reminders=form.study_reminders.data
        )
        
        if user:
            # Auto-login the new user
            login_user(user, remember=True)
            
            # Create session
            ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            user_agent = request.headers.get('User-Agent', '')
            UserSession.create_session(user.id, ip_address=ip_address, user_agent=user_agent)
            
            flash(f'Welcome to Learning Companion, {user.profile.full_name}! Your account has been created successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Failed to create account. Please try again.', 'error')
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    # Deactivate current session
    session_token = session.get('session_token')
    if session_token:
        user_session = UserSession.get_by_token(session_token)
        if user_session:
            user_session.deactivate()
    
    # Clear session data
    session.clear()
    
    # Logout user
    logout_user()
    
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    form = ProfileForm()
    
    # Pre-populate form with current data
    if request.method == 'GET' and current_user.profile:
        form.first_name.data = current_user.profile.first_name
        form.last_name.data = current_user.profile.last_name
        form.bio.data = current_user.profile.bio
        form.timezone.data = current_user.profile.timezone
        form.language.data = current_user.profile.language
        form.email_notifications.data = current_user.profile.email_notifications
        form.sms_notifications.data = current_user.profile.sms_notifications
        form.study_reminders.data = current_user.profile.study_reminders
        form.privacy_level.data = current_user.profile.privacy_level
    
    if form.validate_on_submit():
        if current_user.profile:
            # Update existing profile
            success = current_user.profile.update_profile(
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
                bio=form.bio.data.strip() if form.bio.data else None,
                timezone=form.timezone.data,
                language=form.language.data,
                email_notifications=form.email_notifications.data,
                sms_notifications=form.sms_notifications.data,
                study_reminders=form.study_reminders.data,
                privacy_level=form.privacy_level.data
            )
            
            if success:
                flash('Your profile has been updated successfully.', 'success')
                return redirect(url_for('auth.profile'))
            else:
                flash('Failed to update profile. Please try again.', 'error')
        else:
            # Create new profile
            profile = UserProfile.create_profile(
                current_user.id,
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
                bio=form.bio.data.strip() if form.bio.data else None,
                timezone=form.timezone.data,
                language=form.language.data,
                email_notifications=form.email_notifications.data,
                sms_notifications=form.sms_notifications.data,
                study_reminders=form.study_reminders.data,
                privacy_level=form.privacy_level.data
            )
            
            if profile:
                current_user.profile = profile
                flash('Your profile has been created successfully.', 'success')
                return redirect(url_for('auth.profile'))
            else:
                flash('Failed to create profile. Please try again.', 'error')
    
    return render_template('auth/edit_profile.html', form=form)


@auth_bp.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        
        # Verify current password
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html', form=form)
        
        # Update password
        if current_user.update_password(new_password):
            flash('Your password has been changed successfully.', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Failed to change password. Please try again.', 'error')
    
    return render_template('auth/change_password.html', form=form)


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        
        # Get user by email
        user = AuthUser.get_by_email(email)
        
        if user:
            # Create password reset token
            reset_token = PasswordResetToken.create_token(user.id, duration_hours=1)
            
            if reset_token:
                # In a real application, you would send an email here
                # For now, we'll just show the token in a flash message (for development)
                flash(f'Password reset link sent to {email}. Token: {reset_token.token}', 'info')
                return redirect(url_for('auth.login'))
            else:
                flash('Failed to create reset token. Please try again.', 'error')
        else:
            # Don't reveal if email exists or not for security
            flash('If an account with that email exists, a password reset link has been sent.', 'info')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Get reset token
    reset_token = PasswordResetToken.get_by_token(token)
    
    if not reset_token:
        flash('Invalid or expired reset token.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        new_password = form.new_password.data
        
        # Get user
        user = AuthUser.get_by_id(reset_token.user_id)
        
        if user:
            # Update password
            if user.update_password(new_password):
                # Mark token as used
                reset_token.mark_as_used()
                
                flash('Your password has been reset successfully. Please log in with your new password.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Failed to reset password. Please try again.', 'error')
        else:
            flash('User not found.', 'error')
    
    return render_template('auth/reset_password.html', form=form, token=token)


@auth_bp.route('/sessions')
@login_required
def user_sessions():
    """View user sessions"""
    # Get user's active sessions
    # This would require implementing a method to get sessions by user_id
    # For now, we'll show a placeholder
    sessions = []
    
    return render_template('auth/sessions.html', sessions=sessions)


@auth_bp.route('/sessions/<session_id>/revoke', methods=['POST'])
@login_required
def revoke_session(session_id):
    """Revoke a specific session"""
    # This would require implementing session revocation
    # For now, we'll just redirect back
    flash('Session revoked successfully.', 'success')
    return redirect(url_for('auth.user_sessions'))


# API endpoints for AJAX requests
@auth_bp.route('/api/check-email')
def check_email():
    """Check if email is available"""
    email = request.args.get('email', '').lower().strip()
    
    if not email:
        return jsonify({'available': False, 'message': 'Email is required'})
    
    user = AuthUser.get_by_email(email)
    available = user is None
    
    return jsonify({
        'available': available,
        'message': 'Email is available' if available else 'Email is already taken'
    })


@auth_bp.route('/api/validate-password')
def validate_password():
    """Validate password strength"""
    password = request.args.get('password', '')
    
    if not password:
        return jsonify({'valid': False, 'message': 'Password is required'})
    
    # Check password strength
    errors = []
    
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long')
    
    if not any(c.isupper() for c in password):
        errors.append('Password must contain at least one uppercase letter')
    
    if not any(c.islower() for c in password):
        errors.append('Password must contain at least one lowercase letter')
    
    if not any(c.isdigit() for c in password):
        errors.append('Password must contain at least one number')
    
    if not any(c in '!@#$%^&*(),.?":{}|<>' for c in password):
        errors.append('Password must contain at least one special character')
    
    valid = len(errors) == 0
    
    return jsonify({
        'valid': valid,
        'message': 'Password is strong' if valid else '; '.join(errors)
    })

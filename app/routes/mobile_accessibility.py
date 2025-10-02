from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.mobile_accessibility import (
    UserAccessibilityPreferences, UserMobilePreferences, OfflineData,
    DeviceSync, AccessibilityAuditLog
)
from app.forms import (
    AccessibilityPreferencesForm, MobilePreferencesForm, DeviceRegistrationForm,
    OfflineDataForm, AccessibilityTestForm, SyncStatusForm
)
from app.routes.topics import get_current_user
from datetime import datetime
import uuid
import json

mobile_accessibility = Blueprint('mobile_accessibility', __name__)


@mobile_accessibility.route('/accessibility')
@login_required
def accessibility_dashboard():
    """Main accessibility dashboard"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        # Get user preferences
        accessibility_prefs = UserAccessibilityPreferences.get_user_preferences(user.id)
        mobile_prefs = UserMobilePreferences.get_user_preferences(user.id)
        
        # Get audit log
        audit_log = AccessibilityAuditLog.get_user_audit_log(user.id, limit=10)
        
        return render_template('mobile_accessibility/dashboard.html',
                             accessibility_prefs=accessibility_prefs,
                             mobile_prefs=mobile_prefs,
                             audit_log=audit_log)
    
    except Exception as e:
        flash('Error loading accessibility dashboard.', 'error')
        return redirect(url_for('main.dashboard'))


@mobile_accessibility.route('/accessibility/preferences', methods=['GET', 'POST'])
@login_required
def accessibility_preferences():
    """Manage accessibility preferences"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = AccessibilityPreferencesForm()
        
        if form.validate_on_submit():
            success = UserAccessibilityPreferences.update_preferences(
                user.id,
                screen_reader_enabled=form.screen_reader_enabled.data,
                high_contrast_mode=form.high_contrast_mode.data,
                text_size=form.text_size.data,
                keyboard_navigation=form.keyboard_navigation.data,
                reduced_motion=form.reduced_motion.data,
                color_blind_friendly=form.color_blind_friendly.data,
                focus_indicators=form.focus_indicators.data
            )
            
            if success:
                # Log the action
                UserAccessibilityPreferences.log_accessibility_action(
                    user.id,
                    'preferences_updated',
                    {
                        'screen_reader_enabled': form.screen_reader_enabled.data,
                        'high_contrast_mode': form.high_contrast_mode.data,
                        'text_size': form.text_size.data
                    }
                )
                
                flash('Accessibility preferences updated successfully!', 'success')
                return redirect(url_for('mobile_accessibility.accessibility_preferences'))
            else:
                flash('Error updating accessibility preferences.', 'error')
        else:
            # Pre-populate form with current preferences
            prefs = UserAccessibilityPreferences.get_user_preferences(user.id)
            form.screen_reader_enabled.data = prefs.screen_reader_enabled
            form.high_contrast_mode.data = prefs.high_contrast_mode
            form.text_size.data = prefs.text_size
            form.keyboard_navigation.data = prefs.keyboard_navigation
            form.reduced_motion.data = prefs.reduced_motion
            form.color_blind_friendly.data = prefs.color_blind_friendly
            form.focus_indicators.data = prefs.focus_indicators
        
        return render_template('mobile_accessibility/preferences.html', form=form)
    
    except Exception as e:
        flash('Error loading accessibility preferences.', 'error')
        return redirect(url_for('mobile_accessibility.accessibility_dashboard'))


@mobile_accessibility.route('/mobile/preferences', methods=['GET', 'POST'])
@login_required
def mobile_preferences():
    """Manage mobile preferences"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = MobilePreferencesForm()
        
        if form.validate_on_submit():
            success = UserMobilePreferences.update_preferences(
                user.id,
                offline_mode=form.offline_mode.data,
                auto_sync=form.auto_sync.data,
                sync_frequency=form.sync_frequency.data,
                data_usage_limit=form.data_usage_limit.data,
                push_notifications=form.push_notifications.data,
                vibration_enabled=form.vibration_enabled.data,
                haptic_feedback=form.haptic_feedback.data
            )
            
            if success:
                flash('Mobile preferences updated successfully!', 'success')
                return redirect(url_for('mobile_accessibility.mobile_preferences'))
            else:
                flash('Error updating mobile preferences.', 'error')
        else:
            # Pre-populate form with current preferences
            prefs = UserMobilePreferences.get_user_preferences(user.id)
            form.offline_mode.data = prefs.offline_mode
            form.auto_sync.data = prefs.auto_sync
            form.sync_frequency.data = prefs.sync_frequency
            form.data_usage_limit.data = prefs.data_usage_limit
            form.push_notifications.data = prefs.push_notifications
            form.vibration_enabled.data = prefs.vibration_enabled
            form.haptic_feedback.data = prefs.haptic_feedback
        
        return render_template('mobile_accessibility/mobile_preferences.html', form=form)
    
    except Exception as e:
        flash('Error loading mobile preferences.', 'error')
        return redirect(url_for('mobile_accessibility.accessibility_dashboard'))


@mobile_accessibility.route('/mobile/offline')
@login_required
def offline_management():
    """Manage offline data"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        # Get cached data
        cached_data = OfflineData.get_cached_data(user.id)
        
        # Group by data type
        data_by_type = {}
        for data in cached_data:
            if data.data_type not in data_by_type:
                data_by_type[data.data_type] = []
            data_by_type[data.data_type].append(data)
        
        return render_template('mobile_accessibility/offline_management.html',
                             cached_data=cached_data,
                             data_by_type=data_by_type)
    
    except Exception as e:
        flash('Error loading offline management.', 'error')
        return redirect(url_for('mobile_accessibility.accessibility_dashboard'))


@mobile_accessibility.route('/mobile/offline/action', methods=['POST'])
@login_required
def offline_action():
    """Handle offline data actions"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = OfflineDataForm()
        
        if form.validate_on_submit():
            data_type = form.data_type.data
            action = form.action.data
            
            if action == 'download':
                # Simulate downloading data for offline
                flash(f'Downloading {data_type} for offline access...', 'info')
            elif action == 'clear':
                success = OfflineData.clear_cache(user.id, data_type if data_type != 'all' else None)
                if success:
                    flash(f'Cache cleared for {data_type}.', 'success')
                else:
                    flash('Error clearing cache.', 'error')
            elif action == 'sync':
                # Simulate syncing with server
                flash(f'Syncing {data_type} with server...', 'info')
        
        return redirect(url_for('mobile_accessibility.offline_management'))
    
    except Exception as e:
        flash('Error performing offline action.', 'error')
        return redirect(url_for('mobile_accessibility.offline_management'))


@mobile_accessibility.route('/mobile/devices')
@login_required
def device_management():
    """Manage registered devices"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        # Get user devices
        devices = DeviceSync.get_user_devices(user.id)
        
        return render_template('mobile_accessibility/device_management.html',
                             devices=devices)
    
    except Exception as e:
        flash('Error loading device management.', 'error')
        return redirect(url_for('mobile_accessibility.accessibility_dashboard'))


@mobile_accessibility.route('/mobile/devices/register', methods=['GET', 'POST'])
@login_required
def register_device():
    """Register a new device"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = DeviceRegistrationForm()
        
        if form.validate_on_submit():
            # Generate device ID
            device_id = str(uuid.uuid4())
            
            device = DeviceSync.register_device(
                user.id,
                device_id,
                form.device_name.data,
                form.device_type.data
            )
            
            if device:
                flash(f'Device "{form.device_name.data}" registered successfully!', 'success')
                return redirect(url_for('mobile_accessibility.device_management'))
            else:
                flash('Error registering device.', 'error')
        
        return render_template('mobile_accessibility/register_device.html', form=form)
    
    except Exception as e:
        flash('Error registering device.', 'error')
        return redirect(url_for('mobile_accessibility.device_management'))


@mobile_accessibility.route('/accessibility/test', methods=['GET', 'POST'])
@login_required
def accessibility_test():
    """Accessibility testing tools"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = AccessibilityTestForm()
        
        if form.validate_on_submit():
            # Log the test
            UserAccessibilityPreferences.log_accessibility_action(
                user.id,
                'accessibility_test',
                {
                    'test_type': form.test_type.data,
                    'description': form.test_description.data
                }
            )
            
            flash(f'Accessibility test "{form.test_type.data}" logged successfully!', 'success')
            return redirect(url_for('mobile_accessibility.accessibility_test'))
        
        return render_template('mobile_accessibility/accessibility_test.html', form=form)
    
    except Exception as e:
        flash('Error loading accessibility test.', 'error')
        return redirect(url_for('mobile_accessibility.accessibility_dashboard'))


@mobile_accessibility.route('/accessibility/audit')
@login_required
def accessibility_audit():
    """View accessibility audit log"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        # Get audit log
        audit_log = AccessibilityAuditLog.get_user_audit_log(user.id, limit=100)
        
        return render_template('mobile_accessibility/audit_log.html',
                             audit_log=audit_log)
    
    except Exception as e:
        flash('Error loading accessibility audit.', 'error')
        return redirect(url_for('mobile_accessibility.accessibility_dashboard'))


@mobile_accessibility.route('/api/accessibility/preferences')
@login_required
def api_accessibility_preferences():
    """API endpoint for accessibility preferences"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        prefs = UserAccessibilityPreferences.get_user_preferences(user.id)
        
        return jsonify({
            'screen_reader_enabled': prefs.screen_reader_enabled,
            'high_contrast_mode': prefs.high_contrast_mode,
            'text_size': prefs.text_size,
            'keyboard_navigation': prefs.keyboard_navigation,
            'reduced_motion': prefs.reduced_motion,
            'color_blind_friendly': prefs.color_blind_friendly,
            'focus_indicators': prefs.focus_indicators
        })
    
    except Exception as e:
        return jsonify({'error': 'Error loading preferences'}), 500


@mobile_accessibility.route('/api/mobile/preferences')
@login_required
def api_mobile_preferences():
    """API endpoint for mobile preferences"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        prefs = UserMobilePreferences.get_user_preferences(user.id)
        
        return jsonify({
            'offline_mode': prefs.offline_mode,
            'auto_sync': prefs.auto_sync,
            'sync_frequency': prefs.sync_frequency,
            'data_usage_limit': prefs.data_usage_limit,
            'push_notifications': prefs.push_notifications,
            'vibration_enabled': prefs.vibration_enabled,
            'haptic_feedback': prefs.haptic_feedback
        })
    
    except Exception as e:
        return jsonify({'error': 'Error loading preferences'}), 500


@mobile_accessibility.route('/api/offline/status')
@login_required
def api_offline_status():
    """API endpoint for offline status"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        # Get cached data count
        cached_data = OfflineData.get_cached_data(user.id)
        
        return jsonify({
            'is_offline': len(cached_data) > 0,
            'cached_items': len(cached_data),
            'last_sync': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': 'Error loading offline status'}), 500

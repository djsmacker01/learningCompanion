from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.forms import ContactForm
from app.models import get_supabase_client
from datetime import datetime
import uuid

support = Blueprint('support', __name__)

@support.route('/help')
def help_center():
    """Help center with FAQ and guides"""
    return render_template('support/help_center.html')

@support.route('/documentation')
def documentation():
    """Technical documentation and API reference"""
    return render_template('support/documentation.html')

@support.route('/contact', methods=['GET', 'POST'])
def contact_us():
    """Contact support form"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # In a real application, you would:
        # 1. Save the support ticket to database
        # 2. Send email notification to support team
        # 3. Send confirmation email to user
        # 4. Create ticket in support system
        
        # For now, we'll just show a success message
        flash('Thank you for contacting us! We will get back to you within 24 hours.', 'success')
        return redirect(url_for('support.contact_us'))
    
    return render_template('support/contact_us.html', form=form)

@support.route('/community')
def community():
    """Community page with stats and activity"""
    return render_template('support/community.html')

@support.route('/privacy')
def privacy_policy():
    """Privacy policy page"""
    return render_template('legal/privacy_policy.html')

@support.route('/terms')
def terms_of_service():
    """Terms of service page"""
    return render_template('legal/terms_of_service.html')

@support.route('/cookies')
def cookie_policy():
    """Cookie policy page"""
    return render_template('legal/cookie_policy.html')

@support.route('/gdpr')
def gdpr():
    """GDPR compliance page"""
    return render_template('legal/gdpr.html')

@support.route('/api/support-ticket', methods=['POST'])
@login_required
def create_support_ticket():
    """API endpoint to create support ticket"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['subject', 'message', 'priority']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create support ticket
        ticket_data = {
            'id': str(uuid.uuid4()),
            'user_id': current_user.id,
            'subject': data['subject'],
            'message': data['message'],
            'priority': data['priority'],
            'status': 'open',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # In a real application, save to database
        # For now, just return success
        return jsonify({
            'success': True,
            'ticket_id': ticket_data['id'],
            'message': 'Support ticket created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@support.route('/api/data-export', methods=['POST'])
@login_required
def export_user_data():
    """API endpoint to export user data (GDPR compliance)"""
    try:
        # In a real application, you would:
        # 1. Collect all user data from database
        # 2. Format it according to GDPR requirements
        # 3. Send it to user's email
        # 4. Log the export request
        
        return jsonify({
            'success': True,
            'message': 'Data export request submitted. You will receive an email with your data within 30 days.',
            'export_id': str(uuid.uuid4())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@support.route('/api/data-deletion', methods=['POST'])
@login_required
def delete_user_data():
    """API endpoint to delete user data (GDPR compliance)"""
    try:
        # In a real application, you would:
        # 1. Verify user identity
        # 2. Delete all user data from database
        # 3. Send confirmation email
        # 4. Log the deletion request
        
        return jsonify({
            'success': True,
            'message': 'Data deletion request submitted. Your account and data will be permanently deleted within 30 days.',
            'deletion_id': str(uuid.uuid4())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


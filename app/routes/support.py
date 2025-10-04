from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.forms import ContactForm
from app.models import get_supabase_client
from datetime import datetime
import uuid

support = Blueprint('support', __name__)

@support.route('/help')
def help_center():
    
    return render_template('support/help_center.html')

@support.route('/documentation')
def documentation():
    
    return render_template('support/documentation.html')

@support.route('/contact', methods=['GET', 'POST'])
def contact_us():
    
    form = ContactForm()
    
    if form.validate_on_submit():
        
        
        
        
        
        
        
        flash('Thank you for contacting us! We will get back to you within 24 hours.', 'success')
        return redirect(url_for('support.contact_us'))
    
    return render_template('support/contact_us.html', form=form)

@support.route('/community')
def community():
    
    return render_template('support/community.html')

@support.route('/privacy')
def privacy_policy():
    
    return render_template('legal/privacy_policy.html')

@support.route('/terms')
def terms_of_service():
    
    return render_template('legal/terms_of_service.html')

@support.route('/cookies')
def cookie_policy():
    
    return render_template('legal/cookie_policy.html')

@support.route('/gdpr')
def gdpr():
    
    return render_template('legal/gdpr.html')

@support.route('/api/support-ticket', methods=['POST'])
@login_required
def create_support_ticket():
    
    try:
        data = request.get_json()
        
        
        required_fields = ['subject', 'message', 'priority']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        
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
    
    try:
        
        
        
        
        
        
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
    
    try:
        
        
        
        
        
        
        return jsonify({
            'success': True,
            'message': 'Data deletion request submitted. Your account and data will be permanently deleted within 30 days.',
            'deletion_id': str(uuid.uuid4())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



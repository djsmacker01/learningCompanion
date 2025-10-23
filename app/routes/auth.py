from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('auth/login.html')
        

        from app.models.auth import AuthUser
        

        user = AuthUser.get_by_username_or_email(username)
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        flash('Registration functionality coming soon!', 'info')
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


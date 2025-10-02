from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import User
from app.models.social_features import (
    Friend, StudyGroup, StudyGroupMember, SocialChallenge, 
    ChallengeParticipant, SocialAchievement, SocialActivity
)
from app.forms import (
    FriendRequestForm, StudyGroupForm, SocialChallengeForm, ShareAchievementForm,
    StudySessionSocialForm, SocialSearchForm, GroupInviteForm, ChallengeProgressForm
)
from app.routes.topics import get_current_user
from datetime import datetime, timedelta
import json

social = Blueprint('social', __name__)


@social.route('/social')
@login_required
def social_dashboard():
    """Main social features dashboard"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        # Get user's social data
        friends = Friend.get_friends(user.id)
        pending_requests = Friend.get_pending_requests(user.id)
        user_groups = StudyGroup.get_user_groups(user.id)
        active_challenges = SocialChallenge.get_active_challenges()
        user_achievements = SocialAchievement.get_user_achievements(user.id, is_shared=True)
        recent_activity = SocialActivity.get_user_activity(user.id, limit=10)
        
        return render_template('social/dashboard.html',
                             friends=friends,
                             pending_requests=pending_requests,
                             user_groups=user_groups,
                             active_challenges=active_challenges,
                             user_achievements=user_achievements,
                             recent_activity=recent_activity)
    
    except Exception as e:
        flash('Error loading social dashboard.', 'error')
        return redirect(url_for('main.dashboard'))


@social.route('/social/friends')
@login_required
def friends_list():
    """View and manage friends"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        friends = Friend.get_friends(user.id)
        pending_requests = Friend.get_pending_requests(user.id)
        
        return render_template('social/friends.html',
                             friends=friends,
                             pending_requests=pending_requests)
    
    except Exception as e:
        flash('Error loading friends list.', 'error')
        return redirect(url_for('social.social_dashboard'))


@social.route('/social/friends/add', methods=['GET', 'POST'])
@login_required
def add_friend():
    """Send a friend request"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = FriendRequestForm()
        
        if form.validate_on_submit():
            # In a real app, you'd look up the user by email
            # For now, we'll simulate finding a user
            friend_email = form.friend_email.data
            
            # Simulate finding user by email (in real app, query database)
            if friend_email == 'friend@example.com':
                friend_id = 'mock-friend-id'
                
                success = Friend.send_friend_request(friend_id)
                
                if success:
                    flash('Friend request sent successfully!', 'success')
                    return redirect(url_for('social.friends_list'))
                else:
                    flash('Error sending friend request.', 'error')
            else:
                flash('User not found with that email address.', 'error')
        
        return render_template('social/add_friend.html', form=form)
    
    except Exception as e:
        flash('Error adding friend.', 'error')
        return redirect(url_for('social.friends_list'))


@social.route('/social/friends/accept/<user_id>', methods=['POST'])
@login_required
def accept_friend_request(user_id):
    """Accept a friend request"""
    try:
        success = Friend.accept_friend_request(user_id)
        
        if success:
            flash('Friend request accepted!', 'success')
        else:
            flash('Error accepting friend request.', 'error')
        
        return redirect(url_for('social.friends_list'))
    
    except Exception as e:
        flash('Error accepting friend request.', 'error')
        return redirect(url_for('social.friends_list'))


@social.route('/social/groups')
@login_required
def study_groups():
    """View study groups"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        public_groups = StudyGroup.get_public_groups()
        user_groups = StudyGroup.get_user_groups(user.id)
        
        return render_template('social/study_groups.html',
                             public_groups=public_groups,
                             user_groups=user_groups)
    
    except Exception as e:
        flash('Error loading study groups.', 'error')
        return redirect(url_for('social.social_dashboard'))


@social.route('/social/groups/create', methods=['GET', 'POST'])
@login_required
def create_study_group():
    """Create a new study group"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = StudyGroupForm()
        
        if form.validate_on_submit():
            group = StudyGroup.create_group(
                name=form.name.data,
                description=form.description.data,
                creator_id=user.id,
                is_public=form.is_public.data,
                max_members=form.max_members.data
            )
            
            if group:
                flash('Study group created successfully!', 'success')
                return redirect(url_for('social.study_groups'))
            else:
                flash('Error creating study group.', 'error')
        
        return render_template('social/create_group.html', form=form)
    
    except Exception as e:
        flash('Error creating study group.', 'error')
        return redirect(url_for('social.study_groups'))


@social.route('/social/groups/<group_id>/join', methods=['POST'])
@login_required
def join_study_group(group_id):
    """Join a study group"""
    try:
        success = StudyGroup.join_group(group_id)
        
        if success:
            flash('Successfully joined the study group!', 'success')
        else:
            flash('Error joining study group.', 'error')
        
        return redirect(url_for('social.study_groups'))
    
    except Exception as e:
        flash('Error joining study group.', 'error')
        return redirect(url_for('social.study_groups'))


@social.route('/social/groups/<group_id>')
@login_required
def view_study_group(group_id):
    """View a study group"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        # Get group details (simplified for demo)
        group = {
            'id': group_id,
            'name': 'Sample Study Group',
            'description': 'A sample study group for demonstration',
            'creator_id': 'mock-creator-id',
            'is_public': True,
            'max_members': 50,
            'created_at': datetime.utcnow()
        }
        
        members = StudyGroupMember.get_group_members(group_id)
        
        return render_template('social/group_detail.html',
                             group=group,
                             members=members)
    
    except Exception as e:
        flash('Error loading study group.', 'error')
        return redirect(url_for('social.study_groups'))


@social.route('/social/challenges')
@login_required
def social_challenges():
    """View social challenges"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        global_challenges = SocialChallenge.get_active_challenges()
        user_participations = ChallengeParticipant.get_user_participations(user.id)
        
        return render_template('social/challenges.html',
                             global_challenges=global_challenges,
                             user_participations=user_participations)
    
    except Exception as e:
        flash('Error loading challenges.', 'error')
        return redirect(url_for('social.social_dashboard'))


@social.route('/social/challenges/create', methods=['GET', 'POST'])
@login_required
def create_challenge():
    """Create a new social challenge"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = SocialChallengeForm()
        
        if form.validate_on_submit():
            challenge = SocialChallenge.create_challenge(
                title=form.title.data,
                description=form.description.data,
                challenge_type=form.challenge_type.data,
                target_value=form.target_value.data,
                target_unit=form.target_unit.data,
                creator_id=user.id,
                start_date=form.start_date.data,
                end_date=form.end_date.data
            )
            
            if challenge:
                flash('Challenge created successfully!', 'success')
                return redirect(url_for('social.social_challenges'))
            else:
                flash('Error creating challenge.', 'error')
        
        return render_template('social/create_challenge.html', form=form)
    
    except Exception as e:
        flash('Error creating challenge.', 'error')
        return redirect(url_for('social.social_challenges'))


@social.route('/social/challenges/<challenge_id>/join', methods=['POST'])
@login_required
def join_challenge(challenge_id):
    """Join a challenge"""
    try:
        success = SocialChallenge.join_challenge(challenge_id)
        
        if success:
            flash('Successfully joined the challenge!', 'success')
        else:
            flash('Error joining challenge.', 'error')
        
        return redirect(url_for('social.social_challenges'))
    
    except Exception as e:
        flash('Error joining challenge.', 'error')
        return redirect(url_for('social.social_challenges'))


@social.route('/social/challenges/<challenge_id>/progress', methods=['GET', 'POST'])
@login_required
def update_challenge_progress(challenge_id):
    """Update challenge progress"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = ChallengeProgressForm()
        form.challenge_id.data = challenge_id
        
        if form.validate_on_submit():
            success = ChallengeParticipant.update_progress(
                challenge_id, 
                form.progress.data
            )
            
            if success:
                flash('Progress updated successfully!', 'success')
                return redirect(url_for('social.social_challenges'))
            else:
                flash('Error updating progress.', 'error')
        
        return render_template('social/update_progress.html', 
                             form=form, 
                             challenge_id=challenge_id)
    
    except Exception as e:
        flash('Error updating progress.', 'error')
        return redirect(url_for('social.social_challenges'))


@social.route('/social/achievements')
@login_required
def social_achievements():
    """View and share achievements"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        user_achievements = SocialAchievement.get_user_achievements(user.id)
        shared_achievements = SocialAchievement.get_user_achievements(user.id, is_shared=True)
        
        return render_template('social/achievements.html',
                             user_achievements=user_achievements,
                             shared_achievements=shared_achievements)
    
    except Exception as e:
        flash('Error loading achievements.', 'error')
        return redirect(url_for('social.social_dashboard'))


@social.route('/social/achievements/share', methods=['GET', 'POST'])
@login_required
def share_achievement():
    """Share an achievement"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = ShareAchievementForm()
        
        if form.validate_on_submit():
            achievement_data = {
                'title': form.achievement_title.data,
                'description': form.achievement_description.data,
                'share_with_friends': form.share_with_friends.data,
                'share_with_groups': form.share_with_groups.data
            }
            
            achievement = SocialAchievement.create_achievement(
                user_id=user.id,
                achievement_type=form.achievement_type.data,
                achievement_data=achievement_data,
                is_shared=True
            )
            
            if achievement:
                flash('Achievement shared successfully!', 'success')
                return redirect(url_for('social.social_achievements'))
            else:
                flash('Error sharing achievement.', 'error')
        
        return render_template('social/share_achievement.html', form=form)
    
    except Exception as e:
        flash('Error sharing achievement.', 'error')
        return redirect(url_for('social.social_achievements'))


@social.route('/social/activity')
@login_required
def activity_feed():
    """View social activity feed"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        recent_activity = SocialActivity.get_user_activity(user.id, limit=50)
        
        return render_template('social/activity_feed.html',
                             recent_activity=recent_activity)
    
    except Exception as e:
        flash('Error loading activity feed.', 'error')
        return redirect(url_for('social.social_dashboard'))


@social.route('/social/search')
@login_required
def social_search():
    """Search social content"""
    try:
        form = SocialSearchForm()
        
        results = []
        query = request.args.get('query', '')
        search_type = request.args.get('search_type', 'all')
        
        if query:
            if search_type in ['all', 'groups']:
                # Search study groups
                public_groups = StudyGroup.get_public_groups()
                matching_groups = [g for g in public_groups if query.lower() in g.name.lower() or query.lower() in (g.description or '').lower()]
                results.extend([{'type': 'group', 'data': g} for g in matching_groups])
        
        return render_template('social/search.html',
                             form=form,
                             results=results,
                             query=query,
                             search_type=search_type)
    
    except Exception as e:
        flash('Error searching social content.', 'error')
        return redirect(url_for('social.social_dashboard'))


@social.route('/social/sessions/share', methods=['GET', 'POST'])
@login_required
def share_study_session():
    """Share a study session with friends/groups"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = StudySessionSocialForm()
        
        # Populate group choices
        user_groups = StudyGroup.get_user_groups(user.id)
        form.group_id.choices = [(group.id, group.name) for group in user_groups]
        
        if form.validate_on_submit():
            # In a real app, you'd create a social session record
            # For now, we'll just show a success message
            flash('Study session shared successfully!', 'success')
            return redirect(url_for('sessions.session_history'))
        
        return render_template('social/share_session.html', form=form)
    
    except Exception as e:
        flash('Error sharing study session.', 'error')
        return redirect(url_for('sessions.session_history'))

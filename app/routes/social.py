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
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
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
        print(f"Error loading social dashboard: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error loading social dashboard: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))


@social.route('/social/friends')
@login_required
def friends_list():
    
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
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = FriendRequestForm()
        
        if form.validate_on_submit():
            friend_email = form.friend_email.data.lower().strip()
            
            # Check if it's your own email
            if friend_email == user.email:
                flash("You cannot add yourself as a friend!", 'error')
                return render_template('social/add_friend.html', form=form)
            
            # Try to find existing user with this email
            existing_user = User.get_user_by_email(friend_email)
            
            if existing_user:
                # User exists - send friend request
                success = Friend.send_friend_request(user.id, existing_user.id)
                
                if success:
                    flash(f'Friend request sent!', 'success')
                    return redirect(url_for('social.friends_list'))
                else:
                    flash('Error sending friend request. You may already be friends or have a pending request.', 'error')
            else:
                # User doesn't exist - they need to register first
                flash('User not found. They need to create an account first before you can add them as a friend.', 'info')
        
        return render_template('social/add_friend.html', form=form)
    
    except Exception as e:
        print(f"Error adding friend: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error adding friend: {str(e)}', 'error')
        return redirect(url_for('social.friends_list'))


@social.route('/social/friends/accept/<user_id>', methods=['POST'])
@login_required
def accept_friend_request(user_id):
    
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
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = StudyGroupForm()
        
        if form.validate_on_submit():
            # Convert string 'true'/'false' to boolean
            is_public_value = form.is_public.data == 'true'
            
            print(f"\n{'='*60}")
            print(f"DEBUG: Form submitted!")
            print(f"  - form.is_public.data (raw): '{form.is_public.data}' (type: {type(form.is_public.data)})")
            print(f"  - is_public_value (converted): {is_public_value} (type: {type(is_public_value)})")
            print(f"{'='*60}\n")
            
            group = StudyGroup.create_group(
                name=form.name.data,
                description=form.description.data,
                creator_id=user.id,
                is_public=is_public_value,
                max_members=form.max_members.data
            )
            
            if group:
                print(f"\n{'='*60}")
                print(f"DEBUG: Group created successfully!")
                print(f"  - Group ID: {group.id}")
                print(f"  - Group name: {group.name}")
                print(f"  - Group is_public attribute: {group.is_public} (type: {type(group.is_public)})")
                print(f"{'='*60}\n")
            else:
                print(f"\n{'='*60}")
                print(f"ERROR: Group creation returned None!")
                print(f"{'='*60}\n")
            
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
    
    try:
        success = StudyGroup.join_group(group_id)
        
        if success:
            flash('Successfully joined the study group!', 'success')
        else:
            flash('Error joining study group.', 'error')
        
        return redirect(url_for('social.study_groups'))
    
    except Exception as e:
        print(f"Error joining study group: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error joining study group: {str(e)}', 'error')
        return redirect(url_for('social.study_groups'))


@social.route('/social/groups/<group_id>')
@login_required
def view_study_group(group_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        
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
    
    try:
        form = SocialSearchForm()
        
        results = []
        query = request.args.get('query', '')
        search_type = request.args.get('search_type', 'all')
        
        if query:
            if search_type in ['all', 'groups']:
                
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
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = StudySessionSocialForm()
        
        
        user_groups = StudyGroup.get_user_groups(user.id)
        form.group_id.choices = [(group.id, group.name) for group in user_groups]
        
        if form.validate_on_submit():
            
            
            flash('Study session shared successfully!', 'success')
            return redirect(url_for('sessions.session_history'))
        
        return render_template('social/share_session.html', form=form)
    
    except Exception as e:
        flash('Error sharing study session.', 'error')
        return redirect(url_for('sessions.session_history'))


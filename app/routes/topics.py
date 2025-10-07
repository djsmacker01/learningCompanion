from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Topic, User
from app.models.study_session import StudySession
from app.forms import (
    TopicForm, ShareTopicForm, JoinTopicForm, CSVImportForm, BulkTopicForm, FileUploadForm,
    TopicNoteForm, TopicAttachmentForm, TopicTagForm, TopicContentForm, TopicVersionForm, ContentSearchForm
)
import os
import csv
import io
from werkzeug.utils import secure_filename

topics = Blueprint('topics', __name__)

import uuid
from app.models import get_supabase_client

def get_current_user():
    
    if current_user.is_authenticated:
        return current_user
    return None

@topics.route('/topics')
@login_required
def list_topics():
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topics_list = Topic.get_all_by_user(user.id)
        return render_template('topics/list.html', topics=topics_list)
    except Exception as e:
        flash('Error loading topics. Please try again.', 'error')
        return render_template('topics/list.html', topics=[])

@topics.route('/topics/debug')
@login_required
def debug_env():
    import os
    return {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'Not set')[:20] + '...' if os.getenv('SUPABASE_SERVICE_ROLE_KEY') else 'Not set',
        'SUPABASE_AVAILABLE': os.getenv('SUPABASE_AVAILABLE', 'Not set')
    }

@topics.route('/topics/new', methods=['GET', 'POST'])
@login_required
def create_topic():
    form = TopicForm()
    
    if form.validate_on_submit():
        try:
            print(f"=== TOPIC CREATION REQUEST ===")
            print(f"Attempting to create topic: {form.title.data.strip()}")
            user = get_current_user()
            if not user:
                flash('User not authenticated.', 'error')
                return redirect(url_for('auth.login'))
            
            print(f"User ID: {user.id}")
            print(f"Supabase URL: {os.getenv('SUPABASE_URL')}")
            print(f"Supabase Service Role Key: {os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'Not set')[:20]}...")
            print(f"Supabase Available: {os.getenv('SUPABASE_AVAILABLE', 'Not set')}")
            
            from app.models import get_supabase_client, SUPABASE_AVAILABLE
            client = get_supabase_client()
            print(f"Supabase client available: {SUPABASE_AVAILABLE}")
            print(f"Supabase client object: {client is not None}")
            
            topic = Topic.create(
                title=form.title.data.strip(),
                description=form.description.data.strip(),
                user_id=user.id
            )
            
            if topic:
                flash('Topic created successfully!', 'success')
                return redirect(url_for('topics.view_topic', topic_id=topic.id))
            else:
                flash('Error creating topic. Please try again.', 'error')
        except Exception as e:
            print(f"Exception creating topic: {e}")
            flash(f'Error creating topic: {str(e)}', 'error')
    
    return render_template('topics/form.html', form=form, title='Create New Topic')

@topics.route('/topics/<topic_id>')
@login_required
def view_topic(topic_id):
    try:
        print(f"=== VIEWING TOPIC ===")
        print(f"Topic ID: {topic_id}")
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        print(f"User ID: {user.id}")
        
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topic = Topic.get_by_id(topic_id, user.id)
        print(f"Topic found: {topic is not None}")
        if topic:
            print(f"Topic title: {topic.title}")
        
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        print(f"Getting session data for topic: {topic_id}")
        try:
            topic_sessions = StudySession.get_topic_sessions(topic_id, user.id)
            print(f"Got {len(topic_sessions)} sessions")
        except Exception as e:
            print(f"Error getting topic sessions: {e}")
            topic_sessions = []
        
        try:
            topic_progress = StudySession.get_topic_progress(topic_id, user.id)
            print(f"Got topic progress: {topic_progress}")
        except Exception as e:
            print(f"Error getting topic progress: {e}")
            topic_progress = {}
        
        recent_sessions = topic_sessions[:5]
        
        print(f"Rendering template with topic: {topic.title}")
        return render_template('topics/view.html', 
                             topic=topic, 
                             topic_sessions=topic_sessions,
                             topic_progress=topic_progress,
                             recent_sessions=recent_sessions)
    except Exception as e:
        print(f"ERROR: Exception in view_topic: {e}")
        import traceback
        traceback.print_exc()
        flash('Error loading topic. Please try again.', 'error')
        return redirect(url_for('topics.list_topics'))

@topics.route('/topics/<topic_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_topic(topic_id):
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topic = Topic.get_by_id(topic_id, user.id)
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        form = TopicForm()
        
        if request.method == 'GET':
            form.title.data = topic.title
            form.description.data = topic.description
        
        if form.validate_on_submit():
            success = topic.update(
                title=form.title.data.strip(),
                description=form.description.data.strip()
            )
            
            if success:
                flash('Topic updated successfully!', 'success')
                return redirect(url_for('topics.view_topic', topic_id=topic.id))
            else:
                flash('Error updating topic. Please try again.', 'error')
        
        return render_template('topics/form.html', form=form, topic=topic, title='Edit Topic')
    
    except Exception as e:
        flash('Error loading topic. Please try again.', 'error')
        return redirect(url_for('topics.list_topics'))

@topics.route('/topics/<topic_id>/delete', methods=['POST'])
@login_required
def delete_topic(topic_id):
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topic = Topic.get_by_id(topic_id, user.id)
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        success = topic.delete()
        
        if success:
            flash('Topic deleted successfully!', 'success')
        else:
            flash('Error deleting topic. Please try again.', 'error')
        
        return redirect(url_for('topics.list_topics'))
    
    except Exception as e:
        flash('Error deleting topic. Please try again.', 'error')
        return redirect(url_for('topics.list_topics'))


@topics.route('/topics/<topic_id>/share', methods=['GET', 'POST'])
@login_required
def share_topic(topic_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topic = Topic.get_by_id(topic_id, user.id)
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        form = ShareTopicForm()
        
        if form.validate_on_submit():
            expires_at = form.expires_at.data
            max_uses = form.max_uses.data
            
            share_code = Topic.share_topic(
                topic_id, 
                user.id, 
                expires_at=expires_at, 
                max_uses=max_uses
            )
            
            if share_code:
                flash(f'Topic shared successfully! Share code: {share_code}', 'success')
                return redirect(url_for('topics.view_topic', topic_id=topic_id))
            else:
                flash('Failed to share topic. Please try again.', 'error')
        
        return render_template('topics/share.html', topic=topic, form=form)
    
    except Exception as e:
        flash('Error sharing topic. Please try again.', 'error')
        return redirect(url_for('topics.list_topics'))


@topics.route('/topics/<topic_id>/revoke-sharing', methods=['POST'])
@login_required
def revoke_topic_sharing(topic_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        success = Topic.revoke_topic_sharing(topic_id, user.id)
        
        if success:
            flash('Topic sharing revoked successfully.', 'success')
        else:
            flash('Failed to revoke topic sharing. Please try again.', 'error')
        
        return redirect(url_for('topics.view_topic', topic_id=topic_id))
    
    except Exception as e:
        flash('Error revoking topic sharing. Please try again.', 'error')
        return redirect(url_for('topics.list_topics'))


@topics.route('/topics/join', methods=['GET', 'POST'])
@login_required
def join_topic():
    
    form = JoinTopicForm()
    
    if form.validate_on_submit():
        share_code = form.share_code.data.strip().upper()
        
        try:
            user = get_current_user()
            if not user:
                flash('User not authenticated.', 'error')
                return redirect(url_for('auth.login'))
            
            topic_id = Topic.join_topic_with_code(share_code, user.id)
            
            if topic_id:
                flash('Successfully joined the topic!', 'success')
                return redirect(url_for('topics.view_topic', topic_id=topic_id))
            else:
                flash('Invalid or expired share code. Please check and try again.', 'error')
        
        except Exception as e:
            flash(f'Error joining topic: {str(e)}', 'error')
    
    return render_template('topics/join.html', form=form)


@topics.route('/topics/shared')
@login_required
def shared_topics():
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        shared_topics_list = Topic.get_shared_topics(user.id)
        return render_template('topics/shared.html', topics=shared_topics_list)
    
    except Exception as e:
        flash('Error loading shared topics. Please try again.', 'error')
        return render_template('topics/shared.html', topics=[])


@topics.route('/topics/import/csv', methods=['GET', 'POST'])
@login_required
def import_topics_csv():
    
    form = CSVImportForm()
    
    if form.validate_on_submit():
        try:
            csv_file = form.csv_file.data
            if not csv_file:
                flash('No file selected.', 'error')
                return render_template('topics/import_csv.html', form=form)
            
            
            csv_content = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            
            imported_count = 0
            errors = []
            
            for row_num, row in enumerate(csv_reader, start=2):  
                try:
                    title = row.get('title', '').strip()
                    description = row.get('description', '').strip()
                    
                    if not title:
                        errors.append(f"Row {row_num}: Title is required")
                        continue
                    
                    
                    topic = Topic.create(
                        title=title,
                        description=description,
                        user_id=user.id
                    )
                    
                    if topic:
                        imported_count += 1
                    else:
                        errors.append(f"Row {row_num}: Failed to create topic")
                        
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
            
            if imported_count > 0:
                flash(f'Successfully imported {imported_count} topics!', 'success')
            if errors:
                flash(f'Some topics failed to import: {len(errors)} errors', 'warning')
                for error in errors[:5]:  
                    flash(error, 'error')
            
            return redirect(url_for('topics.list_topics'))
            
        except Exception as e:
            flash(f'Error importing CSV: {str(e)}', 'error')
    
    return render_template('topics/import_csv.html', form=form)


@topics.route('/topics/import/bulk', methods=['GET', 'POST'])
@login_required
def import_topics_bulk():
    
    form = BulkTopicForm()
    
    if form.validate_on_submit():
        try:
            topics_data = form.topics_data.data.strip()
            lines = [line.strip() for line in topics_data.split('\n') if line.strip()]
            
            imported_count = 0
            errors = []
            
            for line_num, line in enumerate(lines, start=1):
                try:
                    if '|' in line:
                        title, description = line.split('|', 1)
                        title = title.strip()
                        description = description.strip()
                    else:
                        title = line.strip()
                        description = f"Imported topic: {title}"
                    
                    if not title:
                        errors.append(f"Line {line_num}: Title is required")
                        continue
                    
                    
                    topic = Topic.create(
                        title=title,
                        description=description,
                        user_id=user.id
                    )
                    
                    if topic:
                        imported_count += 1
                    else:
                        errors.append(f"Line {line_num}: Failed to create topic")
                        
                except Exception as e:
                    errors.append(f"Line {line_num}: {str(e)}")
            
            if imported_count > 0:
                flash(f'Successfully created {imported_count} topics!', 'success')
            if errors:
                flash(f'Some topics failed to create: {len(errors)} errors', 'warning')
                for error in errors[:5]:  
                    flash(error, 'error')
            
            return redirect(url_for('topics.list_topics'))
            
        except Exception as e:
            flash(f'Error creating topics: {str(e)}', 'error')
    
    return render_template('topics/import_bulk.html', form=form)


@topics.route('/topics/import/materials', methods=['GET', 'POST'])
@login_required
def import_materials():
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        form = FileUploadForm()
        
        if form.validate_on_submit():
            try:
                file = form.file.data
                title = form.title.data.strip()
                description = form.description.data.strip()
                
                if not file:
                    flash('No file selected.', 'error')
                    return render_template('topics/import_materials.html', form=form)
                
                # Process the uploaded file
                from app.utils.document_processor import DocumentProcessor
                doc_processor = DocumentProcessor()
                
                # Check if document processing is available
                available_formats = DocumentProcessor.is_document_processing_available()
                file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else 'unknown'
                
                # Check if the file type is supported
                supported_formats = DocumentProcessor.get_supported_formats()
                if file_extension not in supported_formats:
                    topic = Topic.create(
                        title=title,
                        description=f"{description}\n\nUploaded file: {file.filename}\n\nUnsupported file type: {file_extension}\n\nSupported formats: {', '.join(supported_formats)}",
                        user_id=user.id
                    )
                    
                    if topic:
                        flash(f'Material "{title}" uploaded but file type not supported. See topic details for supported formats.', 'warning')
                        return redirect(url_for('topics.view_topic', topic_id=topic.id))
                    else:
                        flash('Failed to create topic for material.', 'error')
                        return render_template('topics/import_materials.html', form=form)
                
                # Process the document
                processing_result = doc_processor.process_document(file)
                
                if processing_result['success']:
                    content_info = processing_result['content_info']
                    file_info = processing_result['file_info']
                    file_type = processing_result.get('file_type', file_extension)
                    
                    # Create enhanced description with extracted content
                    enhanced_description = f"{description}\n\n"
                    enhanced_description += f"File: {file_info['original_filename']}\n"
                    enhanced_description += f"Size: {file_info['file_size']:,} bytes\n"
                    enhanced_description += f"Word count: {content_info['word_count']:,} words\n"
                    enhanced_description += f"Extraction method: {content_info['extraction_method']}\n"
                    enhanced_description += f"File type: {file_type.upper()}\n\n"
                    
                    if content_info.get('cleaned_text') or content_info.get('text_content'):
                        enhanced_description += f"EXTRACTED CONTENT FROM {file_type.upper()}:\n"
                        enhanced_description += "=" * 50 + "\n\n"
                        
                        # Add the extracted text (truncate if too long)
                        extracted_text = content_info.get('cleaned_text') or content_info.get('text_content', '')
                        if len(extracted_text) > 5000:
                            enhanced_description += extracted_text[:5000] + "\n\n... (content truncated - full content available in topic details) ..."
                        else:
                            enhanced_description += extracted_text
                        
                        # Add key sections if available
                        if content_info.get('key_sections'):
                            enhanced_description += "\n\nKEY SECTIONS FOUND:\n"
                            enhanced_description += "-" * 30 + "\n"
                            for section in content_info['key_sections'][:10]:  # Limit to 10 sections
                                enhanced_description += f"- {section['title']}\n"
                    
                    # Add special handling for markdown files
                    if file_type == 'markdown' and content_info.get('html_content'):
                        enhanced_description += "\n\nRENDERED MARKDOWN:\n"
                        enhanced_description += "-" * 30 + "\n"
                        enhanced_description += "(HTML content available for rich display)\n"
                    
                    # Create the topic with extracted content
                    topic = Topic.create(
                        title=title,
                        description=enhanced_description,
                        user_id=user.id
                    )
                    
                    if topic:
                        flash(f'Material "{title}" uploaded and processed successfully! Content extracted from {file_type.upper()} document.', 'success')
                        return redirect(url_for('topics.view_topic', topic_id=topic.id))
                    else:
                        flash('Failed to create topic for material.', 'error')
                else:
                    # Document processing failed, create topic with detailed error info
                    content_info = processing_result.get('content_info', {})
                    error_msg = processing_result.get('error', content_info.get('error', 'Unknown error'))
                    is_image_based = processing_result.get('is_image_based', content_info.get('is_image_based', False))
                    suggestions = processing_result.get('suggestions', content_info.get('suggestions', []))
                    file_info = processing_result.get('file_info', {})
                    
                    # Create enhanced error description
                    error_description = f"{description}\n\n"
                    error_description += f"Uploaded file: {file.filename}\n"
                    error_description += f"File size: {file_info.get('file_size', 0):,} bytes\n"
                    error_description += f"File type: {file_extension.upper()}\n"
                    extraction_method = processing_result.get('extraction_method', 'unknown')
                    if 'content_info' in processing_result and processing_result['content_info']:
                        extraction_method = processing_result['content_info'].get('extraction_method', extraction_method)
                    error_description += f"Extraction method attempted: {extraction_method}\n\n"
                    
                    if is_image_based:
                        error_description += "IMAGE-BASED PDF DETECTED\n"
                        error_description += "=" * 30 + "\n\n"
                        error_description += f"Issue: {error_msg}\n\n"
                        error_description += "SOLUTIONS:\n"
                        for i, suggestion in enumerate(suggestions, 1):
                            error_description += f"{i}. {suggestion}\n"
                        error_description += "\nNote: This PDF appears to be a scanned image rather than text-based content."
                    else:
                        error_description += f"{file_extension.upper()} Processing Error: {error_msg}\n\n"
                        
                        # Add suggestions if available
                        if suggestions:
                            error_description += "SUGGESTIONS:\n"
                            for i, suggestion in enumerate(suggestions, 1):
                                error_description += f"{i}. {suggestion}\n"
                        
                        # Add library installation info if needed
                        if "not available" in error_msg.lower():
                            required_libs = DocumentProcessor.get_required_libraries()
                            if required_libs:
                                error_description += f"\nRequired libraries: {', '.join(required_libs)}"
                    
                    topic = Topic.create(
                        title=title,
                        description=error_description,
                        user_id=user.id
                    )
                    
                    if topic:
                        if is_image_based:
                            flash(f'Material "{title}" uploaded but appears to be an image-based PDF. See topic details for solutions.', 'warning')
                        else:
                            flash(f'Material "{title}" uploaded but {file_extension.upper()} processing failed: {error_msg}', 'warning')
                        return redirect(url_for('topics.view_topic', topic_id=topic.id))
                    else:
                        flash('Failed to create topic for material.', 'error')
                        
            except Exception as e:
                flash(f'Error uploading material: {str(e)}', 'error')
        
        return render_template('topics/import_materials.html', form=form)
    
    except Exception as e:
        flash('Error loading upload page.', 'error')
        return redirect(url_for('topics.list_topics'))


@topics.route('/topics/test-document-processing')
@login_required
def test_document_processing():
    """Test route to verify document processing functionality"""
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        from app.utils.document_processor import DocumentProcessor
        
        # Check document processing availability
        available_formats = DocumentProcessor.is_document_processing_available()
        supported_formats = DocumentProcessor.get_supported_formats()
        required_libs = DocumentProcessor.get_required_libraries()
        
        result = {
            'available_formats': available_formats,
            'supported_formats': supported_formats,
            'required_libraries': required_libs,
            'status': 'ready' if any(available_formats.values()) else 'missing_libraries'
        }
        
        # Create detailed status display
        status_html = """
        <h2>Document Processing Status</h2>
        <div style="font-family: monospace; background: #f5f5f5; padding: 20px; border-radius: 5px;">
        """
        
        status_html += f"<h3>Supported Formats:</h3><ul>"
        for format_type in supported_formats:
            status = "✅" if available_formats.get(format_type, False) else "❌"
            status_html += f"<li>{status} {format_type.upper()}</li>"
        status_html += "</ul>"
        
        status_html += f"<h3>Library Status:</h3><ul>"
        for lib, available in available_formats.items():
            status = "✅ Available" if available else "❌ Missing"
            status_html += f"<li><strong>{lib}:</strong> {status}</li>"
        status_html += "</ul>"
        
        if required_libs:
            status_html += f"<h3>Missing Libraries:</h3><ul>"
            for lib in required_libs:
                status_html += f"<li>{lib}</li>"
            status_html += "</ul>"
        
        status_html += f"<p><strong>Overall Status:</strong> {result['status']}</p>"
        status_html += "</div>"
        status_html += '<p><a href="' + url_for('topics.import_materials') + '">← Back to Upload</a></p>'
        
        return status_html
        
    except Exception as e:
        return f"Error: {str(e)}"


@topics.route('/topics/<topic_id>/content', methods=['GET', 'POST'])
@login_required
def topic_content(topic_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topic = Topic.get_by_id(topic_id, user.id)
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        
        from app.models.content_management import TopicAttachment, TopicNote, TopicVersion, TopicTag
        
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        attachments = TopicAttachment.get_topic_attachments(topic_id, user.id)
        notes = TopicNote.get_topic_notes(topic_id, user.id)
        versions = TopicVersion.get_topic_versions(topic_id, user.id)
        available_tags = TopicTag.get_all_tags()
        
        
        content_form = TopicContentForm()
        content_form.tags.choices = [(tag.name, tag.name) for tag in available_tags]
        content_form.tags.data = topic.tags
        
        if content_form.validate_on_submit():
            
            success = Topic.update_topic_content(
                topic_id, user.id,
                title=content_form.title.data,
                description=content_form.description.data,
                notes=content_form.notes.data,
                tags=content_form.tags.data
            )
            
            if success:
                flash('Topic content updated successfully!', 'success')
                return redirect(url_for('topics.topic_content', topic_id=topic_id))
            else:
                flash('Error updating topic content.', 'error')
        
        
        content_form.title.data = topic.title
        content_form.description.data = topic.description
        content_form.notes.data = topic.notes
        
        return render_template('topics/content.html', 
                             topic=topic, 
                             attachments=attachments,
                             notes=notes,
                             versions=versions,
                             content_form=content_form)
    
    except Exception as e:
        flash('Error loading topic content.', 'error')
        return redirect(url_for('topics.list_topics'))


@topics.route('/topics/<topic_id>/notes/add', methods=['GET', 'POST'])
@login_required
def add_topic_note(topic_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topic = Topic.get_by_id(topic_id, user.id)
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        form = TopicNoteForm()
        
        if form.validate_on_submit():
            from app.models.content_management import TopicNote
            
            note = TopicNote.create_note(
                topic_id=topic_id,
                user_id=user.id,
                title=form.title.data,
                content=form.content.data,
                note_type=form.note_type.data,
                is_public=form.is_public.data
            )
            
            if note:
                flash('Note added successfully!', 'success')
                return redirect(url_for('topics.topic_content', topic_id=topic_id))
            else:
                flash('Error adding note.', 'error')
        
        return render_template('topics/add_note.html', topic=topic, form=form)
    
    except Exception as e:
        flash('Error adding note.', 'error')
        return redirect(url_for('topics.list_topics'))


@topics.route('/topics/<topic_id>/attachments/upload', methods=['GET', 'POST'])
@login_required
def upload_topic_attachment(topic_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topic = Topic.get_by_id(topic_id, user.id)
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        form = TopicAttachmentForm()
        
        if form.validate_on_submit():
            from app.models.content_management import TopicAttachment
            
            file = form.file.data
            if file:
                
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                
                
                file_path = f"uploads/{unique_filename}"
                
                attachment = TopicAttachment.create_attachment(
                    topic_id=topic_id,
                    user_id=user.id,
                    filename=unique_filename,
                    original_filename=file.filename,
                    file_path=file_path,
                    file_size=len(file.read()),
                    file_type=filename.split('.')[-1].lower(),
                    mime_type=file.content_type,
                    description=form.description.data,
                    is_public=form.is_public.data
                )
                
                if attachment:
                    flash('File uploaded successfully!', 'success')
                    return redirect(url_for('topics.topic_content', topic_id=topic_id))
                else:
                    flash('Error uploading file.', 'error')
        
        return render_template('topics/upload_attachment.html', topic=topic, form=form)
    
    except Exception as e:
        flash('Error uploading attachment.', 'error')
        return redirect(url_for('topics.list_topics'))


@topics.route('/topics/<topic_id>/versions')
@login_required
def topic_versions(topic_id):
    
    try:
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        topic = Topic.get_by_id(topic_id, user.id)
        if not topic:
            flash('Topic not found.', 'error')
            return redirect(url_for('topics.list_topics'))
        
        from app.models.content_management import TopicVersion
        user = get_current_user()
        if not user:
            flash('User not authenticated.', 'error')
            return redirect(url_for('auth.login'))
        
        versions = TopicVersion.get_topic_versions(topic_id, user.id)
        
        return render_template('topics/versions.html', topic=topic, versions=versions)
    
    except Exception as e:
        flash('Error loading version history.', 'error')
        return redirect(url_for('topics.list_topics'))


@topics.route('/topics/<topic_id>/versions/<int:version_number>/restore', methods=['POST'])
@login_required
def restore_topic_version(topic_id, version_number):
    
    try:
        from app.models.content_management import TopicVersion
        
        success = TopicVersion.restore_version(topic_id, version_number)
        
        if success:
            flash(f'Topic restored to version {version_number}!', 'success')
        else:
            flash('Error restoring version.', 'error')
        
        return redirect(url_for('topics.topic_versions', topic_id=topic_id))
    
    except Exception as e:
        flash('Error restoring version.', 'error')
        return redirect(url_for('topics.list_topics'))


@topics.route('/topics/search')
@login_required
def search_content():
    
    try:
        form = ContentSearchForm()
        
        
        from app.models.content_management import TopicTag
        available_tags = TopicTag.get_all_tags()
        form.tags.choices = [(tag.name, tag.name) for tag in available_tags]
        
        results = []
        query = request.args.get('query', '')
        selected_tags = request.args.getlist('tags')
        content_type = request.args.get('content_type', 'all')
        
        if query or selected_tags:
            if content_type in ['all', 'topics']:
                
                if selected_tags:
                    user = get_current_user()
                    if not user:
                        flash('User not authenticated.', 'error')
                        return redirect(url_for('auth.login'))
                    
                    topics = Topic.search_topics_by_tags(user.id, selected_tags)
                else:
                    user = get_current_user()
                    if not user:
                        flash('User not authenticated.', 'error')
                        return redirect(url_for('auth.login'))
                    
                    topics = Topic.get_all_by_user(user.id)
                    
                    
                    if query:
                        topics = [t for t in topics if query.lower() in t.title.lower() or 
                                 query.lower() in (t.description or '').lower()]
                    
                    results.extend([{'type': 'topic', 'data': t} for t in topics])
        
        return render_template('topics/search.html', 
                             form=form, 
                             results=results,
                             query=query,
                             selected_tags=selected_tags,
                             content_type=content_type)
    
    except Exception as e:
        flash('Error searching content.', 'error')
        return redirect(url_for('topics.list_topics'))


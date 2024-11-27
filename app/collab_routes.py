from flask import Blueprint, current_app, render_template, redirect, send_from_directory, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta

from app.email import send_email
from . import db
from .models import User, Request as RequestModel
from .forms import RequestForm

collab = Blueprint('collab', __name__)

UPLOAD_FOLDER = 'app/static/uploads/resumes'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Utility function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route to create a request
@collab.route('/create_request/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def create_request(receiver_id):
    professor = User.query.get(receiver_id)
    if not professor or professor.role.lower() != 'teacher/professor':
        flash('Invalid recipient selected.')
        return redirect(url_for('main.dashboard'))

    form = RequestForm()
    if form.validate_on_submit():
        expiration_date = datetime.utcnow() + timedelta(days=30)
        filename = None

        # Handle file upload if resume is provided
        if form.resume.data:
            if allowed_file(form.resume.data.filename):
                filename = secure_filename(form.resume.data.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                form.resume.data.save(file_path)
            else:
                flash('Only PDF files are allowed for resumes.')
                return redirect(url_for('collab.create_request', receiver_id=receiver_id))

        # Create the request
        new_request = RequestModel(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            name=form.name.data,
            email=form.email.data,
            resume=filename,
            message=form.message.data,
            status='Pending',
            expiration_date=expiration_date
        )
        db.session.add(new_request)
        db.session.commit()

        send_email(
            to_email=professor.email,
            subject="New Collaboration Request",
            body=f"""
            Hello {professor.user_name},
            You have received a new collaboration request from {form.name.data}.
            Message: {form.message.data or 'No message provided.'}
            Kind regards,
            The CollabHub Team
            """,
            cc_email=current_user.email  # CC the sender
        )

        flash('Request sent successfully!', 'success')
        return redirect(url_for('collab.my_requests'))

    return render_template('create_request.html', form=form, professor=professor)


# Route for professors to view received requests
@collab.route('/view_requests', methods=['GET'])
@login_required
def view_requests():
    if current_user.role.lower() != 'teacher/professor':
        flash('Access denied. This page is for professors only.', 'danger')
        return redirect(url_for('main.dashboard'))

    requests = RequestModel.query.filter_by(receiver_id=current_user.id).all()
    return render_template('view_requests.html', requests=requests)


# Route for students to view their sent requests
@collab.route('/my_requests', methods=['GET'])
@login_required
def my_requests():
    requests = RequestModel.query.filter_by(sender_id=current_user.id).all()
    return render_template('my_requests.html', requests=requests)


# Route for professors to approve or decline requests
@collab.route('/update_request/<int:request_id>/<string:status>', methods=['POST'])
@login_required
def update_request(request_id, status):
    if current_user.role.lower() != 'teacher/professor':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    request_instance = RequestModel.query.get(request_id)
    if not request_instance or request_instance.receiver_id != current_user.id:
        flash('Request not found.', 'danger')
        return redirect(url_for('collab.view_requests'))

    if status not in ['Accepted', 'Declined']:
        flash('Invalid status update.', 'danger')
        return redirect(url_for('collab.view_requests'))

    request_instance.status = status
    db.session.commit()
    flash(f'Request {status.lower()} successfully.', 'success')
    return redirect(url_for('collab.view_requests'))

@collab.route('/uploads/resumes/<filename>')
def download_resume(filename):
    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'resumes')
    return send_from_directory(uploads_dir, filename)
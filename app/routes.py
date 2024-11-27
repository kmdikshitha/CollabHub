from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms import ProfileForm
from app.models import Profile, User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('base.html')

@main.route('/CollabHub')
@login_required
def dashboard():
    return render_template('dashboard.html',user_name=current_user.user_name, user_role=current_user.role.lower())


@main.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    profile=Profile.query.filter_by(id=current_user.id).first()
    form=ProfileForm(obj=profile)

    if form.validate_on_submit():
        if profile:
            profile.name = form.name.data
            profile.email = form.email.data
            profile.bio = form.bio.data
            profile.research_areas = form.research_areas.data
            profile.publications = form.publications.data
            profile.location = form.location.data
        else:
            new_profile = Profile(
                user_id=current_user.id,
                name=form.name.data,
                email=form.email.data,
                bio=form.bio.data,
                research_areas=form.research_areas.data,
                publications=form.publications.data,
                location=form.location.data
            )
            db.session.add(new_profile)

        db.session.commit()
        flash('Profile saved successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('create_profile.html', form=form)

@main.route('/view_profiles')
@login_required
def view_profiles():
    search_query = request.args.get('search', '').lower()
    profiles = Profile.query.filter(Profile.user_id != current_user.id)
    if search_query:
        profiles = profiles.join(User).filter(
            (User.user_name.ilike(f"%{search_query}%")) |
            (User.email.ilike(f"%{search_query}%"))
        )
    profiles = profiles.all()
    return render_template('view_profiles.html', profiles=profiles)
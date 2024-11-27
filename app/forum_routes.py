from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.forms import ForumForm
from .models import Comment, Forum, User
from . import db
forum = Blueprint('forum', __name__)

# Route to display all forum posts
@forum.route('/forum_page', methods=['GET'])
@login_required
def forum_page():
    posts = db.session.query(Forum, User.user_name).join(User, Forum.user_id == User.id).order_by(Forum.time_stamp.desc()).all()   
    # for post, user_name in posts:
    #     post.comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.time_stamp.asc()).all()    
    # Add comments with their user names for each post
    posts_with_comments = []
    for post, user_name in posts:
        comments = db.session.query(Comment.content, Comment.time_stamp, User.user_name).join(User, Comment.user_id == User.id).filter(Comment.post_id == post.id).order_by(Comment.time_stamp.asc()).all()
        # Transform into a structured dictionary
        post_data = {
            "post": post,
            "user_name": user_name,
            "comments": [{"content": c.content, "user_name": c.user_name, "time_stamp": c.time_stamp} for c in comments],
        }
        posts_with_comments.append(post_data)
    return render_template('forum_page.html', posts=posts_with_comments)

# Route to create a new forum post
@forum.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = ForumForm()
    if form.validate_on_submit():
        new_post = Forum(
            user_id=current_user.id,
            title=form.title.data,
            body=form.body.data,
            time_stamp=datetime.utcnow(),
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been successfully created!', 'success')
        return redirect(url_for('forum.forum_page'))
    return render_template('create_post.html', form=form)

@forum.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content')
    if content:
        comment = Comment(post_id=post_id, user_id=current_user.id, content=content)
        db.session.add(comment)
        db.session.commit()
        flash("Comment added successfully!", "success")
    else:
        flash("Comment cannot be empty.", "error")
    return redirect(url_for('forum.forum_page'))

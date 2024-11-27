from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Enum

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(Enum('Student', 'Teacher/Professor', name='role_enum'), nullable=False)
    department=db.Column(db.String(150), nullable=False)
    institution = db.Column(db.String(120), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)
    forums = db.relationship('Forum', backref='user', lazy=True)
    sent_requests = db.relationship('Request', foreign_keys='Request.sender_id', backref='sender', lazy=True)
    received_requests = db.relationship('Request', foreign_keys='Request.receiver_id', backref='receiver', lazy=True)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    research_areas = db.Column(db.JSON, nullable=False)
    publications = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=False)

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True)
    
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Who is sending
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Who is receiving
    name = db.Column(db.String(120), nullable=False)  # Sender's full name
    email = db.Column(db.String(120), nullable=False)  # Sender's email
    resume = db.Column(db.String(300), nullable=True)  # Path to uploaded resume
    message = db.Column(db.Text, nullable=True)  # Optional message
    status = db.Column(Enum('Pending', 'Accepted', 'Declined', 'Expired', name='status_enum'), nullable=False, default = 'pending')
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp
    expiration_date = db.Column(db.DateTime, nullable=False)
    # sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_requests')  # Relate to sender
    # receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_requests')  # Relate to receiver

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)

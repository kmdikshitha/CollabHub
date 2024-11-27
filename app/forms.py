from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()],render_kw={"class": "form"})
    user_name=StringField('Username', validators=[DataRequired()],render_kw={"class": "form"})
    password= PasswordField('Password', validators=[DataRequired()],render_kw={"class": "form"})
    confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],render_kw={"class": "form"})
    role=SelectField('Role', choices=[('Student', 'Student'),('Teacher/Professor' , 'Teacher/Professor')], validators=[DataRequired()], render_kw={"class": "form"})
    department=StringField('Department', validators=[DataRequired()], render_kw={"class": "form"})
    institution=StringField('Institution', validators=[DataRequired()], render_kw={"class": "form"})
    submit= SubmitField('Register',render_kw={"class": "btn btn-primary"})

class LoginForm(FlaskForm):
    email_or_username=StringField('Email or Username', validators=[DataRequired()],render_kw={"class": "form"})
    password= PasswordField('Password', validators=[DataRequired()],render_kw={"class": "form"})
    submit=SubmitField('Login', render_kw={"class": "btn btn-primary"})

class RequestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"class": "form"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form"})
    resume = FileField('Resume (PDF only)', render_kw={"class": "form"})
    message = TextAreaField('Message (Optional)', render_kw={"class": "form"})
    submit = SubmitField('Send Request', render_kw={"class": "btn btn-primary"})

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"class": "form"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form"})
    bio = TextAreaField('Bio', validators=[DataRequired()], render_kw={"class": "form"})
    research_areas = TextAreaField('Research Areas (comma-separated)', validators=[DataRequired()], render_kw={"class": "form"})
    publications = TextAreaField('Publications', validators=[DataRequired()], render_kw={"class": "form"})
    location = StringField('Location', validators=[DataRequired()], render_kw={"class": "form"})
    submit = SubmitField('Save Profile', render_kw={"class": "btn btn-primary"})

class ForumForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=500)], render_kw={"class": "form"})
    body = TextAreaField('Body', validators=[DataRequired(), Length(max=5000)], render_kw={"class": "form"})
    submit = SubmitField('Post', render_kw={"class": "btn btn-primary"})

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search', render_kw={"class": "btn btn-primary"})



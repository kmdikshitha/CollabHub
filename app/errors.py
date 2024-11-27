from flask import Blueprint, render_template
from app import app  # or your 'create_app' function

# Create an error blueprint
errors = Blueprint('errors', __name__)

# Catch all 500 errors (Internal Server Errors)
@errors.app_errorhandler(500)
def internal_server_error(error):
    # Log the error here if needed
    return render_template('error.html', error=error), 500

# Catch all 404 errors (Page Not Found)
@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error="Page not found"), 404

# Catch any specific exceptions, like SQLAlchemy errors
from sqlalchemy.exc import SQLAlchemyError
@errors.app_errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    return render_template('error.html', error="A database error occured"), 500

@errors.app_errorhandler(401)
def unauthorized_error(error):
    return render_template('error.html', error="Unauthorized access. Please log in."), 401


import os

# General Config
SECRET_KEY = os.environ.get('SECRET_KEY') or 'randomtestforcollabhub'  # Replace 'your_secret_key' with something more secure.

# Database Config
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'  # SQLite as fallback, use a proper DB in production.
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Recommended to keep this False to save resources.

# Scheduler Config (Optional, for Background Jobs)
SCHEDULER_API_ENABLED = True

# Debug Mode (for development only)
DEBUG = os.environ.get('FLASK_DEBUG') == '1'

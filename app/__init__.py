from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler

db= SQLAlchemy()
migrate=Migrate()
login_manager= LoginManager()

def create_app(config_filename=None):
    app=Flask(__name__, static_folder='static')
    app.config.from_pyfile(config_filename or './config.py')

    #Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)

    #Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    from .collab_routes import collab as collab_blueprint
    app.register_blueprint(collab_blueprint, url_prefix = '/collab')

    from .forum_routes import forum as forum_blueprint
    app.register_blueprint(forum_blueprint, url_prefix = '/forum')

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)


    scheduler = BackgroundScheduler()
    from app.email import check_expirations_and_notify
    scheduler.add_job(func=check_expirations_and_notify, trigger="interval", hours=24)
    scheduler.start()

    return app

    
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


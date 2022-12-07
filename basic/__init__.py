from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from basic.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
root_path = ''


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from basic.Users.routes import users
    from basic.Pics.routes import pics
    from basic.main.routes import main
    from basic.errors.handlers import  errors

    app.register_blueprint(users)
    app.register_blueprint(pics)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    root_path = app.root_path
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    return app
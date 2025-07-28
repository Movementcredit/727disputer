from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    
    login.login_view = 'auth.login'

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.disputer import bp as disputer_bp
    app.register_blueprint(disputer_bp)

    from app.funnel import bp as funnel_bp
    app.register_blueprint(funnel_bp)

    from app.crm import bp as crm_bp
    app.register_blueprint(crm_bp)

    return app
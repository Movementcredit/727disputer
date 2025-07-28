from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

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

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.disputer.routes import disputer_bp
    app.register_blueprint(disputer_bp)

    from app.funnel.routes import funnel_bp
    app.register_blueprint(funnel_bp)

    from app.crm.routes import crm_bp
    app.register_blueprint(crm_bp)

    return app

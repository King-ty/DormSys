from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# from flask_login import LoginManager
from flask_cors import CORS
from flask_redis import FlaskRedis
from config import config
import os
from flask_migrate import Migrate

mail = Mail()
db = SQLAlchemy()

# login_manager = LoginManager()
# login_manager.login_view = "user.login"

redis_client = FlaskRedis(decode_responses=True)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    CORS(app, supports_credentials=True)  # cors解决跨域

    mail.init_app(app)
    db.init_app(app)
    # login_manager.init_app(app)
    redis_client.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix="/api")

    from .user import user as user_blueprint

    app.register_blueprint(user_blueprint, url_prefix="/api/user")

    from .dormitory import dormitory as dormitory_blueprint

    app.register_blueprint(dormitory_blueprint, url_prefix="/api/dormitory")

    from .building import building as building_blueprint

    app.register_blueprint(building_blueprint, url_prefix="/api/building")

    return app


app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)

from app import commands

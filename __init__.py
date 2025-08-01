from flask import Flask
from .extensions import db, login_manager,migrate,csrf
from flask_wtf.csrf import generate_csrf
from .config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    csrf.init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    from .models import User  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    print("✅ Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    from .routes import register_blueprints
    register_blueprints(app)
    @app.context_processor
    def inject_csrf_token():
     return dict(new_token=generate_csrf())
    return app




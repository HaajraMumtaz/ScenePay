from .main_routes import main
from .upload_routes import upload_bp

def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(upload_bp)
    print(app.url_map)


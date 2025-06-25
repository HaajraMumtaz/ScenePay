from .main_routes import main
def register_blueprints(app):
    app.register_blueprint(main)

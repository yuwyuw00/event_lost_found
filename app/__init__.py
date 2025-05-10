from flask import Flask, render_template  # Add render_template here
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import logging

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    load_dotenv()  # Load environment variables from .env file

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config')  # Load default config
    app.config.from_pyfile('config.py', silent=True)  # Load from config.py, if exists

    # Set up logging
    log_level = app.config.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=log_level)
    app.logger.setLevel(log_level)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Setup login manager
    login_manager.login_view = "auth.login"  # Ensure users are redirected to login if needed
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User  # Import here to avoid circular import
        return User.query.get(int(user_id))

    # Register the blueprints
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    # Register the dashboard blueprint
    from app.controllers.dashboard_controller import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Register the event blueprint
    from app.controllers.event_controller import event_bp
    app.register_blueprint(event_bp)

    # Register the item blueprint (if applicable)
    from app.controllers.item_controller import item_bp
    app.register_blueprint(item_bp)

    # Error handling: 404 and 500
    @app.errorhandler(404)
    def page_not_found(error):
        app.logger.error(f"404 error: {error}")
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(f"500 error: {error}")
        return render_template('errors/500.html'), 500

    return app

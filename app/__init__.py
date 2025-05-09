from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    load_dotenv()  # Load environment variables from .env file
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config')
    app.config.from_pyfile('config.py', silent=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register the blueprints
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    # Import the User model directly (NO circular import)
    from app.models.user import User

    # Setup login manager
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register the dashboard blueprint
    from app.controllers.dashboard_controller import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Register the event blueprint
    from app.controllers.event_controller import event_bp
    app.register_blueprint(event_bp)

    # Register the item blueprint (if applicable)
    from app.controllers.item_controller import item_bp
    app.register_blueprint(item_bp)

    return app

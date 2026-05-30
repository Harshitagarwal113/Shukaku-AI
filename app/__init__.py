from flask import Flask
from config import config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Global limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["180 per day", "40 per hour"],
    storage_uri="memory://"
)

def create_app(config_name='default'):
    """Flask application factory."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize limiter
    limiter.init_app(app)
    
    # Register blueprints/routes
    from app.web.routes import web_bp
    app.register_blueprint(web_bp)
    
    return app

from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Initialize CORS - Enable for all domains and all routes
    cors.init_app(app, 
                  origins=['*'],  # Allow all origins for development
                  methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
                  allow_headers=['Content-Type', 'Authorization'],
                  supports_credentials=True)
    
    # Import models here - PENTING untuk Flask-Migrate!
    with app.app_context():
        from app.models import user  # Import semua models
    
    # Register blueprints
    from app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    
    # Add a simple health check endpoint
    @app.route('/')
    def health_check():
        return {'message': 'Flask API is running!', 'status': 'success'}, 200
    
    @app.route('/health')
    def health():
        return {'message': 'API is healthy', 'status': 'success'}, 200
    
    return app
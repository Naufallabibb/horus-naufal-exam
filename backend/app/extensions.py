"""
Flask extensions initialization
Extensions yang digunakan dalam aplikasi Flask
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Inisialisasi extensions
# Extensions akan diinisialisasi dengan aplikasi Flask di app/__init__.py

# Database ORM
db = SQLAlchemy()

# Database Migration
migrate = Migrate()

# Cross-Origin Resource Sharing untuk frontend
cors = CORS()

# JSON Web Token untuk autentikasi
jwt = JWTManager()

# Callback untuk JWT error handling
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {
        'status': 'error',
        'message': 'Token has expired',
        'code': 'token_expired'
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'status': 'error', 
        'message': 'Invalid token',
        'code': 'invalid_token'
    }, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
        'status': 'error',
        'message': 'Authorization token is required', 
        'code': 'authorization_required'
    }, 401
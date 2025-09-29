from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.utils.validators import validate_user_data, validate_login_data, validate_update_data

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate request data
        is_valid, error_message = validate_user_data(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == data['username']) | 
            (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({'error': 'Username atau email sudah terdaftar'}), 409
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            nama=data['nama']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registrasi berhasil',
            'data': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Terjadi kesalahan server: {str(e)}'}), 500

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate request data
        is_valid, error_message = validate_login_data(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Find user by username
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Username atau password salah'}), 401
        
        # Create access token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login berhasil',
            'token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan server: {str(e)}'}), 500

@users_bp.route('', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)
        
        # Build query
        query = User.query
        
        # Add search filter if provided
        if search:
            query = query.filter(
                (User.nama.contains(search)) |
                (User.username.contains(search)) |
                (User.email.contains(search))
            )
        
        # Execute query with pagination
        if per_page > 0:
            users_paginated = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            users = users_paginated.items
            total = users_paginated.total
        else:
            users = query.all()
            total = len(users)
        
        users_data = [user.to_dict() for user in users]
        
        return jsonify({
            'message': 'Data users berhasil diambil',
            'data': users_data,
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan server: {str(e)}'}), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User tidak ditemukan'}), 404
        
        return jsonify({
            'message': 'Data user berhasil diambil',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan server: {str(e)}'}), 500

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate request data
        is_valid, error_message = validate_update_data(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Find user by ID
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User tidak ditemukan'}), 404
        
        # Check if username or email already exists for other users
        existing_user = User.query.filter(
            ((User.username == data.get('username')) | 
             (User.email == data.get('email'))) &
            (User.id != user_id)
        ).first()
        
        if existing_user:
            return jsonify({'error': 'Username atau email sudah digunakan pengguna lain'}), 409
        
        # Update user data
        if 'username' in data and data['username']:
            user.username = data['username']
        if 'email' in data and data['email']:
            user.email = data['email']
        if 'nama' in data and data['nama']:
            user.nama = data['nama']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Data user berhasil diperbarui',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Terjadi kesalahan server: {str(e)}'}), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        # Find user by ID
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User tidak ditemukan'}), 404
        
        # Get current user ID from JWT token
        current_user_id = int(get_jwt_identity())
        
        # Prevent user from deleting themselves
        if user_id == current_user_id:
            return jsonify({'error': 'Anda tidak dapat menghapus akun Anda sendiri'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User berhasil dihapus',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Terjadi kesalahan server: {str(e)}'}), 500

# Additional endpoint for getting current user profile
@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User tidak ditemukan'}), 404
        
        return jsonify({
            'message': 'Data user berhasil diambil',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan server: {str(e)}'}), 500

# Logout endpoint (optional - for token blacklisting if implemented)
@users_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # In a more advanced implementation, you might want to blacklist the token
        # For now, we'll just return a success message
        # The actual logout logic happens on the frontend by removing the token
        
        return jsonify({
            'message': 'Logout berhasil'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan server: {str(e)}'}), 500
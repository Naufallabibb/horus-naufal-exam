from app.models.user import User
from app.extensions import db

class UserService:
    @staticmethod
    def create_user(username, password, email, nama):
        """Create a new user"""
        user = User(username=username, email=email, nama=nama)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        return User.query.all()
    
    @staticmethod
    def update_user(user, **kwargs):
        """Update user data"""
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user):
        """Delete user"""
        db.session.delete(user)
        db.session.commit()
    
    @staticmethod
    def user_exists(username=None, email=None, exclude_id=None):
        """Check if user exists by username or email"""
        query = User.query
        
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        
        if username and email:
            return query.filter((User.username == username) | (User.email == email)).first() is not None
        elif username:
            return query.filter_by(username=username).first() is not None
        elif email:
            return query.filter_by(email=email).first() is not None
        
        return False
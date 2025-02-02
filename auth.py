from functools import wraps
from flask import request, redirect, url_for, flash
from flask_login import current_user
import jwt
from datetime import datetime, timedelta
from app import app

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need administrator privileges to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_token(user_id: int) -> str:
    """Generate JWT token for API authentication."""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return {'message': 'Token is missing'}, 401
            
        try:
            token = token.split('Bearer ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return {'message': 'Invalid token'}, 401
            
        return f(current_user_id, *args, **kwargs)
    
    return decorated

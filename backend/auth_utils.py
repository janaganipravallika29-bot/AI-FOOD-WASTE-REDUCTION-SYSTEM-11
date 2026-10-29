"""
FoodWise AI - Authentication Utilities
Handles JWT/itsdangerous token generation, verification, password strength checks,
and route protection decorators.
"""
import os
import re
from functools import wraps
from flask import request, jsonify, g
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

# Secret key resolution
SECRET_KEY = os.environ.get('SECRET_KEY', 'foodwise-ai-super-secret-production-key-2026-secure')
AUTH_SALT = 'foodwise-auth-token'
RESET_SALT = 'foodwise-reset-token'

serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_auth_token(user_id, role='user', expires_in=7 * 86400):
    """
    Generate a signed, tamper-proof session token.
    Default expiry: 7 days.
    """
    payload = {
        'uid': user_id,
        'role': role
    }
    return serializer.dumps(payload, salt=AUTH_SALT)


def verify_auth_token(token, max_age=7 * 86400):
    """
    Verify and decode a session token.
    Returns payload dictionary or None if invalid/expired.
    """
    if not token:
        return None
    try:
        data = serializer.loads(token, salt=AUTH_SALT, max_age=max_age)
        return data
    except (SignatureExpired, BadSignature, Exception):
        return None


def generate_reset_token(user_id):
    """
    Generate a secure 1-hour password reset token.
    """
    return serializer.dumps({'uid': user_id}, salt=RESET_SALT)


def verify_reset_token(token, max_age=3600):
    """
    Verify 1-hour password reset token.
    """
    if not token:
        return None
    try:
        data = serializer.loads(token, salt=RESET_SALT, max_age=max_age)
        return data.get('uid')
    except (SignatureExpired, BadSignature, Exception):
        return None


def validate_password_strength(password):
    """
    Validates that password has at least 8 characters,
    at least one number, and at least one letter.
    """
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    return True, ""


def get_token_from_request():
    """Extract auth token from Authorization header or fw_session cookie."""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:].strip()
    cookie_token = request.cookies.get('fw_session')
    if cookie_token:
        return cookie_token.strip()
    return None


def login_required(f):
    """
    Decorator to protect routes requiring an authenticated user.
    Loads and attaches current_user to Flask `g`.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from backend.models import db, User

        token = get_token_from_request()
        if not token:
            return jsonify({'success': False, 'message': 'Authentication required. Please sign in.'}), 401

        payload = verify_auth_token(token)
        if not payload or 'uid' not in payload:
            return jsonify({'success': False, 'message': 'Session expired or invalid. Please sign in again.'}), 401

        user = db.session.get(User, payload['uid'])
        if not user or user.status != 'active':
            return jsonify({'success': False, 'message': 'User account not found or suspended.'}), 401

        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorator to protect routes requiring an administrator role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from backend.models import db, User

        token = get_token_from_request()
        if not token:
            return jsonify({'success': False, 'message': 'Administrator authentication required.'}), 401

        payload = verify_auth_token(token)
        if not payload or 'uid' not in payload:
            return jsonify({'success': False, 'message': 'Session expired or invalid.'}), 401

        user = db.session.get(User, payload['uid'])
        if not user or user.status != 'active':
            return jsonify({'success': False, 'message': 'Account not found or suspended.'}), 401

        if user.role != 'admin':
            return jsonify({'success': False, 'message': 'Access forbidden: Administrator privileges required.'}), 403

        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function


def set_auth_cookie(response, token, remember=True):
    """Set secure HttpOnly authentication cookie on response object."""
    max_age = 30 * 86400 if remember else 86400
    is_prod = os.environ.get('VERCEL') == '1' or os.environ.get('ENV') == 'production'
    response.set_cookie(
        'fw_session',
        token,
        max_age=max_age,
        httponly=True,
        secure=is_prod,
        samesite='Lax',
        path='/'
    )
    return response


def clear_auth_cookie(response):
    """Clear authentication cookie from response."""
    response.set_cookie('fw_session', '', expires=0, path='/')
    return response

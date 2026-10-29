"""
FoodWise AI - Database Models
Defines User, Food, and PredictionLog tables with SQLAlchemy.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default='user', nullable=False)  # 'user', 'admin', 'demo'
    status = db.Column(db.String(30), default='active', nullable=False)  # 'active', 'suspended'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Password reset support
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expires_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    foods = db.relationship('Food', backref='owner', cascade='all, delete-orphan', lazy=True)
    predictions = db.relationship('PredictionLog', backref='user', cascade='all, delete-orphan', lazy=True)

    def set_password(self, password):
        """Generate secure salted hash for password."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify plain password against hashed password."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_counts=False):
        """Return public dictionary representation of user."""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        if include_counts:
            data['food_count'] = len(self.foods) if self.foods else 0
            data['prediction_count'] = len(self.predictions) if self.predictions else 0
        return data


class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    food_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='other')
    quantity = db.Column(db.Float, nullable=False, default=1.0)
    unit = db.Column(db.String(30), nullable=False, default='kg')
    storage_type = db.Column(db.String(50), nullable=False, default='refrigerator')
    purchase_date = db.Column(db.String(20), nullable=True)
    expiry_date = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(30), nullable=False, default='fresh')  # 'fresh', 'near_expiry', 'expired', 'consumed', 'wasted'
    risk = db.Column(db.String(20), nullable=False, default='low')  # 'low', 'medium', 'high'
    risk_score = db.Column(db.Integer, nullable=False, default=0)
    notes = db.Column(db.Text, nullable=True)
    wasted_qty = db.Column(db.Float, nullable=True, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'food_name': self.food_name,
            'category': self.category,
            'quantity': self.quantity,
            'unit': self.unit,
            'storage_type': self.storage_type,
            'purchase_date': self.purchase_date,
            'expiry_date': self.expiry_date,
            'status': self.status,
            'risk': self.risk,
            'risk_score': self.risk_score,
            'notes': self.notes or '',
            'wasted_qty': self.wasted_qty or 0.0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PredictionLog(db.Model):
    __tablename__ = 'prediction_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    food_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    risk_score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(20), nullable=False, default='low')
    confidence = db.Column(db.Float, nullable=False, default=0.85)
    spoilage_factors = db.Column(db.Text, nullable=True)
    recommendations = db.Column(db.Text, nullable=True)  # JSON or text
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'food_name': self.food_name,
            'category': self.category,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'confidence': self.confidence,
            'spoilage_factors': self.spoilage_factors,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


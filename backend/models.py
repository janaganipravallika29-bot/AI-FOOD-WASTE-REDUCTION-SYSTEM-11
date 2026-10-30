"""
FoodWise AI - Database Models
Defines User, NGO, Food, Donation, PickupDetail, and PredictionLog tables with SQLAlchemy.
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
    role = db.Column(db.String(30), default='user', nullable=False)  # 'user' (donor), 'ngo', 'admin', 'demo'
    status = db.Column(db.String(30), default='active', nullable=False)  # 'active', 'suspended'
    phone = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Password reset support
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expires_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    foods = db.relationship('Food', backref='owner', cascade='all, delete-orphan', lazy=True)
    predictions = db.relationship('PredictionLog', backref='user', cascade='all, delete-orphan', lazy=True)
    donations = db.relationship('Donation', backref='donor', foreign_keys='Donation.donor_id', cascade='all, delete-orphan', lazy=True)
    ngo_profile = db.relationship('NGO', backref='account', uselist=False, cascade='all, delete-orphan', lazy=True)

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
            'phone': self.phone or '',
            'address': self.address or '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        if self.ngo_profile:
            data['ngo_id'] = self.ngo_profile.id
            data['ngo_name'] = self.ngo_profile.name
            data['ngo_verified'] = self.ngo_profile.is_verified
        if include_counts:
            data['food_count'] = len(self.foods) if self.foods else 0
            data['prediction_count'] = len(self.predictions) if self.predictions else 0
            data['donation_count'] = len(self.donations) if self.donations else 0
        return data


class NGO(db.Model):
    __tablename__ = 'ngos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    name = db.Column(db.String(180), nullable=False, index=True)
    reg_number = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False, default='Citywide')
    accepted_food_types = db.Column(db.String(255), nullable=False, default='Cooked Meals, Raw Veggies, Bakery, Groceries')
    capacity_kg = db.Column(db.Float, nullable=False, default=150.0)
    is_verified = db.Column(db.Boolean, nullable=False, default=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    donations = db.relationship('Donation', backref='target_ngo', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'reg_number': self.reg_number,
            'contact_person': self.contact_person,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'accepted_food_types': self.accepted_food_types,
            'capacity_kg': self.capacity_kg,
            'is_verified': self.is_verified,
            'description': self.description or '',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


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
    expiry_date = db.Column(db.String(30), nullable=True)
    prep_time = db.Column(db.String(30), nullable=True)  # Preparation time / date
    location = db.Column(db.String(255), nullable=True)   # Donor pickup location
    image_url = db.Column(db.Text, nullable=True)         # Food image data URL or path
    status = db.Column(db.String(30), nullable=False, default='fresh')  # 'fresh', 'near_expiry', 'expired', 'consumed', 'wasted', 'donated'
    risk = db.Column(db.String(20), nullable=False, default='low')  # 'low', 'medium', 'high'
    risk_score = db.Column(db.Integer, nullable=False, default=0)
    donation_status = db.Column(db.String(30), nullable=False, default='not_donated') # 'not_donated', 'pending', 'accepted', 'completed'
    donation_suitable = db.Column(db.String(30), nullable=False, default='safe') # 'safe', 'use_soon', 'unsafe'
    notes = db.Column(db.Text, nullable=True)
    wasted_qty = db.Column(db.Float, nullable=True, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    donations = db.relationship('Donation', backref='food_item', cascade='all, delete-orphan', lazy=True)

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
            'prep_time': self.prep_time or '',
            'location': self.location or '',
            'image_url': self.image_url or '',
            'status': self.status,
            'risk': self.risk,
            'risk_score': self.risk_score,
            'donation_status': self.donation_status,
            'donation_suitable': self.donation_suitable,
            'notes': self.notes or '',
            'wasted_qty': self.wasted_qty or 0.0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id', ondelete='CASCADE'), nullable=False, index=True)
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngos.id', ondelete='CASCADE'), nullable=False, index=True)
    status = db.Column(db.String(40), nullable=False, default='Pending') 
    # Status values: 'Pending', 'Accepted', 'Rejected', 'Pickup Scheduled', 'Collected', 'Delivered', 'Completed'
    donor_notes = db.Column(db.Text, nullable=True)
    ngo_notes = db.Column(db.Text, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    pickup = db.relationship('PickupDetail', backref='donation', uselist=False, cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'donor_name': self.donor.name if self.donor else 'Donor',
            'donor_phone': self.donor.phone if self.donor else '',
            'donor_location': self.food_item.location if self.food_item and self.food_item.location else (self.donor.address if self.donor else ''),
            'food_id': self.food_id,
            'food_name': self.food_item.food_name if self.food_item else 'Food',
            'food_category': self.food_item.category if self.food_item else 'other',
            'food_quantity': self.food_item.quantity if self.food_item else 1,
            'food_unit': self.food_item.unit if self.food_item else 'kg',
            'food_prep_time': self.food_item.prep_time if self.food_item else '',
            'food_expiry': self.food_item.expiry_date if self.food_item else '',
            'food_image': self.food_item.image_url if self.food_item else '',
            'ai_risk_score': self.food_item.risk_score if self.food_item else 0,
            'ai_suitable': self.food_item.donation_suitable if self.food_item else 'safe',
            'ngo_id': self.ngo_id,
            'ngo_name': self.target_ngo.name if self.target_ngo else 'NGO',
            'ngo_contact': self.target_ngo.contact_person if self.target_ngo else '',
            'ngo_phone': self.target_ngo.phone if self.target_ngo else '',
            'ngo_address': self.target_ngo.address if self.target_ngo else '',
            'status': self.status,
            'donor_notes': self.donor_notes or '',
            'ngo_notes': self.ngo_notes or '',
            'rejection_reason': self.rejection_reason or '',
            'pickup': self.pickup.to_dict() if self.pickup else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PickupDetail(db.Model):
    __tablename__ = 'pickup_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donation_id = db.Column(db.Integer, db.ForeignKey('donations.id', ondelete='CASCADE'), nullable=False, unique=True)
    scheduled_time = db.Column(db.String(100), nullable=True)
    agent_name = db.Column(db.String(120), nullable=True)
    agent_phone = db.Column(db.String(50), nullable=True)
    vehicle_info = db.Column(db.String(100), nullable=True)
    pickup_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'donation_id': self.donation_id,
            'scheduled_time': self.scheduled_time or '',
            'agent_name': self.agent_name or '',
            'agent_phone': self.agent_phone or '',
            'vehicle_info': self.vehicle_info or '',
            'pickup_notes': self.pickup_notes or '',
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
    donation_suitable = db.Column(db.String(30), nullable=False, default='safe')  # 'safe', 'use_soon', 'unsafe'
    spoilage_factors = db.Column(db.Text, nullable=True)
    recommendations = db.Column(db.Text, nullable=True)
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
            'donation_suitable': self.donation_suitable,
            'spoilage_factors': self.spoilage_factors,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

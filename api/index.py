"""
FoodWise AI - Primary Application & API Entry Point
Compatible with Vercel Serverless Functions and standalone local Flask runner.
Integrates Food Waste AI Prediction and Instant NGO Food Donation Workflow.
"""
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

from flask import Flask, request, jsonify, make_response, send_from_directory, g
from dotenv import load_dotenv

# Load local environment if .env exists
load_dotenv()

from backend.models import db, User, NGO, Food, Donation, PickupDetail, PredictionLog, Notification
from backend.database import configure_database, seed_initial_data
from backend.auth_utils import (
    generate_auth_token, verify_auth_token, generate_reset_token, verify_reset_token,
    validate_password_strength, login_required, admin_required, ngo_required,
    set_auth_cookie, clear_auth_cookie
)
from backend.ai_engine import calculate_waste_risk

# Directory configuration for static files
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PAGES_DIR = os.path.join(BASE_DIR, 'pages')

app = Flask(__name__, static_folder=BASE_DIR)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'foodwise-ai-super-secret-production-key-2026-secure')

# Configure database
configure_database(app)

# Ensure database tables exist and are seeded
with app.app_context():
    try:
        db.create_all()
        seed_initial_data()
    except Exception as e:
        print(f"[Init Error] Database setup notice: {e}")


# ============================================================================
# CORS & OPTIONS PREFLIGHT HANDLER
# ============================================================================
@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        res = make_response('', 204)
        origin = request.headers.get('Origin')
        if origin:
            res.headers['Access-Control-Allow-Origin'] = origin
            res.headers['Access-Control-Allow-Credentials'] = 'true'
        else:
            res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept'
        res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        return res


@app.after_request
def apply_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    else:
        response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route('/api/signup', methods=['POST', 'OPTIONS'])
def signup():
    """Register either a regular Donor/User or an NGO Organization."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    role = (data.get('role') or 'user').strip().lower()
    phone = (data.get('phone') or '').strip()
    address = (data.get('address') or '').strip()

    # NGO specific fields
    reg_number = (data.get('reg_number') or '').strip()
    city = (data.get('city') or 'Citywide').strip()
    accepted_food_types = (data.get('accepted_food_types') or 'Cooked Meals, Raw Veggies, Bakery, Groceries').strip()
    capacity_kg = float(data.get('capacity_kg') or 150.0)

    # Validation
    if not name:
        return jsonify({'success': False, 'message': 'Full name or Organization name is required.'}), 400

    if not email or not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'message': 'A valid email address is required.'}), 400

    valid_pwd, pwd_err = validate_password_strength(password)
    if not valid_pwd:
        return jsonify({'success': False, 'message': pwd_err}), 400

    # Duplicate check
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'An account with this email address already exists. Please sign in.'}), 409

    try:
        user_role = 'ngo' if role == 'ngo' else 'user'
        new_user = User(
            name=name,
            email=email,
            role=user_role,
            status='active',
            phone=phone,
            address=address
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # If registered as NGO, create linked NGO profile
        if user_role == 'ngo':
            new_ngo = NGO(
                user_id=new_user.id,
                name=name,
                reg_number=reg_number or f"NGO-{datetime.utcnow().strftime('%Y%m%d%H%M')}",
                contact_person=name,
                email=email,
                phone=phone or '+91 98000 00000',
                address=address or 'Main NGO Office',
                city=city,
                accepted_food_types=accepted_food_types,
                capacity_kg=capacity_kg,
                is_verified=True,
                description=data.get('description') or 'Registered Food Rescue NGO Organization.'
            )
            db.session.add(new_ngo)
            db.session.commit()
        else:
            # Starter food items for regular donors
            today = datetime.utcnow().date()
            starter_foods = [
                Food(
                    user_id=new_user.id,
                    food_name='Fresh Apples',
                    category='fruits',
                    quantity=3.0,
                    unit='kg',
                    storage_type='refrigerator',
                    purchase_date=today.isoformat(),
                    expiry_date=(today + timedelta(days=8)).isoformat(),
                    prep_time='Fresh Farm Harvest',
                    location=address or 'Home Kitchen',
                    status='fresh',
                    risk='low',
                    risk_score=15,
                    donation_suitable='safe',
                    notes='Welcome to FoodWise AI! You can donate surplus food directly to NGOs.'
                ),
                Food(
                    user_id=new_user.id,
                    food_name='Cooked Rice & Lentil Curry',
                    category='cooked',
                    quantity=10.0,
                    unit='pack',
                    storage_type='countertop',
                    purchase_date=today.isoformat(),
                    expiry_date=(today + timedelta(days=1)).isoformat(),
                    prep_time='Prepared today at 11:30 AM',
                    location=address or 'Catering Kitchen',
                    status='fresh',
                    risk='medium',
                    risk_score=44,
                    donation_suitable='use_soon',
                    notes='Fresh surplus meal boxes suitable for rapid donation.'
                )
            ]
            db.session.add_all(starter_foods)
            db.session.commit()

        token = generate_auth_token(new_user.id, role=new_user.role)
        res_data = {
            'success': True,
            'message': f"Account created successfully as {'NGO Organization' if user_role == 'ngo' else 'Donor'}! Welcome to FoodWise AI.",
            'token': token,
            'user': new_user.to_dict()
        }
        res = make_response(jsonify(res_data), 201)
        return set_auth_cookie(res, token, remember=True)

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500


@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    remember = bool(data.get('remember', True))

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401

    if user.status != 'active':
        return jsonify({'success': False, 'message': 'This account has been deactivated. Please contact support.'}), 403

    user.last_login = datetime.utcnow()
    db.session.commit()

    token = generate_auth_token(user.id, role=user.role, expires_in=30 * 86400 if remember else 86400)
    
    # Guide frontend to correct dashboard depending on role
    redirect_target = 'dashboard.html'
    if user.role == 'ngo':
        redirect_target = 'ngo_dashboard.html'
    elif user.role == 'admin':
        redirect_target = 'admin.html'

    res_data = {
        'success': True,
        'message': f'Welcome back, {user.name}!',
        'token': token,
        'user': user.to_dict(),
        'redirect': redirect_target
    }
    res = make_response(jsonify(res_data), 200)
    return set_auth_cookie(res, token, remember=remember)


@app.route('/api/demo-login', methods=['POST', 'OPTIONS'])
def demo_login():
    """Sign into the safe demo donor account."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    demo_email = 'demo@foodwise.ai'
    user = User.query.filter_by(email=demo_email).first()

    if not user:
        seed_initial_data()
        user = User.query.filter_by(email=demo_email).first()

    if not user:
        return jsonify({'success': False, 'message': 'Demo account is currently unavailable.'}), 500

    token = generate_auth_token(user.id, role=user.role, expires_in=86400)
    res_data = {
        'success': True,
        'message': 'Logged in to Demo Donor Account! Explore all features safely.',
        'token': token,
        'user': user.to_dict(),
        'redirect': 'dashboard.html'
    }
    res = make_response(jsonify(res_data), 200)
    return set_auth_cookie(res, token, remember=False)


@app.route('/api/demo-ngo-login', methods=['POST', 'OPTIONS'])
def demo_ngo_login():
    """Sign into the official Demo NGO account to test NGO acceptance & pickup scheduling."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    ngo_email = 'ngo@foodwise.ai'
    user = User.query.filter_by(email=ngo_email).first()

    if not user:
        seed_initial_data()
        user = User.query.filter_by(email=ngo_email).first()

    if not user:
        return jsonify({'success': False, 'message': 'Demo NGO account is currently unavailable.'}), 500

    token = generate_auth_token(user.id, role='ngo', expires_in=86400)
    res_data = {
        'success': True,
        'message': 'Logged in as Feeding India Operations (NGO)!',
        'token': token,
        'user': user.to_dict(),
        'redirect': 'ngo_dashboard.html'
    }
    res = make_response(jsonify(res_data), 200)
    return set_auth_cookie(res, token, remember=False)


@app.route('/api/logout', methods=['POST', 'GET', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    res = make_response(jsonify({'success': True, 'message': 'Logged out successfully.'}))
    return clear_auth_cookie(res)


@app.route('/api/me', methods=['GET', 'OPTIONS'])
@login_required
def get_current_profile():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    return jsonify({
        'success': True,
        'user': user.to_dict(include_counts=True)
    })


@app.route('/api/user/profile', methods=['POST', 'OPTIONS'])
@login_required
def update_profile():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    if user.role == 'demo':
        return jsonify({'success': False, 'message': 'Demo account profile is read-only.'}), 403

    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    phone = (data.get('phone') or '').strip()
    address = (data.get('address') or '').strip()
    new_password = data.get('password') or ''

    if name:
        user.name = name
    if phone:
        user.phone = phone
    if address:
        user.address = address

    if new_password:
        valid_pwd, pwd_err = validate_password_strength(new_password)
        if not valid_pwd:
            return jsonify({'success': False, 'message': pwd_err}), 400
        user.set_password(new_password)

    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully!',
            'user': user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to update profile: {str(e)}'}), 500


# ============================================================================
# FORGOT & RESET PASSWORD FLOW
# ============================================================================

@app.route('/api/forgot-password', methods=['POST', 'OPTIONS'])
def forgot_password():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()

    if not email:
        return jsonify({'success': False, 'message': 'Please enter your registered email address.'}), 400

    user = User.query.filter_by(email=email).first()
    generic_msg = "If your email is registered in our system, you will receive password reset instructions."

    if not user:
        return jsonify({'success': True, 'message': generic_msg})

    if user.role == 'demo':
        return jsonify({'success': False, 'message': 'Password reset is disabled for the public demo account.'}), 400

    reset_token = generate_reset_token(user.id)
    user.reset_token = reset_token
    user.reset_token_expires_at = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    origin = request.headers.get('Origin') or request.host_url.rstrip('/')
    reset_link = f"{origin}/pages/reset_password.html?token={reset_token}"

    smtp_host = os.environ.get('SMTP_HOST')
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))

    email_sent = False
    if smtp_host and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'FoodWise AI - Password Reset Request'
            msg['From'] = f"FoodWise AI <{smtp_user}>"
            msg['To'] = email

            text = f"Hello {user.name},\n\nYou requested a password reset for FoodWise AI.\nClick the link below:\n{reset_link}\n\nExpires in 1 hour."
            msg.attach(MIMEText(text, 'plain'))

            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            email_sent = True
        except Exception as err:
            print(f"[Email Error] Failed to send email via SMTP: {err}")

    res_payload = {
        'success': True,
        'message': generic_msg,
        'email_service_configured': bool(smtp_host and smtp_user and smtp_pass),
        'email_sent': email_sent
    }

    if not email_sent:
        res_payload['dev_reset_link'] = reset_link

    return jsonify(res_payload)


@app.route('/api/reset-password', methods=['POST', 'OPTIONS'])
def reset_password():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    data = request.get_json(silent=True) or {}
    token = (data.get('token') or '').strip()
    new_password = data.get('password') or ''

    if not token:
        return jsonify({'success': False, 'message': 'Password reset token is required.'}), 400

    user_id = verify_reset_token(token)
    if not user_id:
        return jsonify({'success': False, 'message': 'This reset token has expired or is invalid.'}), 400

    user = db.session.get(User, user_id)
    if not user or user.reset_token != token:
        return jsonify({'success': False, 'message': 'This reset token is invalid or has already been used.'}), 400

    if user.reset_token_expires_at and user.reset_token_expires_at < datetime.utcnow():
        return jsonify({'success': False, 'message': 'This reset token has expired.'}), 400

    valid_pwd, pwd_err = validate_password_strength(new_password)
    if not valid_pwd:
        return jsonify({'success': False, 'message': pwd_err}), 400

    try:
        user.set_password(new_password)
        user.reset_token = None
        user.reset_token_expires_at = None
        db.session.commit()
        return jsonify({'success': True, 'message': 'Password reset successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to reset password: {str(e)}'}), 500


# ============================================================================
# REGISTERED NGO DIRECTORY & MANAGEMENT
# ============================================================================

@app.route('/api/ngos', methods=['GET', 'OPTIONS'])
def list_ngos():
    """Returns verified registered NGOs available for donations."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    # Seed if empty
    if NGO.query.count() == 0:
        seed_initial_data()

    ngos = NGO.query.filter_by(is_verified=True).order_by(NGO.name.asc()).all()
    return jsonify({
        'success': True,
        'count': len(ngos),
        'ngos': [n.to_dict() for n in ngos]
    })


@app.route('/api/ngo/register', methods=['POST', 'OPTIONS'])
def register_ngo():
    """Dedicated NGO Organization registration."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    phone = (data.get('phone') or '').strip()
    address = (data.get('address') or '').strip()
    city = (data.get('city') or 'Citywide').strip()
    reg_number = (data.get('reg_number') or '').strip()
    contact_person = (data.get('contact_person') or name).strip()
    accepted_food_types = (data.get('accepted_food_types') or 'Cooked Meals, Raw Veggies, Bakery, Groceries').strip()
    capacity_kg = float(data.get('capacity_kg') or 200.0)

    if not name or not email or not password or not phone or not address:
        return jsonify({'success': False, 'message': 'Organization name, email, password, phone, and address are required.'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'An account with this email already exists.'}), 409

    try:
        user = User(
            name=name,
            email=email,
            role='ngo',
            status='active',
            phone=phone,
            address=address
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        ngo = NGO(
            user_id=user.id,
            name=name,
            reg_number=reg_number or f"NGO-{datetime.utcnow().strftime('%Y%m%d%H%M')}",
            contact_person=contact_person,
            email=email,
            phone=phone,
            address=address,
            city=city,
            accepted_food_types=accepted_food_types,
            capacity_kg=capacity_kg,
            is_verified=True,
            description=data.get('description') or 'Verified FoodWise NGO Food Rescue Partner.'
        )
        db.session.add(ngo)
        db.session.commit()

        token = generate_auth_token(user.id, role='ngo')
        res = make_response(jsonify({
            'success': True,
            'message': 'NGO Organization registered successfully!',
            'token': token,
            'user': user.to_dict(),
            'ngo': ngo.to_dict(),
            'redirect': 'ngo_dashboard.html'
        }), 201)
        return set_auth_cookie(res, token, remember=True)

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to register NGO: {str(e)}'}), 500


# ============================================================================
# AUTOMATIC NGO MATCHING & DISPATCH ENGINE
# ============================================================================

def find_best_matching_ngo(food_item, donor=None, excluded_ngo_ids=None):
    """
    Automatic NGO Matching Algorithm.
    Scores registered, verified NGOs based on:
    1. Quantity capacity vs active commitments (0-40 pts)
    2. Category acceptance match (0-35 pts)
    3. Location proximity / citywide coverage (0-25 pts)
    4. Active queue availability (0-10 pts)
    Returns best matching NGO or None if no eligible NGO is available.
    """
    if excluded_ngo_ids is None:
        excluded_ngo_ids = set()
    else:
        excluded_ngo_ids = set(excluded_ngo_ids)

    query = NGO.query.filter_by(is_verified=True)
    if excluded_ngo_ids:
        query = query.filter(~NGO.id.in_(excluded_ngo_ids))
    candidates = query.all()

    if not candidates:
        return None

    donor_loc = ((food_item.location or '') + ' ' + ((donor.address or '') if donor else '')).lower()
    food_cat = (food_item.category or 'other').lower()
    food_qty = float(food_item.quantity or 1.0)

    scored_ngos = []

    for ngo in candidates:
        score = 0

        # --- A. Capacity Evaluation (0-40 pts) ---
        active_donations = Donation.query.filter(
            Donation.ngo_id == ngo.id,
            Donation.status.in_(['Accepted', 'Pickup Scheduled', 'Collected', 'Delivered'])
        ).all()
        current_load = sum(d.food_item.quantity for d in active_donations if d.food_item)
        remaining_capacity = max(0.0, float(ngo.capacity_kg or 150.0) - current_load)

        if remaining_capacity >= food_qty:
            score += 40
        elif float(ngo.capacity_kg or 150.0) >= food_qty:
            score += 20
        else:
            # If food item exceeds daily capacity, skip
            continue

        # --- B. Category Match (0-35 pts) ---
        accepted_types = (ngo.accepted_food_types or '').lower()
        if 'all' in accepted_types:
            score += 35
        elif food_cat in accepted_types:
            score += 35
        elif food_cat == 'cooked' and any(k in accepted_types for k in ('cooked', 'meal', 'catering', 'hot')):
            score += 35
        elif food_cat in ('vegetables', 'fruits') and any(k in accepted_types for k in ('veggie', 'raw', 'produce', 'fruit')):
            score += 35
        elif food_cat == 'bakery' and any(k in accepted_types for k in ('bake', 'bread')):
            score += 35
        elif food_cat == 'dairy' and any(k in accepted_types for k in ('dairy', 'milk')):
            score += 35
        elif food_cat == 'packaged' and any(k in accepted_types for k in ('package', 'grocer', 'canned')):
            score += 35
        elif food_cat == 'grains' and any(k in accepted_types for k in ('grain', 'rice', 'pulse')):
            score += 35
        else:
            score += 15

        # --- C. Location Proximity (0-25 pts) ---
        ngo_loc = f"{ngo.city} {ngo.address}".lower()
        donor_words = [w for w in re.split(r'[\s,.-]+', donor_loc) if len(w) > 3]
        matched_loc_words = [w for w in donor_words if w in ngo_loc]

        if matched_loc_words:
            score += 25
        elif 'citywide' in ngo.city.lower() or 'nationwide' in (ngo.description or '').lower():
            score += 18
        else:
            score += 8

        # --- D. Availability (0-10 pts) ---
        pending_count = Donation.query.filter_by(ngo_id=ngo.id, status='Pending').count()
        if pending_count == 0:
            score += 10
        elif pending_count <= 2:
            score += 6
        else:
            score += 2

        scored_ngos.append((score, ngo))

    if not scored_ngos:
        return None

    scored_ngos.sort(key=lambda x: x[0], reverse=True)
    best_score, best_ngo = scored_ngos[0]

    if best_score < 25:
        return None

    return best_ngo


def dispatch_donation_to_ngo(food_item, donor, ngo, notes='', trigger='Automatic AI matching'):
    """
    Creates donation record, links food and NGO, updates statuses, and creates real-time notifications.
    """
    donation = Donation(
        donor_id=donor.id,
        food_id=food_item.id,
        ngo_id=ngo.id,
        status='Pending',
        donor_notes=notes or f'Automatically matched by FoodWise AI based on proximity ({ngo.city}) and capacity.'
    )
    food_item.donation_status = 'pending'
    food_item.status = 'donated'
    db.session.add(donation)
    db.session.flush()

    # Notify NGO
    if ngo.user_id:
        db.session.add(Notification(
            user_id=ngo.user_id,
            donation_id=donation.id,
            title='New Surplus Food Rescue Request',
            message=f"New surplus food donation from {donor.name}: {food_item.quantity} {food_item.unit} of {food_item.food_name}. AI Safety: {(food_item.donation_suitable or 'safe').upper()}.",
            type='donation_request'
        ))

    # Notify Donor
    db.session.add(Notification(
        user_id=donor.id,
        donation_id=donation.id,
        title='Donation Auto-Dispatched to NGO',
        message=f"Your food item '{food_item.food_name}' was automatically matched and dispatched to {ngo.name} (Donation #{donation.id}).",
        type='donation_request'
    ))

    return donation


# ============================================================================
# DONATION WORKFLOW (DONOR -> NGO)
# ============================================================================

@app.route('/api/donations', methods=['GET', 'POST', 'OPTIONS'])
@login_required
def handle_donations():
    """
    GET: Returns donations for current user (if donor: their donations; if NGO: incoming requests).
    POST: Donor initiates a new donation to an NGO after AI verifies food is safe/donatable.
    """
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user

    if request.method == 'GET':
        if user.role == 'ngo':
            ngo = NGO.query.filter_by(user_id=user.id).first()
            if not ngo:
                # Fallback to first NGO if demo NGO
                ngo = NGO.query.first()
            donations = Donation.query.filter_by(ngo_id=ngo.id).order_by(Donation.created_at.desc()).all() if ngo else []
        elif user.role == 'admin':
            donations = Donation.query.order_by(Donation.created_at.desc()).all()
        else:
            donations = Donation.query.filter_by(donor_id=user.id).order_by(Donation.created_at.desc()).all()

        return jsonify({
            'success': True,
            'count': len(donations),
            'donations': [d.to_dict() for d in donations]
        })

    # POST: Create a donation request
    data = request.get_json(silent=True) or {}
    food_id = data.get('food_id')
    ngo_id = data.get('ngo_id')
    donor_notes = data.get('donor_notes') or ''

    if not food_id:
        return jsonify({'success': False, 'message': 'food_id is required to create a donation.'}), 400

    food = db.session.get(Food, food_id)
    if not food:
        return jsonify({'success': False, 'message': 'Food item not found.'}), 404

    # Authorization: Ensure user owns this food item or is admin/demo
    if food.user_id != user.id and user.role not in ('admin', 'demo'):
        return jsonify({'success': False, 'message': 'You can only donate food items from your own inventory.'}), 403

    # AI Safety & Expiry Validation
    if food.donation_suitable == 'unsafe' or food.status == 'expired':
        return jsonify({
            'success': False,
            'message': 'Cannot donate this food item. AI food safety analysis marked this item as NOT SAFE TO DONATE due to expiration or critical spoilage risk.'
        }), 400

    # Auto-match NGO if not explicitly provided
    if ngo_id:
        ngo = db.session.get(NGO, ngo_id)
        if not ngo or not ngo.is_verified:
            return jsonify({'success': False, 'message': 'Selected NGO organization was not found or is not currently verified.'}), 404
    else:
        past_ngo_ids = {d.ngo_id for d in Donation.query.filter_by(food_id=food.id).all()}
        ngo = find_best_matching_ngo(food, user, excluded_ngo_ids=past_ngo_ids)
        if not ngo:
            food.donation_status = 'available_for_donation'
            db.session.commit()
            return jsonify({
                'success': False,
                'status': 'available_for_donation',
                'message': 'NO SUITABLE NGO AVAILABLE RIGHT NOW. Saved as Available for Donation.'
            }), 200

    # Prevent duplicate active donation for same food and NGO
    existing_active = Donation.query.filter(
        Donation.food_id == food.id,
        Donation.ngo_id == ngo.id,
        Donation.status.in_(['Pending', 'Accepted', 'Pickup Scheduled', 'Collected'])
    ).first()
    if existing_active:
        return jsonify({
            'success': False,
            'message': f"A donation request for this item is already active with {ngo.name} (Donation #{existing_active.id}).",
            'donation': existing_active.to_dict()
        }), 409

    try:
        donation = dispatch_donation_to_ngo(food, user, ngo, notes=donor_notes)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f"Food donation request successfully sent to {ngo.name}! Track pickup progress on your dashboard.",
            'donation': donation.to_dict(),
            'ngo': ngo.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to create donation: {str(e)}'}), 500


@app.route('/api/donations/<int:donation_id>', methods=['GET', 'OPTIONS'])
@login_required
def get_donation_detail(donation_id):
    """Fetch single donation status & real-time tracking details."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    donation = db.session.get(Donation, donation_id)
    if not donation:
        return jsonify({'success': False, 'message': 'Donation record not found.'}), 404

    # Access control
    if donation.donor_id != user.id and user.role != 'admin':
        # Check if user is the assigned NGO
        ngo = NGO.query.filter_by(user_id=user.id).first()
        if not ngo or ngo.id != donation.ngo_id:
            return jsonify({'success': False, 'message': 'Access denied.'}), 403

    return jsonify({
        'success': True,
        'donation': donation.to_dict()
    })


# ============================================================================
# NGO DASHBOARD & PICKUP MANAGEMENT
# ============================================================================

@app.route('/api/ngo/donations', methods=['GET', 'OPTIONS'])
@ngo_required
def get_ngo_donations():
    """Fetch all incoming, active, and completed donations for the authenticated NGO."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    ngo = NGO.query.filter_by(user_id=user.id).first()

    if not ngo:
        # Fallback to first NGO for demo testing
        ngo = NGO.query.first()

    if not ngo:
        return jsonify({'success': True, 'donations': [], 'stats': {}})

    donations = Donation.query.filter_by(ngo_id=ngo.id).order_by(Donation.created_at.desc()).all()
    
    # NGO KPIs
    pending_count = sum(1 for d in donations if d.status == 'Pending')
    accepted_count = sum(1 for d in donations if d.status in ('Accepted', 'Pickup Scheduled'))
    completed_count = sum(1 for d in donations if d.status == 'Completed')
    total_kg = sum(d.food_item.quantity for d in donations if d.food_item and d.status in ('Accepted', 'Pickup Scheduled', 'Collected', 'Delivered', 'Completed'))

    return jsonify({
        'success': True,
        'ngo': ngo.to_dict(),
        'stats': {
            'pending': pending_count,
            'accepted': accepted_count,
            'completed': completed_count,
            'total_kg_rescued': round(total_kg, 1),
            'total_requests': len(donations)
        },
        'donations': [d.to_dict() for d in donations]
    })


@app.route('/api/ngo/donations/<int:donation_id>/status', methods=['POST', 'OPTIONS'])
@ngo_required
def update_donation_status(donation_id):
    """
    NGO updates donation status.
    Workflow:
    Pending -> Accepted | Rejected
    Accepted -> Pickup Scheduled
    Pickup Scheduled -> Collected
    Collected -> Delivered
    Delivered -> Completed
    """
    if request.method == 'OPTIONS':
        return make_response('', 204)

    data = request.get_json(silent=True) or {}
    new_status = (data.get('status') or '').strip()
    ngo_notes = data.get('ngo_notes') or ''
    rejection_reason = data.get('rejection_reason') or ''

    valid_statuses = ['Pending', 'Accepted', 'Rejected', 'Pickup Scheduled', 'Collected', 'Delivered', 'Completed']
    if new_status not in valid_statuses:
        return jsonify({'success': False, 'message': f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400

    donation = db.session.get(Donation, donation_id)
    if not donation:
        return jsonify({'success': False, 'message': 'Donation record not found.'}), 404

    rerouted_donation = None
    next_ngo_data = None

    if new_status == 'Rejected':
        donation.status = 'Rejected'
        if rejection_reason:
            donation.rejection_reason = rejection_reason

        # Notify donor of rejection
        db.session.add(Notification(
            user_id=donation.donor_id,
            donation_id=donation.id,
            title='Donation Request Declined',
            message=f"{donation.target_ngo.name if donation.target_ngo else 'NGO Partner'} could not accept donation #{donation.id}: {rejection_reason or 'Daily capacity reached'}. Searching for next eligible NGO...",
            type='donation_rejected'
        ))

        # Automatically search for next suitable verified NGO
        past_ngo_ids = {d.ngo_id for d in Donation.query.filter_by(food_id=donation.food_id).all()}
        next_ngo = find_best_matching_ngo(donation.food_item, donation.donor, excluded_ngo_ids=past_ngo_ids)

        if next_ngo:
            rerouted_donation = dispatch_donation_to_ngo(
                donation.food_item,
                donation.donor,
                next_ngo,
                notes=f"Auto-rerouted to {next_ngo.name} after previous NGO declined: {rejection_reason or 'Capacity reached'}"
            )
            donation.food_item.donation_status = 'pending'
            next_ngo_data = next_ngo.to_dict()

            # Notify donor about automatic rerouting
            db.session.add(Notification(
                user_id=donation.donor_id,
                donation_id=rerouted_donation.id,
                title='Donation Auto-Rerouted to Next NGO',
                message=f"FoodWise AI automatically rerouted your food '{donation.food_item.food_name}' to {next_ngo.name} (Donation #{rerouted_donation.id}).",
                type='donation_rerouted'
            ))
        else:
            donation.food_item.donation_status = 'available_for_donation'
            db.session.add(Notification(
                user_id=donation.donor_id,
                donation_id=donation.id,
                title='No Further Matching NGOs Available',
                message=f"All partner NGOs in your area are currently at maximum capacity. Your food remains saved as Available for Donation.",
                type='system'
            ))

    elif new_status == 'Accepted':
        donation.status = 'Accepted'
        if donation.food_item:
            donation.food_item.donation_status = 'accepted'
        db.session.add(Notification(
            user_id=donation.donor_id,
            donation_id=donation.id,
            title='Donation Accepted by NGO!',
            message=f"{donation.target_ngo.name if donation.target_ngo else 'NGO'} accepted your donation #{donation.id}! Volunteer pickup will be scheduled shortly.",
            type='donation_accepted'
        ))

    elif new_status == 'Completed':
        donation.status = 'Completed'
        if donation.food_item:
            donation.food_item.donation_status = 'completed'
            donation.food_item.status = 'consumed'
        db.session.add(Notification(
            user_id=donation.donor_id,
            donation_id=donation.id,
            title='Food Rescue Mission Completed!',
            message=f"Your donated food #{donation.id} has been delivered and distributed by {donation.target_ngo.name if donation.target_ngo else 'NGO'}. Thank you for reducing waste!",
            type='donation_completed'
        ))

    else:
        donation.status = new_status
        if donation.food_item:
            donation.food_item.donation_status = new_status.lower().replace(' ', '_')

    # If pickup info is supplied with status update
    scheduled_time = data.get('scheduled_time')
    agent_name = data.get('agent_name')
    agent_phone = data.get('agent_phone')
    vehicle_info = data.get('vehicle_info')
    pickup_notes = data.get('pickup_notes')

    if scheduled_time or agent_name:
        pickup = PickupDetail.query.filter_by(donation_id=donation.id).first()
        if not pickup:
            pickup = PickupDetail(donation_id=donation.id)
            db.session.add(pickup)

        if scheduled_time: pickup.scheduled_time = scheduled_time
        if agent_name: pickup.agent_name = agent_name
        if agent_phone: pickup.agent_phone = agent_phone
        if vehicle_info: pickup.vehicle_info = vehicle_info
        if pickup_notes: pickup.pickup_notes = pickup_notes
        pickup.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        msg = f"Donation status updated to '{new_status}'."
        if new_status == 'Rejected' and next_ngo_data:
            msg = f"Donation rejected. FoodWise AI automatically rerouted request to {next_ngo_data['name']} (Donation #{rerouted_donation.id})."
        elif new_status == 'Rejected':
            msg = "Donation rejected. No other matching NGOs currently open; food saved as Available for Donation."

        return jsonify({
            'success': True,
            'message': msg,
            'donation': donation.to_dict(),
            'rerouted_donation': rerouted_donation.to_dict() if rerouted_donation else None,
            'next_ngo': next_ngo_data
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to update status: {str(e)}'}), 500


@app.route('/api/ngo/donations/<int:donation_id>/pickup', methods=['POST', 'OPTIONS'])
@ngo_required
def schedule_pickup(donation_id):
    """Dedicated endpoint to schedule or modify pickup logistics."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    data = request.get_json(silent=True) or {}
    scheduled_time = (data.get('scheduled_time') or '').strip()
    agent_name = (data.get('agent_name') or '').strip()
    agent_phone = (data.get('agent_phone') or '').strip()
    vehicle_info = (data.get('vehicle_info') or '').strip()
    pickup_notes = (data.get('pickup_notes') or '').strip()

    if not scheduled_time or not agent_name:
        return jsonify({'success': False, 'message': 'Scheduled pickup time and volunteer/driver name are required.'}), 400

    donation = db.session.get(Donation, donation_id)
    if not donation:
        return jsonify({'success': False, 'message': 'Donation record not found.'}), 404

    pickup = PickupDetail.query.filter_by(donation_id=donation.id).first()
    if not pickup:
        pickup = PickupDetail(donation_id=donation.id)
        db.session.add(pickup)

    pickup.scheduled_time = scheduled_time
    pickup.agent_name = agent_name
    pickup.agent_phone = agent_phone
    pickup.vehicle_info = vehicle_info
    pickup.pickup_notes = pickup_notes
    pickup.updated_at = datetime.utcnow()

    donation.status = 'Pickup Scheduled'
    if donation.food_item:
        donation.food_item.donation_status = 'pickup_scheduled'

    # Notify donor about pickup schedule
    db.session.add(Notification(
        user_id=donation.donor_id,
        donation_id=donation.id,
        title='Food Pickup Scheduled by NGO',
        message=f"{donation.target_ngo.name if donation.target_ngo else 'Assigned NGO'} assigned volunteer {agent_name} ({agent_phone}) for pickup at {scheduled_time}.",
        type='pickup_scheduled'
    ))

    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Pickup successfully scheduled with {agent_name} for {scheduled_time}!',
            'donation': donation.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to schedule pickup: {str(e)}'}), 500


# ============================================================================
# USER FOOD RECORDS & AI PREDICTION
# ============================================================================

@app.route('/api/foods', methods=['GET', 'POST', 'OPTIONS'])
@login_required
def user_foods():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user

    # GET: List current user's food records
    if request.method == 'GET':
        foods = Food.query.filter_by(user_id=user.id).order_by(Food.created_at.desc()).all()
        return jsonify({
            'success': True,
            'count': len(foods),
            'foods': [f.to_dict() for f in foods]
        })

    # POST: Add new food record
    data = request.get_json(silent=True) or {}
    food_name = (data.get('food_name') or data.get('name') or '').strip()
    if not food_name:
        return jsonify({'success': False, 'message': 'Food name is required.'}), 400

    category = (data.get('category') or 'other').strip().lower()
    quantity = float(data.get('quantity') or 1.0)
    unit = (data.get('unit') or 'kg').strip()
    storage_type = (data.get('storage_type') or 'refrigerator').strip().lower()
    purchase_date = data.get('purchase_date') or datetime.utcnow().date().isoformat()
    expiry_date = data.get('expiry_date') or None
    prep_time = data.get('prep_time') or ''
    location = data.get('location') or (user.address if user else '')
    image_url = data.get('image_url') or ''
    notes = data.get('notes') or ''
    status = data.get('status') or 'fresh'

    # Compute AI waste risk & donation safety
    ai_result = calculate_waste_risk(
        food_name=food_name,
        category=category,
        quantity=quantity,
        storage_type=storage_type,
        expiry_date_str=expiry_date,
        purchase_date_str=purchase_date,
        prep_time_str=prep_time
    )

    try:
        new_food = Food(
            user_id=user.id,
            food_name=food_name,
            category=category,
            quantity=quantity,
            unit=unit,
            storage_type=storage_type,
            purchase_date=purchase_date,
            expiry_date=expiry_date,
            prep_time=prep_time,
            location=location,
            image_url=image_url,
            status=status,
            risk=ai_result['risk'],
            risk_score=ai_result['score'],
            donation_suitable=ai_result['donation_suitable'],
            donation_status='not_donated',
            notes=notes
        )
        db.session.add(new_food)
        db.session.flush()

        # Automatic NGO Matching & Dispatch
        auto_donation = None

        if ai_result['donation_suitable'] in ('safe', 'use_soon'):
            matched_ngo = find_best_matching_ngo(new_food, user)
            if matched_ngo:
                donation = dispatch_donation_to_ngo(new_food, user, matched_ngo)
                auto_donation = {
                    'matched': True,
                    'status': 'dispatched',
                    'donation_id': donation.id,
                    'ngo': matched_ngo.to_dict(),
                    'message': f"Automatically matched and dispatched to {matched_ngo.name}!"
                }
            else:
                new_food.donation_status = 'available_for_donation'
                auto_donation = {
                    'matched': False,
                    'status': 'available_for_donation',
                    'message': 'NO SUITABLE NGO AVAILABLE RIGHT NOW. Saved as Available for Donation.'
                }
        else:
            new_food.donation_status = 'unsafe'
            auto_donation = {
                'matched': False,
                'blocked': True,
                'message': 'NOT SAFE TO DONATE: ' + ai_result.get('donation_reason', 'Perishable food risk detected.')
            }

        db.session.commit()

        success_msg = f"{food_name} analyzed successfully!"
        if auto_donation and auto_donation.get('matched'):
            success_msg = f"{food_name} analyzed! Automatically matched and sent to {auto_donation['ngo']['name']} (Donation #{auto_donation['donation_id']})."
        elif auto_donation and auto_donation.get('status') == 'available_for_donation':
            success_msg = f"{food_name} analyzed! No suitable NGO available right now; saved as Available for Donation."

        return jsonify({
            'success': True,
            'message': success_msg,
            'food': new_food.to_dict(),
            'ai_prediction': ai_result,
            'auto_donation': auto_donation
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to add food record: {str(e)}'}), 500


@app.route('/api/foods/<int:food_id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
@login_required
def single_food_item(food_id):
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    food = Food.query.filter_by(id=food_id, user_id=user.id).first()

    if not food:
        return jsonify({'success': False, 'message': 'Food item not found or you do not have permission to access it.'}), 404

    if request.method == 'GET':
        return jsonify({'success': True, 'food': food.to_dict()})

    if request.method == 'PUT':
        data = request.get_json(silent=True) or {}
        if 'food_name' in data: food.food_name = data['food_name'].strip()
        if 'category' in data: food.category = data['category'].strip().lower()
        if 'quantity' in data: food.quantity = float(data['quantity'])
        if 'unit' in data: food.unit = data['unit'].strip()
        if 'storage_type' in data: food.storage_type = data['storage_type'].strip().lower()
        if 'purchase_date' in data: food.purchase_date = data['purchase_date']
        if 'expiry_date' in data: food.expiry_date = data['expiry_date']
        if 'prep_time' in data: food.prep_time = data['prep_time']
        if 'location' in data: food.location = data['location']
        if 'image_url' in data: food.image_url = data['image_url']
        if 'status' in data: food.status = data['status']
        if 'notes' in data: food.notes = data['notes']

        # Re-evaluate AI risk
        ai_result = calculate_waste_risk(
            food_name=food.food_name,
            category=food.category,
            quantity=food.quantity,
            storage_type=food.storage_type,
            expiry_date_str=food.expiry_date
        )
        food.risk = ai_result['risk']
        food.risk_score = ai_result['score']
        food.donation_suitable = ai_result['donation_suitable']
        food.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Food item updated successfully!', 'food': food.to_dict()})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Failed to update: {str(e)}'}), 500

    if request.method == 'DELETE':
        try:
            db.session.delete(food)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Food item removed successfully.'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Failed to delete: {str(e)}'}), 500


@app.route('/api/predict', methods=['POST', 'OPTIONS'])
@login_required
def predict_food_risk():
    """AI waste risk and donation suitability prediction."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    data = request.get_json(silent=True) or {}

    food_name = (data.get('food_name') or 'Food Item').strip()
    category = (data.get('category') or 'other').strip().lower()
    quantity = float(data.get('quantity') or 1.0)
    storage_type = (data.get('storage_type') or 'refrigerator').strip().lower()
    expiry_date = data.get('expiry_date')
    prep_time = data.get('prep_time')

    ai_result = calculate_waste_risk(
        food_name=food_name,
        category=category,
        quantity=quantity,
        storage_type=storage_type,
        expiry_date_str=expiry_date,
        prep_time_str=prep_time
    )

    try:
        log = PredictionLog(
            user_id=user.id,
            food_name=food_name,
            category=category,
            risk_score=ai_result['score'],
            risk_level=ai_result['risk'],
            confidence=ai_result['confidence'],
            donation_suitable=ai_result['donation_suitable'],
            recommendations=str(ai_result['tips'])
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        pass

    return jsonify({
        'success': True,
        'prediction': ai_result
    })


@app.route('/api/dashboard/stats', methods=['GET', 'OPTIONS'])
@login_required
def dashboard_stats():
    """Live dashboard KPIs for donor, including donation metrics."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    foods = Food.query.filter_by(user_id=user.id).all()
    donations = Donation.query.filter_by(donor_id=user.id).all()

    today = datetime.utcnow().date()
    total = len(foods)
    consumed = sum(1 for f in foods if f.status == 'consumed')
    wasted = sum(1 for f in foods if f.status == 'wasted' or (f.wasted_qty and f.wasted_qty > 0))
    donated_count = len(donations)

    near_expiry = 0
    high_risk = 0
    medium_risk = 0
    low_risk = 0

    for f in foods:
        if f.risk == 'high' or f.risk_score >= 65:
            high_risk += 1
        elif f.risk == 'medium' or f.risk_score >= 35:
            medium_risk += 1
        else:
            low_risk += 1

        if f.status not in ('consumed', 'wasted', 'donated') and f.expiry_date:
            try:
                exp = datetime.strptime(f.expiry_date.split('T')[0], '%Y-%m-%d').date()
                diff = (exp - today).days
                if 0 <= diff <= 3:
                    near_expiry += 1
            except Exception:
                pass

    efficiency = 88
    if total > 0:
        efficiency = max(15, min(98, round(((total - wasted) / total) * 100 - (high_risk * 2))))

    return jsonify({
        'success': True,
        'stats': {
            'total': total,
            'consumed': consumed,
            'wasted': wasted,
            'near_expiry': near_expiry,
            'donated': donated_count,
            'efficiency_score': efficiency,
            'risk_breakdown': {
                'high': high_risk,
                'medium': medium_risk,
                'low': low_risk
            }
        }
    })


# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================

@app.route('/api/admin/login', methods=['POST', 'OPTIONS'])
def admin_login():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return jsonify({'success': False, 'message': 'Admin email and password required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid administrator credentials.'}), 401

    if user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied: You do not have administrator permissions.'}), 403

    token = generate_auth_token(user.id, role='admin', expires_in=86400)
    res_data = {
        'success': True,
        'message': f'Welcome Administrator, {user.name}!',
        'token': token,
        'user': user.to_dict()
    }
    res = make_response(jsonify(res_data), 200)
    return set_auth_cookie(res, token, remember=False)


@app.route('/api/admin/users', methods=['GET', 'OPTIONS'])
@admin_required
def admin_get_users():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    users = User.query.order_by(User.created_at.desc()).all()
    user_list = [u.to_dict(include_counts=True) for u in users]

    return jsonify({
        'success': True,
        'count': len(user_list),
        'users': user_list
    })


@app.route('/api/admin/ngos', methods=['GET', 'OPTIONS'])
@admin_required
def admin_get_ngos():
    """List all registered NGOs for verification & management."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    ngos = NGO.query.order_by(NGO.created_at.desc()).all()
    return jsonify({
        'success': True,
        'count': len(ngos),
        'ngos': [n.to_dict() for n in ngos]
    })


@app.route('/api/admin/ngos/<int:ngo_id>/verify', methods=['POST', 'OPTIONS'])
@admin_required
def admin_verify_ngo(ngo_id):
    """Toggle verification status of an NGO."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    ngo = db.session.get(NGO, ngo_id)
    if not ngo:
        return jsonify({'success': False, 'message': 'NGO not found.'}), 404

    ngo.is_verified = not ngo.is_verified
    db.session.commit()
    state_str = "Verified" if ngo.is_verified else "Unverified"
    return jsonify({
        'success': True,
        'message': f"NGO '{ngo.name}' marked as {state_str}.",
        'ngo': ngo.to_dict()
    })


@app.route('/api/admin/donations', methods=['GET', 'OPTIONS'])
@admin_required
def admin_get_donations():
    """Global donation oversight."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    donations = Donation.query.order_by(Donation.created_at.desc()).all()
    pending = sum(1 for d in donations if d.status == 'Pending')
    accepted = sum(1 for d in donations if d.status in ('Accepted', 'Pickup Scheduled'))
    completed = sum(1 for d in donations if d.status == 'Completed')
    rejected = sum(1 for d in donations if d.status == 'Rejected')

    return jsonify({
        'success': True,
        'stats': {
            'total': len(donations),
            'pending': pending,
            'accepted': accepted,
            'completed': completed,
            'rejected': rejected
        },
        'donations': [d.to_dict() for d in donations]
    })


@app.route('/api/admin/stats', methods=['GET', 'OPTIONS'])
@admin_required
def admin_get_stats():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    total_users = User.query.count()
    total_ngos = NGO.query.count()
    total_foods = Food.query.count()
    total_predictions = PredictionLog.query.count()
    total_donations = Donation.query.count()
    completed_donations = Donation.query.filter_by(status='Completed').count()

    return jsonify({
        'success': True,
        'stats': {
            'total_users': total_users,
            'total_ngos': total_ngos,
            'total_foods': total_foods,
            'total_predictions': total_predictions,
            'total_donations': total_donations,
            'completed_donations': completed_donations
        }
    })


# ============================================================================
# NOTIFICATIONS & RETRY MATCHING ENDPOINTS
# ============================================================================

@app.route('/api/notifications', methods=['GET', 'OPTIONS'])
@login_required
def get_user_notifications():
    """Retrieve in-app notifications for authenticated user (donor or NGO)."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    notifs = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).limit(40).all()
    unread_count = sum(1 for n in notifs if not n.is_read)

    return jsonify({
        'success': True,
        'unread_count': unread_count,
        'count': len(notifs),
        'notifications': [n.to_dict() for n in notifs]
    })


@app.route('/api/notifications/read', methods=['POST', 'OPTIONS'])
@login_required
def mark_notifications_read():
    """Mark all or a specific notification as read."""
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    data = request.get_json(silent=True) or {}
    notif_id = data.get('notification_id')

    if notif_id:
        notif = Notification.query.filter_by(id=notif_id, user_id=user.id).first()
        if notif:
            notif.is_read = True
    else:
        Notification.query.filter_by(user_id=user.id, is_read=False).update({'is_read': True})

    db.session.commit()
    return jsonify({'success': True, 'message': 'Notifications marked as read.'})


@app.route('/api/donations/retry-match/<int:food_id>', methods=['POST', 'OPTIONS'])
@login_required
def retry_ngo_matching(food_id):
    """
    Retry automatic matching for foods currently in 'available_for_donation' state.
    """
    if request.method == 'OPTIONS':
        return make_response('', 204)

    user = g.current_user
    food = db.session.get(Food, food_id)
    if not food:
        return jsonify({'success': False, 'message': 'Food item not found.'}), 404

    if food.user_id != user.id and user.role not in ('admin', 'demo'):
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    if food.donation_suitable == 'unsafe' or food.status == 'expired':
        return jsonify({'success': False, 'message': 'Cannot match food marked as unsafe or expired.'}), 400

    past_ngo_ids = {d.ngo_id for d in Donation.query.filter_by(food_id=food.id).all()}
    best_ngo = find_best_matching_ngo(food, user, excluded_ngo_ids=past_ngo_ids)

    if not best_ngo:
        return jsonify({
            'success': False,
            'status': 'available_for_donation',
            'message': 'NO SUITABLE NGO AVAILABLE RIGHT NOW. Saved as Available for Donation.'
        }), 200

    donation = dispatch_donation_to_ngo(food, user, best_ngo, notes='Retried automated match after wait period.')
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f"Successfully matched and dispatched to {best_ngo.name}!",
        'donation': donation.to_dict(),
        'ngo': best_ngo.to_dict()
    }), 201


# ============================================================================
# STATIC FILE SERVING
# ============================================================================

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/pages/<path:filename>')
def serve_pages(filename):
    return send_from_directory(PAGES_DIR, filename)


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"==================================================")
    print(f" FoodWise AI Backend Running on http://127.0.0.1:{port}")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=True)

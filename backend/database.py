"""
FoodWise AI - Database Management & Seeding
Handles database connection configuration (PostgreSQL, SQLite, Neon, Supabase)
and automatic seeding of default Admin and Demo accounts.
"""
import os
from datetime import datetime, timedelta
from backend.models import db, User, Food, PredictionLog


def configure_database(app):
    """Configure SQLAlchemy URI and connection settings."""
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        # Compatibility fix: SQLAlchemy 1.4+ requires 'postgresql://' instead of legacy 'postgres://'
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Fallback to SQLite
        is_vercel = os.environ.get('VERCEL') == '1'
        if is_vercel:
            # On Vercel serverless, only /tmp is writable
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/foodwise.db'
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            db_dir = os.path.join(base_dir, 'database')
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, 'app.db')
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True
    }
    db.init_app(app)


def seed_initial_data():
    """Seed Admin and Demo accounts with rich initial data if not already present."""
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@foodwise.ai').strip().lower()
    admin_pass = os.environ.get('ADMIN_PASSWORD', 'Admin@FoodWise2026!')

    # 1. Admin Account
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(
            name='FoodWise Administrator',
            email=admin_email,
            role='admin',
            status='active'
        )
        admin_user.set_password(admin_pass)
        db.session.add(admin_user)
        db.session.commit()
        print(f"[Seed] Admin account created: {admin_email}")

    # 2. Demo Account
    demo_email = 'demo@foodwise.ai'
    demo_pass = os.environ.get('DEMO_PASSWORD', 'Demo@FoodWise2026!')
    demo_user = User.query.filter_by(email=demo_email).first()

    if not demo_user:
        demo_user = User(
            name='FoodWise Demo User',
            email=demo_email,
            role='demo',
            status='active'
        )
        demo_user.set_password(demo_pass)
        db.session.add(demo_user)
        db.session.commit()
        print(f"[Seed] Demo account created: {demo_email}")

    # Seed Demo Foods if demo user has no records
    demo_foods_count = Food.query.filter_by(user_id=demo_user.id).count()
    if demo_foods_count == 0:
        today = datetime.utcnow().date()
        demo_items = [
            {
                'food_name': 'Fresh Whole Milk',
                'category': 'dairy',
                'quantity': 2.0,
                'unit': 'L',
                'storage_type': 'refrigerator',
                'purchase_date': (today - timedelta(days=2)).isoformat(),
                'expiry_date': (today + timedelta(days=1)).isoformat(),
                'status': 'fresh',
                'risk': 'high',
                'risk_score': 84,
                'notes': 'Organic pasteurized milk'
            },
            {
                'food_name': 'Organic Tomatoes',
                'category': 'vegetables',
                'quantity': 1.5,
                'unit': 'kg',
                'storage_type': 'countertop',
                'purchase_date': (today - timedelta(days=3)).isoformat(),
                'expiry_date': (today + timedelta(days=2)).isoformat(),
                'status': 'fresh',
                'risk': 'high',
                'risk_score': 78,
                'notes': 'Ripe red cluster tomatoes'
            },
            {
                'food_name': 'Whole Wheat Bread',
                'category': 'bakery',
                'quantity': 1.0,
                'unit': 'loaf',
                'storage_type': 'pantry',
                'purchase_date': (today - timedelta(days=1)).isoformat(),
                'expiry_date': (today + timedelta(days=3)).isoformat(),
                'status': 'fresh',
                'risk': 'medium',
                'risk_score': 54,
                'notes': 'Sliced sandwich loaf'
            },
            {
                'food_name': 'Chicken Breast',
                'category': 'meat',
                'quantity': 1.2,
                'unit': 'kg',
                'storage_type': 'refrigerator',
                'purchase_date': (today - timedelta(days=1)).isoformat(),
                'expiry_date': (today + timedelta(days=1)).isoformat(),
                'status': 'fresh',
                'risk': 'high',
                'risk_score': 88,
                'notes': 'Requires cooking or freezing today'
            },
            {
                'food_name': 'Basmati Rice',
                'category': 'grains',
                'quantity': 5.0,
                'unit': 'kg',
                'storage_type': 'pantry',
                'purchase_date': (today - timedelta(days=14)).isoformat(),
                'expiry_date': (today + timedelta(days=180)).isoformat(),
                'status': 'fresh',
                'risk': 'low',
                'risk_score': 8,
                'notes': 'Stored in airtight pantry container'
            },
            {
                'food_name': 'Greek Yogurt',
                'category': 'dairy',
                'quantity': 0.5,
                'unit': 'kg',
                'storage_type': 'refrigerator',
                'purchase_date': (today - timedelta(days=4)).isoformat(),
                'expiry_date': (today + timedelta(days=2)).isoformat(),
                'status': 'fresh',
                'risk': 'medium',
                'risk_score': 62,
                'notes': 'Plain unflavored yogurt'
            },
            {
                'food_name': 'Baby Spinach',
                'category': 'vegetables',
                'quantity': 0.3,
                'unit': 'kg',
                'storage_type': 'refrigerator',
                'purchase_date': (today - timedelta(days=2)).isoformat(),
                'expiry_date': (today + timedelta(days=2)).isoformat(),
                'status': 'fresh',
                'risk': 'high',
                'risk_score': 72,
                'notes': 'Crisper drawer in sealed box'
            },
            {
                'food_name': 'Fuji Apples',
                'category': 'fruits',
                'quantity': 2.0,
                'unit': 'kg',
                'storage_type': 'refrigerator',
                'purchase_date': (today - timedelta(days=5)).isoformat(),
                'expiry_date': (today + timedelta(days=14)).isoformat(),
                'status': 'fresh',
                'risk': 'low',
                'risk_score': 20,
                'notes': 'Keep crisp in refrigerator'
            }
        ]

        for item_data in demo_items:
            food = Food(user_id=demo_user.id, **item_data)
            db.session.add(food)
        db.session.commit()
        print(f"[Seed] Added {len(demo_items)} sample food records for Demo user.")


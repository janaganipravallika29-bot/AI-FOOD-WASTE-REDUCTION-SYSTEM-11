"""
FoodWise AI - Database Management & Seeding
Handles database connection configuration (PostgreSQL, SQLite, Neon, Supabase)
and automatic seeding of default Admin, Demo, and registered NGO accounts.
"""
import os
from datetime import datetime, timedelta
from backend.models import db, User, NGO, Food, Donation, PickupDetail, PredictionLog


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
    """Seed Admin, Demo, and verified registered NGOs with sample records."""
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@foodwise.ai').strip().lower()
    admin_pass = os.environ.get('ADMIN_PASSWORD', 'Admin@FoodWise2026!')

    # 1. Admin Account
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(
            name='FoodWise Administrator',
            email=admin_email,
            role='admin',
            status='active',
            phone='+1 800 555 0199',
            address='Admin Headquarters, Tech Park'
        )
        admin_user.set_password(admin_pass)
        db.session.add(admin_user)
        db.session.commit()
        print(f"[Seed] Admin account created: {admin_email}")

    # 2. Demo Account (Donor)
    demo_email = 'demo@foodwise.ai'
    demo_pass = os.environ.get('DEMO_PASSWORD', 'Demo@FoodWise2026!')
    demo_user = User.query.filter_by(email=demo_email).first()

    if not demo_user:
        demo_user = User(
            name='FoodWise Demo User',
            email=demo_email,
            role='demo',
            status='active',
            phone='+1 555 432 9988',
            address='742 Evergreen Terrace, Springfield'
        )
        demo_user.set_password(demo_pass)
        db.session.add(demo_user)
        db.session.commit()
        print(f"[Seed] Demo account created: {demo_email}")

    # 3. NGO Login Account
    ngo_email = 'ngo@foodwise.ai'
    ngo_pass = os.environ.get('NGO_PASSWORD', 'Ngo@FoodWise2026!')
    ngo_user = User.query.filter_by(email=ngo_email).first()

    if not ngo_user:
        ngo_user = User(
            name='Feeding India Operations',
            email=ngo_email,
            role='ngo',
            status='active',
            phone='+91 98765 43210',
            address='Sector 18, Institutional Area, New Delhi'
        )
        ngo_user.set_password(ngo_pass)
        db.session.add(ngo_user)
        db.session.commit()
        print(f"[Seed] NGO Account created: {ngo_email}")

    # 4. Registered NGOs List in Database
    if NGO.query.count() == 0:
        sample_ngos = [
            {
                'user_id': ngo_user.id,
                'name': 'Feeding India Food Rescue',
                'reg_number': 'NGO-DL-2018-8841',
                'contact_person': 'Priya Sharma (Coordinator)',
                'email': 'feeding.india@foodwise.org',
                'phone': '+91 98765 43210',
                'address': 'Plot 42, Food Rescue Hub, Sector 18',
                'city': 'New Delhi / NCR',
                'accepted_food_types': 'Cooked Meals, Raw Veggies, Packaged Groceries, Dairy',
                'capacity_kg': 500.0,
                'is_verified': True,
                'description': 'Nationwide hunger relief network operating insulated food distribution vans 24/7.'
            },
            {
                'user_id': None,
                'name': 'Robin Hood Army Community Chapter',
                'reg_number': 'NGO-MH-2015-4421',
                'contact_person': 'Rahul Mehta (Volunteer Lead)',
                'email': 'mumbai.robinhood@foodwise.org',
                'phone': '+91 98111 22334',
                'address': 'Community Centre, Bandra West',
                'city': 'Mumbai',
                'accepted_food_types': 'Cooked Meals, Bakery, Canned Goods, Fruits',
                'capacity_kg': 350.0,
                'is_verified': True,
                'description': 'Volunteer-based organization that redistributes surplus food from restaurants and donors.'
            },
            {
                'user_id': None,
                'name': 'Akshaya Annadanam Foundation',
                'reg_number': 'NGO-TS-2019-7102',
                'contact_person': 'K. Venkatesh (Operations Head)',
                'email': 'annadanam@akshayafoundation.org',
                'phone': '+91 94400 11223',
                'address': 'Road No. 12, Banjara Hills',
                'city': 'Hyderabad',
                'accepted_food_types': 'Cooked Meals, Grains, Vegetables, Milk & Dairy',
                'capacity_kg': 400.0,
                'is_verified': True,
                'description': 'Dedicated to eradicating classroom hunger and feeding shelter homes with hot fresh food.'
            },
            {
                'user_id': None,
                'name': 'City Food Bank & Rescue Hub',
                'reg_number': 'NGO-KA-2020-3392',
                'contact_person': 'Ananya Roy (Logistics Director)',
                'email': 'bangalore.foodbank@foodrescue.in',
                'phone': '+91 99000 88776',
                'address': '100ft Road, Indiranagar',
                'city': 'Bengaluru',
                'accepted_food_types': 'All Types: Cooked, Dry Grains, Produce, Dairy, Bakery',
                'capacity_kg': 600.0,
                'is_verified': True,
                'description': 'Refrigerated van fleet connecting institutional donors with 35+ local shelters.'
            },
            {
                'user_id': None,
                'name': 'Hope Community Kitchen Shelter',
                'reg_number': 'NGO-TN-2021-1205',
                'contact_person': 'S. Ramanathan (Kitchen Manager)',
                'email': 'hope.chennai@communityrelief.org',
                'phone': '+91 97890 55443',
                'address': 'Greams Road, Thousand Lights',
                'city': 'Chennai',
                'accepted_food_types': 'Fresh Vegetables, Fruits, Grains, Bakery',
                'capacity_kg': 250.0,
                'is_verified': True,
                'description': 'Community kitchen providing 1,200 warm meals daily to homeless seniors and children.'
            }
        ]

        for ngo_data in sample_ngos:
            ngo = NGO(**ngo_data)
            db.session.add(ngo)
        db.session.commit()
        print(f"[Seed] Added {len(sample_ngos)} registered NGOs to database.")

    # 5. Seed Demo Foods & Initial Donations if empty
    demo_foods_count = Food.query.filter_by(user_id=demo_user.id).count()
    if demo_foods_count == 0:
        today = datetime.utcnow().date()
        demo_items = [
            {
                'food_name': 'Fresh Whole Milk',
                'category': 'dairy',
                'quantity': 4.0,
                'unit': 'L',
                'storage_type': 'refrigerator',
                'purchase_date': (today - timedelta(days=1)).isoformat(),
                'expiry_date': (today + timedelta(days=2)).isoformat(),
                'prep_time': 'Fresh Packaged',
                'location': '742 Evergreen Terrace, Springfield',
                'status': 'fresh',
                'risk': 'medium',
                'risk_score': 42,
                'donation_suitable': 'safe',
                'donation_status': 'pending',
                'notes': 'Sealed pasteurized milk cartons.'
            },
            {
                'food_name': 'Organic Tomatoes',
                'category': 'vegetables',
                'quantity': 5.0,
                'unit': 'kg',
                'storage_type': 'countertop',
                'purchase_date': (today - timedelta(days=2)).isoformat(),
                'expiry_date': (today + timedelta(days=3)).isoformat(),
                'prep_time': 'Fresh Harvest',
                'location': '742 Evergreen Terrace, Springfield',
                'status': 'fresh',
                'risk': 'low',
                'risk_score': 24,
                'donation_suitable': 'safe',
                'donation_status': 'accepted',
                'notes': 'Ripe farm-fresh red tomatoes.'
            },
            {
                'food_name': 'Vegetable Biryani & Curry Boxes',
                'category': 'cooked',
                'quantity': 25.0,
                'unit': 'pack',
                'storage_type': 'countertop',
                'purchase_date': today.isoformat(),
                'expiry_date': (today + timedelta(days=1)).isoformat(),
                'prep_time': 'Prepared 3 hours ago',
                'location': 'Grand Feast Banquet, City Center',
                'status': 'fresh',
                'risk': 'medium',
                'risk_score': 48,
                'donation_suitable': 'use_soon',
                'donation_status': 'pickup_scheduled',
                'notes': 'Surplus catering meal boxes, neatly packed in hygienic disposable containers.'
            },
            {
                'food_name': 'Whole Wheat Sliced Bread',
                'category': 'bakery',
                'quantity': 8.0,
                'unit': 'loaf',
                'storage_type': 'pantry',
                'purchase_date': (today - timedelta(days=1)).isoformat(),
                'expiry_date': (today + timedelta(days=4)).isoformat(),
                'prep_time': 'Baked Yesterday',
                'location': 'Bakery Corner, Main Street',
                'status': 'fresh',
                'risk': 'low',
                'risk_score': 18,
                'donation_suitable': 'safe',
                'donation_status': 'completed',
                'notes': 'Fresh artisan whole wheat bread loaves.'
            },
            {
                'food_name': 'Expired Dairy Cream',
                'category': 'dairy',
                'quantity': 1.0,
                'unit': 'L',
                'storage_type': 'countertop',
                'purchase_date': (today - timedelta(days=7)).isoformat(),
                'expiry_date': (today - timedelta(days=2)).isoformat(),
                'prep_time': 'Expired',
                'location': '742 Evergreen Terrace',
                'status': 'expired',
                'risk': 'high',
                'risk_score': 95,
                'donation_suitable': 'unsafe',
                'donation_status': 'not_donated',
                'notes': 'Past expiration date - not suitable for donation.'
            }
        ]

        created_foods = []
        for item_data in demo_items:
            food = Food(user_id=demo_user.id, **item_data)
            db.session.add(food)
            created_foods.append(food)
        db.session.commit()
        print(f"[Seed] Added {len(demo_items)} food records for Demo user.")

        # Seed sample donations to connect Donor & NGO workflow
        primary_ngo = NGO.query.filter_by(is_verified=True).first()
        if primary_ngo and len(created_foods) >= 4:
            # 1. Pending donation
            d1 = Donation(
                donor_id=demo_user.id,
                food_id=created_foods[0].id,
                ngo_id=primary_ngo.id,
                status='Pending',
                donor_notes='Available for pickup between 2 PM and 6 PM.'
            )
            db.session.add(d1)

            # 2. Accepted donation
            d2 = Donation(
                donor_id=demo_user.id,
                food_id=created_foods[1].id,
                ngo_id=primary_ngo.id,
                status='Accepted',
                donor_notes='Packaged in wooden crates.',
                ngo_notes='Accepted! Assigning pickup volunteer shortly.'
            )
            db.session.add(d2)

            # 3. Pickup Scheduled donation
            d3 = Donation(
                donor_id=demo_user.id,
                food_id=created_foods[2].id,
                ngo_id=primary_ngo.id,
                status='Pickup Scheduled',
                donor_notes='Food is ready at the service entrance.',
                ngo_notes='Pickup vehicle dispatched.'
            )
            db.session.add(d3)
            db.session.flush()

            p3 = PickupDetail(
                donation_id=d3.id,
                scheduled_time=(datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %I:%M %p'),
                agent_name='Vikram Singh (Food Rescue Volunteer)',
                agent_phone='+91 98222 33445',
                vehicle_info='White Maruti Eeco (DL-8C-4412)',
                pickup_notes='Please keep meal boxes in carton at service entrance.'
            )
            db.session.add(p3)

            # 4. Completed donation
            d4 = Donation(
                donor_id=demo_user.id,
                food_id=created_foods[3].id,
                ngo_id=primary_ngo.id,
                status='Completed',
                donor_notes='Surplus morning bake.',
                ngo_notes='Collected and successfully distributed to 45 children at Asha Shelter Home.'
            )
            db.session.add(d4)

            db.session.commit()
            print("[Seed] Seeded initial sample donations with full lifecycle.")

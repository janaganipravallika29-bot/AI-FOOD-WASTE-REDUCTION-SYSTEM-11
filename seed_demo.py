"""
FoodWise AI - Standalone Database Seed Script
Initializes the database and seeds initial Admin and Demo accounts.
Run with:
    python seed_demo.py
"""
from api.index import app
from backend.models import db
from backend.database import seed_initial_data

if __name__ == '__main__':
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Seeding initial data...")
        seed_initial_data()
        print("Database ready!")


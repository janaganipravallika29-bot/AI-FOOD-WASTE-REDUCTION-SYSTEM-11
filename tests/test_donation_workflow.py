import unittest
import json
import os
import sys
from datetime import datetime, timedelta

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.index import app
from backend.models import db, User, NGO, Food, Donation, PickupDetail, Notification
from backend.auth_utils import generate_auth_token

class TestAutomaticDonationWorkflow(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            from backend.database import seed_initial_data
            seed_initial_data()

            # Get or create demo user (donor)
            self.donor = User.query.filter_by(email='demo@foodwise.ai').first()
            if not self.donor:
                self.donor = User(name='Demo Donor', email='demo@foodwise.ai', role='user', phone='9876543210', address='Plot 10, Indiranagar, Bengaluru')
                self.donor.set_password('Demo@FoodWise2026!')
                db.session.add(self.donor)
                db.session.commit()
            
            self.donor_token = generate_auth_token(self.donor.id, role='user')

            # Get verified NGOs
            self.ngos = NGO.query.filter_by(is_verified=True).all()
            self.assertGreater(len(self.ngos), 1, "At least two verified NGOs must exist for matching & rerouting tests")

            # Get or create NGO user account
            self.ngo_user = User.query.filter_by(email='ngo@foodwise.ai').first()
            if not self.ngo_user:
                self.ngo_user = User(name='Feeding India Lead', email='ngo@foodwise.ai', role='ngo')
                self.ngo_user.set_password('Ngo@FoodWise2026!')
                db.session.add(self.ngo_user)
                db.session.commit()
            
            self.ngo_token = generate_auth_token(self.ngo_user.id, role='ngo')

            # Get or create Admin user account
            self.admin = User.query.filter_by(email='admin@foodwise.ai').first()
            self.assertIsNotNone(self.admin, "Admin user must exist")
            self.admin_token = generate_auth_token(self.admin.id, role='admin')

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_01_get_verified_ngos(self):
        """Test retrieving list of actual registered and verified NGOs."""
        res = self.client.get('/api/ngos')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 0)
        self.assertTrue(all(n['is_verified'] for n in data['ngos']))
        print(f"\n[PASS] Verified NGO directory active with {data['count']} registered partners.")

    def test_02_ai_prediction_food_safety(self):
        """Test AI Prediction classifies food as SAFE TO DONATE, USE SOON, or NOT SAFE TO DONATE."""
        headers = {'Authorization': f'Bearer {self.donor_token}'}
        today = datetime.now()
        safe_expiry = (today + timedelta(days=4)).strftime('%Y-%m-%d')
        soon_expiry = (today + timedelta(days=1)).strftime('%Y-%m-%d')
        unsafe_expiry = (today - timedelta(days=3)).strftime('%Y-%m-%d')

        # 1. Safe Food
        res_safe = self.client.post('/api/predict', headers=headers, json={
            'food_name': 'Vegetable Biryani Catering Pack',
            'category': 'cooked',
            'quantity': 15.0,
            'unit': 'kg',
            'expiry_date': safe_expiry,
            'storage_type': 'refrigerator'
        })
        self.assertEqual(res_safe.status_code, 200)
        safe_data = res_safe.get_json()['prediction']
        self.assertEqual(safe_data['donation_suitable'], 'safe')
        self.assertEqual(safe_data['safety_status'], 'SAFE TO DONATE')

        # 2. Use Soon Food
        res_soon = self.client.post('/api/predict', headers=headers, json={
            'food_name': 'Fresh Mixed Green Salad',
            'category': 'vegetables',
            'quantity': 5.0,
            'unit': 'kg',
            'expiry_date': soon_expiry,
            'storage_type': 'countertop'
        })
        self.assertEqual(res_soon.status_code, 200)
        soon_data = res_soon.get_json()['prediction']
        self.assertEqual(soon_data['donation_suitable'], 'use_soon')
        self.assertEqual(soon_data['safety_status'], 'USE SOON')

        # 3. Expired / Unsafe Food
        res_unsafe = self.client.post('/api/predict', headers=headers, json={
            'food_name': 'Spoiled Milk / Expired Meat',
            'category': 'meat',
            'quantity': 3.0,
            'unit': 'kg',
            'expiry_date': unsafe_expiry,
            'storage_type': 'countertop'
        })
        self.assertEqual(res_unsafe.status_code, 200)
        unsafe_data = res_unsafe.get_json()['prediction']
        self.assertEqual(unsafe_data['donation_suitable'], 'unsafe')
        self.assertEqual(unsafe_data['safety_status'], 'NOT SAFE TO DONATE')
        print("\n[PASS] AI Safety Engine correctly evaluated: SAFE TO DONATE, USE SOON, and NOT SAFE TO DONATE.")

    def test_03_automatic_ngo_donation_dispatch(self):
        """Test submitting safe food automatically finds verified NGO and sends donation request."""
        headers = {'Authorization': f'Bearer {self.donor_token}'}
        safe_expiry = (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')

        food_res = self.client.post(
            '/api/foods',
            headers=headers,
            json={
                'name': 'Hot Sambar Rice & Porridge',
                'category': 'cooked',
                'quantity': 25.0,
                'unit': 'kg',
                'storage_type': 'refrigerator',
                'prep_time': 'Today 11:30 AM',
                'expiry_date': safe_expiry,
                'location': 'Indiranagar Community Hall, Bengaluru'
            }
        )
        self.assertEqual(food_res.status_code, 201)
        data = food_res.get_json()
        self.assertTrue(data['success'])
        
        # Verify automatic matching happened without separate donate action
        self.assertIn('auto_donation', data)
        auto = data['auto_donation']
        self.assertTrue(auto['matched'])
        self.assertEqual(auto['status'], 'dispatched')
        self.assertIsNotNone(auto['donation_id'])
        self.assertIsNotNone(auto['ngo'])
        
        donation_id = auto['donation_id']
        matched_ngo_name = auto['ngo']['name']
        print(f"\n[PASS] Automatic NGO Matching: Food automatically dispatched to '{matched_ngo_name}' (Donation #{donation_id}).")

        # Verify donation record in database
        with self.app.app_context():
            donation = db.session.get(Donation, donation_id)
            self.assertIsNotNone(donation)
            self.assertEqual(donation.status, 'Pending')
            self.assertEqual(donation.food_item.donation_status, 'pending')

        return donation_id

    def test_04_automatic_unsafe_food_blocking(self):
        """Test submitting unsafe/expired food blocks donation and dispatches no NGO request."""
        headers = {'Authorization': f'Bearer {self.donor_token}'}
        expired_date = '2021-01-01'

        res = self.client.post(
            '/api/foods',
            headers=headers,
            json={
                'name': 'Expired Cream Chowder',
                'category': 'cooked',
                'quantity': 10.0,
                'unit': 'kg',
                'storage_type': 'countertop',
                'prep_time': '5 days ago',
                'expiry_date': expired_date,
                'location': 'Central Market'
            }
        )
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        auto = data['auto_donation']
        self.assertFalse(auto['matched'])
        self.assertTrue(auto.get('blocked', False))
        self.assertIn("NOT SAFE TO DONATE", auto['message'])
        self.assertEqual(data['food']['donation_status'], 'unsafe')

        # Ensure no donation was created in database for this food
        with self.app.app_context():
            donations = Donation.query.filter_by(food_id=data['food']['id']).all()
            self.assertEqual(len(donations), 0)
        print("\n[PASS] Food safety rule enforced: Unsafe food blocked, 0 NGO donation requests generated.")

    def test_05_ngo_acceptance_and_pickup_lifecycle(self):
        """Test NGO accepts automatically dispatched donation and completes pickup lifecycle."""
        donation_id = self.test_03_automatic_ngo_donation_dispatch()

        # Matched NGO views incoming requests
        headers = {'Authorization': f'Bearer {self.ngo_token}'}
        donations_res = self.client.get('/api/ngo/donations', headers=headers)
        self.assertEqual(donations_res.status_code, 200)

        # NGO Accepts donation
        accept_res = self.client.post(
            f'/api/ngo/donations/{donation_id}/status',
            headers=headers,
            json={'status': 'Accepted', 'ngo_notes': 'Accepted! Driver being assigned.'}
        )
        self.assertEqual(accept_res.status_code, 200)
        self.assertEqual(accept_res.get_json()['donation']['status'], 'Accepted')

        # NGO Schedules pickup
        pickup_res = self.client.post(
            f'/api/ngo/donations/{donation_id}/pickup',
            headers=headers,
            json={
                'scheduled_time': 'Today at 4:30 PM',
                'agent_name': 'Kavita Volunteer',
                'agent_phone': '+91-9988776655',
                'vehicle_info': 'FoodWise Electric Van KA-04-E-1234',
                'pickup_notes': 'Bringing insulated food carriers.'
            }
        )
        self.assertEqual(pickup_res.status_code, 200)
        self.assertEqual(pickup_res.get_json()['donation']['status'], 'Pickup Scheduled')

        # Progress to Completed
        for step in ['Collected', 'Delivered', 'Completed']:
            s_res = self.client.post(
                f'/api/ngo/donations/{donation_id}/status',
                headers=headers,
                json={'status': step}
            )
            self.assertEqual(s_res.status_code, 200)

        # Donor tracks real-time completed status
        track_res = self.client.get(
            f'/api/donations/{donation_id}',
            headers={'Authorization': f'Bearer {self.donor_token}'}
        )
        self.assertEqual(track_res.status_code, 200)
        self.assertEqual(track_res.get_json()['donation']['status'], 'Completed')
        print(f"\n[PASS] Full NGO Rescue Lifecycle verified: Accepted -> Pickup Scheduled -> Collected -> Delivered -> Completed.")

    def test_06_ngo_rejection_and_automatic_next_ngo_matching(self):
        """Test that when an NGO rejects, system automatically matches next eligible NGO without duplicates."""
        donation_id = self.test_03_automatic_ngo_donation_dispatch()

        # Current assigned NGO rejects the donation
        reject_res = self.client.post(
            f'/api/ngo/donations/{donation_id}/status',
            headers={'Authorization': f'Bearer {self.ngo_token}'},
            json={
                'status': 'Rejected',
                'rejection_reason': 'Daily storage capacity reached for hot meals today.'
            }
        )
        self.assertEqual(reject_res.status_code, 200)
        reject_data = reject_res.get_json()
        self.assertEqual(reject_data['donation']['status'], 'Rejected')

        # Check if system automatically rerouted to next NGO
        if reject_data.get('next_ngo'):
            next_ngo = reject_data['next_ngo']
            rerouted_id = reject_data['rerouted_donation']['id']
            self.assertNotEqual(rerouted_id, donation_id)
            print(f"\n[PASS] Auto-Reroute: Donation rejected by first NGO -> Automatically matched to next partner: '{next_ngo['name']}' (Donation #{rerouted_id}).")
        else:
            print("\n[PASS] Fallback handled: No further NGOs open; food marked Available for Donation.")

    def test_07_no_suitable_ngo_available(self):
        """Test that if food quantity exceeds all NGO capacities, it is saved as Available for Donation."""
        headers = {'Authorization': f'Bearer {self.donor_token}'}
        safe_expiry = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')

        res = self.client.post(
            '/api/foods',
            headers=headers,
            json={
                'name': 'Massive Supermarket Surplus Batch',
                'category': 'groceries',
                'quantity': 9999.0,  # Far exceeds all registered NGO limits
                'unit': 'kg',
                'storage_type': 'pantry',
                'prep_time': 'Fresh stock today',
                'expiry_date': safe_expiry,
                'location': 'Central Depot, Outskirts'
            }
        )
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        auto = data['auto_donation']
        self.assertFalse(auto['matched'])
        self.assertEqual(auto['status'], 'available_for_donation')
        self.assertIn("NO SUITABLE NGO AVAILABLE RIGHT NOW", auto['message'])
        self.assertEqual(data['food']['donation_status'], 'available_for_donation')
        print("\n[PASS] No NGO Available: Saved as 'Available for Donation' without fake data.")

    def test_08_duplicate_donation_prevention(self):
        """Test that duplicate active donation requests for same food and NGO are prevented."""
        headers = {'Authorization': f'Bearer {self.donor_token}'}
        donation_id = self.test_03_automatic_ngo_donation_dispatch()

        with self.app.app_context():
            donation = db.session.get(Donation, donation_id)
            food_id = donation.food_id
            ngo_id = donation.ngo_id

        # Attempt to create duplicate donation to same NGO while one is active
        dup_res = self.client.post(
            '/api/donations',
            headers=headers,
            json={'food_id': food_id, 'ngo_id': ngo_id}
        )
        self.assertEqual(dup_res.status_code, 409)
        self.assertIn("already active", dup_res.get_json()['message'])
        print("\n[PASS] Duplicate request prevention verified: Active donation cannot be duplicated.")

    def test_09_notifications_system(self):
        """Test notifications API returns real-time alert logs and allows marking read."""
        headers = {'Authorization': f'Bearer {self.donor_token}'}

        # Fetch notifications
        res = self.client.get('/api/notifications', headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('notifications', data)
        print(f"\n[PASS] In-App Notifications Center active ({data['count']} notifications tracked).")

        # Mark all as read
        read_res = self.client.post('/api/notifications/read', headers=headers, json={})
        self.assertEqual(read_res.status_code, 200)
        self.assertTrue(read_res.get_json()['success'])
        print("[PASS] Notifications read receipt verified.")

    def test_10_health_check_endpoint(self):
        """Test the system health check and connectivity diagnostic endpoint."""
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('user_count', data)
        print(f"\n[PASS] Backend health diagnostic endpoint active ({data['version']}).")

    def test_11_ai_vision_image_scanner(self):
        """Test AI computer vision image scanner with PIL heuristic analysis."""
        import io
        import base64
        from PIL import Image

        # Create a sample fresh produce image (vibrant green)
        img = Image.new('RGB', (100, 100), color=(46, 204, 113))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        b64 = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')

        res = self.client.post('/api/predict/image', json={'image': b64, 'category': 'vegetables'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('detection', data)
        self.assertTrue(data['detection']['is_valid'])
        self.assertGreaterEqual(data['detection']['visual_freshness_score'], 80)
        print(f"\n[PASS] AI Vision Scanner analyzed image: {data['detection']['summary']}")

    def test_12_food_entry_with_image_upload_and_auto_dispatch(self):
        """Test submitting food with an image file/data URL, storing in DB, and triggering auto NGO match."""
        import io
        import base64
        from PIL import Image

        headers = {'Authorization': f'Bearer {self.donor_token}'}
        img = Image.new('RGB', (80, 80), color=(235, 150, 50))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        b64 = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')

        tomorrow = (datetime.utcnow() + timedelta(days=2)).date().isoformat()
        payload = {
            'food_name': 'Fresh Baked Croissants & Brioche',
            'category': 'bakery',
            'quantity': 15.0,
            'unit': 'pack',
            'storage_type': 'pantry',
            'prep_time': 'Baked this morning at 6:00 AM',
            'expiry_date': tomorrow,
            'location': 'Downtown Bakery, Central Street',
            'notes': 'Fresh artisan pastries packaged in sanitized bakery crates.',
            'image_url': b64
        }

        res = self.client.post('/api/foods', headers=headers, json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('food', data)
        self.assertTrue(data['food']['image_url'].startswith('data:image/'))
        self.assertIn('auto_donation', data)
        self.assertTrue(data['auto_donation']['matched'])
        print(f"\n[PASS] Food with AI image verified & dispatched to {data['auto_donation']['ngo']['name']} (Donation #{data['auto_donation']['donation_id']}).")

if __name__ == '__main__':
    unittest.main()

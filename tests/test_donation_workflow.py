import unittest
import json
import os
import sys
from datetime import datetime, timedelta

# Ensure backend modules are loadable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.index import app
from backend.models import db, User, NGO, Food, Donation, PickupDetail
from backend.auth_utils import generate_auth_token

class TestDonationWorkflow(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            # Get or create demo user
            self.donor = User.query.filter_by(email='demo@foodwise.ai').first()
            if not self.donor:
                self.donor = User(name='Demo Donor', email='demo@foodwise.ai', role='user', phone='9876543210', address='123 Green St')
                self.donor.set_password('Demo@FoodWise2026!')
                db.session.add(self.donor)
                db.session.commit()
            
            self.donor_token = generate_auth_token(self.donor.id, role='user')

            # Get or create verified NGO
            self.ngo = NGO.query.filter_by(is_verified=True).first()
            self.assertIsNotNone(self.ngo, "At least one verified NGO must exist")

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

    def test_01_get_verified_ngos(self):
        """Test retrieving the list of verified NGOs for donation."""
        res = self.client.get('/api/ngos')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 0)
        self.assertTrue(all(n['is_verified'] for n in data['ngos']))
        print(f"\n[PASS] GET /api/ngos returned {data['count']} verified NGOs.")

    def test_02_ai_prediction_food_safety(self):
        """Test AI Prediction gives correct safety flags for safe, use-soon, and unsafe foods."""
        headers = {'Authorization': f'Bearer {self.donor_token}'}
        today = datetime.utcnow()
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
        print("\n[PASS] AI Safety Prediction correctly evaluated: safe, use_soon, and unsafe.")

    def test_03_create_food_and_donation_flow(self):
        """Test donor adds food and submits donation to a registered NGO."""
        today = datetime.utcnow()
        safe_expiry = (today + timedelta(days=4)).strftime('%Y-%m-%d')

        # Add food entry
        food_res = self.client.post(
            '/api/foods',
            headers={'Authorization': f'Bearer {self.donor_token}'},
            json={
                'name': 'Steamed Basmati Rice & Dal',
                'category': 'cooked',
                'quantity': 12.0,
                'unit': 'kg',
                'storage_type': 'refrigerator',
                'prep_time': 'Today 11:00 AM',
                'expiry_date': safe_expiry,
                'location': 'Community Hall, Sector 4, Bangalore'
            }
        )
        self.assertEqual(food_res.status_code, 201)
        food_data = food_res.get_json()
        food_id = food_data['food']['id']

        # Initiate Donation to NGO
        don_res = self.client.post(
            '/api/donations',
            headers={'Authorization': f'Bearer {self.donor_token}'},
            json={
                'food_id': food_id,
                'ngo_id': self.ngo.id,
                'donor_notes': 'Packed in 3 insulated thermal containers.'
            }
        )
        self.assertEqual(don_res.status_code, 201)
        don_data = don_res.get_json()
        self.assertTrue(don_data['success'])
        donation_id = don_data['donation']['id']
        self.assertEqual(don_data['donation']['status'], 'Pending')
        print(f"\n[PASS] Donation #{donation_id} created for food #{food_id} -> NGO '{self.ngo.name}'.")

        # Block Unsafe Food Donation
        unsafe_food = self.client.post(
            '/api/foods',
            headers={'Authorization': f'Bearer {self.donor_token}'},
            json={
                'name': 'Expired Seafood Soup',
                'category': 'cooked',
                'quantity': 4.0,
                'unit': 'kg',
                'storage_type': 'countertop',
                'expiry_date': '2020-01-01'
            }
        ).get_json()['food']

        blocked_don_res = self.client.post(
            '/api/donations',
            headers={'Authorization': f'Bearer {self.donor_token}'},
            json={
                'food_id': unsafe_food['id'],
                'ngo_id': self.ngo.id
            }
        )
        self.assertEqual(blocked_don_res.status_code, 400)
        self.assertIn("NOT SAFE TO DONATE", blocked_don_res.get_json()['message'])
        print("\n[PASS] Food safety policy successfully prevented donation of unsafe/expired food.")

        return donation_id

    def test_04_ngo_accept_and_pickup_progression(self):
        """Test NGO views incoming donation, schedules pickup, and marks completed."""
        donation_id = self.test_03_create_food_and_donation_flow()

        # NGO views donations
        ngo_view_res = self.client.get(
            '/api/ngo/donations',
            headers={'Authorization': f'Bearer {self.ngo_token}'}
        )
        self.assertEqual(ngo_view_res.status_code, 200)
        ngo_view_data = ngo_view_res.get_json()
        self.assertTrue(ngo_view_data['success'])

        # NGO schedules pickup
        pickup_res = self.client.post(
            f'/api/ngo/donations/{donation_id}/pickup',
            headers={'Authorization': f'Bearer {self.ngo_token}'},
            json={
                'scheduled_time': 'Today at 5:00 PM',
                'agent_name': 'Sunil Volunteer',
                'agent_phone': '+91-9123456780',
                'vehicle_info': 'FoodWise Eco Van KA-01-AB-9876',
                'pickup_notes': 'Arriving with temperature monitored boxes.'
            }
        )
        self.assertEqual(pickup_res.status_code, 200)
        pickup_data = pickup_res.get_json()
        self.assertEqual(pickup_data['donation']['status'], 'Pickup Scheduled')
        self.assertEqual(pickup_data['donation']['pickup']['agent_name'], 'Sunil Volunteer')
        print(f"\n[PASS] Pickup scheduled by NGO for Donation #{donation_id}.")

        # Progressive status updates: Collected -> Delivered -> Completed
        for step_status in ['Collected', 'Delivered', 'Completed']:
            stat_res = self.client.post(
                f'/api/ngo/donations/{donation_id}/status',
                headers={'Authorization': f'Bearer {self.ngo_token}'},
                json={'status': step_status}
            )
            self.assertEqual(stat_res.status_code, 200)
            self.assertEqual(stat_res.get_json()['donation']['status'], step_status)
        
        # Verify donor can track the completed status
        track_res = self.client.get(
            f'/api/donations/{donation_id}',
            headers={'Authorization': f'Bearer {self.donor_token}'}
        )
        self.assertEqual(track_res.status_code, 200)
        track_data = track_res.get_json()
        self.assertEqual(track_data['donation']['status'], 'Completed')
        print(f"\n[PASS] Complete donation lifecycle: Pending -> Pickup Scheduled -> Collected -> Delivered -> Completed verified!")

    def test_05_admin_ngo_management_and_oversight(self):
        """Test admin can list NGOs, toggle verification, and monitor all platform donations."""
        # Admin lists NGOs
        ngos_res = self.client.get(
            '/api/admin/ngos',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(ngos_res.status_code, 200)
        self.assertGreater(ngos_res.get_json()['count'], 0)

        # Admin toggles NGO verification
        toggle_res = self.client.post(
            f'/api/admin/ngos/{self.ngo.id}/verify',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(toggle_res.status_code, 200)

        # Toggle back to original state
        toggle_back_res = self.client.post(
            f'/api/admin/ngos/{self.ngo.id}/verify',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(toggle_back_res.status_code, 200)

        # Admin views global donations
        donations_res = self.client.get(
            '/api/admin/donations',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(donations_res.status_code, 200)
        don_data = donations_res.get_json()
        self.assertTrue(don_data['success'])
        self.assertIn('stats', don_data)
        print(f"\n[PASS] Admin oversight verified: {don_data['stats']['total']} total platform donations tracked.")

if __name__ == '__main__':
    unittest.main()

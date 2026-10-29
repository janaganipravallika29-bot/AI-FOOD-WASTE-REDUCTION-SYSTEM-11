"""
FoodWise AI - Comprehensive Automated Test Suite
Verifies all authentication, authorization, session, password-reset,
and user-specific data isolation scenarios.
"""
import unittest
import json
from api.index import app
from backend.models import db, User, Food
from backend.auth_utils import generate_auth_token, verify_reset_token


class FoodWiseAuthTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            from backend.database import seed_initial_data
            seed_initial_data()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Scenario 1: New user registration succeeds
    def test_01_user_registration_success(self):
        payload = {
            'name': 'Alice Test',
            'email': 'alice@example.com',
            'password': 'Password123!'
        }
        res = self.client.post('/api/signup', data=json.dumps(payload), content_type='application/json')
        data = res.get_json()
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIn('token', data)
        self.assertEqual(data['user']['email'], 'alice@example.com')
        self.assertEqual(data['user']['role'], 'user')

    # Scenario 2: Existing user login with correct credentials
    def test_02_user_login_success(self):
        # First register
        self.client.post('/api/signup', data=json.dumps({
            'name': 'Bob Test',
            'email': 'bob@example.com',
            'password': 'Password123!'
        }), content_type='application/json')

        # Then login
        res = self.client.post('/api/login', data=json.dumps({
            'email': 'bob@example.com',
            'password': 'Password123!'
        }), content_type='application/json')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['name'], 'Bob Test')

    # Scenario 3: Incorrect password is rejected
    def test_03_incorrect_password_rejected(self):
        self.client.post('/api/signup', data=json.dumps({
            'name': 'Charlie',
            'email': 'charlie@example.com',
            'password': 'Password123!'
        }), content_type='application/json')

        res = self.client.post('/api/login', data=json.dumps({
            'email': 'charlie@example.com',
            'password': 'WrongPassword999'
        }), content_type='application/json')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertIn('Invalid email or password', data['message'])

    # Scenario 4: Unregistered email cannot log in
    def test_04_unregistered_email_rejected(self):
        res = self.client.post('/api/login', data=json.dumps({
            'email': 'ghost@example.com',
            'password': 'Password123!'
        }), content_type='application/json')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # Scenario 5: Duplicate email registration rejected
    def test_05_duplicate_email_rejected(self):
        payload = {
            'name': 'Dan Original',
            'email': 'dan@example.com',
            'password': 'Password123!'
        }
        res1 = self.client.post('/api/signup', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res1.status_code, 201)

        # Duplicate attempt
        res2 = self.client.post('/api/signup', data=json.dumps({
            'name': 'Dan Clone',
            'email': 'dan@example.com',
            'password': 'Password123!'
        }), content_type='application/json')
        data2 = res2.get_json()
        self.assertEqual(res2.status_code, 409)
        self.assertFalse(data2['success'])
        self.assertIn('already exists', data2['message'])

    # Scenario 6: Empty fields and invalid email formats handled
    def test_06_validation_handling(self):
        # Empty name
        r1 = self.client.post('/api/signup', data=json.dumps({
            'name': '',
            'email': 'valid@example.com',
            'password': 'Password123!'
        }), content_type='application/json')
        self.assertEqual(r1.status_code, 400)

        # Invalid email format
        r2 = self.client.post('/api/signup', data=json.dumps({
            'name': 'Valid Name',
            'email': 'not-an-email',
            'password': 'Password123!'
        }), content_type='application/json')
        self.assertEqual(r2.status_code, 400)

        # Short password
        r3 = self.client.post('/api/signup', data=json.dumps({
            'name': 'Valid Name',
            'email': 'valid2@example.com',
            'password': '123'
        }), content_type='application/json')
        self.assertEqual(r3.status_code, 400)

    # Scenario 9: Demo account login works
    def test_09_demo_account_login(self):
        res = self.client.post('/api/demo-login')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['email'], 'demo@foodwise.ai')
        self.assertEqual(data['user']['role'], 'demo')

        # Verify demo user has pre-populated food records
        token = data['token']
        food_res = self.client.get('/api/foods', headers={'Authorization': f'Bearer {token}'})
        food_data = food_res.get_json()
        self.assertEqual(food_res.status_code, 200)
        self.assertGreaterEqual(len(food_data['foods']), 5)

    # Scenario 10: Logout endpoint
    def test_10_logout_clears_session(self):
        res = self.client.post('/api/logout')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Scenario 11: Protected endpoints reject unauthenticated access
    def test_11_protected_endpoints_reject_unauthenticated(self):
        res = self.client.get('/api/me')
        self.assertEqual(res.status_code, 401)

        res_foods = self.client.get('/api/foods')
        self.assertEqual(res_foods.status_code, 401)

    # Scenario 12: Private data isolation between users
    def test_12_user_data_isolation(self):
        # Register User A
        res_a = self.client.post('/api/signup', data=json.dumps({
            'name': 'User A',
            'email': 'userA@example.com',
            'password': 'Password123!'
        }), content_type='application/json')
        token_a = res_a.get_json()['token']

        # Register User B
        res_b = self.client.post('/api/signup', data=json.dumps({
            'name': 'User B',
            'email': 'userB@example.com',
            'password': 'Password123!'
        }), content_type='application/json')
        token_b = res_b.get_json()['token']

        # User A adds a private food
        add_res = self.client.post('/api/foods', headers={'Authorization': f'Bearer {token_a}'}, data=json.dumps({
            'food_name': 'Private Caviar A',
            'category': 'other',
            'quantity': 1,
            'unit': 'jar'
        }), content_type='application/json')
        food_a_id = add_res.get_json()['food']['id']

        # User B fetches their foods -> Caviar A must NOT be present
        b_foods_res = self.client.get('/api/foods', headers={'Authorization': f'Bearer {token_b}'})
        b_foods = b_foods_res.get_json()['foods']
        b_food_names = [f['food_name'] for f in b_foods]
        self.assertNotIn('Private Caviar A', b_food_names)

        # User B attempts to delete User A's food item -> Rejected (404/Forbidden)
        del_res = self.client.delete(f'/api/foods/{food_a_id}', headers={'Authorization': f'Bearer {token_b}'})
        self.assertEqual(del_res.status_code, 404)

    # Scenario 13: Normal users cannot access Admin functionality
    def test_13_normal_user_cannot_access_admin(self):
        # Register normal user
        res = self.client.post('/api/signup', data=json.dumps({
            'name': 'Regular User',
            'email': 'reg@example.com',
            'password': 'Password123!'
        }), content_type='application/json')
        token = res.get_json()['token']

        # Try to access admin users endpoint
        admin_res = self.client.get('/api/admin/users', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(admin_res.status_code, 403)

        # Admin login with admin account works
        admin_login_res = self.client.post('/api/admin/login', data=json.dumps({
            'email': 'admin@foodwise.ai',
            'password': 'Admin@FoodWise2026!'
        }), content_type='application/json')
        self.assertEqual(admin_login_res.status_code, 200)
        admin_token = admin_login_res.get_json()['token']

        # Admin accessing admin users endpoint succeeds
        admin_users_res = self.client.get('/api/admin/users', headers={'Authorization': f'Bearer {admin_token}'})
        self.assertEqual(admin_users_res.status_code, 200)

    # Scenario 14: Forgot password and reset workflow
    def test_14_forgot_password_reset_flow(self):
        # Register user
        self.client.post('/api/signup', data=json.dumps({
            'name': 'Reset Target',
            'email': 'reset_me@example.com',
            'password': 'Password123!'
        }), content_type='application/json')

        # Request reset
        forgot_res = self.client.post('/api/forgot-password', data=json.dumps({
            'email': 'reset_me@example.com'
        }), content_type='application/json')
        forgot_data = forgot_res.get_json()
        self.assertEqual(forgot_res.status_code, 200)
        self.assertTrue(forgot_data['success'])

        # In dev mode, reset link with token is returned
        self.assertIn('dev_reset_link', forgot_data)
        token = forgot_data['dev_reset_link'].split('token=')[1]

        # Reset password using token
        reset_res = self.client.post('/api/reset-password', data=json.dumps({
            'token': token,
            'password': 'NewBrandNewPassword456!'
        }), content_type='application/json')
        reset_data = reset_res.get_json()
        self.assertEqual(reset_res.status_code, 200)
        self.assertTrue(reset_data['success'])

        # Try logging in with old password -> must fail
        old_login = self.client.post('/api/login', data=json.dumps({
            'email': 'reset_me@example.com',
            'password': 'Password123!'
        }), content_type='application/json')
        self.assertEqual(old_login.status_code, 401)

        # Login with new password -> must succeed
        new_login = self.client.post('/api/login', data=json.dumps({
            'email': 'reset_me@example.com',
            'password': 'NewBrandNewPassword456!'
        }), content_type='application/json')
        self.assertEqual(new_login.status_code, 200)

        # Single-use check: reusing same reset token must be rejected
        reuse_res = self.client.post('/api/reset-password', data=json.dumps({
            'token': token,
            'password': 'AnotherPassword789!'
        }), content_type='application/json')
        self.assertEqual(reuse_res.status_code, 400)


if __name__ == '__main__':
    unittest.main()


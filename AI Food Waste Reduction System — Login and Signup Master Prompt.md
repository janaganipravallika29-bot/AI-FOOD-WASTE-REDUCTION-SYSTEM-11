# MASTER PROMPT — LOGIN / SIGNUP AUTHENTICATION

You are an expert Flask authentication and security developer.

My project is:

**AI FOOD WASTE REDUCTION SYSTEM**

The project already contains:

- Professional frontend
- Flask backend
- SQLAlchemy database
- User model

Now implement a complete, secure, professional **LOGIN + SIGNUP + LOGOUT + SESSION MANAGEMENT + ROLE-BASED AUTHENTICATION** system.

Do not create a frontend-only login using localStorage.

Authentication must use the Flask backend and database.

---

# 1. AUTHENTICATION TECHNOLOGY

Use:

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug password hashing
- Jinja2 templates
- Sessions
- Environment variables

Install if required:

```bash
pip install flask flask-sqlalchemy flask-login python-dotenv
```

Update:

```text
requirements.txt
```

---

# 2. AUTHENTICATION FLOW

Implement this complete flow:

```text
HOME
  ↓
GET STARTED
  ↓
SIGNUP
  ↓
VALIDATE USER
  ↓
HASH PASSWORD
  ↓
SAVE USER TO DATABASE
  ↓
LOGIN
  ↓
VERIFY EMAIL + PASSWORD
  ↓
CREATE SESSION
  ↓
DASHBOARD
```

Logout:

```text
DASHBOARD
  ↓
LOGOUT
  ↓
DESTROY SESSION
  ↓
LOGIN PAGE
```

---

# 3. USER DATABASE MODEL

Use the existing `users` table.

Required fields:

```text
id
name
email
password_hash
role
created_at
updated_at
```

Do NOT create another user table if one already exists.

---

# 4. SIGNUP PAGE

Use the existing:

```text
templates/signup.html
```

Create a professional form:

```text
CREATE YOUR ACCOUNT

Full Name
[________________________]

Email Address
[________________________]

Password
[________________________] 👁

Confirm Password
[________________________] 👁

Password Strength
[████████░░]

☐ I agree to the Terms and Conditions

[ CREATE ACCOUNT ]

Already have an account?
LOGIN
```

---

# 5. SIGNUP FRONTEND VALIDATION

Before submitting, validate:

### Name

- Required
- Minimum 2 characters
- No unnecessary special characters

### Email

- Required
- Valid email format

### Password

Minimum requirements:

- At least 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

Optionally recommend:

- Special character

### Confirm Password

Must match password.

Display errors directly below the relevant field.

---

# 6. PASSWORD STRENGTH INDICATOR

Create a dynamic password strength indicator.

States:

```text
Weak
Medium
Strong
```

Example:

```text
Password Strength: Strong
```

Do not rely only on frontend validation.

The backend must validate password requirements again.

---

# 7. SIGNUP BACKEND ROUTE

Create:

```text
GET  /signup
POST /signup
```

When POST is received:

```text
Signup Form
     ↓
Flask
     ↓
Validate Input
     ↓
Check Email
     ↓
Check Password
     ↓
Hash Password
     ↓
Create User
     ↓
Database
     ↓
Success Message
     ↓
Login
```

---

# 8. EMAIL DUPLICATE CHECK

Before creating a user:

```text
Search users table by email
```

If the email already exists:

Display:

```text
An account with this email already exists.
Please login instead.
```

Do not create duplicate accounts.

The database must also enforce email uniqueness.

---

# 9. PASSWORD HASHING

NEVER store passwords as plain text.

Use:

```python
from werkzeug.security import generate_password_hash
```

Store:

```text
password_hash
```

not:

```text
password
```

When creating a user:

```python
password_hash = generate_password_hash(password)
```

---

# 10. LOGIN PAGE

Use:

```text
templates/login.html
```

Design:

```text
WELCOME BACK 👋

Login to your AI Food Waste Dashboard

Email Address
[________________________]

Password
[________________________] 👁

☐ Remember Me

[ LOGIN ]

Forgot Password?

Don't have an account?
CREATE ACCOUNT
```

Maintain the same green/teal environmental design as the rest of the application.

---

# 11. LOGIN BACKEND ROUTE

Create:

```text
GET  /login
POST /login
```

Flow:

```text
Login Form
    ↓
Flask
    ↓
Find User by Email
    ↓
Check Password Hash
    ↓
Valid?
 ┌──┴──┐
NO    YES
 ↓      ↓
Error   login_user()
         ↓
      Dashboard
```

Use:

```python
check_password_hash()
```

---

# 12. INVALID LOGIN

If email does not exist or password is incorrect, display:

```text
Invalid email or password.
```

Do not reveal whether the email exists.

Do not show sensitive database information.

---

# 13. FLASK-LOGIN

Configure Flask-Login properly.

Create:

```python
LoginManager
```

Set:

```text
login_view = "auth.login"
```

Implement:

```python
@login_manager.user_loader
def load_user(user_id):
    ...
```

The `User` model must implement the Flask-Login requirements.

---

# 14. SESSION MANAGEMENT

After successful login:

```python
login_user(user)
```

The user should remain logged in while navigating between protected pages.

Protected pages:

```text
/dashboard
/food-entry
/predict
/recommendations
/reports
/profile
```

Use:

```python
@login_required
```

where appropriate.

---

# 15. LOGOUT

Create:

```text
GET /logout
```

Use:

```python
logout_user()
```

Then redirect to:

```text
/login
```

Show:

```text
You have been logged out successfully.
```

---

# 16. PROTECTED ROUTES

Unauthenticated users must NOT access:

```text
Dashboard
Food Entry
Prediction
Recommendations
Reports
Profile
```

If they try:

```text
/login
```

or the configured login route should be used automatically.

---

# 17. ADMIN AUTHENTICATION

Use the existing:

```text
role
```

field.

Allowed roles:

```text
user
admin
```

Normal user:

```text
role = user
```

Admin:

```text
role = admin
```

Do NOT allow users to select `admin` during signup.

The signup form must NEVER contain an admin-role field.

---

# 18. ADMIN LOGIN

If an admin logs in:

```text
LOGIN
  ↓
Check role
  ↓
admin
  ↓
ADMIN DASHBOARD
```

Normal user:

```text
LOGIN
  ↓
Check role
  ↓
user
  ↓
USER DASHBOARD
```

---

# 19. ADMIN ACCESS PROTECTION

Create an authorization decorator or helper.

Only:

```text
current_user.role == "admin"
```

can access:

```text
/admin
/admin/users
/admin/foods
/admin/predictions
/admin/reports
```

Normal users attempting to access admin pages must receive:

```text
403 Forbidden
```

or be safely redirected to the dashboard.

---

# 20. REMEMBER ME

Implement the:

```text
☐ Remember Me
```

checkbox using Flask-Login's supported session behavior.

Do not create insecure custom authentication tokens.

---

# 21. USER SESSION DATA

After login, the application should be able to access:

```text
current_user.id
current_user.name
current_user.email
current_user.role
```

Use this information to display:

```text
Welcome, Pravalika 👋
```

or the actual logged-in user's name.

---

# 22. NAVIGATION CHANGES

Before login, navbar should show:

```text
Home
About
Features
How It Works
Login
Get Started
```

After login:

```text
Dashboard
Food Entry
Predictions
Recommendations
Reports
Profile
Logout
```

For admin:

```text
Admin Dashboard
Users
Food Entries
Predictions
Reports
Logout
```

Do not show admin links to normal users.

---

# 23. FLASH MESSAGES

Use Flask flash messages.

Signup success:

```text
Account created successfully. Please login.
```

Login success:

```text
Welcome back!
```

Wrong login:

```text
Invalid email or password.
```

Duplicate email:

```text
An account with this email already exists.
```

Logout:

```text
You have been logged out.
```

Unauthorized:

```text
You are not authorized to access this page.
```

Display messages using attractive alert components.

---

# 24. DATABASE CONNECTION

Signup must write to:

```text
users
```

Login must read from:

```text
users
```

Example:

```text
SIGNUP
 ↓
Flask
 ↓
SQLAlchemy
 ↓
users table
```

Login:

```text
LOGIN
 ↓
Flask
 ↓
SQLAlchemy
 ↓
users table
 ↓
Password verification
 ↓
Flask session
```

---

# 25. ACTIVITY LOGGING

If the existing `activities` table is available, record:

### Successful signup

```text
ACCOUNT_CREATED
```

### Successful login

```text
LOGIN
```

### Logout

```text
LOGOUT
```

### Profile update

```text
PROFILE_UPDATED
```

Do not store passwords or sensitive authentication information in activity logs.

---

# 26. SECURITY REQUIREMENTS

Implement:

- Password hashing
- Secure sessions
- Login protection
- Role-based authorization
- Input validation
- Email uniqueness
- Safe error messages
- CSRF protection for forms if using Flask-WTF
- Environment-based secret key
- No passwords in logs
- No passwords in URLs
- No credentials in JavaScript
- No authentication through localStorage

---

# 27. SECRET KEY

Use `.env`.

Example:

```text
SECRET_KEY=replace_with_a_secure_random_secret
```

Load it using:

```python
from dotenv import load_dotenv
```

Never hardcode the production secret key.

Add:

```text
.env
```

to `.gitignore`.

---

# 28. OPTIONAL FORGOT PASSWORD UI

Create a professional:

```text
Forgot Password?
```

interface.

For the initial local project version, you may create the UI and route structure without implementing real email delivery.

Do NOT pretend a password-reset email was sent if no email service is configured.

If implementing password reset later, use a secure, time-limited token.

---

# 29. AUTHENTICATION FILE STRUCTURE

Use a modular structure:

```text
routes/
│
└── auth_routes.py
```

Put authentication routes inside:

```text
auth_routes.py
```

Do not put all authentication logic into a huge `app.py`.

Suggested structure:

```text
app.py
config.py

models/
└── user.py

routes/
└── auth_routes.py

templates/
├── login.html
└── signup.html

static/
├── css/
│   └── style.css
└── js/
    └── script.js
```

---

# 30. BLUEPRINT

Create:

```python
auth_bp = Blueprint(
    "auth",
    __name__
)
```

Routes:

```text
/auth/signup
/auth/login
/auth/logout
```

If the existing project uses routes without `/auth`, preserve the current URL structure so existing frontend navigation does not break.

---

# 31. USER MODEL

Make sure the User model supports Flask-Login.

Example:

```python
from flask_login import UserMixin

class User(UserMixin, db.Model):
    ...
```

The model must provide the required user identity functionality.

---

# 32. LOGIN REDIRECT

After successful normal-user login:

```text
/dashboard
```

After successful admin login:

```text
/admin
```

If the user was redirected to login from a protected page, safely return them to the intended page where appropriate.

Do not allow unsafe external redirect URLs.

---

# 33. SIGNUP REDIRECT

After successful signup:

```text
Signup
 ↓
Save User
 ↓
Flash Success
 ↓
Login
```

Do not automatically create an admin account from public signup.

---

# 34. RESPONSIVE AUTHENTICATION UI

Login and signup must work properly on:

- Desktop
- Laptop
- Tablet
- Mobile

On mobile:

```text
Image/illustration
      ↓
Form
```

Use clean spacing and readable fields.

---

# 35. LOGIN/SIGNUP DESIGN

Use the same branding as:

**AI FOOD WASTE REDUCTION SYSTEM**

Visual theme:

- Green
- Emerald
- Teal
- White
- Light gray
- Environmental/AI icons

Add subtle animations:

- Form fade-in
- Button hover
- Input focus
- Password strength animation

Do not overuse animations.

---

# 36. VALIDATION ERROR DESIGN

Example:

```text
Email Address
[wrong-email]

⚠ Please enter a valid email address.
```

Password:

```text
Password
[123]

⚠ Password must contain at least 8 characters.
```

Confirm password:

```text
⚠ Passwords do not match.
```

Make errors clear and accessible.

---

# 37. DATABASE TESTING

Test signup:

```text
Create new user
 ↓
Check users table
 ↓
Verify password_hash exists
 ↓
Verify plain password is NOT stored
```

Test duplicate:

```text
Existing email
 ↓
Signup
 ↓
Error
 ↓
No duplicate database record
```

Test login:

```text
Correct email + password
 ↓
Dashboard
```

Test invalid login:

```text
Wrong password
 ↓
Error
```

Test logout:

```text
Logout
 ↓
Protected page
 ↓
Redirect to login
```

---

# 38. SECURITY TESTING

Test:

```text
Normal user → /admin
```

Expected:

```text
BLOCKED
```

Test:

```text
Logged-out user → /dashboard
```

Expected:

```text
REDIRECT TO LOGIN
```

Test:

```text
User modifies role field in browser
```

Expected:

```text
Admin role must NOT be accepted from signup form.
```

Test:

```text
Wrong password
```

Expected:

```text
No login session created.
```

---

# 39. FINAL AUTHENTICATION FLOW

The final system must work exactly like this:

```text
                 HOME
                   │
                   ↓
             GET STARTED
                   │
                   ↓
             ┌───────────┐
             │  SIGNUP   │
             └─────┬─────┘
                   ↓
            Validate Input
                   ↓
             Hash Password
                   ↓
              DATABASE
                   │
                   ↓
                LOGIN
                   │
             ┌─────┴─────┐
             ↓           ↓
           USER         ADMIN
             ↓           ↓
        DASHBOARD    ADMIN PANEL
             │
             ↓
        FOOD ENTRY
             ↓
         AI PREDICTION
             ↓
       RECOMMENDATIONS
             ↓
          REPORTS
             ↓
           LOGOUT
             ↓
           LOGIN
```

---

# 40. FINAL FILES

After implementation, ensure these exist:

```text
app.py
config.py
requirements.txt
.env
.gitignore

models/
└── user.py

routes/
└── auth_routes.py

templates/
├── login.html
├── signup.html
├── dashboard.html
└── 403.html

static/
├── css/
│   └── style.css
└── js/
    └── script.js
```

Do not duplicate files if they already exist.

---

# 41. FINAL CHECKLIST

Before finishing, verify:

[ ] Signup page works

[ ] Login page works

[ ] Logout works

[ ] User is saved in database

[ ] Password is hashed

[ ] Duplicate email is prevented

[ ] Password validation works

[ ] Confirm password validation works

[ ] Flask-Login works

[ ] Sessions work

[ ] Protected pages work

[ ] Normal users cannot access admin pages

[ ] Admin users can access admin pages

[ ] Flash messages work

[ ] Dashboard displays logged-in user's name

[ ] Navbar changes after login

[ ] Logout removes authentication

[ ] Mobile login works

[ ] Mobile signup works

[ ] No credentials are stored in localStorage

[ ] No plain-text passwords are stored

[ ] No secrets are exposed in frontend code

[ ] `.env` is protected

[ ] Authentication routes are modular

[ ] Existing frontend navigation still works

---

# FINAL INSTRUCTION

Implement the complete authentication system for:

**AI FOOD WASTE REDUCTION SYSTEM**

Connect:

**Signup → Flask → Password Hashing → Database → Login → Flask-Login Session → User Dashboard**

and:

**Admin Login → Role Verification → Admin Dashboard**

Build it completely, test it, connect it to the existing frontend and database, and make it ready for the next stage:

**FOOD ENTRY → ML MODEL → PREDICTION → RECOMMENDATIONS → DASHBOARD → REPORTS → ADMIN → TESTING → DEPLOYMENT.**
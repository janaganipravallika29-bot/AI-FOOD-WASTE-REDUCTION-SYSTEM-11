# MASTER PROMPT — FLASK BACKEND DEVELOPMENT

You are an expert Python Flask backend developer.

I already have a frontend for my project:

**AI FOOD WASTE REDUCTION SYSTEM**

Now build the complete Flask backend from scratch and connect it properly with the existing frontend.

The backend must be professional, secure, modular, database-ready, ML-ready, and suitable for a college project demonstration.

Do not create only a basic Flask server. Implement the complete backend required for the application.

---

# 1. TECHNOLOGY STACK

Use:

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug password hashing
- Flask-CORS if required
- python-dotenv
- SQLite for initial development
- PostgreSQL-ready configuration for deployment
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Pillow

Install:

```bash
pip install flask flask-sqlalchemy flask-login flask-cors python-dotenv pandas numpy scikit-learn joblib pillow
```

Generate:

```text
requirements.txt
```

---

# 2. BACKEND FOLDER STRUCTURE

Create this structure:

```text
AI_Food_Waste_Reduction_System/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── database/
│   └── app.db
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── food_entry.py
│   ├── prediction.py
│   └── recommendation.py
│
├── ml/
│   ├── train_model.py
│   ├── prediction.py
│   ├── preprocessing.py
│   ├── dataset.csv
│   └── food_waste_model.pkl
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── food_routes.py
│   ├── dashboard_routes.py
│   ├── report_routes.py
│   └── admin_routes.py
│
├── utils/
│   ├── recommendations.py
│   └── helpers.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── food_entry.html
│   ├── prediction.html
│   ├── recommendations.html
│   ├── reports.html
│   ├── profile.html
│   ├── admin.html
│   ├── 404.html
│   └── 500.html
│
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    ├── images/
    └── uploads/
```

If the frontend files already exist, DO NOT overwrite them unnecessarily. Modify only what is required to connect them to Flask.

---

# 3. FLASK APPLICATION

Create `app.py`.

Configure:

- Flask application
- Secret key
- SQLAlchemy
- Flask-Login
- Error handlers
- Blueprint registration
- Database initialization

The application should run using:

```bash
python app.py
```

and open:

```text
http://127.0.0.1:5000
```

---

# 4. CONFIGURATION

Create:

```text
config.py
```

Use environment variables.

Example:

```text
SECRET_KEY
DATABASE_URL
UPLOAD_FOLDER
```

Do not hardcode sensitive credentials.

Create `.env`.

Do NOT expose `.env` publicly.

---

# 5. DATABASE

Use:

**SQLite for development**

Database:

```text
database/app.db
```

Make the architecture PostgreSQL-ready for deployment.

Use SQLAlchemy ORM.

---

# 6. USER MODEL

Create a `User` model.

Fields:

```text
id
name
email
password_hash
role
created_at
```

Roles:

```text
user
admin
```

Email must be unique.

Never store plain-text passwords.

Use:

```python
generate_password_hash()
check_password_hash()
```

---

# 7. FOOD ENTRY MODEL

Create:

```text
FoodEntry
```

Fields:

```text
id
user_id
food_name
category
quantity
unit
purchase_date
expiry_date
storage_type
temperature
previous_waste
image_filename
created_at
```

Create relationship:

```text
User → FoodEntry
```

One user can have multiple food entries.

---

# 8. PREDICTION MODEL

Create:

```text
Prediction
```

Fields:

```text
id
food_entry_id
waste_level
confidence
created_at
```

Possible values:

```text
LOW
MEDIUM
HIGH
```

---

# 9. RECOMMENDATION MODEL

Create:

```text
Recommendation
```

Fields:

```text
id
food_entry_id
recommendation_text
created_at
```

---

# 10. SIGNUP BACKEND

Create route:

```text
/signup
```

Method:

```text
GET
POST
```

When user submits signup:

1. Validate name.
2. Validate email.
3. Validate password.
4. Validate confirm password.
5. Check whether email already exists.
6. Hash password.
7. Create user.
8. Save to database.
9. Redirect to login.

Show appropriate error messages.

---

# 11. LOGIN BACKEND

Create:

```text
/login
```

Method:

```text
GET
POST
```

Flow:

```text
Login Form
     ↓
Flask
     ↓
Find User
     ↓
Verify Password
     ↓
Create Login Session
     ↓
Dashboard
```

Use Flask-Login.

---

# 12. LOGOUT

Create:

```text
/logout
```

When logout is clicked:

```text
logout_user()
```

Then redirect to:

```text
/login
```

---

# 13. LOGIN PROTECTION

Protect private pages.

Unauthenticated users should NOT access:

```text
/dashboard
/food-entry
/prediction
/recommendations
/reports
/profile
```

If not logged in, redirect to:

```text
/login
```

---

# 14. DASHBOARD BACKEND

Create:

```text
/dashboard
```

Retrieve actual database information.

Calculate:

```text
Total Food Entries
Low Risk Count
Medium Risk Count
High Risk Count
Total Quantity
Estimated Food Saved
Waste Reduction Percentage
```

Send these values to:

```text
dashboard.html
```

Do NOT hardcode dashboard statistics.

---

# 15. FOOD ENTRY BACKEND

Create:

```text
/food-entry
```

Support:

```text
GET
POST
```

The form should accept:

```text
food_name
category
quantity
unit
purchase_date
expiry_date
storage_type
temperature
previous_waste
food_image
```

Validate all fields.

Save the food information in the database.

---

# 16. IMAGE UPLOAD

Allow:

```text
JPG
JPEG
PNG
WEBP
```

Save files to:

```text
static/uploads/
```

Use secure filenames.

Use:

```python
secure_filename()
```

Limit upload size.

Do not allow arbitrary file types.

---

# 17. FOOD VALIDATION

Validate:

### Food name

Must not be empty.

### Quantity

Must be numeric and greater than zero.

### Dates

Expiry date should not be earlier than purchase date.

### Temperature

Must be a valid numeric value if provided.

### Image

Must be an allowed image type.

Display useful validation errors.

---

# 18. ML MODEL

Create:

```text
ml/train_model.py
```

Create or load a dataset containing:

```text
food_name
category
quantity
days_remaining
storage_type
temperature
previous_waste
waste_level
```

Train a classification model.

Use:

```text
RandomForestClassifier
```

or another appropriate classification algorithm.

Output:

```text
LOW
MEDIUM
HIGH
```

Save the trained model:

```text
ml/food_waste_model.pkl
```

---

# 19. ML PREDICTION

Create:

```text
ml/prediction.py
```

The function should:

```text
receive food data
       ↓
preprocess features
       ↓
load trained model
       ↓
predict waste level
       ↓
calculate confidence
       ↓
return result
```

Example output:

```text
Prediction: HIGH
Confidence: 87%
```

Do not use fake/random predictions in the final backend.

The prediction must come from the trained model.

---

# 20. PREDICTION ROUTE

Create:

```text
/predict
```

Method:

```text
POST
```

Flow:

```text
Food Entry
     ↓
Calculate Days Remaining
     ↓
Prepare Features
     ↓
ML Model
     ↓
LOW / MEDIUM / HIGH
     ↓
Save Prediction
     ↓
Generate Recommendations
     ↓
Save Recommendations
     ↓
Prediction Page
```

---

# 21. PREDICTION PAGE DATA

Send:

```text
food_name
category
quantity
expiry_date
days_remaining
waste_level
confidence
```

to:

```text
prediction.html
```

The frontend must display the actual backend result.

---

# 22. RECOMMENDATION ENGINE

Create:

```text
utils/recommendations.py
```

Generate recommendations based on:

```text
waste_level
days_remaining
category
storage_type
quantity
```

For HIGH:

```text
Consume food soon.
Improve storage conditions.
Consider meal planning.
Avoid purchasing additional quantity.
Consider safe donation where appropriate.
```

For MEDIUM:

```text
Monitor expiry.
Improve storage.
Use FIFO.
Plan meals around the food.
```

For LOW:

```text
Continue proper storage.
Monitor expiry.
Maintain current food management practices.
```

Save recommendations to the database.

---

# 23. RECOMMENDATIONS ROUTE

Create:

```text
/recommendations/<food_id>
```

Only allow the logged-in user to access their own recommendations.

Display:

```text
Food
Prediction
Confidence
Recommendations
```

---

# 24. REPORT BACKEND

Create:

```text
/reports
```

Retrieve data from the database.

Calculate:

```text
Total Food Entries
Total High Risk
Total Medium Risk
Total Low Risk
Total Quantity
Waste Reduction
Food Saved
```

Provide data required by Chart.js.

Use JSON endpoints if necessary.

---

# 25. REPORT API

Create an endpoint such as:

```text
/api/reports
```

Return JSON:

```json
{
  "total_entries": 50,
  "low": 20,
  "medium": 18,
  "high": 12
}
```

Also provide monthly/weekly statistics where possible.

The frontend Chart.js graphs should use this real data instead of permanently hardcoded sample data.

---

# 26. PROFILE BACKEND

Create:

```text
/profile
```

Display:

```text
Name
Email
Account Created
Total Food Entries
Total Predictions
Waste Reduction
```

Allow the user to update basic profile information.

---

# 27. ADMIN BACKEND

Create admin-only routes:

```text
/admin
/admin/users
/admin/foods
/admin/predictions
/admin/reports
```

Only users with:

```text
role == "admin"
```

can access these pages.

If a normal user attempts to access an admin route:

```text
403 Forbidden
```

or redirect to dashboard.

---

# 28. ADMIN STATISTICS

Admin dashboard should show:

```text
Total Users
Total Food Entries
Total Predictions
High Risk Predictions
Medium Risk Predictions
Low Risk Predictions
```

Retrieve all information from the database.

---

# 29. ADMIN USER MANAGEMENT

Allow admin to:

- View users
- Search users
- View user details
- View account creation date
- View user food entries
- Change appropriate user status if implemented

Do not allow accidental deletion without confirmation.

---

# 30. ADMIN FOOD MANAGEMENT

Display:

```text
User
Food
Category
Quantity
Expiry
Prediction
Created Date
```

Provide search/filter options.

---

# 31. API ENDPOINTS

Create clean backend endpoints.

Required routes:

```text
GET  /
GET  /login
POST /login
GET  /signup
POST /signup
GET  /logout

GET  /dashboard

GET  /food-entry
POST /food-entry

POST /predict

GET  /prediction/<id>

GET  /recommendations/<food_id>

GET  /reports
GET  /api/reports

GET  /profile
POST /profile

GET  /admin
GET  /admin/users
GET  /admin/foods
GET  /admin/predictions
GET  /admin/reports
```

---

# 32. BLUEPRINT ARCHITECTURE

Do not put the entire application inside one huge `app.py`.

Use Flask Blueprints:

```text
auth_routes.py
food_routes.py
dashboard_routes.py
report_routes.py
admin_routes.py
```

Register all blueprints inside `app.py`.

Keep the application modular.

---

# 33. DATABASE INITIALIZATION

Provide a simple way to create the database.

For example:

```bash
python
```

Then:

```python
from app import app, db

with app.app_context():
    db.create_all()
```

If appropriate, create an initialization script.

---

# 34. CREATE ADMIN USER

Provide a secure initialization method for creating an admin account.

Do not hardcode a publicly known admin password.

Use environment variables or a setup command.

Example:

```text
ADMIN_EMAIL
ADMIN_PASSWORD
```

The password must be hashed before storing.

---

# 35. ERROR HANDLING

Implement:

```text
404
500
403
```

Create user-friendly pages.

Log useful backend errors without exposing sensitive information.

---

# 36. SECURITY

Implement:

- Password hashing
- Login sessions
- Authorization
- Secure filenames
- File type validation
- Upload size limit
- CSRF protection if forms are implemented accordingly
- Environment variables
- No hardcoded API keys
- SQLAlchemy ORM instead of raw SQL where possible
- Input validation
- Proper access control

Never expose:

```text
password_hash
SECRET_KEY
database credentials
API keys
```

to the frontend.

---

# 37. FRONTEND CONNECTION

Connect the existing frontend pages to Flask.

Update forms such as:

```html
<form method="POST" action="/login">
```

Signup:

```html
<form method="POST" action="/signup">
```

Food entry:

```html
<form method="POST" action="/food-entry" enctype="multipart/form-data">
```

Prediction:

```html
<form method="POST" action="/predict">
```

Make sure all routes match the Flask backend.

---

# 38. FLASH MESSAGES

Use Flask flash messages.

Examples:

```text
Account created successfully.
Invalid email or password.
Food entry saved successfully.
Prediction generated successfully.
Profile updated successfully.
You are not authorized to access this page.
```

Display them professionally in the frontend.

---

# 39. DATABASE RELATIONSHIPS

Implement:

```text
User
 │
 ├── FoodEntry
 │      │
 │      ├── Prediction
 │      │
 │      └── Recommendation
 │
 └── Reports
```

Use SQLAlchemy relationships and foreign keys.

---

# 40. COMPLETE APPLICATION FLOW

The finished backend must support this:

```text
HOME
 ↓
SIGNUP
 ↓
DATABASE USER CREATED
 ↓
LOGIN
 ↓
SESSION CREATED
 ↓
DASHBOARD
 ↓
FOOD ENTRY
 ↓
DATABASE
 ↓
ML MODEL
 ↓
PREDICTION
 ↓
DATABASE
 ↓
RECOMMENDATIONS
 ↓
DATABASE
 ↓
DASHBOARD
 ↓
REPORTS
```

Admin:

```text
ADMIN LOGIN
 ↓
ADMIN DASHBOARD
 ↓
USERS
 ↓
FOOD ENTRIES
 ↓
PREDICTIONS
 ↓
REPORTS
```

---

# 41. TESTING

After implementation, test every route.

Test:

### Authentication

```text
Signup
Duplicate email
Login
Wrong password
Logout
Protected pages
```

### Food Entry

```text
Valid data
Invalid data
Missing fields
Image upload
Invalid image
```

### ML

```text
LOW
MEDIUM
HIGH
```

### Database

```text
User creation
Food entry
Prediction
Recommendation
```

### Authorization

```text
Normal user → Admin page = BLOCKED
Admin → Admin page = ALLOWED
```

### Reports

Ensure statistics are calculated from actual database records.

---

# 42. DO NOT USE FAKE DATA IN FINAL BACKEND

Frontend sample data can exist temporarily.

But after backend integration:

- Dashboard data must come from database.
- Predictions must come from ML model.
- Recommendations must come from backend logic.
- Reports must come from database.
- Admin statistics must come from database.

Do not use random prediction values.

---

# 43. RUNNING THE PROJECT

The final project must run using:

```bash
venv\Scripts\activate
python app.py
```

Then:

```text
http://127.0.0.1:5000
```

Ensure there are no import errors.

---

# 44. FINAL BACKEND CHECK

Before finishing, verify:

[ ] Flask starts successfully

[ ] Homepage loads

[ ] Signup works

[ ] User is stored in database

[ ] Password is hashed

[ ] Login works

[ ] Logout works

[ ] Dashboard works

[ ] Food entry works

[ ] Image upload works

[ ] ML model loads

[ ] Prediction works

[ ] Prediction is saved

[ ] Recommendations are generated

[ ] Recommendations are saved

[ ] Reports work

[ ] Charts receive real data

[ ] Profile works

[ ] Admin authentication works

[ ] Admin dashboard works

[ ] Unauthorized users are blocked

[ ] Error pages work

[ ] Database relationships work

[ ] No hardcoded passwords

[ ] No exposed secrets

[ ] No broken navigation

[ ] No unnecessary duplicate code

---

# FINAL INSTRUCTION

Build the complete Flask backend from scratch and integrate it with my existing **AI FOOD WASTE REDUCTION SYSTEM** frontend.

Do not stop at creating `app.py`.

Implement:

**Flask Application → Configuration → Database → Models → Authentication → Sessions → Food Entry → Image Upload → ML Model → Prediction → Recommendations → Dashboard → Reports → Admin → Security → Error Handling → Testing**

Make the backend clean, modular, secure, scalable, and ready for the next stage: **production deployment with PostgreSQL and a cloud hosting service.**

At the end, explain:

1. What files you created.
2. What each file does.
3. How the frontend connects to Flask.
4. How the database works.
5. How the ML model works.
6. How to start the application.
7. How to test each feature.
8. What remains to be done for deployment.
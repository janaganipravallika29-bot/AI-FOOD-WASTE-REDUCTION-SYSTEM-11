# MASTER PROMPT — DATABASE DEVELOPMENT

You are an expert database engineer and Flask-SQLAlchemy developer.

I am developing a project called:

**AI FOOD WASTE REDUCTION SYSTEM**

The frontend and Flask backend are already being developed.

Now create and integrate the complete database system with the Flask backend.

The database must store users, food entries, AI predictions, recommendations, reports/statistics, and admin-related information.

Use:

**SQLite + Flask-SQLAlchemy for development**

and make the architecture **PostgreSQL-ready for deployment**.

Do not use localStorage as the permanent database.

---

# 1. DATABASE TECHNOLOGY

Use:

- SQLite
- SQLAlchemy
- Flask-SQLAlchemy
- Python
- PostgreSQL-compatible database design

Development database:

```text
database/app.db
```

The Flask backend must communicate with the database through SQLAlchemy ORM.

Do not use raw SQL unnecessarily.

---

# 2. DATABASE FOLDER STRUCTURE

Create:

```text
AI_Food_Waste_Reduction_System/
│
├── database/
│   ├── app.db
│   └── init_db.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── food_entry.py
│   ├── prediction.py
│   ├── recommendation.py
│   └── activity.py
│
├── app.py
├── config.py
├── requirements.txt
└── .env
```

If model files already exist, improve them instead of unnecessarily creating duplicates.

---

# 3. DATABASE DESIGN

Create the following main tables:

```text
users
food_entries
predictions
recommendations
activities
```

The main relationship should be:

```text
USER
  │
  ├───────────────┐
  ↓               ↓
FOOD ENTRIES    ACTIVITIES
  │
  ├──────────────┐
  ↓              ↓
PREDICTIONS   RECOMMENDATIONS
```

---

# 4. USERS TABLE

Create a `users` table.

Fields:

```text
id
name
email
password_hash
role
created_at
updated_at
```

### Requirements

`id`:

- Integer
- Primary key
- Auto increment

`name`:

- String
- Required

`email`:

- String
- Required
- Unique
- Indexed

`password_hash`:

- String
- Required
- Never store plain-text passwords

`role`:

- String
- Default: `user`

Allowed roles:

```text
user
admin
```

`created_at`:

- DateTime
- Automatically created

`updated_at`:

- DateTime
- Automatically updated when profile changes

---

# 5. USERS TABLE EXAMPLE

Example records:

```text
1 | Pravalika | user@example.com | hashed_password | user
2 | Admin | admin@example.com | hashed_password | admin
```

Never display `password_hash` in the frontend.

---

# 6. FOOD ENTRIES TABLE

Create:

```text
food_entries
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
updated_at
```

### Field requirements

`id`:

- Primary key

`user_id`:

- Foreign key → users.id
- Required
- Indexed

`food_name`:

- Required

`category`:

Examples:

```text
Vegetables
Fruits
Dairy
Grains
Meat
Bakery
Beverages
Other
```

`quantity`:

- Numeric
- Must be greater than 0

`unit`:

Examples:

```text
kg
g
L
ml
pieces
packets
```

`purchase_date`:

- Date

`expiry_date`:

- Date

`storage_type`:

Examples:

```text
Refrigerator
Freezer
Room Temperature
Pantry
Other
```

`temperature`:

- Float
- Optional

`previous_waste`:

- Float
- Default 0

`image_filename`:

- String
- Optional

`created_at`:

- DateTime

`updated_at`:

- DateTime

---

# 7. FOOD ENTRY RELATIONSHIP

Implement:

```text
User 1 ──────── * FoodEntry
```

One user can create many food entries.

When a user is deleted, decide carefully how related food records should be handled. Use appropriate SQLAlchemy cascade behavior.

---

# 8. PREDICTIONS TABLE

Create:

```text
predictions
```

Fields:

```text
id
food_entry_id
waste_level
confidence
model_version
created_at
```

`waste_level` must support:

```text
LOW
MEDIUM
HIGH
```

`confidence`:

- Float
- Store prediction confidence percentage or probability consistently.

Example:

```text
87.5
```

`model_version`:

Example:

```text
1.0
```

This allows future ML models to be tracked.

---

# 9. PREDICTION RELATIONSHIP

Implement:

```text
FoodEntry 1 ──────── * Prediction
```

Although the initial system may create one prediction per food analysis, keep the design flexible enough to support multiple prediction records over time.

---

# 10. RECOMMENDATIONS TABLE

Create:

```text
recommendations
```

Fields:

```text
id
food_entry_id
recommendation_text
recommendation_type
priority
created_at
```

`recommendation_type` examples:

```text
Consumption
Storage
Purchase Planning
Meal Planning
Donation
```

`priority`:

```text
LOW
MEDIUM
HIGH
```

---

# 11. RECOMMENDATION RELATIONSHIP

Implement:

```text
FoodEntry 1 ──────── * Recommendation
```

One food entry can have multiple recommendations.

Example:

```text
Tomatoes
 ├── Consume soon
 ├── Improve storage
 └── Avoid purchasing excess quantity
```

---

# 12. ACTIVITIES TABLE

Create an activity/history table:

```text
activities
```

Fields:

```text
id
user_id
activity_type
description
created_at
```

Activity types may include:

```text
LOGIN
LOGOUT
FOOD_ADDED
PREDICTION_CREATED
RECOMMENDATION_CREATED
REPORT_GENERATED
PROFILE_UPDATED
```

This will help create an activity history in the dashboard.

---

# 13. COMPLETE DATABASE RELATIONSHIP

Implement this structure:

```text
                         ┌─────────────────┐
                         │      USERS      │
                         ├─────────────────┤
                         │ id              │
                         │ name            │
                         │ email           │
                         │ password_hash   │
                         │ role            │
                         │ created_at      │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ↓                           ↓
          ┌─────────────────┐          ┌─────────────────┐
          │  FOOD_ENTRIES   │          │   ACTIVITIES    │
          ├─────────────────┤          ├─────────────────┤
          │ id              │          │ id              │
          │ user_id         │          │ user_id         │
          │ food_name       │          │ activity_type   │
          │ category        │          │ description     │
          │ quantity        │          │ created_at      │
          │ expiry_date     │          └─────────────────┘
          │ storage_type    │
          │ temperature     │
          └────────┬────────┘
                   │
             ┌─────┴─────┐
             ↓           ↓
   ┌────────────────┐ ┌────────────────────┐
   │  PREDICTIONS   │ │  RECOMMENDATIONS   │
   ├────────────────┤ ├────────────────────┤
   │ id             │ │ id                 │
   │ food_entry_id  │ │ food_entry_id     │
   │ waste_level    │ │ recommendation     │
   │ confidence     │ │ type               │
   │ model_version  │ │ priority            │
   │ created_at     │ │ created_at          │
   └────────────────┘ └────────────────────┘
```

---

# 14. SQLALCHEMY MODELS

Use Flask-SQLAlchemy models.

Example architecture:

```python
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

Follow the same clean approach for all models.

---

# 15. DATABASE INITIALIZATION

Create:

```text
database/init_db.py
```

It must:

1. Create database directory if it does not exist.
2. Create all database tables.
3. Optionally create an initial admin account using environment variables.
4. Print a success message.

Example:

```text
Database initialized successfully.
Tables created:
- users
- food_entries
- predictions
- recommendations
- activities
```

---

# 16. DATABASE CONFIGURATION

In `config.py`, configure:

```text
SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS
```

For development:

```text
sqlite:///database/app.db
```

Use environment variables so PostgreSQL can later be configured without changing application code.

---

# 17. DATABASE CONNECTION

The Flask application must initialize:

```text
Flask
 ↓
SQLAlchemy
 ↓
SQLite
 ↓
app.db
```

Do not create a new database connection for every request manually.

Use Flask-SQLAlchemy correctly.

---

# 18. MIGRATION-READY STRUCTURE

Make the project ready for Flask-Migrate.

Install:

```bash
pip install flask-migrate
```

Configure the application so future schema changes can use migrations.

Expected commands:

```bash
flask db init
flask db migrate -m "Initial database"
flask db upgrade
```

If migrations are not required for the initial version, still keep the architecture compatible with them.

---

# 19. DATABASE VALIDATION

Implement validation before saving data.

### User

Check:

```text
Name is not empty
Email is valid
Email is unique
Password meets minimum requirements
```

### Food

Check:

```text
Food name exists
Quantity > 0
Purchase date is valid
Expiry date >= purchase date
```

### Prediction

Check:

```text
Waste level is LOW/MEDIUM/HIGH
Confidence is between 0 and 100
```

---

# 20. DATABASE INDEXES

Add indexes where useful:

```text
users.email
food_entries.user_id
food_entries.expiry_date
predictions.food_entry_id
activities.user_id
```

This will improve query performance.

---

# 21. DATABASE SECURITY

Follow these rules:

- Never store plain-text passwords.
- Use password hashing.
- Never expose database credentials.
- Never expose `.env`.
- Add `.env` to `.gitignore`.
- Use SQLAlchemy ORM.
- Validate all user input.
- Do not construct SQL queries using unsafe string concatenation.

---

# 22. DASHBOARD DATABASE QUERIES

The dashboard must retrieve actual database information.

Calculate:

```text
Total Food Entries
```

from `food_entries`.

Calculate:

```text
Low Risk
Medium Risk
High Risk
```

from `predictions`.

Calculate:

```text
Recent Food Entries
```

from `food_entries`.

Calculate:

```text
Recent Activities
```

from `activities`.

Do not hardcode these values.

---

# 23. REPORT DATABASE QUERIES

Create queries for:

### Daily

```text
Food entries per day
Predictions per day
High-risk foods per day
```

### Weekly

```text
Food entries per week
Waste risk distribution
```

### Monthly

```text
Food entries per month
Low/Medium/High distribution
Food categories
```

These results will later be sent to Chart.js.

---

# 24. FOOD CATEGORY STATISTICS

Create database queries to calculate:

```text
Vegetables
Fruits
Dairy
Grains
Meat
Bakery
Beverages
Other
```

and their:

```text
Total Entries
Total Quantity
High Risk Count
```

---

# 25. EXPIRY QUERIES

Create queries to identify:

### Expiring Soon

Food where:

```text
expiry_date <= today + 3 days
```

### Expired

Food where:

```text
expiry_date < today
```

### Safe/Remaining

Food where:

```text
expiry_date > today
```

These results should appear on the dashboard.

---

# 26. HIGH-RISK FOOD QUERY

Create a query that retrieves the user's high-risk foods.

Example:

```text
SELECT foods whose latest prediction is HIGH
```

Display them on the dashboard as:

```text
⚠ High Risk Food

Tomatoes
2 kg
Expires in 2 days

Milk
1 L
Expires tomorrow
```

---

# 27. RECENT ACTIVITY

Show the user's latest activities:

```text
Food added
Prediction generated
Recommendation created
Report generated
Profile updated
```

Sort by newest first.

---

# 28. ADMIN DATABASE QUERIES

Admin dashboard must retrieve:

```text
Total Users
Total Food Entries
Total Predictions
Total Recommendations
High Risk Predictions
Medium Risk Predictions
Low Risk Predictions
```

Also provide:

```text
Users per month
Food entries per month
Prediction distribution
Food category distribution
```

---

# 29. DELETE OPERATIONS

Implement safe deletion.

If a user or food entry is deleted:

- Handle related predictions.
- Handle related recommendations.
- Handle activities appropriately.

Use SQLAlchemy cascade rules where appropriate.

Do not leave broken foreign-key records.

---

# 30. DATABASE TEST DATA

Create optional seed data for development.

Example foods:

```text
Tomatoes
Milk
Rice
Apples
Bread
Potatoes
Chicken
Vegetables
```

Create realistic:

```text
quantities
expiry dates
storage types
predictions
recommendations
```

Make it clear that this is only development/demo data.

---

# 31. DATABASE TESTING

Test:

### Users

```text
Create user
Read user
Update user
Duplicate email
Delete user
```

### Food

```text
Create food
Read food
Update food
Delete food
```

### Predictions

```text
Create prediction
Retrieve prediction
Link to food entry
```

### Recommendations

```text
Create recommendation
Retrieve recommendations
Link to food entry
```

### Relationships

Verify:

```text
User → FoodEntry
FoodEntry → Prediction
FoodEntry → Recommendation
User → Activity
```

---

# 32. SAMPLE DATABASE FLOW

When a user adds:

```text
Food:
Tomatoes

Quantity:
2 kg

Expiry:
2 days

Storage:
Room Temperature
```

save it to:

```text
food_entries
```

Then ML predicts:

```text
HIGH
87%
```

save it to:

```text
predictions
```

Then generate:

```text
Consume soon
Improve storage
Avoid excess purchase
```

save them to:

```text
recommendations
```

Create an activity:

```text
Prediction created for Tomatoes
```

save it to:

```text
activities
```

---

# 33. DATABASE → FLASK → FRONTEND FLOW

Implement:

```text
HTML Form
     ↓
Flask Route
     ↓
Validation
     ↓
SQLAlchemy Model
     ↓
SQLite Database
     ↓
Query
     ↓
Flask
     ↓
Jinja Template
     ↓
Frontend
```

For charts:

```text
Database
   ↓
Flask API
   ↓
JSON
   ↓
Chart.js
   ↓
Dashboard
```

---

# 34. POSTGRESQL READY

Do not write SQLite-specific application logic unnecessarily.

The application should later support:

```text
PostgreSQL
```

by changing:

```text
DATABASE_URL
```

in `.env`.

Do not require major application-code changes when switching databases.

---

# 35. ENVIRONMENT VARIABLES

Create `.env.example`:

```text
SECRET_KEY=change_this
DATABASE_URL=sqlite:///database/app.db
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=change_this
```

Do not commit the real `.env`.

Add to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
database/*.db
```

---

# 36. FINAL DATABASE FILES

The final implementation should contain:

```text
database/
├── app.db
└── init_db.py

models/
├── __init__.py
├── user.py
├── food_entry.py
├── prediction.py
├── recommendation.py
└── activity.py
```

---

# 37. FINAL DATABASE CHECKLIST

Before finishing, verify:

[ ] Database is created successfully

[ ] `app.db` exists

[ ] Users table exists

[ ] Food entries table exists

[ ] Predictions table exists

[ ] Recommendations table exists

[ ] Activities table exists

[ ] Foreign keys work

[ ] Relationships work

[ ] Email uniqueness works

[ ] Password hashes are stored

[ ] Food validation works

[ ] Expiry queries work

[ ] High-risk queries work

[ ] Dashboard statistics work

[ ] Reports work

[ ] Admin statistics work

[ ] Delete cascades work correctly

[ ] Database is Flask-integrated

[ ] PostgreSQL-ready configuration exists

[ ] `.env` is protected

---

# FINAL INSTRUCTION

Build the complete database layer for the:

**AI FOOD WASTE REDUCTION SYSTEM**

Integrate:

**Flask → SQLAlchemy → Database → User Authentication → Food Entries → ML Predictions → Recommendations → Activities → Dashboard → Reports → Admin**

Do not create a disconnected database.

Every database table must be connected to the Flask backend and used by the corresponding frontend feature.

At the end, provide:

1. Complete database structure.
2. All SQLAlchemy models.
3. Relationships between tables.
4. Database initialization instructions.
5. Migration instructions.
6. Sample/seed data instructions.
7. Database testing instructions.
8. How Flask communicates with the database.
9. How to view the database during development.
10. How to switch from SQLite to PostgreSQL during deployment.

The final database must be clean, normalized, secure, maintainable, and ready for the next stages:
**Login/Signup → Food Entry → ML Prediction → Recommendations → Dashboard → Reports → Admin → Testing → Deployment.**
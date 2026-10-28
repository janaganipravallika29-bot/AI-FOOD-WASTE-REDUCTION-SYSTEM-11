# MASTER PROMPT — COMPLETE DEPLOYMENT MODULE

You are an expert DevOps engineer, Flask developer, Python developer, database administrator, security engineer, ML deployment engineer, and cloud deployment specialist.

My project title is:

**AI FOOD WASTE REDUCTION SYSTEM**

The application has already been developed with:

- Professional Frontend
- Flask Backend
- Database
- Login/Signup
- Authentication
- Food Entry
- ML Model
- Prediction
- Recommendations
- User Dashboard
- Reports
- Admin Panel
- Testing

Now prepare the complete application for:

# PRODUCTION DEPLOYMENT

Do not rebuild the application unnecessarily.

First inspect the complete existing project and identify:

- Flask entry point
- Database type
- Database configuration
- ML model files
- Uploaded files
- Static files
- Environment variables
- Authentication
- Admin system
- Report exports
- Dependencies
- Existing tests

Then configure the project for secure production deployment.

---

# 1. DEPLOYMENT ARCHITECTURE

Use this production architecture:

```text
USER
  ↓
DOMAIN
  ↓
HTTPS
  ↓
PRODUCTION SERVER
  ↓
GUNICORN
  ↓
FLASK APPLICATION
  ↓
DATABASE
  ↓
ML MODEL
  ↓
REPORTS / FILE STORAGE
```

Do NOT use:

```text
flask run
```

as the production web server.

Use a production WSGI server such as:

```text
Gunicorn
```

For Windows development/testing, keep the existing local development command available.

---

# 2. PRODUCTION ENVIRONMENT

Create a production configuration.

Use environment variables for:

```text
SECRET_KEY
DATABASE_URL
FLASK_ENV
FLASK_DEBUG
MODEL_PATH
UPLOAD_FOLDER
MAX_CONTENT_LENGTH
```

If the project uses other secrets or configuration values, include them appropriately.

Never hardcode secrets.

---

# 3. .ENV FILE

Create:

```text
.env.example
```

Example structure:

```text
SECRET_KEY=replace_with_secure_random_value
DATABASE_URL=replace_with_production_database_url
FLASK_ENV=production
FLASK_DEBUG=False
MODEL_PATH=models/model.pkl
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=5242880
```

Do NOT place real secrets in `.env.example`.

If `.env` is used locally, ensure it is excluded from Git.

---

# 4. GITIGNORE

Create/update:

```text
.gitignore
```

Include:

```text
.env
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
.coverage
htmlcov/
instance/
*.sqlite
*.db
static/uploads/*
exports/*
```

Keep required placeholder files such as:

```text
static/uploads/.gitkeep
exports/.gitkeep
```

if necessary.

Do not accidentally ignore source code or ML model files that are required for deployment.

---

# 5. REQUIREMENTS.TXT

Review:

```text
requirements.txt
```

Ensure every production dependency is listed.

Typical dependencies may include:

```text
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
python-dotenv
gunicorn
pandas
numpy
scikit-learn
joblib
Pillow
reportlab
```

Only include packages actually used by the project.

Remove unnecessary dependencies.

Pin compatible versions where appropriate.

---

# 6. PRODUCTION FLASK CONFIGURATION

Create/update:

```text
config.py
```

Use separate configurations:

```text
DevelopmentConfig
TestingConfig
ProductionConfig
```

Production must use:

```text
DEBUG = False
TESTING = False
```

Do not expose debugging information to users.

---

# 7. SECRET KEY

Generate a strong production secret key.

Never use:

```text
secret
123456
flask-secret
mysecretkey
```

Never commit the real secret key to Git.

Load it from:

```text
SECRET_KEY
```

environment variable.

---

# 8. PRODUCTION APP ENTRY POINT

Ensure the project has a production WSGI entry point.

For example:

```text
wsgi.py
```

Conceptually:

```python
from app import app

application = app
```

Adapt this to the actual Flask application factory or structure.

The deployment platform must be able to start the application with Gunicorn.

---

# 9. GUNICORN

Add Gunicorn to:

```text
requirements.txt
```

Production startup command should follow the actual project structure.

Example:

```bash
gunicorn wsgi:application
```

If the application exposes a different WSGI object, use the correct one.

Do NOT blindly use this command if it does not match the actual application structure.

---

# 10. DATABASE

Identify the current database.

If currently using:

```text
SQLite
```

determine whether it is suitable for the intended production environment.

For a real multi-user production deployment, prefer a managed relational database such as:

```text
PostgreSQL
```

if supported by the deployment platform.

Do not lose existing schema or data.

---

# 11. DATABASE URL

Load production database configuration from:

```text
DATABASE_URL
```

Do not hardcode:

```text
postgres://...
```

or database passwords inside Python files.

Support the database URL format required by the selected deployment platform.

---

# 12. DATABASE MIGRATIONS

If Flask-Migrate/Alembic is not already configured, add it where appropriate.

Create migrations for:

```text
User
FoodEntry
Prediction
Recommendation
WasteRecord
ActivityLog
```

and all existing models.

Do NOT recreate the database destructively during deployment.

---

# 13. PRODUCTION DATABASE INITIALIZATION

Provide a safe deployment process:

```text
Install dependencies
      ↓
Configure environment variables
      ↓
Connect database
      ↓
Run migrations
      ↓
Create required initial data
      ↓
Start application
```

Never automatically delete production tables.

---

# 14. ADMIN ACCOUNT

Do NOT create a hardcoded admin account in application startup.

Provide a secure command such as:

```bash
python create_admin.py
```

or an equivalent management command.

The command must securely request:

```text
Admin Name
Admin Email
Admin Password
```

Hash the password before storing it.

Never print the password.

---

# 15. ML MODEL DEPLOYMENT

Identify the exact ML model files used by the application.

Examples:

```text
models/
├── model.pkl
├── scaler.pkl
├── encoder.pkl
```

or the actual project structure.

Verify that all required model artifacts are available in production.

Do not retrain the model during application startup.

---

# 16. ML MODEL PATH

Use an environment variable:

```text
MODEL_PATH
```

or a safe project-relative configuration.

The application must fail gracefully if the model file is missing.

Display:

```text
AI prediction service temporarily unavailable.
```

rather than exposing a Python traceback.

---

# 17. MODEL LOADING

Load the model efficiently.

Do not repeatedly load the model for every prediction request unless the existing architecture specifically requires it.

Prefer:

```text
Application startup
      ↓
Load model
      ↓
Keep model available
      ↓
Prediction requests
```

Verify memory requirements before deployment.

---

# 18. FILE UPLOADS

The Food Entry module may allow image uploads.

Configure:

```text
UPLOAD_FOLDER
MAX_CONTENT_LENGTH
```

Use secure filenames.

Limit allowed file types.

Reject dangerous files.

Do not allow arbitrary filesystem paths.

---

# 19. PRODUCTION FILE STORAGE

Do NOT assume local disk is permanent on every cloud platform.

Determine whether the chosen deployment platform provides persistent storage.

If persistent storage is unavailable, use appropriate object storage for:

```text
Food images
Generated reports
Uploaded files
```

Only implement external storage if required by the chosen deployment platform.

---

# 20. STATIC FILES

Ensure:

```text
static/
templates/
```

are correctly served in production.

If the deployment platform requires a reverse proxy/static asset strategy, configure it appropriately.

Verify:

```text
CSS
JavaScript
Images
Icons
Fonts
```

load correctly.

---

# 21. DATABASE SECURITY

Production database must:

```text
Use strong credentials
Use encrypted connections where supported
Restrict public access where possible
Use least-privilege credentials
```

Never expose database credentials to frontend JavaScript.

---

# 22. HTTPS

Production deployment must use:

```text
HTTPS
```

Do not use plain HTTP for authenticated production traffic.

Verify:

```text
Login
Signup
Food Entry
Admin
Reports
```

all work correctly over HTTPS.

---

# 23. COOKIE SECURITY

Configure secure session cookies appropriately.

Production should use settings such as:

```text
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

Adjust `SameSite` only when the application architecture requires another value.

---

# 24. CSRF PROTECTION

If forms use CSRF protection, ensure it remains enabled in production.

Test:

```text
Login
Signup
Food Entry
Admin actions
Settings
```

Do not disable CSRF merely to make forms work.

---

# 25. CORS

Do not enable:

```text
CORS(*)
```

unless actually required.

If frontend and backend are served from different origins, configure only the required production origin.

---

# 26. DEBUG MODE

Production must have:

```text
FLASK_DEBUG=False
```

Never expose Flask debugger publicly.

Verify intentionally that visiting an error page does not reveal:

```text
Python traceback
Source code
Environment variables
File paths
Database credentials
```

---

# 27. ERROR HANDLERS

Create professional production error pages:

```text
templates/errors/
├── 400.html
├── 403.html
├── 404.html
└── 500.html
```

Display friendly messages.

Example:

```text
Something went wrong.

Please try again later.
```

Do not expose technical details.

---

# 28. HEALTH CHECK

Create:

```text
/health
```

The endpoint should verify application availability.

Example response:

```json
{
    "status": "healthy"
}
```

Do not expose sensitive system information.

If database health is included, expose only a minimal status.

---

# 29. ADMIN HEALTH CHECK

Keep detailed system checks restricted to admins:

```text
/admin/health
```

Check:

```text
Application
Database
ML Model
```

Do not expose internal details publicly.

---

# 30. LOGGING

Configure production logging.

Log:

```text
Application errors
Warnings
Authentication events where appropriate
Database failures
ML prediction failures
Admin security events
```

Do NOT log:

```text
Passwords
Secret keys
API keys
Session tokens
Full sensitive user data
```

---

# 31. LOG ROTATION

Prevent log files from growing indefinitely.

Use the deployment platform's logging system where possible.

If local file logging is required, configure rotation.

---

# 32. DATABASE BACKUP

Create a production backup strategy.

For managed PostgreSQL:

```text
Use platform/database backups
```

For other databases:

```text
Scheduled backups
```

Verify that backups can actually be restored.

Do not consider a backup successful merely because a backup command ran.

---

# 33. BACKUP POLICY

Document:

```text
Backup frequency
Retention period
Restore procedure
Database owner
```

Do not store backups in a publicly accessible directory.

---

# 34. DOMAIN

Prepare the application for a custom domain.

Example:

```text
www.yourdomain.com
```

Use the actual domain after the user chooses/purchases one.

Do not invent a domain that the user does not own.

Configure:

```text
DNS
HTTPS
Application URL
Allowed origins
```

as required.

---

# 35. DEPLOYMENT PLATFORM

Choose a platform appropriate for a Flask + ML + database application.

Possible options include:

```text
Render
Railway
PythonAnywhere
AWS
Google Cloud
Azure
DigitalOcean
```

Prefer a simple managed deployment platform for the first production deployment unless the project has specific infrastructure requirements.

Do not deploy simultaneously to multiple platforms.

---

# 36. DEPLOYMENT DOCUMENTATION

Create:

```text
DEPLOYMENT.md
```

Include:

```text
Prerequisites
Project setup
Environment variables
Database setup
Migration commands
Admin creation
Local production test
Deployment steps
Domain setup
HTTPS setup
Troubleshooting
Rollback
Backup
```

---

# 37. LOCAL PRODUCTION TEST

Before uploading to the cloud:

Run the application in production configuration locally.

Conceptually:

```text
FLASK_DEBUG=False
```

Start with Gunicorn where supported by the local environment.

Verify:

```text
Home
Signup
Login
Dashboard
Food Entry
ML Prediction
Recommendations
Reports
Admin
Logout
```

---

# 38. RUN TEST SUITE BEFORE DEPLOYMENT

Run:

```bash
pytest
```

Do not deploy if critical tests fail.

Expected:

```text
All critical tests PASS
```

If tests fail:

```text
Fix
↓
Retest
↓
Deploy
```

---

# 39. SECURITY SCAN

Before deployment check:

```text
No .env committed
No passwords in source
No API keys in source
No debug mode
No exposed admin bypass
No unsafe SQL
No unrestricted file uploads
No production database credentials in Git
```

Search the repository for:

```text
password
secret
api_key
token
DATABASE_URL
```

Manually review every match before deployment.

Do not simply delete legitimate configuration references.

---

# 40. GIT REPOSITORY

Prepare the repository:

```text
git init
git add .
git commit -m "Prepare AI Food Waste Reduction System for production"
```

Only if Git is not already configured.

Do not commit:

```text
.env
production credentials
private keys
database dumps
large temporary files
test secrets
```

---

# 41. GITHUB

If using GitHub:

Create a repository:

```text
AI-Food-Waste-Reduction-System
```

Push only safe source code.

Use:

```text
README.md
```

with:

```text
Project Description
Features
Technology Stack
Installation
Usage
Testing
Deployment
Screenshots
```

Do not publish secret information.

---

# 42. README STRUCTURE

Create/update:

```text
README.md
```

Include:

```text
# AI Food Waste Reduction System

## Overview

## Features

## Technology Stack

## Project Architecture

## Installation

## Environment Variables

## Database

## ML Model

## Running Locally

## Testing

## Deployment

## Admin Panel

## Security

## Future Enhancements
```

---

# 43. DEPLOYMENT CONFIGURATION

Create the configuration required by the selected platform.

Examples:

```text
Procfile
render.yaml
railway configuration
Dockerfile
```

Only create files required by the actual selected deployment method.

Do not create unnecessary deployment configurations.

---

# 44. DOCKER OPTION

If Docker is selected, create:

```text
Dockerfile
.dockerignore
```

Dockerfile must:

```text
Use a suitable Python base image
Install dependencies
Copy application
Set production environment
Expose application port
Run Gunicorn
```

Do not use Flask development server in Docker production.

---

# 45. PORT CONFIGURATION

The application must use the platform-provided port.

Conceptually:

```python
port = int(os.environ.get("PORT", 5000))
```

Do not hardcode only port 5000 for cloud deployment.

Gunicorn should bind appropriately for the platform.

---

# 46. ENVIRONMENT VARIABLES

Document required production variables.

Example:

```text
SECRET_KEY
DATABASE_URL
FLASK_DEBUG
FLASK_ENV
MODEL_PATH
UPLOAD_FOLDER
MAX_CONTENT_LENGTH
```

Add only variables actually used by the application.

---

# 47. API KEYS

If the project uses an external AI service such as a generative AI API:

Store the key only in the deployment platform's secret/environment settings.

Never put it in:

```text
HTML
JavaScript
GitHub
README
Database
```

Frontend code must never expose private API keys.

---

# 48. CORS AND FRONTEND URL

If frontend and backend are separate:

Configure:

```text
FRONTEND_URL
```

or equivalent.

Allow only the production frontend origin.

If Flask serves the frontend itself, avoid unnecessary CORS configuration.

---

# 49. DEPLOYMENT PROCESS

Use this sequence:

```text
LOCAL PROJECT
      ↓
RUN TESTS
      ↓
FIX BUGS
      ↓
SECURITY CHECK
      ↓
GIT COMMIT
      ↓
CREATE PRODUCTION DATABASE
      ↓
SET ENVIRONMENT VARIABLES
      ↓
DEPLOY APPLICATION
      ↓
RUN DATABASE MIGRATIONS
      ↓
CREATE ADMIN
      ↓
START GUNICORN
      ↓
OPEN HTTPS URL
      ↓
SMOKE TEST
      ↓
LIVE APPLICATION
```

---

# 50. POST-DEPLOYMENT SMOKE TEST

After deployment test:

```text
Homepage
Signup
Login
Logout
Dashboard
Food Entry
Image Upload
ML Prediction
Recommendation
Reports
CSV Export
PDF Export
Admin Login
Admin Dashboard
Admin Reports
```

Verify all pages load over HTTPS.

---

# 51. PRODUCTION DATABASE TEST

Create a test user in production only if appropriate.

Verify:

```text
Signup
Food Entry
Prediction
Recommendation
Report
```

Then remove the temporary test account/data if it is not intended to remain.

Do not use real personal information for smoke testing.

---

# 52. PRODUCTION ADMIN TEST

Verify:

```text
Admin Login
Admin Dashboard
User Management
Reports
System Health
Logout
```

Then verify normal users cannot access:

```text
/admin/*
/api/admin/*
```

---

# 53. PRODUCTION PERFORMANCE

After deployment check:

```text
Homepage response
Login response
Dashboard response
Prediction response
Reports response
Admin dashboard response
```

Identify slow endpoints.

Do not optimize blindly.

---

# 54. ML PRODUCTION TEST

Run a real non-sensitive test prediction.

Verify:

```text
Food Entry
      ↓
ML Model
      ↓
Prediction
      ↓
Database
      ↓
Recommendation
      ↓
Dashboard
```

Ensure the production model loads correctly.

---

# 55. REPORT PRODUCTION TEST

Generate:

```text
CSV
PDF
Print
```

Verify:

```text
Correct data
Correct formatting
No secrets
No broken links
```

---

# 56. ROLLBACK PLAN

Create a rollback procedure.

If deployment fails:

```text
Stop problematic release
↓
Restore previous application version
↓
Verify database compatibility
↓
Check application health
```

Never blindly roll back database migrations if they may destroy data.

---

# 57. MONITORING

Configure basic monitoring:

```text
Application uptime
HTTP errors
Database errors
ML errors
CPU/memory if supported
```

Use the deployment platform's monitoring where possible.

---

# 58. ALERTING

If supported, configure alerts for:

```text
Application down
Repeated 500 errors
Database connection failure
High resource usage
```

Do not send sensitive data in alerts.

---

# 59. SECURITY HEADERS

Configure appropriate security headers, preferably using a well-maintained library or reverse proxy.

Consider:

```text
X-Content-Type-Options
Content-Security-Policy
Referrer-Policy
Strict-Transport-Security
```

Test compatibility before enforcing strict policies.

---

# 60. RATE LIMITING

Protect sensitive endpoints where appropriate:

```text
Login
Signup
Password-related endpoints
Admin APIs
Prediction APIs
```

Use a suitable Flask rate-limiting solution if needed.

Do not rate-limit normal page navigation so aggressively that legitimate users are blocked.

---

# 61. SESSION SECURITY

Verify:

```text
Session cookies secure
Logout invalidates session
Admin sessions protected
Session secrets not exposed
```

Do not store sensitive information unnecessarily in client-side sessions.

---

# 62. PRODUCTION ERROR HANDLING

Test:

```text
404
403
500
Database unavailable
ML model unavailable
Invalid upload
Invalid API request
```

All must return safe user-facing errors.

---

# 63. DEPLOYMENT FOLDER STRUCTURE

Final structure should resemble:

```text
AI_Food_Waste_Reduction_System/
│
├── app.py
├── wsgi.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── DEPLOYMENT.md
│
├── create_admin.py
│
├── models/
│   ├── user.py
│   ├── food_entry.py
│   ├── prediction.py
│   ├── recommendation.py
│   ├── waste_record.py
│   └── activity_log.py
│
├── routes/
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── food_routes.py
│   ├── prediction_routes.py
│   ├── recommendation_routes.py
│   ├── report_routes.py
│   └── admin_routes.py
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
│   │
│   ├── errors/
│   │   ├── 400.html
│   │   ├── 403.html
│   │   ├── 404.html
│   │   └── 500.html
│   │
│   └── admin/
│       ├── dashboard.html
│       ├── users.html
│       ├── food_entries.html
│       ├── predictions.html
│       ├── recommendations.html
│       ├── reports.html
│       ├── activity.html
│       └── settings.html
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
│
├── models_ml/
│   └── trained_model_files
│
├── tests/
│
└── migrations/
```

Adapt this to the actual existing project.

Do not duplicate or move files unnecessarily.

---

# 64. DEPLOYMENT PLATFORM SELECTION

Before actually deploying, inspect the project's:

```text
ML model size
Database requirements
File upload requirements
Expected traffic
Persistent storage requirements
Python version
```

Then select ONE appropriate platform.

For a student/college project, prefer a simple managed platform if it supports:

```text
Python
Flask
Gunicorn
Database
Environment Variables
Persistent/appropriate file storage
```

Document why the selected platform was chosen.

---

# 65. DOMAIN CONFIGURATION

When the user provides a domain:

Configure:

```text
DNS
A/AAAA/CNAME records as required
HTTPS
Application URL
```

Do not invent DNS values.

Use the exact DNS records supplied by the selected hosting provider.

---

# 66. FINAL DEPLOYMENT CHECKLIST

Before deployment:

[ ] Application runs locally

[ ] All tests pass

[ ] Critical bugs fixed

[ ] Security checks completed

[ ] Debug mode disabled

[ ] Secret key configured

[ ] Database configured

[ ] Database migrations ready

[ ] Admin creation process ready

[ ] ML model available

[ ] Upload security configured

[ ] Requirements complete

[ ] .gitignore configured

[ ] .env excluded from Git

[ ] README complete

[ ] Deployment documentation complete

[ ] Production WSGI configured

[ ] Gunicorn configured

[ ] Error pages configured

[ ] Health endpoint configured

[ ] HTTPS configured

[ ] Session security configured

[ ] CSRF configured where applicable

[ ] CORS restricted where applicable

[ ] Logging configured

[ ] Backup strategy configured

[ ] Monitoring configured

---

# 67. POST-DEPLOYMENT CHECKLIST

After deployment:

[ ] Website opens

[ ] HTTPS works

[ ] Home page works

[ ] Signup works

[ ] Login works

[ ] Logout works

[ ] Dashboard works

[ ] Food Entry works

[ ] Image Upload works if implemented

[ ] ML Prediction works

[ ] Recommendations work

[ ] Reports work

[ ] CSV export works

[ ] PDF export works

[ ] Admin login works

[ ] Admin dashboard works

[ ] Admin reports work

[ ] Normal user cannot access admin

[ ] Database writes work

[ ] Database reads work

[ ] Error pages work

[ ] Health check works

[ ] No secrets exposed

[ ] No debug traceback exposed

[ ] No critical browser console errors

---

# 68. FINAL OUTPUT REQUIRED FROM ANTIGRAVITY

After completing deployment preparation, provide a clear final report:

```text
PROJECT:
AI FOOD WASTE REDUCTION SYSTEM

DEPLOYMENT STATUS:
READY / NOT READY

HOSTING PLATFORM:
[actual selected platform]

DATABASE:
[actual database]

PYTHON VERSION:
[actual version]

WSGI SERVER:
Gunicorn

PRODUCTION URL:
[actual URL if deployed]

DATABASE STATUS:
Connected / Not Connected

ML MODEL:
Available / Not Available

HTTPS:
Enabled / Not Enabled

ADMIN:
Configured / Not Configured

TESTS:
[actual result]

SECURITY:
[actual result]

REMAINING ISSUES:
[list]
```

If deployment cannot be completed because an external account, domain, payment method, cloud credential, or other user action is required, do NOT pretend that deployment succeeded.

Clearly identify the exact remaining manual step.

---

# FINAL INSTRUCTION

Prepare and deploy the complete:

**AI FOOD WASTE REDUCTION SYSTEM**

from local development to production.

The final architecture must be:

```text
FRONTEND
   ↓
FLASK BACKEND
   ↓
AUTHENTICATION
   ↓
DATABASE
   ↓
ML MODEL
   ↓
PREDICTION
   ↓
RECOMMENDATIONS
   ↓
DASHBOARD
   ↓
REPORTS
   ↓
ADMIN
   ↓
TESTING
   ↓
SECURITY
   ↓
GUNICORN
   ↓
PRODUCTION SERVER
   ↓
DATABASE
   ↓
HTTPS
   ↓
LIVE WEBSITE
```

Do not claim the website is live until the deployment has actually succeeded.

Do not expose secrets.

Do not use development mode in production.

Do not delete production data.

Do not invent a deployment URL.

Do not skip testing or security verification.

The final result must be a secure, production-ready, professionally deployed **AI FOOD WASTE REDUCTION SYSTEM**.
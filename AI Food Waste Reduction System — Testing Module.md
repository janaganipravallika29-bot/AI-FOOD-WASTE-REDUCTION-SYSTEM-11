# MASTER PROMPT — COMPLETE TESTING MODULE

You are an expert QA engineer, Flask developer, Python tester, database tester, ML testing engineer, security tester, and deployment engineer.

My project title is:

**AI FOOD WASTE REDUCTION SYSTEM**

The following modules have already been implemented:

- Frontend Design
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

Now perform COMPLETE TESTING of the entire application.

Do not modify working functionality unnecessarily.

First inspect the existing project and understand the current architecture, database models, routes, templates, JavaScript, ML model, authentication, and admin system.

Then implement a complete testing system.

---

# 1. TESTING OBJECTIVE

Test the complete application flow:

```text
Frontend
   ↓
Forms
   ↓
JavaScript
   ↓
Flask Routes
   ↓
Authentication
   ↓
Database
   ↓
Food Entry
   ↓
ML Model
   ↓
Prediction
   ↓
Recommendations
   ↓
Dashboard
   ↓
Reports
   ↓
Admin
   ↓
Security
   ↓
Deployment Readiness
```

The application must work without critical errors.

---

# 2. TESTING TYPES

Perform:

```text
1. Unit Testing
2. Integration Testing
3. Functional Testing
4. Database Testing
5. API Testing
6. Authentication Testing
7. Authorization Testing
8. ML Model Testing
9. Frontend Testing
10. Form Validation Testing
11. Report Testing
12. Admin Testing
13. Security Testing
14. Error Handling Testing
15. Responsive Testing
16. Performance Testing
17. Regression Testing
```

---

# 3. CREATE TEST FOLDER

Create:

```text
tests/
```

Expected structure:

```text
tests/
├── __init__.py
├── conftest.py
├── test_auth.py
├── test_food_entry.py
├── test_prediction.py
├── test_recommendations.py
├── test_dashboard.py
├── test_reports.py
├── test_admin.py
├── test_database.py
├── test_api.py
├── test_security.py
└── test_ml_model.py
```

Do not duplicate files that already exist.

---

# 4. TESTING FRAMEWORK

Use:

```text
pytest
```

Add required testing dependencies to:

```text
requirements.txt
```

Use Flask's test client.

Example:

```python
client = app.test_client()
```

Use a separate test database.

NEVER run destructive tests against the production database.

---

# 5. TEST CONFIGURATION

Create a testing configuration.

Example:

```text
TESTING=True
```

Use:

```text
SQLite test database
```

or another isolated database already supported by the project.

The test database must be automatically created and cleaned appropriately.

---

# 6. TEST FIXTURES

Create reusable fixtures for:

```text
Anonymous Client
Regular User
Admin User
Food Entry
Prediction
Recommendation
Waste Record
```

Example conceptual users:

```text
user@test.com
admin@test.com
```

Use test-only passwords.

Never use real production credentials.

---

# 7. APPLICATION STARTUP TEST

Verify:

```text
Flask application starts successfully
```

Test:

```text
app.py
```

Expected:

```text
No startup exception
```

---

# 8. DATABASE CONNECTION TEST

Verify:

```text
Database connection
Tables
Migrations
Models
Relationships
Indexes
```

Test that all required tables exist.

Expected:

```text
Users
Food Entries
Predictions
Recommendations
Waste Records
Activity Logs
```

Only test ActivityLog if implemented.

---

# 9. USER REGISTRATION TEST

Test successful signup.

Input:

```text
Name
Valid Email
Strong Password
Confirm Password
```

Expected:

```text
Account created
User redirected to login/dashboard
Password securely hashed
Role automatically USER
```

---

# 10. INVALID SIGNUP TESTS

Test:

```text
Empty name
Empty email
Invalid email
Weak password
Password mismatch
Duplicate email
Very long input
Invalid characters where applicable
```

Expected:

```text
Validation error
No database corruption
```

---

# 11. ADMIN ROLE SIGNUP SECURITY TEST

Attempt:

```text
role=ADMIN
```

during normal signup.

Expected:

```text
Admin role must NOT be granted.
```

A normal registration must always create:

```text
role=USER
```

unless a secure admin creation process is explicitly used.

---

# 12. LOGIN TEST

Test valid login:

```text
Correct email
Correct password
```

Expected:

```text
Successful authentication
Correct dashboard redirect
Session created
```

---

# 13. INVALID LOGIN TEST

Test:

```text
Wrong password
Unknown email
Empty email
Empty password
Invalid email
```

Expected:

```text
Login rejected
Friendly error message
No crash
```

---

# 14. LOGOUT TEST

Test:

```text
Login
Logout
Access protected page
```

Expected:

```text
Protected page redirects to login
```

---

# 15. SESSION TESTING

Verify:

```text
Session created after login
Session removed after logout
Protected routes require authentication
```

Verify user identity cannot be modified through browser requests.

---

# 16. PASSWORD SECURITY TEST

Verify passwords are:

```text
Hashed
```

Never stored as:

```text
Plain text
```

Verify password hashes are not displayed in:

```text
HTML
API responses
Admin pages
Logs
Reports
```

---

# 17. FOOD ENTRY TEST

Test successful food entry.

Example:

```text
Food Name: Tomato
Category: Vegetables
Quantity: 2
Unit: kg
Purchase Date: valid date
Expiry Date: future date
```

Expected:

```text
Food record created
Database record created
Correct user_id stored
```

---

# 18. FOOD ENTRY VALIDATION

Test:

```text
Empty food name
Negative quantity
Zero quantity
Invalid date
Expiry before purchase
Invalid category
Extremely large quantity
Invalid file upload
Unsupported image format
```

Expected:

```text
Validation error
No invalid database record
```

---

# 19. FOOD IMAGE TESTING

If image upload exists, test:

```text
Valid image
Invalid extension
Large file
Empty file
Corrupted image
```

Allowed formats should match the project configuration.

Verify:

```text
Secure filename
File size limit
Correct upload directory
No executable files accepted
```

---

# 20. USER DATA ISOLATION TEST

Create:

```text
User A
User B
```

User A creates food:

```text
Tomato
```

User B creates food:

```text
Milk
```

Verify:

```text
User A sees Tomato only.
User B sees Milk only.
```

This is a CRITICAL security test.

---

# 21. ML MODEL TESTING

Test the ML model independently.

Input:

```text
Valid food data
```

Expected:

```text
Prediction returned
```

Prediction must belong to expected categories:

```text
LOW
MEDIUM
HIGH
```

or whatever categories the actual model supports.

Do not assume labels that differ from the existing model.

---

# 22. ML INVALID INPUT TEST

Test:

```text
Missing values
Invalid values
Negative quantity
Unknown category
Malformed image
Wrong feature format
```

Expected:

```text
Controlled error
No application crash
```

---

# 23. ML PREDICTION DATABASE TEST

After prediction:

Verify:

```text
Prediction record created
Food entry linked
Correct user linked
Risk stored
Confidence stored only if model provides it
Model version stored if implemented
Timestamp stored
```

---

# 24. ML MODEL FAILURE TEST

Simulate model failure.

Expected:

```text
Friendly error
Application remains running
Database remains consistent
No incomplete prediction record
```

---

# 25. PREDICTION PAGE TEST

Verify:

```text
Food information displayed
Prediction displayed
Risk level displayed
Confidence displayed only when available
Model information displayed if implemented
```

---

# 26. RECOMMENDATION TESTING

Test:

```text
Prediction
   ↓
Recommendation generation
```

Expected:

```text
Relevant recommendation returned
Recommendation stored if persistence is implemented
Correct food entry linked
Correct user linked
```

---

# 27. RECOMMENDATION VALIDATION

Test cases for:

```text
LOW risk
MEDIUM risk
HIGH risk
```

Verify recommendations correspond to actual project logic.

Do not test against invented expected text if the recommendation engine is dynamic.

Test:

```text
Recommendation exists
Recommendation type is valid
Recommendation belongs to correct user/food entry
```

---

# 28. DASHBOARD TESTING

Test dashboard after login.

Verify:

```text
Total food items
Risk statistics
Recent food
Recent predictions
Recommendations
Waste information
```

All displayed values must match database data.

---

# 29. DASHBOARD EMPTY STATE

Create a new user with no data.

Expected:

```text
No food entries yet
No predictions yet
No recommendations yet
```

No fake statistics.

---

# 30. REPORT TESTING

Test:

```text
Reports page
Summary
Risk distribution
Category distribution
Waste trend
Usage vs waste
High-risk foods
Expiring foods
Prediction analytics
Recommendation analytics
```

Verify all values match database records.

---

# 31. REPORT FILTER TESTING

Test:

```text
Date Range
Category
Risk
```

Verify filters affect:

```text
Cards
Charts
Tables
Insights
Exports
```

---

# 32. REPORT DATE VALIDATION

Test:

```text
Start date > End date
Invalid date
Missing date
Future date
Very large date range
```

Expected:

```text
Controlled validation
No SQL errors
No crash
```

---

# 33. REPORT EXPORT TESTING

Test:

```text
CSV Export
PDF Export
Print
```

Verify:

```text
Correct user data
Correct filters
Correct date range
No password
No API key
No authentication token
```

---

# 34. ADMIN ACCESS TESTING

Create:

```text
Admin
Normal User
```

Test:

```text
Admin → /admin/dashboard
```

Expected:

```text
Allowed
```

Test:

```text
User → /admin/dashboard
```

Expected:

```text
403 or secure redirect
```

---

# 35. ADMIN API SECURITY

Normal user must not access:

```text
/api/admin/users
/api/admin/reports
/api/admin/dashboard/statistics
/api/admin/health
```

Expected:

```text
403 Forbidden
```

or the project's secure equivalent.

---

# 36. ADMIN USER MANAGEMENT TEST

Test:

```text
View users
Search users
Filter users
Pagination
View user details
Change role
Disable/delete where implemented
```

Verify database updates correctly.

---

# 37. LAST ADMIN PROTECTION

If there is only one admin:

Attempt to remove or demote that admin.

Expected:

```text
Action rejected or confirmation policy applied.
System must not accidentally become adminless.
```

---

# 38. ACTIVITY LOG TEST

If activity logging exists, verify important admin actions create logs:

```text
Admin Login
Viewed User
Role Change
User Disable/Delete
Report Export
Settings Change
```

Never log:

```text
Passwords
API keys
Session tokens
```

---

# 39. API TESTING

Test every important endpoint.

Examples:

```text
/auth/login
/auth/signup
/dashboard
/food-entry
/prediction
/recommendations
/reports
/admin/dashboard
/admin/users
```

Verify:

```text
Status Code
Response
Authentication
Authorization
Validation
Error Handling
```

---

# 40. HTTP STATUS TESTING

Use appropriate status codes.

Examples:

```text
200 → Success
201 → Created
400 → Bad Request
401 → Unauthenticated
403 → Forbidden
404 → Not Found
405 → Method Not Allowed
500 → Internal Server Error
```

Do not return sensitive exception details.

---

# 41. CSRF TESTING

If forms use Flask-WTF or another CSRF system:

Test:

```text
Valid CSRF token
Missing CSRF token
Invalid CSRF token
```

Expected:

```text
Invalid requests rejected.
```

---

# 42. SQL INJECTION TEST

Test input fields with malicious-looking values such as:

```text
' OR '1'='1
```

and similar injection attempts.

Verify:

```text
No SQL injection
No database corruption
```

Use parameterized ORM/database queries.

Never construct SQL using raw user input.

---

# 43. XSS TEST

Test fields such as:

```text
Food Name
User Name
Recommendation Text
Search
```

with HTML/JavaScript-like input.

Verify the application escapes untrusted content.

Do not render raw user input as HTML.

---

# 44. PATH TRAVERSAL TEST

For file uploads, test malicious filenames such as:

```text
../../file
```

Verify:

```text
Secure filename handling
No arbitrary filesystem access
```

---

# 45. FILE UPLOAD SECURITY

Verify:

```text
Allowed extensions
File size limit
MIME validation where appropriate
Secure filenames
Upload directory isolation
```

Reject dangerous executable files.

---

# 46. AUTHORIZATION TESTING

Test object-level authorization.

Example:

```text
User A
 ↓
Try accessing User B's food ID
```

Expected:

```text
403 or 404
```

Never reveal User B's data.

Test the same for:

```text
Predictions
Recommendations
Waste Records
Reports
```

---

# 47. 404 TESTING

Test invalid URLs:

```text
/random-page
/admin/random-page
/food/999999
```

Expected:

```text
Professional 404 page
```

No traceback.

---

# 48. 500 ERROR TESTING

Simulate controlled backend failure.

Expected:

```text
Professional error page/message
```

Do not display:

```text
Python traceback
File paths
Database credentials
Secret configuration
```

---

# 49. DATABASE TRANSACTION TESTING

For multi-step operations:

```text
Food Entry
 ↓
Prediction
 ↓
Recommendation
```

If a later operation fails, verify database consistency.

Do not leave incomplete or orphaned records unless the architecture intentionally supports them.

Use transactions where appropriate.

---

# 50. DUPLICATE DATA TEST

Test repeated submissions.

Verify the application handles:

```text
Double-click submit
Browser refresh
Repeated API request
```

appropriately.

Avoid accidental duplicate records where the business logic requires idempotency.

---

# 51. FRONTEND FORM TESTING

Test every form:

```text
Signup
Login
Food Entry
Filters
Search
Admin actions
```

Test:

```text
Valid data
Empty data
Invalid data
Boundary values
Long text
Special characters
```

---

# 52. JAVASCRIPT TESTING

Check browser console.

There must be no unexpected:

```text
JavaScript errors
404 static file errors
Failed API requests
Undefined variables
```

Verify:

```text
Buttons work
Navigation works
Charts render
Filters work
Modal dialogs work
Forms submit correctly
```

---

# 53. RESPONSIVE TESTING

Test:

```text
Desktop
Laptop
Tablet
Mobile
```

Check:

```text
Navigation
Forms
Tables
Charts
Cards
Buttons
Reports
Admin sidebar
```

No major horizontal overflow except intentionally scrollable tables.

---

# 54. ACCESSIBILITY TESTING

Verify:

```text
Labels
ARIA where needed
Keyboard navigation
Focus states
Alt text
Heading hierarchy
Button labels
Color contrast
```

Do not communicate risk using color alone.

---

# 55. PERFORMANCE TESTING

Test:

```text
Dashboard load
Reports load
Admin dashboard load
Large food dataset
Large user dataset
Large prediction dataset
```

Look for:

```text
N+1 queries
Unnecessary database queries
Large API responses
Slow chart rendering
Unnecessary ML inference
```

---

# 56. ML PERFORMANCE

Do not retrain the ML model on every request.

Verify:

```text
Model loads efficiently
Prediction response is acceptable
Model is reused where appropriate
```

---

# 57. DATABASE PERFORMANCE

Verify indexes exist where appropriate for:

```text
user_id
created_at
expiry_date
category
risk/waste_level
```

Do not add unnecessary indexes blindly.

---

# 58. REGRESSION TESTING

After fixing a bug:

Run the entire test suite again.

Verify that fixes did not break:

```text
Login
Signup
Food Entry
Prediction
Recommendations
Dashboard
Reports
Admin
```

---

# 59. TEST COMMANDS

Add useful commands to project documentation.

Example:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

For coverage if configured:

```bash
pytest --cov
```

Use the project's actual environment and dependency setup.

---

# 60. REQUIREMENTS

Ensure testing dependencies are present.

Example:

```text
pytest
pytest-cov
```

Only add packages that are actually needed.

---

# 61. TEST REPORT

Generate a test report containing:

```text
AI FOOD WASTE REDUCTION SYSTEM

Testing Summary

Total Tests
Passed
Failed
Skipped
Errors

Module
Status

Authentication
Food Entry
ML Model
Prediction
Recommendations
Dashboard
Reports
Admin
Database
Security
```

Example:

```text
Authentication     PASS
Food Entry         PASS
Prediction         PASS
Reports            PASS
Admin              PASS
Security           PASS
```

Use actual results.

Never claim PASS if the test was not executed.

---

# 62. BUG TRACKING

If tests fail, create:

```text
TESTING_REPORT.md
```

Include:

```text
Bug ID
Module
Test
Expected Result
Actual Result
Severity
Status
Fix
```

Severity:

```text
Critical
High
Medium
Low
```

Do not hide failures.

---

# 63. CRITICAL BUGS

Treat these as critical:

```text
Normal user can access admin panel
User can access another user's data
Passwords exposed
API keys exposed
SQL injection possible
Authentication bypass
Database corruption
ML system crashes entire application
```

These must be fixed before deployment.

---

# 64. FINAL TEST FLOW

Run:

```text
1. Install dependencies
2. Configure test environment
3. Create test database
4. Run migrations
5. Run unit tests
6. Run integration tests
7. Run API tests
8. Run authentication tests
9. Run authorization tests
10. Run database tests
11. Run ML tests
12. Run report tests
13. Run admin tests
14. Run security tests
15. Run frontend checks
16. Run performance checks
17. Run regression tests
18. Generate testing report
```

---

# 65. FINAL QUALITY CHECK

Before declaring testing complete, verify:

[ ] Application starts

[ ] Database connects

[ ] Signup works

[ ] Login works

[ ] Logout works

[ ] Authentication works

[ ] Authorization works

[ ] User role security works

[ ] Food entry works

[ ] Food validation works

[ ] Image upload security works if implemented

[ ] ML prediction works

[ ] ML failure handled

[ ] Recommendations work

[ ] Dashboard works

[ ] Reports work

[ ] Report filters work

[ ] CSV export works

[ ] PDF export works

[ ] Admin dashboard works

[ ] Admin authorization works

[ ] User management works

[ ] Admin reports work

[ ] Activity logging works if implemented

[ ] Database isolation works

[ ] SQL injection protection verified

[ ] XSS protection verified

[ ] File upload security verified

[ ] CSRF protection verified where applicable

[ ] Error pages work

[ ] Responsive design verified

[ ] Accessibility checked

[ ] Performance checked

[ ] Regression tests passed

[ ] No critical security issues

[ ] No fake test results

[ ] Testing report generated

---

# 66. FINAL INSTRUCTION TO ANTIGRAVITY

Do NOT simply create test files and claim the project is tested.

Actually inspect the existing application.

Run the tests.

Identify failures.

Fix the implementation where appropriate.

Run the tests again.

Repeat until the application reaches a stable state.

At the end, provide:

```text
1. Tests created
2. Tests executed
3. Tests passed
4. Tests failed
5. Bugs discovered
6. Bugs fixed
7. Remaining warnings
8. Security issues
9. Final test status
```

Do not claim 100% success unless the tests actually pass.

The final application must be ready for the next stage:

**DEPLOYMENT → PRODUCTION CONFIGURATION → LIVE WEBSITE.**
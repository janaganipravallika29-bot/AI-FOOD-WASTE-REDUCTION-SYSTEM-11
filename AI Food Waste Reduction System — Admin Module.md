# MASTER PROMPT — ADMIN MODULE

You are an expert full-stack Flask developer, database engineer, security engineer, UI/UX designer, and system administrator.

My project title is:

**AI FOOD WASTE REDUCTION SYSTEM**

The following modules are already implemented:

- Frontend Design
- Flask Backend
- Database
- Login/Signup
- Authentication
- Food Entry
- ML Model
- Prediction
- Smart Recommendations
- User Dashboard
- Reports

Now implement the complete:

# ADMIN MODULE

The Admin module must provide a secure administration panel for managing and monitoring the entire application.

IMPORTANT:

The Admin panel must be completely separate from the normal user dashboard.

Normal users must NEVER be able to access admin pages or admin APIs.

Do not use fake statistics or hardcoded database values.

---

# 1. ADMIN SYSTEM OBJECTIVE

Final application flow:

```text
USER
 ↓
LOGIN
 ↓
USER DASHBOARD
 ↓
Food Entry
 ↓
Prediction
 ↓
Recommendations
 ↓
Reports


ADMIN
 ↓
ADMIN LOGIN
 ↓
ADMIN DASHBOARD
 ↓
Users
Food Entries
Predictions
Recommendations
Reports
Analytics
System Monitoring
```

---

# 2. ROLE-BASED ACCESS CONTROL

Add a role system to the User model.

Use:

```text
role
```

Possible values:

```text
USER
ADMIN
```

Default new registration:

```text
USER
```

Never allow users to select:

```text
ADMIN
```

during normal signup.

---

# 3. ADMIN AUTHORIZATION

Create a reusable decorator:

```python
@admin_required
```

The decorator must verify:

```text
User is logged in
AND
User role == ADMIN
```

If not logged in:

```text
→ /login
```

If logged in but not an admin:

```text
→ 403 Forbidden
```

Never rely only on hiding admin buttons in HTML.

Authorization must be enforced on the Flask backend.

---

# 4. ADMIN LOGIN

Use the existing authentication system.

Admin login:

```text
/login
```

After successful authentication:

```text
role == ADMIN
      ↓
/admin/dashboard
```

Normal user:

```text
role == USER
      ↓
/dashboard
```

Do not create a separate password database for admins.

Use secure password hashing already used by the application.

---

# 5. ADMIN URLS

Create:

```text
/admin/dashboard
/admin/users
/admin/food-entries
/admin/predictions
/admin/recommendations
/admin/reports
/admin/settings
/admin/activity
```

Optional:

```text
/admin/users/<user_id>
/admin/food-entries/<food_id>
/admin/predictions/<prediction_id>
```

All admin routes must use:

```python
@admin_required
```

---

# 6. ADMIN FILE STRUCTURE

Create/update:

```text
routes/admin_routes.py
```

Templates:

```text
templates/admin/
├── dashboard.html
├── users.html
├── user_details.html
├── food_entries.html
├── predictions.html
├── recommendations.html
├── reports.html
├── activity.html
└── settings.html
```

CSS:

```text
static/css/admin.css
```

JavaScript:

```text
static/js/admin.js
```

---

# 7. ADMIN DASHBOARD

Create:

```text
/admin/dashboard
```

Page title:

```text
ADMIN DASHBOARD
```

Subtitle:

```text
Monitor and manage the AI Food Waste Reduction System.
```

---

# 8. ADMIN SIDEBAR

Create a professional sidebar:

```text
🏠 Dashboard
👥 Users
🍎 Food Entries
🤖 Predictions
💡 Recommendations
📊 Reports
📈 Analytics
📝 Activity Logs
⚙ Settings
🚪 Logout
```

Use the existing application theme.

---

# 9. ADMIN TOP BAR

Display:

```text
AI FOOD WASTE REDUCTION SYSTEM

Admin Panel
```

Right side:

```text
Admin Name
Profile
Logout
```

Do not display passwords.

---

# 10. ADMIN SUMMARY CARDS

Create:

```text
TOTAL USERS
TOTAL FOOD ENTRIES
TOTAL PREDICTIONS
TOTAL RECOMMENDATIONS
```

Additional cards:

```text
HIGH-RISK FOODS
MEDIUM-RISK FOODS
LOW-RISK FOODS
RECORDED FOOD WASTE
```

All values must come from the database.

Never hardcode numbers.

---

# 11. USER STATISTICS

Show:

```text
Total Registered Users
Active Users
New Users
Admin Users
```

If activity tracking is not available, do not invent "active users".

Display:

```text
Activity data unavailable
```

instead.

---

# 12. FOOD STATISTICS

Show:

```text
Total Food Items
Total Quantity Tracked
Food Categories
Expiring Food
Expired Food
```

Use actual FoodEntry records.

---

# 13. PREDICTION STATISTICS

Show:

```text
Total Predictions
LOW
MEDIUM
HIGH
Average Confidence
```

Only calculate confidence if confidence data exists.

Do not invent confidence scores.

---

# 14. RECOMMENDATION STATISTICS

Show:

```text
Total Recommendations
High Priority
Medium Priority
Low Priority
```

Use actual Recommendation records.

---

# 15. WASTE ANALYTICS

Create:

```text
TOTAL RECORDED WASTE
WASTE BY CATEGORY
WASTE BY REASON
WASTE TREND
```

Use actual WasteRecord data.

If no waste records exist:

```text
No waste data available yet.
```

Do not create fake values.

---

# 16. ADMIN CHARTS

Create professional charts:

```text
1. User Growth
2. Food Entries Over Time
3. Risk Distribution
4. Food Category Distribution
5. Waste Trend
6. Waste Reason Distribution
7. Prediction Distribution
```

Use Chart.js if already used in the project.

Charts must use database-generated data.

---

# 17. USER GROWTH CHART

Create:

```text
USER REGISTRATION TREND
```

X-axis:

```text
Date
```

Y-axis:

```text
Number of Users
```

Use actual user creation dates.

If there is insufficient historical data:

```text
Not enough user history yet.
```

---

# 18. FOOD ENTRY TREND

Create:

```text
FOOD ENTRY TREND
```

Display number of food entries by:

```text
Day
Week
Month
```

Use actual database timestamps.

---

# 19. RISK DISTRIBUTION

Create:

```text
AI WASTE-RISK DISTRIBUTION
```

Show:

```text
LOW
MEDIUM
HIGH
```

Use latest prediction per food item where appropriate.

Do not count every historical prediction as the current risk.

---

# 20. CATEGORY DISTRIBUTION

Create:

```text
FOOD CATEGORY DISTRIBUTION
```

Categories:

```text
Vegetables
Fruits
Dairy
Grains
Meat
Bakery
Cooked Food
Beverages
Other
```

Use actual records.

---

# 21. ADMIN USERS PAGE

Create:

```text
/admin/users
```

Display:

```text
USERS
```

Table:

```text
ID
Name
Email
Role
Created Date
Status
Actions
```

Actions:

```text
View
Edit Role
Disable
Delete
```

Be careful with destructive actions.

---

# 22. USER SEARCH

Add:

```text
Search users...
```

Search:

```text
Name
Email
```

Use backend filtering.

---

# 23. USER FILTER

Filters:

```text
All
USER
ADMIN
```

Optional status:

```text
Active
Disabled
```

Only implement status if the User model supports it.

---

# 24. USER PAGINATION

Display:

```text
10 / 25 / 50 / 100
```

records per page.

Add:

```text
Previous
Next
```

Do not load thousands of users at once.

---

# 25. USER DETAILS

Create:

```text
/admin/users/<user_id>
```

Display:

```text
Name
Email
Role
Registration Date
Food Entries Count
Predictions Count
Recommendations Count
Waste Records Count
```

Do not display:

```text
Password
Password Hash
Authentication Tokens
Session Information
```

---

# 26. EDIT USER ROLE

Allow authorized admin to change:

```text
USER
ADMIN
```

Before changing the role, show confirmation:

```text
Are you sure you want to change this user's role?
```

Do not allow an admin to accidentally remove the last administrative account without warning.

---

# 27. DELETE USER

Create:

```text
DELETE USER
```

This must require confirmation.

Example:

```text
This action permanently removes the user's account and associated data.
Are you sure?
```

Use appropriate database cascading rules.

Never delete data accidentally.

Prefer soft-delete/disable if the project supports it.

---

# 28. ADMIN FOOD ENTRIES PAGE

Create:

```text
/admin/food-entries
```

Table:

```text
Food
Category
Quantity
Unit
Expiry Date
User
Risk
Created Date
Action
```

Admin can:

```text
View
```

Do not allow unnecessary editing/deletion unless required.

---

# 29. FOOD ENTRY SEARCH

Search:

```text
Food Name
Category
User Email
```

Filters:

```text
Category
Risk
Date Range
```

Use pagination.

---

# 30. ADMIN PREDICTIONS PAGE

Create:

```text
/admin/predictions
```

Table:

```text
Food
User
Risk
Confidence
Model Version
Created Date
```

Show:

```text
LOW
MEDIUM
HIGH
```

Use actual prediction data.

---

# 31. ADMIN RECOMMENDATIONS PAGE

Create:

```text
/admin/recommendations
```

Table:

```text
Food
User
Recommendation
Priority
Created Date
Status
```

If status tracking does not exist:

```text
Do not invent it.
```

---

# 32. ADMIN REPORTS

Create:

```text
/admin/reports
```

Include:

```text
User Statistics
Food Statistics
Prediction Statistics
Recommendation Statistics
Waste Statistics
```

Add filters:

```text
Date Range
Category
Risk
```

---

# 33. ADMIN EXPORT

Allow administrators to export aggregate/application reports:

```text
Export CSV
Export PDF
Print
```

Exports must respect filters.

Do not expose passwords or authentication information.

---

# 34. ADMIN ACTIVITY LOG

Create:

```text
/admin/activity
```

If an activity-log table exists, display:

```text
Timestamp
User
Action
Resource
Status
```

Example:

```text
12 Aug 2026 10:20
Admin
Viewed Reports
Reports
Success
```

If activity logging does not yet exist, implement a simple:

```text
ActivityLog
```

model.

---

# 35. ACTIVITY LOG MODEL

If required, create:

```text
ActivityLog
```

Fields:

```text
id
user_id
action
resource_type
resource_id
timestamp
ip_address
status
```

Do not store passwords or sensitive authentication secrets.

---

# 36. LOG IMPORTANT ADMIN ACTIONS

Record actions such as:

```text
Admin Login
Viewed User
Changed User Role
Disabled User
Deleted User
Viewed Report
Exported Report
Changed Settings
```

Do not log sensitive credentials.

---

# 37. ADMIN SETTINGS

Create:

```text
/admin/settings
```

Possible settings:

```text
Application Name
Application Description
Prediction Model Version
Report Settings
Pagination Size
```

Do not expose API keys in the frontend.

Do not place secret keys directly in HTML.

---

# 38. ML MODEL INFORMATION

Admin dashboard should show:

```text
AI MODEL
```

Display:

```text
Model Name
Model Version
Last Updated
Number of Predictions
```

If these values exist in configuration/model metadata.

Do not claim model accuracy unless it has been properly evaluated and stored.

---

# 39. SYSTEM HEALTH

Create:

```text
SYSTEM STATUS
```

Check:

```text
Flask Application
Database Connection
ML Model Availability
Required Configuration
```

Display:

```text
✓ Database Connected
✓ ML Model Available
✓ Application Running
```

Only display a check if the actual check succeeds.

---

# 40. DATABASE HEALTH

Create a backend health check:

```text
/api/admin/health
```

Return status for:

```text
database
model
application
```

Protect endpoint with admin authorization.

---

# 41. SECURITY

Implement:

```text
Authentication
Authorization
Role-Based Access Control
CSRF Protection where applicable
Secure Password Hashing
Session Security
Input Validation
SQL Injection Protection
XSS Protection
```

Never trust frontend role values.

Never allow:

```text
role=ADMIN
```

through signup.

---

# 42. ADMIN API SECURITY

Every admin API must verify:

```python
@login_required
@admin_required
```

Example:

```text
/api/admin/users
/api/admin/statistics
/api/admin/reports
/api/admin/health
```

Normal users must receive:

```text
403 Forbidden
```

---

# 43. ADMIN DASHBOARD API

Create:

```text
/api/admin/dashboard/statistics
```

Example structure:

```json
{
    "success": true,
    "statistics": {
        "users": 100,
        "food_entries": 250,
        "predictions": 240,
        "recommendations": 180,
        "high_risk": 30,
        "medium_risk": 80,
        "low_risk": 130
    }
}
```

The numbers above are examples only.

Calculate actual values from the database.

---

# 44. ADMIN JAVASCRIPT

Create/update:

```text
static/js/admin.js
```

Functions:

```text
loadAdminStatistics()
loadUserGrowth()
loadFoodTrend()
loadRiskDistribution()
loadCategoryDistribution()
loadWasteTrend()
loadPredictionStatistics()
searchUsers()
filterUsers()
deleteUser()
updateUserRole()
exportAdminReport()
checkSystemHealth()
```

---

# 45. RESPONSIVE DESIGN

Desktop:

```text
Sidebar + Main Content
```

Tablet:

```text
Collapsible Sidebar
```

Mobile:

```text
Hamburger Menu
Single-column Cards
Scrollable Tables
Responsive Charts
```

---

# 46. ADMIN EMPTY STATES

If there are no users:

```text
No users registered yet.
```

If there are no food entries:

```text
No food entries available.
```

If there are no predictions:

```text
No predictions generated yet.
```

If there are no waste records:

```text
No waste records available yet.
```

Never show fake statistics.

---

# 47. ERROR HANDLING

Use friendly messages:

```text
Unable to load admin data.
Please try again.
```

For unauthorized users:

```text
You do not have permission to access this page.
```

Do not expose:

```text
Python traceback
Database credentials
Secret keys
Stack traces
```

---

# 48. DATABASE CHANGES

If the User model does not have a role:

Add:

```text
role
```

Default:

```text
USER
```

If necessary, create:

```text
ActivityLog
```

Do not destroy existing database data.

Create proper migration/update logic.

---

# 49. INITIAL ADMIN ACCOUNT

Create a safe setup method for creating the first admin.

Use an environment variable or secure CLI command.

Example concept:

```text
python create_admin.py
```

The script should ask for:

```text
Admin Name
Admin Email
Admin Password
```

Hash the password securely before storing it.

Do NOT hardcode an admin password into source code.

Do NOT print the password into logs.

---

# 50. ADMIN LOGOUT

Admin logout:

```text
/admin/logout
```

or reuse the existing secure logout route.

After logout:

```text
/admin/dashboard
```

must not be accessible.

Redirect to:

```text
/login
```

---

# 51. TESTING

Create/update:

```text
tests/test_admin.py
```

Test:

```text
Admin Login
Normal User Login
Role Detection
Admin Dashboard
Admin APIs
Normal User Access
Unauthorized Access
User Listing
User Search
User Filtering
User Details
Role Change
User Disable/Delete
Food Entries
Predictions
Recommendations
Reports
Exports
Activity Logs
System Health
Admin Logout
```

---

# 52. SECURITY TEST

Test:

```text
USER
 ↓
/admin/dashboard
 ↓
403
```

Test:

```text
USER
 ↓
/api/admin/users
 ↓
403
```

Test:

```text
ADMIN
 ↓
/admin/dashboard
 ↓
200
```

Test:

```text
ADMIN
 ↓
/api/admin/dashboard/statistics
 ↓
200
```

---

# 53. DATA ISOLATION

Verify that:

```text
Normal User
```

cannot access:

```text
All Users
All Food Entries
All Predictions
All Recommendations
All Waste Records
```

Only admins can access aggregate application-wide data.

---

# 54. ADMIN UI DESIGN

Use a professional administrative interface.

Design:

```text
AI + Food + Analytics
```

Use:

- Clean cards
- Data tables
- Charts
- Status badges
- Icons
- Responsive sidebar
- Professional spacing
- Consistent typography
- Subtle shadows
- Rounded components

Do not make the interface excessively colorful.

Keep it suitable for a college project demonstration.

---

# 55. FINAL ADMIN STRUCTURE

Use:

```text
AI_Food_Waste_Reduction_System/
│
├── app.py
├── requirements.txt
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
│   ├── login.html
│   ├── dashboard.html
│   ├── reports.html
│   │
│   └── admin/
│       ├── dashboard.html
│       ├── users.html
│       ├── user_details.html
│       ├── food_entries.html
│       ├── predictions.html
│       ├── recommendations.html
│       ├── reports.html
│       ├── activity.html
│       └── settings.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── admin.css
│   │   └── print.css
│   │
│   └── js/
│       ├── script.js
│       ├── dashboard.js
│       ├── reports.js
│       └── admin.js
│
├── tests/
│   ├── test_auth.py
│   ├── test_dashboard.py
│   ├── test_reports.py
│   └── test_admin.py
│
└── create_admin.py
```

Do not duplicate files that already exist.

---

# 56. COMPLETE ADMIN FLOW

The completed system must work as:

```text
APPLICATION
      │
      ▼
    LOGIN
      │
      ├────────────── USER ──────────────┐
      │                                  │
      ▼                                  ▼
 USER DASHBOARD                    FOOD ENTRY
      │                                  │
      ▼                                  ▼
 PREDICTION                      AI ANALYSIS
      │                                  │
      ▼                                  ▼
 RECOMMENDATIONS                 REPORTS
      │
      ▼
 USER REPORTS


LOGIN
  │
  └──────── ADMIN ────────┐
                          ▼
                  ADMIN DASHBOARD
                          │
       ┌──────────────────┼─────────────────┐
       ▼                  ▼                 ▼
     USERS          FOOD ENTRIES       PREDICTIONS
       │                  │                 │
       ▼                  ▼                 ▼
 RECOMMENDATIONS       REPORTS          ANALYTICS
       │                  │                 │
       └──────────────────┼─────────────────┘
                          ▼
                   SYSTEM MONITORING
```

---

# 57. FINAL CHECKLIST

Before completing the Admin module:

[ ] User role system implemented

[ ] New users default to USER

[ ] Users cannot select ADMIN during signup

[ ] Admin authorization implemented

[ ] Admin login routing works

[ ] User login routing works

[ ] Admin dashboard works

[ ] Admin statistics come from database

[ ] User management works

[ ] User search works

[ ] User filtering works

[ ] User pagination works

[ ] User details work

[ ] Role management works

[ ] Safe delete/disable behavior implemented

[ ] Food entry management works

[ ] Prediction management works

[ ] Recommendation management works

[ ] Admin reports work

[ ] Admin charts work

[ ] Waste analytics work

[ ] Activity logging works

[ ] System health works

[ ] Database health check works

[ ] ML model status works

[ ] CSV export works

[ ] PDF export works

[ ] Admin settings work

[ ] Admin logout works

[ ] Normal users cannot access admin pages

[ ] Normal users cannot access admin APIs

[ ] No passwords displayed

[ ] No API keys exposed

[ ] No fake statistics

[ ] No fake charts

[ ] Responsive design works

[ ] Security validation implemented

[ ] Tests pass

---

# FINAL INSTRUCTION

Implement the complete **ADMIN MODULE** for:

**AI FOOD WASTE REDUCTION SYSTEM**

Connect:

**Authentication → Role-Based Access Control → Admin Dashboard → Users → Food Entries → ML Predictions → Recommendations → Reports → Analytics → Activity Logs → System Monitoring**

The Admin module must be secure, database-driven, responsive, professional, and fully connected to the existing Flask application.

Do not rebuild the existing modules unnecessarily.

Reuse the existing models, authentication, database, routes, styles, and components wherever possible.

Do not use fake data.

After completing this module, leave the entire project ready for the final stages:

**TESTING → SECURITY TESTING → DEPLOYMENT → PRODUCTION CONFIGURATION.**
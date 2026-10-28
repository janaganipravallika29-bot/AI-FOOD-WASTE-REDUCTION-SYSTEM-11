# MASTER PROMPT — DASHBOARD MODULE

You are an expert full-stack Flask developer, database engineer, UI/UX designer, data visualization developer, and AI application developer.

My project title is:

**AI FOOD WASTE REDUCTION SYSTEM**

The following modules are already implemented:

- Frontend
- Flask Backend
- Database
- Login/Signup
- Authentication
- Food Entry
- ML Model
- Prediction
- Smart Recommendations

Now implement the complete:

**DASHBOARD MODULE**

The dashboard must become the main control center after login.

---

# 1. DASHBOARD OBJECTIVE

After successful login:

```text
LOGIN
  ↓
DASHBOARD
  ↓
Food Entry
  ↓
AI Prediction
  ↓
Smart Recommendations
  ↓
Reports
```

The dashboard must show the user's food-waste information in a simple, colorful, professional, and easy-to-understand interface.

Do not use hardcoded statistics.

All dashboard statistics must come from the database.

---

# 2. DASHBOARD URL

Create/update:

```text
/dashboard
```

The dashboard must require authentication.

Use the existing login system.

If the user is not logged in:

```text
/dashboard
     ↓
/login
```

---

# 3. DASHBOARD FILE

Create/update:

```text
templates/dashboard.html
```

Use the existing project design system.

Do not create a completely unrelated design.

Maintain consistent:

- Colors
- Typography
- Buttons
- Cards
- Navigation
- Spacing
- Icons

---

# 4. DASHBOARD LAYOUT

Create the following structure:

```text
┌────────────────────────────────────────────────────┐
│ AI FOOD WASTE REDUCTION SYSTEM                     │
│ Logo     Dashboard  Food Entry  Reports  Profile  │
├────────────────────────────────────────────────────┤
│                                                    │
│ Welcome back, [Username] 👋                        │
│ Track your food and reduce waste with AI.          │
│                                                    │
├────────────────────────────────────────────────────┤
│                                                    │
│ Total Food │ High Risk │ Medium │ Low Risk        │
│     25     │     5     │    8   │    12           │
│                                                    │
├────────────────────────────────────────────────────┤
│                                                    │
│       WASTE RISK DISTRIBUTION                      │
│                                                    │
│             [Chart]                                │
│                                                    │
├─────────────────────────┬──────────────────────────┤
│ Foods Expiring Soon     │ Smart Recommendations   │
│                         │                          │
│ Tomatoes — 2 days       │ 🍅 Prioritize tomatoes  │
│ Milk — 3 days           │ 🥛 Plan milk usage      │
│ Bread — 4 days          │                          │
├─────────────────────────┴──────────────────────────┤
│                                                    │
│ Recent Food Entries                                │
│                                                    │
│ Food | Category | Expiry | Risk | Action           │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

# 5. SIDEBAR

Create a professional sidebar.

Navigation:

```text
🏠 Dashboard
🍎 Food Entry
🤖 AI Predictions
💡 Recommendations
📊 Reports
👤 Profile
⚙ Settings
🚪 Logout
```

On mobile, convert the sidebar into a hamburger menu.

---

# 6. TOP NAVIGATION

Desktop header:

```text
AI FOOD WASTE REDUCTION SYSTEM

Dashboard
Food Entry
Predictions
Recommendations
Reports

[Profile]
[Logout]
```

Show the logged-in user's name.

Do not display passwords or sensitive information.

---

# 7. WELCOME SECTION

Display:

```text
Welcome back, [Username] 👋
```

Subtitle:

```text
Monitor your food, understand waste risk, and take smarter actions.
```

Add primary button:

```text
+ ADD FOOD
```

Button should redirect to:

```text
/food-entry
```

or the existing food-entry route.

---

# 8. SUMMARY CARDS

Create four main statistics cards.

## CARD 1

```text
🍎 TOTAL FOOD ITEMS
```

Calculate:

```text
COUNT(food_entries)
```

for the logged-in user.

---

## CARD 2

```text
⚠ HIGH WASTE RISK
```

Calculate the number of the user's latest predictions where:

```text
risk = HIGH
```

---

## CARD 3

```text
⚡ MEDIUM WASTE RISK
```

Calculate:

```text
risk = MEDIUM
```

---

## CARD 4

```text
✓ LOW WASTE RISK
```

Calculate:

```text
risk = LOW
```

Never hardcode:

```text
25
5
8
12
```

These are examples only.

---

# 9. ADDITIONAL STATISTICS

Add another statistics section:

```text
Total Predictions
Foods Expiring Soon
Food Used
Food Wasted
Waste Reduction Rate
Recommendations Generated
```

Only display values that exist in the database.

If a metric has no data:

```text
0
```

instead of fake information.

---

# 10. WASTE RISK CHART

Create:

```text
Food Waste Risk Distribution
```

Use Chart.js if available.

Chart:

```text
LOW
MEDIUM
HIGH
```

Example:

```text
LOW       ████████████ 12
MEDIUM    ████████      8
HIGH      █████         5
```

Use actual database values.

Do not hardcode chart data.

---

# 11. CHART API

Create an endpoint:

```text
/api/dashboard/risk-distribution
```

Return:

```json
{
    "low": 12,
    "medium": 8,
    "high": 5
}
```

These values must be calculated from the current user's database records.

---

# 12. EXPIRING SOON SECTION

Create:

```text
⏳ FOODS EXPIRING SOON
```

Show foods with the nearest upcoming expiry dates.

Example:

```text
Tomatoes
2 days remaining

Milk
3 days remaining

Bread
4 days remaining
```

Show maximum:

```text
5 items
```

---

# 13. EXPIRY STATUS

Use:

```text
days_until_expiry
```

calculated by the backend.

Display:

```text
5+ days
Upcoming
```

```text
1–3 days
Soon
```

```text
0 days
Expires today
```

```text
< 0
Expired
```

Do not tell users that a food is safe based on this status.

---

# 14. EXPIRED FOOD SECTION

If expired items exist, display:

```text
⚠ ITEMS REQUIRING ATTENTION
```

Example:

```text
Milk
Expiry date passed

Tomatoes
Expiry date passed
```

Use cautious wording:

```text
These items have passed their recorded expiry dates.
Follow product labeling and applicable food-safety guidance.
```

Do not recommend consuming expired food.

---

# 15. RECENT FOOD ENTRIES

Create:

```text
RECENT FOOD ENTRIES
```

Table:

```text
Food
Category
Quantity
Expiry
Risk
Action
```

Example:

```text
Tomatoes
Vegetables
2 kg
14 Aug
HIGH
View
```

Show the latest:

```text
5–10
```

records.

---

# 16. VIEW FOOD BUTTON

Each row should contain:

```text
[VIEW]
```

which opens:

```text
/food/<food_id>
```

Use the existing food details route.

Verify ownership.

---

# 17. AI PREDICTION SECTION

Create:

```text
🤖 RECENT AI PREDICTIONS
```

Show:

```text
Food
Risk
Confidence
Date
Action
```

Example:

```text
Tomatoes
HIGH
87%
12 Aug
View
```

Click:

```text
[VIEW]
```

to:

```text
/prediction/<food_id>
```

---

# 18. SMART RECOMMENDATIONS SECTION

Create:

```text
💡 SMART RECOMMENDATIONS
```

Show the highest-priority recommendations.

Example:

```text
⚡ High Priority

Prioritize tomatoes in your upcoming meal.

[VIEW RECOMMENDATIONS]
```

Link to:

```text
/recommendations/<food_id>
```

Only show the current user's recommendations.

---

# 19. PRIORITY ACTIONS

Create a section:

```text
⚡ PRIORITY ACTIONS
```

Sort by:

```text
HIGH
MEDIUM
LOW
```

Then by nearest expiry.

Example:

```text
1. Tomatoes — HIGH
2. Milk — HIGH
3. Bread — MEDIUM
```

---

# 20. QUICK ACTIONS

Create four attractive buttons:

```text
+ Add Food
🤖 Analyze Food
💡 Recommendations
📊 View Reports
```

Links:

```text
Add Food
→ /food-entry

Analyze Food
→ food entry / prediction flow

Recommendations
→ /recommendations

Reports
→ /reports
```

Use the actual routes already present in the project.

Do not create broken links.

---

# 21. WASTE REDUCTION PROGRESS

Create:

```text
♻ WASTE REDUCTION PROGRESS
```

Display a progress bar based on real user data.

If the project has:

```text
total food
used food
wasted food
```

calculate:

```text
waste_reduction_rate =
used_food / total_tracked_food * 100
```

Use the exact definition established in the database.

Do not invent a progress percentage.

If insufficient data exists:

```text
Start tracking your food to see your progress.
```

---

# 22. FOOD USED VS WASTED

Create a chart:

```text
Food Usage Overview
```

Categories:

```text
USED
WASTED
```

Use actual `WasteRecord`/food-status data.

If the project does not yet contain used/wasted tracking:

Do not fabricate the chart.

Instead display:

```text
Start recording food usage and waste to see this analysis.
```

---

# 23. MONTHLY WASTE TREND

Create:

```text
Monthly Food Waste Trend
```

Use actual database data.

Example:

```text
Jan  Feb  Mar  Apr  May  Jun  Jul  Aug
```

Plot:

```text
Wasted Quantity
```

If historical data does not exist, show:

```text
Not enough historical data yet.
```

Do not generate fake historical values.

---

# 24. CATEGORY BREAKDOWN

Create:

```text
FOOD CATEGORY BREAKDOWN
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
Other
```

Calculate actual number of food entries per category.

Display as a chart.

---

# 25. AI INSIGHTS

Create:

```text
🤖 AI INSIGHTS
```

Generate simple insights from real data.

Examples:

```text
You currently have 3 high-risk food items.

Vegetables are your most frequently tracked category.

2 food items are approaching their recorded expiry dates.
```

Only generate insights when the underlying data supports them.

Do not fabricate insights.

---

# 26. PERSONALIZED MESSAGE

Use:

```text
Based on your current food records...
```

Example:

```text
You have several food items that should be prioritized.
Check your smart recommendations to plan their use.
```

This should update dynamically.

---

# 27. EMPTY DASHBOARD

If a new user has no food entries:

Display:

```text
🌱 YOUR DASHBOARD IS READY

You haven't added any food items yet.

Start tracking your food to receive AI-powered waste-risk
predictions and personalized recommendations.

[ + ADD YOUR FIRST FOOD ]
```

Do not display fake statistics.

---

# 28. FIRST FOOD FLOW

When the user clicks:

```text
+ ADD YOUR FIRST FOOD
```

redirect to:

```text
/food-entry
```

After adding food:

```text
Food Entry
   ↓
Dashboard
```

The dashboard should update automatically.

---

# 29. BACKEND DASHBOARD ROUTE

Create/update:

```text
routes/dashboard_routes.py
```

Route:

```python
@app.route("/dashboard")
@login_required
def dashboard():
```

Retrieve:

```text
Current User
Food Entries
Latest Predictions
Recommendations
Waste Records
Statistics
```

---

# 30. DATABASE QUERIES

Use efficient queries.

Calculate:

```text
total_food
high_risk
medium_risk
low_risk
expiring_soon
expired
recent_predictions
recent_recommendations
used_food
wasted_food
```

Filter all user-specific records using:

```text
current_user.id
```

Never show another user's data.

---

# 31. LATEST PREDICTION LOGIC

If multiple predictions exist for the same food:

Use the latest prediction:

```text
ORDER BY created_at DESC
```

Do not count every historical prediction as a current food risk.

---

# 32. SECURITY

Dashboard must enforce:

```text
@login_required
```

Every database query must be scoped to the current user.

Never accept:

```text
user_id
```

from the frontend for authorization.

Use:

```python
current_user.id
```

from the authenticated session.

---

# 33. ADMIN DASHBOARD

Create a separate admin dashboard:

```text
/admin/dashboard
```

Only authorized admins can access it.

Admin statistics:

```text
Total Users
Total Food Entries
Total Predictions
High Risk Foods
Medium Risk Foods
Low Risk Foods
Total Recommendations
Total Waste Records
```

Do not expose unnecessary personal information.

---

# 34. ADMIN CHARTS

Create:

```text
User Growth
Food Entries
Prediction Distribution
Food Category Distribution
Waste Trend
```

All charts must use actual database data.

---

# 35. ADMIN DASHBOARD API

Create endpoints such as:

```text
/api/admin/dashboard/statistics
/api/admin/dashboard/risk-distribution
/api/admin/dashboard/category-distribution
```

Protect every admin endpoint.

---

# 36. PROFILE SECTION

Dashboard header should include:

```text
[Profile]
```

Clicking it should open:

```text
/profile
```

Display only appropriate user information.

Do not display passwords.

---

# 37. LOGOUT

Logout button:

```text
🚪 Logout
```

Use the existing logout route.

After logout:

```text
/dashboard
```

must not remain accessible.

Redirect to:

```text
/login
```

---

# 38. RESPONSIVE DESIGN

Desktop:

```text
Sidebar | Main Dashboard
```

Tablet:

```text
Collapsible Sidebar
```

Mobile:

```text
☰ Menu
Dashboard
Cards
Charts
Lists
```

Summary cards should stack on mobile.

Charts must resize correctly.

Tables should become horizontally scrollable or card-based on mobile.

---

# 39. PROFESSIONAL UI

Use:

- Modern cards
- Rounded corners
- Subtle shadows
- Clean spacing
- Professional typography
- Food/AI-themed icons
- Smooth hover effects
- Responsive layout
- Consistent buttons
- Clear section headings

Suggested visual theme:

```text
Food + Nature + AI
```

Keep the design professional rather than overly decorative.

---

# 40. ACCESSIBILITY

Implement:

- Semantic HTML
- Proper heading hierarchy
- ARIA labels where necessary
- Keyboard navigation
- Visible focus states
- Accessible chart descriptions
- Good contrast
- Text labels alongside icons

Do not communicate risk only through color.

---

# 41. DASHBOARD JAVASCRIPT

Update:

```text
static/js/dashboard.js
```

Use Fetch/AJAX for dynamic dashboard data where appropriate.

Functions:

```text
loadDashboardStats()
loadRiskDistribution()
loadRecentPredictions()
loadRecommendations()
loadExpiringFoods()
loadCategoryDistribution()
```

Do not make unnecessary API calls.

---

# 42. API RESPONSE FORMAT

Example:

```json
{
    "success": true,
    "statistics": {
        "total_food": 25,
        "high_risk": 5,
        "medium_risk": 8,
        "low_risk": 12,
        "expiring_soon": 3
    }
}
```

Do not hardcode these values.

---

# 43. PERFORMANCE

Optimize:

- Database queries
- Dashboard API calls
- Chart rendering
- Image loading
- CSS/JS loading

Avoid running the ML model just to display dashboard statistics.

Dashboard should read stored predictions from the database.

---

# 44. REFRESH BEHAVIOR

After:

```text
Food added
Prediction generated
Recommendation generated
Food marked used
Waste recorded
```

the dashboard should reflect the updated data.

Use:

```text
Fetch/AJAX
```

or reload the dashboard where appropriate.

---

# 45. ERROR STATE

If dashboard API fails:

```text
Unable to load dashboard data.
Please refresh and try again.
```

Do not show Python traceback.

Log technical errors server-side.

---

# 46. TESTING

Create/update:

```text
tests/test_dashboard.py
```

Test:

```text
Authentication
Dashboard access
User-specific data
Statistics
Risk distribution
Expiring foods
Recent predictions
Recommendations
Empty dashboard
Admin access
Unauthorized admin access
API responses
```

---

# 47. SECURITY TEST

Test:

```text
User A
↓
Dashboard
↓
Only User A data
```

Then:

```text
User B
↓
Dashboard
↓
Only User B data
```

No cross-user data leakage.

---

# 48. FINAL FILE STRUCTURE

Maintain the existing project.

Expected:

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
│   └── waste_record.py
│
├── routes/
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── food_routes.py
│   ├── prediction_routes.py
│   └── recommendation_routes.py
│
├── templates/
│   ├── dashboard.html
│   ├── food_entry.html
│   ├── prediction.html
│   ├── recommendations.html
│   └── admin/
│       └── dashboard.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── script.js
│       └── dashboard.js
│
└── tests/
    ├── test_dashboard.py
    ├── test_prediction.py
    └── test_recommendations.py
```

Do not duplicate files that already exist.

---

# 49. COMPLETE DASHBOARD FLOW

The final system must work as:

```text
LOGIN
  ↓
DASHBOARD
  ↓
┌──────────────────────────────┐
│ Welcome User                 │
├──────────────────────────────┤
│ Total Food                   │
│ High Risk                    │
│ Medium Risk                  │
│ Low Risk                     │
├──────────────────────────────┤
│ Risk Distribution Chart      │
├──────────────────────────────┤
│ Foods Expiring Soon          │
├──────────────────────────────┤
│ Recent AI Predictions        │
├──────────────────────────────┤
│ Smart Recommendations        │
├──────────────────────────────┤
│ Food Category Chart          │
├──────────────────────────────┤
│ Food Used vs Wasted          │
├──────────────────────────────┤
│ Monthly Waste Trend          │
├──────────────────────────────┤
│ Recent Food Entries          │
└──────────────────────────────┘
```

---

# 50. FINAL CHECKLIST

Before completing the dashboard:

[ ] Dashboard route works

[ ] Login protection works

[ ] User name displayed

[ ] Total food count comes from database

[ ] High-risk count comes from latest predictions

[ ] Medium-risk count comes from database

[ ] Low-risk count comes from database

[ ] Expiring foods displayed

[ ] Expired foods handled carefully

[ ] Risk chart works

[ ] Category chart works

[ ] Recent predictions displayed

[ ] Confidence displayed

[ ] Recommendations displayed

[ ] Priority actions displayed

[ ] Recent food entries displayed

[ ] Add Food button works

[ ] Prediction links work

[ ] Recommendation links work

[ ] Reports link works

[ ] Profile link works

[ ] Logout works

[ ] Empty dashboard works

[ ] Admin dashboard works

[ ] Admin authorization works

[ ] User data isolation works

[ ] No hardcoded statistics

[ ] No fake chart data

[ ] Responsive design works

[ ] Accessibility implemented

[ ] Error handling works

[ ] Tests pass

---

# FINAL INSTRUCTION

Implement the complete **DASHBOARD MODULE** for:

**AI FOOD WASTE REDUCTION SYSTEM**

Connect:

**LOGIN → DASHBOARD → FOOD ENTRY → ML PREDICTION → SMART RECOMMENDATIONS → REPORTS**

The dashboard must be fully functional, database-driven, secure, responsive, colorful, professional, and suitable for a college project demonstration.

Do not use fake statistics, fake charts, fake predictions, or fake user data.

After completing this module, leave the project ready for the next modules:

**REPORTS → ADMIN → TESTING → DEPLOYMENT.**
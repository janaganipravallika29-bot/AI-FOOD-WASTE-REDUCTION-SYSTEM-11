# MASTER PROMPT — REPORTS MODULE

You are an expert full-stack Flask developer, database engineer, data analytics engineer, UI/UX designer, and reporting-system developer.

My project title is:

**AI FOOD WASTE REDUCTION SYSTEM**

The following modules are already implemented:

- Professional Frontend
- Flask Backend
- Database
- Login/Signup
- Authentication
- Food Entry
- ML Model
- Prediction
- Smart Recommendations
- Dashboard

Now implement the complete:

# REPORTS MODULE

The Reports module must collect real data from the database and provide the user with a professional analytics and reporting dashboard.

Do NOT use fake statistics or hardcoded chart values.

---

# 1. REPORTS OBJECTIVE

The report flow must be:

```text
LOGIN
   ↓
DASHBOARD
   ↓
REPORTS
   ↓
DATABASE
   ↓
ANALYTICS
   ↓
CHARTS
   ↓
FILTERS
   ↓
SUMMARY
   ↓
FOOD WASTE INSIGHTS
   ↓
EXPORT REPORT
```

The Reports module should help users understand:

- How much food they tracked
- How much food was used
- How much food was wasted
- Waste-risk distribution
- Food categories
- High-risk foods
- Expiring foods
- Prediction history
- Recommendation activity
- Waste trends
- Waste reduction progress

---

# 2. REPORTS PAGE

Create/update:

```text
templates/reports.html
```

Route:

```text
/reports
```

Require authentication:

```python
@login_required
```

A normal user must only see their own data.

---

# 3. REPORT PAGE HEADER

Display:

```text
AI FOOD WASTE REPORTS
```

Subtitle:

```text
Analyze your food records, AI predictions, and waste-reduction progress.
```

Add buttons:

```text
[ + ADD FOOD ]
[ EXPORT REPORT ]
[ PRINT REPORT ]
```

Use the existing project navigation and styling.

---

# 4. REPORT FILTERS

Create a professional filter section:

```text
REPORT FILTERS
```

Filters:

```text
Date Range
Food Category
Waste Risk
Storage Type
```

Date options:

```text
Today
Last 7 Days
Last 30 Days
Last 3 Months
This Year
Custom Range
```

Category:

```text
All
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

Risk:

```text
All
LOW
MEDIUM
HIGH
```

Add:

```text
[ APPLY FILTERS ]
[ RESET ]
```

---

# 5. FILTER URL

Use query parameters where appropriate.

Example:

```text
/reports?start_date=2026-08-01&end_date=2026-08-12&category=Vegetables&risk=HIGH
```

Validate all filter values on the backend.

Do not trust frontend filtering for security.

---

# 6. REPORT SUMMARY CARDS

Create summary cards:

```text
TOTAL FOOD ITEMS
TOTAL QUANTITY TRACKED
TOTAL USED
TOTAL WASTED
HIGH RISK
MEDIUM RISK
LOW RISK
```

All values must come from the database.

Example only:

```text
Total Food Items: 25
Total Quantity: 48 kg
Used: 32 kg
Wasted: 8 kg
High Risk: 5
Medium Risk: 8
Low Risk: 12
```

These numbers are examples and MUST NOT be hardcoded.

---

# 7. WASTE REDUCTION RATE

Calculate the rate using actual tracked data.

If valid usage data exists:

```text
waste_reduction_rate =
used_quantity /
(used_quantity + wasted_quantity)
× 100
```

Display:

```text
WASTE REDUCTION PROGRESS

78%
```

Use the actual project definition if a different waste-reduction metric has already been established.

If insufficient data exists:

```text
Not enough data to calculate waste-reduction progress.
```

Do not invent a percentage.

---

# 8. REPORT OVERVIEW

Create:

```text
REPORT OVERVIEW
```

Display a short dynamically generated summary.

Example:

```text
You tracked 25 food items during the selected period.

5 items currently have a high estimated waste risk.

8 items have a medium estimated waste risk.

Your most frequently tracked category is Vegetables.
```

Generate these statements only when supported by actual data.

---

# 9. WASTE RISK DISTRIBUTION

Create a chart:

```text
WASTE RISK DISTRIBUTION
```

Display:

```text
LOW
MEDIUM
HIGH
```

Use:

```text
Chart.js
```

or the project's existing chart library.

Data must come from the database.

Example API:

```text
/api/reports/risk-distribution
```

Response:

```json
{
    "low": 12,
    "medium": 8,
    "high": 5
}
```

Do not hardcode these values.

---

# 10. FOOD CATEGORY DISTRIBUTION

Create:

```text
FOOD CATEGORY DISTRIBUTION
```

Show the number of food items by category.

Example:

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

Use an appropriate chart such as:

```text
Doughnut
Bar
Pie
```

Use actual database data.

---

# 11. WASTE TREND

Create:

```text
FOOD WASTE TREND
```

Show waste over time.

X-axis:

```text
Date
```

Y-axis:

```text
Wasted Quantity
```

Allow:

```text
Daily
Weekly
Monthly
```

Use real WasteRecord data.

If there is insufficient historical data:

```text
Not enough historical data yet.
```

Do not fabricate previous months.

---

# 12. FOOD USAGE VS WASTE

Create:

```text
FOOD USAGE VS WASTE
```

Show:

```text
USED
WASTED
```

Example:

```text
Used: 32 kg
Wasted: 8 kg
```

Use actual database records.

If food usage tracking has not been recorded, display:

```text
Usage data will appear after you start recording food usage.
```

---

# 13. HIGH-RISK FOOD REPORT

Create:

```text
HIGH WASTE-RISK FOODS
```

Table:

```text
Food
Category
Quantity
Expiry
Risk
Confidence
Action
```

Example:

```text
Tomatoes
Vegetables
2 kg
14 Aug
HIGH
87%
View
```

Only show the user's records.

---

# 14. EXPIRING FOOD REPORT

Create:

```text
FOODS APPROACHING EXPIRY
```

Display:

```text
Food
Expiry Date
Days Remaining
Risk
```

Sort by:

```text
Nearest expiry first
```

Use backend-calculated days remaining.

---

# 15. EXPIRED FOOD REPORT

If expired food exists:

```text
ITEMS PAST RECORDED EXPIRY
```

Display:

```text
Food
Category
Recorded Expiry
Days Past
```

Add notice:

```text
These items have passed their recorded expiry dates.
Follow product labeling and applicable food-safety guidance.
The AI waste-risk score is not a food-safety determination.
```

Do not recommend consuming expired food.

---

# 16. PREDICTION ANALYTICS

Create:

```text
AI PREDICTION ANALYTICS
```

Show:

```text
Total Predictions
LOW Predictions
MEDIUM Predictions
HIGH Predictions
Average Confidence
Latest Model Version
```

Calculate average confidence only from real confidence values.

If the model does not provide confidence:

```text
Confidence data unavailable.
```

Do not invent confidence.

---

# 17. MODEL VERSION REPORT

Display:

```text
AI MODEL INFORMATION
```

Example:

```text
Model Version: 1.0
Predictions Generated: 25
Last Prediction: 12 Aug 2026
```

Use the actual model version from the prediction records.

---

# 18. PREDICTION HISTORY

Create:

```text
PREDICTION HISTORY
```

Table:

```text
Date
Food
Risk
Confidence
Model Version
```

Add pagination.

Show:

```text
10 records per page
```

Allow:

```text
Previous
Next
```

---

# 19. RECOMMENDATION ANALYTICS

Create:

```text
SMART RECOMMENDATION ANALYTICS
```

Show:

```text
Total Recommendations
High Priority
Medium Priority
Low Priority
```

Break down by type:

```text
Meal Planning
Storage
Portion Planning
Freezing
Sharing
Donation
Tracking
```

Use actual Recommendation records.

---

# 20. WASTE REASON ANALYSIS

If WasteRecord contains reason:

Create:

```text
WHY FOOD WAS WASTED
```

Possible reasons:

```text
Expired
Over-purchased
Forgotten
Spoiled
Cooked Too Much
Other
```

Display a chart.

Example:

```text
Expired       10
Over-purchased 5
Forgotten      3
Other          2
```

Use actual database values.

---

# 21. TOP WASTED CATEGORIES

Create:

```text
TOP WASTED FOOD CATEGORIES
```

Calculate categories with the largest recorded wasted quantity.

Example:

```text
Vegetables
Dairy
Fruits
Bakery
```

Sort by:

```text
Wasted quantity DESC
```

Do not create rankings if waste quantities are unavailable.

---

# 22. TOP HIGH-RISK FOODS

Create:

```text
FOODS NEEDING ATTENTION
```

Rank foods by:

```text
Risk
Days Remaining
```

Example:

```text
1. Tomatoes — HIGH — 2 days
2. Milk — HIGH — 1 day
3. Bread — MEDIUM — 3 days
```

Use actual data.

---

# 23. PERSONALIZED INSIGHTS

Create:

```text
AI FOOD WASTE INSIGHTS
```

Generate useful observations from database information.

Examples:

```text
You currently have 4 high-risk food items.

Vegetables are your most frequently tracked food category.

You recorded the highest waste quantity in the Dairy category.

Several food items are approaching their recorded expiry dates.
```

Only display insights supported by data.

Never generate fake insights.

---

# 24. RECOMMENDATION IMPACT

If the system tracks recommendation actions, calculate:

```text
Recommendations Generated
Actions Completed
Food Used After Recommendation
Food Wasted After Recommendation
```

If action tracking is not implemented:

Display:

```text
Recommendation impact tracking will become available
after action tracking is enabled.
```

Do not invent impact percentages.

---

# 25. DATE RANGE ANALYTICS

When the user changes the date range, update:

```text
Summary Cards
Charts
Tables
Insights
```

All report components must use the selected date range.

---

# 26. CUSTOM DATE RANGE

Allow:

```text
Start Date
End Date
```

Validate:

```text
start_date <= end_date
```

If invalid:

```text
Please select a valid date range.
```

Do not allow invalid or malformed dates to reach database queries.

---

# 27. REPORT API

Create/update:

```text
routes/report_routes.py
```

Possible endpoints:

```text
/reports
/api/reports/summary
/api/reports/risk-distribution
/api/reports/category-distribution
/api/reports/waste-trend
/api/reports/usage-vs-waste
/api/reports/predictions
/api/reports/recommendations
/api/reports/waste-reasons
```

Protect all user endpoints with:

```python
@login_required
```

---

# 28. USER DATA SECURITY

Every report query must filter by:

```python
current_user.id
```

Never accept `user_id` from the browser to determine whose report is shown.

User A must never see:

```text
User B's FoodEntry
User B's Prediction
User B's Recommendation
User B's WasteRecord
```

---

# 29. ADMIN REPORTS

Create:

```text
/admin/reports
```

Only authorized admins can access it.

Admin reports may include aggregate:

```text
Total Users
Total Food Items
Total Predictions
Total Recommendations
Total Recorded Waste
Risk Distribution
Category Distribution
Waste Trends
```

Use aggregate information where possible.

Do not expose unnecessary personal data.

---

# 30. ADMIN REPORT APIs

Create:

```text
/api/admin/reports/summary
/api/admin/reports/risk-distribution
/api/admin/reports/category-distribution
/api/admin/reports/waste-trend
```

Protect with admin authorization.

---

# 31. EXPORT CSV

Add:

```text
[ EXPORT CSV ]
```

Export the filtered report data.

Example columns:

```text
Food Name
Category
Quantity
Unit
Purchase Date
Expiry Date
Days Remaining
Risk
Confidence
Model Version
Created Date
```

Use Python's CSV functionality or pandas if already used by the project.

The exported data must respect the current filters.

A normal user can export only their own records.

---

# 32. EXPORT PDF

Add:

```text
[ EXPORT PDF ]
```

Generate a professional PDF report containing:

```text
AI FOOD WASTE REDUCTION SYSTEM

User Report

Report Period

Summary Statistics

Waste Risk Distribution

Food Category Distribution

Waste Trend

High-Risk Foods

Expiring Foods

Recommendations

Waste Records

Generated Date
```

Use a suitable Python PDF library such as:

```text
ReportLab
```

Do not expose sensitive authentication information.

---

# 33. PRINT REPORT

Add:

```text
[ PRINT REPORT ]
```

Use:

```javascript
window.print()
```

Create a print stylesheet:

```text
static/css/print.css
```

Hide:

```text
Sidebar
Navigation
Buttons
Interactive controls
```

when printing.

Keep:

```text
Report title
Statistics
Charts where printable
Tables
Insights
```

---

# 34. REPORT DATE

Display:

```text
Generated on: 12 August 2026
```

Use the current server date/time.

Do not hardcode the date.

---

# 35. REPORT HEADER

For exported reports use:

```text
AI FOOD WASTE REDUCTION SYSTEM

Food Waste Analytics Report
```

Include:

```text
User
Report Period
Generated Date
```

Do not include passwords or authentication tokens.

---

# 36. REPORT FOOTER

Add:

```text
AI Food Waste Reduction System
Generated from recorded application data.
```

Also include:

```text
AI predictions are estimated waste-risk assessments
and are not food-safety determinations.
```

---

# 37. REPORT TABLE PAGINATION

For large datasets use pagination.

Default:

```text
10 records per page
```

Allow:

```text
10
25
50
100
```

Do not load thousands of records unnecessarily into the browser.

---

# 38. SEARCH

Add a search field:

```text
Search food...
```

Search:

```text
Food Name
Category
```

Use backend filtering for large datasets.

---

# 39. SORTING

Allow sorting by:

```text
Date
Food Name
Category
Quantity
Risk
Confidence
Expiry Date
```

Validate sort fields server-side.

Do not insert raw user-provided sort fields directly into SQL.

---

# 40. REPORT DASHBOARD DESIGN

Use a professional layout:

```text
------------------------------------------------
AI FOOD WASTE REPORTS
Analyze your food waste data
------------------------------------------------

[Date Range] [Category] [Risk] [Apply]

------------------------------------------------
| Total Food | Used | Wasted | High Risk       |
------------------------------------------------

------------------------------------------------
| Risk Distribution | Category Distribution    |
------------------------------------------------

------------------------------------------------
| Waste Trend                                      |
------------------------------------------------

------------------------------------------------
| Usage vs Waste | Waste Reasons                  |
------------------------------------------------

------------------------------------------------
HIGH-RISK FOODS
------------------------------------------------

EXPIRING FOODS
------------------------------------------------

AI INSIGHTS
------------------------------------------------

[ EXPORT CSV ] [ EXPORT PDF ] [ PRINT ]
------------------------------------------------
```

---

# 41. COLORS

Use the existing application theme.

Risk status should be visually distinguishable:

```text
LOW
MEDIUM
HIGH
```

But never rely only on color.

Use:

```text
LOW
MEDIUM
HIGH
```

text labels and icons.

---

# 42. RESPONSIVE DESIGN

Desktop:

```text
Two-column charts
```

Tablet:

```text
Flexible cards
```

Mobile:

```text
Single-column layout
```

Tables should be horizontally scrollable or converted into cards.

Filters should stack vertically on mobile.

---

# 43. ACCESSIBILITY

Implement:

- Semantic HTML
- Accessible labels
- Keyboard navigation
- Focus indicators
- Proper headings
- Screen-reader-friendly chart descriptions
- Accessible buttons
- Sufficient contrast

---

# 44. FRONTEND JAVASCRIPT

Create/update:

```text
static/js/reports.js
```

Functions:

```text
loadReportSummary()
loadRiskChart()
loadCategoryChart()
loadWasteTrend()
loadUsageWasteChart()
loadPredictionAnalytics()
loadRecommendationAnalytics()
loadWasteReasons()
applyFilters()
resetFilters()
exportCSV()
exportPDF()
printReport()
```

Use Fetch/AJAX where appropriate.

---

# 45. CHART RENDERING

Use Chart.js if already installed.

Charts:

```text
1. Risk Distribution
2. Category Distribution
3. Waste Trend
4. Used vs Wasted
5. Waste Reasons
6. Recommendation Types
```

Destroy/reuse existing chart instances when filters change to prevent duplicate charts.

---

# 46. EMPTY REPORT STATE

If the user has no records:

Display:

```text
NO REPORT DATA YET

Start adding food items to generate your personalized
food-waste analytics.

[ + ADD FOOD ]
```

Do not display fake charts.

---

# 47. PARTIAL DATA

If only food entries exist but no waste records:

Show available reports:

```text
Food Entries
Risk Predictions
Category Distribution
```

For unavailable sections:

```text
Waste tracking data is not available yet.
```

Do not create fake values.

---

# 48. ERROR HANDLING

Handle:

```text
Invalid date
Database failure
Unauthorized request
Missing data
Export failure
Chart API failure
PDF generation failure
CSV generation failure
```

Show friendly messages:

```text
Unable to load this report.
Please try again later.
```

Do not expose stack traces to users.

---

# 49. PERFORMANCE

Use efficient database queries.

Avoid:

```text
N+1 queries
```

Use:

```text
aggregation
grouping
pagination
indexes
```

where appropriate.

Do not run ML predictions during report generation.

Reports should use stored prediction results.

---

# 50. DATABASE INDEXES

If appropriate, add indexes to:

```text
FoodEntry.user_id
FoodEntry.category
FoodEntry.expiry_date

Prediction.food_entry_id
Prediction.created_at
Prediction.waste_level

Recommendation.food_entry_id
Recommendation.created_at

WasteRecord.user_id
WasteRecord.created_at
WasteRecord.reason
```

Use indexes only where compatible with the existing database.

---

# 51. TESTING

Create/update:

```text
tests/test_reports.py
```

Test:

```text
Authentication
User data isolation
Report summary
Date filters
Category filters
Risk filters
Search
Sorting
Pagination
Risk chart API
Category chart API
Waste trend API
CSV export
PDF export
Print layout
Admin reports
Empty data
Partial data
```

---

# 52. SECURITY TEST

Verify:

```text
User A
   ↓
/reports
   ↓
Only User A data
```

Verify:

```text
User B
   ↓
/reports
   ↓
Only User B data
```

Verify:

```text
Normal User
   ↓
/admin/reports
   ↓
403 / Unauthorized
```

---

# 53. FINAL FILE STRUCTURE

Maintain the existing project structure.

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
│   ├── recommendation_routes.py
│   └── report_routes.py
│
├── templates/
│   ├── dashboard.html
│   ├── food_entry.html
│   ├── prediction.html
│   ├── recommendations.html
│   ├── reports.html
│   └── admin/
│       ├── dashboard.html
│       └── reports.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── print.css
│   │
│   └── js/
│       ├── script.js
│       ├── dashboard.js
│       └── reports.js
│
├── exports/
│   └── .gitkeep
│
└── tests/
    ├── test_dashboard.py
    ├── test_prediction.py
    ├── test_recommendations.py
    └── test_reports.py
```

Do not duplicate existing files.

---

# 54. COMPLETE REPORT FLOW

The completed system must work as:

```text
LOGIN
  ↓
DASHBOARD
  ↓
REPORTS
  ↓
SELECT DATE RANGE
  ↓
SELECT CATEGORY
  ↓
SELECT RISK
  ↓
APPLY FILTERS
  ↓
DATABASE QUERY
  ↓
SUMMARY
  ↓
RISK ANALYTICS
  ↓
CATEGORY ANALYTICS
  ↓
WASTE TREND
  ↓
USAGE VS WASTE
  ↓
HIGH-RISK FOODS
  ↓
EXPIRING FOODS
  ↓
PREDICTION ANALYTICS
  ↓
RECOMMENDATION ANALYTICS
  ↓
WASTE REASONS
  ↓
AI INSIGHTS
  ↓
EXPORT CSV / PDF
```

---

# 55. FINAL CHECKLIST

Before completing the Reports module:

[ ] Reports page created

[ ] Login protection works

[ ] User-specific data isolation works

[ ] Date filters work

[ ] Category filter works

[ ] Risk filter works

[ ] Search works

[ ] Sorting works

[ ] Pagination works

[ ] Summary statistics come from database

[ ] Risk distribution chart works

[ ] Category chart works

[ ] Waste trend works

[ ] Used vs wasted works when data exists

[ ] High-risk report works

[ ] Expiring food report works

[ ] Expired food report works

[ ] Prediction analytics works

[ ] Confidence handled correctly

[ ] Model version displayed

[ ] Recommendation analytics works

[ ] Waste reason analytics works

[ ] Personalized insights use real data

[ ] Empty state works

[ ] Partial data works

[ ] CSV export works

[ ] PDF export works

[ ] Print report works

[ ] Admin reports work

[ ] Admin authorization works

[ ] No fake statistics

[ ] No fake historical data

[ ] No fake confidence

[ ] Responsive design works

[ ] Accessibility implemented

[ ] Error handling works

[ ] Tests pass

---

# FINAL INSTRUCTION

Implement the complete **REPORTS MODULE** for:

**AI FOOD WASTE REDUCTION SYSTEM**

Connect:

**Database → Food Entries → ML Predictions → Smart Recommendations → Waste Records → Analytics → Reports → CSV/PDF Export**

The Reports module must be professional enough for a college project demonstration and fully functional from frontend to Flask backend to database.

Use only real application data.

Never generate fake statistics, fake historical data, fake predictions, or fake confidence scores.

After completing this module, leave the application ready for the next modules:

**ADMIN → TESTING → DEPLOYMENT.**
# MASTER PROMPT — PREDICTION MODULE

You are an expert Flask developer, Machine Learning engineer, database engineer, and professional UI/UX developer.

My project title is:

**AI FOOD WASTE REDUCTION SYSTEM**

The following modules are already implemented:

- Frontend
- Flask backend
- Database
- Login/Signup
- Authentication
- Food Entry
- ML Model

Now implement the complete **PREDICTION MODULE** and connect it with the existing system.

The prediction flow must be:

```text
LOGIN
   ↓
DASHBOARD
   ↓
FOOD ENTRY
   ↓
DATABASE
   ↓
TRAINED ML MODEL
   ↓
PREDICTION
   ↓
LOW / MEDIUM / HIGH
   ↓
CONFIDENCE SCORE
   ↓
EXPLANATION
   ↓
DATABASE
   ↓
PREDICTION PAGE
   ↓
SMART RECOMMENDATIONS
```

Do not create random or fake predictions.

Use the already trained ML model from the ML module.

---

# 1. PREDICTION OBJECTIVE

The prediction module must determine the estimated **food-waste risk** for a food entry.

Possible results:

```text
LOW
MEDIUM
HIGH
```

Example:

```text
Food: Tomatoes
Category: Vegetables
Quantity: 2 kg
Days Remaining: 2 days

Waste Risk: HIGH
Confidence: 87%
```

IMPORTANT:

This is a **food-waste risk prediction**, not a food-safety certification.

Never tell the user that food is definitely safe or unsafe based only on the ML prediction.

---

# 2. PREDICTION PAGE

Create or update:

```text
templates/prediction.html
```

The page must have a professional, modern, colorful design matching the existing AI Food Waste Reduction System.

Page title:

```text
AI FOOD WASTE PREDICTION
```

Subtitle:

```text
Analyze your food data and understand its estimated waste risk.
```

---

# 3. FOOD SUMMARY

At the top display the food information:

```text
Food Name
Category
Quantity
Unit
Purchase Date
Expiry Date
Days Remaining
Storage Type
Temperature
Previous Waste
```

Example:

```text
┌────────────────────────────────────┐
│ 🍅 Tomatoes                        │
│                                    │
│ Category: Vegetables               │
│ Quantity: 2 kg                     │
│ Purchase Date: 10 Aug 2026         │
│ Expiry Date: 14 Aug 2026           │
│ Days Remaining: 2                  │
│ Storage: Refrigerator              │
│ Temperature: 5°C                   │
└────────────────────────────────────┘
```

---

# 4. ANALYZE BUTTON

If prediction has not yet been generated, show:

```text
[ 🤖 ANALYZE WITH AI ]
```

When clicked:

```text
Preparing food data...
Running prediction...
Calculating waste risk...
```

Show a loading animation.

Disable the button while processing to prevent duplicate requests.

---

# 5. PREDICTION ROUTE

Create:

```text
POST /predict/<int:food_id>
```

Use:

```python
@login_required
```

The route must:

1. Verify login.
2. Retrieve food entry.
3. Verify ownership.
4. Calculate current days remaining.
5. Prepare ML features.
6. Load/use the trained model.
7. Generate prediction.
8. Calculate confidence.
9. Generate explanation.
10. Save prediction.
11. Return prediction result.

---

# 6. OWNERSHIP SECURITY

A normal user may only predict their own food.

Verify:

```python
food_entry.user_id == current_user.id
```

If not:

```text
403 Forbidden
```

or a safe not-found response.

Never accept a user ID from the browser and use it for authorization.

Admins may access authorized records according to the existing admin permission system.

---

# 7. FEATURE EXTRACTION

Take the existing FoodEntry record and prepare:

```text
food_category
quantity
days_until_expiry
storage_type
temperature
previous_waste
```

Do not use:

```text
user_id
email
password
username
image filename
```

as ML features.

---

# 8. DAYS REMAINING

Calculate on the backend:

```text
expiry_date - current_date
```

Do not trust a browser-supplied `days_remaining`.

Example:

```text
Today: August 12
Expiry: August 15

Days Remaining = 3
```

---

# 9. MODEL PREDICTION

Use:

```text
ml/models/food_waste_model.joblib
```

or the exact model path used by the existing ML module.

Do NOT retrain the model when the user clicks Analyze.

Correct:

```text
Saved Model
    ↓
Input Features
    ↓
Prediction
```

Incorrect:

```text
Input
 ↓
Train Model
 ↓
Prediction
```

---

# 10. PREDICTION RESULT

The model must return one of:

```text
LOW
MEDIUM
HIGH
```

Example:

```python
prediction = "HIGH"
```

Normalize the result to uppercase before storing/displaying it.

---

# 11. CONFIDENCE SCORE

If the trained model supports:

```python
predict_proba()
```

calculate the probability of the predicted class.

Example:

```text
0.874
```

Display:

```text
87.4%
```

Store the numeric confidence value in the database.

Do not fabricate a confidence value.

If the model does not support probability estimates, do not invent one. Instead display an appropriate message such as:

```text
Confidence score unavailable for this model.
```

---

# 12. PREDICTION DATABASE

Use the existing `Prediction` model/table.

Required information:

```text
id
food_entry_id
waste_level
confidence
model_version
created_at
```

When prediction is generated:

```text
Food Entry
     ↓
Prediction
     ↓
Database
```

Example:

```text
food_entry_id = 25
waste_level = HIGH
confidence = 87.4
model_version = 1.0
```

---

# 13. MODEL VERSION

Read the model version from the ML configuration/metadata.

Example:

```text
Model Version: 1.0
```

Do not hardcode different versions in multiple files.

Maintain one source of truth for the model version.

---

# 14. PREDICTION HISTORY

If the same food is analyzed multiple times, preserve prediction history where the existing database design supports it.

Display:

```text
Prediction History
```

Example:

```text
Date          Risk       Confidence
12 Aug 2026   HIGH       87%
11 Aug 2026   MEDIUM     72%
```

This can later be used for reports.

---

# 15. RESULT CARD

After prediction, show a large result card:

```text
┌──────────────────────────────────┐
│       AI WASTE RISK              │
│                                  │
│             HIGH                 │
│                                  │
│       Confidence: 87%            │
│                                  │
│      Model Version: 1.0          │
└──────────────────────────────────┘
```

Use visual styling that clearly distinguishes LOW, MEDIUM, and HIGH.

Do not depend only on color.

Include text labels and icons.

---

# 16. LOW RISK

If:

```text
LOW
```

display:

```text
LOW WASTE RISK
```

Example explanation:

```text
The current food information indicates a relatively lower
estimated risk of waste.
```

Do not say:

```text
This food is completely safe.
```

---

# 17. MEDIUM RISK

If:

```text
MEDIUM
```

display:

```text
MEDIUM WASTE RISK
```

Example:

```text
The food has some factors that may increase the likelihood
of waste. Consider planning its use soon.
```

---

# 18. HIGH RISK

If:

```text
HIGH
```

display:

```text
HIGH WASTE RISK
```

Example:

```text
The current information indicates a higher estimated
likelihood of food waste. Consider prioritizing its use
or taking appropriate waste-reduction actions.
```

Do not claim the food is spoiled.

---

# 19. EXPLANATION SECTION

Create:

```text
WHY THIS RESULT?
```

Display factors based on actual food data.

Example:

```text
Why is the risk high?

• Only 2 days remain before expiry.
• Previous waste amount is relatively high.
• The current storage information was considered.
```

Do not claim that a particular feature caused the ML prediction unless the explanation method supports that claim.

Use careful wording such as:

```text
Factors considered in this estimate:
```

---

# 20. FACTORS CARD

Create a card:

```text
FACTORS CONSIDERED
```

Show:

```text
⏳ Days Remaining: 2
📦 Quantity: 2 kg
🏷 Category: Vegetables
❄ Storage: Refrigerator
🌡 Temperature: 5°C
♻ Previous Waste: 0.8 kg
```

This allows users to understand the information supplied to the model.

---

# 21. PREDICTION STATUS

Display:

```text
AI ANALYSIS COMPLETE
```

After successful prediction.

If prediction fails:

```text
AI ANALYSIS FAILED
```

with:

```text
Please try again later.
```

Do not expose Python exceptions.

---

# 22. ERROR HANDLING

Handle:

```text
Food entry not found
Unauthorized food entry
Model file missing
Invalid ML input
Database error
Prediction error
Missing required feature
```

Example:

```text
AI prediction is temporarily unavailable.
Please try again later.
```

Log technical details server-side.

---

# 23. API RESPONSE

If the project uses AJAX/Fetch, return:

```json
{
    "success": true,
    "prediction": {
        "risk_level": "HIGH",
        "confidence": 87.4,
        "model_version": "1.0"
    }
}
```

Error:

```json
{
    "success": false,
    "message": "Prediction could not be generated."
}
```

Do not expose internal exception details.

---

# 24. FRONTEND JAVASCRIPT

Update:

```text
static/js/script.js
```

Create:

```text
analyzeFood(foodId)
```

Function flow:

```text
Click Analyze
      ↓
Disable Button
      ↓
Show Loading
      ↓
POST /predict/<food_id>
      ↓
Receive JSON
      ↓
Display Prediction
      ↓
Display Confidence
      ↓
Display Explanation
      ↓
Enable Buttons
```

Use `fetch()` if the existing application uses AJAX.

Do not reload the entire page unnecessarily.

---

# 25. PREDICTION PAGE URL

Use:

```text
/prediction/<int:food_id>
```

Example:

```text
/prediction/25
```

The route must verify ownership before showing the food information.

---

# 26. VIEW EXISTING PREDICTION

If a prediction already exists:

```text
/prediction/25
```

should display the latest prediction.

Example:

```text
Latest AI Prediction
HIGH
87%
```

Provide:

```text
[ ANALYZE AGAIN ]
```

if the application supports re-analysis.

---

# 27. RE-ANALYSIS

If the user changes important food information such as:

```text
Quantity
Expiry Date
Storage Type
Temperature
Previous Waste
```

allow a new prediction.

Save a new prediction record or update the existing one according to the established project design.

Preserve history if reports require it.

---

# 28. DASHBOARD INTEGRATION

After prediction, update the dashboard.

Display:

```text
Total Predictions
Low Risk
Medium Risk
High Risk
```

These values must be calculated from the database.

Example:

```text
Total Analyses: 20
Low Risk: 8
Medium Risk: 7
High Risk: 5
```

Never hardcode these numbers.

---

# 29. DASHBOARD RECENT PREDICTIONS

Add:

```text
RECENT AI ANALYSIS
```

Example:

```text
Food          Risk       Confidence
Tomatoes      HIGH       87%
Milk          MEDIUM     74%
Rice          LOW        92%
```

Only show the logged-in user's predictions on the normal user dashboard.

---

# 30. CHART

Create/update the dashboard chart:

```text
Food Waste Risk Distribution
```

Show:

```text
LOW
MEDIUM
HIGH
```

Use actual database values.

Use Chart.js if already included in the project.

---

# 31. NOTIFICATION

After a HIGH prediction, show a non-alarming notification:

```text
⚠ High waste-risk estimate detected.
Consider prioritizing this food for use or exploring
waste-reduction options.
```

For MEDIUM:

```text
Food has a medium estimated waste risk.
Consider planning its use soon.
```

For LOW:

```text
Food currently has a low estimated waste risk.
Continue monitoring its expiry and storage.
```

---

# 32. RECOMMENDATIONS BUTTON

After prediction, show:

```text
[ VIEW SMART RECOMMENDATIONS ]
```

Link to:

```text
/recommendations/<food_id>
```

The recommendation module will be implemented separately.

Do not put the complete recommendation engine inside the prediction module.

---

# 33. SAVE ACTIVITY

If an Activity model already exists, create:

```text
AI_PREDICTION
```

Example:

```text
AI prediction generated for Tomatoes: HIGH
```

Associate it with the logged-in user.

Do not store passwords or other sensitive authentication data in activity logs.

---

# 34. PREDICTION SECURITY

Make sure:

```text
User A
```

cannot access:

```text
/prediction/<User B's food_id>
```

through manually changing the URL.

Always verify ownership server-side.

---

# 35. ADMIN VIEW

Create/update:

```text
/admin/predictions
```

Admin can see:

```text
User
Food
Risk
Confidence
Model Version
Date
```

Admin statistics:

```text
Total Predictions
LOW
MEDIUM
HIGH
Average Confidence
Current Model Version
```

Do not expose private user information unnecessarily.

---

# 36. REPORT DATA

Make prediction data available for the Reports module.

Required fields:

```text
food
category
risk
confidence
date
model_version
```

Reports can later calculate:

```text
Total AI Analyses
High Risk Percentage
Medium Risk Percentage
Low Risk Percentage
```

---

# 37. PREDICTION PAGE DESIGN

Use a professional layout:

```text
------------------------------------------------
          AI FOOD WASTE PREDICTION
------------------------------------------------

Food Summary
┌──────────────────────────────────────────────┐
│ 🍅 Tomatoes                                  │
│ Category: Vegetables                         │
│ Quantity: 2 kg                               │
│ Expiry: 14 Aug 2026                          │
│ Days Remaining: 2                            │
└──────────────────────────────────────────────┘

                 AI RESULT

┌──────────────────────────────────────────────┐
│              WASTE RISK                     │
│                                              │
│                  HIGH                        │
│                                              │
│             Confidence: 87%                  │
│             Model: 1.0                       │
└──────────────────────────────────────────────┘

Factors Considered
• Days Remaining: 2
• Quantity: 2 kg
• Storage: Refrigerator
• Previous Waste: 0.8 kg

[ VIEW SMART RECOMMENDATIONS ]

[ BACK TO DASHBOARD ]
------------------------------------------------
```

---

# 38. RESPONSIVE DESIGN

The prediction page must work on:

```text
Desktop
Laptop
Tablet
Mobile
```

Desktop:

```text
Food Summary | Prediction Result
              |
              Factors
```

Mobile:

```text
Food Summary
     ↓
Prediction
     ↓
Factors
     ↓
Recommendations
```

---

# 39. ACCESSIBILITY

Use:

- Semantic HTML
- Labels
- Keyboard navigation
- Accessible buttons
- Clear focus states
- Text labels
- Meaningful error messages
- Good contrast

Do not use only green/yellow/red colors to communicate LOW/MEDIUM/HIGH.

---

# 40. LOADING ANIMATION

While predicting:

```text
🤖 AI ANALYZING...

Processing food information...
```

Use a simple CSS animation.

Do not make the loading message claim a technical step that is not actually happening.

---

# 41. MODEL LIMITATION NOTICE

Add near the result:

```text
AI Prediction Notice

This result is an estimated food-waste risk based on the
information provided and the trained model. It is not a
guarantee of food quality or safety.
```

This notice must remain visible.

---

# 42. TEST CASES

Test:

### Test 1 — Normal prediction

```text
Login
↓
Food Entry
↓
Analyze
↓
Prediction displayed
↓
Prediction saved
```

### Test 2 — Not logged in

```text
Open /prediction/1
↓
Redirect to /login
```

### Test 3 — Unauthorized

```text
User A
↓
User B food ID
↓
403 / Not Found
```

### Test 4 — Model missing

Temporarily remove the model file.

Verify:

```text
Controlled error
```

instead of a server traceback.

### Test 5 — Invalid input

Verify the prediction is rejected safely.

### Test 6 — Re-analysis

Run prediction again and verify prediction history behaves according to the database design.

---

# 43. TESTING FILE

Create/update:

```text
tests/test_prediction.py
```

Test:

```text
Authentication
Ownership
Prediction route
Model loading
Prediction result
Confidence
Database save
Invalid input
Error handling
```

---

# 44. FINAL FILE STRUCTURE

Maintain the existing project structure.

Expected relevant files:

```text
AI_Food_Waste_Reduction_System/
│
├── app.py
├── requirements.txt
│
├── models/
│   ├── user.py
│   ├── food_entry.py
│   └── prediction.py
│
├── routes/
│   ├── auth_routes.py
│   ├── food_routes.py
│   └── prediction_routes.py
│
├── ml/
│   ├── models/
│   │   └── food_waste_model.joblib
│   ├── predict.py
│   └── explanation.py
│
├── templates/
│   ├── food_entry.html
│   ├── prediction.html
│   └── dashboard.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── tests/
    └── test_prediction.py
```

Do not duplicate files that already exist.

---

# 45. COMPLETE FINAL FLOW

The completed system must work as:

```text
USER LOGIN
     ↓
USER DASHBOARD
     ↓
ADD FOOD
     ↓
FOOD ENTRY DATABASE
     ↓
CLICK "ANALYZE WITH AI"
     ↓
FLASK PREDICTION ROUTE
     ↓
VERIFY USER OWNERSHIP
     ↓
EXTRACT FOOD FEATURES
     ↓
CALCULATE DAYS REMAINING
     ↓
LOAD TRAINED ML MODEL
     ↓
GENERATE PREDICTION
     ↓
LOW / MEDIUM / HIGH
     ↓
CALCULATE CONFIDENCE
     ↓
GENERATE FACTOR EXPLANATION
     ↓
SAVE PREDICTION
     ↓
DISPLAY RESULT
     ↓
VIEW SMART RECOMMENDATIONS
     ↓
DASHBOARD
     ↓
REPORTS
```

---

# 46. FINAL CHECKLIST

Before completing the module verify:

[ ] Prediction page works

[ ] Prediction route works

[ ] Login required

[ ] Food ownership verified

[ ] Food data loaded from database

[ ] Days remaining calculated by backend

[ ] ML model loaded correctly

[ ] No random prediction

[ ] LOW/MEDIUM/HIGH returned

[ ] Confidence calculated from model probability when supported

[ ] No fake confidence

[ ] Model version stored

[ ] Prediction saved to database

[ ] Prediction history works

[ ] Explanation uses actual input information

[ ] Dashboard statistics update

[ ] Recent predictions appear

[ ] Admin prediction page works

[ ] Recommendation button works

[ ] Error handling works

[ ] Unauthorized access blocked

[ ] Loading state works

[ ] Mobile design works

[ ] Accessibility implemented

[ ] Tests pass

[ ] Food safety disclaimer displayed

---

# FINAL INSTRUCTION

Implement the complete **PREDICTION MODULE** for the **AI FOOD WASTE REDUCTION SYSTEM**.

Connect the existing:

**Food Entry + Database + Trained ML Model + Flask Backend**

to produce a real:

**LOW / MEDIUM / HIGH food-waste risk prediction**

with:

**Confidence + Explanation + Database Storage + Dashboard Integration + Recommendation Link + Admin Support + Security + Testing.**

Do not create fake predictions, fake confidence scores, or fake statistics.

After completing this module, the project must be ready for the next module:

**SMART RECOMMENDATIONS.**
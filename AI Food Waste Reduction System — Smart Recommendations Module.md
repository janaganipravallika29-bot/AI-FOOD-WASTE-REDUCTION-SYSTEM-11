# MASTER PROMPT — SMART RECOMMENDATIONS MODULE

You are an expert Flask developer, AI/ML engineer, database engineer, and professional UI/UX developer.

My project title is:

**AI FOOD WASTE REDUCTION SYSTEM**

The following modules are already implemented:

- Professional frontend
- Flask backend
- Database
- Login/Signup
- Authentication
- Food Entry
- ML Model
- Prediction
- Prediction database
- Dashboard

Now implement the complete:

**SMART RECOMMENDATIONS MODULE**

The recommendation system must use the actual food-entry information and prediction result.

The flow must be:

```text
FOOD ENTRY
    ↓
DATABASE
    ↓
ML PREDICTION
    ↓
LOW / MEDIUM / HIGH
    ↓
RECOMMENDATION ENGINE
    ↓
SMART ACTIONS
    ↓
RECOMMENDATION PAGE
    ↓
DASHBOARD
    ↓
REPORTS
```

Do not create random recommendations.

---

# 1. PURPOSE

The recommendation system should help users reduce food waste by suggesting practical actions based on:

```text
Food Name
Food Category
Quantity
Expiry Date
Days Remaining
Storage Type
Temperature
Previous Waste
Waste Risk
Prediction Confidence
```

Examples of recommendation categories:

```text
Prioritize Consumption
Storage Guidance
Meal Planning
Portion Planning
Sharing / Donation
Freezing
Recipe Ideas
Waste Tracking
```

---

# 2. IMPORTANT SAFETY RULE

Recommendations must not claim that food is safe or unsafe merely because of the AI prediction.

The system predicts:

**WASTE RISK**

not:

**FOOD SAFETY**

For expired or potentially spoiled food, display cautious guidance such as:

```text
This item has passed its entered expiry date. Follow the product
label and applicable food-safety guidance before deciding what to do.
When in doubt, discard it safely.
```

Do not instruct users to consume food that may be unsafe.

---

# 3. RECOMMENDATION ENGINE

Create:

```text
ml/
└── recommendation_engine.py
```

The engine should accept:

```text
food_entry
prediction
```

and return a structured list of recommendations.

Conceptually:

```python
generate_recommendations(food_entry, prediction)
```

Return:

```python
[
    {
        "type": "PRIORITY",
        "title": "...",
        "description": "...",
        "priority": "HIGH"
    }
]
```

---

# 4. RECOMMENDATION TYPES

Use these categories:

```text
PRIORITY
STORAGE
MEAL_PLANNING
PORTION_CONTROL
FREEZING
SHARING
DONATION
TRACKING
```

Do not generate irrelevant recommendations.

---

# 5. RISK-BASED RECOMMENDATIONS

## LOW RISK

If:

```text
risk = LOW
```

recommendations can include:

```text
Continue monitoring expiry date.
Use normal meal planning.
Maintain appropriate storage.
Avoid buying more than needed.
```

Example:

```text
Low waste risk

Your food currently has a lower estimated waste risk.
Continue monitoring the expiry date and plan meals around
the quantity you have.
```

---

# 6. MEDIUM RISK

If:

```text
risk = MEDIUM
```

recommend:

```text
Prioritize this food in upcoming meals.
Review the quantity you have.
Plan portions.
Monitor expiry closely.
Consider freezing where appropriate and where compatible
with the food/product instructions.
```

Example:

```text
Medium waste risk

Consider using this food in your next few meals and avoid
purchasing additional quantities until the current stock is used.
```

---

# 7. HIGH RISK

If:

```text
risk = HIGH
```

recommend:

```text
Prioritize use soon.
Plan meals around the item.
Consider appropriate storage/freezing where suitable.
Consider sharing/donation where appropriate and legally permitted.
Avoid buying additional quantities.
```

Example:

```text
High waste risk

Prioritize this food when planning your next meals.
If it is suitable for freezing, consider freezing it according
to the product's storage guidance.
```

Do not say:

```text
Eat immediately
```

if the item may be expired.

---

# 8. DAYS-UNTIL-EXPIRY RULES

Use backend-calculated:

```text
days_until_expiry
```

Rules:

### More than 7 days

```text
Normal planning
Monitor stock
Avoid over-purchasing
```

### 4–7 days

```text
Consider including it in upcoming meals
```

### 1–3 days

```text
Prioritize use
Plan meals
Consider appropriate preservation
```

### 0 days

```text
Check product labeling and applicable food-safety guidance
```

### Less than 0

```text
Expired-item caution
```

Do not recommend consumption.

---

# 9. EXPIRY WARNING

If:

```text
days_until_expiry < 0
```

display prominently:

```text
⚠ EXPIRY DATE PASSED
```

Recommendation:

```text
This item has passed its entered expiry date. Do not rely on the
AI waste-risk score to determine whether it is safe to consume.
Follow the product label and applicable food-safety guidance.
```

---

# 10. FOOD CATEGORY RECOMMENDATIONS

Create category-specific recommendation logic.

Categories:

```text
Vegetables
Fruits
Dairy
Grains
Meat
Bakery
Beverages
Cooked Food
Other
```

---

# 11. VEGETABLE RECOMMENDATIONS

For vegetables:

```text
Meal planning
Appropriate refrigeration
Use in soups/curries where suitable
Portion planning
Freezing where suitable
```

Example:

```text
Try planning your next meal around the vegetables you already have
before purchasing more.
```

Avoid giving food-safety claims.

---

# 12. FRUIT RECOMMENDATIONS

For fruits:

```text
Prioritize ripe fruit
Meal planning
Smoothies/recipes where appropriate
Appropriate storage
Freezing where suitable
```

Example:

```text
Plan a meal or snack that uses the fruit you already have
before buying additional fruit.
```

---

# 13. DAIRY RECOMMENDATIONS

For dairy:

```text
Monitor expiry/use-by information
Maintain appropriate refrigeration
Avoid purchasing excess quantity
Use planned portions
```

Do not provide unsafe storage instructions.

---

# 14. GRAINS RECOMMENDATIONS

For grains:

```text
Store appropriately
Track quantity
Avoid bulk purchases beyond expected usage
Use older stock first where appropriate
```

---

# 15. BAKERY RECOMMENDATIONS

For bakery items:

```text
Plan consumption
Store according to product instructions
Freeze where suitable
Avoid buying excessive quantities
```

---

# 16. MEAT RECOMMENDATIONS

For meat:

Use especially cautious language.

Recommend:

```text
Follow package storage instructions.
Monitor the product's use-by date.
Use or preserve according to appropriate food-safety guidance.
```

Do not provide unsafe instructions for handling expired meat.

---

# 17. COOKED FOOD RECOMMENDATIONS

For cooked food:

```text
Track preparation date
Follow appropriate storage guidance
Plan portions
Avoid preparing excessive quantities
```

Do not give a universal safe-storage time unless the application is explicitly configured with a validated food-safety source.

---

# 18. QUANTITY-BASED RECOMMENDATIONS

If quantity is unusually high relative to the user's previous waste or expected usage, show:

```text
You have a relatively large quantity recorded.
Consider planning several meals or portions before purchasing more.
```

Do not assume a universal serving size.

---

# 19. PREVIOUS WASTE BASED RECOMMENDATIONS

If:

```text
previous_waste > 0
```

show:

```text
Previous waste detected

Your previous records indicate that some of this type/quantity
was wasted before. Consider buying a smaller quantity next time
or planning its use before purchasing more.
```

Do not shame the user.

---

# 20. STORAGE RECOMMENDATION

Use the existing:

```text
storage_type
temperature
```

to provide general guidance.

Examples:

```text
Refrigerator
```

```text
Continue following the product's recommended refrigeration
instructions.
```

For:

```text
Room Temperature
```

```text
Check whether the product label recommends room-temperature
storage and follow the manufacturer's instructions.
```

Do not invent precise temperature requirements for every food.

---

# 21. MEAL PLANNING

Create a recommendation:

```text
🍽 MEAL PLANNING
```

Example:

```text
Plan your next meal around this food to help use existing stock
before purchasing more.
```

If food category is known, make the suggestion category-specific.

---

# 22. PORTION CONTROL

Create:

```text
📦 PORTION PLANNING
```

Example:

```text
Divide the available quantity into planned portions so you can
track how much is being used.
```

Do not prescribe medically specific serving sizes.

---

# 23. FREEZING RECOMMENDATION

Only recommend freezing where it is reasonably applicable.

Example:

```text
❄ FREEZING OPTION

If this product is suitable for freezing, consider freezing an
unused portion according to the product's instructions.
```

Never recommend freezing expired food.

---

# 24. SHARING RECOMMENDATION

If quantity is high and the item is not expired:

```text
🤝 SHARING OPTION

If you have more than you expect to use, consider sharing
appropriate food with family, friends, or neighbors while it
is still suitable for sharing.
```

---

# 25. DONATION RECOMMENDATION

If appropriate:

```text
❤️ DONATION OPTION

If this food is suitable for donation, consider contacting a
local food-support organization and follow its acceptance,
packaging, and safety requirements.
```

Do not recommend donating:

```text
Expired food
Food with uncertain condition
Food that may be unsafe
```

---

# 26. RECIPE SUGGESTIONS

Create a simple recipe suggestion system based on category.

Examples:

Vegetables:

```text
Vegetable curry
Soup
Stir-fry
```

Fruits:

```text
Fruit bowl
Smoothie
Fruit-based breakfast
```

Bread:

```text
Toast
Sandwich
Bread-based meal
```

Rice:

```text
Fried rice
Rice bowl
```

Do not claim that a recipe makes unsafe or spoiled food safe.

---

# 27. RECOMMENDATION PRIORITY

Each recommendation must have:

```text
HIGH
MEDIUM
LOW
```

Example:

```text
HIGH
Prioritize use soon.
```

```text
MEDIUM
Plan the item into an upcoming meal.
```

```text
LOW
Continue monitoring the expiry date.
```

---

# 28. RECOMMENDATION SCORE

Optionally calculate a simple priority score using:

```text
days_until_expiry
waste_risk
quantity
previous_waste
```

But do not confuse this with the ML model's confidence.

Keep separate:

```text
ML Confidence
```

and:

```text
Recommendation Priority
```

---

# 29. DATABASE MODEL

Use the existing `Recommendation` model if available.

Required fields:

```text
id
food_entry_id
prediction_id
type
title
description
priority
created_at
```

If the project already has a recommendation table, extend it instead of creating a duplicate.

---

# 30. DATABASE RELATIONSHIP

Maintain:

```text
FoodEntry
   ↓
Prediction
   ↓
Recommendation
```

A recommendation must reference the correct:

```text
food_entry_id
prediction_id
```

---

# 31. RECOMMENDATION ROUTE

Create:

```text
GET /recommendations/<int:food_id>
```

Use:

```python
@login_required
```

Verify:

```text
food_entry.user_id == current_user.id
```

before showing recommendations.

---

# 32. GENERATE RECOMMENDATIONS ROUTE

Create:

```text
POST /recommendations/<int:food_id>/generate
```

Flow:

```text
Food ID
 ↓
Get FoodEntry
 ↓
Verify User
 ↓
Get Latest Prediction
 ↓
Recommendation Engine
 ↓
Generate Recommendations
 ↓
Save Recommendations
 ↓
Return Results
```

---

# 33. LATEST PREDICTION

The recommendation engine should use the latest prediction for the selected food.

Do not use an unrelated prediction from another food entry.

Example:

```text
food_id = 25
      ↓
latest prediction WHERE food_entry_id = 25
```

---

# 34. RECOMMENDATION PAGE

Create/update:

```text
templates/recommendations.html
```

Title:

```text
SMART FOOD WASTE RECOMMENDATIONS
```

Subtitle:

```text
Personalized actions based on your food information and AI waste-risk estimate.
```

---

# 35. PAGE STRUCTURE

Use:

```text
Food Summary
      ↓
AI Risk Summary
      ↓
Priority Action
      ↓
Smart Recommendations
      ↓
Meal Planning
      ↓
Storage Guidance
      ↓
Sharing/Donation
      ↓
Waste Reduction Tips
```

---

# 36. AI RISK SUMMARY

Display:

```text
Current Risk: HIGH
Confidence: 87%
Days Remaining: 2
```

Then:

```text
Based on the information provided, this food currently has a
higher estimated risk of becoming waste.
```

---

# 37. PRIORITY ACTION CARD

Create a highlighted card:

```text
┌──────────────────────────────────────┐
│ ⚡ PRIORITY ACTION                   │
│                                      │
│ Plan to use this food in an          │
│ upcoming meal.                       │
│                                      │
│ Priority: HIGH                       │
└──────────────────────────────────────┘
```

This should be generated based on actual food data.

---

# 38. RECOMMENDATION CARDS

Each recommendation should appear as a card:

```text
┌──────────────────────────────────────┐
│ 🍽 MEAL PLANNING                     │
│                                      │
│ Plan an upcoming meal around this    │
│ food to help use your current stock. │
│                                      │
│ Priority: HIGH                       │
└──────────────────────────────────────┘
```

Use icons, titles, descriptions, and priority labels.

---

# 39. NUMBER OF RECOMMENDATIONS

Generate approximately:

```text
3–6
```

useful recommendations.

Do not overwhelm the user.

Do not generate duplicate recommendations.

---

# 40. DUPLICATE PREVENTION

Before saving recommendations, prevent exact duplicate recommendations for the same food/prediction.

Possible approach:

```text
food_entry_id
prediction_id
type
```

Use this combination where appropriate.

---

# 41. RECOMMENDATION REFRESH

If a new prediction is generated:

```text
New Prediction
      ↓
New Recommendation Set
```

The recommendations should correspond to the latest prediction.

Keep history if required by the reports design.

---

# 42. DASHBOARD INTEGRATION

Add:

```text
SMART RECOMMENDATIONS
```

to the dashboard.

Show:

```text
High Priority Actions
Foods Expiring Soon
Recommended Actions
```

Example:

```text
⚠ 3 foods need attention

Tomatoes — High
Milk — Medium
Bread — Medium
```

Only show the current user's information.

---

# 43. NOTIFICATIONS

Add dashboard notification cards.

Examples:

```text
⚠ Tomatoes have a high estimated waste risk.
```

```text
⏳ Milk is approaching its entered expiry date.
```

```text
💡 You have several foods that could be prioritized in upcoming meals.
```

Do not create alarming or unsafe messages.

---

# 44. SMART RECOMMENDATION BUTTONS

Add actions where appropriate:

```text
[ PLAN MEAL ]
[ VIEW FOOD ]
[ VIEW PREDICTION ]
[ MARK AS USED ]
[ SHARE ]
```

If a button is not actually implemented, do not create a fake button.

---

# 45. MARK AS USED

If implementing:

```text
POST /food/<food_id>/used
```

allow the user to mark the food as:

```text
USED
```

This can later improve analytics.

Do not automatically assume the food was used.

---

# 46. WASTE TRACKING

Allow the user to optionally record:

```text
Used Quantity
Wasted Quantity
Reason
```

Possible waste reasons:

```text
Expired
Over-purchased
Forgotten
Spoiled
Cooked too much
Other
```

This data can later improve reports and future ML training.

---

# 47. WASTE RECORD DATABASE

If implementing waste tracking, create/use:

```text
WasteRecord
```

Fields:

```text
id
food_entry_id
user_id
quantity
unit
reason
created_at
```

Do not mix waste records with predictions.

---

# 48. FUTURE ML FEEDBACK

If a user marks:

```text
USED
```

or:

```text
WASTED
```

store the event.

This can later be used as real feedback for improving the ML model.

Do not automatically retrain the production model from user feedback.

---

# 49. ADMIN VIEW

Create/update:

```text
/admin/recommendations
```

Admin can view aggregate information such as:

```text
Recommendation Type
Priority
Food Category
Number Generated
```

Avoid exposing unnecessary personal information.

---

# 50. REPORT INTEGRATION

Reports should be able to calculate:

```text
Recommendations Generated
High Priority Recommendations
Medium Priority Recommendations
Low Priority Recommendations
```

Also:

```text
Food Used
Food Wasted
Waste Reduction Actions
```

where those events exist in the database.

---

# 51. FRONTEND JAVASCRIPT

Update:

```text
static/js/script.js
```

Create:

```text
generateRecommendations(foodId)
```

Flow:

```text
Click Generate
     ↓
Loading
     ↓
POST request
     ↓
Receive recommendations
     ↓
Display cards
```

Do not refresh the entire page unnecessarily.

---

# 52. LOADING STATE

Show:

```text
🤖 Generating smart recommendations...
```

Use a spinner.

Disable the button while processing.

---

# 53. ERROR HANDLING

Handle:

```text
Food not found
Unauthorized user
Prediction not found
Database error
Recommendation generation error
Invalid food ID
```

Display:

```text
Unable to generate recommendations right now.
Please try again later.
```

Do not expose technical errors.

---

# 54. SECURITY

Ensure:

```text
User A
```

cannot access:

```text
/recommendations/User B's food
```

Verify ownership server-side.

Never trust:

```text
user_id
```

from the frontend.

---

# 55. RESPONSIVE DESIGN

Desktop:

```text
Food Summary | AI Risk
----------------------
Recommendation Cards
Recommendation Cards
```

Mobile:

```text
Food Summary
     ↓
AI Risk
     ↓
Priority Action
     ↓
Recommendations
```

Ensure cards work correctly on small screens.

---

# 56. ACCESSIBILITY

Use:

- Semantic HTML
- Clear headings
- Accessible buttons
- Keyboard navigation
- Focus states
- Text labels
- Icons with accessible meaning
- Good contrast

Do not rely only on color for priority.

---

# 57. TESTING

Create/update:

```text
tests/test_recommendations.py
```

Test:

```text
User authentication
Food ownership
Prediction existence
LOW recommendation generation
MEDIUM recommendation generation
HIGH recommendation generation
Expired food handling
Category recommendations
Duplicate prevention
Database save
Recommendation retrieval
```

---

# 58. TEST EXAMPLE

Input:

```text
Food:
Tomatoes

Category:
Vegetables

Quantity:
2 kg

Days Remaining:
2

Storage:
Refrigerator

Previous Waste:
0.5 kg

Risk:
HIGH
```

Expected recommendation types may include:

```text
PRIORITY
MEAL_PLANNING
STORAGE
PORTION_CONTROL
```

The exact recommendations should be generated from the rules and available data.

---

# 59. EXPIRED FOOD TEST

Input:

```text
days_until_expiry = -1
```

Expected:

```text
EXPIRY WARNING
```

Do NOT generate:

```text
Eat this immediately
Freeze this now
Donate this
```

Instead provide cautious guidance based on product labeling and applicable food-safety guidance.

---

# 60. FINAL FILE STRUCTURE

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
│   ├── food_routes.py
│   ├── prediction_routes.py
│   └── recommendation_routes.py
│
├── ml/
│   ├── models/
│   │   └── food_waste_model.joblib
│   ├── predict.py
│   ├── explanation.py
│   └── recommendation_engine.py
│
├── templates/
│   ├── dashboard.html
│   ├── food_entry.html
│   ├── prediction.html
│   └── recommendations.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── tests/
    ├── test_ml.py
    ├── test_prediction.py
    └── test_recommendations.py
```

Do not duplicate existing files.

---

# 61. COMPLETE SYSTEM FLOW

The final working flow must be:

```text
LOGIN
  ↓
DASHBOARD
  ↓
ADD FOOD
  ↓
FOOD ENTRY
  ↓
DATABASE
  ↓
AI PREDICTION
  ↓
LOW / MEDIUM / HIGH
  ↓
CONFIDENCE
  ↓
SMART RECOMMENDATION ENGINE
  ↓
PRIORITY ACTION
  ↓
MEAL PLANNING
  ↓
STORAGE GUIDANCE
  ↓
PORTION PLANNING
  ↓
SHARING / DONATION WHEN APPROPRIATE
  ↓
WASTE TRACKING
  ↓
DASHBOARD
  ↓
REPORTS
```

---

# 62. FINAL CHECKLIST

Before completing the module:

[ ] Recommendation engine created

[ ] Uses actual food entry data

[ ] Uses latest prediction

[ ] LOW recommendations work

[ ] MEDIUM recommendations work

[ ] HIGH recommendations work

[ ] Expiry rules work

[ ] Expired food warning works

[ ] Category-based recommendations work

[ ] Quantity-based recommendations work

[ ] Previous-waste recommendations work

[ ] Storage guidance works

[ ] Meal planning suggestions work

[ ] Portion planning works

[ ] Freezing suggestions are conditional

[ ] Sharing suggestions are conditional

[ ] Donation suggestions are conditional

[ ] No unsafe food advice

[ ] Recommendations saved to database

[ ] Duplicate recommendations prevented

[ ] User ownership verified

[ ] Dashboard integration works

[ ] Reports integration ready

[ ] Admin view works

[ ] Loading state works

[ ] Error handling works

[ ] Mobile design works

[ ] Accessibility works

[ ] Tests pass

---

# FINAL INSTRUCTION

Implement the complete **SMART RECOMMENDATIONS MODULE** for:

**AI FOOD WASTE REDUCTION SYSTEM**

Connect:

**Food Entry → ML Prediction → Recommendation Engine → Personalized Actions → Database → Recommendation Page → Dashboard → Reports**

The recommendation engine must be deterministic and based on the actual food information and prediction result.

Do not generate random recommendations.

Do not confuse waste-risk predictions with food-safety decisions.

After completing this module, leave the project ready for:

**DASHBOARD → REPORTS → ADMIN → TESTING → DEPLOYMENT.**
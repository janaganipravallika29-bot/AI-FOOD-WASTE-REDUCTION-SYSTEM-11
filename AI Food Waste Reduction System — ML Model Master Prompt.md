# MASTER PROMPT — MACHINE LEARNING MODEL

You are an expert Machine Learning Engineer and Flask Backend Developer.

My project is:

**AI FOOD WASTE REDUCTION SYSTEM**

The following modules are already implemented:

- Professional frontend
- Flask backend
- SQLAlchemy database
- Login/Signup
- User authentication
- User/Admin roles
- Food Entry module
- Food Entry database
- Image upload

Now implement the complete **MACHINE LEARNING MODEL** for food-waste-risk prediction.

The ML system must be connected to the existing Flask backend and database.

Do NOT create a fake/random prediction.

The prediction must come from an actual trained ML model.

The system should predict:

```text
LOW
MEDIUM
HIGH
```

food-waste risk.

---

# 1. ML OBJECTIVE

The model should estimate the likelihood that a food item may contribute to food waste based on information such as:

```text
Food Category
Quantity
Days Until Expiry
Storage Type
Storage Temperature
Previous Waste
```

The system should produce:

```text
Waste Risk Level
Confidence Score
```

Example:

```text
Food:
Tomatoes

Risk:
HIGH

Confidence:
87%

Reason:
The item has a short remaining shelf-life and previous waste is relatively high.
```

The reason should be generated from actual input factors, not invented randomly.

---

# 2. IMPORTANT ML PRINCIPLE

Do NOT claim that the model predicts actual food spoilage or guarantees that food is unsafe.

The model predicts:

**Food Waste Risk**

not:

**Food Safety**

The application must clearly distinguish:

```text
Food Waste Risk ≠ Food Safety Certification
```

---

# 3. ML TECHNOLOGY

Use:

```text
Python
pandas
numpy
scikit-learn
joblib
Flask
SQLAlchemy
```

Add required packages to:

```text
requirements.txt
```

Expected:

```text
pandas
numpy
scikit-learn
joblib
```

---

# 4. ML PROJECT STRUCTURE

Create:

```text
ml/
│
├── data/
│   └── food_waste_dataset.csv
│
├── models/
│   └── food_waste_model.joblib
│
├── preprocessing/
│   └── preprocessing.py
│
├── train_model.py
├── evaluate_model.py
└── predict.py
```

If the project already has an ML folder, extend the existing structure instead of duplicating it.

---

# 5. DATASET

The model needs a dataset containing historical food-waste examples.

Use a legitimate dataset if available.

If no suitable dataset is already supplied, create a clearly labeled **synthetic training dataset for demonstration purposes** based on realistic feature ranges.

Do NOT present synthetic data as real-world collected data.

The dataset should contain features such as:

```text
food_category
quantity
days_until_expiry
storage_type
temperature
previous_waste
waste_risk
```

Example:

```text
Vegetables,2.0,2,Room Temperature,25,1.0,HIGH
Fruits,1.5,7,Refrigerator,5,0.2,MEDIUM
Grains,5.0,30,Pantry,22,0.1,LOW
```

---

# 6. TARGET VARIABLE

Target:

```text
waste_risk
```

Allowed values:

```text
LOW
MEDIUM
HIGH
```

The model must perform multiclass classification.

---

# 7. FEATURES

Use these primary features:

```text
food_category
quantity
days_until_expiry
storage_type
temperature
previous_waste
```

Derived feature:

```text
previous_waste_ratio
```

where appropriate.

Do not use:

```text
user_id
email
name
password
image filename
```

as ML features.

These are not meaningful prediction features and could create privacy or leakage problems.

---

# 8. DERIVED FEATURES

Calculate:

### Days Until Expiry

```text
expiry_date - current_date
```

Example:

```text
Expiry Date = August 15
Today = August 12

Days Until Expiry = 3
```

Do not accept this value blindly from the frontend.

Calculate it in the backend.

---

# 9. PREVIOUS WASTE RATIO

If useful, calculate:

```text
previous_waste_ratio =
previous_waste / quantity
```

Handle:

```text
quantity = 0
```

safely.

Quantity should already be validated as greater than zero.

---

# 10. DATA PREPROCESSING

Use a proper scikit-learn preprocessing pipeline.

Categorical features:

```text
food_category
storage_type
```

Use:

```text
OneHotEncoder
```

Numeric features:

```text
quantity
days_until_expiry
temperature
previous_waste
```

Use appropriate numerical preprocessing such as:

```text
StandardScaler
```

Combine preprocessing and model into a single:

```text
Pipeline
```

This prevents inconsistent preprocessing between training and prediction.

---

# 11. MODEL SELECTION

Train and compare multiple classification models.

At minimum:

```text
Logistic Regression
Random Forest
Decision Tree
```

Optionally:

```text
Gradient Boosting
```

Compare them using validation metrics.

Choose the best appropriate model based on validation performance and practical considerations.

Do NOT simply choose a model because it produces the highest training accuracy.

---

# 12. TRAIN/TEST SPLIT

Use:

```text
80% training
20% testing
```

Use:

```python
train_test_split(
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

when class counts permit stratification.

---

# 13. MODEL EVALUATION

Calculate:

```text
Accuracy
Precision
Recall
F1 Score
Confusion Matrix
```

For multiclass classification, report appropriate macro/weighted averages.

Print the results after training.

Example:

```text
MODEL EVALUATION
------------------------
Accuracy: 89.2%
Precision: 88.7%
Recall: 87.9%
F1 Score: 88.1%
```

Do not hardcode these values.

They must come from the actual evaluation.

---

# 14. CLASS BALANCE

Before training:

```text
Check class distribution
```

Display:

```text
LOW: ...
MEDIUM: ...
HIGH: ...
```

If the classes are heavily imbalanced, use an appropriate strategy such as:

```text
class_weight="balanced"
```

where supported.

Do not artificially inflate the evaluation results.

---

# 15. TRAINING SCRIPT

Create:

```text
ml/train_model.py
```

It should:

1. Load dataset.
2. Validate columns.
3. Clean missing values.
4. Create derived features.
5. Split data.
6. Build preprocessing pipeline.
7. Train candidate models.
8. Evaluate models.
9. Select the best model.
10. Save the complete pipeline.

Save:

```text
ml/models/food_waste_model.joblib
```

---

# 16. SAVE COMPLETE PIPELINE

Save the preprocessing and model together.

For example:

```text
Pipeline
 ├── preprocessing
 └── classifier
```

Save using:

```python
joblib.dump()
```

This means Flask does not need to recreate preprocessing manually.

---

# 17. MODEL VERSION

Store a model version such as:

```text
1.0
```

When the model is retrained:

```text
1.1
1.2
2.0
```

The prediction database should store the model version used.

---

# 18. PREDICTION MODULE

Create:

```text
ml/predict.py
```

It should load:

```text
food_waste_model.joblib
```

and expose a clean prediction function.

Conceptually:

```python
predict_food_waste(features)
```

Return:

```text
risk_level
confidence
```

Example:

```python
{
    "risk_level": "HIGH",
    "confidence": 87.4
}
```

---

# 19. CONFIDENCE SCORE

If the selected classifier supports:

```text
predict_proba()
```

use it to calculate the predicted class probability.

Convert it to a percentage:

```text
0.874 → 87.4%
```

Do not call this a guarantee.

Display:

```text
Model confidence: 87%
```

Also add a small explanation:

```text
This is an AI-generated risk estimate, not a food-safety determination.
```

---

# 20. FLASK PREDICTION ROUTE

Create:

```text
POST /predict/<int:food_id>
```

The route must:

1. Require login.
2. Retrieve food entry.
3. Verify ownership.
4. Extract features.
5. Calculate days until expiry.
6. Load model.
7. Run prediction.
8. Save prediction.
9. Generate recommendation-ready information.
10. Return the result.

---

# 21. OWNERSHIP SECURITY

Normal users can only request predictions for their own food entries.

Check:

```text
food_entry.user_id == current_user.id
```

If false:

```text
403 Forbidden
```

or a safe not-found response.

Admin users may access authorized administrative prediction functions.

Never trust a user-provided `user_id`.

---

# 22. FEATURE PREPARATION

When predicting:

```text
FoodEntry
   ↓
Feature Preparation
   ↓
DataFrame
   ↓
Saved ML Pipeline
   ↓
Prediction
```

Example feature object:

```text
food_category = Vegetables
quantity = 2
days_until_expiry = 2
storage_type = Room Temperature
temperature = 25
previous_waste = 0.8
```

---

# 23. DATABASE PREDICTION TABLE

Use the existing:

```text
predictions
```

table.

Required:

```text
id
food_entry_id
waste_level
confidence
model_version
created_at
```

Save:

```text
waste_level = LOW / MEDIUM / HIGH
confidence = actual model confidence
model_version = 1.0
```

Do not create a second prediction table.

---

# 24. PREDICTION RELATIONSHIP

Maintain:

```text
FoodEntry
     │
     └── Prediction
```

The prediction must reference the correct:

```text
food_entry_id
```

---

# 25. PREDICTION HISTORY

Do not automatically delete older predictions unless the application's data policy requires it.

Keep prediction history so the system can later support:

```text
Model comparison
Prediction history
Reports
Analytics
Model version tracking
```

---

# 26. PREDICTION RESULT PAGE

Create or update:

```text
templates/prediction.html
```

Display:

```text
AI FOOD WASTE ANALYSIS
```

Example:

```text
Food:
Tomatoes

Category:
Vegetables

Quantity:
2 kg

Days Until Expiry:
2 days
```

Then:

```text
WASTE RISK

HIGH

Model Confidence
87%
```

---

# 27. RISK VISUALIZATION

Use clear visual indicators:

```text
LOW
MEDIUM
HIGH
```

Example layout:

```text
┌──────────────────────────────┐
│       WASTE RISK             │
│                              │
│          HIGH                │
│                              │
│      Confidence: 87%         │
└──────────────────────────────┘
```

Use accessible labels in addition to color.

---

# 28. AI EXPLANATION

Display the important contributing factors.

For example:

```text
Why this result?

• Only 2 days remain before expiry.
• The food is stored at room temperature.
• Previous waste amount is relatively high.
```

These explanations must be derived from actual input values and predefined explanation logic.

Do not falsely claim that the model mathematically used a specific feature unless that is supported by the model/explanation method.

---

# 29. EXPLANATION ENGINE

Create:

```text
ml/explanation.py
```

Use rule-based explanations based on the actual input.

Examples:

If:

```text
days_until_expiry <= 3
```

then:

```text
Short remaining shelf-life increases waste risk.
```

If:

```text
previous_waste > 0
```

then:

```text
Previous waste for this food amount is a relevant risk indicator.
```

If storage conditions are relevant:

```text
Current storage information was considered in the prediction.
```

Keep explanations honest and understandable.

---

# 30. RECOMMENDATION-READY OUTPUT

After prediction, prepare data for the next module:

```text
risk_level
confidence
days_until_expiry
food_category
quantity
storage_type
previous_waste
```

The next module will generate:

**SMART RECOMMENDATIONS**

Do not hardcode recommendations into the ML model itself.

Keep:

```text
ML Prediction
```

separate from:

```text
Recommendation Engine
```

---

# 31. EXAMPLE PREDICTION FLOW

Example input:

```text
Food:
Milk

Category:
Dairy

Quantity:
1 L

Days Until Expiry:
1

Storage:
Refrigerator

Temperature:
5°C

Previous Waste:
0.5 L
```

Flow:

```text
Food Entry
    ↓
Feature Preparation
    ↓
ML Pipeline
    ↓
Prediction
    ↓
HIGH
    ↓
Confidence
    ↓
Save to Database
    ↓
Prediction Page
    ↓
Recommendation Module
```

---

# 32. MODEL LOADING

Do not train the model every time a user requests a prediction.

Correct:

```text
Application startup
      ↓
Load trained model
      ↓
Prediction requests
      ↓
Use loaded model
```

Incorrect:

```text
User clicks Predict
      ↓
Train model
      ↓
Predict
```

Training should be a separate process.

---

# 33. MODEL ERROR HANDLING

If the model file is missing:

```text
food_waste_model.joblib
```

show a controlled error.

Example:

```text
AI prediction is temporarily unavailable.
Please try again later.
```

Do not show a Python traceback to the user.

Log the technical error on the server.

---

# 34. INVALID INPUT HANDLING

If required ML features are missing:

```text
Prediction cannot be generated because required food information is missing.
```

Do not make a prediction from incomplete data unless the model was specifically designed to handle missing values.

---

# 35. MODEL INPUT VALIDATION

Before prediction verify:

```text
quantity > 0
days_until_expiry is valid
temperature is numeric if provided
previous_waste >= 0
category is valid
storage_type is valid
```

---

# 36. API RESPONSE

If using JSON API:

Successful response:

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

# 37. FRONTEND AI ANALYSIS

When user clicks:

```text
ANALYZE WITH AI
```

show:

```text
Analyzing food data...

Preparing features...
Running AI model...
Generating risk estimate...
```

Do not claim individual processing stages unless they actually occur.

A simple loading state is sufficient.

After completion:

```text
Prediction Result
```

---

# 38. PREDICTION DATABASE FLOW

Implement:

```text
Food Entry
    ↓
food_entries
    ↓
Feature Extraction
    ↓
ML Model
    ↓
Prediction
    ↓
predictions
    ↓
Dashboard
    ↓
Reports
```

---

# 39. DASHBOARD INTEGRATION

Update dashboard statistics from the actual prediction database.

Display:

```text
Total Predictions
Low Risk
Medium Risk
High Risk
```

Example:

```text
Total Analyses       120
Low Risk              45
Medium Risk           50
High Risk             25
```

These must come from database queries.

Never hardcode the numbers.

---

# 40. DASHBOARD CHART

Create a chart using Chart.js or the project's existing chart library.

Chart:

```text
Food Waste Risk Distribution
```

Categories:

```text
LOW
MEDIUM
HIGH
```

Values must come from Flask/database.

---

# 41. REPORT INTEGRATION

Reports should eventually show:

```text
Prediction Count
Low Risk Percentage
Medium Risk Percentage
High Risk Percentage
```

The ML module must expose the required database data to the reports module.

---

# 42. ADMIN ML STATISTICS

Admin dashboard should show:

```text
Total Predictions
Low Risk
Medium Risk
High Risk
Average Confidence
Current Model Version
```

Also show:

```text
Model Performance
```

using the actual evaluation results from model training.

Do not mix training evaluation metrics with user prediction confidence.

---

# 43. TRAINING REPORT

Create:

```text
ml/model_metrics.json
```

Store:

```text
model_name
model_version
accuracy
precision
recall
f1_score
training_date
```

Example structure:

```json
{
  "model_version": "1.0",
  "model_name": "RandomForestClassifier",
  "accuracy": 0.89,
  "precision": 0.88,
  "recall": 0.87,
  "f1_score": 0.88
}
```

These values must be generated by the training script.

---

# 44. MODEL REPRODUCIBILITY

Use fixed random seeds where appropriate:

```text
random_state = 42
```

Save:

```text
dataset version
model version
training date
```

This makes future model updates traceable.

---

# 45. DATA LEAKAGE PREVENTION

Do not allow information from the test set to influence preprocessing or training.

Use:

```text
Pipeline
```

so transformations are fitted only on training data.

Do not calculate preprocessing statistics from the complete dataset before splitting.

---

# 46. MODEL VALIDATION

If the dataset is sufficiently large, consider cross-validation for model selection.

For example:

```text
Stratified K-Fold
```

Use it appropriately.

Do not use complex validation methods unnecessarily for a tiny synthetic dataset.

---

# 47. MODEL LIMITATIONS

Add a section to the prediction page:

```text
About AI Prediction

This system estimates food-waste risk from the information provided.
The result is an AI-generated estimate and should not be treated as
a guarantee about food safety, quality, or spoilage.
```

---

# 48. TESTING

Test at least these examples:

### LOW

Food with:

```text
Long expiry period
Low previous waste
Appropriate storage
```

### MEDIUM

Food with:

```text
Moderate expiry period
Moderate previous waste
```

### HIGH

Food with:

```text
Very short expiry period
Higher previous waste
Risk-related storage conditions
```

Do not expect manually chosen examples to always produce a specific class unless the trained data supports it.

---

# 49. MODEL UNIT TESTS

Create:

```text
tests/
└── test_ml.py
```

Test:

```text
Model loads
Prediction returns valid class
Confidence is between 0 and 100
Required features are accepted
Invalid features are rejected
Prediction database record is created
Model version is stored
```

---

# 50. FLASK INTEGRATION TEST

Test:

```text
Login
 ↓
Add Food
 ↓
Click Analyze
 ↓
Flask Prediction Route
 ↓
ML Model
 ↓
Prediction Saved
 ↓
Prediction Page
```

Verify the database contains:

```text
food_entry_id
waste_level
confidence
model_version
created_at
```

---

# 51. PERFORMANCE

Do not retrain during normal user requests.

Avoid repeatedly loading the model from disk for every prediction if the application architecture permits keeping it in memory.

For production, use appropriate application startup/model-loading patterns.

---

# 52. SECURITY

Do not expose:

```text
Model file
Training dataset
Internal file paths
Server exceptions
Database credentials
```

through the frontend.

Validate all prediction requests.

Require authentication.

Verify food-entry ownership.

---

# 53. FINAL FILE STRUCTURE

Expected:

```text
AI_Food_Waste_Reduction_System/
│
├── app.py
├── config.py
├── requirements.txt
│
├── models/
│   ├── user.py
│   ├── food_entry.py
│   ├── prediction.py
│   └── recommendation.py
│
├── routes/
│   ├── auth_routes.py
│   ├── food_routes.py
│   └── prediction_routes.py
│
├── ml/
│   ├── data/
│   │   └── food_waste_dataset.csv
│   │
│   ├── models/
│   │   └── food_waste_model.joblib
│   │
│   ├── preprocessing/
│   │   └── preprocessing.py
│   │
│   ├── train_model.py
│   ├── evaluate_model.py
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
│   ├── js/
│   └── uploads/
│
└── tests/
    └── test_ml.py
```

Do not duplicate existing files.

---

# 54. COMPLETE ML FLOW

The final implementation must work like this:

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
           EXTRACT FEATURES
                   ↓
          PREPROCESS FEATURES
                   ↓
             ML MODEL
                   ↓
       ┌───────────┼───────────┐
       ↓           ↓           ↓
      LOW        MEDIUM       HIGH
       └───────────┼───────────┘
                   ↓
             CONFIDENCE
                   ↓
            SAVE PREDICTION
                   ↓
          PREDICTION PAGE
                   ↓
        SMART RECOMMENDATIONS
                   ↓
              DASHBOARD
                   ↓
               REPORTS
```

---

# 55. FINAL CHECKLIST

Before completing the implementation, verify:

[ ] Dataset exists

[ ] Dataset is clearly labeled as real or synthetic

[ ] Features are defined

[ ] Target variable is defined

[ ] Data preprocessing works

[ ] Train/test split works

[ ] Multiple models are evaluated

[ ] Best model is selected appropriately

[ ] Accuracy is calculated

[ ] Precision is calculated

[ ] Recall is calculated

[ ] F1 score is calculated

[ ] Confusion matrix is generated

[ ] Complete pipeline is saved

[ ] Model can be loaded

[ ] Prediction function works

[ ] Confidence is calculated correctly

[ ] Model version is stored

[ ] Flask prediction route works

[ ] Login is required

[ ] Food ownership is checked

[ ] Prediction is saved to database

[ ] Prediction page works

[ ] Dashboard statistics update

[ ] Admin statistics update

[ ] Model limitations are displayed

[ ] No fake/random predictions are used

[ ] No model training occurs during user prediction

[ ] ML unit tests pass

[ ] Flask integration test passes

---

# FINAL INSTRUCTION

Implement the complete ML module for:

**AI FOOD WASTE REDUCTION SYSTEM**

Connect:

**Food Entry → Feature Extraction → Preprocessing → Trained ML Model → LOW/MEDIUM/HIGH Waste Risk → Confidence → Database → Prediction Page → Dashboard**

Use a real trained machine-learning pipeline and clearly identify any synthetic/demo dataset used during development.

Do not generate random predictions.

Do not confuse food-waste risk with food-safety determination.

After completing this module, leave the project ready for the next stage:

**SMART RECOMMENDATIONS → DASHBOARD → REPORTS → ADMIN → TESTING → DEPLOYMENT.**
# MASTER PROMPT — FOOD ENTRY MODULE

You are an expert Flask backend developer, frontend developer, database engineer, and UI/UX designer.

My project is:

**AI FOOD WASTE REDUCTION SYSTEM**

The following modules are already implemented:

- Professional frontend
- Flask backend
- SQLAlchemy database
- Login/Signup
- Flask-Login authentication
- User sessions
- User/Admin roles

Now implement the complete **FOOD ENTRY MODULE**.

Do not create a disconnected form.

The Food Entry module must be fully connected:

**Logged-in User → Food Entry Form → Flask Backend → Validation → Database → AI Prediction Ready → Dashboard**

---

# 1. FOOD ENTRY PURPOSE

The Food Entry page allows a logged-in user to enter information about food they have purchased or stored.

The system must collect enough information for the future ML model to predict food waste risk.

The user should be able to enter:

- Food name
- Food category
- Quantity
- Unit
- Purchase date
- Expiry date
- Storage type
- Storage temperature
- Previous waste amount
- Optional food image

After submitting:

```text
FOOD ENTRY
    ↓
FLASK BACKEND
    ↓
VALIDATION
    ↓
DATABASE
    ↓
SUCCESS
    ↓
AI ANALYSIS / PREDICTION
```

---

# 2. USER ACCESS

Only authenticated users can access:

```text
/food-entry
```

Use:

```python
@login_required
```

If the user is not logged in:

```text
/food-entry
    ↓
/login
```

A user must only be able to create and view their own food records.

Admin users may access all records through the admin panel.

---

# 3. FRONTEND FILE

Use the existing:

```text
templates/food_entry.html
```

Do not create a duplicate file if it already exists.

Connect it to:

```text
static/css/style.css
static/js/script.js
```

Maintain the same professional design used throughout the application.

---

# 4. FOOD ENTRY PAGE DESIGN

Create a professional page with:

## Header

```text
FOOD ENTRY

Add your food information and let AI analyze your waste risk.
```

Use an environmental + AI theme.

---

# 5. FOOD ENTRY FORM

Create:

```html
<form
    method="POST"
    action="/food-entry"
    enctype="multipart/form-data"
>
```

Fields:

```text
Food Name
Food Category
Quantity
Unit
Purchase Date
Expiry Date
Storage Type
Storage Temperature
Previous Waste Amount
Food Image
```

Use proper:

```text
<label>
<input>
<select>
<button>
```

Do not rely only on placeholder text.

---

# 6. FOOD NAME

Field:

```text
Food Name *
```

Example:

```text
Tomatoes
Milk
Rice
Apples
Bread
Chicken
Potatoes
```

HTML name:

```text
food_name
```

Validation:

- Required
- Minimum 2 characters
- Maximum 100 characters

---

# 7. FOOD CATEGORY

Create a dropdown:

```text
Food Category *
```

Options:

```text
Select Category
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

HTML name:

```text
category
```

The backend must validate the category.

---

# 8. QUANTITY

Create:

```text
Quantity *
```

Example:

```text
2
5
1.5
```

HTML:

```text
quantity
```

Validation:

- Required
- Numeric
- Greater than 0
- Reasonable maximum

Do not accept:

```text
-5
0
abc
```

---

# 9. UNIT

Create dropdown:

```text
Unit *
```

Options:

```text
kg
g
L
ml
pieces
packets
boxes
```

HTML name:

```text
unit
```

---

# 10. PURCHASE DATE

Create:

```text
Purchase Date *
```

HTML:

```text
<input type="date" name="purchase_date">
```

The backend must validate the date.

Do not allow invalid date values.

---

# 11. EXPIRY DATE

Create:

```text
Expiry Date *
```

HTML:

```text
<input type="date" name="expiry_date">
```

Validation:

```text
expiry_date >= purchase_date
```

If invalid:

```text
Expiry date cannot be earlier than purchase date.
```

---

# 12. DAYS REMAINING

Calculate automatically:

```text
Expiry Date - Current Date
```

Display:

```text
Days Remaining: 3 days
```

Use JavaScript for immediate frontend feedback.

IMPORTANT:

The backend must calculate the final value again.

Do not trust the value sent by the browser.

---

# 13. EXPIRY STATUS

Show a visual status.

Examples:

```text
🟢 Safe
Food has sufficient remaining days.
```

```text
🟡 Expiring Soon
Food should be consumed soon.
```

```text
🔴 Expired
Expiry date has passed.
```

Use:

```text
expiry_date
```

to calculate this.

---

# 14. STORAGE TYPE

Create:

```text
Storage Type *
```

Options:

```text
Refrigerator
Freezer
Room Temperature
Pantry
Cupboard
Other
```

HTML name:

```text
storage_type
```

---

# 15. STORAGE TEMPERATURE

Create:

```text
Storage Temperature
```

Example:

```text
5 °C
25 °C
-18 °C
```

HTML name:

```text
temperature
```

Make this optional.

Validate that it is numeric when provided.

---

# 16. PREVIOUS WASTE

Create:

```text
Previous Waste Amount
```

Description:

```text
Approximate amount of similar food wasted previously.
```

Example:

```text
0.5 kg
```

Fields:

```text
previous_waste
previous_waste_unit
```

If the existing database has only `previous_waste`, maintain compatibility with that schema.

Default:

```text
0
```

---

# 17. FOOD IMAGE UPLOAD

Add an optional image upload section.

Design:

```text
┌──────────────────────────────────┐
│                                  │
│             📷                   │
│       Upload Food Image          │
│                                  │
│  Drag & Drop or Browse Files     │
│                                  │
│  JPG • JPEG • PNG • WEBP         │
│                                  │
└──────────────────────────────────┘
```

Allow:

```text
JPG
JPEG
PNG
WEBP
```

---

# 18. IMAGE PREVIEW

When a user selects an image:

```text
Selected Image
       ↓
Preview
       ↓
Remove / Change
```

Use JavaScript.

Show:

```text
Image Preview
```

before submission.

Do not upload the image until the form is submitted.

---

# 19. IMAGE SECURITY

Backend must:

- Use `secure_filename()`
- Validate extension
- Validate MIME type where appropriate
- Limit file size
- Store only allowed image formats
- Generate a safe unique filename if needed

Store images in:

```text
static/uploads/
```

Do not allow:

```text
.exe
.php
.js
.sh
.html
```

or other executable files.

---

# 20. BACKEND ROUTE

Create:

```text
GET  /food-entry
POST /food-entry
```

Use Flask.

Example structure:

```python
@food_bp.route("/food-entry", methods=["GET", "POST"])
@login_required
def food_entry():
    ...
```

If the existing project uses another blueprint structure, follow the existing architecture.

Do not create duplicate routes.

---

# 21. GET REQUEST

When the user opens:

```text
/food-entry
```

show the form.

Pre-fill user-specific information only where appropriate.

Do not expose information belonging to another user.

---

# 22. POST REQUEST

When the form is submitted:

```text
Browser
   ↓
POST /food-entry
   ↓
Flask
   ↓
Validate Input
   ↓
Calculate Days Remaining
   ↓
Validate Image
   ↓
Create FoodEntry
   ↓
Database
   ↓
Activity Log
   ↓
Prediction Stage
```

---

# 23. DATABASE MODEL

Use the existing `FoodEntry` model.

Required fields:

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

Do not create a second food table.

---

# 24. USER RELATIONSHIP

When creating a food entry:

```python
food_entry.user_id = current_user.id
```

Never accept `user_id` directly from the frontend.

The logged-in user ID must come from:

```python
current_user.id
```

This prevents users from creating records under another user's account.

---

# 25. BACKEND VALIDATION

Validate all fields on the server.

### Food Name

Required.

### Category

Must be one of the allowed categories.

### Quantity

Must be:

```text
> 0
```

### Unit

Must be one of the allowed units.

### Purchase Date

Required.

### Expiry Date

Required.

Must satisfy:

```text
expiry_date >= purchase_date
```

### Storage Type

Must be one of the allowed storage types.

### Temperature

Optional, but numeric if supplied.

### Previous Waste

Optional.

Must be:

```text
>= 0
```

---

# 26. CALCULATE DAYS REMAINING

Do NOT trust a `days_remaining` value submitted by the browser.

Calculate it in Flask:

```text
days_remaining =
expiry_date - current_date
```

Store it only if the existing schema supports it.

Otherwise calculate it when needed.

---

# 27. EXPIRED FOOD

If:

```text
days_remaining < 0
```

mark the food as:

```text
EXPIRED
```

Show:

```text
⚠ This food has already expired.
```

Do not automatically claim that expired food is safe to eat.

---

# 28. EXPIRING SOON

If:

```text
0 <= days_remaining <= 3
```

mark:

```text
EXPIRING SOON
```

Show:

```text
⚠ This food is approaching its expiry date.
```

---

# 29. SAFE STATUS

If:

```text
days_remaining > 3
```

show:

```text
SAFE / MONITOR
```

Avoid making medical or food-safety guarantees. The system should provide management guidance rather than claim food is definitely safe.

---

# 30. DATABASE SAVE

After validation:

```text
Food Form
    ↓
FoodEntry Object
    ↓
db.session.add()
    ↓
db.session.commit()
```

Save:

```text
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
```

---

# 31. ACTIVITY LOG

If the existing `activities` table exists, create:

```text
activity_type:
FOOD_ADDED
```

Description:

```text
Added food entry: Tomatoes
```

Associate it with:

```text
current_user.id
```

Do not log passwords or sensitive authentication information.

---

# 32. SUCCESS MESSAGE

After successfully saving:

```text
Food entry added successfully!
```

Then redirect to the next stage.

Preferred flow:

```text
Food Entry
    ↓
Saved Successfully
    ↓
AI Prediction
```

If the ML module is not yet implemented, temporarily redirect to the dashboard or a clearly marked prediction-ready page.

Do NOT generate fake predictions.

---

# 33. AI-READY STRUCTURE

The food entry module must be prepared for the next module:

**ML MODEL → PREDICTION**

The collected fields should be available to the prediction module:

```text
food_name
category
quantity
unit
purchase_date
expiry_date
days_remaining
storage_type
temperature
previous_waste
```

Flow:

```text
Food Entry
    ↓
Database
    ↓
ML Preprocessing
    ↓
ML Model
    ↓
Prediction
```

---

# 34. PREDICTION BUTTON

If the ML prediction module is already available, after saving display:

```text
Food Saved Successfully!

[ ANALYZE WITH AI ]
```

The button should send the food entry ID to the prediction route.

Example:

```text
POST /predict
```

Do not send the entire database record unnecessarily.

---

# 35. USER FOOD HISTORY

Create a section on the food entry page or dashboard:

```text
MY RECENT FOOD
```

Display only the logged-in user's records.

Columns:

```text
Food
Category
Quantity
Expiry
Status
Prediction
Action
```

Example:

```text
Tomatoes
Vegetables
2 kg
2 days
Expiring Soon
Pending
View
```

---

# 36. FOOD DETAILS PAGE

If useful, create:

```text
/food/<int:food_id>
```

Show:

```text
Food Name
Category
Quantity
Purchase Date
Expiry Date
Days Remaining
Storage Type
Temperature
Previous Waste
Image
Prediction
Recommendations
```

IMPORTANT:

Verify that the food entry belongs to:

```text
current_user.id
```

unless the logged-in user is an authorized admin.

---

# 37. EDIT FOOD ENTRY

Create:

```text
GET  /food/<int:food_id>/edit
POST /food/<int:food_id>/edit
```

Allow the owner to update:

```text
Food Name
Category
Quantity
Unit
Expiry Date
Storage Type
Temperature
Previous Waste
Image
```

Revalidate everything on the server.

---

# 38. DELETE FOOD ENTRY

Create:

```text
POST /food/<int:food_id>/delete
```

Do not use an unsafe GET request for deletion.

Show confirmation:

```text
Are you sure you want to delete this food entry?

[ CANCEL ] [ DELETE ]
```

When deleted, correctly handle:

```text
Predictions
Recommendations
Activities
```

according to the existing SQLAlchemy cascade design.

---

# 39. USER DATA SECURITY

A normal user must only be able to:

```text
CREATE → their own food entries
VIEW → their own food entries
EDIT → their own food entries
DELETE → their own food entries
```

A normal user must NOT be able to manipulate another user's `food_id` through the URL.

Always verify ownership on the backend.

---

# 40. ADMIN ACCESS

Admin users may access food records through:

```text
/admin/foods
```

The admin page can display:

```text
User
Food
Category
Quantity
Expiry
Prediction
Created Date
```

Do not weaken normal user ownership checks.

---

# 41. FRONTEND VALIDATION

Use JavaScript for immediate feedback.

Validate:

```text
Food Name
Category
Quantity
Unit
Purchase Date
Expiry Date
Temperature
Previous Waste
Image
```

But remember:

**Frontend validation is not security.**

All validation must also happen in Flask.

---

# 42. LOADING STATE

When clicking:

```text
ANALYZE FOOD
```

show:

```text
Analyzing your food information...

⏳ Processing...
```

Disable the button temporarily to prevent accidental duplicate submissions.

If the request fails, restore the button and show an error.

---

# 43. DUPLICATE SUBMISSION PROTECTION

Prevent accidental duplicate food entries when the user double-clicks the submit button.

Use:

- Disabled submit button
- Loading state
- Server-side safeguards where appropriate

Do not blindly create duplicate records.

---

# 44. FLASH MESSAGES

Use Flask flash messages:

Success:

```text
✓ Food entry added successfully.
```

Error:

```text
⚠ Please correct the highlighted fields.
```

Image:

```text
⚠ Invalid image format.
```

Expiry:

```text
⚠ Expiry date cannot be before purchase date.
```

---

# 45. DASHBOARD INTEGRATION

After a food entry is saved, update the dashboard statistics.

For example:

```text
Total Food Entries
```

must increase.

Recent food entries should display the newly added record.

Expiring-soon foods should update automatically.

---

# 46. DATABASE QUERIES

Create queries for:

### User's food entries

```text
WHERE user_id = current_user.id
```

### Recent entries

Sort:

```text
created_at DESC
```

### Expiring soon

```text
expiry_date <= today + 3 days
```

### Expired

```text
expiry_date < today
```

### Category statistics

Group by:

```text
category
```

These will later be used by the dashboard and reports.

---

# 47. API-READY DESIGN

If the project uses API endpoints, create:

```text
GET /api/foods
GET /api/foods/<id>
POST /api/foods
PUT /api/foods/<id>
DELETE /api/foods/<id>
```

Protect these endpoints with authentication and ownership checks.

If the current project uses server-rendered Jinja forms instead, do not unnecessarily duplicate functionality.

---

# 48. IMAGE STORAGE

Store uploaded files:

```text
static/uploads/
```

Database should store only:

```text
image_filename
```

not the entire binary image.

Example:

```text
tomatoes_8f92a.jpg
```

The frontend can then construct the appropriate static URL.

---

# 49. FILE SIZE

Configure a reasonable maximum upload size, for example:

```text
5 MB
```

If exceeded:

```text
Image is too large. Please upload an image smaller than 5 MB.
```

---

# 50. PROFESSIONAL UI

The Food Entry page should contain:

### Section 1

```text
Food Information
```

### Section 2

```text
Purchase & Expiry
```

### Section 3

```text
Storage Information
```

### Section 4

```text
Previous Waste
```

### Section 5

```text
Food Image
```

### Section 6

```text
AI Analysis
```

Use cards and clean spacing.

---

# 51. RESPONSIVE DESIGN

The page must work on:

- Desktop
- Laptop
- Tablet
- Mobile

On desktop:

```text
Food Information     Image Upload
Storage Information  Preview
```

On mobile:

```text
Food Information
       ↓
Storage
       ↓
Image Upload
       ↓
AI Analysis
```

---

# 52. ACCESSIBILITY

Implement:

- Labels for every field
- Keyboard navigation
- Clear focus states
- Accessible buttons
- Meaningful error messages
- Alt text for uploaded image preview
- Good color contrast

Do not use color alone to communicate risk/status.

---

# 53. ERROR HANDLING

Handle:

```text
Invalid food ID
Unauthorized food access
Invalid quantity
Invalid category
Invalid date
Invalid image
Database error
Upload error
Missing form fields
```

Never expose Python traceback details to normal users.

---

# 54. TESTING

Test:

### Create

```text
Add Tomatoes
2 kg
Vegetables
Expiry in 2 days
```

Verify database record.

### Invalid quantity

```text
-2
```

Must fail.

### Invalid date

```text
Expiry before purchase
```

Must fail.

### Invalid image

```text
.exe
```

Must fail.

### Ownership

User A must NOT access User B's food entry.

### Login

Logged-out user must be redirected to login.

### Admin

Admin can view records through admin panel.

---

# 55. COMPLETE FOOD ENTRY FLOW

The final flow must be:

```text
LOGIN
  ↓
DASHBOARD
  ↓
+ ADD FOOD
  ↓
FOOD ENTRY FORM
  ↓
ENTER FOOD DETAILS
  ↓
UPLOAD OPTIONAL IMAGE
  ↓
CLIENT VALIDATION
  ↓
FLASK SERVER
  ↓
SERVER VALIDATION
  ↓
CALCULATE DAYS REMAINING
  ↓
SAVE IMAGE
  ↓
SAVE FOOD ENTRY
  ↓
SAVE ACTIVITY
  ↓
AI PREDICTION
  ↓
PREDICTION RESULT
```

---

# 56. FILES TO CREATE OR UPDATE

Use the existing project architecture.

Expected files:

```text
routes/
└── food_routes.py

models/
└── food_entry.py

templates/
├── food_entry.html
└── food_details.html

static/
├── css/
│   └── style.css
└── js/
    └── script.js

static/uploads/
```

Update:

```text
app.py
```

to register the food blueprint if necessary.

Update:

```text
models/__init__.py
```

if necessary.

Do not create duplicate models or routes.

---

# 57. FINAL CHECKLIST

Before finishing, verify:

[ ] Food Entry page opens

[ ] Login is required

[ ] Form is professional

[ ] Food name validation works

[ ] Category validation works

[ ] Quantity validation works

[ ] Unit validation works

[ ] Purchase date works

[ ] Expiry date works

[ ] Days remaining is calculated

[ ] Storage type works

[ ] Temperature works

[ ] Previous waste works

[ ] Image upload works

[ ] Image preview works

[ ] Invalid files are rejected

[ ] Image size limit works

[ ] Food record is saved in database

[ ] Correct user_id is stored

[ ] Activity is logged

[ ] Duplicate submissions are prevented

[ ] User can view their own entries

[ ] User cannot access another user's entry

[ ] User can edit their entry

[ ] User can delete their entry

[ ] Admin can manage records

[ ] Dashboard statistics update

[ ] ML prediction integration is ready

[ ] No fake prediction is generated

[ ] Mobile layout works

[ ] Error handling works

[ ] Flash messages work

---

# FINAL INSTRUCTION

Build and integrate the complete **FOOD ENTRY MODULE** for:

**AI FOOD WASTE REDUCTION SYSTEM**

Connect:

**Login → Dashboard → Food Entry → Flask → Validation → Database → Image Upload → Activity Log → ML Prediction Ready**

Do not stop at designing the HTML form.

Implement the complete frontend, Flask routes, database integration, validation, image upload, ownership/security checks, edit/delete functionality, dashboard integration, and ML-ready data flow.

After completing this module, the project must be ready for the next stage:

**ML MODEL → FOOD WASTE PREDICTION → SMART RECOMMENDATIONS.**
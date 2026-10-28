# MASTER PROMPT — FRONTEND DESIGN

You are an expert UI/UX designer and frontend developer.

Build a complete, modern, professional, colorful, responsive frontend website from scratch for my college project.

## PROJECT TITLE

**AI FOOD WASTE REDUCTION SYSTEM**

## PROJECT PURPOSE

Create a professional web application that helps users reduce food waste by allowing them to enter food information, analyze food waste risk using AI/ML, receive smart recommendations, monitor their food waste statistics, and generate reports.

The frontend must be designed so that it can later connect easily to a **Python Flask backend, database, authentication system, and machine-learning model**.

Do not create only a landing page. Build the complete frontend interface for the entire application.

---

# 1. TECHNOLOGY REQUIREMENTS

Use:

- HTML5
- CSS3
- Vanilla JavaScript
- Bootstrap 5 if useful
- Chart.js for dashboard/report charts
- Font Awesome or another suitable icon library
- Google Fonts

Do NOT use React, Angular, Vue, or other frameworks unless specifically required.

The frontend must be compatible with a Flask application using:

```text
templates/
static/
static/css/
static/js/
static/images/
static/uploads/
```

All pages must be connected through proper navigation.

---

# 2. DESIGN STYLE

Create a modern environmental/AI-themed design.

Use a professional combination of:

- Green
- Emerald
- Teal
- White
- Light backgrounds
- Small yellow/orange highlights where appropriate

The design should communicate:

- Food
- Sustainability
- Artificial Intelligence
- Environment
- Smart technology
- Waste reduction

Do not make the website look childish.

Make it suitable for:

- College project demonstration
- Project review
- Viva
- Portfolio
- Hackathon presentation

Use:

- Rounded cards
- Soft shadows
- Modern buttons
- Clean typography
- Beautiful icons
- Gradient backgrounds where appropriate
- Subtle hover effects
- Smooth animations
- Proper spacing
- Professional dashboard components

---

# 3. RESPONSIVE DESIGN

The entire website must be responsive.

Support:

- Desktop
- Laptop
- Tablet
- Mobile

Use responsive CSS.

The navigation menu must become a mobile hamburger menu on smaller screens.

Cards and tables must automatically adapt to smaller screens.

---

# 4. FRONTEND FOLDER STRUCTURE

Create:

```text
templates/
│
├── index.html
├── login.html
├── signup.html
├── dashboard.html
├── food_entry.html
├── prediction.html
├── recommendations.html
├── reports.html
├── profile.html
├── admin.html
├── 404.html
└── 500.html

static/
│
├── css/
│   └── style.css
│
├── js/
│   └── script.js
│
└── images/
```

Keep CSS and JavaScript separate from HTML.

Do not put large amounts of CSS inside HTML.

---

# 5. HOME PAGE — index.html

Create a visually impressive landing page.

## Navigation Bar

Logo:

**AI Food Waste**

Navigation:

- Home
- About
- AI Features
- How It Works
- Benefits
- Contact
- Login
- Get Started

Make the navbar sticky.

Logo can include a food/leaf/AI icon.

---

# 6. HERO SECTION

Create a large hero section.

Main heading:

**AI FOOD WASTE REDUCTION SYSTEM**

Subtitle:

**Turn Food Waste into Smart Decisions with Artificial Intelligence**

Description:

"Monitor your food, predict waste risks, receive intelligent recommendations, and build a more sustainable future."

Buttons:

**GET STARTED**

**LEARN MORE**

Add a beautiful food/sustainability/AI illustration or visual element.

Include floating statistics such as:

```text
40%
Waste Reduction

AI Powered
Prediction

Smart
Recommendations
```

---

# 7. ABOUT FOOD WASTE SECTION

Heading:

**Why Food Waste Matters**

Explain briefly:

- Food waste wastes valuable resources.
- It increases environmental pollution.
- It wastes money.
- Better planning can significantly reduce unnecessary waste.

Create 3 or 4 cards:

```text
Food Loss
Environmental Impact
Money Wasted
Sustainable Future
```

Use appropriate icons.

---

# 8. AI FEATURES SECTION

Heading:

**Powerful AI Features**

Create feature cards for:

### AI Waste Prediction

Predict whether food has:

- Low waste risk
- Medium waste risk
- High waste risk

### Smart Recommendations

Provide personalized actions based on prediction.

### Food Monitoring

Track food quantity and expiry dates.

### Waste Analytics

Show statistics and trends.

### Expiry Awareness

Help users identify food approaching expiry.

### Reports

Generate useful food waste reports.

Each card should contain:

- Icon
- Title
- Description
- Hover effect

---

# 9. HOW IT WORKS SECTION

Create a beautiful step-by-step timeline.

Show:

```text
01
Create Account
       ↓
02
Enter Food Information
       ↓
03
AI Analyzes Food
       ↓
04
Waste Risk Prediction
       ↓
05
Smart Recommendations
       ↓
06
Reduce Food Waste
```

Use connecting lines/arrows.

---

# 10. BENEFITS SECTION

Create cards:

```text
Reduce Food Waste
Save Money
Improve Food Management
Protect Environment
Make Better Decisions
Track Progress
```

---

# 11. CALL-TO-ACTION SECTION

Create a strong CTA:

**Ready to Reduce Food Waste?**

Text:

"Start using AI-powered food waste management today."

Button:

**START NOW**

---

# 12. FOOTER

Footer should contain:

```text
AI FOOD WASTE REDUCTION SYSTEM

Smart Technology for a Sustainable Future

Quick Links
Home
About
Features
How It Works
Login

Contact
Email
Phone

© 2026 AI Food Waste Reduction System
```

---

# 13. LOGIN PAGE — login.html

Create a modern login interface.

Left side:

- Food/AI/environment illustration
- Project title
- Short motivational message

Right side:

```text
Welcome Back!

Email
[________________]

Password
[________________]

☐ Remember Me

[ LOGIN ]

Forgot Password?

Don't have an account?
Create Account
```

Add password show/hide icon.

Include validation messages.

Make the design professional.

---

# 14. SIGNUP PAGE — signup.html

Create:

```text
Create Your Account

Full Name
Email
Password
Confirm Password

☐ I agree to the Terms and Conditions

[ CREATE ACCOUNT ]

Already have an account?
Login
```

Add password strength indicator.

Show validation errors clearly.

---

# 15. DASHBOARD — dashboard.html

Create a professional AI dashboard.

Sidebar:

```text
Dashboard
Food Entry
Predictions
Recommendations
Reports
Profile
Logout
```

Top navigation:

```text
Welcome, User 👋
Notifications
Profile
```

Main dashboard:

## Statistics Cards

```text
Total Food Entries
25

High Risk Foods
8

Food Saved
17 kg

Waste Reduction
68%
```

Use attractive icons.

---

# 16. DASHBOARD CHARTS

Create charts using Chart.js.

### Chart 1

**Food Waste Risk Distribution**

Pie/doughnut chart:

```text
Low
Medium
High
```

### Chart 2

**Monthly Food Waste Trend**

Line chart.

### Chart 3

**Food Category Analysis**

Bar chart.

Use sample data in frontend initially.

Later the Flask backend will replace sample data with database data.

---

# 17. RECENT FOOD ENTRIES

Create a table:

```text
Food
Category
Quantity
Expiry
Risk
Status
Action
```

Example:

```text
Tomato
Vegetable
2 kg
2 days
High
Analyze

Milk
Dairy
1 L
4 days
Medium
View

Rice
Grain
5 kg
20 days
Low
View
```

Add:

**VIEW ALL**

button.

---

# 18. FOOD ENTRY PAGE — food_entry.html

Create a beautiful form.

Heading:

**Enter Food Information**

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
```

Dropdowns:

Food Category:

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

Storage:

```text
Refrigerator
Freezer
Room Temperature
Pantry
Other
```

Add:

**Upload Food Image**

with drag-and-drop interface.

Button:

**ANALYZE FOOD WITH AI**

---

# 19. IMAGE UPLOAD UI

Create a professional upload component:

```text
┌─────────────────────────────┐
│                             │
│        📷 Upload Image      │
│                             │
│ Drag & Drop Image Here      │
│ or                          │
│ Browse Files                │
│                             │
└─────────────────────────────┘
```

Show image preview after selecting a file.

Only allow suitable image formats such as:

```text
JPG
JPEG
PNG
WEBP
```

---

# 20. PREDICTION PAGE — prediction.html

Create an AI analysis result screen.

Heading:

**AI FOOD WASTE PREDICTION**

Show:

```text
Food:
Tomatoes

Quantity:
2 KG

Expiry:
2 Days Remaining
```

Large prediction card:

```text
AI PREDICTION

HIGH WASTE RISK

87% Confidence
```

Create a visual risk meter.

Show:

```text
LOW       MEDIUM       HIGH
----------------------------●
```

Add buttons:

**VIEW RECOMMENDATIONS**

**BACK TO DASHBOARD**

---

# 21. RECOMMENDATIONS PAGE

Heading:

**SMART RECOMMENDATIONS**

Display personalized cards.

Example:

```text
⚠ High Waste Risk

Recommended Actions:

✓ Consume the food soon
✓ Store under recommended conditions
✓ Avoid purchasing excess quantity
✓ Consider meal planning
✓ Consider donation if food is safe
```

Also create:

**Food Storage Tips**

**Meal Planning Tips**

**Purchase Planning Tips**

---

# 22. REPORTS PAGE — reports.html

Heading:

**FOOD WASTE REPORTS**

Statistics:

```text
Total Food Added
Total Food Saved
Total Waste
Waste Reduction %
```

Charts:

- Weekly Waste
- Monthly Waste
- Food Category Waste
- Prediction Distribution

Add:

```text
[ DOWNLOAD REPORT ]
```

button.

Also include a filter:

```text
Today
This Week
This Month
This Year
Custom Date
```

---

# 23. PROFILE PAGE — profile.html

Create:

```text
My Profile

Profile Image

Full Name
Email
Account Created

Statistics:

Food Entries
Predictions
Recommendations
Waste Reduced
```

Buttons:

```text
Edit Profile
Change Password
Logout
```

---

# 24. ADMIN DASHBOARD — admin.html

Create a separate professional admin interface.

Sidebar:

```text
Admin Dashboard
Users
Food Entries
Predictions
Reports
System Settings
Logout
```

Statistics:

```text
Total Users
Total Food Entries
Total Predictions
High Risk Predictions
```

Create tables:

### Users

```text
ID
Name
Email
Role
Joined Date
Status
Action
```

### Food Entries

```text
User
Food
Category
Quantity
Prediction
Date
Action
```

Add search and filtering.

---

# 25. ERROR PAGES

Create:

### 404.html

```text
404

Page Not Found

The page you're looking for doesn't exist.

[ BACK TO HOME ]
```

### 500.html

```text
500

Something Went Wrong

Please try again later.

[ BACK TO HOME ]
```

Use the same project branding.

---

# 26. JAVASCRIPT REQUIREMENTS

Create:

```text
static/js/script.js
```

Implement frontend functionality for:

- Mobile navigation
- Form validation
- Password show/hide
- Password strength
- Image preview
- Drag-and-drop image upload
- Alert messages
- Modal windows
- Dashboard chart initialization
- Search/filter UI
- Sidebar toggle
- Smooth scrolling
- Loading animation
- AI analysis loading state

When the user clicks:

**ANALYZE FOOD WITH AI**

show:

```text
Analyzing Food...

AI is processing your food information...
```

with a loading animation.

Later this button will send data to Flask.

---

# 27. BACKEND-READY FRONTEND

VERY IMPORTANT:

Design the frontend so that it can later connect to Flask.

Use forms with appropriate names and IDs.

Example:

```html
<form method="POST" action="/predict">
```

Use meaningful field names:

```text
food_name
category
quantity
unit
purchase_date
expiry_date
storage_type
temperature
previous_waste
food_image
```

Do not hardcode the final prediction.

Initially use sample frontend data, but structure the page so Flask can replace it dynamically.

---

# 28. ACCESSIBILITY

Implement:

- Proper labels
- Keyboard navigation
- Alt text for images
- Good color contrast
- Readable fonts
- Clear error messages
- Focus states
- Accessible buttons

---

# 29. ANIMATIONS

Use subtle professional animations:

- Fade-in
- Slide-up
- Card hover
- Button hover
- Progress animation
- Chart animation
- Page transitions

Do NOT overuse animations.

The website should feel fast and professional.

---

# 30. PERFORMANCE

Optimize the frontend:

- Avoid unnecessary libraries.
- Compress large images.
- Use reusable CSS classes.
- Avoid duplicated code.
- Keep JavaScript organized.
- Use semantic HTML.
- Make the website fast on mobile.

---

# 31. IMPORTANT UI REQUIREMENT

Every page must look like it belongs to the SAME application.

Maintain consistent:

- Navbar
- Sidebar
- Colors
- Typography
- Buttons
- Cards
- Icons
- Footer
- Spacing
- Border radius
- Shadows

Do not create unrelated designs for different pages.

---

# 32. NAVIGATION FLOW

Implement this complete navigation:

```text
HOME
 ↓
GET STARTED
 ↓
LOGIN / SIGNUP
 ↓
DASHBOARD
 ↓
FOOD ENTRY
 ↓
AI ANALYSIS
 ↓
PREDICTION
 ↓
RECOMMENDATIONS
 ↓
DASHBOARD
 ↓
REPORTS
```

Additional:

```text
Dashboard → Profile
Dashboard → Logout
Admin → Users
Admin → Food Entries
Admin → Reports
```

---

# 33. SAMPLE DATA

Use realistic sample data for frontend demonstration.

Example:

```text
Tomatoes
Milk
Rice
Apples
Bread
Vegetables
Chicken
Potatoes
```

Use realistic quantities, expiry dates, and prediction levels.

Clearly structure the code so these sample values can later be replaced by Flask/database data.

---

# 34. FINAL QUALITY REQUIREMENT

Do not generate a basic student-level website.

Create a **professional, modern, colorful AI + sustainability themed web application** suitable for demonstrating a final-year/college project.

The final frontend must look polished enough for:

- College project demonstration
- Faculty review
- Viva
- Portfolio
- Hackathon
- Internship presentation

Before finishing:

1. Check every page.
2. Check every navigation link.
3. Check responsive design.
4. Check forms.
5. Check buttons.
6. Check charts.
7. Check image upload UI.
8. Check mobile layout.
9. Remove broken links.
10. Remove placeholder errors.
11. Keep CSS and JavaScript organized.
12. Make everything ready for Flask integration.

## FINAL INSTRUCTION

Start from scratch and generate the complete frontend implementation for the **AI FOOD WASTE REDUCTION SYSTEM**.

Create all required HTML, CSS, JavaScript, image placeholders/assets structure, navigation, responsive layouts, forms, dashboard, charts, prediction UI, recommendation UI, reports, profile, admin panel, authentication pages, error pages, and Flask-ready form structures.

Do not stop after creating the homepage.

Build the **entire frontend from beginning to end**, keeping the code clean, modular, professional, responsive, and ready to connect to the Flask backend and database in the next development stage.
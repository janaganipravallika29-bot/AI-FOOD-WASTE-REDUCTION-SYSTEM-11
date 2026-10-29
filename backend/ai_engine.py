"""
FoodWise AI - AI Waste Risk Prediction & Recommendations Engine
Computes risk scores, predicts shelf-life, and generates food rescue recommendations.
"""
from datetime import datetime

FOOD_KNOWLEDGE = {
    'dairy': {
        'spoilage_rate': 4,
        'ideal_storage': 'refrigerator',
        'tips': ['Keep in main fridge compartment, not door shelves where temperature fluctuates.', 'Can freeze before expiry for cooking or baking.'],
        'recipes': ['Homemade Paneer', 'Pancake Batter', 'Cream Soup Base']
    },
    'meat': {
        'spoilage_rate': 2,
        'ideal_storage': 'refrigerator',
        'tips': ['Freeze raw meat immediately if not cooking within 48 hours.', 'Keep in lowest shelf to avoid cross-contamination.'],
        'recipes': ['Stir Fry', 'Slow-cooked Stew', 'Curry or Marinade']
    },
    'vegetables': {
        'spoilage_rate': 5,
        'ideal_storage': 'refrigerator',
        'tips': ['Store away from ethylene-producing fruits like apples and bananas.', 'Wrap greens in paper towels to absorb excess moisture.'],
        'recipes': ['Vegetable Broth', 'Roasted Veggie Medley', 'Stir Fry']
    },
    'fruits': {
        'spoilage_rate': 4,
        'ideal_storage': 'refrigerator',
        'tips': ['Freeze overripe berries or bananas for morning smoothies.', 'Store citrus at cool room temp or crisper drawer.'],
        'recipes': ['Fruit Smoothie', 'Fruit Compote or Jam', 'Baked Dessert Topping']
    },
    'bakery': {
        'spoilage_rate': 4,
        'ideal_storage': 'pantry',
        'tips': ['Freeze sliced bread and toast directly from freezer.', 'Stale bread makes excellent breadcrumbs or croutons.'],
        'recipes': ['Crispy Garlic Croutons', 'French Toast', 'Bread Pudding']
    },
    'grains': {
        'spoilage_rate': 180,
        'ideal_storage': 'pantry',
        'tips': ['Store in airtight containers in a cool, dark cupboard.', 'Cooked grains must be chilled within 2 hours.'],
        'recipes': ['Fried Rice', 'Grain Salad', 'Rice Pudding']
    },
    'other': {
        'spoilage_rate': 7,
        'ideal_storage': 'pantry',
        'tips': ['Check label expiration dates and store in cool, dry conditions.'],
        'recipes': ['Mixed Casserole', 'Soup Integration']
    }
}


def calculate_waste_risk(food_name, category, quantity, storage_type, expiry_date_str=None, purchase_date_str=None):
    """
    Calculate 0-100 waste risk score, risk level ('low', 'medium', 'high'),
    confidence score, and tailored rescue recommendations.
    """
    cat = (category or 'other').lower()
    profile = FOOD_KNOWLEDGE.get(cat, FOOD_KNOWLEDGE['other'])
    storage = (storage_type or 'refrigerator').lower()

    # Calculate days until expiry
    days_left = 3
    if expiry_date_str:
        try:
            today = datetime.utcnow().date()
            exp = datetime.strptime(expiry_date_str.split('T')[0], '%Y-%m-%d').date()
            days_left = (exp - today).days
        except Exception:
            days_left = 3

    score = 0

    # 1. Expiry date urgency
    if days_left <= 0:
        score += 55
    elif days_left == 1:
        score += 48
    elif days_left == 2:
        score += 40
    elif days_left == 3:
        score += 30
    elif days_left <= 5:
        score += 18
    elif days_left <= 7:
        score += 10
    else:
        score += 4

    # 2. Category Perishability
    if cat == 'meat':
        score += 24
    elif cat == 'dairy':
        score += 18
    elif cat in ('vegetables', 'fruits'):
        score += 14
    elif cat == 'bakery':
        score += 12
    else:
        score += 4

    # 3. Storage Appropriateness
    ideal = profile['ideal_storage']
    if storage != ideal:
        if ideal == 'refrigerator' and storage in ('countertop', 'pantry'):
            score += 22  # High risk of bacterial growth
        elif ideal == 'pantry' and storage == 'refrigerator':
            score += 6
        elif storage == 'freezer':
            score -= 16  # Freezing substantially extends shelf life

    # 4. Quantity factor
    try:
        qty = float(quantity)
        if qty > 4:
            score += 10
        elif qty > 2:
            score += 5
    except Exception:
        pass

    # Normalize score between 0 and 99
    score = max(5, min(99, score))

    if score >= 65:
        risk_level = 'high'
    elif score >= 35:
        risk_level = 'medium'
    else:
        risk_level = 'low'

    confidence = round(0.85 + (0.001 * (score % 10)), 2)

    return {
        'score': score,
        'risk': risk_level,
        'days_left': days_left,
        'confidence': confidence,
        'storage_match': storage == ideal,
        'tips': profile['tips'],
        'recipes': profile['recipes']
    }


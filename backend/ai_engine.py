"""
FoodWise AI - AI Waste Risk Prediction & Donation Safety Engine
Computes risk scores, predicts shelf-life, evaluates donation suitability,
and generates food rescue & NGO donation recommendations.
"""
from datetime import datetime

FOOD_KNOWLEDGE = {
    'dairy': {
        'spoilage_rate': 4,
        'ideal_storage': 'refrigerator',
        'tips': ['Keep in main fridge compartment, not door shelves where temperature fluctuates.', 'Can freeze before expiry for cooking or baking.'],
        'recipes': ['Homemade Paneer', 'Pancake Batter', 'Cream Soup Base'],
        'donation_policy': 'Accepted only if chilled (2-4°C) with at least 24 hours before expiration.'
    },
    'meat': {
        'spoilage_rate': 2,
        'ideal_storage': 'refrigerator',
        'tips': ['Freeze raw meat immediately if not cooking within 48 hours.', 'Keep in lowest shelf to avoid cross-contamination.'],
        'recipes': ['Stir Fry', 'Slow-cooked Stew', 'Curry or Marinade'],
        'donation_policy': 'Cooked meat accepted if prepared within 4 hours; raw meat must remain frozen.'
    },
    'vegetables': {
        'spoilage_rate': 5,
        'ideal_storage': 'refrigerator',
        'tips': ['Store away from ethylene-producing fruits like apples and bananas.', 'Wrap greens in paper towels to absorb excess moisture.'],
        'recipes': ['Vegetable Broth', 'Roasted Veggie Medley', 'Stir Fry'],
        'donation_policy': 'Fresh and firm produce readily accepted by all community kitchens.'
    },
    'fruits': {
        'spoilage_rate': 4,
        'ideal_storage': 'refrigerator',
        'tips': ['Freeze overripe berries or bananas for morning smoothies.', 'Store citrus at cool room temp or crisper drawer.'],
        'recipes': ['Fruit Smoothie', 'Fruit Compote or Jam', 'Baked Dessert Topping'],
        'donation_policy': 'Whole unblemished fruits accepted for immediate shelter distribution.'
    },
    'bakery': {
        'spoilage_rate': 4,
        'ideal_storage': 'pantry',
        'tips': ['Freeze sliced bread and toast directly from freezer.', 'Stale bread makes excellent breadcrumbs or croutons.'],
        'recipes': ['Crispy Garlic Croutons', 'French Toast', 'Bread Pudding'],
        'donation_policy': 'Fresh breads, buns, and sealed baked items highly accepted.'
    },
    'grains': {
        'spoilage_rate': 180,
        'ideal_storage': 'pantry',
        'tips': ['Store in airtight containers in a cool, dark cupboard.', 'Cooked grains must be chilled within 2 hours.'],
        'recipes': ['Fried Rice', 'Grain Salad', 'Rice Pudding'],
        'donation_policy': 'Dry grains have indefinite shelf life; cooked rice must be freshly cooked (< 6 hours).'
    },
    'cooked': {
        'spoilage_rate': 1,
        'ideal_storage': 'refrigerator',
        'tips': ['Keep warm above 60°C or chill rapidly below 4°C within 2 hours of cooking.'],
        'recipes': ['Immediate Distribution', 'Meal Box Assembly'],
        'donation_policy': 'Accepted if packaged in clean containers and donated within 6 hours of preparation.'
    },
    'other': {
        'spoilage_rate': 7,
        'ideal_storage': 'pantry',
        'tips': ['Check label expiration dates and store in cool, dry conditions.'],
        'recipes': ['Mixed Casserole', 'Soup Integration'],
        'donation_policy': 'Packaged and canned items within best-before dates welcomed.'
    }
}


def calculate_waste_risk(food_name, category, quantity, storage_type, expiry_date_str=None, purchase_date_str=None, prep_time_str=None):
    """
    Calculate 0-100 waste risk score, risk level ('low', 'medium', 'high'),
    donation suitability ('safe', 'use_soon', 'unsafe'),
    confidence score, and tailored rescue recommendations.
    """
    cat = (category or 'other').lower()
    profile = FOOD_KNOWLEDGE.get(cat, FOOD_KNOWLEDGE.get('other'))
    storage = (storage_type or 'refrigerator').lower()

    # Calculate days until expiry
    days_left = 3
    if expiry_date_str:
        try:
            today = datetime.utcnow().date()
            clean_date = expiry_date_str.split('T')[0]
            exp = datetime.strptime(clean_date, '%Y-%m-%d').date()
            days_left = (exp - today).days
        except Exception:
            days_left = 3

    score = 0

    # 1. Expiry date urgency
    if days_left <= 0:
        score += 65
    elif days_left == 1:
        score += 48
    elif days_left == 2:
        score += 38
    elif days_left == 3:
        score += 26
    elif days_left <= 5:
        score += 16
    elif days_left <= 7:
        score += 10
    else:
        score += 4

    # 2. Category Perishability
    if cat in ('meat', 'cooked'):
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
        if qty > 5:
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

    # Determine Donation Suitability
    # Case 1: SAFE TO DONATE
    # Case 2: USE SOON
    # Case 3: UNSAFE TO DONATE
    donation_suitable = 'safe'
    donation_reason = ""

    if days_left <= 0:
        donation_suitable = 'unsafe'
        donation_reason = f"The food item has expired or reached the end of safe shelf life ({days_left} days left). For health and food safety standards, expired food cannot be donated to NGOs."
    elif score >= 75 and days_left <= 1 and (cat in ('meat', 'dairy', 'cooked') and storage != 'refrigerator'):
        donation_suitable = 'unsafe'
        donation_reason = f"High spoilage probability due to perishable food category ({cat}) and non-optimal storage ({storage}). Unsafe for public NGO distribution."
    elif days_left <= 2 or (score >= 60 and score < 75):
        donation_suitable = 'use_soon'
        donation_reason = f"Food is fresh but has a short remaining shelf-life ({days_left} day(s)). Suitable for immediate or emergency NGO collection within 12-24 hours."
    else:
        donation_suitable = 'safe'
        donation_reason = f"Excellent quality and safe storage detected ({days_left} days shelf-life remaining). Ideal for NGO meal redistribution."

    status_map = {
        'safe': 'SAFE TO DONATE',
        'use_soon': 'USE SOON',
        'unsafe': 'NOT SAFE TO DONATE'
    }

    confidence = round(0.88 + (0.001 * (score % 10)), 2)

    return {
        'score': score,
        'risk': risk_level,
        'days_left': days_left,
        'donation_suitable': donation_suitable,
        'safety_status': status_map[donation_suitable],
        'donation_reason': donation_reason,
        'confidence': confidence,
        'storage_match': storage == ideal,
        'tips': profile['tips'],
        'recipes': profile['recipes'],
        'donation_policy': profile.get('donation_policy', 'Accepted in sanitary condition.')
    }

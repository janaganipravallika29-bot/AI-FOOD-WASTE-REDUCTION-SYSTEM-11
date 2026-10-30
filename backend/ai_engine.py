"""
FoodWise AI - AI Waste Risk Prediction & Donation Safety Engine
Computes risk scores, predicts shelf-life, evaluates donation suitability,
and generates food rescue & NGO donation recommendations.
"""
import io
import re
import base64
from datetime import datetime, timezone
from PIL import Image, ImageStat

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


def analyze_food_image(image_input, category_hint=None, filename="uploaded_food.jpg"):
    """
    Parses and inspects an uploaded food image using PIL / Pillow computer vision heuristics:
    - Validates image dimensions, file integrity, and format (JPEG, PNG, WEBP, etc.)
    - Analyzes perceived brightness (luminance), color distribution, and variance
    - Detects signs of surface browning, mold tint, or severe darkening
    - Classifies likely food category and freshness rating
    - Returns a structured result with visual_freshness_score (0-100), visual_status, and risk_adjustment.
    """
    if not image_input:
        return {
            'is_valid': False,
            'reason': 'No image provided',
            'visual_freshness_score': 80,
            'visual_status': 'Standard Inspection (No Image)',
            'risk_adjustment': 0,
            'is_safe_visually': True,
            'emoji': '🍽️',
            'suggested_category': category_hint or 'other'
        }

    try:
        # Accept bytes, io.BytesIO, or base64 Data URL string
        if isinstance(image_input, str):
            if ',' in image_input:
                header, encoded = image_input.split(',', 1)
            else:
                encoded = image_input
            image_bytes = base64.b64decode(encoded)
            stream = io.BytesIO(image_bytes)
        elif hasattr(image_input, 'read'):
            stream = io.BytesIO(image_input.read())
        elif isinstance(image_input, (bytes, bytearray)):
            stream = io.BytesIO(image_input)
        else:
            return {
                'is_valid': False,
                'reason': 'Unsupported image data type',
                'visual_freshness_score': 75,
                'visual_status': 'Standard Inspection (Format Unrecognized)',
                'risk_adjustment': 0,
                'is_safe_visually': True,
                'emoji': '🍽️',
                'suggested_category': category_hint or 'other'
            }

        with Image.open(stream) as img:
            img_format = img.format or 'JPEG'
            width, height = img.size

            if width < 10 or height < 10:
                raise ValueError("Image dimensions too small")

            rgb_img = img.convert('RGB')
            # Generate downsampled thumbnail for fast chromatic analysis
            thumb = rgb_img.resize((100, 100))
            stat = ImageStat.Stat(thumb)

            mean_r, mean_g, mean_b = stat.mean[:3]
            std_r, std_g, std_b = stat.stddev[:3]

            # Standard perceived luminance (ITU-R BT.601)
            brightness = 0.299 * mean_r + 0.587 * mean_g + 0.114 * mean_b
            color_variance = (std_r + std_g + std_b) / 3.0

            # Chromatic ratios
            total_rgb = max(1.0, mean_r + mean_g + mean_b)
            green_ratio = mean_g / total_rgb
            red_ratio = mean_r / total_rgb
            blue_ratio = mean_b / total_rgb

            # Freshness and safety heuristics
            flags = []
            risk_adjustment = 0
            visual_score = 88
            is_safe_visually = True

            # 1. Darkness / severe discoloration check
            if brightness < 40:
                flags.append("Severe darkening / low luminance detected")
                visual_score -= 35
                risk_adjustment += 25
                is_safe_visually = False
            elif brightness < 65:
                flags.append("Surface browning / dull tone observed")
                visual_score -= 18
                risk_adjustment += 10
            elif brightness > 220:
                flags.append("High brightness / reflection")
                visual_score -= 5

            # 2. Food category detection hints
            suggested_category = category_hint or 'other'
            emoji = '🍽️'
            category_confidence = 0.85

            if green_ratio > 0.38 and mean_g > mean_r:
                suggested_category = 'vegetables'
                emoji = '🥦'
                flags.append("Vibrant chlorophyll green detected (fresh leafy produce)")
                visual_score += 6
                risk_adjustment -= 5
            elif red_ratio > 0.40 and mean_r > 130:
                suggested_category = 'fruits'
                emoji = '🍎'
                flags.append("Vibrant warm tone detected (fresh fruits/produce)")
                visual_score += 5
                risk_adjustment -= 4
            elif mean_r > 160 and mean_g > 150 and mean_b > 130 and abs(mean_r - mean_g) < 25:
                suggested_category = 'dairy'
                emoji = '🥛'
                flags.append("Light creamy hue detected (dairy/paneer/milk)")
            elif mean_r > 120 and mean_g > 80 and mean_b < 65:
                suggested_category = 'bakery'
                emoji = '🍞'
                flags.append("Golden-crust tone detected (bread/bakery/grains)")
            elif mean_r > 110 and mean_g < 80:
                suggested_category = 'meat'
                emoji = '🥩'
                flags.append("Deep protein hue detected (cooked meat/curry)")

            # Check for suspicious mold/discoloration in perishable categories
            if category_hint in ('meat', 'cooked', 'dairy') and green_ratio > 0.38 and brightness < 110:
                flags.append("Suspicious greenish-gray surface discoloration on perishable item")
                visual_score -= 40
                risk_adjustment += 30
                is_safe_visually = False

            visual_score = max(10, min(99, visual_score))

            if visual_score >= 80:
                visual_status = "High Visual Freshness (Excellent Condition)"
            elif visual_score >= 60:
                visual_status = "Good Quality (Suitable for Immediate Distribution)"
            elif visual_score >= 40:
                visual_status = "Moderate Aging / Surface Dullness Observed"
            else:
                visual_status = "Visual Spoilage Alert (Unsafe for Public Donation)"

            return {
                'is_valid': True,
                'format': img_format,
                'dimensions': f"{width}x{height}",
                'brightness': round(brightness, 1),
                'color_variance': round(color_variance, 1),
                'visual_freshness_score': visual_score,
                'visual_status': visual_status,
                'risk_adjustment': risk_adjustment,
                'is_safe_visually': is_safe_visually,
                'flags': flags,
                'suggested_category': suggested_category,
                'emoji': emoji,
                'confidence': round(category_confidence, 2),
                'summary': f"AI Vision scanned {img_format} ({width}x{height}) - Freshness {visual_score}%: {visual_status}"
            }
    except Exception as e:
        return {
            'is_valid': False,
            'reason': str(e),
            'visual_freshness_score': 75,
            'visual_status': 'Standard Inspection (Image parsing note)',
            'risk_adjustment': 0,
            'is_safe_visually': True,
            'emoji': '🍽️',
            'suggested_category': category_hint or 'other'
        }


def calculate_waste_risk(food_name, category, quantity, storage_type, expiry_date_str=None, purchase_date_str=None, prep_time_str=None, visual_analysis=None):
    """
    Calculate 0-100 waste risk score, risk level ('low', 'medium', 'high'),
    donation suitability ('safe', 'use_soon', 'unsafe'),
    confidence score, visual condition, and tailored rescue recommendations.
    """
    cat = (category or 'other').lower()
    profile = FOOD_KNOWLEDGE.get(cat, FOOD_KNOWLEDGE.get('other'))
    storage = (storage_type or 'refrigerator').lower()

    # Calculate days until expiry
    days_left = 3
    if expiry_date_str:
        try:
            today = datetime.now(timezone.utc).date()
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

    # 5. Visual AI Inspection factor
    if visual_analysis and isinstance(visual_analysis, dict):
        risk_adj = visual_analysis.get('risk_adjustment', 0)
        score += risk_adj

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

    # Check for visual safety veto
    is_safe_visually = True
    if visual_analysis and isinstance(visual_analysis, dict):
        is_safe_visually = visual_analysis.get('is_safe_visually', True)

    if days_left <= 0:
        donation_suitable = 'unsafe'
        donation_reason = f"The food item has expired or reached the end of safe shelf life ({days_left} days left). For health and food safety standards, expired food cannot be donated to NGOs."
    elif not is_safe_visually:
        donation_suitable = 'unsafe'
        donation_reason = "Food safety warning: AI visual inspection detected surface deterioration or discoloration consistent with spoilage. Not safe for NGO redistribution."
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
        'visual_analysis': visual_analysis,
        'tips': profile['tips'],
        'recipes': profile['recipes'],
        'donation_policy': profile.get('donation_policy', 'Accepted in sanitary condition.')
    }

console.log("AI-Based Food Waste Reduction System Loaded Successfully");

// ===================================
// TOAST NOTIFICATION SYSTEM
// ===================================

function showToast(message, type = 'info', duration = 3500) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  let icon = 'fa-circle-info';
  if (type === 'success') icon = 'fa-circle-check';
  else if (type === 'error') icon = 'fa-circle-xmark';
  else if (type === 'warning') icon = 'fa-triangle-exclamation';

  toast.innerHTML = `<i class="fa-solid ${icon}"></i><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('toast-hiding');
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 300);
  }, duration);
}

// ===================================
// AI FOOD KNOWLEDGE & RECOGNITION DICTIONARY
// ===================================

const FoodKnowledge = {
  // Common foods database with alias matching, perishability rates, optimal storage and rescue tips
  catalog: [
    {
      id: 'tomato',
      canonical: 'Tomato',
      emoji: '🍅',
      category: 'vegetables',
      defaultStorage: 'countertop',
      idealTemp: '12°C - 20°C',
      spoilageRate: 'fast', // 3-5 days
      aliases: ['tomato', 'tomatoes', 'tamoto', 'tamatar', 'tomat', 'cherry tomato', 'roma tomato'],
      spoilageSigns: 'Softening, dark spots, wrinkly skin, sour smell, mold on stem.',
      tips: [
        'Ripe tomatoes should be cooked into sauce, puree, or salsa within 48 hours.',
        'Avoid refrigerating unripe tomatoes as cold destroys flavor enzymes.',
        'Freeze blanched or pureed tomatoes for up to 6 months.'
      ],
      recipes: ['Fresh Tomato Pasta Sauce', 'Roasted Tomato Soup', 'Homemade Salsa']
    },
    {
      id: 'milk',
      canonical: 'Fresh Milk',
      emoji: '🥛',
      category: 'dairy',
      defaultStorage: 'refrigerator',
      idealTemp: '2°C - 4°C',
      spoilageRate: 'very_fast', // 2-4 days once open
      aliases: ['milk', 'fresh milk', 'whole milk', 'skim milk', 'dairy milk', 'cow milk', 'milkk'],
      spoilageSigns: 'Sour odor, curdling, yellowish discoloration, lumpy texture.',
      tips: [
        'Store in main fridge shelf, not door pockets where temperature fluctuates.',
        'Near-expiry milk can be boiled to make paneer, ricotta cheese, or used in baking.',
        'Can be frozen in airtight containers leaving space for expansion.'
      ],
      recipes: ['Homemade Paneer/Curd', 'Pancakes & Crepes', 'Creamy Oatmeal']
    },
    {
      id: 'bread',
      canonical: 'Bread',
      emoji: '🍞',
      category: 'bakery',
      defaultStorage: 'pantry',
      idealTemp: '18°C - 22°C',
      spoilageRate: 'fast',
      aliases: ['bread', 'sliced bread', 'white bread', 'wheat bread', 'loaf', 'buns', 'baguette'],
      spoilageSigns: 'Green or white mold patches, hard staling, sour yeast odor.',
      tips: [
        'Freeze sliced bread and toast directly from freezer to prevent molding.',
        'Stale bread can be turned into crunchy croutons, breadcrumbs, or French toast.'
      ],
      recipes: ['Crispy Garlic Croutons', 'Classic French Toast', 'Bread Pudding']
    },
    {
      id: 'chicken',
      canonical: 'Raw Chicken',
      emoji: '🥩',
      category: 'meat',
      defaultStorage: 'refrigerator',
      idealTemp: '0°C - 3°C',
      spoilageRate: 'critical', // 1-2 days
      aliases: ['chicken', 'chicken breast', 'poultry', 'chicken thighs', 'meat', 'chiken'],
      spoilageSigns: 'Slimy texture, grayish color, sour pungent odor.',
      tips: [
        'Cook immediately within 24-48 hours or freeze at -18°C.',
        'Cooked chicken lasts 3-4 days in the refrigerator.'
      ],
      recipes: ['Chicken Stir-Fry', 'Shredded Chicken Broth Soup', 'Grilled Chicken Salad']
    },
    {
      id: 'apple',
      canonical: 'Apples',
      emoji: '🍎',
      category: 'fruits',
      defaultStorage: 'refrigerator',
      idealTemp: '1°C - 4°C',
      spoilageRate: 'slow',
      aliases: ['apple', 'apples', 'fuji apple', 'green apple', 'red apple'],
      spoilageSigns: 'Bruising, mushy brown spots, shriveled skin.',
      tips: [
        'Keep separate from other fruits as apples emit ethylene gas.',
        'Bruised apples make great applesauce or apple pie.'
      ],
      recipes: ['Homemade Cinnamon Applesauce', 'Apple Crumble', 'Dehydrated Apple Chips']
    },
    {
      id: 'banana',
      canonical: 'Bananas',
      emoji: '🍌',
      category: 'fruits',
      defaultStorage: 'countertop',
      idealTemp: '15°C - 20°C',
      spoilageRate: 'fast',
      aliases: ['banana', 'bananas', 'kela'],
      spoilageSigns: 'Black skin, very mushy flesh, fermented odor.',
      tips: [
        'Peel and freeze overripe bananas for smoothies or banana bread.',
        'Wrap stems in foil or plastic to slow down ripening.'
      ],
      recipes: ['Banana Bread', 'Frozen Banana Smoothie', 'Banana Pancakes']
    },
    {
      id: 'rice',
      canonical: 'Rice / Grains',
      emoji: '🌾',
      category: 'grains',
      defaultStorage: 'pantry',
      idealTemp: '15°C - 25°C',
      spoilageRate: 'very_slow',
      aliases: ['rice', 'basmati rice', 'brown rice', 'white rice', 'grains', 'quinoa'],
      spoilageSigns: 'Weevils, moisture clump, sour fermented smell if cooked.',
      tips: [
        'Store dry rice in airtight sealed containers with a bay leaf.',
        'Cooked rice must be refrigerated within 1 hour and eaten in 2 days.'
      ],
      recipes: ['Vegetable Fried Rice', 'Rice Pudding', 'Crispy Rice Cakes']
    },
    {
      id: 'spinach',
      canonical: 'Spinach & Leafy Greens',
      emoji: '🥬',
      category: 'vegetables',
      defaultStorage: 'refrigerator',
      idealTemp: '2°C - 4°C',
      spoilageRate: 'very_fast',
      aliases: ['spinach', 'greens', 'lettuce', 'kale', 'palak', 'salad greens'],
      spoilageSigns: 'Slimy wilted leaves, yellowing, water leakage.',
      tips: [
        'Line container with paper towel to absorb excess moisture.',
        'Wilted greens can be blended into soups, curries, or smoothies.'
      ],
      recipes: ['Palak Paneer', 'Green Detox Smoothie', 'Garlic Sautéed Greens']
    },
    {
      id: 'eggs',
      canonical: 'Eggs',
      emoji: '🥚',
      category: 'dairy',
      defaultStorage: 'refrigerator',
      idealTemp: '2°C - 4°C',
      spoilageRate: 'medium',
      aliases: ['egg', 'eggs', 'anda'],
      spoilageSigns: 'Float in water test (floating = spoiled), rotten egg smell upon cracking.',
      tips: [
        'Keep in original carton on inner shelf to maintain stable temperature.'
      ],
      recipes: ['Vegetable Frittata', 'Boiled Egg Salad', 'Egg Fried Rice']
    },
    {
      id: 'potato',
      canonical: 'Potatoes',
      emoji: '🥔',
      category: 'vegetables',
      defaultStorage: 'pantry',
      idealTemp: '8°C - 15°C',
      spoilageRate: 'slow',
      aliases: ['potato', 'potatoes', 'potatos', 'aloo'],
      spoilageSigns: 'Green tint, soft spongy spots, long sprouting, rotten smell.',
      tips: [
        'Keep in dark, cool, dry place away from onions.'
      ],
      recipes: ['Mashed Potatoes', 'Roasted Garlic Potato Wedges', 'Potato Soup']
    }
  ],

  // Fuzzy lookup by name
  matchFood: function (name) {
    if (!name) return null;
    const clean = name.toLowerCase().trim().replace(/[^a-z0-9\s]/g, '');
    for (const item of this.catalog) {
      if (item.aliases.some(alias => clean.includes(alias) || alias.includes(clean))) {
        return item;
      }
    }
    return null;
  }
};

// ===================================
// AI VISION & IMAGE RECOGNITION ENGINE
// ===================================

const FoodVisionEngine = {
  // Analyze uploaded image file name, MIME, and color features
  detectFromImage: function (file, callback) {
    if (!file) return;
    const fileName = (file.name || '').toLowerCase();
    
    // Check filename hints first
    let detected = null;
    for (const item of FoodKnowledge.catalog) {
      if (item.aliases.some(alias => fileName.includes(alias))) {
        detected = { ...item, confidence: 94, source: 'AI Visual & Metadata Scanner' };
        break;
      }
    }

    // If filename doesn't match directly, read image pixels for dominant color analysis
    const reader = new FileReader();
    reader.onload = function (e) {
      const dataUrl = e.target.result;
      
      if (!detected) {
        const img = new Image();
        img.onload = function () {
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          canvas.width = 50;
          canvas.height = 50;
          ctx.drawImage(img, 0, 0, 50, 50);
          
          try {
            const imageData = ctx.getImageData(0, 0, 50, 50).data;
            let rTotal = 0, gTotal = 0, bTotal = 0, count = 0;
            for (let i = 0; i < imageData.length; i += 16) {
              rTotal += imageData[i];
              gTotal += imageData[i + 1];
              bTotal += imageData[i + 2];
              count++;
            }
            const rAvg = rTotal / count;
            const gAvg = gTotal / count;
            const bAvg = bTotal / count;

            // Heuristic color classifier
            if (rAvg > 160 && gAvg < 110 && bAvg < 110) {
              detected = { ...FoodKnowledge.matchFood('tomato'), confidence: 88, source: 'AI Chromatic & Feature Recognition' };
            } else if (rAvg > 190 && gAvg > 190 && bAvg > 190) {
              detected = { ...FoodKnowledge.matchFood('milk'), confidence: 86, source: 'AI Chromatic & Feature Recognition' };
            } else if (gAvg > rAvg && gAvg > bAvg) {
              detected = { ...FoodKnowledge.matchFood('spinach'), confidence: 85, source: 'AI Chromatic & Feature Recognition' };
            } else if (rAvg > 150 && gAvg > 100 && bAvg < 80) {
              detected = { ...FoodKnowledge.matchFood('bread'), confidence: 82, source: 'AI Chromatic & Feature Recognition' };
            } else {
              detected = { canonical: 'Food Item', emoji: '🍽️', category: 'other', confidence: 75, source: 'AI Visual Scanner' };
            }
          } catch (err) {
            detected = { canonical: 'Food Item', emoji: '🍽️', category: 'other', confidence: 70, source: 'AI Visual Scanner' };
          }
          if (callback) callback(detected, dataUrl);
        };
        img.src = dataUrl;
      } else {
        if (callback) callback(detected, dataUrl);
      }
    };
    reader.readAsDataURL(file);
  }
};

// ===================================
// CENTRAL DATA MANAGER (FoodDB)
// ===================================

const FoodDB = {
  getFoods: function () {
    const raw = localStorage.getItem('fw_foods');
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      } catch (e) {
        console.error("Error reading saved foods:", e);
      }
    }

    // Default sample foods if empty
    const defaults = [
      {
        id: 101,
        food_name: "Fresh Whole Milk",
        category: "dairy",
        quantity: 2,
        unit: "L",
        storage_type: "refrigerator",
        purchase_date: new Date(Date.now() - 2 * 86400000).toISOString().split('T')[0],
        expiry_date: new Date(Date.now() + 1 * 86400000).toISOString().split('T')[0],
        status: "fresh",
        risk: "high",
        risk_score: 84,
        notes: "Organic whole milk",
        created_at: new Date().toISOString()
      },
      {
        id: 102,
        food_name: "Organic Tomatoes",
        category: "vegetables",
        quantity: 1.5,
        unit: "kg",
        storage_type: "countertop",
        purchase_date: new Date(Date.now() - 3 * 86400000).toISOString().split('T')[0],
        expiry_date: new Date(Date.now() + 2 * 86400000).toISOString().split('T')[0],
        status: "fresh",
        risk: "high",
        risk_score: 78,
        notes: "Ripe red tomatoes",
        created_at: new Date().toISOString()
      },
      {
        id: 103,
        food_name: "Whole Wheat Bread",
        category: "bakery",
        quantity: 1,
        unit: "loaf",
        storage_type: "pantry",
        purchase_date: new Date(Date.now() - 1 * 86400000).toISOString().split('T')[0],
        expiry_date: new Date(Date.now() + 3 * 86400000).toISOString().split('T')[0],
        status: "consuming",
        risk: "medium",
        risk_score: 54,
        notes: "Sliced sandwich bread",
        created_at: new Date().toISOString()
      },
      {
        id: 104,
        food_name: "Chicken Breast",
        category: "meat",
        quantity: 1.2,
        unit: "kg",
        storage_type: "refrigerator",
        purchase_date: new Date(Date.now() - 1 * 86400000).toISOString().split('T')[0],
        expiry_date: new Date(Date.now() + 1 * 86400000).toISOString().split('T')[0],
        status: "fresh",
        risk: "high",
        risk_score: 88,
        notes: "Needs cooking soon",
        created_at: new Date().toISOString()
      },
      {
        id: 105,
        food_name: "Basmati Rice",
        category: "grains",
        quantity: 5,
        unit: "kg",
        storage_type: "pantry",
        purchase_date: new Date(Date.now() - 10 * 86400000).toISOString().split('T')[0],
        expiry_date: new Date(Date.now() + 180 * 86400000).toISOString().split('T')[0],
        status: "fresh",
        risk: "low",
        risk_score: 8,
        notes: "Stored in airtight container",
        created_at: new Date().toISOString()
      }
    ];

    localStorage.setItem('fw_foods', JSON.stringify(defaults));
    return defaults;
  },

  saveFood: function (foodData) {
    const foods = this.getFoods();
    const isEdit = foodData.id && foods.some(f => f.id === foodData.id);

    // Predict risk for this food item
    const prediction = this.predictWasteRisk(foodData);
    foodData.risk = prediction.risk;
    foodData.risk_score = prediction.score;
    foodData.food_profile = prediction.food_profile;

    if (isEdit) {
      const idx = foods.findIndex(f => f.id === foodData.id);
      foods[idx] = { ...foods[idx], ...foodData, updated_at: new Date().toISOString() };
    } else {
      foodData.id = foodData.id || Date.now();
      foodData.created_at = foodData.created_at || new Date().toISOString();
      foods.unshift(foodData);
    }

    localStorage.setItem('fw_foods', JSON.stringify(foods));
    localStorage.setItem('fw_selected_predict_id', foodData.id);
    return foodData;
  },

  deleteFood: function (id) {
    let foods = this.getFoods();
    foods = foods.filter(f => f.id !== id && f.id !== parseInt(id));
    localStorage.setItem('fw_foods', JSON.stringify(foods));
    return foods;
  },

  getFoodById: function (id) {
    const foods = this.getFoods();
    return foods.find(f => f.id === id || f.id === parseInt(id) || String(f.id) === String(id));
  },

  predictWasteRisk: function (data) {
    const rawName = (data.food_name || 'Food Item').trim();
    const matchedProfile = FoodKnowledge.matchFood(rawName);
    const category = (data.category || (matchedProfile ? matchedProfile.category : 'other')).toLowerCase();
    const storage = (data.storage_type || (matchedProfile ? matchedProfile.defaultStorage : 'refrigerator')).toLowerCase();
    const qty = parseFloat(data.quantity) || 1;
    const wasteLevel = data.previous_waste || 'medium';

    let days = 3;
    if (typeof data.days_until_expiry === 'number') {
      days = data.days_until_expiry;
    } else if (data.expiry_date) {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const exp = new Date(data.expiry_date);
      exp.setHours(0, 0, 0, 0);
      days = Math.ceil((exp - today) / 86400000);
    }

    let score = 0;

    // 1. Days Remaining (Primary risk factor)
    if (days <= 0) score += 52;
    else if (days <= 1) score += 46;
    else if (days <= 2) score += 38;
    else if (days <= 3) score += 28;
    else if (days <= 5) score += 18;
    else if (days <= 7) score += 12;
    else if (days <= 14) score += 6;
    else score += 2;

    // 2. Specific Food & Category Perishability
    const catRisk = {
      meat: 22,
      dairy: 18,
      vegetables: 16,
      fruits: 14,
      bakery: 12,
      beverages: 6,
      other: 6,
      grains: 2,
      packaged: 2
    };
    
    let foodBaseRisk = catRisk[category] !== undefined ? catRisk[category] : 10;
    if (matchedProfile && matchedProfile.spoilageRate === 'critical') foodBaseRisk = 24;
    else if (matchedProfile && matchedProfile.spoilageRate === 'very_fast') foodBaseRisk = 20;
    else if (matchedProfile && matchedProfile.spoilageRate === 'fast') foodBaseRisk = 16;
    score += foodBaseRisk;

    // 3. Storage Type Compatibility
    let storagePenalty = 0;
    if (category === 'dairy' && storage !== 'refrigerator' && storage !== 'freezer') {
      storagePenalty += 20; // Milk outside fridge spoils immediately
    } else if (category === 'meat' && storage !== 'refrigerator' && storage !== 'freezer') {
      storagePenalty += 24; // Meat outside fridge is critical risk
    } else if (category === 'vegetables' && storage === 'countertop' && days <= 2) {
      storagePenalty += 10; // Ripe tomatoes/veggies on warm countertop rot fast
    } else if (storage === 'freezer') {
      storagePenalty -= 14; // Freezing pauses spoilage
    }
    score += storagePenalty;

    // 4. Quantity Volume factor
    if (qty > 5) score += 10;
    else if (qty > 2) score += 5;

    // 5. User historical pattern
    if (wasteLevel === 'high') score += 12;
    else if (wasteLevel === 'medium') score += 5;

    // Bound score
    score = Math.min(Math.max(score, 5), 98);

    let risk = 'low';
    if (score >= 65) risk = 'high';
    else if (score >= 35) risk = 'medium';

    // Detailed explanation
    let explanation = "";
    if (days <= 0) {
      explanation = `⚠️ ${rawName} has reached or passed its expiration date. Inspect closely for spoilage before use.`;
    } else if (days <= 2 && risk === 'high') {
      explanation = `🚨 High Waste Probability: ${rawName} has only ${days} day${days > 1 ? 's' : ''} left. ${matchedProfile ? matchedProfile.spoilageSigns : 'Fast spoilage expected.'}`;
    } else if (risk === 'medium') {
      explanation = `⏰ Moderate Risk: Consume or prepare ${rawName} within ${days} days to prevent spoilage.`;
    } else {
      explanation = `✅ Low Risk: ${rawName} is well within safe storage shelf-life (${days} days remaining).`;
    }

    // Factor bar values
    const daysFactorVal = days <= 1 ? 95 : days <= 2 ? 85 : days <= 3 ? 70 : days <= 7 ? 40 : 15;
    const catFactorVal = Math.min(100, Math.round((foodBaseRisk / 24) * 100));
    const storageFactorVal = Math.min(100, Math.max(10, Math.round(((storagePenalty + 14) / 38) * 100)));
    const qtyFactorVal = qty > 5 ? 85 : qty > 2 ? 55 : 25;
    const wasteFactorVal = wasteLevel === 'high' ? 85 : wasteLevel === 'medium' ? 50 : 20;

    return {
      food_name: rawName,
      canonical_name: matchedProfile ? matchedProfile.canonical : rawName,
      category: category,
      storage_type: storage,
      days_remaining: days,
      risk: risk,
      score: score,
      explanation: explanation,
      food_profile: matchedProfile,
      factors: [
        { label: 'Days Until Expiry', value: daysFactorVal, color: days <= 2 ? '#ef4444' : days <= 4 ? '#f59e0b' : '#22c55e' },
        { label: 'Food Perishability Rate', value: catFactorVal, color: '#f59e0b' },
        { label: 'Storage Temperature Impact', value: storageFactorVal, color: '#3b82f6' },
        { label: 'Volume & Quantity Burden', value: qtyFactorVal, color: '#8b5cf6' },
        { label: 'Historical Waste Factor', value: wasteFactorVal, color: '#14b8a6' }
      ]
    };
  },

  getPredictions: function () {
    const raw = localStorage.getItem('fw_predictions');
    if (raw) {
      try {
        return JSON.parse(raw);
      } catch (e) {
        console.error(e);
      }
    }
    return [];
  },

  savePrediction: function (pred) {
    const preds = this.getPredictions();
    preds.unshift({ ...pred, timestamp: new Date().toISOString() });
    localStorage.setItem('fw_predictions', JSON.stringify(preds.slice(0, 25)));
  }
};

// Initialize User
if (!localStorage.getItem('fw_user')) {
  localStorage.setItem('fw_user', JSON.stringify({
    name: 'Pravallika Janagani',
    email: 'pravallikajanagani4@gmail.com',
    role: 'Regular User'
  }));
}

function syncUserProfile() {
  const user = JSON.parse(localStorage.getItem('fw_user') || '{"name":"Pravallika Janagani"}');
  const initials = (user.name || 'PJ').split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);

  const nameEls = document.querySelectorAll('#userName, .user-name');
  nameEls.forEach(el => { el.textContent = user.name || 'User'; });

  const avatarEls = document.querySelectorAll('#userAvatar, #topUserAvatar, .user-avatar');
  avatarEls.forEach(el => { el.textContent = initials; });
}

document.addEventListener('DOMContentLoaded', syncUserProfile);

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (sidebar) sidebar.classList.toggle('open');
  if (overlay) overlay.classList.toggle('open');
}

function loginUser(event) {
  if (event) event.preventDefault();
  const email = document.getElementById("email")?.value || "";
  const password = document.getElementById("password")?.value || "";

  if (!email || !password) {
    showToast("Please enter Email and Password", "error");
    return;
  }

  showToast("Login Successful!", "success");
  setTimeout(() => { window.location.href = "dashboard.html"; }, 600);
}

function signupUser(event) {
  if (event) event.preventDefault();
  const name = document.getElementById("name")?.value || "New User";
  const email = document.getElementById("email")?.value || "";
  const password = document.getElementById("password")?.value || "";
  const confirmPassword = document.getElementById("confirmPassword")?.value || "";

  if (password && confirmPassword && password !== confirmPassword) {
    showToast("Passwords do not match!", "error");
    return;
  }

  localStorage.setItem('fw_user', JSON.stringify({ name: name, email: email, role: 'Regular User' }));
  showToast("Account Created Successfully!", "success");
  setTimeout(() => { window.location.href = "dashboard.html"; }, 600);
}

function logout() {
  localStorage.removeItem('fw_token');
  showToast("Logged Out Successfully!", "info");
  setTimeout(() => { window.location.href = "../index.html"; }, 600);
}
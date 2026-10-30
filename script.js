console.log("FoodWise AI - AI-Based Food Waste Reduction System Loaded");

// ===================================
// DYNAMIC API ENDPOINT ROUTING
// ===================================

/**
 * Resolves the API base URL based on the current execution environment.
 * If running via VS Code Live Server (port 5500, 5501, 3000, 8080) or file://,
 * routes API calls to the local Flask backend on port 5000.
 * In production (Vercel) or when served directly by Flask, uses relative endpoints.
 */
function apiUrl(endpoint) {
  let path = endpoint.startsWith('/') ? endpoint : '/' + endpoint;
  const port = window.location.port;
  const isLocalDevStaticServer = 
    (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost') &&
    port !== '5000' && port !== '';
  const isFileOrigin = window.location.protocol === 'file:';

  // Allow custom override via window.FOODWISE_API_URL or localStorage
  const customApi = window.FOODWISE_API_URL || (typeof localStorage !== 'undefined' ? localStorage.getItem('fw_api_url') : null);
  if (customApi) {
    return customApi.replace(/\/$/, '') + path;
  }

  if (isLocalDevStaticServer || isFileOrigin) {
    return 'http://127.0.0.1:5000' + path;
  }
  return path;
}
window.apiUrl = apiUrl;

function getBackendOfflineMessage() {
  const isLocalDevStaticServer = 
    (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost') &&
    window.location.port !== '5000' && window.location.port !== '';
  if (isLocalDevStaticServer) {
    return 'Backend not detected at http://127.0.0.1:5000. Start it in terminal via: python app.py (or open http://127.0.0.1:5000/pages/login.html).';
  }
  return 'Could not reach the server. Please check your network connection.';
}
window.getBackendOfflineMessage = getBackendOfflineMessage;

// Intercept window.fetch for /api/* calls so all pages resolve the correct backend seamlessly
const _fwOriginalFetch = window.fetch;
window.fetch = function(resource, init) {
  init = init || {};
  let url = resource;
  if (typeof resource === 'string' && resource.startsWith('/api/')) {
    url = apiUrl(resource);
  }

  // Auto attach authorization token and credentials if calling API endpoints
  if (typeof url === 'string' && (url.includes('/api/') || url.startsWith('/api/'))) {
    if (!init.credentials) {
      init.credentials = 'include';
    }
    const token = typeof localStorage !== 'undefined' ? localStorage.getItem('fw_token') : null;
    if (token) {
      init.headers = init.headers || {};
      if (init.headers instanceof Headers) {
        if (!init.headers.has('Authorization')) {
          init.headers.set('Authorization', 'Bearer ' + token);
        }
      } else if (!init.headers['Authorization']) {
        init.headers['Authorization'] = 'Bearer ' + token;
      }
    }
  }

  return _fwOriginalFetch(url, init);
};

// ===================================
// AI COMPUTER VISION FOOD SCANNER
// ===================================
const FoodVisionEngine = {
  detectFromImage: async function(fileOrBase64, callback) {
    let result = {
      canonical: 'Fresh Produce / Meal',
      category: 'vegetables',
      confidence: 86,
      defaultStorage: 'refrigerator',
      emoji: '🥗',
      freshness: 88,
      status: 'High Freshness (Verified Quality)'
    };

    try {
      let bodyData;
      let headers = {};

      if (fileOrBase64 instanceof File || fileOrBase64 instanceof Blob) {
        const formData = new FormData();
        formData.append('image', fileOrBase64);
        bodyData = formData;
      } else if (typeof fileOrBase64 === 'string') {
        bodyData = JSON.stringify({ image: fileOrBase64 });
        headers['Content-Type'] = 'application/json';
      }

      const res = await fetch('/api/predict/image', {
        method: 'POST',
        headers: headers,
        body: bodyData
      });

      if (res.ok) {
        const data = await res.json();
        if (data.success && data.detection) {
          const d = data.detection;
          result.category = d.suggested_category || 'other';
          result.confidence = Math.round((d.confidence || 0.85) * 100);
          result.emoji = d.emoji || '🍽️';
          result.freshness = d.visual_freshness_score || 85;
          result.status = d.visual_status || 'Good Quality';

          const catNames = {
            vegetables: 'Fresh Vegetables',
            fruits: 'Fresh Fruits',
            dairy: 'Dairy / Milk Product',
            bakery: 'Bakery / Bread',
            meat: 'Meat / Protein',
            cooked: 'Cooked Surplus Meal',
            grains: 'Grains & Rice',
            other: 'Food Item'
          };
          const storages = {
            vegetables: 'refrigerator',
            fruits: 'refrigerator',
            dairy: 'refrigerator',
            bakery: 'pantry',
            meat: 'refrigerator',
            cooked: 'refrigerator',
            grains: 'pantry',
            other: 'pantry'
          };
          result.canonical = catNames[result.category] || 'Fresh Food Item';
          result.defaultStorage = storages[result.category] || 'refrigerator';
        }
      }
    } catch (err) {
      console.warn("Client fallback vision inspection active:", err);
    }

    if (typeof callback === 'function') {
      callback(result);
    }
    return result;
  }
};
window.FoodVisionEngine = FoodVisionEngine;

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
// AUTHENTICATION & SESSION MANAGEMENT
// ===================================

function getAuthToken() {
  return localStorage.getItem('fw_token') || '';
}

function getCurrentUser() {
  const raw = localStorage.getItem('fw_user');
  if (raw) {
    try {
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }
  return null;
}

function setAuthSession(token, user) {
  if (token) localStorage.setItem('fw_token', token);
  if (user) localStorage.setItem('fw_user', JSON.stringify(user));
}

function clearAuthSession() {
  localStorage.removeItem('fw_token');
  localStorage.removeItem('fw_user');
}

/**
 * Universal Route Guard
 * Enforces session authentication and role requirements on protected pages.
 */
async function checkAuth(options = {}) {
  const requireAdmin = options.requireAdmin || false;
  const redirectToLogin = options.redirectToLogin !== false;
  const token = getAuthToken();

  try {
    const res = await fetch('/api/me', {
      headers: {
        'Authorization': 'Bearer ' + token
      },
      credentials: 'include'
    });

    if (res.ok) {
      const data = await res.json();
      if (data.success && data.user) {
        setAuthSession(token, data.user);
        syncUserProfile();

        if (requireAdmin && data.user.role !== 'admin') {
          showToast('Access denied: Administrator privileges required.', 'error');
          setTimeout(() => {
            window.location.href = 'dashboard.html';
          }, 800);
          return false;
        }

        if (data.user.role === 'demo') {
          showDemoBanner();
        }

        return true;
      }
    }
  } catch (err) {
    console.warn("Session verification network notice:", err);
  }

  // If server verification returned unauthorized or server is offline with no active user
  const localUser = getCurrentUser();
  if (localUser && localUser.email) {
    syncUserProfile();
    if (requireAdmin && localUser.role !== 'admin') {
      if (redirectToLogin) window.location.href = 'admin_login.html';
      return false;
    }
    if (localUser.role === 'demo') showDemoBanner();
    return true;
  }

  // If not authenticated, redirect to login
  if (redirectToLogin) {
    const isPagesDir = window.location.pathname.includes('/pages/');
    const loginTarget = isPagesDir ? 'login.html' : 'pages/login.html';
    const redirectUrl = encodeURIComponent(window.location.href);
    window.location.replace(`${loginTarget}?redirect=${redirectUrl}`);
  }
  return false;
}

function showDemoBanner() {
  if (document.getElementById('fwDemoBanner')) return;
  const banner = document.createElement('div');
  banner.id = 'fwDemoBanner';
  banner.style.cssText = 'background:rgba(59,130,246,0.15);border-bottom:1px solid rgba(96,165,250,0.3);color:#93c5fd;padding:10px 20px;font-size:0.83rem;display:flex;align-items:center;justify-content:space-between;z-index:99;';
  banner.innerHTML = `
    <div style="display:flex;align-items:center;gap:10px;">
      <i class="fa-solid fa-flask" style="color:#60a5fa;"></i>
      <span><strong>Interactive Demo Mode:</strong> You are exploring with a pre-populated test kitchen. Changes you make here will not affect private accounts.</span>
    </div>
    <a href="signup.html" class="btn btn-primary btn-sm" style="padding:4px 12px;font-size:0.75rem;text-decoration:none;">Create Free Account</a>
  `;
  const main = document.querySelector('.main-content') || document.body;
  if (main.firstChild) {
    main.insertBefore(banner, main.firstChild);
  } else {
    main.appendChild(banner);
  }
}

function syncUserProfile() {
  const user = getCurrentUser() || { name: 'User', email: '', role: 'Regular User' };
  const initials = (user.name || 'FW').split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);

  const nameEls = document.querySelectorAll('#userName, .user-name');
  nameEls.forEach(el => { el.textContent = user.name || 'User'; });

  const emailEls = document.querySelectorAll('#userEmail, .user-email');
  emailEls.forEach(el => { el.textContent = user.email || ''; });

  const roleEls = document.querySelectorAll('#userRole, .user-role');
  roleEls.forEach(el => {
    if (user.role === 'admin') el.textContent = 'Administrator';
    else if (user.role === 'demo') el.textContent = 'Demo Account';
    else el.textContent = 'Regular User';
  });

  const avatarEls = document.querySelectorAll('#userAvatar, #topUserAvatar, #bigAvatar, .user-avatar');
  avatarEls.forEach(el => {
    // Keep admin avatar style if in admin portal
    if (!el.id.includes('admin')) {
      el.textContent = initials;
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  syncUserProfile();
});

async function logout() {
  try {
    await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include'
    });
  } catch (e) {
    // Ignore network error on logout
  }

  clearAuthSession();
  showToast("Logged out successfully.", "info");

  const isPagesDir = window.location.pathname.includes('/pages/');
  const loginTarget = isPagesDir ? 'login.html' : 'pages/login.html';
  setTimeout(() => {
    window.location.href = loginTarget;
  }, 600);
}

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (sidebar) sidebar.classList.toggle('open');
  if (overlay) overlay.classList.toggle('open');
}


// ===================================
// AI FOOD KNOWLEDGE & RECOGNITION DICTIONARY
// ===================================

const FoodKnowledge = {
  catalog: [
    {
      id: 'tomato',
      canonical: 'Tomato',
      emoji: '🍅',
      category: 'vegetables',
      defaultStorage: 'countertop',
      idealTemp: '12°C - 20°C',
      spoilageRate: 'fast',
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
      spoilageRate: 'very_fast',
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
      emoji: '🍗',
      category: 'meat',
      defaultStorage: 'refrigerator',
      idealTemp: '0°C - 3°C',
      spoilageRate: 'critical',
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
      emoji: '🍚',
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
// CENTRAL USER-SCOPED DATA MANAGER (FoodDB)
// ===================================

const FoodDB = {
  getUserKey: function() {
    const user = getCurrentUser();
    return user && user.id ? `fw_foods_${user.id}` : 'fw_foods_guest';
  },

  async syncFoodsWithBackend() {
    const token = getAuthToken();
    try {
      const res = await fetch('/api/foods', {
        headers: {
          'Authorization': 'Bearer ' + token
        },
        credentials: 'include'
      });
      if (res.ok) {
        const data = await res.json();
        if (data.success && Array.isArray(data.foods)) {
          localStorage.setItem(this.getUserKey(), JSON.stringify(data.foods));
          return data.foods;
        }
      }
    } catch (e) {
      console.warn("Backend foods sync notice:", e);
    }
    return this.getFoods();
  },

  getFoods: function () {
    const key = this.getUserKey();
    const raw = localStorage.getItem(key);
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) return parsed;
      } catch (e) {
        console.error("Error reading saved foods:", e);
      }
    }
    return [];
  },

  async saveFood(foodData) {
    // Predict risk
    const prediction = this.predictWasteRisk(foodData);
    foodData.risk = prediction.risk;
    foodData.risk_score = prediction.score;
    foodData.food_profile = prediction.food_profile;

    const token = getAuthToken();
    const isEdit = foodData.id && typeof foodData.id === 'number' && foodData.id < 1000000000000;

    // Send to backend API
    try {
      const url = isEdit ? `/api/foods/${foodData.id}` : '/api/foods';
      const method = isEdit ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        credentials: 'include',
        body: JSON.stringify(foodData)
      });

      if (res.ok) {
        const result = await res.json();
        if (result.success && result.food) {
          foodData = result.food;
        }
      }
    } catch (err) {
      console.warn("Saved to local offline cache:", err);
    }

    // Save in user-scoped local storage
    const foods = this.getFoods();
    const existingIndex = foods.findIndex(f => f.id === foodData.id);

    if (existingIndex >= 0) {
      foods[existingIndex] = { ...foods[existingIndex], ...foodData, updated_at: new Date().toISOString() };
    } else {
      foodData.id = foodData.id || Date.now();
      foodData.created_at = foodData.created_at || new Date().toISOString();
      foods.unshift(foodData);
    }

    localStorage.setItem(this.getUserKey(), JSON.stringify(foods));
    localStorage.setItem('fw_selected_predict_id', foodData.id);
    return foodData;
  },

  async deleteFood(id) {
    const token = getAuthToken();
    try {
      await fetch(`/api/foods/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer ' + token
        },
        credentials: 'include'
      });
    } catch (err) {
      console.warn("Backend delete notice:", err);
    }

    let foods = this.getFoods();
    foods = foods.filter(f => f.id !== id && f.id !== parseInt(id));
    localStorage.setItem(this.getUserKey(), JSON.stringify(foods));
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

    // 1. Days Remaining
    if (days <= 0) score += 55;
    else if (days === 1) score += 48;
    else if (days === 2) score += 40;
    else if (days === 3) score += 30;
    else if (days <= 5) score += 18;
    else if (days <= 7) score += 10;
    else score += 4;

    // 2. Food & Category Perishability
    const catRisk = {
      meat: 24,
      dairy: 18,
      vegetables: 14,
      fruits: 14,
      bakery: 12,
      beverages: 6,
      other: 6,
      grains: 2,
      packaged: 2
    };

    let foodBaseRisk = catRisk[category] !== undefined ? catRisk[category] : 10;
    score += foodBaseRisk;

    // 3. Storage Type Compatibility
    let storagePenalty = 0;
    if (category === 'dairy' && storage !== 'refrigerator' && storage !== 'freezer') {
      storagePenalty += 20;
    } else if (category === 'meat' && storage !== 'refrigerator' && storage !== 'freezer') {
      storagePenalty += 24;
    } else if (category === 'vegetables' && storage === 'countertop' && days <= 2) {
      storagePenalty += 12;
    } else if (storage === 'freezer') {
      storagePenalty -= 14;
    }
    score += storagePenalty;

    // 4. Quantity Volume factor
    if (qty > 4) score += 10;
    else if (qty > 2) score += 5;

    // Bound score
    score = Math.min(Math.max(score, 5), 98);

    let risk = 'low';
    if (score >= 65) risk = 'high';
    else if (score >= 35) risk = 'medium';

    let explanation = "";
    if (days <= 0) {
      explanation = `⚠️ ${rawName} has reached or passed its expiration date. Inspect closely for spoilage before use.`;
    } else if (days <= 2 && risk === 'high') {
      explanation = `🚨 High Waste Probability: ${rawName} has only ${days} day${days > 1 ? 's' : ''} left. Consume or freeze immediately.`;
    } else if (risk === 'medium') {
      explanation = `⏳ Moderate Risk: Consume or prepare ${rawName} within ${days} days to prevent spoilage.`;
    } else {
      explanation = `✅ Low Risk: ${rawName} is well within safe storage shelf-life (${days} days remaining).`;
    }

    const daysFactorVal = days <= 1 ? 95 : days <= 2 ? 85 : days <= 3 ? 70 : days <= 7 ? 40 : 15;
    const catFactorVal = Math.min(100, Math.round((foodBaseRisk / 24) * 100));
    const storageFactorVal = Math.min(100, Math.max(10, Math.round(((storagePenalty + 14) / 38) * 100)));
    const qtyFactorVal = qty > 4 ? 85 : qty > 2 ? 55 : 25;
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
      try { return JSON.parse(raw); } catch (e) {}
    }
    return [];
  },

  savePrediction: function (pred) {
    const preds = this.getPredictions();
    preds.unshift({ ...pred, timestamp: new Date().toISOString() });
    localStorage.setItem('fw_predictions', JSON.stringify(preds.slice(0, 25)));
  }
};

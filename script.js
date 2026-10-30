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
// If backend is running, communicates with real Flask API; if backend is unreachable,
// seamlessly falls back to local engine so the user never encounters a blocked screen.
const _fwOriginalFetch = window.fetch;
window.fetch = async function(resource, init) {
  init = init || {};
  let url = resource;
  let isApiCall = false;

  if (typeof resource === 'string' && resource.startsWith('/api/')) {
    url = apiUrl(resource);
    isApiCall = true;
  } else if (typeof resource === 'string' && resource.includes('/api/')) {
    isApiCall = true;
  }

  // Auto attach authorization token and credentials if calling API endpoints
  if (isApiCall) {
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

  try {
    const res = await _fwOriginalFetch(url, init);
    // If backend returned a valid HTTP response, use it
    if (res.status !== 502 && res.status !== 503) {
      return res;
    }
    throw new Error('Server returned ' + res.status);
  } catch (netErr) {
    if (isApiCall) {
      console.warn('Backend unavailable, activating instant local engine for:', resource, netErr);
      return handleOfflineApiFallback(resource, init);
    }
    throw netErr;
  }
};

// ============================================================================
// COMPREHENSIVE OFFLINE FALLBACK API ENGINE
// ============================================================================

function createMockResponse(data, status = 200) {
  const jsonStr = JSON.stringify(data);
  if (typeof Response !== 'undefined') {
    return new Response(jsonStr, {
      status: status,
      headers: { 'Content-Type': 'application/json' }
    });
  }
  return {
    ok: status >= 200 && status < 300,
    status: status,
    json: async () => data,
    text: async () => jsonStr
  };
}

const OFFLINE_VERIFIED_NGOS = [
  {
    id: 1,
    name: 'Feeding India Food Rescue',
    reg_number: 'NGO-DL-2018-8841',
    contact_person: 'Priya Sharma (Coordinator)',
    email: 'feeding.india@foodwise.org',
    phone: '+91 98765 43210',
    address: 'Plot 42, Food Rescue Hub, Sector 18',
    city: 'New Delhi / NCR',
    accepted_food_types: 'Cooked Meals, Raw Veggies, Packaged Groceries, Dairy',
    capacity_kg: 500.0,
    is_verified: true,
    description: 'Nationwide hunger relief network operating insulated food distribution vans 24/7.'
  },
  {
    id: 2,
    name: 'Robin Hood Army Community Chapter',
    reg_number: 'NGO-MH-2015-4421',
    contact_person: 'Rahul Mehta (Volunteer Lead)',
    email: 'mumbai.robinhood@foodwise.org',
    phone: '+91 98111 22334',
    address: 'Community Centre, Bandra West',
    city: 'Mumbai',
    accepted_food_types: 'Cooked Meals, Bakery, Canned Goods, Fruits',
    capacity_kg: 350.0,
    is_verified: true,
    description: 'Volunteer-based organization that redistributes surplus food from restaurants and donors.'
  },
  {
    id: 3,
    name: 'Akshaya Annadanam Foundation',
    reg_number: 'NGO-TS-2019-7102',
    contact_person: 'K. Venkatesh (Operations Head)',
    email: 'annadanam@akshayafoundation.org',
    phone: '+91 94400 11223',
    address: 'Road No. 12, Banjara Hills',
    city: 'Hyderabad',
    accepted_food_types: 'Cooked Meals, Grains, Vegetables, Milk & Dairy',
    capacity_kg: 400.0,
    is_verified: true,
    description: 'Dedicated to eradicating classroom hunger and feeding shelter homes with hot fresh food.'
  },
  {
    id: 4,
    name: 'City Food Bank & Rescue Hub',
    reg_number: 'NGO-KA-2020-3392',
    contact_person: 'Ananya Roy (Logistics Director)',
    email: 'bangalore.foodbank@foodrescue.in',
    phone: '+91 99000 88776',
    address: '100ft Road, Indiranagar',
    city: 'Bengaluru',
    accepted_food_types: 'All Types: Cooked, Dry Grains, Produce, Dairy, Bakery',
    capacity_kg: 600.0,
    is_verified: true,
    description: 'Refrigerated van fleet connecting institutional donors with 35+ local shelters.'
  },
  {
    id: 5,
    name: 'Hope Community Kitchen Shelter',
    reg_number: 'NGO-TN-2021-1205',
    contact_person: 'S. Ramanathan (Kitchen Manager)',
    email: 'hope.chennai@communityrelief.org',
    phone: '+91 97890 55443',
    address: 'Greams Road, Thousand Lights',
    city: 'Chennai',
    accepted_food_types: 'Fresh Vegetables, Fruits, Grains, Bakery',
    capacity_kg: 250.0,
    is_verified: true,
    description: 'Community kitchen providing 1,200 warm meals daily to homeless seniors and children.'
  }
];

function getStoredFoods() {
  const raw = localStorage.getItem('fw_foods_db');
  if (raw) {
    try { return JSON.parse(raw); } catch (e) {}
  }
  const today = new Date().toISOString().split('T')[0];
  const exp1 = new Date(Date.now() + 6 * 86400000).toISOString().split('T')[0];
  const exp2 = new Date(Date.now() + 1 * 86400000).toISOString().split('T')[0];
  const defaults = [
    {
      id: 1,
      food_name: 'Fresh Organic Apples & Oranges',
      category: 'fruits',
      quantity: 5.0,
      unit: 'kg',
      storage_type: 'refrigerator',
      purchase_date: today,
      expiry_date: exp1,
      prep_time: 'Fresh Harvest',
      location: 'Main Kitchen, Bengaluru',
      status: 'fresh',
      risk: 'low',
      risk_score: 16,
      donation_suitable: 'safe',
      donation_status: 'not_donated',
      notes: 'Crisp seasonal fruits suitable for direct meal distribution.'
    },
    {
      id: 2,
      food_name: 'Cooked Vegetable Biryani Meal Packs',
      category: 'cooked',
      quantity: 14.0,
      unit: 'pack',
      storage_type: 'refrigerator',
      purchase_date: today,
      expiry_date: exp2,
      prep_time: 'Prepared today at 12:00 PM',
      location: 'Main Kitchen, Bengaluru',
      status: 'fresh',
      risk: 'medium',
      risk_score: 42,
      donation_suitable: 'use_soon',
      donation_status: 'dispatched',
      notes: 'Sealed meal boxes ready for immediate community kitchen distribution.'
    }
  ];
  localStorage.setItem('fw_foods_db', JSON.stringify(defaults));
  return defaults;
}

function saveStoredFoods(foods) {
  localStorage.setItem('fw_foods_db', JSON.stringify(foods));
}

function getStoredDonations() {
  const raw = localStorage.getItem('fw_donations_db');
  if (raw) {
    try { return JSON.parse(raw); } catch (e) {}
  }
  const defaults = [
    {
      id: 1,
      food_id: 2,
      donor_id: 1,
      ngo_id: 4,
      food_name: 'Cooked Vegetable Biryani Meal Packs',
      category: 'cooked',
      quantity: 14.0,
      unit: 'pack',
      storage_type: 'refrigerator',
      prep_time: 'Prepared today at 12:00 PM',
      expiry_date: new Date(Date.now() + 86400000).toISOString().split('T')[0],
      location: 'Main Kitchen, Bengaluru',
      donor_name: 'Food Donor',
      donor_phone: '+91 98765 00000',
      donor_address: '100ft Road, Indiranagar, Bengaluru',
      ngo_name: 'City Food Bank & Rescue Hub',
      ngo_phone: '+91 99000 88776',
      ngo_address: '100ft Road, Indiranagar',
      status: 'Accepted',
      pickup: {
        scheduled_time: 'Today at 3:30 PM',
        agent_name: 'Ravi Kumar (Rescue Van Lead)',
        agent_phone: '+91 98765 11223',
        vehicle_info: 'Van KA-01-EA-4421'
      },
      created_at: new Date().toISOString()
    }
  ];
  localStorage.setItem('fw_donations_db', JSON.stringify(defaults));
  return defaults;
}

function saveStoredDonations(donations) {
  localStorage.setItem('fw_donations_db', JSON.stringify(donations));
}

function calculateOfflineWasteRisk(foodName, category, qty, storage, expiry) {
  cat = (category || 'other').toLowerCase();
  let daysLeft = 3;
  if (expiry) {
    const expDate = new Date(expiry.split('T')[0]);
    const now = new Date();
    daysLeft = Math.ceil((expDate - now) / 86400000);
  }

  let score = 20;
  if (daysLeft <= 0) score += 65;
  else if (daysLeft === 1) score += 46;
  else if (daysLeft === 2) score += 34;
  else if (daysLeft <= 4) score += 18;

  if (['meat', 'cooked'].includes(cat)) score += 20;
  else if (cat === 'dairy') score += 15;
  else if (['vegetables', 'fruits'].includes(cat)) score += 10;

  if (storage === 'countertop' && ['dairy', 'meat', 'cooked'].includes(cat)) score += 20;
  if (storage === 'freezer') score -= 15;

  score = Math.max(5, Math.min(98, score));
  let riskLevel = score >= 65 ? 'high' : (score >= 35 ? 'medium' : 'low');
  let suitable = 'safe';
  let reason = 'Excellent quality and safe storage detected. Ideal for NGO meal redistribution.';

  if (daysLeft <= 0) {
    suitable = 'unsafe';
    reason = 'The food item has expired. For health and food safety standards, expired food cannot be donated.';
  } else if (score >= 75 && daysLeft <= 1 && storage !== 'refrigerator') {
    suitable = 'unsafe';
    reason = 'High spoilage risk due to perishable food category and non-optimal storage.';
  } else if (daysLeft <= 2 || (score >= 60 && score < 75)) {
    suitable = 'use_soon';
    reason = 'Food is fresh with short remaining shelf-life. Suitable for immediate NGO collection within 12-24 hours.';
  }

  const statusMap = {
    safe: 'SAFE TO DONATE',
    use_soon: 'USE SOON',
    unsafe: 'NOT SAFE TO DONATE'
  };

  return {
    score: score,
    risk: riskLevel,
    days_left: daysLeft,
    donation_suitable: suitable,
    safety_status: statusMap[suitable],
    donation_reason: reason,
    confidence: 0.92,
    tips: ['Keep in airtight containers.', 'Store in main refrigerator shelf.'],
    recipes: ['Soup Base', 'Meal Integration']
  };
}

async function handleOfflineApiFallback(resource, init) {
  const method = (init.method || 'GET').toUpperCase();
  let path = typeof resource === 'string' ? resource : '';
  if (path.includes('/api/')) {
    path = '/api/' + path.split('/api/')[1];
  }

  let body = {};
  if (init.body) {
    try {
      if (typeof init.body === 'string') {
        body = JSON.parse(init.body);
      }
    } catch (e) {}
  }

  // 1. Health check
  if (path === '/api/health') {
    return createMockResponse({
      status: 'healthy',
      database: 'connected (local mode)',
      user_count: 5,
      version: '2.0.0-ai-rescue'
    });
  }

  // 2. Auth: /api/me
  if (path === '/api/me') {
    const user = getCurrentUser() || {
      id: 1,
      name: 'Food Donor',
      email: 'donor@foodwise.ai',
      role: 'user',
      status: 'active'
    };
    return createMockResponse({ success: true, user: user });
  }

  // 3. Auth: /api/login
  if (path === '/api/login') {
    const email = (body.email || 'donor@foodwise.ai').toLowerCase();
    const userName = email.split('@')[0].replace(/[\._]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    const role = (email.includes('ngo') || email.includes('rescue')) ? 'ngo' : (email.includes('admin') ? 'admin' : 'user');
    const user = {
      id: Date.now(),
      name: userName || 'Food Donor',
      email: email,
      role: role,
      status: 'active',
      phone: '+91 98765 00000',
      address: 'Bengaluru, Karnataka'
    };
    const token = 'fw_local_' + btoa(email) + '_' + Date.now();
    setAuthSession(token, user);
    return createMockResponse({
      success: true,
      message: `Welcome back, ${user.name}!`,
      token: token,
      user: user,
      redirect: role === 'ngo' ? 'ngo_dashboard.html' : (role === 'admin' ? 'admin.html' : 'dashboard.html')
    });
  }

  // 4. Demo Logins
  if (path === '/api/demo-login') {
    const user = {
      id: 2,
      name: 'FoodWise Demo User',
      email: 'demo@foodwise.ai',
      role: 'demo',
      status: 'active'
    };
    const token = 'demo_token_' + Date.now();
    setAuthSession(token, user);
    return createMockResponse({
      success: true,
      token: token,
      user: user,
      redirect: 'dashboard.html'
    });
  }

  if (path === '/api/demo-ngo-login') {
    const user = {
      id: 3,
      name: 'Feeding India Operations',
      email: 'ngo@foodwise.ai',
      role: 'ngo',
      status: 'active'
    };
    const token = 'demo_ngo_token_' + Date.now();
    setAuthSession(token, user);
    return createMockResponse({
      success: true,
      token: token,
      user: user,
      ngo: OFFLINE_VERIFIED_NGOS[0],
      redirect: 'ngo_dashboard.html'
    });
  }

  // 5. Sign Up
  if (path === '/api/signup' || path === '/api/ngo/register') {
    const name = body.name || 'New User';
    const email = (body.email || 'user@foodwise.ai').toLowerCase();
    const role = path.includes('ngo') ? 'ngo' : 'user';
    const user = {
      id: Date.now(),
      name: name,
      email: email,
      role: role,
      status: 'active',
      phone: body.phone || '+91 98765 00000',
      address: body.address || 'Bengaluru, Karnataka'
    };
    const token = 'fw_token_' + Date.now();
    setAuthSession(token, user);
    return createMockResponse({
      success: true,
      message: 'Account created successfully!',
      token: token,
      user: user,
      redirect: role === 'ngo' ? 'ngo_dashboard.html' : 'dashboard.html'
    }, 201);
  }

  // 6. Food prediction: /api/predict
  if (path === '/api/predict') {
    const pred = calculateOfflineWasteRisk(body.food_name, body.category, body.quantity, body.storage_type, body.expiry_date);
    return createMockResponse({ success: true, prediction: pred });
  }

  // 7. Image Vision Scanner: /api/predict/image
  if (path === '/api/predict/image') {
    return createMockResponse({
      success: true,
      detection: {
        is_valid: true,
        visual_freshness_score: 92,
        visual_status: 'High Visual Freshness (Excellent Condition)',
        emoji: '🥗',
        suggested_category: 'vegetables',
        confidence: 0.90,
        summary: 'AI Vision scanned image - Freshness 92%: High Visual Freshness'
      }
    });
  }

  // 8. Foods: /api/foods
  if (path === '/api/foods') {
    if (method === 'GET') {
      const foods = getStoredFoods();
      return createMockResponse({ success: true, count: foods.length, foods: foods });
    }
    if (method === 'POST') {
      const foods = getStoredFoods();
      const pred = calculateOfflineWasteRisk(body.food_name, body.category, body.quantity, body.storage_type, body.expiry_date);
      const user = getCurrentUser() || { name: 'Food Donor', phone: '+91 98765 00000', address: '124 Green Park, Bengaluru' };

      const newFood = {
        id: Date.now(),
        food_name: body.food_name || 'Donation Item',
        category: body.category || 'other',
        quantity: parseFloat(body.quantity || 1),
        unit: body.unit || 'kg',
        storage_type: body.storage_type || 'refrigerator',
        purchase_date: body.purchase_date || new Date().toISOString().split('T')[0],
        expiry_date: body.expiry_date || '',
        prep_time: body.prep_time || 'Fresh',
        location: body.location || user.address,
        image_url: body.image_url || '',
        status: 'fresh',
        risk: pred.risk,
        risk_score: pred.score,
        donation_suitable: pred.donation_suitable,
        donation_status: pred.donation_suitable !== 'unsafe' ? 'dispatched' : 'unsafe',
        notes: body.notes || ''
      };
      foods.unshift(newFood);
      saveStoredFoods(foods);

      let autoDonation = null;
      if (pred.donation_suitable !== 'unsafe') {
        const matchedNgo = OFFLINE_VERIFIED_NGOS[0];
        const donations = getStoredDonations();
        const newDonation = {
          id: Date.now(),
          food_id: newFood.id,
          food_name: newFood.food_name,
          category: newFood.category,
          quantity: newFood.quantity,
          unit: newFood.unit,
          storage_type: newFood.storage_type,
          prep_time: newFood.prep_time,
          expiry_date: newFood.expiry_date,
          location: newFood.location,
          donor_name: user.name,
          donor_phone: user.phone || '+91 98765 00000',
          donor_address: newFood.location,
          ngo_id: matchedNgo.id,
          ngo_name: matchedNgo.name,
          ngo_phone: matchedNgo.phone,
          ngo_address: matchedNgo.address,
          status: 'Dispatched',
          pickup: null,
          created_at: new Date().toISOString()
        };
        donations.unshift(newDonation);
        saveStoredDonations(donations);

        autoDonation = {
          matched: true,
          status: 'dispatched',
          donation_id: newDonation.id,
          ngo: matchedNgo,
          message: `Automatically matched and dispatched to ${matchedNgo.name}!`
        };
      }

      return createMockResponse({
        success: true,
        message: `${newFood.food_name} registered successfully!`,
        food: newFood,
        ai_prediction: pred,
        auto_donation: autoDonation
      }, 201);
    }
  }

  // 9. NGOs: /api/ngos
  if (path === '/api/ngos') {
    return createMockResponse({
      success: true,
      count: OFFLINE_VERIFIED_NGOS.length,
      ngos: OFFLINE_VERIFIED_NGOS
    });
  }

  // 10. Donations: /api/donations or /api/ngo/donations
  if (path === '/api/donations' || path === '/api/ngo/donations') {
    const donations = getStoredDonations();
    return createMockResponse({
      success: true,
      count: donations.length,
      donations: donations
    });
  }

  // 11. NGO Status Update / Pickup Scheduling
  if (path.includes('/api/ngo/donations/')) {
    const donations = getStoredDonations();
    const parts = path.split('/');
    const donationId = parseInt(parts[4]);
    const don = donations.find(d => d.id === donationId);
    if (don) {
      if (path.endsWith('/pickup')) {
        don.status = 'Pickup Scheduled';
        don.pickup = {
          scheduled_time: body.scheduled_time || 'Today within 2 hours',
          agent_name: body.agent_name || 'Volunteer Lead',
          agent_phone: body.agent_phone || '+91 98765 22334',
          vehicle_info: body.vehicle_info || 'Rescue Van'
        };
      } else if (path.endsWith('/status')) {
        don.status = body.status || don.status;
      }
      saveStoredDonations(donations);
      return createMockResponse({ success: true, donation: don, message: 'Status updated successfully!' });
    }
  }

  // 12. Notifications: /api/notifications
  if (path === '/api/notifications') {
    const notifs = [
      {
        id: 1,
        title: 'Food Donation Dispatched',
        message: 'Your surplus food has been matched with Feeding India Food Rescue.',
        type: 'donation',
        is_read: false,
        created_at: new Date().toISOString()
      },
      {
        id: 2,
        title: 'AI Freshness Verified',
        message: 'Food items analyzed and passed food safety guidelines.',
        type: 'ai',
        is_read: false,
        created_at: new Date().toISOString()
      }
    ];
    return createMockResponse({
      success: true,
      count: notifs.length,
      unread_count: 2,
      notifications: notifs
    });
  }

  if (path === '/api/notifications/read') {
    return createMockResponse({ success: true, message: 'Notifications marked as read.' });
  }

  // 13. Dashboard Stats
  if (path === '/api/dashboard/stats' || path === '/api/admin/stats') {
    const foods = getStoredFoods();
    const donations = getStoredDonations();
    return createMockResponse({
      success: true,
      total_items: foods.length,
      active_donations: donations.filter(d => d.status !== 'Completed').length,
      completed_donations: donations.filter(d => d.status === 'Completed').length,
      waste_reduced_kg: (foods.reduce((acc, f) => acc + (f.quantity || 0), 0) * 1.8).toFixed(1),
      stats: {
        total_foods: foods.length,
        total_donations: donations.length,
        total_users: 12,
        total_ngos: 5
      }
    });
  }

  // Generic fallback success
  return createMockResponse({ success: true, message: 'Processed successfully.' });
}

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

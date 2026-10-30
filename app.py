"""
FoodWise AI - Local Development Server
Run directly with:
    python app.py
"""
import os
from api.index import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"==================================================")
    print(f" * FoodWise AI Server starting...")
    print(f" * Local URL: http://127.0.0.1:{port}")
    print(f" * Login:     http://127.0.0.1:{port}/pages/login.html")
    print(f" * Signup:    http://127.0.0.1:{port}/pages/signup.html")
    print(f" * Admin:     http://127.0.0.1:{port}/pages/admin_login.html")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=True)


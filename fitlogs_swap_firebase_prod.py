"""
swap_firebase_prod.py — FitLogs
Run this after merging dev into main, before pushing to production.
Restores the production Firebase config.

Usage:
  python3 swap_firebase_prod.py

Place this file in your fitlogs repo root directory.
"""

import re

# ── Production Firebase config — fill these in once ──────────
# Get from Firebase Console -> your fitlogs prod project -> Project Settings -> Config
PROD_CONFIG = {
    "apiKey":            "AIzaSyCijB-swICTSogPkJEy4IUskw4IRCc5eas",
    "authDomain":        "fitlogs-prod.firebaseapp.com",
    "projectId":         "fitlogs-prod",
    "storageBucket":     "fitlogs-prod.firebasestorage.app",
    "messagingSenderId": "637779864992",
    "appId":             "1:637779864992:web:2a709ffa36c49e557e48c5",
}

# ── Railway URLs ──────────────────────────────────────────────
PROD_RAILWAY_URL = "PASTE_FITLOGS_PROD_RAILWAY_URL_HERE"
DEV_RAILWAY_URL  = "PASTE_FITLOGS_DEV_RAILWAY_URL_HERE"

def swap_config(filename="index.html"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already on production config
    if PROD_CONFIG["projectId"] in content:
        print("✅ Already using production Firebase config — no change needed.")
        return

    # Find and replace the initializeApp config block
    pattern = r'(const fbApp\s*=\s*initializeApp\s*\(\s*\{)(.*?)(\}\s*\))'

    new_config_str = """
  apiKey:            "{apiKey}",
  authDomain:        "{authDomain}",
  projectId:         "{projectId}",
  storageBucket:     "{storageBucket}",
  messagingSenderId: "{messagingSenderId}",
  appId:             "{appId}"
""".format(**PROD_CONFIG)

    def replace_config(match):
        return match.group(1) + new_config_str + match.group(3)

    new_content, count = re.subn(pattern, replace_config, content, flags=re.DOTALL)

    if count == 0:
        print("❌ Could not find initializeApp config block.")
        return

    # Also restore production Railway URL
    if PROD_RAILWAY_URL != "PASTE_FITLOGS_PROD_RAILWAY_URL_HERE":
        new_content = new_content.replace(DEV_RAILWAY_URL, PROD_RAILWAY_URL)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Swapped Firebase config to production ({PROD_CONFIG['projectId']})")
    print(f"   authDomain: {PROD_CONFIG['authDomain']}")
    print(f"   projectId:  {PROD_CONFIG['projectId']}")

if __name__ == "__main__":
    swap_config()
    print("\nNext steps:")
    print("  git add index.html")
    print('  git commit -m "Restore production Firebase config"')
    print("  git push origin main")

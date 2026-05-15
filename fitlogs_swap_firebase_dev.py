"""
swap_firebase_dev.py — FitLogs
Run this after copying index.html to the dev branch.
Replaces the production Firebase config with the dev config.

Usage:
  python3 swap_firebase_dev.py

Place this file in your fitlogs repo root directory.
"""

import re

# ── Dev Firebase config — fill these in once ─────────────────
# Get from Firebase Console -> your fitlogs dev project -> Project Settings -> Config
DEV_CONFIG = {
    "apiKey":            "AIzaSyB4tzLecMq4YdFsNvhSyPBTMWYhgtiv1Y0",
    "authDomain":        "fitlogs-dev.firebaseapp.com",
    "projectId":         "fitlogs-dev",
    "storageBucket":     "fitlogs-dev.firebasestorage.app",
    "messagingSenderId": "449996807760",
    "appId":             "1:449996807760:web:3b79c5788e88dbf4b57b55",
}

# ── Dev Railway URL (if applicable) ──────────────────────────
DEV_RAILWAY_URL  = "PASTE_FITLOGS_DEV_RAILWAY_URL_HERE"
PROD_RAILWAY_URL = "PASTE_FITLOGS_PROD_RAILWAY_URL_HERE"

def swap_config(filename="index.html"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already on dev config
    if DEV_CONFIG["projectId"] in content:
        print("✅ Already using dev Firebase config — no change needed.")
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
""".format(**DEV_CONFIG)

    def replace_config(match):
        return match.group(1) + new_config_str + match.group(3)

    new_content, count = re.subn(pattern, replace_config, content, flags=re.DOTALL)

    if count == 0:
        print("❌ Could not find initializeApp config block. Check the pattern.")
        return

    # Also swap Railway URL if configured
    if DEV_RAILWAY_URL != "PASTE_FITLOGS_DEV_RAILWAY_URL_HERE":
        new_content = new_content.replace(PROD_RAILWAY_URL, DEV_RAILWAY_URL)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Swapped Firebase config to dev ({DEV_CONFIG['projectId']})")
    print(f"   authDomain: {DEV_CONFIG['authDomain']}")
    print(f"   projectId:  {DEV_CONFIG['projectId']}")

if __name__ == "__main__":
    swap_config()
    print("\nNext steps:")
    print("  git add index.html")
    print('  git commit -m "Update dev Firebase config"')
    print("  git push origin dev")

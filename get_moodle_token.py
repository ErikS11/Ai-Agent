"""Get a student's Moodle token (the same one the Moodle mobile app uses).

Run:  python get_moodle_token.py
Signs in once with the student's Moodle username and password and prints the token
to paste into .env as MOODLE_TOKEN. The password is not saved anywhere.
Requires: Site administration > General > Mobile app > Mobile settings >
"Enable web services for mobile devices" turned on.
"""

import getpass
import os

import requests
from dotenv import load_dotenv

load_dotenv()
base = os.getenv("MOODLE_URL", "http://localhost:8080").rstrip("/")
username = input(f"Moodle username at {base}: ").strip()
password = getpass.getpass("Password (hidden): ")

r = requests.post(
    f"{base}/login/token.php",
    data={"username": username, "password": password, "service": "moodle_mobile_app"},
    timeout=30,
)
r.raise_for_status()
data = r.json()
if "token" in data:
    print(f"\nToken for {username}:\n{data['token']}\n\nPut it in .env as MOODLE_TOKEN=...")
else:
    print(f"\nMoodle said: {data.get('error') or data}")
    print("Check the username/password, and that mobile web services are enabled.")

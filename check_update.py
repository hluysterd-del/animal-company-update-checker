import requests
import json
import os
import sys
from datetime import datetime, timezone

APP_ID = "6741173617"
APP_NAME = "Animal Company"
ITUNES_API = f"https://itunes.apple.com/lookup?id={APP_ID}"
DECRYPT_URL = f"https://decrypt.day/app/id{APP_ID}"
VERSION_FILE = "last_known_version.txt"

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")


def get_current_version():
    """Fetch the current version from the iTunes API."""
    resp = requests.get(ITUNES_API, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data["resultCount"] == 0:
        raise Exception("App not found on iTunes API")
    result = data["results"][0]
    return result["version"], result.get("releaseNotes", "No release notes")


def get_last_known_version():
    """Read the last known version from file."""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    return None


def save_version(version):
    """Save the current version to file."""
    with open(VERSION_FILE, "w") as f:
        f.write(version)


def send_discord_webhook(version, release_notes):
    """Send update notification to Discord."""
    embed = {
        "title": f"🐾 {APP_NAME} IPA Updated!",
        "description": (
            f"**To:** `{version}`\n\n"
            f"**Release Notes:**\n{release_notes}\n\n"
            f"[View on decrypt.day]({DECRYPT_URL})"
        ),
        "color": 0x57F287,  # green
        "footer": {"text": "Animal Company Update Checker"},
    }
    payload = {
        "content": "@everyone @here",
        "embeds": [embed],
    }
    resp = requests.post(DISCORD_WEBHOOK, json=payload, timeout=15)
    resp.raise_for_status()
    print(f"Webhook sent successfully for version {version}")


def update_status_page(current_version, release_notes, updated):
    """Update the status JSON file for the GitHub Pages website."""
    status = {
        "app_name": APP_NAME,
        "current_version": current_version,
        "release_notes": release_notes,
        "last_checked": datetime.now(timezone.utc).isoformat(),
        "decrypt_url": DECRYPT_URL,
        "updated_this_run": updated,
    }
    os.makedirs("docs", exist_ok=True)
    with open("docs/status.json", "w") as f:
        json.dump(status, f, indent=2)


def main():
    force = "--force" in sys.argv

    print("Checking for Animal Company updates...")
    current_version, release_notes = get_current_version()
    print(f"Current version: {current_version}")

    last_version = get_last_known_version()
    print(f"Last known version: {last_version or 'None (first run)'}")

    updated = False
    if force or last_version is None or current_version != last_version:
        if last_version is None:
            print("First run — sending current version notification")
        elif force:
            print("Forced send")
        else:
            print(f"New update detected: {last_version} -> {current_version}")

        send_discord_webhook(current_version, release_notes)
        save_version(current_version)
        updated = True
    else:
        print("No new update found.")

    update_status_page(current_version, release_notes, updated)


if __name__ == "__main__":
    main()

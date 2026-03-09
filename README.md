# Animal Company IPA Update Checker

Monitors [Animal Company Companion](https://decrypt.day/app/id6741173617) for updates and sends Discord webhook notifications with `@everyone`.

## How it works

- Checks the Apple iTunes API every 15 minutes via GitHub Actions
- Compares the current version against the last known version stored in `last_known_version.txt`
- If a new version is detected, sends a Discord webhook notification
- Runs 24/7 automatically

## Setup

1. **Create a new GitHub repository** (private recommended)

2. **Push this folder to the repo:**
   ```bash
   cd animal-company-update-checker
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. **Add your Discord webhook as a secret:**
   - Go to your repo → **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `DISCORD_WEBHOOK`
   - Value: your Discord webhook URL
   - Click **Add secret**

4. **Enable GitHub Actions:**
   - Go to your repo → **Actions** tab
   - Enable workflows if prompted
   - The checker will run automatically every 15 minutes

5. **First run:** Click **Actions** → **Check Animal Company Updates** → **Run workflow** to trigger it manually and send the first notification.

## Run locally

```bash
pip install requests
python check_update.py
```

Use `--force` flag to send the webhook even if no new version is found:
```bash
python check_update.py --force
```

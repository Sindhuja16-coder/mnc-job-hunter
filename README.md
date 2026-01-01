# 🚀 Daily Job Hunter Bot

A fully automated Python bot that scrapes the web for fresh job listings and delivers a summary directly to your inbox every morning.

## 🛠 Tech Stack
- **Python 3.9** (Scripting & Logic)
- **GitHub Actions** (CI/CD Automation & Scheduling)
- **SerpApi** (Google Search API)
- **SMTP Library** (Email Notifications)

## ⚙️ How It Works
1. The bot wakes up automatically at **9:00 AM IST** (via GitHub Actions Cron).
2. It searches Google Jobs for specific keywords (e.g., "Intune Administrator", "Fresher").
3. It filters the results to ensure they are relevant.
4. It sends a formatted email with the top 10 job links.

## 🚀 How to Use This (Setup)

Want to run this for yourself? Follow these steps:

### 1. Fork this Repository
Click the **Fork** button at the top right of this page to save a copy to your own GitHub account.

### 2. Get Your API Keys
- **SerpApi:** Sign up at [SerpApi](https://serpapi.com/) and get your free API Key.
- **Gmail App Password:** Go to your Google Account > Security > 2-Step Verification > App Passwords, and generate a password for the bot.

### 3. Set Up GitHub Secrets
Go to **Settings** > **Secrets and variables** > **Actions** > **New repository secret** and add these four:

| Secret Name | Value |
| :--- | :--- |
| `SERPAPI_KEY` | Your SerpApi Key |
| `EMAIL_USER` | Your Gmail address (sender) |
| `EMAIL_PASS` | Your Gmail App Password |
| `EMAIL_RECEIVER` | The email address to receive alerts |

### 4. Enable the Workflow
Go to the **Actions** tab and enable the workflow. It will now run automatically every day!

## 🤝 Contributing
Feel free to fork this repo and submit Pull Requests if you want to add features like WhatsApp alerts or LinkedIn scraping!

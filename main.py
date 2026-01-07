import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from serpapi import GoogleSearch

# ==========================================
# 👇 PASTE YOUR KEYS INSIDE THE QUOTES BELOW 👇
# ==========================================
# (Keep these secret! We will remove them before uploading to GitHub)

# --- CLOUD CONFIGURATION ---
# This tells the script: "Don't look here. Look in the GitHub secure vault."
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")

# Safety Check: If the keys are missing, stop the script.
if not SERPAPI_KEY or not EMAIL_USER:
    print("Error: Keys not found. Make sure they are set in GitHub Secrets.")
    exit(1)

# ==========================================

# TARGET_MNCS: The script highlights these companies in GREEN in your email.
TARGET_MNCS = [
    "Accenture", "Capgemini", "Microsoft", "Oracle", "Infosys", 
    "TCS", "Wipro", "HCL", "Deloitte", "IBM", "Genpact", "Mindtree"
]

def search_jobs():
    print("Searching for jobs...")
    
    # We search for "Endpoint Administrator" OR "Intune" 
    # The 'chips' parameter ensures we only get jobs posted 'today' or '3 days ago'
    params = {
        "api_key": SERPAPI_KEY, 
        "engine": "google_jobs",
        "q": "End user support Hyderabad, Endpoint Engineer, Intune administraor", # Very simple query to test
        "google_domain": "google.co.in",
        "gl": "in",
        "hl": "en"
        # We removed "chips" completely to get ALL jobs (old and new)
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("jobs_results", [])
    except Exception as e:
        print(f"❌ API Error: {e}")
        return []

def filter_and_format(job, count, email_content):
    # Get job details and convert title to lowercase
    title = job.get("title", "")
    company = job.get("company", "")
    location = job.get("location", "")
    job_title_lower = title.lower()

    # A. SKIP if it's a Senior/Manager/Lead role
    if any(word in job_title_lower for word in ["senior", "manager", "lead", "architect"]):
        return count, email_content

    # B. SKIP if it requires 5+, 8+, or 10+ years
    if any(years in job_title_lower for years in ["10+ years", "8+ years", "5+ years"]):
        return count, email_content

    # Determine the best link to use
    link = job.get("share_link")
    if job.get("related_links"):
        link = job.get("related_links")[0].get("link")

    # Check if it matches your target MNC list
    is_mnc = any(mnc.lower() in company.lower() for mnc in TARGET_MNCS)

    # Set styles based on MNC status
    if is_mnc:
        style, prefix = "color: green; font-weight: bold; font-size: 1.1em;", "★ [MNC MATCH] "
    else:
        style, prefix = "color: #333;", ""

    # Build the HTML content for this job
    email_content += f"""
    <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
        <div style="{style}">{prefix}{title}</div>
        <div style="color: #555;">🏢 <b>{company}</b> | 📍 {location}</div>
        <div style="margin-top: 5px;">
            <a href="{link}" style="background-color: #007bff; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">View Job</a>
        </div>
    </div>
    """
    return count + 1, email_content
    if count == 0:
        print("⚠️ No new jobs found today. No email sent.")
        return

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = f"🚀 {count} New Endpoint Admin Jobs Found"

    body = f"""
    <h3>Daily Job Alert for {datetime.now().strftime('%Y-%m-%d')}</h3>
    <p>Found {count} jobs matching your profile in Hyderabad.</p>
    <hr>
    {content}
    """
    
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"Email Sent Successfully to {EMAIL_RECEIVER}!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    if "PASTE_YOUR" in SERPAPI_KEY or "PASTE_YOUR" in EMAIL_PASS:
        print("❌ STOP: You didn't paste your API Keys in the code yet!")
    else:
        jobs = search_jobs()
        if jobs:
            count = 0
            email_content = ""
            for job in jobs:
                count, email_content = filter_and_format(job, count, email_content)
            
            send_email(count, email_content)








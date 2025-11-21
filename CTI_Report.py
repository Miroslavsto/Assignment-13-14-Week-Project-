# CTI Threat Briefing Script
# Student: Miroslav Stojanovic
# Course: CIS 226
# Date: November 14, 2025

import requests
from fpdf import FPDF
from datetime import datetime

# -------------------------------
# Step 1: Set the email to check
# -------------------------------
email_to_check = "employee@example.com"  # Replace with the target email

# HIBP API settings
api_key = "YOUR_HIBP_API_KEY_HERE"       # Replace with your API key
hibp_api_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email_to_check}"

headers = {
    "User-Agent": "CTI‑Report‑Script",
    "hibp-api-key": api_key
}

# -------------------------------
# Step 2: Call the HIBP API
# -------------------------------
response = requests.get(hibp_api_url, headers=headers)

if response.status_code == 200:
    breaches = response.json()
elif response.status_code == 404:
    # 404 means no breaches found for that email
    breaches = []
else:
    # Other status codes indicate an error
    print(f"Error: HTTP status {response.status_code}")
    breaches = []

# -------------------------------
# Step 3: Generate PDF report
# -------------------------------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Daily CTI Threat Briefing", ln=True, align="C")
pdf.set_font("Arial", '', 12)
pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
pdf.ln(10)

if breaches:
    pdf.cell(0, 10, f"Breaches found for {email_to_check}:", ln=True)
    pdf.ln(5)
    for breach in breaches:
        title = breach.get('Title', 'Unknown')
        date = breach.get('BreachDate', 'Unknown')
        pdf.multi_cell(0, 8, f"- {title} ({date})")
else:
    pdf.cell(0, 10, f"No breaches found for {email_to_check}.", ln=True)

# -------------------------------
# Step 4: Save PDF
# -------------------------------
pdf_file_name = f"CTI_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
pdf.output(pdf_file_name)

print(f"PDF report generated: {pdf_file_name}")

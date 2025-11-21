import requests
from datetime import datetime, timedelta
from fpdf import FPDF

# Set API endpoint and headers
url = "https://haveibeenpwned.com/api/v3/breaches"
headers = {"User-Agent": "CTI-Lab-Student"}

# Send GET request to HIBP API
response = requests.get(url, headers=headers)
if not response.ok:
    print("Error fetching data:", response.status_code)
    exit()

# Convert response to JSON
breaches = response.json()

# Calculate date range for recent breaches
today = datetime.utcnow()
week_ago = today - timedelta(days=7)

# Filter breaches added in the last 7 days
recent_breaches = []
for breach in breaches:
    added_date_str = breach.get("AddedDate", "")
    if added_date_str:
        added_date = datetime.strptime(added_date_str, "%Y-%m-%dT%H:%M:%SZ")
        if added_date >= week_ago:
            recent_breaches.append({
                "Name": breach["Name"],
                "Domain": breach["Domain"],
                "BreachDate": breach["BreachDate"],
                "AddedDate": added_date_str,
                "DataClasses": breach["DataClasses"],
                "Description": breach["Description"]
            })

# Print breach info to console
if not recent_breaches:
    print("No new breaches in the last 7 days.")
else:
    print("ALERT: Recent Breaches (Last 7 Days):\n")
    for breach in recent_breaches:
        print(f"Name: {breach['Name']}")
        print(f"Domain: {breach['Domain']}")
        print(f"Breach Date: {breach['BreachDate']}")
        print(f"Added to HIBP: {breach['AddedDate']}")
        print(f"Data Exposed: {', '.join(breach['DataClasses'])}")
        print(f"Summary: {breach['Description'][:150]}...")
        print("-" * 50)
# Generate PDF report
if recent_breaches:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Weekly CTI Report: Recent Breaches", ln=True, align="C")
    pdf.ln(10)

    for breach in recent_breaches:
        pdf.multi_cell(0, 10, f"""
Name: {breach['Name']}
Domain: {breach['Domain']}
Breach Date: {breach['BreachDate']}
Added to HIBP: {breach['AddedDate']}
Data Exposed: {', '.join(breach['DataClasses'])}
Summary: {breach['Description'][:300]}...
        """)
        pdf.ln()

    filename = f"hibp_breach_report_{today.strftime('%Y-%m-%d')}.pdf"
    pdf.output(filename)
    print(f"\nPDF report saved as: {filename}")

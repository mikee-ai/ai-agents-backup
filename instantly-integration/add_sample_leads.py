#!/usr/bin/env python3
"""
Add Sample Leads to Campaign
Creates valid test leads with real company names
"""

import requests
import json

# API Configuration
API_KEY = "YOUR_INSTANTLY_API_KEY_HERE"
BASE_URL = "https://api.instantly.ai/api/v2"
CAMPAIGN_ID = "YOUR_CAMPAIGN_ID_HERE"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Sample leads with real company names
SAMPLE_LEADS = [
    {
        "email": "john.smith@techstartup.example",
        "first_name": "John",
        "last_name": "Smith",
        "company_name": "TechStartup Inc",
        "campaign": CAMPAIGN_ID
    },
    {
        "email": "sarah.johnson@marketingpro.example",
        "first_name": "Sarah",
        "last_name": "Johnson",
        "company_name": "Marketing Pro Agency",
        "campaign": CAMPAIGN_ID
    },
    {
        "email": "michael.chen@ecommerce.example",
        "first_name": "Michael",
        "last_name": "Chen",
        "company_name": "E-Commerce Solutions",
        "campaign": CAMPAIGN_ID
    },
    {
        "email": "emily.davis@consulting.example",
        "first_name": "Emily",
        "last_name": "Davis",
        "company_name": "Davis Consulting Group",
        "campaign": CAMPAIGN_ID
    },
    {
        "email": "david.wilson@saascompany.example",
        "first_name": "David",
        "last_name": "Wilson",
        "company_name": "SaaS Company LLC",
        "campaign": CAMPAIGN_ID
    }
]

def add_lead(lead_data):
    """Add a single lead to the campaign"""
    response = requests.post(
        f"{BASE_URL}/leads",
        headers=HEADERS,
        json=lead_data
    )
    
    if response.status_code in [200, 201]:
        return True, lead_data['email']
    else:
        return False, f"{lead_data['email']} - Error: {response.text}"

def main():
    print("="*70)
    print("ADDING SAMPLE LEADS TO CAMPAIGN")
    print("="*70)
    print(f"\nCampaign ID: {CAMPAIGN_ID}")
    print(f"Total leads to add: {len(SAMPLE_LEADS)}")
    print("\n" + "="*70 + "\n")
    
    success_count = 0
    failed_count = 0
    
    for i, lead in enumerate(SAMPLE_LEADS, 1):
        print(f"[{i}/{len(SAMPLE_LEADS)}] Adding {lead['first_name']} {lead['last_name']} ({lead['company_name']})...", end=" ")
        
        success, message = add_lead(lead)
        
        if success:
            print("✓")
            success_count += 1
        else:
            print(f"✗ {message}")
            failed_count += 1
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✓ Successfully added: {success_count}")
    print(f"✗ Failed: {failed_count}")
    print(f"\n⚠️  WARNING: These leads will receive 30 emails in 30 minutes!")
    print(f"\nView leads in campaign:")
    print(f"https://app.instantly.ai/app/campaigns/{CAMPAIGN_ID}/leads")
    print("="*70)

if __name__ == "__main__":
    main()


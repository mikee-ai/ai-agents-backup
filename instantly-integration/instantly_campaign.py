#!/usr/bin/env python3
"""
Instantly.ai API Integration Script
Creates a cold email campaign with maximum sending capabilities
"""

import requests
import json
from datetime import datetime, timedelta

# API Configuration
API_KEY = "b5371cca-dcb4-4923-81df-d85777c69987:fvUoAqYEXpDE"
BASE_URL = "https://api.instantly.ai/api/v2"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_authentication():
    """Test API authentication by listing campaigns"""
    print("Testing API authentication...")
    response = requests.get(f"{BASE_URL}/campaigns", headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def list_email_accounts():
    """List available email accounts for sending"""
    print("\nListing email accounts...")
    response = requests.get(f"{BASE_URL}/accounts", headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        accounts = response.json()
        print(f"Response: {json.dumps(accounts, indent=2)}")
        return accounts
    else:
        print(f"Error: {response.text}")
        return None

def create_campaign(email_accounts):
    """Create a cold email campaign with maximum sending settings"""
    print("\nCreating cold email campaign...")
    
    # Extract email addresses from accounts
    email_list = []
    if email_accounts and 'data' in email_accounts:
        email_list = [acc['email'] for acc in email_accounts['data'] if acc.get('email')]
    
    # If no accounts found, we'll create the campaign structure anyway
    if not email_list:
        print("Warning: No email accounts found. Campaign will be created but needs email accounts to send.")
        email_list = []
    
    campaign_data = {
        "name": "Maximum Outreach Campaign - Daily",
        "campaign_schedule": {
            "schedules": [
                {
                    "name": "Weekday Schedule",
                    "timing": {
                        "from": "08:00",
                        "to": "18:00"
                    },
                    "days": {
                        "0": False,  # Sunday
                        "1": True,   # Monday
                        "2": True,   # Tuesday
                        "3": True,   # Wednesday
                        "4": True,   # Thursday
                        "5": True,   # Friday
                        "6": False   # Saturday
                    },
                    "timezone": "America/New_York"
                },
                {
                    "name": "Weekend Schedule",
                    "timing": {
                        "from": "09:00",
                        "to": "17:00"
                    },
                    "days": {
                        "0": True,   # Sunday
                        "1": False,
                        "2": False,
                        "3": False,
                        "4": False,
                        "5": False,
                        "6": True    # Saturday
                    },
                    "timezone": "America/New_York"
                }
            ],
            "start_date": datetime.utcnow().isoformat() + "Z",
            "end_date": None  # No end date for continuous sending
        },
        "sequences": [
            {
                "steps": [
                    {
                        "variants": [
                            {
                                "subject": "Quick question about {{company_name}}",
                                "body": "Hi {{first_name}},\n\nI noticed {{company_name}} and wanted to reach out.\n\n{{personalization}}\n\nWould you be open to a quick chat?\n\nBest regards"
                            }
                        ],
                        "wait_time_hours": 0,
                        "wait_time_minutes": 0
                    },
                    {
                        "variants": [
                            {
                                "subject": "Re: Quick question about {{company_name}}",
                                "body": "Hi {{first_name}},\n\nJust following up on my previous email.\n\nI'd love to discuss how we can help {{company_name}}.\n\nLet me know if you're interested.\n\nBest"
                            }
                        ],
                        "wait_time_hours": 48,
                        "wait_time_minutes": 0
                    },
                    {
                        "variants": [
                            {
                                "subject": "Re: Quick question about {{company_name}}",
                                "body": "Hi {{first_name}},\n\nLast follow-up from me.\n\nIf you're interested in learning more, I'm here to help.\n\nThanks for your time!"
                            }
                        ],
                        "wait_time_hours": 72,
                        "wait_time_minutes": 0
                    }
                ]
            }
        ],
        "email_list": email_list,
        "daily_limit": 500,  # Maximum daily emails per account
        "daily_max_leads": 500,  # Maximum new leads to contact daily
        "email_gap": 5,  # 5 minutes between emails
        "random_wait_max": 15,  # Random wait up to 15 minutes
        "stop_on_reply": True,  # Stop when lead replies
        "stop_on_auto_reply": True,  # Stop on auto-reply
        "link_tracking": True,  # Track link clicks
        "open_tracking": True,  # Track email opens
        "text_only": False,  # Send HTML emails
        "first_email_text_only": False,
        "prioritize_new_leads": True,  # Prioritize new leads
        "match_lead_esp": False,
        "stop_for_company": True,  # Stop for entire company on reply
        "insert_unsubscribe_header": True,
        "allow_risky_contacts": False,
        "disable_bounce_protect": False
    }
    
    response = requests.post(f"{BASE_URL}/campaigns", headers=HEADERS, json=campaign_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code in [200, 201]:
        campaign = response.json()
        print(f"Campaign created successfully!")
        print(f"Campaign ID: {campaign.get('id')}")
        print(f"Response: {json.dumps(campaign, indent=2)}")
        return campaign
    else:
        print(f"Error creating campaign: {response.text}")
        return None

def add_sample_leads(campaign_id):
    """Add sample leads to the campaign"""
    print(f"\nAdding sample leads to campaign {campaign_id}...")
    
    sample_leads = [
        {
            "email": "lead1@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "company_name": "Example Corp",
            "personalization": "I saw your recent work on AI and thought we could collaborate.",
            "campaign": campaign_id
        },
        {
            "email": "lead2@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "company_name": "Tech Solutions Inc",
            "personalization": "Your company's growth in the tech sector is impressive.",
            "campaign": campaign_id
        }
    ]
    
    for lead in sample_leads:
        response = requests.post(f"{BASE_URL}/leads", headers=HEADERS, json=lead)
        if response.status_code in [200, 201]:
            print(f"✓ Added lead: {lead['email']}")
        else:
            print(f"✗ Failed to add lead {lead['email']}: {response.text}")
    
    return True

def activate_campaign(campaign_id):
    """Activate the campaign to start sending"""
    print(f"\nActivating campaign {campaign_id}...")
    response = requests.post(f"{BASE_URL}/campaigns/{campaign_id}/activate", headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code in [200, 201]:
        print("Campaign activated successfully!")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    else:
        print(f"Error activating campaign: {response.text}")
        return False

def get_campaign_analytics(campaign_id):
    """Get campaign analytics"""
    print(f"\nFetching analytics for campaign {campaign_id}...")
    response = requests.get(
        f"{BASE_URL}/campaigns/analytics",
        headers=HEADERS,
        params={"campaign_id": campaign_id}
    )
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        analytics = response.json()
        print(f"Analytics: {json.dumps(analytics, indent=2)}")
        return analytics
    else:
        print(f"Error fetching analytics: {response.text}")
        return None

def main():
    """Main execution function"""
    print("=" * 60)
    print("Instantly.ai Cold Email Campaign Setup")
    print("=" * 60)
    
    # Step 1: Test authentication
    if not test_authentication():
        print("\n❌ Authentication failed. Please check your API key.")
        return
    
    print("\n✓ Authentication successful!")
    
    # Step 2: List email accounts
    email_accounts = list_email_accounts()
    
    # Step 3: Create campaign
    campaign = create_campaign(email_accounts)
    if not campaign:
        print("\n❌ Failed to create campaign.")
        return
    
    campaign_id = campaign.get('id')
    print(f"\n✓ Campaign created with ID: {campaign_id}")
    
    # Step 4: Add sample leads (optional - comment out if not needed)
    # add_sample_leads(campaign_id)
    
    # Step 5: Activate campaign (commented out for safety - uncomment to activate)
    # activate_campaign(campaign_id)
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print(f"\nCampaign ID: {campaign_id}")
    print("\nNext steps:")
    print("1. Add leads to the campaign using the API or Instantly.ai dashboard")
    print("2. Uncomment activate_campaign() in the script to start sending")
    print("3. Monitor campaign performance through analytics")
    print("\nNote: Campaign is created but NOT activated for safety.")
    print("Activate it manually when ready to start sending emails.")

if __name__ == "__main__":
    main()


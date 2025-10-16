#!/usr/bin/env python3
"""
Instantly.ai Cold Email Campaign Creator
AI Agents: Help Businesses Make Money & Save Money
"""

import requests
import json
from datetime import datetime

# API Configuration - DO NOT DECODE, use the base64 string directly
API_KEY = "YOUR_INSTANTLY_API_KEY_HERE"
BASE_URL = "https://api.instantly.ai/api/v2"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_auth():
    """Test API authentication"""
    print("Testing API connection...")
    response = requests.get(f"{BASE_URL}/campaigns", headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Connected! Found {len(data.get('items', []))} existing campaigns")
        return True
    else:
        print(f"✗ Connection failed: {response.text}")
        return False

def list_accounts():
    """List email accounts"""
    print("\nFetching email accounts...")
    response = requests.get(f"{BASE_URL}/accounts", headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        accounts = data.get('items', [])
        print(f"Found {len(accounts)} email account(s):")
        email_list = []
        for acc in accounts:
            email = acc.get('email')
            status = acc.get('status', 'unknown')
            print(f"  - {email} (status: {status})")
            if email:
                email_list.append(email)
        return email_list
    else:
        print(f"Error: {response.text}")
        return []

def create_campaign(email_list):
    """Create AI Agent cold email campaign"""
    print("\n" + "="*70)
    print("Creating AI Agent Campaign...")
    print("="*70)
    
    campaign_data = {
        "name": "AI Agents - Make & Save Money (Max Outreach)",
        "campaign_schedule": {
            "schedules": [
                {
                    "name": "Weekday Business Hours",
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
                    "timezone": "America/Chicago"
                },
                {
                    "name": "Weekend Hours",
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
                    "timezone": "America/Chicago"
                }
            ],
            "start_date": datetime.utcnow().isoformat() + "Z"
        },
        "sequences": [
            {
                "steps": [
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Save 20+ hours/week with AI agents at {{company_name}}",
                                "body": """Hi {{first_name}},

I noticed {{company_name}} and wanted to reach out about something that could significantly impact your bottom line.

We help businesses like yours deploy AI agents that:
• Generate revenue through automated outreach & sales
• Save money by automating repetitive tasks  
• Free up 20+ hours per week for your team

{{personalization}}

Most of our clients see ROI within the first month - either through increased revenue or cost savings (often both).

Would you be open to a 15-minute call to explore how AI agents could help {{company_name}} make or save money?

Best regards"""
                            },
                            {
                                "subject": "{{first_name}}, automate your way to higher profits",
                                "body": """Hi {{first_name}},

Quick question: What would an extra $10K-50K/month mean for {{company_name}}?

We specialize in deploying AI agents that either:
1. Make you money (automated sales, lead generation, customer engagement)
2. Save you money (replacing manual tasks, reducing overhead)
3. Both (which is what usually happens)

{{personalization}}

Real results from our clients:
✓ 40% reduction in operational costs
✓ 3x increase in qualified leads
✓ Teams freed up to focus on high-value work

Interested in learning how this could work for {{company_name}}?

Best"""
                            }
                        ],
                        "delay": 0
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Save 20+ hours/week with AI agents at {{company_name}}",
                                "body": """Hi {{first_name}},

Just following up on my previous email about AI agents.

I wanted to share a quick case study: One of our clients in your industry automated their customer follow-up process and saw:
• 35% increase in conversion rates
• $25K saved per month in labor costs
• Sales team could focus on closing deals instead of admin work

The setup took less than 2 weeks.

Would you like to see how we could create something similar for {{company_name}}?

Happy to jump on a quick call this week.

Best"""
                            }
                        ],
                        "delay": 2880
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Save 20+ hours/week with AI agents at {{company_name}}",
                                "body": """Hi {{first_name}},

Last follow-up from me - I don't want to be a pest!

I genuinely believe AI agents could help {{company_name}} either:
• Increase revenue through automation
• Reduce costs significantly
• Both

If you're interested, I'm here to help. If not, no worries at all.

Either way, I wish you and {{company_name}} continued success.

Best regards

P.S. If timing isn't right now, feel free to reach out when it makes sense. This offer stands."""
                            }
                        ],
                        "delay": 4320
                    }
                ]
            }
        ],
        "email_list": email_list,
        "daily_limit": 500,
        "daily_max_leads": 500,
        "email_gap": 5,
        "random_wait_max": 15,
        "stop_on_reply": True,
        "stop_on_auto_reply": True,
        "link_tracking": True,
        "open_tracking": True,
        "text_only": False,
        "first_email_text_only": False,
        "prioritize_new_leads": True,
        "match_lead_esp": False,
        "stop_for_company": True,
        "insert_unsubscribe_header": True,
        "allow_risky_contacts": False,
        "disable_bounce_protect": False
    }
    
    response = requests.post(f"{BASE_URL}/campaigns", headers=HEADERS, json=campaign_data)
    
    if response.status_code in [200, 201]:
        campaign = response.json()
        print("✓ Campaign created successfully!")
        print(f"\nCampaign Details:")
        print(f"  ID: {campaign.get('id')}")
        print(f"  Name: {campaign.get('name')}")
        print(f"  Status: {campaign.get('status')} (0=Draft, 1=Active, 2=Paused)")
        print(f"  Daily Limit: {campaign.get('daily_limit')} emails/account")
        print(f"  Daily Max Leads: {campaign.get('daily_max_leads')}")
        return campaign
    else:
        print(f"✗ Error: {response.text}")
        return None

def add_sample_leads(campaign_id):
    """Add sample leads"""
    print(f"\nAdding sample leads to campaign...")
    
    leads = [
        {
            "email": "founder@techstartup.example",
            "first_name": "Sarah",
            "last_name": "Johnson",
            "company_name": "Tech Startup Inc",
            "personalization": "I saw your company is scaling fast and thought AI automation could help you grow even faster.",
            "campaign": campaign_id
        },
        {
            "email": "ceo@marketingagency.example",
            "first_name": "Michael",
            "last_name": "Chen",
            "company_name": "Marketing Pro Agency",
            "personalization": "I noticed your agency handles multiple clients - AI agents could help you scale without hiring more people.",
            "campaign": campaign_id
        }
    ]
    
    added = 0
    for lead in leads:
        response = requests.post(f"{BASE_URL}/leads", headers=HEADERS, json=lead)
        if response.status_code in [200, 201]:
            print(f"  ✓ Added: {lead['email']}")
            added += 1
        else:
            print(f"  ✗ Failed: {lead['email']}")
    
    print(f"\nAdded {added}/{len(leads)} sample leads")
    return added > 0

def activate_campaign(campaign_id):
    """Activate campaign"""
    print(f"\nActivating campaign...")
    response = requests.post(f"{BASE_URL}/campaigns/{campaign_id}/activate", headers=HEADERS)
    
    if response.status_code in [200, 201]:
        print("✓ Campaign activated and sending!")
        return True
    else:
        print(f"✗ Error: {response.text}")
        return False

def main():
    print("="*70)
    print("INSTANTLY.AI - AI AGENTS COLD EMAIL CAMPAIGN")
    print("Help Businesses Make Money & Save Money with AI")
    print("="*70)
    
    # Test connection
    if not test_auth():
        print("\n❌ Cannot connect to Instantly.ai API")
        return
    
    # Get email accounts
    email_list = list_accounts()
    if not email_list:
        print("\n⚠️  No email accounts found!")
        print("Please add email accounts in Instantly.ai dashboard first.")
        print("Continuing with empty email list...")
    
    # Create campaign
    campaign = create_campaign(email_list)
    if not campaign:
        print("\n❌ Failed to create campaign")
        return
    
    campaign_id = campaign.get('id')
    
    # Ask to add sample leads
    print("\n" + "="*70)
    choice = input("Add sample leads? (yes/no): ").strip().lower()
    if choice in ['yes', 'y']:
        add_sample_leads(campaign_id)
    
    # Ask to activate
    print("\n" + "="*70)
    choice = input("ACTIVATE campaign now? (yes/no): ").strip().lower()
    if choice in ['yes', 'y']:
        activate_campaign(campaign_id)
    else:
        print("\n⚠️  Campaign created but NOT activated")
    
    # Summary
    print("\n" + "="*70)
    print("SETUP COMPLETE!")
    print("="*70)
    print(f"\n📧 Campaign ID: {campaign_id}")
    print(f"📊 Dashboard: https://app.instantly.ai/app/campaigns/{campaign_id}")
    print(f"\n💡 Next Steps:")
    print("1. Add your lead list (CSV import or API)")
    print("2. Activate campaign when ready")
    print("3. Monitor replies and analytics")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()


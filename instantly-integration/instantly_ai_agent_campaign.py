#!/usr/bin/env python3
"""
Instantly.ai API Integration Script
Cold Email Campaign: AI Agents to Make Money & Save Money
"""

import requests
import json
from datetime import datetime

# API Configuration
API_KEY = "b5371cca-dcb4-4923-81df-d85777c69987:fvUoAqYEXpDE"
BASE_URL = "https://api.instantly.ai/api/v2"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_authentication():
    """Test API authentication"""
    print("Testing API authentication...")
    response = requests.get(f"{BASE_URL}/campaigns", headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✓ Authentication successful!")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def list_email_accounts():
    """List available email accounts for sending"""
    print("\nListing email accounts...")
    response = requests.get(f"{BASE_URL}/accounts", headers=HEADERS)
    if response.status_code == 200:
        accounts = response.json()
        if 'data' in accounts and len(accounts['data']) > 0:
            print(f"Found {len(accounts['data'])} email account(s)")
            for acc in accounts['data']:
                print(f"  - {acc.get('email', 'N/A')}")
            return accounts
        else:
            print("No email accounts found. Please add email accounts in Instantly.ai dashboard.")
            return None
    else:
        print(f"Error: {response.text}")
        return None

def create_ai_agent_campaign(email_accounts):
    """Create AI Agent value proposition campaign"""
    print("\nCreating AI Agent Campaign...")
    
    # Extract email addresses
    email_list = []
    if email_accounts and 'data' in email_accounts:
        email_list = [acc['email'] for acc in email_accounts['data'] if acc.get('email')]
    
    campaign_data = {
        "name": "AI Agents: Make Money & Save Money - Daily Outreach",
        "campaign_schedule": {
            "schedules": [
                {
                    "name": "Business Hours - Weekdays",
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
                    "name": "Weekend Outreach",
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
            "end_date": None
        },
        "sequences": [
            {
                "steps": [
                    {
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

Best regards,
[Your Name]

P.S. No obligation - just a quick chat to see if this makes sense for your business."""
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

Best,
[Your Name]"""
                            }
                        ],
                        "wait_time_hours": 0,
                        "wait_time_minutes": 0
                    },
                    {
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

Best,
[Your Name]"""
                            },
                            {
                                "subject": "Re: {{first_name}}, automate your way to higher profits",
                                "body": """{{first_name}},

I know you're busy, so I'll keep this brief.

Three ways AI agents help businesses like {{company_name}}:

1. **Make Money**: Automated outreach that generates qualified leads 24/7
2. **Save Money**: Replace repetitive manual tasks (data entry, follow-ups, scheduling)
3. **Scale Faster**: Do more with the same team size

Most businesses choose one focus area and see results within 30 days.

Which would be most valuable for {{company_name}} right now?

Let me know - happy to share specific examples.

Best,
[Your Name]"""
                            }
                        ],
                        "wait_time_hours": 48,
                        "wait_time_minutes": 0
                    },
                    {
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

Best regards,
[Your Name]

P.S. If timing isn't right now, feel free to reach out when it makes sense. This offer stands."""
                            },
                            {
                                "subject": "Re: {{first_name}}, automate your way to higher profits",
                                "body": """{{first_name}},

I'll make this my last email - I know your inbox is probably flooded.

One final thought: What if you could add $20K-$100K to your annual revenue OR save that much in costs with minimal effort?

That's what AI agents do for businesses like {{company_name}}.

If you're curious, I'm happy to show you how. If not, I completely understand.

Thanks for your time, and best of luck with everything!

[Your Name]

P.S. The offer stands whenever you're ready."""
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
        "email_gap": 5,  # 5 minutes between emails (natural pacing)
        "random_wait_max": 15,  # Random wait up to 15 minutes (appears more human)
        "stop_on_reply": True,  # Stop when lead replies
        "stop_on_auto_reply": True,  # Stop on auto-reply
        "link_tracking": True,  # Track link clicks
        "open_tracking": True,  # Track email opens
        "text_only": False,  # Send HTML emails
        "first_email_text_only": False,
        "prioritize_new_leads": True,  # Prioritize new leads
        "match_lead_esp": False,
        "stop_for_company": True,  # Stop for entire company when someone replies
        "insert_unsubscribe_header": True,
        "allow_risky_contacts": False,
        "disable_bounce_protect": False
    }
    
    response = requests.post(f"{BASE_URL}/campaigns", headers=HEADERS, json=campaign_data)
    
    if response.status_code in [200, 201]:
        campaign = response.json()
        print(f"✓ Campaign created successfully!")
        print(f"Campaign ID: {campaign.get('id')}")
        return campaign
    else:
        print(f"✗ Error creating campaign:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def bulk_add_leads(campaign_id, leads_file=None):
    """Add leads to campaign in bulk"""
    print(f"\nAdding leads to campaign...")
    
    # Example leads - replace with your actual lead list
    sample_leads = [
        {
            "email": "founder@techstartup.com",
            "first_name": "Sarah",
            "last_name": "Johnson",
            "company_name": "Tech Startup Inc",
            "personalization": "I saw your company is scaling fast and thought AI automation could help you grow even faster.",
            "campaign": campaign_id,
            "payload": {
                "industry": "Technology",
                "company_size": "50-100",
                "pain_point": "scaling"
            }
        },
        {
            "email": "ceo@marketingagency.com",
            "first_name": "Michael",
            "last_name": "Chen",
            "company_name": "Marketing Pro Agency",
            "personalization": "I noticed your agency handles multiple clients - AI agents could help you scale without hiring more people.",
            "campaign": campaign_id,
            "payload": {
                "industry": "Marketing",
                "company_size": "10-50",
                "pain_point": "client_management"
            }
        },
        {
            "email": "owner@ecommercebiz.com",
            "first_name": "Jessica",
            "last_name": "Martinez",
            "company_name": "E-commerce Solutions",
            "personalization": "Your e-commerce business could benefit from AI-powered customer engagement that works 24/7.",
            "campaign": campaign_id,
            "payload": {
                "industry": "E-commerce",
                "company_size": "25-50",
                "pain_point": "customer_service"
            }
        }
    ]
    
    added_count = 0
    failed_count = 0
    
    for lead in sample_leads:
        response = requests.post(f"{BASE_URL}/leads", headers=HEADERS, json=lead)
        if response.status_code in [200, 201]:
            print(f"✓ Added: {lead['email']}")
            added_count += 1
        else:
            print(f"✗ Failed: {lead['email']} - {response.text}")
            failed_count += 1
    
    print(f"\nLeads Summary: {added_count} added, {failed_count} failed")
    return added_count > 0

def activate_campaign(campaign_id):
    """Activate campaign to start sending"""
    print(f"\nActivating campaign {campaign_id}...")
    response = requests.post(f"{BASE_URL}/campaigns/{campaign_id}/activate", headers=HEADERS)
    
    if response.status_code in [200, 201]:
        print("✓ Campaign activated and sending!")
        return True
    else:
        print(f"✗ Error activating campaign: {response.text}")
        return False

def list_campaigns():
    """List all campaigns"""
    print("\nListing all campaigns...")
    response = requests.get(f"{BASE_URL}/campaigns", headers=HEADERS)
    
    if response.status_code == 200:
        campaigns = response.json()
        if 'data' in campaigns:
            print(f"Found {len(campaigns['data'])} campaign(s):")
            for camp in campaigns['data']:
                status_map = {0: "Draft", 1: "Active", 2: "Paused", 3: "Completed"}
                status = status_map.get(camp.get('status'), "Unknown")
                print(f"  - {camp.get('name')} (ID: {camp.get('id')}, Status: {status})")
        return campaigns
    else:
        print(f"Error: {response.text}")
        return None

def main():
    """Main execution"""
    print("=" * 70)
    print("AI AGENTS COLD EMAIL CAMPAIGN - INSTANTLY.AI SETUP")
    print("Help People & Businesses Make Money or Save Money with AI")
    print("=" * 70)
    
    # Step 1: Test authentication
    if not test_authentication():
        print("\n❌ Authentication failed. Please check your API key.")
        print("\nThe API key format should be: Bearer {your-api-key}")
        print("Make sure you've generated an API key from Instantly.ai dashboard.")
        return
    
    # Step 2: List existing campaigns
    list_campaigns()
    
    # Step 3: List email accounts
    email_accounts = list_email_accounts()
    if not email_accounts or not email_accounts.get('data'):
        print("\n⚠️  No email accounts found!")
        print("Please add email accounts in Instantly.ai dashboard before creating campaigns.")
        print("Go to: Instantly.ai > Settings > Email Accounts")
        # Continue anyway to create the campaign structure
    
    # Step 4: Create campaign
    campaign = create_ai_agent_campaign(email_accounts)
    if not campaign:
        print("\n❌ Failed to create campaign. Check error messages above.")
        return
    
    campaign_id = campaign.get('id')
    
    # Step 5: Add sample leads (optional)
    print("\n" + "=" * 70)
    add_leads = input("Would you like to add sample leads now? (yes/no): ").strip().lower()
    if add_leads in ['yes', 'y']:
        bulk_add_leads(campaign_id)
    
    # Step 6: Activate campaign (optional)
    print("\n" + "=" * 70)
    activate = input("Would you like to ACTIVATE the campaign now? (yes/no): ").strip().lower()
    if activate in ['yes', 'y']:
        activate_campaign(campaign_id)
    else:
        print("\n⚠️  Campaign created but NOT activated.")
        print("To activate later, run: activate_campaign('{campaign_id}')")
    
    # Summary
    print("\n" + "=" * 70)
    print("SETUP COMPLETE!")
    print("=" * 70)
    print(f"\n📧 Campaign: AI Agents - Make Money & Save Money")
    print(f"🆔 Campaign ID: {campaign_id}")
    print(f"📊 Daily Limit: 500 emails per account")
    print(f"🎯 Target: Help businesses make/save money with AI agents")
    print(f"\n📝 Next Steps:")
    print("1. Add your lead list (CSV import or API)")
    print("2. Customize email copy with your name/details")
    print("3. Activate campaign when ready")
    print("4. Monitor replies and analytics")
    print(f"\n💡 Campaign Dashboard: https://app.instantly.ai/app/campaigns/{campaign_id}")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()


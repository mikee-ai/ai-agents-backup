#!/usr/bin/env python3
"""
Update Campaign with 30 Total Steps
Original 3 steps + 27 additional steps
All with 1 minute delays
"""

import requests
import json

# API Configuration
API_KEY = "YjUzNzFjY2EtZGNiNC00OTIzLTgxZGYtZDg1Nzc3YzY5OTg3OlRvZHBXZm9Fb2xqUA=="
BASE_URL = "https://api.instantly.ai/api/v2"
CAMPAIGN_ID = "1dfdc50b-465a-4cea-8a33-d80ef0a3e010"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_email_step(step_num):
    """Create a single email step with variants"""
    
    variants = [
        {
            "subject": f"Re: Custom AI agents for {{{{company_name}}}}? (Follow-up {step_num})",
            "body": f"""<p>{{{{first_name}}}},</p>

<p>Still interested in learning about custom AI agent solutions for {{{{company_name}}}}?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
        },
        {
            "subject": f"Re: AI solutions for {{{{company_name}}}} (Follow-up {step_num})",
            "body": f"""<p>{{{{first_name}}}},</p>

<p>Would you like to explore how AI agents could help {{{{company_name}}}}?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
        },
        {
            "subject": f"Re: {{{{first_name}}}}, AI agents? (Follow-up {step_num})",
            "body": f"""<p>{{{{first_name}}}},</p>

<p>Any interest in custom AI solutions for your business?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
        }
    ]
    
    return {
        "type": "email",
        "variants": variants,
        "delay": 1
    }

def update_campaign_30_steps():
    """Update campaign with 30 total steps"""
    
    print("Creating 30-step email sequence...")
    
    # Create all 30 steps
    steps = []
    
    # Step 1: Initial outreach (3 variants)
    steps.append({
        "type": "email",
        "variants": [
            {
                "subject": "Custom AI agents for {{company_name}}?",
                "body": """<p>{{first_name}},</p>

<p>Interested in learning more about custom AI agents and solutions for {{company_name}}?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
            },
            {
                "subject": "{{first_name}}, AI solutions for your business?",
                "body": """<p>{{first_name}},</p>

<p>Would you be interested in exploring custom AI agent solutions for {{company_name}}?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
            },
            {
                "subject": "AI agents for {{company_name}}",
                "body": """<p>{{first_name}},</p>

<p>Want to learn how custom AI agents could help {{company_name}}?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
            }
        ],
        "delay": 1
    })
    
    # Steps 2-30: Follow-ups
    for i in range(2, 31):
        steps.append(create_email_step(i))
    
    update_data = {
        "sequences": [
            {
                "steps": steps
            }
        ]
    }
    
    response = requests.patch(
        f"{BASE_URL}/campaigns/{CAMPAIGN_ID}",
        headers=HEADERS,
        json=update_data
    )
    
    if response.status_code in [200, 201]:
        print("✓ Campaign updated with 30 steps!")
        print(f"\nTotal Steps: 30")
        print(f"Delay per step: 1 minute")
        print(f"Total sequence time: ~30 minutes")
        print(f"\nEach step has 3 email variants for A/B testing")
        print(f"Total unique emails: 90 variants")
        return True
    else:
        print(f"✗ Error: {response.text}")
        return False

def main():
    print("="*70)
    print("CREATING 30-STEP EMAIL SEQUENCE")
    print("="*70)
    print(f"\nCampaign ID: {CAMPAIGN_ID}")
    print("\nAdding:")
    print("  • Original 3 steps")
    print("  • Plus 27 additional follow-up steps")
    print("  • Total: 30 steps")
    print("  • Each step: 1 minute delay")
    print("  • 3 variants per step")
    print("\n" + "="*70 + "\n")
    
    if update_campaign_30_steps():
        print("\n✓ SUCCESS!")
        print(f"\nView campaign:")
        print(f"https://app.instantly.ai/app/campaigns/{CAMPAIGN_ID}/sequences")
        print("\n⚠️  All 30 emails will send within ~30 minutes!")
        print("\n" + "="*70)
    else:
        print("\n✗ Update failed.")

if __name__ == "__main__":
    main()


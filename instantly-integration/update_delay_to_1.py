#!/usr/bin/env python3
"""
Update Campaign Delays to 1 Minute
All steps will have 1 minute delay
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

def update_delays():
    """Update all step delays to 1 minute"""
    
    print("Updating all delays to 1 minute...")
    
    # All steps with 1 minute delay
    update_data = {
        "sequences": [
            {
                "steps": [
                    {
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
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Custom AI agents for {{company_name}}?",
                                "body": """<p>{{first_name}},</p>

<p>Following up - interested in learning more about AI agent solutions?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
                            },
                            {
                                "subject": "Re: {{first_name}}, AI solutions for your business?",
                                "body": """<p>{{first_name}},</p>

<p>Still interested in exploring custom AI agents for {{company_name}}?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
                            },
                            {
                                "subject": "Re: AI agents for {{company_name}}",
                                "body": """<p>{{first_name}},</p>

<p>Quick follow-up - would you like to learn more about AI solutions for your business?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
                            }
                        ],
                        "delay": 1
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Custom AI agents for {{company_name}}?",
                                "body": """<p>{{first_name}},</p>

<p>Last follow-up - any interest in custom AI agent solutions?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
                            },
                            {
                                "subject": "Re: {{first_name}}, AI solutions for your business?",
                                "body": """<p>{{first_name}},</p>

<p>Final email - let me know if you'd like to explore AI agents for {{company_name}}.</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
                            },
                            {
                                "subject": "Re: AI agents for {{company_name}}",
                                "body": """<p>{{first_name}},</p>

<p>Last note - interested in learning about custom AI solutions?</p>

<p>Best,<br>
Mikee Shattuck<br>
Founder, Mikee.ai</p>"""
                            }
                        ],
                        "delay": 1
                    }
                ]
            }
        ]
    }
    
    response = requests.patch(
        f"{BASE_URL}/campaigns/{CAMPAIGN_ID}",
        headers=HEADERS,
        json=update_data
    )
    
    if response.status_code in [200, 201]:
        print("✓ All delays updated to 1 minute!")
        print("\nDelay Settings:")
        print("  Step 1: 1 minute")
        print("  Step 2: 1 minute")
        print("  Step 3: 1 minute")
        print("\n⚠️  WARNING: All 3 emails will send within ~3 minutes!")
        return True
    else:
        print(f"✗ Error: {response.text}")
        return False

def main():
    print("="*70)
    print("UPDATING DELAYS TO 1 MINUTE")
    print("="*70)
    print(f"\nCampaign ID: {CAMPAIGN_ID}")
    print("\n⚠️  WARNING: This will send all follow-ups within minutes!")
    print("="*70 + "\n")
    
    if update_delays():
        print("\n✓ SUCCESS!")
        print(f"\nView campaign:")
        print(f"https://app.instantly.ai/app/campaigns/{CAMPAIGN_ID}/sequences")
        print("\n" + "="*70)
    else:
        print("\n✗ Update failed.")

if __name__ == "__main__":
    main()


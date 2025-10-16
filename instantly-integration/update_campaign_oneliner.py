#!/usr/bin/env python3
"""
One-Liner Cold Email Campaign
Ultra-short, direct emails about custom AI agents
Signature: Mikee Shattuck, Founder of Mikee.ai
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

def update_campaign_oneliner():
    """Update campaign with one-liner emails"""
    
    print("Updating campaign with one-liner cold emails...")
    
    # One-liner email sequences - 1 day (1440 min) delays
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
                        "delay": 0
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
                        "delay": 1440  # 1 day
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
                        "delay": 1440  # 1 day
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
        print("✓ Campaign updated successfully!")
        print("\nNew Email Style:")
        print("  ✓ Ultra-short one-liners")
        print("  ✓ Direct question format")
        print("  ✓ Focus on interest in learning more")
        print("  ✓ Signature: Mikee Shattuck, Founder, Mikee.ai")
        print("  ✓ 3 variants per step for A/B testing")
        print("  ✓ 1-day delays between steps")
        return True
    else:
        print(f"✗ Error: {response.text}")
        return False

def main():
    print("="*70)
    print("UPDATING TO ONE-LINER COLD EMAILS")
    print("="*70)
    print(f"\nCampaign ID: {CAMPAIGN_ID}")
    print("\nNew approach:")
    print("  • One-liner emails only")
    print("  • Focus on interest in learning more")
    print("  • Custom AI agents and solutions")
    print("  • Signature: Mikee Shattuck, Founder, Mikee.ai")
    print("  • 1-day delays between steps")
    print("\n" + "="*70 + "\n")
    
    if update_campaign_oneliner():
        print("\n✓ SUCCESS!")
        print(f"\nView updated campaign:")
        print(f"https://app.instantly.ai/app/campaigns/{CAMPAIGN_ID}/sequences")
        print("\n" + "="*70)
    else:
        print("\n✗ Update failed. Check error above.")

if __name__ == "__main__":
    main()


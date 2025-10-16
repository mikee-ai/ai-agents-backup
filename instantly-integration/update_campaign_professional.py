#!/usr/bin/env python3
"""
Update Instantly.ai Campaign with Professional Cold Email Copy
1-day delays between steps, punchy professional writing
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

def update_campaign_sequences():
    """Update campaign with professional cold email copy"""
    
    print("Updating campaign with professional cold email sequences...")
    
    # Professional, punchy cold email sequences with 1-day (1440 min) delays
    update_data = {
        "sequences": [
            {
                "steps": [
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Quick question, {{first_name}}",
                                "body": """{{first_name}},

I help companies like {{company_name}} automate their way to an extra $10K-$50K/month.

Most of our clients either:
• Generate more revenue (automated sales & lead gen)
• Cut costs by 30-40% (replace manual work)
• Both

{{personalization}}

Worth a 15-minute conversation?

Best,
[Your Name]"""
                            },
                            {
                                "subject": "{{company_name}} + AI agents?",
                                "body": """{{first_name}},

What if you could free up 20+ hours/week for your team while increasing revenue?

That's exactly what we do with AI agents for companies like {{company_name}}.

{{personalization}}

Real results:
✓ 3x more qualified leads
✓ 40% lower operational costs
✓ Teams focus on high-value work

Quick call this week?

[Your Name]"""
                            }
                        ],
                        "delay": 0
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Quick question, {{first_name}}",
                                "body": """{{first_name}},

Following up on my email about AI automation for {{company_name}}.

Quick case study: A client in your space automated their follow-up process.

Results in 30 days:
• 35% higher conversion rate
• $25K/month saved in labor
• 2-week setup time

Want to see how this works for {{company_name}}?

[Your Name]"""
                            },
                            {
                                "subject": "Re: {{company_name}} + AI agents?",
                                "body": """{{first_name}},

I know you're busy, so I'll be brief.

Most businesses choose one of three paths with AI agents:

1. Make money (automated outreach, 24/7 lead gen)
2. Save money (cut manual tasks, reduce overhead)
3. Both (most common outcome)

Which matters most to {{company_name}} right now?

Happy to share specific examples.

[Your Name]"""
                            }
                        ],
                        "delay": 1440  # 1 day = 1440 minutes
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Quick question, {{first_name}}",
                                "body": """{{first_name}},

Last email from me - promise!

I genuinely think AI agents could add $20K-$100K to {{company_name}}'s bottom line this year.

If you're curious, I'm here. If not, no worries.

Either way, wishing you success.

[Your Name]

P.S. Offer stands whenever timing is right."""
                            },
                            {
                                "subject": "Re: {{company_name}} + AI agents?",
                                "body": """{{first_name}},

Final follow-up.

One question: What would an extra $50K in annual revenue OR savings mean for {{company_name}}?

That's the typical impact we deliver with AI agents.

If you want to explore this, let me know. If not, I completely understand.

Thanks for your time.

[Your Name]"""
                            }
                        ],
                        "delay": 1440  # 1 day = 1440 minutes
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
        print("\nUpdated Sequence:")
        print("  Step 1: Initial outreach (2 variants)")
        print("  Step 2: Follow-up after 1 day (2 variants)")
        print("  Step 3: Final follow-up after 1 day (2 variants)")
        print("\nEmail Style: Professional, punchy, benefit-focused")
        return True
    else:
        print(f"✗ Error: {response.text}")
        return False

def main():
    print("="*70)
    print("UPDATING CAMPAIGN WITH PROFESSIONAL COLD EMAIL COPY")
    print("="*70)
    print(f"\nCampaign ID: {CAMPAIGN_ID}")
    print("Changes:")
    print("  ✓ Professional, punchy writing style")
    print("  ✓ 1-day delays between steps (instead of 2-3 days)")
    print("  ✓ Benefit-focused, ROI-driven messaging")
    print("  ✓ Multiple subject line variants for A/B testing")
    print("\n" + "="*70)
    
    if update_campaign_sequences():
        print("\n✓ SUCCESS!")
        print(f"\nView updated campaign:")
        print(f"https://app.instantly.ai/app/campaigns/{CAMPAIGN_ID}/sequences")
        print("\n" + "="*70)
    else:
        print("\n✗ Update failed. Check error above.")

if __name__ == "__main__":
    main()


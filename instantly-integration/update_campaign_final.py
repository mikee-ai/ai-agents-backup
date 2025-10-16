#!/usr/bin/env python3
"""
Final Campaign Update: Value-focused, simple CTA
Focus: AI agents save time and money
CTA: Reply YES to learn more
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

def update_campaign_final():
    """Update campaign with value-focused copy and simple YES CTA"""
    
    print("Updating campaign with simplified, value-focused copy...")
    
    # Simplified, value-focused email sequences
    update_data = {
        "sequences": [
            {
                "steps": [
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Save time & money with AI agents",
                                "body": """<p>{{first_name}},</p>

<p>AI agents can help {{company_name}} save 20+ hours per week and reduce costs by 30-40%.</p>

<p><strong>What AI agents do:</strong></p>
<ul>
<li>Automate repetitive tasks</li>
<li>Handle customer follow-ups 24/7</li>
<li>Generate and qualify leads automatically</li>
<li>Free up your team for high-value work</li>
</ul>

<p>{{personalization}}</p>

<p><strong>Reply YES to learn more.</strong></p>

<p>Best,<br>
[Your Name]</p>"""
                            },
                            {
                                "subject": "{{first_name}}, automate {{company_name}} with AI",
                                "body": """<p>{{first_name}},</p>

<p>What if {{company_name}} could operate 24/7 without hiring more people?</p>

<p><strong>AI agents deliver:</strong></p>
<ul>
<li>30-40% cost reduction</li>
<li>3x more qualified leads</li>
<li>20+ hours saved per week</li>
<li>Faster response times</li>
</ul>

<p>{{personalization}}</p>

<p><strong>Reply YES to learn more.</strong></p>

<p>[Your Name]</p>"""
                            }
                        ],
                        "delay": 0
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Save time & money with AI agents",
                                "body": """<p>{{first_name}},</p>

<p>Following up on AI agents for {{company_name}}.</p>

<p><strong>Quick example:</strong> A company in your industry automated their customer follow-up process.</p>

<p><strong>Results in 30 days:</strong></p>
<ul>
<li>35% increase in conversions</li>
<li>$25K saved per month</li>
<li>Setup took less than 2 weeks</li>
</ul>

<p><strong>Reply YES to learn more.</strong></p>

<p>[Your Name]</p>"""
                            },
                            {
                                "subject": "Re: {{first_name}}, automate {{company_name}} with AI",
                                "body": """<p>{{first_name}},</p>

<p>Most businesses use AI agents for one of three goals:</p>

<ol>
<li><strong>Save time</strong> - Automate repetitive work</li>
<li><strong>Save money</strong> - Reduce labor costs by 30-40%</li>
<li><strong>Make money</strong> - Generate leads 24/7</li>
</ol>

<p>Which matters most to {{company_name}} right now?</p>

<p><strong>Reply YES to learn more.</strong></p>

<p>[Your Name]</p>"""
                            }
                        ],
                        "delay": 1440  # 1 day
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Save time & money with AI agents",
                                "body": """<p>{{first_name}},</p>

<p>Last email - I don't want to be a pest.</p>

<p>AI agents could save {{company_name}} $20K-$100K annually while freeing up your team to focus on growth.</p>

<p>If you're interested, I'm here to help.</p>

<p><strong>Reply YES to learn more.</strong></p>

<p>Best,<br>
[Your Name]</p>

<p><em>P.S. This offer stands whenever timing is right for you.</em></p>"""
                            },
                            {
                                "subject": "Re: {{first_name}}, automate {{company_name}} with AI",
                                "body": """<p>{{first_name}},</p>

<p>Final follow-up.</p>

<p>One question: What would saving 20+ hours per week OR $50K annually mean for {{company_name}}?</p>

<p>That's what AI agents typically deliver.</p>

<p><strong>Reply YES to learn more.</strong></p>

<p>Thanks for your time.</p>

<p>[Your Name]</p>"""
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
        print("\nKey Changes:")
        print("  ✓ Removed 'I help companies' language")
        print("  ✓ Pure focus on AI agent value (time & money)")
        print("  ✓ Simple CTA: 'Reply YES to learn more'")
        print("  ✓ Clean HTML formatting maintained")
        print("\nAll emails now focus on the core value proposition.")
        return True
    else:
        print(f"✗ Error: {response.text}")
        return False

def main():
    print("="*70)
    print("FINAL CAMPAIGN UPDATE - VALUE-FOCUSED COPY")
    print("="*70)
    print(f"\nCampaign ID: {CAMPAIGN_ID}")
    print("\nUpdating to:")
    print("  • Focus on AI agents saving time & money")
    print("  • Remove 'I help companies' language")
    print("  • Simple CTA: Reply YES to learn more")
    print("\n" + "="*70 + "\n")
    
    if update_campaign_final():
        print("\n✓ SUCCESS!")
        print(f"\nView updated campaign:")
        print(f"https://app.instantly.ai/app/campaigns/{CAMPAIGN_ID}/sequences")
        print("\n" + "="*70)
    else:
        print("\n✗ Update failed. Check error above.")

if __name__ == "__main__":
    main()


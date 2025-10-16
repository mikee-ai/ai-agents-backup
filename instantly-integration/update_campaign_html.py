#!/usr/bin/env python3
"""
Update Instantly.ai Campaign with HTML-formatted emails
Clean spacing and professional formatting
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

def update_campaign_with_html():
    """Update campaign with HTML-formatted emails"""
    
    print("Updating campaign with HTML-formatted emails...")
    
    # HTML-formatted email sequences
    update_data = {
        "sequences": [
            {
                "steps": [
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Quick question, {{first_name}}",
                                "body": """<p>{{first_name}},</p>

<p>I help companies like {{company_name}} automate their way to an extra $10K-$50K/month.</p>

<p>Most of our clients either:</p>
<ul>
<li>Generate more revenue (automated sales & lead gen)</li>
<li>Cut costs by 30-40% (replace manual work)</li>
<li>Both</li>
</ul>

<p>{{personalization}}</p>

<p>Worth a 15-minute conversation?</p>

<p>Best,<br>
[Your Name]</p>"""
                            },
                            {
                                "subject": "{{company_name}} + AI agents?",
                                "body": """<p>{{first_name}},</p>

<p>What if you could free up 20+ hours/week for your team while increasing revenue?</p>

<p>That's exactly what we do with AI agents for companies like {{company_name}}.</p>

<p>{{personalization}}</p>

<p>Real results:</p>
<ul>
<li>3x more qualified leads</li>
<li>40% lower operational costs</li>
<li>Teams focus on high-value work</li>
</ul>

<p>Quick call this week?</p>

<p>[Your Name]</p>"""
                            }
                        ],
                        "delay": 0
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Quick question, {{first_name}}",
                                "body": """<p>{{first_name}},</p>

<p>Following up on my email about AI automation for {{company_name}}.</p>

<p>Quick case study: A client in your space automated their follow-up process.</p>

<p><strong>Results in 30 days:</strong></p>
<ul>
<li>35% higher conversion rate</li>
<li>$25K/month saved in labor</li>
<li>2-week setup time</li>
</ul>

<p>Want to see how this works for {{company_name}}?</p>

<p>[Your Name]</p>"""
                            },
                            {
                                "subject": "Re: {{company_name}} + AI agents?",
                                "body": """<p>{{first_name}},</p>

<p>I know you're busy, so I'll be brief.</p>

<p>Most businesses choose one of three paths with AI agents:</p>

<ol>
<li><strong>Make money</strong> (automated outreach, 24/7 lead gen)</li>
<li><strong>Save money</strong> (cut manual tasks, reduce overhead)</li>
<li><strong>Both</strong> (most common outcome)</li>
</ol>

<p>Which matters most to {{company_name}} right now?</p>

<p>Happy to share specific examples.</p>

<p>[Your Name]</p>"""
                            }
                        ],
                        "delay": 1440  # 1 day
                    },
                    {
                        "type": "email",
                        "variants": [
                            {
                                "subject": "Re: Quick question, {{first_name}}",
                                "body": """<p>{{first_name}},</p>

<p>Last email from me - promise!</p>

<p>I genuinely think AI agents could add $20K-$100K to {{company_name}}'s bottom line this year.</p>

<p>If you're curious, I'm here. If not, no worries.</p>

<p>Either way, wishing you success.</p>

<p>[Your Name]</p>

<p><em>P.S. Offer stands whenever timing is right.</em></p>"""
                            },
                            {
                                "subject": "Re: {{company_name}} + AI agents?",
                                "body": """<p>{{first_name}},</p>

<p>Final follow-up.</p>

<p>One question: What would an extra $50K in annual revenue OR savings mean for {{company_name}}?</p>

<p>That's the typical impact we deliver with AI agents.</p>

<p>If you want to explore this, let me know. If not, I completely understand.</p>

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
        print("✓ Campaign updated with HTML formatting!")
        print("\nFormatting Applied:")
        print("  ✓ Proper paragraph spacing (<p> tags)")
        print("  ✓ Bullet points for lists (<ul>, <li>)")
        print("  ✓ Numbered lists (<ol>)")
        print("  ✓ Bold text for emphasis (<strong>)")
        print("  ✓ Line breaks (<br>)")
        print("\nEmails will now display with clean spacing and structure.")
        return True
    else:
        print(f"✗ Error: {response.text}")
        return False

def main():
    print("="*70)
    print("UPDATING CAMPAIGN WITH HTML FORMATTING")
    print("="*70)
    print(f"\nCampaign ID: {CAMPAIGN_ID}")
    print("\nAdding HTML markup for better readability...")
    print("="*70 + "\n")
    
    if update_campaign_with_html():
        print("\n✓ SUCCESS!")
        print(f"\nView updated campaign:")
        print(f"https://app.instantly.ai/app/campaigns/{CAMPAIGN_ID}/sequences")
        print("\n" + "="*70)
    else:
        print("\n✗ Update failed. Check error above.")

if __name__ == "__main__":
    main()


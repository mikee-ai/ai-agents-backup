# Instantly.ai Cold Email Campaign Setup Guide

## AI Agents Campaign: Help Businesses Make Money & Save Money

This comprehensive guide will help you set up an automated cold email campaign using Instantly.ai to promote AI agents that help businesses increase revenue or reduce costs.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [API Key Issue & Resolution](#api-key-issue--resolution)
3. [Campaign Overview](#campaign-overview)
4. [Setup Instructions](#setup-instructions)
5. [Campaign Configuration](#campaign-configuration)
6. [Lead Management](#lead-management)
7. [Monitoring & Analytics](#monitoring--analytics)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Items

1. **Instantly.ai Account** with **Hypergrowth Plan** or above (API access required)
2. **Valid API Key** generated from Instantly.ai dashboard
3. **Email Accounts** connected to Instantly.ai for sending
4. **Lead List** with contact information (email, name, company)
5. **Python 3.11+** installed (for automation scripts)

### Account Setup

1. Log into [Instantly.ai](https://app.instantly.ai)
2. Navigate to **Settings** > **Integrations** > **API Keys**
3. Click **"Create API Key"**
4. Select appropriate scopes (campaigns, leads, accounts, analytics)
5. Copy and securely store your API key

---

## API Key Issue & Resolution

### Current Status

The provided API key (`YjUzNzFjY2EtZGNiNC00OTIzLTgxZGYtZDg1Nzc3YzY5OTg3OmZ2VW9BcVlFWHBERQ==`) is **not authenticating** with the Instantly.ai API.

**Error received:** `ERR_AUTH_FAILED` (API v1) and `500 Internal Server Error` (API v2)

### Possible Causes

1. **API key is invalid or expired**
2. **Account doesn't have API access** (requires Hypergrowth plan or above)
3. **Workspace is suspended or inactive**
4. **API key format is incorrect** (may be from a different service)
5. **API key needs to be regenerated**

### Resolution Steps

#### Option 1: Generate New API Key (Recommended)

1. Log into Instantly.ai dashboard
2. Go to **Settings** > **Integrations** > **API Keys**
3. Delete old API key if it exists
4. Click **"Create API Key"**
5. Name it: "Cold Email Campaign API"
6. Select scopes:
   - ✅ campaigns:read
   - ✅ campaigns:write
   - ✅ campaigns:all
   - ✅ leads:read
   - ✅ leads:write
   - ✅ accounts:read
   - ✅ analytics:read
7. Click **"Create"**
8. **Copy the key immediately** (it's only shown once)
9. Update the API key in the Python scripts

#### Option 2: Verify Account Status

1. Check that your Instantly.ai subscription is **Hypergrowth** or above
2. Verify workspace is active (not suspended)
3. Ensure billing is current
4. Contact Instantly.ai support if needed

#### Option 3: Use Instantly.ai Dashboard (Manual Setup)

If API continues to fail, you can set up the campaign manually:

1. Use the dashboard to create campaigns
2. Import leads via CSV
3. Configure schedules and settings
4. Monitor through the web interface

---

## Campaign Overview

### Campaign Goal

**Help businesses and individuals use AI agents to make money, save money, or improve operations**

### Value Proposition

- **Make Money**: Automated sales, lead generation, customer engagement 24/7
- **Save Money**: Replace manual tasks, reduce overhead costs by 30-40%
- **Scale Faster**: Do more with existing team size

### Target Audience

- Small to medium business owners
- Startup founders
- Marketing agencies
- E-commerce businesses
- SaaS companies
- Professional services firms

### Campaign Metrics (Maximum Settings)

| Setting | Value | Description |
|---------|-------|-------------|
| Daily Email Limit | 500 per account | Maximum emails sent daily per email account |
| Daily Max Leads | 500 | Maximum new leads contacted per day |
| Email Gap | 5 minutes | Time between sending emails |
| Random Wait | 0-15 minutes | Random delay to appear more human |
| Sending Schedule | 8 AM - 6 PM Weekdays<br>9 AM - 5 PM Weekends | Business hours across 7 days |
| Follow-up Sequence | 3 emails | Initial + 2 follow-ups (48hr, 72hr gaps) |

---

## Setup Instructions

### Step 1: Prepare Your Environment

```bash
# Install required Python packages
pip3 install requests

# Download the setup scripts
# (Scripts are provided in this package)
```

### Step 2: Update API Key

Edit the Python scripts and replace the API key:

```python
# In instantly_ai_agent_campaign.py
API_KEY = "YOUR_NEW_API_KEY_HERE"
```

### Step 3: Add Email Accounts

Before creating campaigns, add email accounts in Instantly.ai:

1. Go to **Settings** > **Email Accounts**
2. Click **"Add Account"**
3. Connect your email (Gmail, Outlook, SMTP)
4. Enable **Warmup** for new accounts
5. Verify account is healthy (green status)

**Recommended:** Use 3-5 email accounts for better deliverability and higher volume

### Step 4: Prepare Lead List

Create a CSV file with your leads:

```csv
email,first_name,last_name,company_name,personalization
john@techco.com,John,Smith,TechCo Inc,"I saw your company is scaling fast"
sarah@agency.com,Sarah,Johnson,Marketing Agency,"Your agency handles multiple clients"
```

**Lead Sources:**
- LinkedIn Sales Navigator
- Apollo.io
- Hunter.io
- ZoomInfo
- Your existing CRM

### Step 5: Run the Campaign Setup Script

```bash
python3 instantly_ai_agent_campaign.py
```

Follow the prompts to:
1. Test authentication
2. Create campaign
3. Add leads
4. Activate campaign

---

## Campaign Configuration

### Email Sequence

#### Email 1: Initial Outreach (Variant A)

**Subject:** Save 20+ hours/week with AI agents at {{company_name}}

**Body:**
```
Hi {{first_name}},

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

P.S. No obligation - just a quick chat to see if this makes sense for your business.
```

#### Email 1: Initial Outreach (Variant B)

**Subject:** {{first_name}}, automate your way to higher profits

**Body:**
```
Hi {{first_name}},

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
[Your Name]
```

#### Email 2: Follow-up (48 hours later)

**Subject:** Re: Save 20+ hours/week with AI agents at {{company_name}}

**Body:**
```
Hi {{first_name}},

Just following up on my previous email about AI agents.

I wanted to share a quick case study: One of our clients in your industry automated their customer follow-up process and saw:
• 35% increase in conversion rates
• $25K saved per month in labor costs
• Sales team could focus on closing deals instead of admin work

The setup took less than 2 weeks.

Would you like to see how we could create something similar for {{company_name}}?

Happy to jump on a quick call this week.

Best,
[Your Name]
```

#### Email 3: Final Follow-up (72 hours later)

**Subject:** Re: Save 20+ hours/week with AI agents at {{company_name}}

**Body:**
```
Hi {{first_name}},

Last follow-up from me - I don't want to be a pest!

I genuinely believe AI agents could help {{company_name}} either:
• Increase revenue through automation
• Reduce costs significantly
• Both

If you're interested, I'm here to help. If not, no worries at all.

Either way, I wish you and {{company_name}} continued success.

Best regards,
[Your Name]

P.S. If timing isn't right now, feel free to reach out when it makes sense. This offer stands.
```

### Campaign Settings Explained

| Setting | Value | Why It Matters |
|---------|-------|----------------|
| **stop_on_reply** | True | Stops emailing when lead responds (prevents spam) |
| **stop_on_auto_reply** | True | Stops on out-of-office messages |
| **stop_for_company** | True | Stops emailing entire company domain when one person replies |
| **link_tracking** | True | Track which links leads click |
| **open_tracking** | True | See who opens your emails |
| **prioritize_new_leads** | True | Contact new leads before retrying old ones |
| **insert_unsubscribe_header** | True | Compliance with email regulations |
| **allow_risky_contacts** | False | Avoid bounces and protect sender reputation |

---

## Lead Management

### Adding Leads via API

```python
import requests

API_KEY = "your-api-key"
CAMPAIGN_ID = "your-campaign-id"

lead_data = {
    "email": "prospect@company.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "company_name": "Example Corp",
    "personalization": "I noticed your recent growth in the tech sector",
    "campaign": CAMPAIGN_ID,
    "payload": {
        "industry": "Technology",
        "company_size": "50-100",
        "pain_point": "scaling"
    }
}

response = requests.post(
    "https://api.instantly.ai/api/v2/leads",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json=lead_data
)

print(response.json())
```

### Bulk Import via CSV

Use the provided `bulk_lead_import.py` script:

```bash
python3 bulk_lead_import.py --campaign-id YOUR_CAMPAIGN_ID --csv leads.csv
```

### Lead Syncing

The campaign automatically syncs leads and tracks:
- Email opens
- Link clicks
- Replies
- Bounces
- Unsubscribes
- Interest status

---

## Monitoring & Analytics

### Key Metrics to Track

1. **Delivery Rate** - % of emails successfully delivered
2. **Open Rate** - % of emails opened (target: 30-50%)
3. **Reply Rate** - % of leads that respond (target: 5-15%)
4. **Click Rate** - % of leads that click links (target: 10-20%)
5. **Bounce Rate** - % of emails that bounce (keep below 2%)
6. **Unsubscribe Rate** - % that opt out (keep below 0.5%)

### Getting Analytics via API

```python
import requests

response = requests.get(
    f"https://api.instantly.ai/api/v2/campaigns/analytics",
    headers={"Authorization": f"Bearer {API_KEY}"},
    params={"campaign_id": CAMPAIGN_ID}
)

analytics = response.json()
print(analytics)
```

### Dashboard Access

View real-time analytics at:
```
https://app.instantly.ai/app/campaigns/{CAMPAIGN_ID}
```

---

## Troubleshooting

### Issue: API Authentication Fails

**Solution:**
1. Regenerate API key from dashboard
2. Verify account has Hypergrowth plan or above
3. Check workspace is active
4. Ensure API key has correct scopes

### Issue: No Email Accounts Available

**Solution:**
1. Add email accounts in Settings > Email Accounts
2. Complete email verification
3. Enable warmup for new accounts
4. Wait for accounts to show "healthy" status

### Issue: Emails Not Sending

**Possible Causes:**
- Campaign not activated
- No leads in campaign
- Email accounts not healthy
- Daily limit reached
- Outside sending schedule hours

**Solution:**
1. Check campaign status (should be "Active")
2. Verify leads are added
3. Check email account health
4. Review daily limits and schedule

### Issue: Low Open Rates

**Solutions:**
- Improve subject lines (test A/B variants)
- Send during business hours
- Warm up email accounts properly
- Clean your lead list (remove invalid emails)
- Personalize more effectively

### Issue: High Bounce Rate

**Solutions:**
- Verify emails before sending (use Email Verification API)
- Clean your lead list
- Remove catch-all and risky emails
- Use fresh, high-quality lead sources

---

## Next Steps

### Once API Key is Working:

1. ✅ Run `instantly_ai_agent_campaign.py` to create campaign
2. ✅ Import your lead list (CSV or API)
3. ✅ Customize email copy with your details
4. ✅ Test with small batch (10-20 leads) first
5. ✅ Monitor results for 3-5 days
6. ✅ Optimize based on metrics
7. ✅ Scale up to full volume

### Optimization Tips:

- **A/B test subject lines** - Try 2-3 variants
- **Personalize heavily** - Reference specific company details
- **Follow up consistently** - 2-3 follow-ups increase response by 50%
- **Track what works** - Double down on high-performing copy
- **Clean your list** - Remove bounces and unsubscribes weekly

### Scaling Strategy:

**Week 1:** 50-100 leads/day (testing phase)  
**Week 2:** 200-300 leads/day (if metrics are good)  
**Week 3:** 500+ leads/day (full scale)

---

## Support & Resources

### Instantly.ai Resources

- **Documentation:** https://developer.instantly.ai/
- **Help Center:** https://help.instantly.ai/
- **API v2 Docs:** https://developer.instantly.ai/api/v2/
- **Community:** Instantly.ai Facebook Group

### Getting Help

1. **API Issues:** Contact Instantly.ai support via dashboard
2. **Script Issues:** Review error messages and logs
3. **Strategy Questions:** Join cold email communities
4. **Technical Support:** Instantly.ai support team

---

## Files Included

1. `instantly_ai_agent_campaign.py` - Main campaign setup script
2. `bulk_lead_import.py` - Bulk lead import utility
3. `test_instantly_auth.py` - API authentication diagnostics
4. `INSTANTLY_AI_SETUP_GUIDE.md` - This comprehensive guide
5. `leads_template.csv` - Sample lead list template

---

## Legal & Compliance

### Important Notes:

- ✅ Only email people who fit your ICP (Ideal Customer Profile)
- ✅ Include unsubscribe option in all emails
- ✅ Honor opt-out requests immediately
- ✅ Comply with CAN-SPAM, GDPR, and local laws
- ✅ Don't buy email lists (use opt-in or B2B sources)
- ✅ Respect "do not contact" requests

### Best Practices:

- Provide value in every email
- Be transparent about who you are
- Make it easy to unsubscribe
- Respond to replies promptly
- Keep your promises

---

## Conclusion

This setup provides a complete cold email campaign system to help you promote AI agents that make or save money for businesses. Once the API key issue is resolved, you'll be able to:

- Send up to 500 emails per day per account
- Automatically follow up with prospects
- Track opens, clicks, and replies
- Sync leads and manage campaigns programmatically
- Scale your outreach efficiently

**Remember:** The key to success is not just volume, but **relevance and value**. Focus on helping businesses solve real problems with AI agents, and the results will follow.

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Status:** Ready to deploy once API key is resolved


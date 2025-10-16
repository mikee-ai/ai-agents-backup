#!/usr/bin/env python3
"""
Inframail Email Account Setup Script
Automatically creates email accounts for cold email campaigns
"""

import requests
import json
import time
from datetime import datetime

# Configuration
INFRAMAIL_API_KEY = "inf_5773448b8c7d5625ae4ab7d4b3227f6d3a147c4a3e8d154d481f51d1a8b4ac"  # From your screenshot
INFRAMAIL_BASE_URL = "https://app.inframail.io/api/v1"

# How many email accounts to create
NUM_ACCOUNTS = 5  # For 2,000 emails/day (400 per account)

# Email account settings
ACCOUNT_PREFIX = "outreach"  # Will create: outreach1@, outreach2@, etc.

class InframailClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = INFRAMAIL_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_email_account(self, email_address, display_name="AI Agents Outreach"):
        """Create a new email account in Inframail"""
        endpoint = f"{self.base_url}/host/agents/email"
        
        payload = {
            "emailAddress": email_address,
            "displayName": display_name,
            "enableWarmup": True,  # Automatically start warmup
            "warmupSettings": {
                "dailyLimit": 50,  # Start slow
                "increasePerDay": 10  # Gradually increase
            }
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating account {email_address}: {e}")
            if hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text}")
            return None
    
    def get_email_accounts(self):
        """Get list of all email accounts"""
        endpoint = f"{self.base_url}/host/agents/email"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting accounts: {e}")
            return None
    
    def get_available_domains(self):
        """Get list of available domains"""
        endpoint = f"{self.base_url}/host/agents/email/domains"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting domains: {e}")
            return None


def main():
    print("=" * 70)
    print("🚀 INFRAMAIL EMAIL ACCOUNT SETUP")
    print("=" * 70)
    print()
    
    # Initialize client
    client = InframailClient(INFRAMAIL_API_KEY)
    
    # Step 1: Get available domains
    print("📋 Step 1: Checking available domains...")
    domains = client.get_available_domains()
    
    if not domains:
        print("❌ Could not retrieve domains. Check your API key.")
        print()
        print("💡 Alternative: Create accounts manually in Inframail dashboard")
        print("   https://app.inframail.io/dashboard")
        return
    
    print(f"✓ Found {len(domains) if isinstance(domains, list) else 'some'} available domains")
    print()
    
    # Step 2: Get existing accounts
    print("📋 Step 2: Checking existing email accounts...")
    existing_accounts = client.get_email_accounts()
    
    if existing_accounts:
        if isinstance(existing_accounts, list):
            print(f"✓ You have {len(existing_accounts)} existing email accounts")
            for acc in existing_accounts[:5]:  # Show first 5
                email = acc.get('emailAddress', acc.get('email', 'Unknown'))
                print(f"   • {email}")
            if len(existing_accounts) > 5:
                print(f"   ... and {len(existing_accounts) - 5} more")
        else:
            print("✓ Existing accounts retrieved")
    print()
    
    # Step 3: Create new accounts
    print(f"📋 Step 3: Creating {NUM_ACCOUNTS} new email accounts...")
    print()
    
    created_accounts = []
    
    for i in range(1, NUM_ACCOUNTS + 1):
        # Note: You'll need to use your actual Inframail domain
        # This is a placeholder - update with your real domain from Inframail
        email_address = f"{ACCOUNT_PREFIX}{i}@yourdomain.com"
        
        print(f"[{i}/{NUM_ACCOUNTS}] Creating {email_address}...")
        
        result = client.create_email_account(email_address)
        
        if result:
            print(f"   ✓ Created successfully")
            created_accounts.append({
                'email': email_address,
                'password': result.get('password', 'Check Inframail dashboard'),
                'created_at': datetime.now().isoformat()
            })
        else:
            print(f"   ✗ Failed to create")
        
        # Rate limiting
        if i < NUM_ACCOUNTS:
            time.sleep(2)  # Wait 2 seconds between creations
        
        print()
    
    # Step 4: Summary
    print("=" * 70)
    print("📊 SETUP SUMMARY")
    print("=" * 70)
    print()
    print(f"✓ Successfully created: {len(created_accounts)}/{NUM_ACCOUNTS} accounts")
    print()
    
    if created_accounts:
        print("📧 Created Email Accounts:")
        print()
        for acc in created_accounts:
            print(f"   Email: {acc['email']}")
            print(f"   Password: {acc['password']}")
            print(f"   Created: {acc['created_at']}")
            print()
        
        # Save to file
        output_file = "/home/ubuntu/inframail_accounts.json"
        with open(output_file, 'w') as f:
            json.dump(created_accounts, f, indent=2)
        
        print(f"💾 Account details saved to: {output_file}")
        print()
    
    # Step 5: Next steps
    print("=" * 70)
    print("📝 NEXT STEPS")
    print("=" * 70)
    print()
    print("1. ✅ Email accounts created in Inframail")
    print("2. ⏳ Inframail is warming up accounts automatically")
    print("3. 🔧 Add these accounts to Instantly.ai:")
    print("   https://app.instantly.ai/app/accounts")
    print()
    print("4. 📊 Set daily limits in Instantly:")
    print("   • 400 emails/day per account")
    print("   • Total: 2,000 emails/day")
    print()
    print("5. 🚀 Activate your campaign:")
    print("   https://app.instantly.ai/app/campaigns/1dfdc50b-465a-4cea-8a33-d80ef0a3e010")
    print()
    print("=" * 70)
    print()
    print("⚠️  IMPORTANT: Email Warmup")
    print("=" * 70)
    print()
    print("New accounts need 2 weeks of warmup before sending 400/day:")
    print()
    print("   Week 1: 50 emails/day")
    print("   Week 2: 100 emails/day")
    print("   Week 3: 200 emails/day")
    print("   Week 4+: 400 emails/day")
    print()
    print("Inframail handles this automatically! ✓")
    print()
    print("💡 To send 2,000 emails tomorrow:")
    print("   • Use pre-warmed accounts from Inframail, OR")
    print("   • Start with 250-500 emails/day and scale up")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()


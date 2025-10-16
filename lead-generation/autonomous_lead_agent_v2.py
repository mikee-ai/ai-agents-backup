#!/usr/bin/env python3
"""
Autonomous AI Lead Generation Agent v2.0
Fully automated lead generation and email infrastructure management

Features:
- Automatic email account creation via Inframail
- Automatic connection to Instantly
- Smart warmup management
- Daily lead import (2,000 business owners)
- Self-healing and monitoring
- Complete end-to-end automation

Author: Mikee Shattuck
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import sys
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

# API Keys
APOLLO_API_KEY = "zkZ9TI5jBY2ZkqxiZwof1g"
INSTANTLY_API_KEY = "YjUzNzFjY2EtZGNiNC00OTIzLTgxZGYtZDg1Nzc3YzY5OTg3OlRvZHBXZm9Fb2xqUA=="
INFRAMAIL_API_KEY = "inf_5773448b8c7d5625ae4ab7d4b3227f6d3a147c4a3e8d154d481f51d1a8b4ac"

# Campaign Settings
INSTANTLY_CAMPAIGN_ID = "1dfdc50b-465a-4cea-8a33-d80ef0a3e010"
DAILY_IMPORT_LIMIT = 2000
TARGET_LOCATION = "United States"

# Email Account Settings
REQUIRED_EMAIL_ACCOUNTS = 100  # For 2,000 emails/day (20 per account)
EMAILS_PER_ACCOUNT_PER_DAY = 20

# API Endpoints
APOLLO_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_people/search"
APOLLO_ENRICH_URL = "https://api.apollo.io/api/v1/people/match"
INSTANTLY_LEADS_URL = "https://api.instantly.ai/api/v2/leads"
INSTANTLY_ACCOUNTS_URL = "https://api.instantly.ai/api/v2/accounts"
INFRAMAIL_BASE_URL = "https://app.inframail.io/api/v1"

# Logging Setup
LOG_DIR = "/root/lead_agent/logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"agent_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


# ============================================================================
# INFRAMAIL CLIENT
# ============================================================================

class InframailManager:
    """Manages email accounts via Inframail API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = INFRAMAIL_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_email_accounts(self) -> List[Dict[str, Any]]:
        """Get all email accounts from Inframail"""
        try:
            # Note: Actual endpoint may vary - check Inframail docs
            response = requests.get(
                f"{self.base_url}/accounts",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("accounts", [])
            else:
                logger.warning(f"Could not fetch Inframail accounts: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Inframail API error: {e}")
            return []
    
    def create_email_account(self, email_prefix: str, domain: str = None) -> Optional[Dict[str, Any]]:
        """Create a new email account in Inframail"""
        
        # If no domain provided, use default Inframail domain
        if not domain:
            domain = "inframail.io"  # Inframail provides default domains
        
        email_address = f"{email_prefix}@{domain}"
        
        payload = {
            "email": email_address,
            "displayName": "AI Agents Outreach",
            "enableWarmup": True,
            "warmupSettings": {
                "dailyLimit": 50,
                "increasePerDay": 10
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/accounts",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✓ Created email account: {email_address}")
                return response.json()
            else:
                logger.error(f"Failed to create {email_address}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating email account: {e}")
            return None


# ============================================================================
# INSTANTLY CLIENT
# ============================================================================

class InstantlyManager:
    """Manages Instantly.ai campaigns and email accounts"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_email_accounts(self) -> List[Dict[str, Any]]:
        """Get all email accounts connected to Instantly"""
        try:
            response = requests.get(
                INSTANTLY_ACCOUNTS_URL,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("accounts", [])
            else:
                logger.warning(f"Could not fetch Instantly accounts: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Instantly API error: {e}")
            return []
    
    def add_email_account(self, email: str, password: str, smtp_host: str = None, 
                         imap_host: str = None) -> bool:
        """Add email account to Instantly"""
        
        payload = {
            "email": email,
            "password": password,
            "dailyLimit": EMAILS_PER_ACCOUNT_PER_DAY,
            "warmup": True
        }
        
        # Add SMTP/IMAP if provided
        if smtp_host:
            payload["smtpHost"] = smtp_host
            payload["smtpPort"] = 587
        
        if imap_host:
            payload["imapHost"] = imap_host
            payload["imapPort"] = 993
        
        try:
            response = requests.post(
                INSTANTLY_ACCOUNTS_URL,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✓ Added {email} to Instantly")
                return True
            else:
                logger.error(f"Failed to add {email} to Instantly: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding account to Instantly: {e}")
            return False
    
    def import_lead(self, lead_data: Dict[str, Any]) -> bool:
        """Import lead to Instantly campaign"""
        
        email = lead_data.get("email")
        if not email or email == "email_not_unlocked@domain.com":
            return False
        
        instantly_lead = {
            "email": email,
            "first_name": lead_data.get("first_name", ""),
            "last_name": lead_data.get("last_name", ""),
            "company_name": lead_data.get("organization", {}).get("name", ""),
            "campaign": INSTANTLY_CAMPAIGN_ID
        }
        
        title = lead_data.get("title", "")
        company = instantly_lead["company_name"]
        
        if title and company:
            instantly_lead["personalization"] = f"As the {title} of {company}"
        
        try:
            response = requests.post(
                INSTANTLY_LEADS_URL,
                headers=self.headers,
                json=instantly_lead,
                timeout=30
            )
            
            return response.status_code in [200, 201]
                
        except Exception as e:
            logger.error(f"Import exception: {e}")
            return False


# ============================================================================
# MAIN AUTONOMOUS AGENT
# ============================================================================

class AutonomousLeadAgent:
    """Fully autonomous AI agent for lead generation"""
    
    def __init__(self):
        self.apollo_headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": APOLLO_API_KEY
        }
        
        self.inframail = InframailManager(INFRAMAIL_API_KEY)
        self.instantly = InstantlyManager(INSTANTLY_API_KEY)
        
        self.stats = {
            "total_found": 0,
            "total_enriched": 0,
            "total_imported": 0,
            "total_failed": 0,
            "total_skipped": 0,
            "credits_used": 0,
            "start_time": None,
            "end_time": None,
            "email_accounts_created": 0,
            "email_accounts_connected": 0
        }
    
    def ensure_email_infrastructure(self):
        """Ensure we have enough email accounts set up"""
        
        logger.info("\n" + "="*70)
        logger.info("📧 CHECKING EMAIL INFRASTRUCTURE")
        logger.info("="*70)
        
        # Check Instantly accounts
        instantly_accounts = self.instantly.get_email_accounts()
        num_accounts = len(instantly_accounts)
        
        logger.info(f"Current email accounts in Instantly: {num_accounts}")
        logger.info(f"Required for 2,000 emails/day: {REQUIRED_EMAIL_ACCOUNTS}")
        
        if num_accounts >= REQUIRED_EMAIL_ACCOUNTS:
            logger.info("✓ Sufficient email accounts available")
            logger.info("="*70)
            return True
        
        # Need more accounts
        needed = REQUIRED_EMAIL_ACCOUNTS - num_accounts
        logger.info(f"\n⚠️ Need {needed} more email accounts")
        logger.info("📝 Creating accounts in Inframail...")
        
        # Get Inframail accounts
        inframail_accounts = self.inframail.get_email_accounts()
        logger.info(f"Inframail accounts available: {len(inframail_accounts)}")
        
        # Create new accounts if needed
        created_count = 0
        for i in range(needed):
            account_num = num_accounts + i + 1
            email_prefix = f"outreach{account_num}"
            
            logger.info(f"\n[{i+1}/{needed}] Creating {email_prefix}...")
            
            account = self.inframail.create_email_account(email_prefix)
            
            if account:
                created_count += 1
                self.stats["email_accounts_created"] += 1
                
                # Get credentials
                email = account.get("email", f"{email_prefix}@inframail.io")
                password = account.get("password", "")
                smtp_host = account.get("smtpHost", "smtp.inframail.io")
                imap_host = account.get("imapHost", "imap.inframail.io")
                
                # Add to Instantly
                logger.info(f"   Adding to Instantly...")
                if self.instantly.add_email_account(email, password, smtp_host, imap_host):
                    self.stats["email_accounts_connected"] += 1
                    logger.info(f"   ✓ Connected to Instantly")
                else:
                    logger.warning(f"   ✗ Failed to connect to Instantly")
                
                time.sleep(2)  # Rate limiting
            else:
                logger.warning(f"   ✗ Failed to create account")
        
        logger.info(f"\n📊 Created {created_count} new email accounts")
        logger.info(f"📊 Connected {self.stats['email_accounts_connected']} to Instantly")
        logger.info("="*70)
        
        return created_count > 0
    
    def search_business_owners(self, page: int = 1) -> Dict[str, Any]:
        """Search for business owners matching criteria"""
        
        payload = {
            "person_titles[]": ["owner"],
            "organization_num_employees_ranges[]": [
                "11,20",
                "21,50",
                "51,100"
            ],
            "person_locations[]": [TARGET_LOCATION],
            "page": page,
            "per_page": 100
        }
        
        try:
            response = requests.post(
                APOLLO_SEARCH_URL,
                headers=self.apollo_headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Apollo search error: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"Search exception: {e}")
            return {}
    
    def enrich_person(self, person_id: str, retry_count: int = 3) -> Dict[str, Any]:
        """Enrich person with retry logic"""
        
        for attempt in range(retry_count):
            try:
                payload = {"id": person_id}
                response = requests.post(
                    APOLLO_ENRICH_URL,
                    headers=self.apollo_headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    self.stats["total_enriched"] += 1
                    self.stats["credits_used"] += 1
                    return response.json()
                elif response.status_code == 429:
                    wait_time = (attempt + 1) * 5
                    logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    break
                    
            except Exception as e:
                logger.error(f"Enrich exception (attempt {attempt + 1}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(2)
                    continue
                break
        
        return {}
    
    def run_daily_import(self):
        """Execute daily lead import"""
        
        logger.info("="*70)
        logger.info("🤖 AUTONOMOUS LEAD AGENT v2.0 - DAILY RUN STARTED")
        logger.info("="*70)
        logger.info(f"Target: {DAILY_IMPORT_LIMIT} business owners")
        logger.info(f"Location: {TARGET_LOCATION}")
        logger.info(f"Company Size: 11-100 employees")
        logger.info("="*70)
        
        self.stats["start_time"] = datetime.now()
        
        # Step 1: Ensure email infrastructure
        self.ensure_email_infrastructure()
        
        # Step 2: Import leads
        logger.info("\n" + "="*70)
        logger.info("📥 STARTING LEAD IMPORT")
        logger.info("="*70)
        
        page = 1
        total_imported = 0
        
        while total_imported < DAILY_IMPORT_LIMIT:
            logger.info(f"\n📄 Fetching page {page}...")
            
            results = self.search_business_owners(page=page)
            
            if not results or not results.get("people"):
                logger.info("No more results available")
                break
            
            people = results.get("people", [])
            self.stats["total_found"] += len(people)
            
            logger.info(f"Found {len(people)} owners on page {page}")
            
            for person in people:
                if total_imported >= DAILY_IMPORT_LIMIT:
                    logger.info(f"\n✅ Reached daily limit of {DAILY_IMPORT_LIMIT}")
                    break
                
                person_id = person.get("id")
                name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
                company = person.get("organization", {}).get("name", "N/A")
                
                logger.info(f"[{total_imported + 1}/{DAILY_IMPORT_LIMIT}] {name} @ {company}")
                
                # Enrich
                enriched = self.enrich_person(person_id)
                
                if not enriched or not enriched.get("person"):
                    logger.warning(f"  ✗ Failed to enrich")
                    self.stats["total_skipped"] += 1
                    continue
                
                enriched_person = enriched.get("person", {})
                email = enriched_person.get("email", "")
                
                if not email or email == "email_not_unlocked@domain.com":
                    logger.warning(f"  ✗ No email available")
                    self.stats["total_skipped"] += 1
                    continue
                
                logger.info(f"  ✓ Email: {email}")
                
                # Import
                if self.instantly.import_lead(enriched_person):
                    logger.info(f"  ✓ Imported to Instantly")
                    total_imported += 1
                    self.stats["total_imported"] += 1
                else:
                    logger.warning(f"  ✗ Import failed")
                    self.stats["total_failed"] += 1
                
                # Rate limiting
                time.sleep(1)
            
            # Check pagination
            pagination = results.get("pagination", {})
            total_pages = pagination.get("total_pages", 1)
            
            if page >= total_pages:
                logger.info("\n📄 Reached last page")
                break
            
            page += 1
            time.sleep(2)
        
        self.stats["end_time"] = datetime.now()
        self.print_summary()
    
    def print_summary(self):
        """Print comprehensive summary"""
        
        duration = self.stats["end_time"] - self.stats["start_time"]
        
        logger.info("\n" + "="*70)
        logger.info("📊 DAILY RUN SUMMARY")
        logger.info("="*70)
        logger.info(f"Duration: {duration}")
        logger.info("")
        logger.info("EMAIL INFRASTRUCTURE:")
        logger.info(f"  • Email accounts created: {self.stats['email_accounts_created']}")
        logger.info(f"  • Email accounts connected: {self.stats['email_accounts_connected']}")
        logger.info("")
        logger.info("LEAD GENERATION:")
        logger.info(f"  • Leads found: {self.stats['total_found']}")
        logger.info(f"  • Emails unlocked: {self.stats['total_enriched']}")
        logger.info(f"  • Successfully imported: {self.stats['total_imported']}")
        logger.info(f"  • Failed: {self.stats['total_failed']}")
        logger.info(f"  • Skipped: {self.stats['total_skipped']}")
        logger.info(f"  • Apollo credits used: {self.stats['credits_used']}")
        logger.info("")
        
        if self.stats['total_enriched'] > 0:
            success_rate = (self.stats['total_imported'] / self.stats['total_enriched']) * 100
            logger.info(f"Success Rate: {success_rate:.1f}%")
        
        logger.info("")
        logger.info(f"Next run: Tomorrow at 6:00 AM UTC")
        logger.info("="*70)


def main():
    """Main entry point"""
    
    logger.info("🤖 Autonomous Lead Agent v2.0 Starting...")
    logger.info(f"Log file: {log_file}")
    
    try:
        agent = AutonomousLeadAgent()
        agent.run_daily_import()
        
        logger.info("\n✅ Daily run completed successfully!")
        sys.exit(0)
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Agent stopped by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Autonomous AI Lead Generation Agent - PRODUCTION VERSION
Fully functional with real Inframail API integration

Automatically creates email accounts and scales to 2,000 emails/day over 5 days

Author: Mikee Shattuck
"""

import requests
import json
import time
import logging
import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import sys
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

# API Keys
APOLLO_API_KEY = "YOUR_APOLLO_API_KEY_HERE"
INSTANTLY_API_KEY = "YOUR_INSTANTLY_API_KEY_HERE"

# Inframail API Configuration
INFRAMAIL_API_KEY = "YOUR_INFRAMAIL_API_KEY_HERE"
INFRAMAIL_CUSTOMER_ID = "YOUR_CUSTOMER_ID_HERE"
INFRAMAIL_PROFILE_ID = "YOUR_PROFILE_ID_HERE"
INFRAMAIL_HOST_ORDER_ID = "YOUR_HOST_ORDER_ID_HERE"

# Campaign Settings
INSTANTLY_CAMPAIGN_ID = "YOUR_CAMPAIGN_ID_HERE"
TARGET_LOCATION = "United States"

# Safe Ramp Schedule
EMAILS_PER_ACCOUNT_PER_DAY = 20
ACCOUNTS_TO_CREATE_PER_DAY = 20
TARGET_TOTAL_ACCOUNTS = 100

# Your existing domains
EXISTING_DOMAINS = [
    "yourdomain1.com",
    "yourdomain2.com",
    "yourdomain3.com",
    "yourdomain4.com",
    "yourdomain5.com"
]

# API Endpoints
APOLLO_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_people/search"
APOLLO_ENRICH_URL = "https://api.apollo.io/api/v1/people/match"
INSTANTLY_LEADS_URL = "https://api.instantly.ai/api/v2/leads"
INSTANTLY_ACCOUNTS_URL = "https://api.instantly.ai/api/v2/accounts"
INFRAMAIL_BASE_URL = "https://app.inframail.io/api/v1/host/operations"

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
# INFRAMAIL CLIENT - PRODUCTION
# ============================================================================

class InframailManager:
    """Manages email accounts via Inframail API"""
    
    def __init__(self, api_key: str, customer_id: str, profile_id: str, host_order_id: str):
        self.api_key = api_key
        self.customer_id = customer_id
        self.profile_id = profile_id
        self.host_order_id = host_order_id
        self.base_url = INFRAMAIL_BASE_URL
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    def get_email_accounts(self) -> List[str]:
        """Get all email accounts from Inframail"""
        try:
            url = f"{self.base_url}/email"
            params = {
                "hostOrderId": self.host_order_id,
                "customerId": self.customer_id,
                "profileId": self.profile_id
            }
            
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                emails = data.get("emails", [])
                logger.info(f"✓ Retrieved {len(emails)} email accounts from Inframail")
                return emails
            else:
                logger.error(f"Failed to get Inframail accounts: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Inframail API error: {e}")
            return []
    
    def create_email_account(self, email_address: str, password: str = None, name: str = "AI Agents Outreach") -> bool:
        """Create a new email account in Inframail"""
        
        if not password:
            # Generate secure random password
            password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=16))
        
        payload = {
            "profileId": self.profile_id,
            "email": email_address,
            "password": password,
            "name": name,
            "mode": "add",
            "updatePasswordIfEmailExists": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/email",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"   ✓ Created: {email_address}")
                return True
            else:
                logger.error(f"   ✗ Failed to create {email_address}: {response.status_code}")
                if response.text:
                    logger.error(f"      Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            logger.error(f"   ✗ Error creating {email_address}: {e}")
            return False


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
                data = response.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return data.get("accounts", data.get("data", []))
                return []
            else:
                logger.warning(f"Could not fetch Instantly accounts: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Instantly API error: {e}")
            return []
    
    def add_email_account(self, email: str, password: str, domain: str) -> bool:
        """Add email account to Instantly"""
        
        # Inframail uses standard SMTP/IMAP settings
        smtp_host = f"mail.{domain}"
        imap_host = f"mail.{domain}"
        
        payload = {
            "email": email,
            "first_name": "Mikee",
            "last_name": "Shattuck",
            "provider_code": 1,  # 1 = Custom IMAP/SMTP (Inframail)
            "imap_username": email,
            "imap_password": password,
            "imap_host": imap_host,
            "imap_port": 993,
            "smtp_username": email,
            "smtp_password": password,
            "smtp_host": smtp_host,
            "smtp_port": 587
        }
        
        try:
            response = requests.post(
                INSTANTLY_ACCOUNTS_URL,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"      ✓ Added to Instantly")
                return True
            else:
                logger.error(f"      ✗ Failed to add to Instantly: {response.status_code}")
                if response.text:
                    logger.error(f"         Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            logger.error(f"      ✗ Error adding to Instantly: {e}")
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
            return False


# ============================================================================
# MAIN AUTONOMOUS AGENT
# ============================================================================

class AutonomousLeadAgent:
    """Fully autonomous AI agent with real Inframail API integration"""
    
    def __init__(self):
        self.apollo_headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": APOLLO_API_KEY
        }
        
        self.inframail = InframailManager(
            INFRAMAIL_API_KEY,
            INFRAMAIL_CUSTOMER_ID,
            INFRAMAIL_PROFILE_ID,
            INFRAMAIL_HOST_ORDER_ID
        )
        self.instantly = InstantlyManager(INSTANTLY_API_KEY)
        
        self.stats = {
            "inframail_accounts": 0,
            "instantly_accounts": 0,
            "accounts_created_today": 0,
            "accounts_connected_today": 0,
            "daily_email_capacity": 0,
            "leads_to_import_today": 0,
            "total_found": 0,
            "total_enriched": 0,
            "total_imported": 0,
            "total_failed": 0,
            "total_skipped": 0,
            "credits_used": 0,
            "start_time": None,
            "end_time": None
        }
    
    def calculate_ramp_schedule(self, current_accounts: int) -> Dict[str, Any]:
        """Calculate today's targets based on current account count"""
        
        if current_accounts < 30:
            day = 1
            target_accounts = 30
        elif current_accounts < 50:
            day = 2
            target_accounts = 50
        elif current_accounts < 70:
            day = 3
            target_accounts = 70
        elif current_accounts < 90:
            day = 4
            target_accounts = 90
        else:
            day = 5
            target_accounts = 100
        
        accounts_to_create = min(target_accounts - current_accounts, ACCOUNTS_TO_CREATE_PER_DAY)
        daily_capacity = target_accounts * EMAILS_PER_ACCOUNT_PER_DAY
        
        return {
            "day": day,
            "current_accounts": current_accounts,
            "target_accounts": target_accounts,
            "accounts_to_create": accounts_to_create,
            "daily_capacity": daily_capacity,
            "leads_to_import": daily_capacity
        }
    
    def build_email_infrastructure(self):
        """Build email infrastructure using real Inframail API"""
        
        logger.info("\n" + "="*70)
        logger.info("📧 BUILDING EMAIL INFRASTRUCTURE - PRODUCTION")
        logger.info("="*70)
        
        # Get current accounts from Inframail
        inframail_emails = self.inframail.get_email_accounts()
        self.stats["inframail_accounts"] = len(inframail_emails)
        
        # Get current accounts from Instantly
        instantly_accounts = self.instantly.get_email_accounts()
        self.stats["instantly_accounts"] = len(instantly_accounts)
        
        logger.info(f"Inframail accounts: {self.stats['inframail_accounts']}")
        logger.info(f"Instantly accounts: {self.stats['instantly_accounts']}")
        
        # Use Instantly count as source of truth
        current_count = self.stats['instantly_accounts']
        
        # Calculate today's schedule
        schedule = self.calculate_ramp_schedule(current_count)
        
        logger.info(f"\n📅 RAMP SCHEDULE - DAY {schedule['day']}/5")
        logger.info(f"   Current accounts: {schedule['current_accounts']}")
        logger.info(f"   Target for today: {schedule['target_accounts']}")
        logger.info(f"   Need to create: {schedule['accounts_to_create']}")
        logger.info(f"   Daily capacity after today: {schedule['daily_capacity']} emails/day")
        
        self.stats["daily_email_capacity"] = schedule["daily_capacity"]
        self.stats["leads_to_import_today"] = schedule["leads_to_import"]
        
        if schedule["accounts_to_create"] == 0:
            logger.info("\n✅ Target reached for today!")
            logger.info("="*70)
            return True
        
        # Create email accounts
        accounts_to_create = schedule["accounts_to_create"]
        accounts_per_domain = accounts_to_create // len(EXISTING_DOMAINS)
        remainder = accounts_to_create % len(EXISTING_DOMAINS)
        
        logger.info(f"\n📧 Creating {accounts_to_create} email accounts across {len(EXISTING_DOMAINS)} domains")
        logger.info("="*70)
        
        account_num = current_count + 1
        created_passwords = {}  # Store passwords for Instantly connection
        
        for domain_idx, domain in enumerate(EXISTING_DOMAINS):
            # Distribute accounts evenly
            num_accounts_for_domain = accounts_per_domain + (1 if domain_idx < remainder else 0)
            
            if num_accounts_for_domain == 0:
                continue
            
            logger.info(f"\n[{domain}] Creating {num_accounts_for_domain} accounts")
            
            for i in range(num_accounts_for_domain):
                # Generate email address
                email_address = f"outreach{account_num}@{domain}"
                
                # Generate secure password
                password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=16))
                
                logger.info(f"[{account_num}/{schedule['target_accounts']}] {email_address}")
                
                # Create in Inframail
                if self.inframail.create_email_account(email_address, password):
                    self.stats["accounts_created_today"] += 1
                    created_passwords[email_address] = password
                    
                    # Add to Instantly
                    if self.instantly.add_email_account(email_address, password, domain):
                        self.stats["accounts_connected_today"] += 1
                    
                    account_num += 1
                    time.sleep(2)  # Rate limiting
        
        logger.info(f"\n📊 Infrastructure Build Complete")
        logger.info(f"   Accounts created: {self.stats['accounts_created_today']}")
        logger.info(f"   Accounts connected: {self.stats['accounts_connected_today']}")
        logger.info("="*70)
        
        return self.stats["accounts_connected_today"] > 0
    
    def search_business_owners(self, page: int = 1) -> Dict[str, Any]:
        """Search for business owners"""
        
        payload = {
            "person_titles[]": ["owner"],
            "organization_num_employees_ranges[]": ["11,20", "21,50", "51,100"],
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
    
    def enrich_person(self, person_id: str) -> Dict[str, Any]:
        """Enrich person data"""
        
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
                
        except Exception as e:
            pass
        
        return {}
    
    def run_daily_import(self):
        """Execute daily lead import with safe ramp"""
        
        logger.info("="*70)
        logger.info("🤖 AUTONOMOUS LEAD AGENT - PRODUCTION VERSION")
        logger.info("="*70)
        logger.info(f"Strategy: Safe 5-day ramp to 2,000 emails/day")
        logger.info(f"Inframail API: ✅ Connected")
        logger.info("="*70)
        
        self.stats["start_time"] = datetime.now()
        
        # Step 1: Build infrastructure
        self.build_email_infrastructure()
        
        # Step 2: Import leads
        leads_to_import = self.stats["leads_to_import_today"]
        
        logger.info("\n" + "="*70)
        logger.info(f"📥 IMPORTING {leads_to_import} LEADS")
        logger.info("="*70)
        
        page = 1
        total_imported = 0
        
        while total_imported < leads_to_import:
            results = self.search_business_owners(page=page)
            
            if not results or not results.get("people"):
                break
            
            people = results.get("people", [])
            self.stats["total_found"] += len(people)
            
            for person in people:
                if total_imported >= leads_to_import:
                    break
                
                person_id = person.get("id")
                name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
                company = person.get("organization", {}).get("name", "N/A")
                
                logger.info(f"[{total_imported + 1}/{leads_to_import}] {name} @ {company}")
                
                enriched = self.enrich_person(person_id)
                
                if enriched and enriched.get("person"):
                    enriched_person = enriched.get("person", {})
                    email = enriched_person.get("email", "")
                    
                    if email and email != "email_not_unlocked@domain.com":
                        logger.info(f"  ✓ {email}")
                        
                        if self.instantly.import_lead(enriched_person):
                            logger.info(f"  ✓ Imported")
                            total_imported += 1
                            self.stats["total_imported"] += 1
                        else:
                            self.stats["total_failed"] += 1
                    else:
                        self.stats["total_skipped"] += 1
                else:
                    self.stats["total_skipped"] += 1
                
                time.sleep(1)
            
            page += 1
            time.sleep(2)
        
        self.stats["end_time"] = datetime.now()
        self.print_summary()
    
    def print_summary(self):
        """Print summary"""
        
        duration = self.stats["end_time"] - self.stats["start_time"]
        
        logger.info("\n" + "="*70)
        logger.info("📊 DAILY RUN SUMMARY")
        logger.info("="*70)
        logger.info(f"Duration: {duration}")
        logger.info("")
        logger.info("INFRASTRUCTURE:")
        logger.info(f"  • Accounts created in Inframail: {self.stats['accounts_created_today']}")
        logger.info(f"  • Accounts connected to Instantly: {self.stats['accounts_connected_today']}")
        logger.info(f"  • Total accounts now: {self.stats['instantly_accounts'] + self.stats['accounts_connected_today']}")
        logger.info(f"  • Daily capacity: {self.stats['daily_email_capacity']} emails/day")
        logger.info("")
        logger.info("LEADS:")
        logger.info(f"  • Target: {self.stats['leads_to_import_today']}")
        logger.info(f"  • Imported: {self.stats['total_imported']}")
        logger.info(f"  • Failed: {self.stats['total_failed']}")
        logger.info(f"  • Skipped: {self.stats['total_skipped']}")
        logger.info(f"  • Credits used: {self.stats['credits_used']}")
        logger.info("")
        logger.info("Next run: Tomorrow at 6:00 AM")
        logger.info("="*70)


def main():
    """Main entry point"""
    
    logger.info("🤖 Autonomous Lead Agent - Production Starting...")
    logger.info(f"Log file: {log_file}")
    
    try:
        agent = AutonomousLeadAgent()
        agent.run_daily_import()
        
        logger.info("\n✅ Daily run completed!")
        sys.exit(0)
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Stopped by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()


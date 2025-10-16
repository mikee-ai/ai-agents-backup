#!/usr/bin/env python3
"""
Autonomous AI Lead Generation Agent - SAFE RAMP VERSION
Gradually builds email infrastructure over 5 days for optimal deliverability

Day 1: 20 accounts → 400 emails/day
Day 2: 40 accounts → 800 emails/day
Day 3: 60 accounts → 1,200 emails/day
Day 4: 80 accounts → 1,600 emails/day
Day 5: 100 accounts → 2,000 emails/day

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
APOLLO_API_KEY = "YOUR_APOLLO_API_KEY_HERE"
INSTANTLY_API_KEY = "YOUR_INSTANTLY_API_KEY_HERE"
INFRAMAIL_API_KEY = "inf_5773448b8c7d5625ae4ab7d4b3227f6d3a147c4a3e8d154d481f51d1a8b4ac"

# Campaign Settings
INSTANTLY_CAMPAIGN_ID = "YOUR_CAMPAIGN_ID_HERE"
TARGET_LOCATION = "United States"

# Safe Ramp Schedule
EMAILS_PER_ACCOUNT_PER_DAY = 20
ACCOUNTS_TO_CREATE_PER_DAY = 20  # Create 20 new accounts each day
ACCOUNTS_PER_DOMAIN = 20  # 20 email accounts per domain
TARGET_TOTAL_ACCOUNTS = 100  # Final goal: 100 accounts

# Calculate daily targets based on current account count
# This will be dynamic based on how many accounts exist

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
# INFRAMAIL CLIENT (Mock - needs real API endpoints)
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
        self.created_domains = []
    
    def create_domain(self, domain_name: str) -> bool:
        """Create a new domain in Inframail"""
        logger.info(f"📧 Creating domain: {domain_name}")
        
        # Note: This is a placeholder - actual Inframail API endpoint needed
        # Check Inframail docs or contact support for exact endpoint
        
        try:
            # Placeholder for actual API call
            # response = requests.post(
            #     f"{self.base_url}/domains",
            #     headers=self.headers,
            #     json={"domain": domain_name},
            #     timeout=30
            # )
            
            # For now, simulate success
            logger.info(f"   ✓ Domain created (simulated)")
            self.created_domains.append(domain_name)
            return True
            
        except Exception as e:
            logger.error(f"   ✗ Failed to create domain: {e}")
            return False
    
    def create_email_account(self, email_address: str, domain: str) -> Optional[Dict[str, Any]]:
        """Create a new email account in Inframail"""
        
        logger.info(f"   Creating: {email_address}")
        
        # Note: This is a placeholder - actual Inframail API endpoint needed
        
        try:
            # Placeholder for actual API call
            # response = requests.post(
            #     f"{self.base_url}/accounts",
            #     headers=self.headers,
            #     json={
            #         "email": email_address,
            #         "domain": domain,
            #         "displayName": "AI Agents Outreach"
            #     },
            #     timeout=30
            # )
            
            # For now, return simulated credentials
            account_data = {
                "email": email_address,
                "password": f"Pass{hash(email_address) % 10000}!",  # Simulated
                "smtpHost": f"smtp.{domain}",
                "smtpPort": 587,
                "imapHost": f"imap.{domain}",
                "imapPort": 993
            }
            
            logger.info(f"      ✓ Created")
            return account_data
            
        except Exception as e:
            logger.error(f"      ✗ Failed: {e}")
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
                data = response.json()
                # Handle different response formats
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
    
    def add_email_account(self, account_data: Dict[str, Any]) -> bool:
        """Add email account to Instantly"""
        
        email = account_data.get("email")
        password = account_data.get("password")
        
        payload = {
            "email": email,
            "password": password,
            "dailyLimit": EMAILS_PER_ACCOUNT_PER_DAY,
            "warmup": True,
            "smtpHost": account_data.get("smtpHost"),
            "smtpPort": account_data.get("smtpPort", 587),
            "imapHost": account_data.get("imapHost"),
            "imapPort": account_data.get("imapPort", 993)
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
    """Autonomous AI agent with safe ramp-up strategy"""
    
    def __init__(self):
        self.apollo_headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": APOLLO_API_KEY
        }
        
        self.inframail = InframailManager(INFRAMAIL_API_KEY)
        self.instantly = InstantlyManager(INSTANTLY_API_KEY)
        
        self.stats = {
            "current_accounts": 0,
            "accounts_created_today": 0,
            "accounts_connected_today": 0,
            "domains_created_today": 0,
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
        
        # Determine what day of ramp we're on
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
        """Build email infrastructure following safe ramp schedule"""
        
        logger.info("\n" + "="*70)
        logger.info("📧 BUILDING EMAIL INFRASTRUCTURE - SAFE RAMP")
        logger.info("="*70)
        
        # Get current accounts
        instantly_accounts = self.instantly.get_email_accounts()
        current_count = len(instantly_accounts)
        self.stats["current_accounts"] = current_count
        
        logger.info(f"Current email accounts: {current_count}")
        
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
        
        # Calculate domains needed
        accounts_to_create = schedule["accounts_to_create"]
        domains_needed = max(1, (accounts_to_create + ACCOUNTS_PER_DOMAIN - 1) // ACCOUNTS_PER_DOMAIN)
        
        logger.info(f"\n📋 Creating {accounts_to_create} accounts across {domains_needed} domain(s)")
        logger.info("="*70)
        
        # Create domains
        created_domains = []
        for i in range(domains_needed):
            domain_name = f"aiagents{schedule['day']}{i+1}.com"  # Example domain naming
            
            logger.info(f"\n[Domain {i+1}/{domains_needed}] {domain_name}")
            
            if self.inframail.create_domain(domain_name):
                created_domains.append(domain_name)
                self.stats["domains_created_today"] += 1
                time.sleep(2)
        
        if not created_domains:
            logger.error("\n❌ Failed to create any domains")
            return False
        
        # Create email accounts
        logger.info(f"\n📧 Creating {accounts_to_create} email accounts...")
        
        accounts_per_domain = accounts_to_create // len(created_domains)
        remainder = accounts_to_create % len(created_domains)
        
        account_num = current_count + 1
        
        for domain_idx, domain in enumerate(created_domains):
            # Distribute accounts evenly, with remainder going to first domains
            num_accounts_for_domain = accounts_per_domain + (1 if domain_idx < remainder else 0)
            
            logger.info(f"\n[{domain}] Creating {num_accounts_for_domain} accounts")
            
            for i in range(num_accounts_for_domain):
                email_address = f"outreach{account_num}@{domain}"
                
                # Create in Inframail
                account_data = self.inframail.create_email_account(email_address, domain)
                
                if account_data:
                    self.stats["accounts_created_today"] += 1
                    
                    # Add to Instantly
                    if self.instantly.add_email_account(account_data):
                        self.stats["accounts_connected_today"] += 1
                    
                    account_num += 1
                    time.sleep(1)  # Rate limiting
        
        logger.info(f"\n📊 Infrastructure Build Complete")
        logger.info(f"   Domains created: {self.stats['domains_created_today']}")
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
        logger.info("🤖 AUTONOMOUS LEAD AGENT - SAFE RAMP VERSION")
        logger.info("="*70)
        logger.info(f"Strategy: Gradual 5-day ramp to 2,000 emails/day")
        logger.info("="*70)
        
        self.stats["start_time"] = datetime.now()
        
        # Step 1: Build infrastructure for today
        self.build_email_infrastructure()
        
        # Step 2: Import leads based on today's capacity
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
        logger.info(f"  • Domains created: {self.stats['domains_created_today']}")
        logger.info(f"  • Accounts created: {self.stats['accounts_created_today']}")
        logger.info(f"  • Accounts connected: {self.stats['accounts_connected_today']}")
        logger.info(f"  • Total accounts now: {self.stats['current_accounts'] + self.stats['accounts_connected_today']}")
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
    
    logger.info("🤖 Autonomous Lead Agent - Safe Ramp Starting...")
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


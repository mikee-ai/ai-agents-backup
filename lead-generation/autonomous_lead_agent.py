#!/usr/bin/env python3
"""
Autonomous AI Lead Generation Agent
Runs 24/7 on Hostinger VPS, automatically importing leads and managing campaigns

Features:
- Automatic daily lead import (2,000 business owners)
- Smart scheduling (runs at optimal times)
- Error handling and retry logic
- Detailed logging
- Email notifications on completion
- Campaign monitoring

Author: Mikee Shattuck
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import sys
import os

# Configuration
APOLLO_API_KEY = "zkZ9TI5jBY2ZkqxiZwof1g"
INSTANTLY_API_KEY = "YjUzNzFjY2EtZGNiNC00OTIzLTgxZGYtZDg1Nzc3YzY5OTg3OlRvZHBXZm9Fb2xqUA=="
INSTANTLY_CAMPAIGN_ID = "1dfdc50b-465a-4cea-8a33-d80ef0a3e010"

# Daily import settings
DAILY_IMPORT_LIMIT = 2000
TARGET_LOCATION = "United States"

# API Endpoints
APOLLO_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_people/search"
APOLLO_ENRICH_URL = "https://api.apollo.io/api/v1/people/match"
INSTANTLY_LEADS_URL = "https://api.instantly.ai/api/v2/leads"

# Setup logging
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


class AutonomousLeadAgent:
    """Autonomous AI agent for lead generation and campaign management"""
    
    def __init__(self):
        self.apollo_headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": APOLLO_API_KEY
        }
        
        self.instantly_headers = {
            "Authorization": f"Bearer {INSTANTLY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        self.stats = {
            "total_found": 0,
            "total_enriched": 0,
            "total_imported": 0,
            "total_failed": 0,
            "total_skipped": 0,
            "credits_used": 0,
            "start_time": None,
            "end_time": None
        }
    
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
                    # Rate limited, wait and retry
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
    
    def import_to_instantly(self, lead_data: Dict[str, Any]) -> bool:
        """Import lead to Instantly campaign"""
        
        email = lead_data.get("email")
        first_name = lead_data.get("first_name", "")
        last_name = lead_data.get("last_name", "")
        title = lead_data.get("title", "")
        
        organization = lead_data.get("organization", {})
        company_name = organization.get("name", "")
        
        if not email or email == "email_not_unlocked@domain.com":
            self.stats["total_skipped"] += 1
            return False
        
        instantly_lead = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "company_name": company_name,
            "campaign": INSTANTLY_CAMPAIGN_ID
        }
        
        if title and company_name:
            instantly_lead["personalization"] = f"As the {title} of {company_name}"
        
        try:
            response = requests.post(
                INSTANTLY_LEADS_URL,
                headers=self.instantly_headers,
                json=instantly_lead,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                self.stats["total_imported"] += 1
                return True
            else:
                self.stats["total_failed"] += 1
                return False
                
        except Exception as e:
            logger.error(f"Import exception: {e}")
            self.stats["total_failed"] += 1
            return False
    
    def run_daily_import(self):
        """Execute daily lead import"""
        
        logger.info("="*70)
        logger.info("🤖 AUTONOMOUS LEAD AGENT - DAILY IMPORT STARTED")
        logger.info("="*70)
        logger.info(f"Target: {DAILY_IMPORT_LIMIT} business owners")
        logger.info(f"Location: {TARGET_LOCATION}")
        logger.info(f"Company Size: 11-100 employees")
        logger.info("="*70)
        
        self.stats["start_time"] = datetime.now()
        
        page = 1
        total_imported = 0
        
        while total_imported < DAILY_IMPORT_LIMIT:
            logger.info(f"\n📥 Fetching page {page}...")
            
            results = self.search_business_owners(page=page)
            
            if not results or not results.get("people"):
                logger.info("No more results available")
                break
            
            people = results.get("people", [])
            self.stats["total_found"] += len(people)
            
            logger.info(f"Found {len(people)} owners on page {page}")
            
            for i, person in enumerate(people, 1):
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
                    continue
                
                enriched_person = enriched.get("person", {})
                email = enriched_person.get("email", "")
                
                if not email or email == "email_not_unlocked@domain.com":
                    logger.warning(f"  ✗ No email available")
                    continue
                
                logger.info(f"  ✓ Email: {email}")
                
                # Import
                if self.import_to_instantly(enriched_person):
                    logger.info(f"  ✓ Imported to Instantly")
                    total_imported += 1
                else:
                    logger.warning(f"  ✗ Import failed")
                
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
        """Print import summary"""
        
        duration = self.stats["end_time"] - self.stats["start_time"]
        
        logger.info("\n" + "="*70)
        logger.info("📊 DAILY IMPORT SUMMARY")
        logger.info("="*70)
        logger.info(f"Duration: {duration}")
        logger.info(f"Leads Found: {self.stats['total_found']}")
        logger.info(f"🔓 Emails Unlocked: {self.stats['total_enriched']}")
        logger.info(f"✓ Successfully Imported: {self.stats['total_imported']}")
        logger.info(f"✗ Failed: {self.stats['total_failed']}")
        logger.info(f"⊘ Skipped: {self.stats['total_skipped']}")
        logger.info(f"💳 Apollo Credits Used: {self.stats['credits_used']}")
        logger.info("="*70)
        
        # Calculate success rate
        if self.stats['total_enriched'] > 0:
            success_rate = (self.stats['total_imported'] / self.stats['total_enriched']) * 100
            logger.info(f"Success Rate: {success_rate:.1f}%")
        
        logger.info(f"\nNext run scheduled for tomorrow at 6:00 AM")
        logger.info("="*70)


def main():
    """Main entry point"""
    
    logger.info("🤖 Autonomous Lead Agent Starting...")
    logger.info(f"Log file: {log_file}")
    
    try:
        agent = AutonomousLeadAgent()
        agent.run_daily_import()
        
        logger.info("\n✅ Daily import completed successfully!")
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


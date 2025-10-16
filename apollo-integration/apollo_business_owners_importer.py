#!/usr/bin/env python3
"""
Apollo.io to Instantly.ai - Business Owners Importer
Targets actual business owners (not just executives at large companies)

Filters:
- Job titles: Owner, Founder, Co-Founder, President & Owner
- Company size: 1-500 employees (small to mid-size businesses)
- Revenue: $1M-$50M (excludes huge corporations)
- Location: Florida

Usage:
    python3 apollo_business_owners_importer.py --daily-limit 100
"""

import requests
import json
import time
import argparse
from datetime import datetime
from typing import List, Dict, Any

# Configuration
APOLLO_API_KEY = "zkZ9TI5jBY2ZkqxiZwof1g"
INSTANTLY_API_KEY = "YjUzNzFjY2EtZGNiNC00OTIzLTgxZGYtZDg1Nzc3YzY5OTg3OlRvZHBXZm9Fb2xqUA=="
INSTANTLY_CAMPAIGN_ID = "1dfdc50b-465a-4cea-8a33-d80ef0a3e010"

# API Endpoints
APOLLO_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_people/search"
APOLLO_ENRICH_URL = "https://api.apollo.io/api/v1/people/match"
INSTANTLY_LEADS_URL = "https://api.instantly.ai/api/v2/leads"

class BusinessOwnersImporter:
    def __init__(self, apollo_key: str, instantly_key: str, campaign_id: str):
        self.apollo_key = apollo_key
        self.instantly_key = instantly_key
        self.campaign_id = campaign_id
        
        self.apollo_headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": apollo_key
        }
        
        self.instantly_headers = {
            "Authorization": f"Bearer {instantly_key}",
            "Content-Type": "application/json"
        }
        
        self.stats = {
            "searched": 0,
            "found": 0,
            "enriched": 0,
            "imported": 0,
            "failed": 0,
            "skipped": 0,
            "credits_used": 0
        }
    
    def search_business_owners(
        self,
        location: str = "Florida",
        per_page: int = 100,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search for actual business owners (not just executives)
        
        Filters:
        - Titles: Owner, Founder, Co-Founder, President & Owner
        - Company size: 1-500 employees (SMBs)
        - Revenue: $1M-$50M (excludes mega-corporations)
        """
        
        payload = {
            # Target actual owners, not just executives
            "person_titles[]": [
                "Owner",
                "Founder",
                "Co-Founder", 
                "Co-Owner",
                "President & Owner",
                "CEO & Founder",
                "Managing Partner"
            ],
            
            # Small to mid-size businesses (not Fortune 500)
            "organization_num_employees_ranges[]": [
                "1,10",      # Micro businesses
                "11,50",     # Small businesses
                "51,200",    # Medium businesses
                "201,500"    # Larger SMBs
            ],
            
            # Revenue range: $1M-$50M (real SMBs, not mega-corps)
            "revenue_range": {
                "min": 1000000,    # $1M minimum
                "max": 50000000    # $50M maximum
            },
            
            # Location
            "person_locations[]": [location],
            
            # Pagination
            "page": page,
            "per_page": per_page
        }
        
        try:
            response = requests.post(
                APOLLO_SEARCH_URL,
                headers=self.apollo_headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Apollo API Error: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            print(f"Error searching Apollo: {e}")
            return {}
    
    def enrich_person(self, person_id: str) -> Dict[str, Any]:
        """
        Enrich a person to unlock their email address
        This consumes 1 export credit per person
        """
        
        payload = {
            "id": person_id
        }
        
        try:
            response = requests.post(
                APOLLO_ENRICH_URL,
                headers=self.apollo_headers,
                json=payload
            )
            
            if response.status_code == 200:
                self.stats["enriched"] += 1
                self.stats["credits_used"] += 1
                return response.json()
            else:
                return {}
                
        except Exception as e:
            return {}
    
    def import_to_instantly(self, lead_data: Dict[str, Any]) -> bool:
        """
        Import a single lead to Instantly.ai campaign
        """
        
        # Extract lead information
        email = lead_data.get("email")
        first_name = lead_data.get("first_name", "")
        last_name = lead_data.get("last_name", "")
        title = lead_data.get("title", "")
        
        # Get company info
        organization = lead_data.get("organization", {})
        company_name = organization.get("name", "")
        
        # Skip if no email or still locked
        if not email or email == "email_not_unlocked@domain.com":
            self.stats["skipped"] += 1
            return False
        
        # Prepare lead for Instantly
        instantly_lead = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "company_name": company_name,
            "campaign": self.campaign_id
        }
        
        # Add custom variables
        if title and company_name:
            instantly_lead["personalization"] = f"As the {title} of {company_name}"
        
        try:
            response = requests.post(
                INSTANTLY_LEADS_URL,
                headers=self.instantly_headers,
                json=instantly_lead
            )
            
            if response.status_code in [200, 201]:
                self.stats["imported"] += 1
                return True
            else:
                self.stats["failed"] += 1
                return False
                
        except Exception as e:
            self.stats["failed"] += 1
            return False
    
    def run_import(
        self,
        daily_limit: int = 100,
        location: str = "Florida"
    ):
        """
        Main import function
        """
        
        print("="*70)
        print("🏢 BUSINESS OWNERS IMPORTER - APOLLO TO INSTANTLY")
        print("="*70)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target: {daily_limit} business owners")
        print(f"Location: {location}")
        print(f"Company Size: 1-500 employees (SMBs)")
        print(f"Revenue: $1M-$50M")
        print(f"Titles: Owner, Founder, Co-Founder, Managing Partner")
        print("="*70 + "\n")
        
        page = 1
        total_imported = 0
        
        while total_imported < daily_limit:
            print(f"📥 Fetching page {page} from Apollo...")
            
            # Search Apollo for business owners
            results = self.search_business_owners(
                location=location,
                per_page=100,
                page=page
            )
            
            if not results or not results.get("people"):
                print("No more results from Apollo")
                break
            
            people = results.get("people", [])
            self.stats["found"] += len(people)
            
            print(f"Found {len(people)} business owners on page {page}\n")
            
            # Process each lead
            for i, person in enumerate(people, 1):
                if total_imported >= daily_limit:
                    print(f"\n✅ Reached daily limit of {daily_limit} leads")
                    break
                
                person_id = person.get("id")
                name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
                title = person.get("title", "")
                
                # Get company info
                org = person.get("organization", {})
                company = org.get("name", "N/A")
                employees = org.get("estimated_num_employees", "N/A")
                
                print(f"[{i}/{len(people)}] {name} - {title}")
                print(f"  🏢 Company: {company} ({employees} employees)")
                
                # Enrich to unlock email (uses 1 credit)
                print(f"  🔓 Unlocking email...", end=" ")
                enriched = self.enrich_person(person_id)
                
                if not enriched or not enriched.get("person"):
                    print("✗ Failed")
                    self.stats["failed"] += 1
                    continue
                
                enriched_person = enriched.get("person", {})
                email = enriched_person.get("email", "")
                
                if not email or email == "email_not_unlocked@domain.com":
                    print(f"✗ No email")
                    self.stats["skipped"] += 1
                    continue
                
                print(f"✓ {email}")
                
                # Import to Instantly
                print(f"  📤 Importing to Instantly...", end=" ")
                if self.import_to_instantly(enriched_person):
                    print("✓\n")
                    total_imported += 1
                else:
                    print("✗\n")
                
                # Rate limiting
                time.sleep(1)
            
            # Check if there are more pages
            pagination = results.get("pagination", {})
            total_pages = pagination.get("total_pages", 1)
            
            if page >= total_pages:
                print("\n📄 Reached last page of results")
                break
            
            page += 1
            print(f"\n{'='*70}\n")
            time.sleep(2)
        
        # Print summary
        print("\n" + "="*70)
        print("📊 IMPORT SUMMARY")
        print("="*70)
        print(f"Business Owners Found: {self.stats['found']}")
        print(f"🔓 Emails Unlocked: {self.stats['enriched']}")
        print(f"✓ Successfully Imported: {self.stats['imported']}")
        print(f"✗ Failed: {self.stats['failed']}")
        print(f"⊘ Skipped (no email): {self.stats['skipped']}")
        print(f"💳 Apollo Credits Used: {self.stats['credits_used']}")
        print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

def main():
    parser = argparse.ArgumentParser(description="Business Owners Importer")
    parser.add_argument("--daily-limit", type=int, default=100, help="Daily lead import limit")
    parser.add_argument("--location", type=str, default="Florida", help="Geographic location")
    
    args = parser.parse_args()
    
    # Create importer
    importer = BusinessOwnersImporter(
        apollo_key=APOLLO_API_KEY,
        instantly_key=INSTANTLY_API_KEY,
        campaign_id=INSTANTLY_CAMPAIGN_ID
    )
    
    # Run import
    importer.run_import(
        daily_limit=args.daily_limit,
        location=args.location
    )

if __name__ == "__main__":
    main()


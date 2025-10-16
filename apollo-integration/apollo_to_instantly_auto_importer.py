#!/usr/bin/env python3
"""
Apollo.io to Instantly.ai Auto-Importer
Automatically searches Apollo for leads and imports them to Instantly campaign

Requirements:
1. Apollo.io API key (from https://app.apollo.io/#/settings/integrations/api)
2. Instantly.ai API key (already configured)
3. Apollo.io paid plan (People Search requires credits)

Usage:
    python3 apollo_to_instantly_auto_importer.py --daily-limit 2000
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
INSTANTLY_LEADS_URL = "https://api.instantly.ai/api/v2/leads"

class ApolloToInstantlyImporter:
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
            "imported": 0,
            "failed": 0,
            "skipped": 0
        }
    
    def search_apollo_leads(
        self,
        seniorities: List[str] = ["owner"],
        min_revenue: int = 1000000,
        location: str = "Florida",
        per_page: int = 100,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search for leads in Apollo.io
        
        Args:
            seniorities: List of seniority levels (owner, founder, c_suite, etc.)
            min_revenue: Minimum company revenue in USD
            location: Geographic location
            per_page: Results per page (max 100)
            page: Page number
            
        Returns:
            API response with people data
        """
        
        payload = {
            "person_seniorities[]": seniorities,
            "revenue_range": {
                "min": min_revenue
            },
            "person_locations[]": [location],
            "page": page,
            "per_page": per_page,
            "contact_email_status[]": ["verified", "likely_to_engage"]  # Only get valid emails
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
    
    def import_to_instantly(self, lead_data: Dict[str, Any]) -> bool:
        """
        Import a single lead to Instantly.ai campaign
        
        Args:
            lead_data: Lead information from Apollo
            
        Returns:
            True if successful, False otherwise
        """
        
        # Extract lead information
        email = lead_data.get("email")
        first_name = lead_data.get("first_name", "")
        last_name = lead_data.get("last_name", "")
        title = lead_data.get("title", "")
        
        # Get company info
        organization = lead_data.get("organization", {})
        company_name = organization.get("name", "")
        
        # Skip if no email
        if not email:
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
        if title:
            instantly_lead["personalization"] = f"I noticed you're the {title} at {company_name}."
        
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
                print(f"Instantly API Error for {email}: {response.status_code} - {response.text}")
                self.stats["failed"] += 1
                return False
                
        except Exception as e:
            print(f"Error importing {email}: {e}")
            self.stats["failed"] += 1
            return False
    
    def run_import(
        self,
        daily_limit: int = 2000,
        seniorities: List[str] = ["owner"],
        min_revenue: int = 1000000,
        location: str = "Florida"
    ):
        """
        Main import function
        
        Args:
            daily_limit: Maximum leads to import per run
            seniorities: Job seniority levels to search
            min_revenue: Minimum company revenue
            location: Geographic location
        """
        
        print("="*70)
        print("APOLLO.IO TO INSTANTLY.AI AUTO-IMPORTER")
        print("="*70)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target: {daily_limit} leads")
        print(f"Filters: {seniorities} | ${min_revenue:,}+ revenue | {location}")
        print("="*70 + "\n")
        
        page = 1
        total_imported = 0
        
        while total_imported < daily_limit:
            print(f"Fetching page {page} from Apollo...")
            
            # Search Apollo
            results = self.search_apollo_leads(
                seniorities=seniorities,
                min_revenue=min_revenue,
                location=location,
                per_page=100,
                page=page
            )
            
            if not results or not results.get("people"):
                print("No more results from Apollo")
                break
            
            people = results.get("people", [])
            self.stats["found"] += len(people)
            
            print(f"Found {len(people)} leads on page {page}")
            
            # Import each lead
            for i, person in enumerate(people, 1):
                if total_imported >= daily_limit:
                    print(f"\nReached daily limit of {daily_limit} leads")
                    break
                
                email = person.get("email", "N/A")
                name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
                company = person.get("organization", {}).get("name", "N/A")
                
                print(f"  [{i}/{len(people)}] Importing: {name} ({email}) - {company}...", end=" ")
                
                if self.import_to_instantly(person):
                    print("✓")
                    total_imported += 1
                else:
                    print("✗")
                
                # Rate limiting - be nice to APIs
                time.sleep(0.5)
            
            # Check if there are more pages
            pagination = results.get("pagination", {})
            total_pages = pagination.get("total_pages", 1)
            
            if page >= total_pages:
                print("\nReached last page of results")
                break
            
            page += 1
            time.sleep(1)  # Pause between pages
        
        # Print summary
        print("\n" + "="*70)
        print("IMPORT SUMMARY")
        print("="*70)
        print(f"Apollo Searches: {self.stats['searched']}")
        print(f"Leads Found: {self.stats['found']}")
        print(f"✓ Successfully Imported: {self.stats['imported']}")
        print(f"✗ Failed: {self.stats['failed']}")
        print(f"⊘ Skipped (no email): {self.stats['skipped']}")
        print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

def main():
    parser = argparse.ArgumentParser(description="Apollo to Instantly Auto-Importer")
    parser.add_argument("--daily-limit", type=int, default=2000, help="Daily lead import limit")
    parser.add_argument("--apollo-key", type=str, help="Apollo.io API key")
    parser.add_argument("--location", type=str, default="Florida", help="Geographic location")
    parser.add_argument("--min-revenue", type=int, default=1000000, help="Minimum company revenue")
    parser.add_argument("--seniority", type=str, default="owner", help="Job seniority (owner, founder, c_suite)")
    
    args = parser.parse_args()
    
    # Get Apollo API key
    apollo_key = args.apollo_key or APOLLO_API_KEY
    
    if not apollo_key:
        print("="*70)
        print("⚠️  APOLLO.IO API KEY REQUIRED")
        print("="*70)
        print("\nYou need an Apollo.io API key to use this importer.")
        print("\nHow to get your Apollo API key:")
        print("1. Go to: https://app.apollo.io/#/settings/integrations/api")
        print("2. Click 'Create API Key'")
        print("3. Copy the key")
        print("4. Run this script with: --apollo-key YOUR_KEY")
        print("\nOr edit this file and add your key to APOLLO_API_KEY variable")
        print("="*70)
        return
    
    # Create importer
    importer = ApolloToInstantlyImporter(
        apollo_key=apollo_key,
        instantly_key=INSTANTLY_API_KEY,
        campaign_id=INSTANTLY_CAMPAIGN_ID
    )
    
    # Run import
    importer.run_import(
        daily_limit=args.daily_limit,
        seniorities=[args.seniority],
        min_revenue=args.min_revenue,
        location=args.location
    )

if __name__ == "__main__":
    main()


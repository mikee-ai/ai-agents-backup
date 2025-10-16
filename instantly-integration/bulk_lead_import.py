#!/usr/bin/env python3
"""
Bulk Lead Import for Instantly.ai
Imports leads from CSV file into a campaign
"""

import requests
import csv
import argparse
import sys
from typing import List, Dict

# API Configuration
API_KEY = "b5371cca-dcb4-4923-81df-d85777c69987:fvUoAqYEXpDE"  # Replace with your actual API key
BASE_URL = "https://api.instantly.ai/api/v2"

def read_csv_leads(csv_file: str) -> List[Dict]:
    """Read leads from CSV file"""
    leads = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)
        
        print(f"✓ Read {len(leads)} leads from {csv_file}")
        return leads
    
    except FileNotFoundError:
        print(f"✗ Error: File '{csv_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error reading CSV: {str(e)}")
        sys.exit(1)

def add_lead_to_campaign(lead_data: Dict, campaign_id: str) -> bool:
    """Add a single lead to campaign via API"""
    
    # Prepare lead payload
    payload = {
        "email": lead_data.get('email'),
        "first_name": lead_data.get('first_name', ''),
        "last_name": lead_data.get('last_name', ''),
        "company_name": lead_data.get('company_name', ''),
        "personalization": lead_data.get('personalization', ''),
        "campaign": campaign_id
    }
    
    # Add custom fields if present
    custom_fields = {}
    for key, value in lead_data.items():
        if key not in ['email', 'first_name', 'last_name', 'company_name', 'personalization']:
            custom_fields[key] = value
    
    if custom_fields:
        payload['payload'] = custom_fields
    
    # Make API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/leads",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"  ✗ Failed: {lead_data.get('email')} - {response.text}")
            return False
    
    except Exception as e:
        print(f"  ✗ Error: {lead_data.get('email')} - {str(e)}")
        return False

def bulk_import(csv_file: str, campaign_id: str, batch_size: int = 10):
    """Import leads in batches"""
    
    print("\n" + "="*70)
    print("BULK LEAD IMPORT TO INSTANTLY.AI")
    print("="*70)
    
    # Read leads from CSV
    leads = read_csv_leads(csv_file)
    
    if not leads:
        print("✗ No leads found in CSV file")
        return
    
    # Validate required fields
    required_fields = ['email']
    for lead in leads:
        if not all(field in lead for field in required_fields):
            print(f"✗ Error: CSV must contain 'email' column")
            sys.exit(1)
    
    # Import leads
    print(f"\nImporting {len(leads)} leads to campaign {campaign_id}...")
    print(f"Batch size: {batch_size}")
    print("-" * 70)
    
    success_count = 0
    failed_count = 0
    
    for i, lead in enumerate(leads, 1):
        print(f"[{i}/{len(leads)}] Adding {lead.get('email')}...", end=" ")
        
        if add_lead_to_campaign(lead, campaign_id):
            print("✓")
            success_count += 1
        else:
            failed_count += 1
        
        # Pause between batches to avoid rate limiting
        if i % batch_size == 0 and i < len(leads):
            print(f"\n  Processed {i} leads, pausing briefly...")
            import time
            time.sleep(2)
    
    # Summary
    print("\n" + "="*70)
    print("IMPORT COMPLETE")
    print("="*70)
    print(f"✓ Successfully imported: {success_count}")
    print(f"✗ Failed: {failed_count}")
    print(f"📊 Success rate: {(success_count/len(leads)*100):.1f}%")
    print("="*70)

def main():
    """Main function with argument parsing"""
    
    parser = argparse.ArgumentParser(
        description='Bulk import leads to Instantly.ai campaign'
    )
    parser.add_argument(
        '--csv',
        required=True,
        help='Path to CSV file with leads'
    )
    parser.add_argument(
        '--campaign-id',
        required=True,
        help='Instantly.ai campaign ID'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='Number of leads to process before pausing (default: 10)'
    )
    parser.add_argument(
        '--api-key',
        help='Instantly.ai API key (overrides default)'
    )
    
    args = parser.parse_args()
    
    # Update API key if provided
    global API_KEY
    if args.api_key:
        API_KEY = args.api_key
    
    # Run import
    bulk_import(args.csv, args.campaign_id, args.batch_size)

if __name__ == "__main__":
    main()


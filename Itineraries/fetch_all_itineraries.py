#!/usr/bin/env python3
"""
Fetch all itinerary entries from Strapi API using pagination.
Strapi returns 25 entries per page by default, so we need to paginate through all pages.
"""

import requests
import json
import time

def fetch_all_itineraries(base_url, max_pages=100):
    """
    Fetch all itinerary entries from Strapi API with pagination.
    
    Args:
        base_url: Base URL for the Strapi API (e.g., "http://127.0.0.1:1337/api/itineraries")
        max_pages: Maximum number of pages to fetch (safety limit)
    
    Returns:
        List of all itinerary entries
    """
    all_entries = []
    page = 1
    page_size = 25  # Strapi default page size
    
    print(f"🔍 Fetching all itinerary entries from {base_url}")
    print(f"📄 Page size: {page_size}")
    print("=" * 60)
    
    while page <= max_pages:
        # Construct URL with pagination parameters
        url = f"{base_url}?pagination[page]={page}&pagination[pageSize]={page_size}"
        
        print(f"📥 Fetching page {page}...", end=" ")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if we have data
            if 'data' not in data or not data['data']:
                print("No more data found")
                break
            
            entries = data['data']
            all_entries.extend(entries)
            
            print(f"✅ Found {len(entries)} entries (Total: {len(all_entries)})")
            
            # Check if we've reached the last page
            pagination = data.get('meta', {}).get('pagination', {})
            total_pages = pagination.get('pageCount', 0)
            current_page = pagination.get('page', page)
            
            if current_page >= total_pages:
                print(f"📄 Reached last page ({total_pages})")
                break
            
            # Add small delay to avoid overwhelming the server
            time.sleep(0.1)
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching page {page}: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON for page {page}: {e}")
            break
        except Exception as e:
            print(f"❌ Unexpected error on page {page}: {e}")
            break
    
    print("=" * 60)
    print(f"📊 FETCH COMPLETE")
    print(f"   Total pages fetched: {page - 1}")
    print(f"   Total entries: {len(all_entries)}")
    
    return all_entries

def save_entries_to_file(entries, filename):
    """Save entries to a JSON file."""
    output_data = {
        "data": entries,
        "meta": {
            "total_entries": len(entries),
            "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(entries)} entries to {filename}")

def main():
    # Configuration
    base_url = "http://127.0.0.1:1337/api/itineraries"
    output_file = "all-itineraries-complete.json"
    
    print("🚀 STRAPI ITINERARIES BULK FETCHER")
    print("=" * 60)
    
    # Fetch all entries
    all_entries = fetch_all_itineraries(base_url)
    
    if all_entries:
        # Save to file
        save_entries_to_file(all_entries, output_file)
        
        # Show summary
        print(f"\n📈 SUMMARY:")
        print(f"   Expected entries: 1421 (from Postman collection)")
        print(f"   Fetched entries: {len(all_entries)}")
        
        if len(all_entries) == 1421:
            print(f"   ✅ Perfect match! All entries fetched successfully.")
        elif len(all_entries) > 1421:
            print(f"   ⚠️  More entries than expected - possible duplicates or new entries")
        else:
            missing = 1421 - len(all_entries)
            print(f"   ❌ Missing {missing} entries - some may not have been uploaded")
        
        # Show first few entries
        print(f"\n📋 SAMPLE ENTRIES:")
        for i, entry in enumerate(all_entries[:5], 1):
            name = entry.get('Name', 'Unknown')
            entry_id = entry.get('id', 'Unknown')
            print(f"   {i}. ID {entry_id}: {name}")
        
        if len(all_entries) > 5:
            print(f"   ... and {len(all_entries) - 5} more entries")
    
    else:
        print("❌ No entries were fetched. Check your API connection and URL.")

if __name__ == "__main__":
    main()


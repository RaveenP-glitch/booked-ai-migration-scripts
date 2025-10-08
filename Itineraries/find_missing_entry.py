#!/usr/bin/env python3
"""
Compare Postman collection with post-migration-check.json to find missing entries.
Since post-migration-check.json only contains 25 entries (a sample), we need to
identify which specific entry from the Postman collection is missing.
"""

import json
import re

def extract_name_from_postman_request(request):
    """Extract the Name field from a Postman request body."""
    try:
        if 'request' in request and 'body' in request['request']:
            body = request['request']['body']
            if 'raw' in body:
                raw_data = body['raw']
                # Parse the JSON from the raw body
                data = json.loads(raw_data)
                if 'data' in data and 'Name' in data['data']:
                    return data['data']['Name']
    except Exception as e:
        print(f"Error extracting name from request: {e}")
    return None

def main():
    print("🔍 FINDING MISSING ITINERARY ENTRY")
    print("=" * 50)
    
    # Load Postman collection
    print("📄 Loading Postman collection...")
    with open('postman-collection/Strapi_Itineraries_Collection_Fixed.postman_collection.json', 'r') as f:
        postman_data = json.load(f)
    
    # Load post-migration data
    print("📄 Loading post-migration data...")
    with open('post-migration-check.json', 'r') as f:
        migration_data = json.load(f)
    
    # Extract names from Postman collection
    print("🔍 Extracting names from Postman collection...")
    postman_names = set()
    postman_entries = []
    
    for i, item in enumerate(postman_data['item']):
        name = extract_name_from_postman_request(item)
        if name:
            postman_names.add(name)
            postman_entries.append({
                'index': i,
                'name': name,
                'request_name': item.get('name', f'Request {i+1}')
            })
    
    print(f"Found {len(postman_names)} unique names in Postman collection")
    
    # Extract names from migration data
    print("🔍 Extracting names from migration data...")
    migration_names = set()
    for entry in migration_data['data']:
        if 'Name' in entry:
            migration_names.add(entry['Name'])
    
    print(f"Found {len(migration_names)} unique names in migration data")
    
    # Find missing names
    missing_names = postman_names - migration_names
    extra_names = migration_names - postman_names
    
    print(f"\n📊 COMPARISON RESULTS:")
    print(f"   Postman collection entries: {len(postman_names)}")
    print(f"   Migration data entries: {len(migration_names)}")
    print(f"   Missing from migration: {len(missing_names)}")
    print(f"   Extra in migration: {len(extra_names)}")
    
    # Show missing entries
    if missing_names:
        print(f"\n❌ MISSING ENTRIES ({len(missing_names)}):")
        missing_entries = [entry for entry in postman_entries if entry['name'] in missing_names]
        
        # Sort by index to show in order
        missing_entries.sort(key=lambda x: x['index'])
        
        for i, entry in enumerate(missing_entries[:20], 1):  # Show first 20
            print(f"  {i}. Index {entry['index']}: {entry['name']}")
            print(f"     Request: {entry['request_name']}")
        
        if len(missing_entries) > 20:
            print(f"     ... and {len(missing_entries) - 20} more missing entries")
        
        # Find the specific missing entry by index
        print(f"\n🔍 DETAILED ANALYSIS:")
        print(f"   First missing entry index: {missing_entries[0]['index']}")
        print(f"   Last missing entry index: {missing_entries[-1]['index']}")
        
        # Check if there's a pattern in missing entries
        missing_indices = [entry['index'] for entry in missing_entries]
        missing_indices.sort()
        
        print(f"\n📈 MISSING INDICES PATTERN:")
        print(f"   Missing indices: {missing_indices[:10]}{'...' if len(missing_indices) > 10 else ''}")
        
        # Check for consecutive missing entries
        consecutive_gaps = []
        for i in range(len(missing_indices) - 1):
            if missing_indices[i+1] - missing_indices[i] > 1:
                consecutive_gaps.append((missing_indices[i], missing_indices[i+1]))
        
        if consecutive_gaps:
            print(f"   Gaps in sequence: {consecutive_gaps[:5]}")
        else:
            print(f"   All missing entries are consecutive")
    
    # Show extra entries (if any)
    if extra_names:
        print(f"\n➕ EXTRA ENTRIES IN MIGRATION DATA ({len(extra_names)}):")
        for i, name in enumerate(sorted(extra_names)[:10], 1):
            print(f"  {i}. {name}")
        if len(extra_names) > 10:
            print(f"     ... and {len(extra_names) - 10} more")
    
    # Summary
    total_expected = len(postman_names)
    total_found = len(postman_names) - len(missing_names)
    success_rate = (total_found / total_expected * 100) if total_expected > 0 else 0
    
    print(f"\n📈 SUMMARY:")
    print(f"   Expected entries: {total_expected}")
    print(f"   Successfully uploaded: {total_found}")
    print(f"   Missing entries: {len(missing_names)}")
    print(f"   Success rate: {success_rate:.1f}%")
    
    if len(missing_names) == 1:
        print(f"\n🎯 SINGLE MISSING ENTRY IDENTIFIED:")
        missing_entry = missing_entries[0]
        print(f"   Name: {missing_entry['name']}")
        print(f"   Index: {missing_entry['index']}")
        print(f"   Request: {missing_entry['request_name']}")
    elif len(missing_names) > 1:
        print(f"\n⚠️  MULTIPLE MISSING ENTRIES: {len(missing_names)}")
        print(f"   This suggests a systematic issue with the upload process")

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Analyze which entries from the Postman collection failed to upload to Strapi.
"""

import json

def extract_name_from_postman_request(request):
    """Extract the Name field from a Postman request body."""
    try:
        if 'request' in request and 'body' in request['request']:
            body = request['request']['body']
            if 'raw' in body:
                raw_data = body['raw']
                data = json.loads(raw_data)
                if 'data' in data and 'Name' in data['data']:
                    return data['data']['Name']
    except Exception as e:
        print(f"Error extracting name from request: {e}")
    return None

def main():
    print("🔍 ANALYZING UPLOAD FAILURES")
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
    postman_entries = []
    
    for i, item in enumerate(postman_data['item']):
        name = extract_name_from_postman_request(item)
        if name:
            postman_entries.append({
                'index': i,
                'name': name,
                'request_name': item.get('name', f'Request {i+1}')
            })
    
    print(f"Found {len(postman_entries)} entries in Postman collection")
    
    # Extract names from migration data
    print("🔍 Extracting names from migration data...")
    migration_names = set()
    migration_entries = []
    
    for entry in migration_data['data']:
        if 'Name' in entry:
            migration_names.add(entry['Name'])
            migration_entries.append({
                'id': entry.get('id'),
                'name': entry['Name'],
                'slug': entry.get('Slug', ''),
                'createdAt': entry.get('createdAt', '')
            })
    
    print(f"Found {len(migration_names)} entries in migration data")
    
    # Find successful and failed uploads
    successful_uploads = []
    failed_uploads = []
    
    for entry in postman_entries:
        if entry['name'] in migration_names:
            successful_uploads.append(entry)
        else:
            failed_uploads.append(entry)
    
    print(f"\n📊 UPLOAD ANALYSIS:")
    print(f"   Total entries in Postman: {len(postman_entries)}")
    print(f"   Successfully uploaded: {len(successful_uploads)}")
    print(f"   Failed uploads: {len(failed_uploads)}")
    print(f"   Success rate: {len(successful_uploads)/len(postman_entries)*100:.1f}%")
    
    # Show successful uploads
    print(f"\n✅ SUCCESSFUL UPLOADS ({len(successful_uploads)}):")
    for i, entry in enumerate(successful_uploads, 1):
        print(f"  {i:2d}. Index {entry['index']:3d}: {entry['name']}")
    
    # Show failed uploads (first 20)
    print(f"\n❌ FAILED UPLOADS (showing first 20 of {len(failed_uploads)}):")
    for i, entry in enumerate(failed_uploads[:20], 1):
        print(f"  {i:2d}. Index {entry['index']:3d}: {entry['name']}")
    
    if len(failed_uploads) > 20:
        print(f"     ... and {len(failed_uploads) - 20} more failed uploads")
    
    # Analyze failure pattern
    print(f"\n🔍 FAILURE PATTERN ANALYSIS:")
    failed_indices = [entry['index'] for entry in failed_uploads]
    failed_indices.sort()
    
    # Check for consecutive failures
    consecutive_failures = []
    current_start = failed_indices[0] if failed_indices else 0
    current_end = current_start
    
    for i in range(1, len(failed_indices)):
        if failed_indices[i] == failed_indices[i-1] + 1:
            current_end = failed_indices[i]
        else:
            if current_end > current_start:
                consecutive_failures.append((current_start, current_end))
            current_start = failed_indices[i]
            current_end = current_start
    
    if current_end > current_start:
        consecutive_failures.append((current_start, current_end))
    
    print(f"   Consecutive failure ranges: {consecutive_failures[:10]}")
    if len(consecutive_failures) > 10:
        print(f"   ... and {len(consecutive_failures) - 10} more ranges")
    
    # Check if failures start from a specific point
    if failed_indices:
        print(f"   First failure at index: {failed_indices[0]}")
        print(f"   Last failure at index: {failed_indices[-1]}")
        
        # Check if all failures are after a certain point
        successful_indices = [entry['index'] for entry in successful_uploads]
        if successful_indices:
            max_successful_index = max(successful_indices)
            failures_after_success = [idx for idx in failed_indices if idx > max_successful_index]
            print(f"   Failures after last successful upload: {len(failures_after_success)}")
    
    # Summary recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if len(failed_uploads) > len(successful_uploads):
        print(f"   ⚠️  Most uploads failed - check Strapi logs for errors")
        print(f"   🔄 Consider re-running the upload process")
        print(f"   📝 Check for API rate limits or authentication issues")
    else:
        print(f"   ✅ Most uploads succeeded")
        print(f"   🔄 Re-upload only the failed entries")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"   1. Check Strapi admin panel for error logs")
    print(f"   2. Verify API authentication and permissions")
    print(f"   3. Check for rate limiting issues")
    print(f"   4. Re-run upload for failed entries only")

if __name__ == "__main__":
    main()






#!/usr/bin/env python3
"""
Script to create a Postman collection with the first 5 itinerary entries using fixed format.
"""

import json

def create_sample_collection():
    # Load the fixed request bodies
    with open('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/postman-collection/full_request_bodies_fixed.json', 'r', encoding='utf-8') as f:
        all_requests = json.load(f)
    
    # Take only the first 5 entries
    sample_requests = all_requests[:5]
    
    # Create Postman collection structure
    postman_collection = {
        "info": {
            "name": "Strapi Itineraries Collection - Sample 5 Entries (Fixed)",
            "description": "Sample collection with first 5 itineraries using correct block format for rich text fields",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": sample_requests
    }
    
    # Save the sample collection
    output_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/postman-collection/Strapi_Itineraries_Sample_5_Collection_Fixed.postman_collection.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(postman_collection, f, indent=2, ensure_ascii=False)
    
    print(f"Fixed sample collection created with {len(sample_requests)} entries")
    print(f"Saved to: {output_file}")
    
    # Print the names of the 5 entries
    print("\nEntries included:")
    for i, request in enumerate(sample_requests, 1):
        print(f"{i}. {request['name']}")

if __name__ == "__main__":
    create_sample_collection()

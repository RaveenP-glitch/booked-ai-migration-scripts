#!/usr/bin/env python3
"""
Script to map image URLs from CSV to image IDs from all-images-without-iti.json
"""

import json
import csv
import re
from urllib.parse import urlparse
import os

def extract_filename_from_url(url):
    """Extract filename from URL."""
    if not url or url.strip() == '':
        return None
    
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If no filename in path, create one from the URL
    if not filename or '.' not in filename:
        # Use the last part of the path or a hash of the URL
        path_parts = parsed_url.path.strip('/').split('/')
        if path_parts and path_parts[-1]:
            filename = path_parts[-1] + '.jpg'  # Default to jpg
        else:
            filename = f"image_{hash(url) % 10000}.jpg"
    
    return filename

def normalize_filename(filename):
    """Normalize filename for comparison by removing extensions and converting to lowercase."""
    if not filename:
        return None
    # Remove extension
    name_without_ext = os.path.splitext(filename)[0]
    # Convert to lowercase for case-insensitive comparison
    return name_without_ext.lower()

def find_image_id_by_url(image_url, image_data):
    """
    Find image ID by matching URL with uploaded images.
    Returns the image ID if found, None otherwise.
    """
    if not image_url or image_url.strip() == '':
        return None
    
    # Extract filename from URL
    url_filename = extract_filename_from_url(image_url)
    if not url_filename:
        return None
    
    url_normalized = normalize_filename(url_filename)
    
    # Search through uploaded images
    for img in image_data:
        if 'name' in img:
            uploaded_name = img['name']
            uploaded_normalized = normalize_filename(uploaded_name)
            
            # Check for exact match
            if url_normalized == uploaded_normalized:
                return img.get('id')
            
            # Check if URL filename is contained in uploaded name
            if url_normalized and uploaded_normalized and url_normalized in uploaded_normalized:
                return img.get('id')
            
            # Check if uploaded name is contained in URL filename
            if url_normalized and uploaded_normalized and uploaded_normalized in url_normalized:
                return img.get('id')
    
    return None

def main():
    # Paths
    csv_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/Booked (Live) - Itineraries.csv'
    json_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/all-images-without-iti.json'
    output_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/postman-collection/image_mapping.json'
    
    print("Loading image data from JSON...")
    
    # Load uploaded images from JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            image_data = json.load(f)
        print(f"Loaded {len(image_data)} uploaded images from JSON file")
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return
    
    print("Processing CSV file...")
    
    # Process CSV and create image mapping
    image_mapping = {}
    processed_count = 0
    found_count = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                processed_count += 1
                
                # Get image URLs from the row
                thumbnail_url = row.get('Thumbnail Image', '').strip()
                main_image_url = row.get('Main Image', '').strip()
                itinerary_image_url = row.get('Itinerary Image', '').strip()
                
                # Create mapping for this row
                row_mapping = {
                    'thumbnail_id': None,
                    'main_image_id': None,
                    'itinerary_image_id': None
                }
                
                # Map thumbnail image
                if thumbnail_url:
                    thumbnail_id = find_image_id_by_url(thumbnail_url, image_data)
                    if thumbnail_id:
                        row_mapping['thumbnail_id'] = thumbnail_id
                        found_count += 1
                
                # Map main image
                if main_image_url:
                    main_image_id = find_image_id_by_url(main_image_url, image_data)
                    if main_image_id:
                        row_mapping['main_image_id'] = main_image_id
                        found_count += 1
                
                # Map itinerary image
                if itinerary_image_url:
                    itinerary_image_id = find_image_id_by_url(itinerary_image_url, image_data)
                    if itinerary_image_id:
                        row_mapping['itinerary_image_id'] = itinerary_image_id
                        found_count += 1
                
                # Store mapping using row number as key
                image_mapping[processed_count] = row_mapping
                
                # Progress indicator
                if processed_count % 100 == 0:
                    print(f"Processed {processed_count} rows, found {found_count} image matches")
    
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return
    
    # Save mapping to JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(image_mapping, f, indent=2, ensure_ascii=False)
        print(f"Image mapping saved to: {output_file}")
    except Exception as e:
        print(f"Error saving mapping file: {e}")
        return
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"IMAGE MAPPING COMPLETED!")
    print(f"Total rows processed: {processed_count}")
    print(f"Total image matches found: {found_count}")
    print(f"Mapping file: {output_file}")
    
    # Show some sample mappings
    print(f"\nSample mappings (first 5 rows):")
    for i in range(1, min(6, processed_count + 1)):
        mapping = image_mapping.get(i, {})
        print(f"Row {i}: Thumbnail={mapping.get('thumbnail_id')}, Main={mapping.get('main_image_id')}, Itinerary={mapping.get('itinerary_image_id')}")

if __name__ == "__main__":
    main()

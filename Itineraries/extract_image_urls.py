#!/usr/bin/env python3
"""
Script to extract all image URLs from the Itineraries CSV file.
This script will scan through all columns and rows to find any URLs 
that point to images (cdn.prod.website-files.com or other image hosting services).
"""

import csv
import re
import os
from urllib.parse import urlparse

def is_image_url(url):
    """Check if a URL points to an image file."""
    if not url or not isinstance(url, str):
        return False
    
    # Check for common image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.tiff']
    parsed_url = urlparse(url.lower())
    
    # Check if URL ends with image extension
    for ext in image_extensions:
        if parsed_url.path.endswith(ext):
            return True
    
    # Check for cdn.prod.website-files.com (Webflow CDN)
    if 'cdn.prod.website-files.com' in url:
        return True
    
    return False

def extract_urls_from_text(text):
    """Extract URLs from text content, including HTML."""
    if not text or not isinstance(text, str):
        return []
    
    # Pattern to match URLs
    url_pattern = r'https?://[^\s<>"\']+(?:[^\s<>"\'.,;!?])'
    urls = re.findall(url_pattern, text)
    
    # Filter for image URLs only
    image_urls = [url for url in urls if is_image_url(url)]
    
    return image_urls

def main():
    csv_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/Booked (Live) - Itineraries.csv'
    output_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/all_image_urls.txt'
    
    print("Starting image URL extraction from Itineraries CSV...")
    
    all_image_urls = set()  # Use set to avoid duplicates
    row_count = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            # Use csv.reader to properly handle CSV format
            csv_reader = csv.reader(file)
            
            # Skip header row
            headers = next(csv_reader)
            print(f"CSV Headers: {headers[:5]}...")  # Show first 5 headers
            
            for row in csv_reader:
                row_count += 1
                
                # Process each cell in the row
                for cell_index, cell in enumerate(row):
                    if cell:  # Skip empty cells
                        # Extract URLs from this cell
                        urls = extract_urls_from_text(cell)
                        all_image_urls.update(urls)
                
                # Progress indicator
                if row_count % 1000 == 0:
                    print(f"Processed {row_count} rows, found {len(all_image_urls)} unique image URLs so far...")
    
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    print(f"\nCompleted processing {row_count} rows")
    print(f"Found {len(all_image_urls)} unique image URLs")
    
    # Sort URLs for better organization
    sorted_urls = sorted(list(all_image_urls))
    
    # Write URLs to file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for url in sorted_urls:
                file.write(url + '\n')
        
        print(f"Image URLs saved to: {output_file}")
        
        # Show some statistics
        cdn_urls = [url for url in sorted_urls if 'cdn.prod.website-files.com' in url]
        print(f"URLs from cdn.prod.website-files.com: {len(cdn_urls)}")
        
        # Show first few URLs as examples
        print("\nFirst 10 URLs found:")
        for i, url in enumerate(sorted_urls[:10]):
            print(f"{i+1}. {url}")
        
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    main()

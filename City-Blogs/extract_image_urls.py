#!/usr/bin/env python3
"""
Script to extract all image URLs from the City-Blogs CSV file.
"""

import csv
import re
import json

def extract_image_urls_from_csv(csv_file):
    """Extract all image URLs from the CSV file."""
    image_urls = set()  # Use set to avoid duplicates
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+\.(?:jpg|jpeg|png|gif|webp|svg)(?:\?[^\s<>"{}|\\^`\[\]]*)?'
    
    print("🔍 Extracting image URLs from CSV...")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        total_rows = 0
        
        for row in reader:
            total_rows += 1
            if total_rows % 10000 == 0:
                print(f"Processed {total_rows:,} rows...")
            
            # Check all columns for image URLs
            for column_name, cell_value in row.items():
                if cell_value and isinstance(cell_value, str):
                    # Find all image URLs in this cell
                    urls = re.findall(url_pattern, cell_value, re.IGNORECASE)
                    for url in urls:
                        # Clean up the URL
                        url = url.strip()
                        if url and url not in image_urls:
                            image_urls.add(url)
    
    print(f"✅ Processed {total_rows:,} rows")
    print(f"📸 Found {len(image_urls):,} unique image URLs")
    
    return sorted(list(image_urls))

def main():
    csv_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/City-Blogs/Booked (Live) - City Blogs all.csv'
    
    # Extract image URLs
    image_urls = extract_image_urls_from_csv(csv_file)
    
    # Save to text file
    output_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/City-Blogs/all_image_urls.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for url in image_urls:
            f.write(url + '\n')
    
    print(f"💾 Saved {len(image_urls):,} image URLs to: {output_file}")
    
    # Show some sample URLs
    print("\n📋 Sample URLs:")
    for i, url in enumerate(image_urls[:10]):
        print(f"{i+1:2d}. {url}")
    
    if len(image_urls) > 10:
        print(f"    ... and {len(image_urls) - 10:,} more")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Extract all unique image URLs from Hotels CSV file
"""

import csv
import re
from pathlib import Path

def extract_image_urls(csv_file_path, output_file_path):
    """
    Extract all unique image URLs from the Hotels CSV file
    
    Args:
        csv_file_path: Path to the CSV file
        output_file_path: Path to output txt file
    """
    unique_urls = set()
    
    # URL pattern to match - looking for https URLs
    url_pattern = re.compile(r'https?://[^\s;,]+\.(jpeg|jpg|png|gif|webp|avif|svg)', re.IGNORECASE)
    
    print(f"Reading CSV file: {csv_file_path}")
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        total_rows = 0
        for row in reader:
            total_rows += 1
            
            # Extract from specific image columns
            image_columns = ['Image', 'Photos', 'Photo 1', 'Photo 2', 'Photo 3']
            
            for column in image_columns:
                if column in row and row[column]:
                    content = row[column]
                    
                    # Handle semicolon-separated URLs in Photos column
                    if ';' in content:
                        urls = content.split(';')
                        for url in urls:
                            url = url.strip()
                            if url and url.startswith('http'):
                                unique_urls.add(url)
                    else:
                        # Single URL
                        content = content.strip()
                        if content and content.startswith('http'):
                            unique_urls.add(content)
            
            # Progress indicator
            if total_rows % 1000 == 0:
                print(f"Processed {total_rows} rows... Found {len(unique_urls)} unique URLs so far")
    
    print(f"\nTotal rows processed: {total_rows}")
    print(f"Total unique image URLs found: {len(unique_urls)}")
    
    # Sort URLs for better organization
    sorted_urls = sorted(unique_urls)
    
    # Write to output file
    print(f"\nWriting URLs to: {output_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for url in sorted_urls:
            f.write(url + '\n')
    
    print(f"✓ Successfully extracted {len(sorted_urls)} unique image URLs")
    
    return sorted_urls

if __name__ == "__main__":
    # File paths
    csv_file = Path(__file__).parent / "Booked (Live) - Hotels-3971.csv"
    output_file = Path(__file__).parent / "all_hotel_image_urls.txt"
    
    # Extract URLs
    urls = extract_image_urls(csv_file, output_file)
    
    # Print some sample URLs
    print("\nSample URLs (first 10):")
    for i, url in enumerate(urls[:10], 1):
        print(f"{i}. {url}")



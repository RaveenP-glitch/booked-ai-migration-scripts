#!/usr/bin/env python3
"""
Script to extract all unique image URLs from the Restaurants CSV file
and save them to a text file.
"""

import csv
import re
from urllib.parse import urlparse

def is_valid_url(url):
    """Check if a string is a valid URL"""
    try:
        result = urlparse(url.strip())
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_urls_from_text(text):
    """Extract URLs from text that may contain multiple URLs separated by semicolons"""
    if not text or text.strip() == '':
        return []
    
    # Split by semicolon and clean up each URL
    urls = []
    for url in text.split(';'):
        url = url.strip()
        if url and is_valid_url(url):
            urls.append(url)
    
    return urls

def main():
    csv_file = 'Booked (Live) - Restaurants.csv'
    output_file = 'all_restaurant_image_urls.txt'
    
    # Columns that contain image URLs
    image_columns = [
        'Image',           # Column 11
        'Signature Dish Image',  # Column 37
        'Photos',          # Column 39
        'Photo 1',         # Column 40
        'Photo 2',         # Column 41
        'Photo 3'          # Column 42
    ]
    
    unique_urls = set()
    total_rows = 0
    
    print(f"Reading CSV file: {csv_file}")
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                total_rows += 1
                if total_rows % 1000 == 0:
                    print(f"Processed {total_rows} rows...")
                
                # Extract URLs from each image column
                for column in image_columns:
                    if column in row and row[column]:
                        urls = extract_urls_from_text(row[column])
                        unique_urls.update(urls)
    
    except FileNotFoundError:
        print(f"Error: Could not find file '{csv_file}'")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Convert to sorted list for consistent output
    sorted_urls = sorted(list(unique_urls))
    
    print(f"\nExtraction complete!")
    print(f"Total rows processed: {total_rows}")
    print(f"Unique image URLs found: {len(sorted_urls)}")
    
    # Write URLs to text file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for url in sorted_urls:
                file.write(url + '\n')
        
        print(f"Unique image URLs saved to: {output_file}")
        
        # Show first few URLs as preview
        if sorted_urls:
            print(f"\nFirst 5 URLs (preview):")
            for i, url in enumerate(sorted_urls[:5]):
                print(f"  {i+1}. {url}")
            
            if len(sorted_urls) > 5:
                print(f"  ... and {len(sorted_urls) - 5} more URLs")
    
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    main()

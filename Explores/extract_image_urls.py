#!/usr/bin/env python3
"""
Script to extract all image URLs from the Explores CSV file.
Extracts URLs from both 'Image' and 'Author Pic' columns.
"""

import csv
import re
from urllib.parse import urlparse

def extract_image_urls(csv_file_path):
    """Extract all image URLs from the CSV file."""
    image_urls = set()  # Use set to avoid duplicates
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Extract from 'Image' column
            if 'Image' in row and row['Image']:
                image_url = row['Image'].strip()
                if image_url and is_valid_image_url(image_url):
                    image_urls.add(image_url)
            
            # Extract from 'Author Pic' column
            if 'Author Pic' in row and row['Author Pic']:
                author_pic_url = row['Author Pic'].strip()
                if author_pic_url and is_valid_image_url(author_pic_url):
                    image_urls.add(author_pic_url)
    
    return sorted(list(image_urls))

def is_valid_image_url(url):
    """Check if the URL is a valid image URL."""
    if not url or url.lower() in ['', 'null', 'none']:
        return False
    
    # Check if it's a valid URL
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
    except:
        return False
    
    # Check if it's likely an image URL
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
    url_lower = url.lower()
    
    # Check for image extensions in URL
    if any(ext in url_lower for ext in image_extensions):
        return True
    
    # Check for common image hosting patterns
    if any(domain in url_lower for domain in ['cdn.', 'images.', 'img.', 'static.']):
        return True
    
    return True  # Accept all valid URLs as they might be images

def main():
    csv_file_path = "Booked (Live) - Explores-all.csv"
    output_file = "all_image_urls.txt"
    
    print(f"Extracting image URLs from {csv_file_path}...")
    
    try:
        image_urls = extract_image_urls(csv_file_path)
        
        print(f"Found {len(image_urls)} unique image URLs")
        
        # Write URLs to file
        with open(output_file, 'w', encoding='utf-8') as f:
            for url in image_urls:
                f.write(url + '\n')
        
        print(f"Image URLs saved to {output_file}")
        
        # Display first few URLs as preview
        print("\nFirst 10 URLs:")
        for i, url in enumerate(image_urls[:10]):
            print(f"{i+1}. {url}")
        
        if len(image_urls) > 10:
            print(f"... and {len(image_urls) - 10} more URLs")
            
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


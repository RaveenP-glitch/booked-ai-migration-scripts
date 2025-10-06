#!/usr/bin/env python3
"""
Script to download all images from the extracted URLs.
Downloads images to the assets directory with proper naming and error handling.
"""

import os
import requests
import time
from urllib.parse import urlparse
import sys
from pathlib import Path

def sanitize_filename(filename):
    """Sanitize filename to be safe for filesystem."""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit filename length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    return filename

def get_filename_from_url(url):
    """Extract filename from URL."""
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
    
    return sanitize_filename(filename)

def download_image(url, output_dir, session):
    """Download a single image."""
    try:
        filename = get_filename_from_url(url)
        output_path = os.path.join(output_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(output_path):
            return True, f"Already exists: {filename}"
        
        # Download the image
        response = session.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Check if it's actually an image
        content_type = response.headers.get('content-type', '').lower()
        if not any(img_type in content_type for img_type in ['image/', 'application/octet-stream']):
            return False, f"Not an image: {url} (content-type: {content_type})"
        
        # Write the file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True, f"Downloaded: {filename} ({len(response.content)} bytes)"
        
    except requests.exceptions.RequestException as e:
        return False, f"Request error for {url}: {str(e)}"
    except Exception as e:
        return False, f"Error downloading {url}: {str(e)}"

def main():
    # Paths
    base_dir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries'
    urls_file = os.path.join(base_dir, 'all_image_urls.txt')
    output_dir = os.path.join(base_dir, 'assets')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Read URLs
    try:
        with open(urls_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading URLs file: {e}")
        return
    
    print(f"Starting download of {len(urls)} images...")
    print(f"Output directory: {output_dir}")
    
    # Download statistics
    successful = 0
    failed = 0
    skipped = 0
    
    # Create a session for connection reuse
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Process each URL
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Processing: {url}")
        
        success, message = download_image(url, output_dir, session)
        
        if success:
            if "Already exists" in message:
                skipped += 1
            else:
                successful += 1
            print(f"  ✓ {message}")
        else:
            failed += 1
            print(f"  ✗ {message}")
        
        # Progress update every 50 downloads
        if i % 50 == 0:
            print(f"\nProgress: {i}/{len(urls)} - Success: {successful}, Failed: {failed}, Skipped: {skipped}\n")
        
        # Small delay to be respectful to the server
        time.sleep(0.1)
    
    # Final statistics
    print(f"\n{'='*60}")
    print(f"Download completed!")
    print(f"Total URLs processed: {len(urls)}")
    print(f"Successfully downloaded: {successful}")
    print(f"Already existed (skipped): {skipped}")
    print(f"Failed downloads: {failed}")
    print(f"Output directory: {output_dir}")
    
    # List downloaded files
    downloaded_files = os.listdir(output_dir)
    print(f"Total files in assets directory: {len(downloaded_files)}")
    
    if failed > 0:
        print(f"\nNote: {failed} downloads failed. You may want to retry the script to attempt failed downloads again.")

if __name__ == "__main__":
    main()


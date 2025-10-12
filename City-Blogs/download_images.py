#!/usr/bin/env python3
"""
Script to download all images from the City-Blogs CSV file.
"""

import requests
import os
import re
from urllib.parse import urlparse, unquote
from pathlib import Path
import time

def sanitize_filename(filename):
    """Sanitize filename to be safe for filesystem."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra spaces and dots
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.strip('._')
    # Limit length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    return filename

def get_filename_from_url(url):
    """Extract filename from URL."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # URL decode the filename
    filename = unquote(filename)
    
    # If no extension, try to get it from the URL
    if '.' not in filename:
        if 'jpg' in url.lower() or 'jpeg' in url.lower():
            filename += '.jpg'
        elif 'png' in url.lower():
            filename += '.png'
        elif 'gif' in url.lower():
            filename += '.gif'
        elif 'webp' in url.lower():
            filename += '.webp'
        elif 'svg' in url.lower():
            filename += '.svg'
        else:
            filename += '.jpg'  # Default to jpg
    
    return sanitize_filename(filename)

def download_image(url, output_dir, session):
    """Download a single image."""
    try:
        response = session.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Get filename
        filename = get_filename_from_url(url)
        
        # Ensure unique filename
        output_path = output_dir / filename
        counter = 1
        while output_path.exists():
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{counter}{ext}"
            output_path = output_dir / new_filename
            counter += 1
        
        # Download and save
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return True, str(output_path)
    
    except Exception as e:
        return False, str(e)

def main():
    # Create assets directory
    assets_dir = Path('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/City-Blogs/assets')
    assets_dir.mkdir(exist_ok=True)
    
    # Read image URLs
    urls_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/City-Blogs/all_image_urls.txt'
    
    print("📖 Reading image URLs...")
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"📸 Found {len(urls):,} image URLs to download")
    print(f"📁 Downloading to: {assets_dir}")
    
    # Create session for connection pooling
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Download images
    successful = 0
    failed = 0
    failed_urls = []
    
    for i, url in enumerate(urls, 1):
        if i % 100 == 0:
            print(f"Progress: {i:,}/{len(urls):,} ({i/len(urls)*100:.1f}%) - Success: {successful:,}, Failed: {failed:,}")
        
        success, result = download_image(url, assets_dir, session)
        
        if success:
            successful += 1
        else:
            failed += 1
            failed_urls.append((url, result))
            if failed <= 10:  # Show first 10 errors
                print(f"Error downloading {url}: {result}")
        
        # Small delay to be respectful
        time.sleep(0.1)
    
    # Final statistics
    print(f"\n✅ Download complete!")
    print(f"📊 Statistics:")
    print(f"   Total URLs: {len(urls):,}")
    print(f"   Successful: {successful:,}")
    print(f"   Failed: {failed:,}")
    print(f"   Success rate: {successful/len(urls)*100:.1f}%")
    
    # Save failed URLs for retry
    if failed_urls:
        failed_file = assets_dir / 'failed_downloads.txt'
        with open(failed_file, 'w', encoding='utf-8') as f:
            for url, error in failed_urls:
                f.write(f"{url}\t{error}\n")
        print(f"💾 Failed URLs saved to: {failed_file}")
    
    # Count downloaded files
    downloaded_files = list(assets_dir.glob('*'))
    image_files = [f for f in downloaded_files if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']]
    print(f"📁 Files in assets directory: {len(image_files):,}")

if __name__ == "__main__":
    main()





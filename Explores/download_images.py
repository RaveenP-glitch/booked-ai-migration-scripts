#!/usr/bin/env python3
"""
Script to download all images from the URLs list to the assets folder.
Handles duplicate filenames, creates proper directory structure, and provides progress tracking.
"""

import os
import requests
import time
from urllib.parse import urlparse, unquote
from pathlib import Path
import hashlib
import re

def sanitize_filename(filename):
    """Sanitize filename to be filesystem-safe."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra spaces and dots
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.strip('._')
    return filename

def get_file_extension(url):
    """Extract file extension from URL."""
    parsed = urlparse(url)
    path = unquote(parsed.path)
    
    # Try to get extension from path
    if '.' in path:
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
            return ext
    
    # Default to .jpg if no extension found
    return '.jpg'

def generate_unique_filename(directory, base_name, extension):
    """Generate a unique filename if the file already exists."""
    counter = 1
    original_name = f"{base_name}{extension}"
    full_path = os.path.join(directory, original_name)
    
    if not os.path.exists(full_path):
        return original_name
    
    while True:
        new_name = f"{base_name}_{counter}{extension}"
        full_path = os.path.join(directory, new_name)
        if not os.path.exists(full_path):
            return new_name
        counter += 1

def download_image(url, output_dir, session):
    """Download a single image from URL."""
    try:
        # Parse URL to get filename
        parsed = urlparse(url)
        path = unquote(parsed.path)
        
        # Extract filename from URL
        if '/' in path:
            filename = os.path.basename(path)
        else:
            # Generate filename from URL hash if no filename in path
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"image_{url_hash}"
        
        # Remove query parameters from filename
        if '?' in filename:
            filename = filename.split('?')[0]
        
        # Get file extension
        extension = get_file_extension(url)
        
        # Remove existing extension from filename if present
        name_without_ext = os.path.splitext(filename)[0]
        filename = sanitize_filename(name_without_ext)
        
        # Generate unique filename
        final_filename = generate_unique_filename(output_dir, filename, extension)
        output_path = os.path.join(output_dir, final_filename)
        
        # Download the image
        response = session.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Check if it's actually an image
        content_type = response.headers.get('content-type', '').lower()
        if not any(img_type in content_type for img_type in ['image/', 'application/octet-stream']):
            print(f"⚠️  Warning: {url} doesn't appear to be an image (content-type: {content_type})")
        
        # Save the image
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True, final_filename, len(response.content)
        
    except requests.exceptions.RequestException as e:
        return False, str(e), 0
    except Exception as e:
        return False, str(e), 0

def main():
    # Configuration
    urls_file = "all_image_urls.txt"
    assets_dir = "assets"
    
    # Create assets directory if it doesn't exist
    os.makedirs(assets_dir, exist_ok=True)
    
    # Read URLs from file
    if not os.path.exists(urls_file):
        print(f"Error: {urls_file} not found!")
        return
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(urls)} URLs to download")
    print(f"Downloading to: {os.path.abspath(assets_dir)}")
    print("-" * 50)
    
    # Statistics
    successful_downloads = 0
    failed_downloads = 0
    total_size = 0
    start_time = time.time()
    
    # Create session for connection reuse
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Download images
    for i, url in enumerate(urls, 1):
        print(f"[{i:4d}/{len(urls)}] Downloading...", end=' ')
        
        success, result, size = download_image(url, assets_dir, session)
        
        if success:
            successful_downloads += 1
            total_size += size
            size_mb = size / (1024 * 1024)
            print(f"✅ {result} ({size_mb:.2f} MB)")
        else:
            failed_downloads += 1
            print(f"❌ Failed: {result}")
        
        # Add small delay to be respectful to the server
        time.sleep(0.1)
        
        # Progress update every 50 downloads
        if i % 50 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed
            eta = (len(urls) - i) / rate if rate > 0 else 0
            print(f"Progress: {i}/{len(urls)} ({i/len(urls)*100:.1f}%) - ETA: {eta/60:.1f} min")
    
    # Final statistics
    elapsed_time = time.time() - start_time
    total_size_mb = total_size / (1024 * 1024)
    
    print("\n" + "=" * 50)
    print("DOWNLOAD COMPLETE")
    print("=" * 50)
    print(f"Total URLs processed: {len(urls)}")
    print(f"Successful downloads: {successful_downloads}")
    print(f"Failed downloads: {failed_downloads}")
    print(f"Total size downloaded: {total_size_mb:.2f} MB")
    print(f"Time elapsed: {elapsed_time/60:.1f} minutes")
    print(f"Average speed: {len(urls)/elapsed_time:.1f} downloads/second")
    print(f"Files saved to: {os.path.abspath(assets_dir)}")
    
    if failed_downloads > 0:
        print(f"\n⚠️  {failed_downloads} downloads failed. Check the output above for details.")
    
    session.close()

if __name__ == "__main__":
    main()


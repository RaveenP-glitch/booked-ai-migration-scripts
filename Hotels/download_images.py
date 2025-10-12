#!/usr/bin/env python3
"""
Download all hotel images from URLs and save to assets directory
"""

import os
import sys
import requests
import time
from pathlib import Path
from urllib.parse import urlparse

def extract_filename_from_url(url):
    """
    Extract the unique filename part from CDN URL
    Example: https://cdn.prod.website-files.com/6613f5a399757c17cec4c187/67f87803cffc66b2f44b732f_photo.jpeg
    Returns: 6613f5a399757c17cec4c187/67f87803cffc66b2f44b732f_photo.jpeg
    """
    # Parse the URL and get the path
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    
    # Get the last two parts (directory/filename)
    if len(path_parts) >= 2:
        return f"{path_parts[-2]}/{path_parts[-1]}"
    else:
        # Fallback to just the filename
        return path_parts[-1]

def download_image(url, output_path, retry_count=3):
    """
    Download an image from URL and save to output_path
    
    Args:
        url: Image URL
        output_path: Path to save the image
        retry_count: Number of retries on failure
    
    Returns:
        bool: True if successful, False otherwise
    """
    for attempt in range(retry_count):
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write image data
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
            
        except requests.exceptions.RequestException as e:
            if attempt < retry_count - 1:
                time.sleep(1)  # Wait before retry
                continue
            else:
                print(f"  ✗ Failed after {retry_count} attempts: {e}")
                return False
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
    
    return False

def download_all_images(url_file, assets_dir):
    """
    Download all images from URL file
    
    Args:
        url_file: Path to file containing URLs
        assets_dir: Directory to save images
    """
    # Read all URLs
    print(f"Reading URLs from: {url_file}")
    with open(url_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    total_urls = len(urls)
    print(f"Found {total_urls} URLs to download\n")
    
    # Create assets directory
    assets_path = Path(assets_dir)
    assets_path.mkdir(exist_ok=True)
    
    # Statistics
    successful = 0
    failed = 0
    skipped = 0
    failed_urls = []
    
    # Download each image
    for i, url in enumerate(urls, 1):
        # Extract filename
        relative_path = extract_filename_from_url(url)
        output_path = assets_path / relative_path
        
        # Skip if already downloaded
        if output_path.exists():
            skipped += 1
            if i % 100 == 0:
                print(f"[{i}/{total_urls}] Skipped (already exists): {relative_path}")
            continue
        
        # Download
        print(f"[{i}/{total_urls}] Downloading: {relative_path}")
        
        if download_image(url, output_path):
            successful += 1
        else:
            failed += 1
            failed_urls.append((url, relative_path))
        
        # Small delay to be nice to the server
        if i % 10 == 0:
            time.sleep(0.1)
        
        # Progress update every 100 images
        if i % 100 == 0:
            print(f"  Progress: {successful} successful, {failed} failed, {skipped} skipped")
    
    # Final summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"Total URLs:        {total_urls}")
    print(f"Successfully downloaded: {successful}")
    print(f"Already existed (skipped): {skipped}")
    print(f"Failed:            {failed}")
    print("="*60)
    
    # Save failed URLs to file
    if failed_urls:
        failed_file = Path(assets_dir).parent / "failed_downloads.txt"
        print(f"\nSaving failed URLs to: {failed_file}")
        with open(failed_file, 'w', encoding='utf-8') as f:
            for url, path in failed_urls:
                f.write(f"{url}\t{path}\n")
        print(f"✓ Failed URLs saved")
    
    print(f"\n✓ Images saved to: {assets_path.absolute()}")
    
    return successful, failed, skipped

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library is not installed")
        print("Please install it by running: pip3 install requests")
        sys.exit(1)
    
    # File paths
    script_dir = Path(__file__).parent
    url_file = script_dir / "all_hotel_image_urls.txt"
    assets_dir = script_dir / "assets"
    
    # Check if URL file exists
    if not url_file.exists():
        print(f"Error: URL file not found: {url_file}")
        sys.exit(1)
    
    print("="*60)
    print("HOTEL IMAGES DOWNLOADER")
    print("="*60)
    print(f"URL file: {url_file}")
    print(f"Assets directory: {assets_dir}")
    print("="*60 + "\n")
    
    # Download images
    successful, failed, skipped = download_all_images(url_file, assets_dir)
    
    # Exit with appropriate code
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)



#!/usr/bin/env python3
"""
Multithreaded script to download all restaurant images from URLs in the text file
to the Restaurants/assets folder, keeping only the last part of the filename.
"""

import os
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import time
from pathlib import Path
import sys

class ImageDownloader:
    def __init__(self, urls_file, output_dir, max_workers=10):
        self.urls_file = urls_file
        self.output_dir = Path(output_dir)
        self.max_workers = max_workers
        self.downloaded_count = 0
        self.failed_count = 0
        self.total_size = 0
        self.file_sizes = []
        self.lock = threading.Lock()
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_filename(self, url):
        """Extract the last part of the URL path as filename"""
        try:
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            if len(path_parts) >= 2:
                # Take the last part (filename) from the path
                filename = path_parts[-1]
                return filename
            else:
                # Fallback: use the entire path
                return parsed_url.path.split('/')[-1] or 'unknown_image'
        except Exception as e:
            print(f"Error extracting filename from {url}: {e}")
            return 'unknown_image'
    
    def download_image(self, url):
        """Download a single image"""
        try:
            filename = self.extract_filename(url)
            filepath = self.output_dir / filename
            
            # Skip if file already exists
            if filepath.exists():
                with self.lock:
                    self.downloaded_count += 1
                    file_size = filepath.stat().st_size
                    self.total_size += file_size
                    self.file_sizes.append(file_size)
                return {'status': 'skipped', 'url': url, 'filename': filename, 'size': file_size}
            
            # Download the image
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save the image
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = filepath.stat().st_size
            
            with self.lock:
                self.downloaded_count += 1
                self.total_size += file_size
                self.file_sizes.append(file_size)
            
            return {'status': 'success', 'url': url, 'filename': filename, 'size': file_size}
            
        except Exception as e:
            with self.lock:
                self.failed_count += 1
            return {'status': 'failed', 'url': url, 'error': str(e)}
    
    def load_urls(self):
        """Load URLs from the text file"""
        urls = []
        try:
            with open(self.urls_file, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    if url:
                        urls.append(url)
            return urls
        except Exception as e:
            print(f"Error loading URLs from {self.urls_file}: {e}")
            return []
    
    def print_progress(self, current, total):
        """Print download progress"""
        percentage = (current / total) * 100
        print(f"\rProgress: {current}/{total} ({percentage:.1f}%) - Downloaded: {self.downloaded_count}, Failed: {self.failed_count}", end='', flush=True)
    
    def download_all(self):
        """Download all images using multithreading"""
        print(f"Loading URLs from {self.urls_file}...")
        urls = self.load_urls()
        
        if not urls:
            print("No URLs found to download.")
            return
        
        print(f"Found {len(urls)} URLs to download")
        print(f"Output directory: {self.output_dir}")
        print(f"Using {self.max_workers} threads")
        print("Starting downloads...\n")
        
        start_time = time.time()
        completed = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all download tasks
            future_to_url = {executor.submit(self.download_image, url): url for url in urls}
            
            # Process completed downloads
            for future in as_completed(future_to_url):
                completed += 1
                result = future.result()
                
                # Print progress every 100 downloads
                if completed % 100 == 0 or completed == len(urls):
                    self.print_progress(completed, len(urls))
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n\nDownload completed!")
        print(f"Total time: {duration:.2f} seconds")
        print(f"Successfully downloaded: {self.downloaded_count} images")
        print(f"Failed downloads: {self.failed_count} images")
        print(f"Total size: {self.total_size / (1024*1024):.2f} MB")
        
        return self.downloaded_count, self.failed_count, self.total_size, self.file_sizes

def analyze_file_sizes(file_sizes):
    """Analyze and display file size distribution"""
    if not file_sizes:
        print("No files to analyze.")
        return
    
    file_sizes.sort()
    total_files = len(file_sizes)
    total_size = sum(file_sizes)
    
    # Calculate statistics
    min_size = min(file_sizes)
    max_size = max(file_sizes)
    avg_size = total_size / total_files
    
    # Calculate percentiles
    p25 = file_sizes[int(total_files * 0.25)]
    p50 = file_sizes[int(total_files * 0.50)]  # median
    p75 = file_sizes[int(total_files * 0.75)]
    p90 = file_sizes[int(total_files * 0.90)]
    p95 = file_sizes[int(total_files * 0.95)]
    
    print(f"\n{'='*60}")
    print(f"FILE SIZE DISTRIBUTION ANALYSIS")
    print(f"{'='*60}")
    print(f"Total files: {total_files:,}")
    print(f"Total size: {total_size / (1024*1024):.2f} MB")
    print(f"Average size: {avg_size / 1024:.2f} KB")
    print(f"")
    print(f"Size Statistics:")
    print(f"  Minimum: {min_size / 1024:.2f} KB")
    print(f"  25th percentile: {p25 / 1024:.2f} KB")
    print(f"  50th percentile (median): {p50 / 1024:.2f} KB")
    print(f"  75th percentile: {p75 / 1024:.2f} KB")
    print(f"  90th percentile: {p90 / 1024:.2f} KB")
    print(f"  95th percentile: {p95 / 1024:.2f} KB")
    print(f"  Maximum: {max_size / 1024:.2f} KB")
    
    # Size ranges
    ranges = [
        (0, 50*1024, "0-50 KB"),
        (50*1024, 100*1024, "50-100 KB"),
        (100*1024, 500*1024, "100-500 KB"),
        (500*1024, 1024*1024, "500 KB-1 MB"),
        (1024*1024, 5*1024*1024, "1-5 MB"),
        (5*1024*1024, float('inf'), "5+ MB")
    ]
    
    print(f"\nSize Distribution:")
    for min_range, max_range, label in ranges:
        count = sum(1 for size in file_sizes if min_range <= size < max_range)
        percentage = (count / total_files) * 100
        print(f"  {label:12}: {count:6,} files ({percentage:5.1f}%)")

def verify_download_count(assets_dir):
    """Verify the actual number of files downloaded"""
    assets_path = Path(assets_dir)
    if not assets_path.exists():
        return 0
    
    # Count image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.avif'}
    image_files = []
    
    for file_path in assets_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    return len(image_files)

def main():
    # Configuration
    urls_file = 'all_restaurant_image_urls.txt'
    output_dir = 'assets'
    max_workers = 15  # Adjust based on your system and network
    
    print(f"Restaurant Image Downloader")
    print(f"{'='*50}")
    
    # Check if URLs file exists
    if not os.path.exists(urls_file):
        print(f"Error: URLs file '{urls_file}' not found!")
        sys.exit(1)
    
    # Create downloader and start downloading
    downloader = ImageDownloader(urls_file, output_dir, max_workers)
    downloaded_count, failed_count, total_size, file_sizes = downloader.download_all()
    
    # Verify download count
    print(f"\n{'='*50}")
    print(f"VERIFICATION")
    print(f"{'='*50}")
    actual_count = verify_download_count(output_dir)
    print(f"Expected downloads: {downloaded_count}")
    print(f"Actual files in assets folder: {actual_count}")
    
    if actual_count == downloaded_count:
        print("✅ Download count verification: PASSED")
    else:
        print("⚠️  Download count verification: MISMATCH")
    
    # Analyze file sizes
    analyze_file_sizes(file_sizes)

if __name__ == "__main__":
    main()




#!/usr/bin/env python3
"""
Multithreaded image downloader for Attractions images
Downloads images from URLs and saves to assets/download directory with progress tracking
"""

import os
import sys
import requests
import time
import threading
from pathlib import Path
from urllib.parse import urlparse
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
MAX_WORKERS = 10  # Number of concurrent download threads
RETRY_COUNT = 3
TIMEOUT = 30
CHUNK_SIZE = 8192

# Thread-safe counters
class DownloadStats:
    def __init__(self):
        self.lock = threading.Lock()
        self.successful = 0
        self.failed = 0
        self.skipped = 0
        self.failed_urls = []
    
    def add_success(self):
        with self.lock:
            self.successful += 1
    
    def add_failure(self, url, path):
        with self.lock:
            self.failed += 1
            self.failed_urls.append((url, path))
    
    def add_skip(self):
        with self.lock:
            self.skipped += 1
    
    def get_stats(self):
        with self.lock:
            return self.successful, self.failed, self.skipped, self.failed_urls.copy()

def extract_filename_from_url(url):
    """
    Extract the unique filename part from CDN URL
    Example: https://cdn.prod.website-files.com/6613f5a399757c17cec4c187/67f87803cffc66b2f44b732f_photo.jpeg
    Returns: 6613f5a399757c17cec4c187/67f87803cffc66b2f44b732f_photo.jpeg
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    
    # Get the last two parts (directory/filename)
    if len(path_parts) >= 2:
        return f"{path_parts[-2]}/{path_parts[-1]}"
    else:
        # Fallback to just the filename
        return path_parts[-1]

def download_image(url, output_path, retry_count=RETRY_COUNT):
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
            response = requests.get(url, timeout=TIMEOUT, stream=True)
            response.raise_for_status()
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write image data
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            
            return True
            
        except requests.exceptions.RequestException as e:
            if attempt < retry_count - 1:
                time.sleep(1)  # Wait before retry
                continue
            else:
                return False
        except Exception as e:
            return False
    
    return False

def download_worker(task, stats, total_urls):
    """
    Worker function to download a single image
    
    Args:
        task: Tuple of (index, url, output_path)
        stats: DownloadStats object
        total_urls: Total number of URLs
    
    Returns:
        dict: Result information
    """
    index, url, output_path = task
    relative_path = extract_filename_from_url(url)
    
    # Skip if already downloaded
    if output_path.exists():
        stats.add_skip()
        return {
            'index': index,
            'status': 'skipped',
            'path': relative_path
        }
    
    # Download
    success = download_image(url, output_path)
    
    if success:
        stats.add_success()
        return {
            'index': index,
            'status': 'success',
            'path': relative_path
        }
    else:
        stats.add_failure(url, relative_path)
        return {
            'index': index,
            'status': 'failed',
            'path': relative_path
        }

def print_progress(stats, total_urls, start_time):
    """Print current progress"""
    successful, failed, skipped, _ = stats.get_stats()
    completed = successful + failed + skipped
    percentage = (completed / total_urls * 100) if total_urls > 0 else 0
    elapsed = time.time() - start_time
    
    if completed > 0:
        avg_time = elapsed / completed
        remaining = total_urls - completed
        eta = avg_time * remaining
        
        # Format ETA nicely
        if eta > 3600:
            eta_str = f"{int(eta/3600)}h {int((eta%3600)/60)}m"
        elif eta > 60:
            eta_str = f"{int(eta/60)}m {int(eta%60)}s"
        else:
            eta_str = f"{int(eta)}s"
    else:
        eta_str = "calculating..."
    
    print(f"\rProgress: {completed}/{total_urls} ({percentage:.1f}%) | "
          f"✓ {successful} | ✗ {failed} | ⊘ {skipped} | "
          f"ETA: {eta_str}", end='', flush=True)

def download_all_images_multithreaded(url_file, download_dir, max_workers=MAX_WORKERS):
    """
    Download all images from URL file using multithreading
    
    Args:
        url_file: Path to file containing URLs
        download_dir: Directory to save images
        max_workers: Number of concurrent download threads
    """
    # Read all URLs
    print(f"Reading URLs from: {url_file}")
    with open(url_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    total_urls = len(urls)
    print(f"Found {total_urls} URLs to download")
    print(f"Using {max_workers} concurrent threads\n")
    
    # Create download directory
    download_path = Path(download_dir)
    download_path.mkdir(exist_ok=True, parents=True)
    
    # Initialize stats
    stats = DownloadStats()
    
    # Prepare tasks
    tasks = []
    for i, url in enumerate(urls, 1):
        relative_path = extract_filename_from_url(url)
        output_path = download_path / relative_path
        tasks.append((i, url, output_path))
    
    # Download with thread pool
    print("Starting downloads...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {executor.submit(download_worker, task, stats, total_urls): task 
                  for task in tasks}
        
        # Process completed tasks
        for future in as_completed(futures):
            result = future.result()
            
            # Print progress every completion
            print_progress(stats, total_urls, start_time)
    
    print("\n")  # New line after progress
    
    # Final summary
    successful, failed, skipped, failed_urls = stats.get_stats()
    elapsed = time.time() - start_time
    
    print("="*70)
    print("DOWNLOAD SUMMARY")
    print("="*70)
    print(f"Total URLs:              {total_urls}")
    print(f"Successfully downloaded: {successful}")
    print(f"Already existed:         {skipped}")
    print(f"Failed:                  {failed}")
    print(f"Time elapsed:            {elapsed:.2f}s ({elapsed/60:.1f} minutes)")
    if successful > 0:
        print(f"Average speed:           {successful/elapsed:.2f} images/sec")
    print("="*70)
    
    # Save failed URLs to file
    if failed_urls:
        failed_file = Path(download_dir).parent / "failed_downloads.txt"
        print(f"\nSaving {len(failed_urls)} failed URLs to: {failed_file}")
        with open(failed_file, 'w', encoding='utf-8') as f:
            f.write("# Failed downloads - Format: URL<TAB>Path\n")
            for url, path in failed_urls:
                f.write(f"{url}\t{path}\n")
        print(f"✓ Failed URLs saved")
    
    print(f"\n✓ Images saved to: {download_path.absolute()}")
    
    return successful, failed, skipped

def main():
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library is not installed")
        print("Please install it by running: pip3 install requests")
        sys.exit(1)
    
    # File paths
    script_dir = Path(__file__).parent
    url_file = script_dir / "assets" / "all_image_urls.txt"
    download_dir = script_dir / "assets" / "download"
    
    # Check if URL file exists
    if not url_file.exists():
        print(f"Error: URL file not found: {url_file}")
        sys.exit(1)
    
    print("="*70)
    print("ATTRACTIONS IMAGES DOWNLOADER (MULTITHREADED)")
    print("="*70)
    print(f"URL file:         {url_file}")
    print(f"Download directory: {download_dir}")
    print(f"Max workers:      {MAX_WORKERS}")
    print(f"Timeout:          {TIMEOUT}s")
    print(f"Retry count:      {RETRY_COUNT}")
    print("="*70 + "\n")
    
    # Download images
    stats = None
    try:
        successful, failed, skipped = download_all_images_multithreaded(
            url_file, download_dir, max_workers=MAX_WORKERS
        )
        
        # Exit with appropriate code
        if failed > 0:
            print(f"\n⚠ Warning: {failed} downloads failed")
            sys.exit(1)
        else:
            print(f"\n✓ All downloads completed successfully!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠ Download interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()


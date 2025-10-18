#!/usr/bin/env python3
"""
Multithreaded image compression script for Attractions
Compresses images > 400KB losslessly and copies all to compressed-images folder
"""

import os
import sys
import shutil
import time
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

# Configuration
MAX_WORKERS = 8  # Number of concurrent compression threads
SIZE_THRESHOLD_KB = 400
SIZE_THRESHOLD_BYTES = SIZE_THRESHOLD_KB * 1024

# Thread-safe counters
class CompressionStats:
    def __init__(self):
        self.lock = threading.Lock()
        self.compressed = 0
        self.copied = 0
        self.failed = 0
        self.original_size = 0
        self.final_size = 0
        self.failed_files = []
    
    def add_compressed(self, original_size, final_size):
        with self.lock:
            self.compressed += 1
            self.original_size += original_size
            self.final_size += final_size
    
    def add_copied(self, size):
        with self.lock:
            self.copied += 1
            self.original_size += size
            self.final_size += size
    
    def add_failure(self, filepath, error):
        with self.lock:
            self.failed += 1
            self.failed_files.append((filepath, str(error)))
    
    def get_stats(self):
        with self.lock:
            return (self.compressed, self.copied, self.failed, 
                    self.original_size, self.final_size, 
                    self.failed_files.copy())

def format_size(bytes):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def compress_image_lossless(input_path, output_path):
    """
    Compress image losslessly using PIL/Pillow
    
    Args:
        input_path: Source image path
        output_path: Destination image path
    
    Returns:
        tuple: (success: bool, original_size: int, final_size: int)
    """
    try:
        original_size = input_path.stat().st_size
        
        # Open image
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if saving as JPEG
            if img.mode in ('RGBA', 'LA', 'P') and input_path.suffix.lower() in ['.jpg', '.jpeg']:
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Compress based on format
            if input_path.suffix.lower() in ['.jpg', '.jpeg']:
                # JPEG: Use high quality with optimization
                img.save(output_path, 'JPEG', quality=95, optimize=True)
            
            elif input_path.suffix.lower() == '.png':
                # PNG: Use optimization with compression
                img.save(output_path, 'PNG', optimize=True, compress_level=9)
            
            elif input_path.suffix.lower() == '.webp':
                # WebP: Use lossless compression
                img.save(output_path, 'WEBP', lossless=True, quality=100, method=6)
            
            elif input_path.suffix.lower() == '.gif':
                # GIF: Just optimize
                img.save(output_path, 'GIF', optimize=True)
            
            else:
                # Other formats: save with optimization if possible
                img.save(output_path, optimize=True)
        
        final_size = output_path.stat().st_size
        return True, original_size, final_size
        
    except Exception as e:
        return False, 0, 0

def process_image(task, stats, total_files):
    """
    Worker function to process a single image
    
    Args:
        task: Tuple of (index, input_path, output_path, needs_compression)
        stats: CompressionStats object
        total_files: Total number of files
    
    Returns:
        dict: Result information
    """
    index, input_path, output_path, needs_compression = task
    
    try:
        if needs_compression:
            # Compress the image
            success, original_size, final_size = compress_image_lossless(input_path, output_path)
            
            if success:
                stats.add_compressed(original_size, final_size)
                reduction = ((original_size - final_size) / original_size * 100) if original_size > 0 else 0
                return {
                    'index': index,
                    'status': 'compressed',
                    'original_size': original_size,
                    'final_size': final_size,
                    'reduction': reduction,
                    'path': input_path.name
                }
            else:
                stats.add_failure(input_path, "Compression failed")
                return {
                    'index': index,
                    'status': 'failed',
                    'path': input_path.name
                }
        else:
            # Just copy the file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(input_path, output_path)
            file_size = input_path.stat().st_size
            stats.add_copied(file_size)
            
            return {
                'index': index,
                'status': 'copied',
                'size': file_size,
                'path': input_path.name
            }
            
    except Exception as e:
        stats.add_failure(input_path, str(e))
        return {
            'index': index,
            'status': 'failed',
            'path': input_path.name,
            'error': str(e)
        }

def print_progress(stats, total_files, start_time):
    """Print current progress"""
    compressed, copied, failed, original_size, final_size, _ = stats.get_stats()
    completed = compressed + copied + failed
    percentage = (completed / total_files * 100) if total_files > 0 else 0
    elapsed = time.time() - start_time
    
    if completed > 0:
        avg_time = elapsed / completed
        remaining = total_files - completed
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
    
    print(f"\rProgress: {completed}/{total_files} ({percentage:.1f}%) | "
          f"🗜️  {compressed} | 📋 {copied} | ✗ {failed} | "
          f"ETA: {eta_str}", end='', flush=True)

def compress_images_multithreaded(download_dir, output_dir, max_workers=MAX_WORKERS):
    """
    Process all images: compress large ones, copy small ones
    
    Args:
        download_dir: Source directory with images
        output_dir: Destination directory for processed images
        max_workers: Number of concurrent threads
    """
    download_path = Path(download_dir)
    output_path = Path(output_dir)
    
    # Scan for all images
    print("Scanning for images...")
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.bmp'}
    all_images = []
    
    for root, dirs, files in os.walk(download_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in image_extensions:
                file_size = file_path.stat().st_size
                needs_compression = file_size > SIZE_THRESHOLD_BYTES
                
                # Preserve directory structure
                relative_path = file_path.relative_to(download_path)
                output_file_path = output_path / relative_path
                
                all_images.append({
                    'input': file_path,
                    'output': output_file_path,
                    'size': file_size,
                    'needs_compression': needs_compression
                })
    
    total_files = len(all_images)
    large_images = sum(1 for img in all_images if img['needs_compression'])
    small_images = total_files - large_images
    
    print(f"Found {total_files:,} images")
    print(f"  - {large_images:,} images > {SIZE_THRESHOLD_KB}KB (will be compressed)")
    print(f"  - {small_images:,} images ≤ {SIZE_THRESHOLD_KB}KB (will be copied as-is)")
    print(f"Using {max_workers} concurrent threads\n")
    
    # Create output directory
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Initialize stats
    stats = CompressionStats()
    
    # Prepare tasks
    tasks = []
    for i, img_info in enumerate(all_images, 1):
        tasks.append((i, img_info['input'], img_info['output'], img_info['needs_compression']))
    
    # Process with thread pool
    print("Starting processing...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {executor.submit(process_image, task, stats, total_files): task 
                  for task in tasks}
        
        # Process completed tasks
        for future in as_completed(futures):
            result = future.result()
            
            # Print progress
            print_progress(stats, total_files, start_time)
    
    print("\n")  # New line after progress
    
    # Final summary
    compressed, copied, failed, original_size, final_size, failed_files = stats.get_stats()
    elapsed = time.time() - start_time
    
    total_saved = original_size - final_size
    reduction_percent = (total_saved / original_size * 100) if original_size > 0 else 0
    
    print("="*70)
    print("COMPRESSION SUMMARY")
    print("="*70)
    print(f"Total files processed:   {total_files:,}")
    print(f"Compressed:              {compressed:,} images")
    print(f"Copied as-is:            {copied:,} images")
    print(f"Failed:                  {failed:,}")
    print(f"\nOriginal total size:     {format_size(original_size)}")
    print(f"Final total size:        {format_size(final_size)}")
    print(f"Space saved:             {format_size(total_saved)} ({reduction_percent:.1f}% reduction)")
    print(f"\nTime elapsed:            {elapsed:.2f}s ({elapsed/60:.1f} minutes)")
    if compressed > 0:
        print(f"Average speed:           {(compressed+copied)/elapsed:.2f} images/sec")
    print("="*70)
    
    # Save failed files to log
    if failed_files:
        failed_file = output_path.parent / "compression_failures.txt"
        print(f"\n⚠️  Saving {len(failed_files)} failures to: {failed_file}")
        with open(failed_file, 'w', encoding='utf-8') as f:
            f.write("# Compression Failures\n")
            f.write("="*70 + "\n\n")
            for filepath, error in failed_files:
                f.write(f"{filepath}\n  Error: {error}\n\n")
        print(f"✓ Failures logged")
    
    print(f"\n✓ All processed images saved to: {output_path.absolute()}")
    
    return compressed, copied, failed

def main():
    # Check if PIL is installed
    try:
        from PIL import Image
    except ImportError:
        print("Error: 'Pillow' library is not installed")
        print("Please install it by running: pip3 install Pillow")
        sys.exit(1)
    
    # File paths
    script_dir = Path(__file__).parent
    download_dir = script_dir / "assets" / "download"
    output_dir = script_dir / "assets" / "compressed-images"
    
    # Check if download directory exists
    if not download_dir.exists():
        print(f"Error: Download directory not found: {download_dir}")
        sys.exit(1)
    
    print("="*70)
    print("ATTRACTIONS IMAGE COMPRESSION (MULTITHREADED)")
    print("="*70)
    print(f"Source directory:     {download_dir}")
    print(f"Output directory:     {output_dir}")
    print(f"Size threshold:       {SIZE_THRESHOLD_KB}KB")
    print(f"Max workers:          {MAX_WORKERS}")
    print(f"Compression mode:     Lossless (high quality)")
    print("="*70 + "\n")
    
    # Process images
    try:
        compressed, copied, failed = compress_images_multithreaded(
            download_dir, output_dir, max_workers=MAX_WORKERS
        )
        
        # Exit with appropriate code
        if failed > 0:
            print(f"\n⚠️  Warning: {failed} files failed to process")
            sys.exit(1)
        else:
            print(f"\n✓ All files processed successfully!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Processing interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()



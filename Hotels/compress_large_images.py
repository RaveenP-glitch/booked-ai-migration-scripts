#!/usr/bin/env python3
"""
Multithreaded image compressor for Hotels images
Compresses images over 400KB and copies all images to compressed-images folder
"""

import os
import sys
import shutil
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import time

# Configuration
MAX_WORKERS = 8  # Number of concurrent compression threads
COMPRESSION_THRESHOLD = 400 * 1024  # 400KB in bytes
QUALITY = 85  # JPEG compression quality (0-100)
MAX_SIZE = (1920, 1080)  # Maximum dimensions for large images

# Thread-safe counters
class CompressionStats:
    def __init__(self):
        self.lock = threading.Lock()
        self.compressed = 0
        self.copied = 0
        self.skipped = 0
        self.failed = 0
        self.original_size = 0
        self.compressed_size = 0
        self.failed_files = []
    
    def add_compressed(self, original_size, compressed_size):
        with self.lock:
            self.compressed += 1
            self.original_size += original_size
            self.compressed_size += compressed_size
    
    def add_copied(self, file_size):
        with self.lock:
            self.copied += 1
            self.original_size += file_size
            self.compressed_size += file_size
    
    def add_skipped(self):
        with self.lock:
            self.skipped += 1
    
    def add_failed(self, file_path):
        with self.lock:
            self.failed += 1
            self.failed_files.append(str(file_path))
    
    def get_stats(self):
        with self.lock:
            return {
                'compressed': self.compressed,
                'copied': self.copied,
                'skipped': self.skipped,
                'failed': self.failed,
                'original_size': self.original_size,
                'compressed_size': self.compressed_size,
                'failed_files': self.failed_files.copy()
            }

def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0

def compress_image(input_path, output_path, quality=QUALITY, max_size=MAX_SIZE):
    """
    Compress an image using PIL
    
    Args:
        input_path: Path to input image
        output_path: Path to save compressed image
        quality: JPEG quality (0-100)
        max_size: Maximum dimensions (width, height)
    
    Returns:
        tuple: (success, original_size, compressed_size)
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparency
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if image is too large
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save compressed image
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            original_size = get_file_size(input_path)
            compressed_size = get_file_size(output_path)
            
            return True, original_size, compressed_size
            
    except Exception as e:
        print(f"  ✗ Compression failed for {input_path}: {e}")
        return False, 0, 0

def copy_file(input_path, output_path):
    """
    Copy a file to destination
    
    Args:
        input_path: Source file path
        output_path: Destination file path
    
    Returns:
        tuple: (success, file_size)
    """
    try:
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(input_path, output_path)
        
        file_size = get_file_size(output_path)
        return True, file_size
        
    except Exception as e:
        print(f"  ✗ Copy failed for {input_path}: {e}")
        return False, 0

def process_image_task(task, stats, total_files):
    """
    Process a single image (compress or copy)
    
    Args:
        task: Tuple of (index, input_path, output_path)
        stats: CompressionStats object
        total_files: Total number of files
    
    Returns:
        dict: Result information
    """
    index, input_path, output_path = task
    
    # Skip if output already exists
    if output_path.exists():
        stats.add_skipped()
        return {
            'index': index,
            'status': 'skipped',
            'path': str(input_path.relative_to(input_path.parents[2]))
        }
    
    # Get file size
    file_size = get_file_size(input_path)
    
    if file_size > COMPRESSION_THRESHOLD:
        # Compress large images
        success, original_size, compressed_size = compress_image(input_path, output_path)
        
        if success:
            stats.add_compressed(original_size, compressed_size)
            compression_ratio = ((original_size - compressed_size) / original_size) * 100
            return {
                'index': index,
                'status': 'compressed',
                'path': str(input_path.relative_to(input_path.parents[2])),
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio
            }
        else:
            stats.add_failed(input_path)
            return {
                'index': index,
                'status': 'failed',
                'path': str(input_path.relative_to(input_path.parents[2]))
            }
    else:
        # Copy small images as-is
        success, file_size = copy_file(input_path, output_path)
        
        if success:
            stats.add_copied(file_size)
            return {
                'index': index,
                'status': 'copied',
                'path': str(input_path.relative_to(input_path.parents[2])),
                'file_size': file_size
            }
        else:
            stats.add_failed(input_path)
            return {
                'index': index,
                'status': 'failed',
                'path': str(input_path.relative_to(input_path.parents[2]))
            }

def print_progress(stats, total_files, start_time):
    """Print current progress"""
    current_stats = stats.get_stats()
    completed = current_stats['compressed'] + current_stats['copied'] + current_stats['skipped']
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
          f"🗜️ {current_stats['compressed']} | 📁 {current_stats['copied']} | "
          f"⊘ {current_stats['skipped']} | ✗ {current_stats['failed']} | "
          f"ETA: {eta_str}", end='', flush=True)

def get_size_distribution(directory):
    """Get size distribution of images in directory"""
    print("\nAnalyzing size distribution...")
    
    size_ranges = {
        'small': 0,      # <50KB
        'medium': 0,     # 50-100KB
        'large': 0,      # 100-200KB
        'xlarge': 0,     # 200-500KB
        'huge': 0        # >500KB
    }
    
    total_size = 0
    total_files = 0
    
    for file_path in directory.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif']:
            file_size = get_file_size(file_path)
            total_size += file_size
            total_files += 1
            
            if file_size < 50 * 1024:
                size_ranges['small'] += 1
            elif file_size < 100 * 1024:
                size_ranges['medium'] += 1
            elif file_size < 200 * 1024:
                size_ranges['large'] += 1
            elif file_size < 500 * 1024:
                size_ranges['xlarge'] += 1
            else:
                size_ranges['huge'] += 1
    
    return size_ranges, total_size, total_files

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
    assets_dir = script_dir / "assets"
    compressed_dir = script_dir / "assets" / "compressed-images"
    
    # Check if assets directory exists
    if not assets_dir.exists():
        print(f"Error: Assets directory not found: {assets_dir}")
        sys.exit(1)
    
    print("="*80)
    print("HOTELS IMAGES COMPRESSOR (MULTITHREADED)")
    print("="*80)
    print(f"Source directory:     {assets_dir}")
    print(f"Target directory:     {compressed_dir}")
    print(f"Compression threshold: {COMPRESSION_THRESHOLD/1024:.0f}KB")
    print(f"Max workers:          {MAX_WORKERS}")
    print(f"JPEG quality:         {QUALITY}")
    print(f"Max dimensions:       {MAX_SIZE[0]}x{MAX_SIZE[1]}")
    print("="*80 + "\n")
    
    # Find all image files
    print("Scanning for image files...")
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}
    image_files = []
    
    for file_path in assets_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            # Skip files in compressed-images directory
            if 'compressed-images' not in str(file_path):
                relative_path = file_path.relative_to(assets_dir)
                output_path = compressed_dir / relative_path
                image_files.append((file_path, output_path))
    
    total_files = len(image_files)
    print(f"Found {total_files} image files to process\n")
    
    if total_files == 0:
        print("No image files found to process.")
        sys.exit(0)
    
    # Initialize stats
    stats = CompressionStats()
    
    # Prepare tasks
    tasks = []
    for i, (input_path, output_path) in enumerate(image_files, 1):
        tasks.append((i, input_path, output_path))
    
    # Process with thread pool
    print("Starting image processing...")
    start_time = time.time()
    
    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all tasks
            futures = {executor.submit(process_image_task, task, stats, total_files): task 
                      for task in tasks}
            
            # Process completed tasks
            for future in as_completed(futures):
                result = future.result()
                
                # Print progress every completion
                print_progress(stats, total_files, start_time)
    
    except KeyboardInterrupt:
        print("\n\n⚠ Processing interrupted by user")
        sys.exit(130)
    
    print("\n")  # New line after progress
    
    # Final summary
    final_stats = stats.get_stats()
    elapsed = time.time() - start_time
    space_saved = final_stats['original_size'] - final_stats['compressed_size']
    compression_percentage = (space_saved / final_stats['original_size'] * 100) if final_stats['original_size'] > 0 else 0
    
    print("="*80)
    print("COMPRESSION SUMMARY")
    print("="*80)
    print(f"Total files processed:  {total_files}")
    print(f"Compressed (>400KB):    {final_stats['compressed']}")
    print(f"Copied (<400KB):        {final_stats['copied']}")
    print(f"Skipped (already exist): {final_stats['skipped']}")
    print(f"Failed:                 {final_stats['failed']}")
    print(f"Time elapsed:           {elapsed:.2f}s ({elapsed/60:.1f} minutes)")
    print(f"Original size:          {final_stats['original_size']/1024/1024:.2f} MB")
    print(f"Final size:             {final_stats['compressed_size']/1024/1024:.2f} MB")
    print(f"Space saved:            {space_saved/1024/1024:.2f} MB ({compression_percentage:.1f}%)")
    print("="*80)
    
    # Save failed files list
    if final_stats['failed_files']:
        failed_file = script_dir / "compression_failed_files.txt"
        print(f"\nSaving {len(final_stats['failed_files'])} failed files to: {failed_file}")
        with open(failed_file, 'w', encoding='utf-8') as f:
            f.write("# Failed compression files\n")
            for file_path in final_stats['failed_files']:
                f.write(f"{file_path}\n")
        print(f"✓ Failed files list saved")
    
    # Get size distribution of compressed images
    print(f"\nAnalyzing compressed images in: {compressed_dir}")
    size_ranges, total_size, total_files_final = get_size_distribution(compressed_dir)
    
    print("\n" + "="*80)
    print("FINAL SIZE DISTRIBUTION")
    print("="*80)
    print(f"Total files:           {total_files_final}")
    print(f"Total size:            {total_size/1024/1024:.2f} MB")
    print(f"Average size:          {total_size/total_files_final/1024:.2f} KB")
    print("\nSize Distribution:")
    print(f"Small (<50KB):         {size_ranges['small']:>6} files ({size_ranges['small']/total_files_final*100:5.1f}%)")
    print(f"Medium (50-100KB):     {size_ranges['medium']:>6} files ({size_ranges['medium']/total_files_final*100:5.1f}%)")
    print(f"Large (100-200KB):     {size_ranges['large']:>6} files ({size_ranges['large']/total_files_final*100:5.1f}%)")
    print(f"Extra Large (200-500KB): {size_ranges['xlarge']:>6} files ({size_ranges['xlarge']/total_files_final*100:5.1f}%)")
    print(f"Huge (>500KB):         {size_ranges['huge']:>6} files ({size_ranges['huge']/total_files_final*100:5.1f}%)")
    print("="*80)
    
    print(f"\n✓ All images processed successfully!")
    print(f"✓ Compressed images saved to: {compressed_dir.absolute()}")
    
    # Exit with appropriate code
    if final_stats['failed'] > 0:
        print(f"\n⚠ Warning: {final_stats['failed']} files failed to process")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()

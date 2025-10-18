#!/usr/bin/env python3
"""
Multithreaded script to compress images larger than 400KB and copy smaller images directly
to the compressed-images directory while preserving original filenames.
"""

import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
from PIL import Image, ImageOps
import sys

class ImageCompressor:
    def __init__(self, source_dir, output_dir, max_workers=8, size_threshold=400*1024):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.max_workers = max_workers
        self.size_threshold = size_threshold  # 400KB in bytes
        
        # Statistics
        self.compressed_count = 0
        self.copied_count = 0
        self.failed_count = 0
        self.total_original_size = 0
        self.total_compressed_size = 0
        self.file_sizes = []
        self.lock = threading.Lock()
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Supported image formats
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.avif'}
    
    def get_image_files(self):
        """Get all image files from source directory"""
        if not self.source_dir.exists():
            print(f"Error: Source directory '{self.source_dir}' does not exist!")
            return []
        
        image_files = []
        for file_path in self.source_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.image_extensions:
                image_files.append(file_path)
        
        return sorted(image_files)
    
    def compress_image(self, image_path):
        """Compress a single image while maintaining quality"""
        try:
            output_path = self.output_dir / image_path.name
            original_size = image_path.stat().st_size
            
            # Open and process the image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (for JPEG compression)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background for transparent images
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Auto-orient the image based on EXIF data
                img = ImageOps.exif_transpose(img)
                
                # Save with compression
                # Use high quality (85) to maintain good visual quality while reducing file size
                img.save(output_path, 'JPEG', quality=85, optimize=True, progressive=True)
            
            compressed_size = output_path.stat().st_size
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            with self.lock:
                self.compressed_count += 1
                self.total_original_size += original_size
                self.total_compressed_size += compressed_size
                self.file_sizes.append(compressed_size)
            
            return {
                'status': 'compressed',
                'filename': image_path.name,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio
            }
            
        except Exception as e:
            with self.lock:
                self.failed_count += 1
            return {
                'status': 'failed',
                'filename': image_path.name,
                'error': str(e)
            }
    
    def copy_image(self, image_path):
        """Copy a small image directly without compression"""
        try:
            output_path = self.output_dir / image_path.name
            file_size = image_path.stat().st_size
            
            # Copy the file
            shutil.copy2(image_path, output_path)
            
            with self.lock:
                self.copied_count += 1
                self.total_original_size += file_size
                self.total_compressed_size += file_size
                self.file_sizes.append(file_size)
            
            return {
                'status': 'copied',
                'filename': image_path.name,
                'size': file_size
            }
            
        except Exception as e:
            with self.lock:
                self.failed_count += 1
            return {
                'status': 'failed',
                'filename': image_path.name,
                'error': str(e)
            }
    
    def process_image(self, image_path):
        """Process a single image - compress if large, copy if small"""
        file_size = image_path.stat().st_size
        
        if file_size > self.size_threshold:
            return self.compress_image(image_path)
        else:
            return self.copy_image(image_path)
    
    def print_progress(self, current, total):
        """Print processing progress"""
        percentage = (current / total) * 100
        print(f"\rProgress: {current}/{total} ({percentage:.1f}%) - "
              f"Compressed: {self.compressed_count}, Copied: {self.copied_count}, Failed: {self.failed_count}", 
              end='', flush=True)
    
    def process_all_images(self):
        """Process all images using multithreading"""
        image_files = self.get_image_files()
        
        if not image_files:
            print("No image files found to process.")
            return
        
        print(f"Found {len(image_files)} images to process")
        print(f"Source directory: {self.source_dir}")
        print(f"Output directory: {self.output_dir}")
        print(f"Size threshold: {self.size_threshold / 1024:.0f} KB")
        print(f"Using {self.max_workers} threads")
        print("Starting image processing...\n")
        
        start_time = time.time()
        completed = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all processing tasks
            future_to_file = {executor.submit(self.process_image, img_file): img_file for img_file in image_files}
            
            # Process completed tasks
            for future in as_completed(future_to_file):
                completed += 1
                result = future.result()
                
                # Print progress every 100 files
                if completed % 100 == 0 or completed == len(image_files):
                    self.print_progress(completed, len(image_files))
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n\nProcessing completed!")
        print(f"Total time: {duration:.2f} seconds")
        print(f"Images compressed: {self.compressed_count}")
        print(f"Images copied: {self.copied_count}")
        print(f"Failed: {self.failed_count}")
        print(f"Total original size: {self.total_original_size / (1024*1024):.2f} MB")
        print(f"Total final size: {self.total_compressed_size / (1024*1024):.2f} MB")
        
        if self.total_original_size > 0:
            total_savings = (1 - self.total_compressed_size / self.total_original_size) * 100
            print(f"Total space saved: {total_savings:.1f}%")
        
        return self.compressed_count, self.copied_count, self.failed_count, self.total_compressed_size, self.file_sizes

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
    print(f"COMPRESSED IMAGES SIZE DISTRIBUTION ANALYSIS")
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
        (100*1024, 200*1024, "100-200 KB"),
        (200*1024, 400*1024, "200-400 KB"),
        (400*1024, 1024*1024, "400 KB-1 MB"),
        (1024*1024, 5*1024*1024, "1-5 MB"),
        (5*1024*1024, float('inf'), "5+ MB")
    ]
    
    print(f"\nSize Distribution:")
    for min_range, max_range, label in ranges:
        count = sum(1 for size in file_sizes if min_range <= size < max_range)
        percentage = (count / total_files) * 100
        print(f"  {label:12}: {count:6,} files ({percentage:5.1f}%)")

def verify_compressed_count(compressed_dir):
    """Verify the actual number of files in compressed directory"""
    compressed_path = Path(compressed_dir)
    if not compressed_path.exists():
        return 0
    
    # Count image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.avif'}
    image_files = []
    
    for file_path in compressed_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    return len(image_files)

def main():
    # Configuration
    source_dir = 'assets'
    output_dir = 'compressed-images'
    max_workers = 8  # Adjust based on your system
    size_threshold = 400 * 1024  # 400KB
    
    print(f"Image Compression Script")
    print(f"{'='*50}")
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found!")
        sys.exit(1)
    
    # Create compressor and start processing
    compressor = ImageCompressor(source_dir, output_dir, max_workers, size_threshold)
    compressed_count, copied_count, failed_count, total_size, file_sizes = compressor.process_all_images()
    
    # Verify compressed count
    print(f"\n{'='*50}")
    print(f"VERIFICATION")
    print(f"{'='*50}")
    actual_count = verify_compressed_count(output_dir)
    expected_count = compressed_count + copied_count
    print(f"Expected files: {expected_count}")
    print(f"Actual files in compressed-images folder: {actual_count}")
    
    if actual_count == expected_count:
        print("✅ File count verification: PASSED")
    else:
        print("⚠️  File count verification: MISMATCH")
    
    # Analyze file sizes
    analyze_file_sizes(file_sizes)

if __name__ == "__main__":
    main()




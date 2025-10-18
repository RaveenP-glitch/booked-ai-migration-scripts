#!/usr/bin/env python3
"""
Analyze downloaded images: verify count, size distribution, and find large files
"""

import os
from pathlib import Path
from collections import defaultdict

# Configuration
DOWNLOAD_DIR = Path(__file__).parent / "assets" / "download"
SIZE_THRESHOLD_KB = 400
SIZE_RANGES = [
    (0, 50, "0-50 KB"),
    (50, 100, "50-100 KB"),
    (100, 200, "100-200 KB"),
    (200, 300, "200-300 KB"),
    (300, 400, "300-400 KB"),
    (400, 500, "400-500 KB"),
    (500, 1000, "500 KB - 1 MB"),
    (1000, float('inf'), "> 1 MB")
]

def get_all_images(directory):
    """Recursively find all image files"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.bmp'}
    images = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                full_path = Path(root) / file
                images.append(full_path)
    
    return images

def analyze_images(images):
    """Analyze image sizes and create distribution"""
    size_distribution = defaultdict(int)
    large_files = []
    total_size = 0
    
    for img_path in images:
        try:
            size_bytes = img_path.stat().st_size
            size_kb = size_bytes / 1024
            total_size += size_bytes
            
            # Categorize by size range
            for min_size, max_size, label in SIZE_RANGES:
                if min_size <= size_kb < max_size:
                    size_distribution[label] += 1
                    break
            
            # Track large files
            if size_kb > SIZE_THRESHOLD_KB:
                large_files.append((img_path, size_kb))
        
        except Exception as e:
            print(f"Error reading {img_path}: {e}")
    
    # Sort large files by size (largest first)
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    return size_distribution, large_files, total_size

def format_size(size_bytes):
    """Format size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def main():
    print("="*80)
    print("IMAGE DOWNLOAD VERIFICATION & SIZE ANALYSIS")
    print("="*80)
    print(f"Download directory: {DOWNLOAD_DIR.absolute()}\n")
    
    # Check if directory exists
    if not DOWNLOAD_DIR.exists():
        print(f"❌ Error: Download directory not found: {DOWNLOAD_DIR}")
        return
    
    # Get all images
    print("Scanning for images...")
    images = get_all_images(DOWNLOAD_DIR)
    total_images = len(images)
    
    print(f"✓ Found {total_images} image files\n")
    
    if total_images == 0:
        print("❌ No images found in download directory!")
        return
    
    # Analyze images
    print("Analyzing image sizes...")
    size_distribution, large_files, total_size = analyze_images(images)
    
    # Display results
    print("\n" + "="*80)
    print("SIZE DISTRIBUTION")
    print("="*80)
    
    for min_size, max_size, label in SIZE_RANGES:
        count = size_distribution[label]
        if count > 0:
            percentage = (count / total_images * 100)
            bar_length = int(percentage / 2)  # Scale to 50 chars max
            bar = "█" * bar_length
            print(f"{label:15} | {count:5} ({percentage:5.1f}%) {bar}")
    
    print("="*80)
    print(f"Total images:     {total_images:,}")
    print(f"Total size:       {format_size(total_size)}")
    print(f"Average size:     {format_size(total_size / total_images)}")
    print(f"Median approx:    {format_size(total_size / total_images)}")
    print("="*80)
    
    # Display large files
    if large_files:
        print(f"\n{'='*80}")
        print(f"⚠️  IMAGES LARGER THAN {SIZE_THRESHOLD_KB} KB")
        print(f"{'='*80}")
        print(f"Found {len(large_files)} images exceeding {SIZE_THRESHOLD_KB} KB:\n")
        
        # Group by size categories
        very_large = [f for f in large_files if f[1] > 1000]  # > 1 MB
        large = [f for f in large_files if 500 <= f[1] <= 1000]  # 500KB - 1MB
        medium = [f for f in large_files if SIZE_THRESHOLD_KB <= f[1] < 500]  # 400-500KB
        
        if very_large:
            print(f"\n🔴 VERY LARGE (> 1 MB): {len(very_large)} files")
            print("-" * 80)
            for img_path, size_kb in very_large[:20]:  # Show first 20
                rel_path = img_path.relative_to(DOWNLOAD_DIR)
                print(f"  {format_size(size_kb * 1024):>12} | {rel_path}")
            if len(very_large) > 20:
                print(f"  ... and {len(very_large) - 20} more files")
        
        if large:
            print(f"\n🟠 LARGE (500 KB - 1 MB): {len(large)} files")
            print("-" * 80)
            for img_path, size_kb in large[:10]:  # Show first 10
                rel_path = img_path.relative_to(DOWNLOAD_DIR)
                print(f"  {format_size(size_kb * 1024):>12} | {rel_path}")
            if len(large) > 10:
                print(f"  ... and {len(large) - 10} more files")
        
        if medium:
            print(f"\n🟡 MEDIUM (400-500 KB): {len(medium)} files")
            print("-" * 80)
            for img_path, size_kb in medium[:10]:  # Show first 10
                rel_path = img_path.relative_to(DOWNLOAD_DIR)
                print(f"  {format_size(size_kb * 1024):>12} | {rel_path}")
            if len(medium) > 10:
                print(f"  ... and {len(medium) - 10} more files")
        
        # Save to file
        large_files_txt = DOWNLOAD_DIR.parent / "large_images_over_400kb.txt"
        with open(large_files_txt, 'w') as f:
            f.write(f"Images larger than {SIZE_THRESHOLD_KB} KB\n")
            f.write(f"Total: {len(large_files)} files\n")
            f.write("="*80 + "\n\n")
            for img_path, size_kb in large_files:
                rel_path = img_path.relative_to(DOWNLOAD_DIR)
                f.write(f"{size_kb:8.2f} KB | {rel_path}\n")
        
        print(f"\n✓ Full list saved to: {large_files_txt}")
        print("="*80)
    else:
        print(f"\n✓ Good news! No images exceed {SIZE_THRESHOLD_KB} KB")
    
    print(f"\n✅ Verification complete!")

if __name__ == "__main__":
    main()



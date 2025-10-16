#!/usr/bin/env python3
"""
Analyze downloaded images - check sizes and distribution
"""

import os
from pathlib import Path
from collections import defaultdict

def format_size(bytes):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def analyze_images(download_dir):
    """Analyze all images in download directory"""
    download_path = Path(download_dir)
    
    # Collect all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.bmp'}
    all_images = []
    
    print("Scanning for images...")
    for root, dirs, files in os.walk(download_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in image_extensions:
                size = file_path.stat().st_size
                all_images.append({
                    'path': file_path,
                    'name': file,
                    'size': size,
                    'size_kb': size / 1024,
                    'relative_path': file_path.relative_to(download_path)
                })
    
    if not all_images:
        print("No images found in download directory!")
        return
    
    # Sort by size
    all_images.sort(key=lambda x: x['size'], reverse=True)
    
    # Calculate statistics
    total_images = len(all_images)
    total_size = sum(img['size'] for img in all_images)
    avg_size = total_size / total_images
    
    # Size distribution
    size_ranges = {
        '0-50KB': 0,
        '50-100KB': 0,
        '100-200KB': 0,
        '200-400KB': 0,
        '400KB-1MB': 0,
        '1MB-2MB': 0,
        '2MB+': 0
    }
    
    images_over_400kb = []
    
    for img in all_images:
        size_kb = img['size_kb']
        
        if size_kb < 50:
            size_ranges['0-50KB'] += 1
        elif size_kb < 100:
            size_ranges['50-100KB'] += 1
        elif size_kb < 200:
            size_ranges['100-200KB'] += 1
        elif size_kb < 400:
            size_ranges['200-400KB'] += 1
        elif size_kb < 1024:
            size_ranges['400KB-1MB'] += 1
            images_over_400kb.append(img)
        elif size_kb < 2048:
            size_ranges['1MB-2MB'] += 1
            images_over_400kb.append(img)
        else:
            size_ranges['2MB+'] += 1
            images_over_400kb.append(img)
    
    # Print summary
    print("\n" + "="*70)
    print("IMAGE DOWNLOAD VERIFICATION & ANALYSIS")
    print("="*70)
    print(f"Total images found:      {total_images:,}")
    print(f"Total size:              {format_size(total_size)}")
    print(f"Average size per image:  {format_size(avg_size)}")
    print(f"Smallest image:          {format_size(all_images[-1]['size'])} - {all_images[-1]['name']}")
    print(f"Largest image:           {format_size(all_images[0]['size'])} - {all_images[0]['name']}")
    print("="*70)
    
    # Print size distribution
    print("\nSIZE DISTRIBUTION:")
    print("-"*70)
    for range_name, count in size_ranges.items():
        percentage = (count / total_images * 100)
        bar_length = int(percentage / 2)
        bar = '█' * bar_length
        print(f"{range_name:15} {count:5} images ({percentage:5.1f}%) {bar}")
    print("-"*70)
    
    # Images over 400KB
    print(f"\n⚠️  IMAGES OVER 400KB: {len(images_over_400kb)} images")
    print("="*70)
    
    if images_over_400kb:
        print(f"\nTop 20 largest images:")
        print("-"*70)
        print(f"{'Size':>12}  {'Filename'}")
        print("-"*70)
        
        for img in images_over_400kb[:20]:
            print(f"{format_size(img['size']):>12}  {img['relative_path']}")
        
        if len(images_over_400kb) > 20:
            print(f"\n... and {len(images_over_400kb) - 20} more images over 400KB")
        
        # Save full list to file
        output_file = download_path.parent / "images_over_400kb.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Images Over 400KB - Full List\n")
            f.write("="*70 + "\n\n")
            f.write(f"Total images over 400KB: {len(images_over_400kb)}\n\n")
            f.write(f"{'Size':>12}  {'Size (KB)':>10}  {'Filename'}\n")
            f.write("-"*70 + "\n")
            
            for img in images_over_400kb:
                f.write(f"{format_size(img['size']):>12}  {img['size_kb']:>10.2f}  {img['relative_path']}\n")
        
        print(f"\n📄 Full list saved to: {output_file}")
    else:
        print("✓ All images are under 400KB!")
    
    # File type distribution
    print("\n" + "="*70)
    print("FILE TYPE DISTRIBUTION:")
    print("-"*70)
    
    file_types = defaultdict(int)
    for img in all_images:
        ext = img['path'].suffix.lower()
        file_types[ext] += 1
    
    for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_images * 100)
        print(f"{ext:10} {count:5} images ({percentage:5.1f}%)")
    
    print("="*70)

def main():
    download_dir = Path(__file__).parent / "assets" / "download"
    
    if not download_dir.exists():
        print(f"Error: Download directory not found: {download_dir}")
        return
    
    analyze_images(download_dir)

if __name__ == "__main__":
    main()


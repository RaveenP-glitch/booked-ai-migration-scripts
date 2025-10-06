#!/usr/bin/env python3
"""
Script to compress images larger than 400KB in the Itineraries assets folder.
Images smaller than 400KB are copied without compression.
All images are saved to a compressed-images folder with the same filenames.
"""

import os
import shutil
from PIL import Image
import glob

def get_file_size_kb(filepath):
    """Get file size in KB."""
    return os.path.getsize(filepath) / 1024

def compress_image(input_path, output_path, quality=85, max_size_kb=400):
    """
    Compress an image while maintaining quality.
    Returns the final file size in KB.
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for JPEG compatibility)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Save with compression
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Check if we achieved the target size
            final_size_kb = get_file_size_kb(output_path)
            
            # If still too large, reduce quality further
            if final_size_kb > max_size_kb and quality > 50:
                quality = max(50, quality - 10)
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                final_size_kb = get_file_size_kb(output_path)
            
            return final_size_kb
            
    except Exception as e:
        print(f"Error compressing {input_path}: {e}")
        return None

def main():
    # Paths
    source_dir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/assets'
    output_dir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/compressed-images'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all JPEG files
    image_files = glob.glob(os.path.join(source_dir, '*.jpeg'))
    image_files.extend(glob.glob(os.path.join(source_dir, '*.jpg')))
    
    print(f"Found {len(image_files)} images to process...")
    print(f"Output directory: {output_dir}")
    
    # Statistics
    compressed_count = 0
    copied_count = 0
    error_count = 0
    total_original_size = 0
    total_compressed_size = 0
    
    # Process each image
    for i, image_path in enumerate(image_files, 1):
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)
        
        # Get original file size
        original_size_kb = get_file_size_kb(image_path)
        total_original_size += original_size_kb
        
        print(f"[{i}/{len(image_files)}] Processing: {filename} ({original_size_kb:.1f} KB)")
        
        try:
            if original_size_kb > 400:
                # Compress the image
                final_size_kb = compress_image(image_path, output_path, quality=85, max_size_kb=400)
                
                if final_size_kb:
                    compressed_count += 1
                    total_compressed_size += final_size_kb
                    compression_ratio = ((original_size_kb - final_size_kb) / original_size_kb) * 100
                    print(f"  ✓ Compressed: {original_size_kb:.1f} KB → {final_size_kb:.1f} KB ({compression_ratio:.1f}% reduction)")
                else:
                    error_count += 1
                    print(f"  ✗ Failed to compress")
            else:
                # Copy without compression
                shutil.copy2(image_path, output_path)
                copied_count += 1
                total_compressed_size += original_size_kb
                print(f"  ✓ Copied (no compression needed)")
        
        except Exception as e:
            error_count += 1
            print(f"  ✗ Error: {e}")
        
        # Progress update every 50 files
        if i % 50 == 0:
            print(f"\nProgress: {i}/{len(image_files)} - Compressed: {compressed_count}, Copied: {copied_count}, Errors: {error_count}\n")
    
    # Final statistics
    print(f"\n{'='*60}")
    print(f"Compression completed!")
    print(f"Total images processed: {len(image_files)}")
    print(f"Images compressed: {compressed_count}")
    print(f"Images copied (no compression): {copied_count}")
    print(f"Errors: {error_count}")
    print(f"")
    print(f"Size reduction:")
    print(f"  Original total size: {total_original_size/1024:.1f} MB")
    print(f"  Compressed total size: {total_compressed_size/1024:.1f} MB")
    print(f"  Space saved: {(total_original_size - total_compressed_size)/1024:.1f} MB")
    print(f"  Overall compression: {((total_original_size - total_compressed_size) / total_original_size) * 100:.1f}%")
    print(f"")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()


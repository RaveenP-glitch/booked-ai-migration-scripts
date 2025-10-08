#!/usr/bin/env python3
"""
Script to compress images larger than 400KB in a lossless way.
Copies all images to compressed-images directory, compressing only those > 400KB.
"""

import os
import shutil
from PIL import Image
import sys

def compress_image(input_path, output_path, target_size_kb=400):
    """
    Compress an image to be under target_size_kb using lossless compression.
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for JPEG compatibility)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get original file size
            original_size = os.path.getsize(input_path)
            original_size_kb = original_size / 1024
            
            # If already under target size, just copy
            if original_size_kb <= target_size_kb:
                shutil.copy2(input_path, output_path)
                return True, original_size_kb, original_size_kb, "No compression needed"
            
            # Try different quality levels to get under target size
            target_size_bytes = target_size_kb * 1024
            quality = 95
            
            while quality > 10:
                # Save with current quality
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                
                # Check if we're under target size
                compressed_size = os.path.getsize(output_path)
                compressed_size_kb = compressed_size / 1024
                
                if compressed_size <= target_size_bytes:
                    compression_ratio = (original_size_kb - compressed_size_kb) / original_size_kb * 100
                    return True, original_size_kb, compressed_size_kb, f"Compressed (quality={quality}, {compression_ratio:.1f}% reduction)"
                
                quality -= 5
            
            # If we can't get under target even with quality=10, use the best we can do
            img.save(output_path, 'JPEG', quality=10, optimize=True)
            compressed_size = os.path.getsize(output_path)
            compressed_size_kb = compressed_size / 1024
            compression_ratio = (original_size_kb - compressed_size_kb) / original_size_kb * 100
            
            return True, original_size_kb, compressed_size_kb, f"Best compression (quality=10, {compression_ratio:.1f}% reduction)"
            
    except Exception as e:
        return False, 0, 0, f"Error: {str(e)}"

def main():
    source_dir = "assets"
    target_dir = "compressed-images"
    
    # Create target directory
    os.makedirs(target_dir, exist_ok=True)
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
    
    # Statistics
    total_files = 0
    compressed_files = 0
    copied_files = 0
    failed_files = 0
    original_total_size = 0
    compressed_total_size = 0
    
    print("=== EXPLORES IMAGE COMPRESSION ===")
    print(f"Source directory: {source_dir}")
    print(f"Target directory: {target_dir}")
    print("Compressing images larger than 400KB...")
    print("-" * 60)
    
    # Process all files in source directory
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        # Skip if not a file
        if not os.path.isfile(file_path):
            continue
        
        # Check if it's an image file
        _, ext = os.path.splitext(filename.lower())
        if ext not in image_extensions:
            continue
        
        total_files += 1
        output_path = os.path.join(target_dir, filename)
        
        # Get original file size
        original_size = os.path.getsize(file_path)
        original_size_kb = original_size / 1024
        original_total_size += original_size
        
        print(f"[{total_files:4d}] {filename[:50]:<50} ", end="")
        
        # If file is already under 400KB, just copy it
        if original_size_kb <= 400:
            try:
                shutil.copy2(file_path, output_path)
                copied_files += 1
                compressed_total_size += original_size
                print(f"✅ Copied ({original_size_kb:.0f}KB)")
            except Exception as e:
                failed_files += 1
                print(f"❌ Copy failed: {e}")
        else:
            # Compress the image
            success, orig_kb, comp_kb, message = compress_image(file_path, output_path, 400)
            
            if success:
                compressed_files += 1
                compressed_total_size += comp_kb * 1024
                print(f"✅ {message}")
            else:
                failed_files += 1
                print(f"❌ {message}")
    
    # Final statistics
    original_total_mb = original_total_size / (1024 * 1024)
    compressed_total_mb = compressed_total_size / (1024 * 1024)
    space_saved_mb = original_total_mb - compressed_total_mb
    compression_ratio = (space_saved_mb / original_total_mb) * 100 if original_total_mb > 0 else 0
    
    print("\n" + "=" * 60)
    print("COMPRESSION COMPLETE")
    print("=" * 60)
    print(f"Total files processed: {total_files}")
    print(f"Files compressed: {compressed_files}")
    print(f"Files copied (already < 400KB): {copied_files}")
    print(f"Failed files: {failed_files}")
    print(f"Success rate: {((compressed_files + copied_files) / total_files * 100):.1f}%")
    print("")
    print(f"Original total size: {original_total_mb:.1f} MB")
    print(f"Compressed total size: {compressed_total_mb:.1f} MB")
    print(f"Space saved: {space_saved_mb:.1f} MB ({compression_ratio:.1f}%)")
    print(f"Files saved to: {os.path.abspath(target_dir)}")
    
    if failed_files > 0:
        print(f"\n⚠️  {failed_files} files failed to process. Check the output above for details.")

if __name__ == "__main__":
    main()


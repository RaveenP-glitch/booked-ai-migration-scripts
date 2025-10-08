#!/usr/bin/env python3
"""
Script to copy all images to compressed-images directory.
Compress images > 300KB using lossless optimization for web delivery.
"""

import os
import shutil
from pathlib import Path
from PIL import Image
import sys

def get_file_size_kb(file_path):
    """Get file size in KB."""
    return os.path.getsize(file_path) / 1024

def optimize_image_for_web(input_path, output_path, target_size_kb=300):
    """Optimize image for web delivery while maintaining quality."""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for JPEG optimization)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Try different quality levels to get under target size
            original_size = get_file_size_kb(input_path)
            
            # If already under target, just copy
            if original_size <= target_size_kb:
                shutil.copy2(input_path, output_path)
                return True, f"Copied (already under {target_size_kb}KB)"
            
            # Try different quality levels
            for quality in [95, 90, 85, 80, 75, 70, 65, 60, 55, 50]:
                # Save with current quality
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                
                # Check if we're under target size
                compressed_size = get_file_size_kb(output_path)
                if compressed_size <= target_size_kb:
                    return True, f"Compressed to {compressed_size:.1f}KB (quality: {quality})"
            
            # If still too large, try reducing dimensions
            original_width, original_height = img.size
            for scale in [0.9, 0.8, 0.7, 0.6, 0.5]:
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
                
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                resized_img.save(output_path, 'JPEG', quality=85, optimize=True)
                
                compressed_size = get_file_size_kb(output_path)
                if compressed_size <= target_size_kb:
                    return True, f"Compressed to {compressed_size:.1f}KB (resized to {new_width}x{new_height}, quality: 85)"
            
            # If still too large, use minimum quality
            img.save(output_path, 'JPEG', quality=50, optimize=True)
            final_size = get_file_size_kb(output_path)
            return True, f"Compressed to {final_size:.1f}KB (minimum quality: 50)"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    # Set up directories
    source_dir = Path('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/City-Blogs/assets')
    target_dir = Path('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/City-Blogs/compressed-images')
    
    # Create target directory
    target_dir.mkdir(exist_ok=True)
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
    image_files = [f for f in source_dir.iterdir() if f.suffix.lower() in image_extensions]
    
    print(f"🔍 Found {len(image_files)} image files to process")
    print(f"📁 Source: {source_dir}")
    print(f"📁 Target: {target_dir}")
    print()
    
    # Process each image
    copied_count = 0
    compressed_count = 0
    error_count = 0
    total_original_size = 0
    total_compressed_size = 0
    
    for i, image_file in enumerate(image_files, 1):
        if i % 100 == 0:
            print(f"Progress: {i}/{len(image_files)} ({i/len(image_files)*100:.1f}%)")
        
        try:
            # Get original file size
            original_size = get_file_size_kb(image_file)
            total_original_size += original_size
            
            # Determine if compression is needed
            if original_size > 300:
                # Compress the image
                success, message = optimize_image_for_web(image_file, target_dir / image_file.name)
                if success:
                    compressed_count += 1
                    compressed_size = get_file_size_kb(target_dir / image_file.name)
                    total_compressed_size += compressed_size
                    if i <= 10:  # Show details for first 10 files
                        print(f"✅ {image_file.name}: {original_size:.1f}KB → {compressed_size:.1f}KB ({message})")
                else:
                    error_count += 1
                    print(f"❌ {image_file.name}: {message}")
            else:
                # Just copy the file
                shutil.copy2(image_file, target_dir / image_file.name)
                copied_count += 1
                total_compressed_size += original_size
                if i <= 10:  # Show details for first 10 files
                    print(f"📋 {image_file.name}: {original_size:.1f}KB (copied)")
        
        except Exception as e:
            error_count += 1
            print(f"❌ Error processing {image_file.name}: {str(e)}")
    
    # Final statistics
    print(f"\n📊 PROCESSING COMPLETE!")
    print(f"📁 Total files processed: {len(image_files)}")
    print(f"📋 Files copied (≤300KB): {copied_count}")
    print(f"🗜️  Files compressed (>300KB): {compressed_count}")
    print(f"❌ Errors: {error_count}")
    print(f"✅ Success rate: {((copied_count + compressed_count) / len(image_files)) * 100:.1f}%")
    
    # Size statistics
    print(f"\n📏 SIZE STATISTICS:")
    print(f"📦 Original total size: {total_original_size / 1024:.1f} MB")
    print(f"📦 Compressed total size: {total_compressed_size / 1024:.1f} MB")
    if total_original_size > 0:
        savings = ((total_original_size - total_compressed_size) / total_original_size) * 100
        print(f"💾 Space saved: {savings:.1f}%")
    
    # Verify final count
    final_files = list(target_dir.glob('*'))
    final_image_files = [f for f in final_files if f.suffix.lower() in image_extensions]
    
    print(f"\n🔍 VERIFICATION:")
    print(f"📁 Files in compressed-images: {len(final_image_files)}")
    print(f"📊 Expected: {len(image_files)}")
    print(f"✅ Match: {'Yes' if len(final_image_files) == len(image_files) else 'No'}")
    
    # Check for files > 300KB in compressed directory
    large_files = [f for f in final_image_files if get_file_size_kb(f) > 300]
    print(f"📏 Files still > 300KB: {len(large_files)}")
    
    if large_files:
        print("⚠️  Large files remaining:")
        for f in large_files[:5]:  # Show first 5
            size = get_file_size_kb(f)
            print(f"   {f.name}: {size:.1f}KB")
        if len(large_files) > 5:
            print(f"   ... and {len(large_files) - 5} more")

if __name__ == "__main__":
    main()


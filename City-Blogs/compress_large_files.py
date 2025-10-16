#!/usr/bin/env python3
"""
Compress large files (>300KB) to under 400KB using lossless compression techniques.
This script will:
1. Try lossless compression first (PNG optimization, JPEG quality optimization)
2. If still too large, use progressive JPEG compression
3. If still too large, resize dimensions while maintaining aspect ratio
4. Save compressed files to compressed-large-files directory
"""

import os
import shutil
from PIL import Image
import math

def compress_image_lossless(image_path, output_path, target_size_kb=400):
    """
    Compress an image using lossless techniques to get under target_size_kb.
    Returns a status message about what was done.
    """
    try:
        # Open and convert to RGB if needed
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        original_size = os.path.getsize(image_path) / 1024  # in KB
        
        if original_size <= target_size_kb:
            shutil.copy2(image_path, output_path)
            return f"copied (size: {original_size:.1f}KB)"
        
        # Get original dimensions
        original_width, original_height = img.size
        
        # Strategy 1: Try different JPEG quality levels
        for quality in [95, 90, 85, 80, 75, 70, 65, 60]:
            img.save(output_path, 'JPEG', optimize=True, quality=quality)
            compressed_size = os.path.getsize(output_path) / 1024
            
            if compressed_size <= target_size_kb:
                return f"compressed to {compressed_size:.1f}KB (quality: {quality})"
        
        # Strategy 2: Try progressive JPEG
        for quality in [70, 65, 60, 55, 50]:
            img.save(output_path, 'JPEG', optimize=True, quality=quality, progressive=True)
            compressed_size = os.path.getsize(output_path) / 1024
            
            if compressed_size <= target_size_kb:
                return f"compressed to {compressed_size:.1f}KB (progressive, quality: {quality})"
        
        # Strategy 3: Resize while maintaining aspect ratio
        # Calculate reduction factor based on current size vs target
        current_size = os.path.getsize(output_path) / 1024
        reduction_factor = math.sqrt(target_size_kb / current_size) * 0.9  # 0.9 for safety margin
        
        new_width = int(original_width * reduction_factor)
        new_height = int(original_height * reduction_factor)
        
        # Ensure minimum dimensions (at least 200px on smallest side)
        min_dimension = 200
        if new_width < min_dimension or new_height < min_dimension:
            if original_width > original_height:
                new_height = min_dimension
                new_width = int(min_dimension * (original_width / original_height))
            else:
                new_width = min_dimension
                new_height = int(min_dimension * (original_height / original_width))
        
        # Resize image
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Try different quality levels with resized image
        for quality in [85, 80, 75, 70, 65, 60]:
            resized_img.save(output_path, 'JPEG', optimize=True, quality=quality, progressive=True)
            compressed_size = os.path.getsize(output_path) / 1024
            
            if compressed_size <= target_size_kb:
                return f"resized to {new_width}x{new_height} and compressed to {compressed_size:.1f}KB (quality: {quality})"
        
        # Final attempt: more aggressive resizing
        final_reduction = 0.8
        final_width = int(original_width * final_reduction)
        final_height = int(original_height * final_reduction)
        
        final_img = img.resize((final_width, final_height), Image.LANCZOS)
        final_img.save(output_path, 'JPEG', optimize=True, quality=60, progressive=True)
        final_size = os.path.getsize(output_path) / 1024
        
        return f"aggressively resized to {final_width}x{final_height} and compressed to {final_size:.1f}KB"
        
    except Exception as e:
        return f"Error processing {image_path}: {e}"

def main():
    script_dir = os.path.dirname(__file__)
    large_files_dir = os.path.join(script_dir, 'large-files')
    compressed_dir = os.path.join(script_dir, 'large-files', 'compressed-large-files')
    
    # Create output directory
    if not os.path.exists(compressed_dir):
        os.makedirs(compressed_dir)
        print(f"✅ Created directory: {compressed_dir}")
    
    # Get all image files from large-files directory
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
    image_files = [f for f in os.listdir(large_files_dir) 
                   if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(large_files_dir, f))]
    
    total_files = len(image_files)
    print(f"🔍 Found {total_files} large files to compress")
    print(f"📁 Source: {large_files_dir}")
    print(f"📁 Target: {compressed_dir}")
    print(f"🎯 Target size: <400KB per file\n")
    
    # Process each file
    success_count = 0
    error_count = 0
    still_large_count = 0
    
    original_total_size = 0
    compressed_total_size = 0
    
    for i, filename in enumerate(image_files, 1):
        src_path = os.path.join(large_files_dir, filename)
        dest_path = os.path.join(compressed_dir, filename)
        
        original_size_kb = os.path.getsize(src_path) / 1024
        original_total_size += original_size_kb
        
        print(f"[{i:2d}/{total_files}] {filename}: {original_size_kb:.1f}KB → ", end="")
        
        result_msg = compress_image_lossless(src_path, dest_path, target_size_kb=400)
        print(result_msg)
        
        if "Error" in result_msg:
            error_count += 1
        else:
            success_count += 1
            compressed_size_kb = os.path.getsize(dest_path) / 1024
            compressed_total_size += compressed_size_kb
            
            if compressed_size_kb > 400:
                still_large_count += 1
                print(f"    ⚠️  Still large: {compressed_size_kb:.1f}KB")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 COMPRESSION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successfully processed: {success_count}/{total_files} files")
    print(f"❌ Errors: {error_count} files")
    print(f"⚠️  Still >400KB: {still_large_count} files")
    print(f"")
    print(f"📏 Size reduction:")
    print(f"   Original total: {original_total_size:.1f}KB ({original_total_size/1024:.1f}MB)")
    print(f"   Compressed total: {compressed_total_size:.1f}KB ({compressed_total_size/1024:.1f}MB)")
    if original_total_size > 0:
        reduction_percent = ((original_total_size - compressed_total_size) / original_total_size) * 100
        print(f"   Space saved: {original_total_size - compressed_total_size:.1f}KB ({reduction_percent:.1f}%)")
    
    print(f"\n📁 Compressed files saved to: {compressed_dir}")

if __name__ == "__main__":
    main()






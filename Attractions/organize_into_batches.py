#!/usr/bin/env python3
"""
Organize images from compressed-images folder into 12 batches
"""

import os
import shutil
from pathlib import Path

def organize_images_into_batches(source_dir, num_batches=12):
    """
    Organize all images into specified number of batch folders
    
    Args:
        source_dir: Source directory containing images
        num_batches: Number of batch folders to create
    """
    source_path = Path(source_dir)
    
    # Collect all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.bmp'}
    all_images = []
    
    print("Scanning for images...")
    for root, dirs, files in os.walk(source_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in image_extensions:
                all_images.append(file_path)
    
    total_images = len(all_images)
    images_per_batch = (total_images + num_batches - 1) // num_batches  # Ceiling division
    
    print(f"\nFound {total_images:,} images")
    print(f"Distributing into {num_batches} batches")
    print(f"Approximately {images_per_batch:,} images per batch")
    print()
    
    # Create batch directories at the same level as compressed-images
    parent_dir = source_path.parent
    batch_base_name = "batch"
    
    # Process images in batches
    for batch_num in range(1, num_batches + 1):
        start_idx = (batch_num - 1) * images_per_batch
        end_idx = min(start_idx + images_per_batch, total_images)
        batch_images = all_images[start_idx:end_idx]
        
        if not batch_images:
            break
        
        # Create batch directory
        batch_dir = parent_dir / f"{batch_base_name}_{batch_num}"
        batch_dir.mkdir(exist_ok=True)
        
        print(f"Processing Batch {batch_num}:")
        print(f"  Creating: {batch_dir.name}")
        print(f"  Images: {len(batch_images):,} (from {start_idx + 1} to {end_idx})")
        
        # Copy images to batch directory
        copied_count = 0
        for img_path in batch_images:
            # Use just the filename (flatten the structure)
            dest_path = batch_dir / img_path.name
            
            # Handle duplicate filenames by adding a counter
            if dest_path.exists():
                base_name = dest_path.stem
                extension = dest_path.suffix
                counter = 1
                while dest_path.exists():
                    dest_path = batch_dir / f"{base_name}_{counter}{extension}"
                    counter += 1
            
            shutil.copy2(img_path, dest_path)
            copied_count += 1
            
            if copied_count % 100 == 0:
                print(f"    Copied {copied_count}/{len(batch_images)} images...", end='\r')
        
        print(f"    Copied {copied_count}/{len(batch_images)} images... ✓")
        print()
    
    print("="*70)
    print("ORGANIZATION SUMMARY")
    print("="*70)
    print(f"Total images organized: {total_images:,}")
    print(f"Number of batches: {num_batches}")
    print(f"Images per batch: ~{images_per_batch:,}")
    print(f"Batch location: {parent_dir.absolute()}")
    print("="*70)
    print(f"\n✓ All images organized into {num_batches} batch folders!")

def main():
    script_dir = Path(__file__).parent
    source_dir = script_dir / "assets" / "compressed-images"
    
    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}")
        return
    
    print("="*70)
    print("ORGANIZE IMAGES INTO BATCHES")
    print("="*70)
    print(f"Source: {source_dir}")
    print(f"Target: 12 batch folders")
    print("="*70)
    print()
    
    organize_images_into_batches(source_dir, num_batches=12)

if __name__ == "__main__":
    main()


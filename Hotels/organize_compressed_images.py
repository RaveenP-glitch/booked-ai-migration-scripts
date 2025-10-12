#!/usr/bin/env python3
"""
Organize compressed images into 12 subdirectories with max 1200 images each
"""

import os
import shutil
import sys
from pathlib import Path
from collections import defaultdict

def organize_images_into_folders(source_dir, max_images_per_folder=1200, num_folders=12):
    """
    Organize images into numbered subdirectories
    
    Args:
        source_dir: Source directory containing images
        max_images_per_folder: Maximum images per folder
        num_folders: Number of folders to create
    """
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"Error: Source directory not found: {source_path}")
        return False
    
    # Find all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}
    image_files = []
    
    print("Scanning for image files...")
    for file_path in source_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    total_images = len(image_files)
    print(f"Found {total_images} image files")
    
    if total_images == 0:
        print("No image files found to organize.")
        return False
    
    # Calculate images per folder
    images_per_folder = total_images // num_folders
    remainder = total_images % num_folders
    
    print(f"\nOrganizing {total_images} images into {num_folders} folders:")
    print(f"Base images per folder: {images_per_folder}")
    if remainder > 0:
        print(f"First {remainder} folders will have {images_per_folder + 1} images")
    
    # Create subdirectories and organize images
    current_index = 0
    successful_moves = 0
    failed_moves = 0
    
    for folder_num in range(1, num_folders + 1):
        # Calculate how many images this folder should have
        if folder_num <= remainder:
            folder_size = images_per_folder + 1
        else:
            folder_size = images_per_folder
        
        # Create folder
        folder_name = f"folder_{folder_num:02d}"
        folder_path = source_path / folder_name
        folder_path.mkdir(exist_ok=True)
        
        print(f"\nCreating {folder_name} with {folder_size} images...")
        
        # Move images to this folder
        for i in range(folder_size):
            if current_index >= total_images:
                break
                
            source_file = image_files[current_index]
            filename = source_file.name
            dest_file = folder_path / filename
            
            try:
                # Move file (rename to move across directories)
                shutil.move(str(source_file), str(dest_file))
                successful_moves += 1
                
                if (i + 1) % 100 == 0:
                    print(f"  Moved {i + 1}/{folder_size} images...")
                    
            except Exception as e:
                print(f"  ✗ Failed to move {filename}: {e}")
                failed_moves += 1
            
            current_index += 1
        
        print(f"  ✓ {folder_name} completed with {folder_size} images")
    
    # Summary
    print("\n" + "="*60)
    print("ORGANIZATION SUMMARY")
    print("="*60)
    print(f"Total images processed: {total_images}")
    print(f"Successfully moved:     {successful_moves}")
    print(f"Failed moves:           {failed_moves}")
    print(f"Folders created:        {num_folders}")
    print("="*60)
    
    # Verify folder contents
    print("\nVerifying folder contents:")
    for folder_num in range(1, num_folders + 1):
        folder_name = f"folder_{folder_num:02d}"
        folder_path = source_path / folder_name
        
        if folder_path.exists():
            image_count = len([f for f in folder_path.iterdir() if f.is_file() and f.suffix.lower() in image_extensions])
            print(f"  {folder_name}: {image_count} images")
        else:
            print(f"  {folder_name}: Not found")
    
    return successful_moves == total_images

def main():
    # File paths
    script_dir = Path(__file__).parent
    compressed_dir = script_dir / "assets" / "compressed-images"
    
    print("="*60)
    print("COMPRESSED IMAGES ORGANIZER")
    print("="*60)
    print(f"Source directory: {compressed_dir}")
    print(f"Max images per folder: 1200")
    print(f"Number of folders: 12")
    print("="*60 + "\n")
    
    # Check if source directory exists
    if not compressed_dir.exists():
        print(f"Error: Compressed images directory not found: {compressed_dir}")
        print("Please run the compression script first.")
        sys.exit(1)
    
    # Organize images
    try:
        success = organize_images_into_folders(
            compressed_dir, 
            max_images_per_folder=1200, 
            num_folders=12
        )
        
        if success:
            print(f"\n✓ All images organized successfully!")
            print(f"✓ Images are now in: {compressed_dir.absolute()}")
            sys.exit(0)
        else:
            print(f"\n⚠ Some images failed to organize")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠ Organization interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

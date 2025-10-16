#!/usr/bin/env python3
"""
Script to find missing images from Attractions/assets folders
that are not present in Strapi media library.
"""

import json
import os
from pathlib import Path
import shutil

# Paths
ASSETS_DIR = Path(__file__).parent / "assets"
MEDIA_JSON_PATH = Path(__file__).parent.parent / "Graphql-asset-manager" / "media-ids-and-names.json"
MISSING_IMAGES_DIR = ASSETS_DIR / "missing_images"

def load_strapi_media():
    """Load the media IDs and names from Strapi"""
    print(f"Loading Strapi media from: {MEDIA_JSON_PATH}")
    with open(MEDIA_JSON_PATH, 'r') as f:
        media_list = json.load(f)
    
    # Create a set of media names for quick lookup
    media_names = {item['name'] for item in media_list}
    print(f"✓ Loaded {len(media_names)} media items from Strapi")
    return media_names

def scan_batch_folders():
    """Scan all batch folders and collect image filenames"""
    print(f"\nScanning batch folders in: {ASSETS_DIR}")
    
    all_images = {}
    batch_folders = sorted([d for d in ASSETS_DIR.iterdir() if d.is_dir() and d.name.startswith('batch_')])
    
    for batch_folder in batch_folders:
        images_in_batch = []
        for file_path in batch_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif']:
                images_in_batch.append(file_path)
        
        all_images[batch_folder.name] = images_in_batch
        print(f"  {batch_folder.name}: {len(images_in_batch)} images")
    
    total_images = sum(len(imgs) for imgs in all_images.values())
    print(f"✓ Total images found: {total_images}")
    
    return all_images

def find_missing_images(strapi_media_names, batch_images):
    """Compare local images against Strapi media and find missing ones"""
    print("\nComparing images...")
    
    missing_images = []
    
    for batch_name, image_paths in batch_images.items():
        for image_path in image_paths:
            image_name = image_path.name
            if image_name not in strapi_media_names:
                missing_images.append({
                    'batch': batch_name,
                    'path': image_path,
                    'name': image_name
                })
    
    print(f"✓ Found {len(missing_images)} missing images")
    return missing_images

def copy_missing_images(missing_images):
    """Copy missing images to a new directory"""
    if not missing_images:
        print("\n✓ No missing images to copy!")
        return
    
    print(f"\nCreating missing images directory: {MISSING_IMAGES_DIR}")
    MISSING_IMAGES_DIR.mkdir(exist_ok=True)
    
    # Create subdirectories for each batch
    batch_counts = {}
    for img_info in missing_images:
        batch_name = img_info['batch']
        if batch_name not in batch_counts:
            batch_counts[batch_name] = 0
        batch_counts[batch_name] += 1
    
    print(f"\nCopying missing images by batch:")
    for batch_name, count in sorted(batch_counts.items()):
        print(f"  {batch_name}: {count} images")
    
    copied_count = 0
    for img_info in missing_images:
        batch_dir = MISSING_IMAGES_DIR / img_info['batch']
        batch_dir.mkdir(exist_ok=True)
        
        dest_path = batch_dir / img_info['name']
        shutil.copy2(img_info['path'], dest_path)
        copied_count += 1
    
    print(f"\n✓ Successfully copied {copied_count} missing images to {MISSING_IMAGES_DIR}")

def save_missing_images_report(missing_images):
    """Save a JSON report of missing images"""
    report_path = ASSETS_DIR / "missing_images_report.json"
    
    report_data = {
        'total_missing': len(missing_images),
        'by_batch': {},
        'images': []
    }
    
    for img_info in missing_images:
        batch_name = img_info['batch']
        if batch_name not in report_data['by_batch']:
            report_data['by_batch'][batch_name] = 0
        report_data['by_batch'][batch_name] += 1
        
        report_data['images'].append({
            'batch': batch_name,
            'filename': img_info['name']
        })
    
    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"✓ Saved report to {report_path}")

def main():
    print("=" * 60)
    print("Finding Missing Images from Attractions Assets")
    print("=" * 60)
    
    # Load Strapi media
    strapi_media_names = load_strapi_media()
    
    # Scan batch folders
    batch_images = scan_batch_folders()
    
    # Find missing images
    missing_images = find_missing_images(strapi_media_names, batch_images)
    
    # Display summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if missing_images:
        print(f"Total missing images: {len(missing_images)}")
        
        # Group by batch
        by_batch = {}
        for img in missing_images:
            batch = img['batch']
            if batch not in by_batch:
                by_batch[batch] = []
            by_batch[batch].append(img['name'])
        
        print("\nMissing images by batch:")
        for batch_name in sorted(by_batch.keys()):
            print(f"  {batch_name}: {len(by_batch[batch_name])} images")
            # Show first 5 examples
            for name in by_batch[batch_name][:5]:
                print(f"    - {name}")
            if len(by_batch[batch_name]) > 5:
                print(f"    ... and {len(by_batch[batch_name]) - 5} more")
        
        # Copy missing images
        copy_missing_images(missing_images)
        
        # Save report
        save_missing_images_report(missing_images)
    else:
        print("✓ All images have been uploaded to Strapi!")
    
    print("\n" + "=" * 60)
    print("✓ Script completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()


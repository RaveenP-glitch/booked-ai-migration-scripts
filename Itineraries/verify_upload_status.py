#!/usr/bin/env python3
"""
Script to verify upload status by comparing compressed-images folder with 
the updated all-images-without-iti.json file.
"""

import json
import os
import glob
from urllib.parse import urlparse

def normalize_filename(filename):
    """Normalize filename for comparison by removing extensions and converting to lowercase."""
    # Remove extension
    name_without_ext = os.path.splitext(filename)[0]
    # Convert to lowercase for case-insensitive comparison
    return name_without_ext.lower()

def get_filename_from_url(url):
    """Extract filename from URL."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If no filename in path, create one from the URL
    if not filename or '.' not in filename:
        # Use the last part of the path or a hash of the URL
        path_parts = parsed_url.path.strip('/').split('/')
        if path_parts and path_parts[-1]:
            filename = path_parts[-1] + '.jpg'  # Default to jpg
        else:
            filename = f"image_{hash(url) % 10000}.jpg"
    
    return filename

def find_matching_uploaded_image(compressed_filename, uploaded_images):
    """
    Find if a compressed image has already been uploaded to Strapi.
    Returns the uploaded image info if found, None otherwise.
    """
    compressed_normalized = normalize_filename(compressed_filename)
    
    for uploaded_img in uploaded_images:
        if 'name' in uploaded_img:
            uploaded_name = uploaded_img['name']
            uploaded_normalized = normalize_filename(uploaded_name)
            
            # Check for exact match
            if compressed_normalized == uploaded_normalized:
                return uploaded_img
            
            # Check if compressed filename is contained in uploaded name
            if compressed_normalized in uploaded_normalized:
                return uploaded_img
            
            # Check if uploaded name is contained in compressed filename
            if uploaded_normalized in compressed_normalized:
                return uploaded_img
    
    return None

def main():
    # Paths
    json_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/all-images-without-iti.json'
    compressed_dir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/compressed-images'
    missing_dir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/missing-images'
    report_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/upload_verification_report.txt'
    
    print("Verifying upload status...")
    
    # Load uploaded images from JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            uploaded_images = json.load(f)
        print(f"Loaded {len(uploaded_images)} uploaded images from JSON file")
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return
    
    # Get compressed images
    compressed_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.svg']:
        compressed_files.extend(glob.glob(os.path.join(compressed_dir, ext)))
    
    print(f"Found {len(compressed_files)} images in compressed-images folder")
    
    # Check if missing-images directory exists and get existing files
    existing_missing_files = set()
    if os.path.exists(missing_dir):
        existing_missing_files = set(os.listdir(missing_dir))
        print(f"Found {len(existing_missing_files)} files in missing-images folder")
    
    # Find upload status
    uploaded_images_found = []
    still_missing = []
    already_in_missing = []
    
    print("\nChecking each compressed image...")
    
    for i, compressed_file in enumerate(compressed_files, 1):
        compressed_filename = os.path.basename(compressed_file)
        
        # Check if this image has been uploaded
        uploaded_match = find_matching_uploaded_image(compressed_filename, uploaded_images)
        
        if uploaded_match:
            uploaded_images_found.append({
                'compressed_file': compressed_file,
                'compressed_name': compressed_filename,
                'uploaded_name': uploaded_match['name'],
                'uploaded_id': uploaded_match.get('id', 'N/A')
            })
        else:
            # Check if it's already in the missing-images folder
            if compressed_filename in existing_missing_files:
                already_in_missing.append({
                    'file': compressed_file,
                    'filename': compressed_filename
                })
            else:
                still_missing.append({
                    'file': compressed_file,
                    'filename': compressed_filename
                })
        
        # Progress indicator
        if i % 100 == 0:
            print(f"Processed {i}/{len(compressed_files)} - Uploaded: {len(uploaded_images_found)}, Missing: {len(still_missing)}, In missing folder: {len(already_in_missing)}")
    
    # Generate report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("UPLOAD STATUS VERIFICATION REPORT\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total compressed images: {len(compressed_files)}\n")
        f.write(f"Successfully uploaded to Strapi: {len(uploaded_images_found)}\n")
        f.write(f"Still missing (not uploaded): {len(still_missing)}\n")
        f.write(f"Already in missing-images folder: {len(already_in_missing)}\n")
        f.write(f"Total uploaded images in JSON: {len(uploaded_images)}\n\n")
        
        upload_percentage = (len(uploaded_images_found) / len(compressed_files)) * 100 if compressed_files else 0
        f.write(f"Upload completion rate: {upload_percentage:.1f}%\n\n")
        
        f.write("STILL MISSING IMAGES:\n")
        f.write("-" * 20 + "\n")
        for i, missing_img in enumerate(still_missing, 1):
            f.write(f"{i:4d}. {missing_img['filename']}\n")
        
        f.write(f"\nALREADY IN MISSING-IMAGES FOLDER:\n")
        f.write("-" * 35 + "\n")
        for i, existing_img in enumerate(already_in_missing[:20], 1):  # Show first 20
            f.write(f"{i:2d}. {existing_img['filename']}\n")
        
        if len(already_in_missing) > 20:
            f.write(f"... and {len(already_in_missing) - 20} more existing files\n")
        
        f.write(f"\nRECENTLY UPLOADED IMAGES (sample):\n")
        f.write("-" * 35 + "\n")
        for i, found_img in enumerate(uploaded_images_found[-20:], 1):  # Show last 20
            f.write(f"{i:2d}. {found_img['compressed_name']} -> {found_img['uploaded_name']} (ID: {found_img['uploaded_id']})\n")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"UPLOAD STATUS VERIFICATION COMPLETED!")
    print(f"Total compressed images: {len(compressed_files)}")
    print(f"Successfully uploaded: {len(uploaded_images_found)}")
    print(f"Still missing: {len(still_missing)}")
    print(f"Already in missing-images folder: {len(already_in_missing)}")
    print(f"Total uploaded images in JSON: {len(uploaded_images)}")
    
    upload_percentage = (len(uploaded_images_found) / len(compressed_files)) * 100 if compressed_files else 0
    print(f"Upload completion rate: {upload_percentage:.1f}%")
    
    print(f"\nReport saved to: {report_file}")
    
    if still_missing:
        print(f"\n⚠️  Still missing {len(still_missing)} images:")
        for i, missing_img in enumerate(still_missing[:10], 1):
            print(f"{i:2d}. {missing_img['filename']}")
        if len(still_missing) > 10:
            print(f"... and {len(still_missing) - 10} more")
    else:
        print(f"\n✅ All images have been uploaded to Strapi!")

if __name__ == "__main__":
    main()

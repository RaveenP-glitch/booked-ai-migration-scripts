#!/usr/bin/env python3
"""
Script to check for name conflicts between images already uploaded to Strapi
and images in the compressed-images folder.
"""

import json
import os
import glob
from collections import defaultdict

def extract_filename_from_path(filepath):
    """Extract just the filename from a file path."""
    return os.path.basename(filepath)

def normalize_filename(filename):
    """Normalize filename for comparison by removing extensions and converting to lowercase."""
    # Remove extension
    name_without_ext = os.path.splitext(filename)[0]
    # Convert to lowercase for case-insensitive comparison
    return name_without_ext.lower()

def main():
    # Paths
    json_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/all-images-without-iti.json'
    compressed_dir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/compressed-images'
    conflicts_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/name_conflicts_report.txt'
    
    print("Checking for name conflicts between Strapi images and compressed images...")
    
    # Load JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            strapi_images = json.load(f)
        print(f"Loaded {len(strapi_images)} images from Strapi JSON file")
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return
    
    # Get compressed images
    compressed_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.svg']:
        compressed_files.extend(glob.glob(os.path.join(compressed_dir, ext)))
    
    print(f"Found {len(compressed_files)} images in compressed-images folder")
    
    # Extract and normalize filenames from Strapi
    strapi_names = {}
    for img in strapi_images:
        if 'name' in img:
            original_name = img['name']
            normalized_name = normalize_filename(original_name)
            strapi_names[normalized_name] = {
                'original_name': original_name,
                'id': img.get('id', 'N/A'),
                'documentId': img.get('documentId', 'N/A')
            }
    
    # Extract and normalize filenames from compressed images
    compressed_names = {}
    for filepath in compressed_files:
        original_name = extract_filename_from_path(filepath)
        normalized_name = normalize_filename(original_name)
        compressed_names[normalized_name] = {
            'original_name': original_name,
            'filepath': filepath
        }
    
    # Find conflicts
    exact_conflicts = []
    potential_conflicts = []
    
    # Check for exact matches
    for normalized_name in strapi_names:
        if normalized_name in compressed_names:
            exact_conflicts.append({
                'normalized_name': normalized_name,
                'strapi_info': strapi_names[normalized_name],
                'compressed_info': compressed_names[normalized_name]
            })
    
    # Check for potential conflicts (similar names)
    for normalized_name in compressed_names:
        if normalized_name not in strapi_names:
            # Check if any Strapi name contains this name or vice versa
            for strapi_normalized in strapi_names:
                if (normalized_name in strapi_normalized or 
                    strapi_normalized in normalized_name) and len(normalized_name) > 10:  # Only check substantial matches
                    potential_conflicts.append({
                        'compressed_name': normalized_name,
                        'compressed_info': compressed_names[normalized_name],
                        'similar_strapi_name': strapi_normalized,
                        'strapi_info': strapi_names[strapi_normalized]
                    })
    
    # Generate report
    with open(conflicts_file, 'w', encoding='utf-8') as f:
        f.write("NAME CONFLICTS ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Strapi images analyzed: {len(strapi_images)}\n")
        f.write(f"Compressed images analyzed: {len(compressed_files)}\n")
        f.write(f"Exact name conflicts: {len(exact_conflicts)}\n")
        f.write(f"Potential conflicts: {len(potential_conflicts)}\n\n")
        
        if exact_conflicts:
            f.write("EXACT NAME CONFLICTS:\n")
            f.write("-" * 30 + "\n")
            for i, conflict in enumerate(exact_conflicts, 1):
                f.write(f"{i}. Normalized name: {conflict['normalized_name']}\n")
                f.write(f"   Strapi: {conflict['strapi_info']['original_name']} (ID: {conflict['strapi_info']['id']})\n")
                f.write(f"   Compressed: {conflict['compressed_info']['original_name']}\n")
                f.write("\n")
        else:
            f.write("✅ NO EXACT NAME CONFLICTS FOUND\n\n")
        
        if potential_conflicts:
            f.write("POTENTIAL CONFLICTS (Similar Names):\n")
            f.write("-" * 40 + "\n")
            for i, conflict in enumerate(potential_conflicts[:20], 1):  # Show first 20
                f.write(f"{i}. Compressed: {conflict['compressed_info']['original_name']}\n")
                f.write(f"   Similar Strapi: {conflict['strapi_info']['original_name']} (ID: {conflict['strapi_info']['id']})\n")
                f.write("\n")
            
            if len(potential_conflicts) > 20:
                f.write(f"... and {len(potential_conflicts) - 20} more potential conflicts\n")
        else:
            f.write("✅ NO POTENTIAL CONFLICTS FOUND\n\n")
        
        # Summary
        f.write("SUMMARY:\n")
        f.write("-" * 10 + "\n")
        if exact_conflicts:
            f.write(f"❌ {len(exact_conflicts)} exact name conflicts found. These will cause upload issues.\n")
        else:
            f.write("✅ No exact name conflicts found.\n")
        
        if potential_conflicts:
            f.write(f"⚠️  {len(potential_conflicts)} potential conflicts found. Review these manually.\n")
        else:
            f.write("✅ No potential conflicts found.\n")
        
        f.write(f"\nTotal compressed images: {len(compressed_files)}\n")
        f.write(f"Images safe to upload: {len(compressed_files) - len(exact_conflicts)}\n")
    
    # Print summary to console
    print(f"\n{'='*60}")
    print(f"CONFLICT ANALYSIS COMPLETED!")
    print(f"Strapi images: {len(strapi_images)}")
    print(f"Compressed images: {len(compressed_files)}")
    print(f"Exact conflicts: {len(exact_conflicts)}")
    print(f"Potential conflicts: {len(potential_conflicts)}")
    
    if exact_conflicts:
        print(f"\n❌ {len(exact_conflicts)} EXACT CONFLICTS FOUND!")
        print("These images will cause upload issues:")
        for i, conflict in enumerate(exact_conflicts[:5], 1):
            print(f"{i}. {conflict['compressed_info']['original_name']} (conflicts with Strapi ID: {conflict['strapi_info']['id']})")
        if len(exact_conflicts) > 5:
            print(f"... and {len(exact_conflicts) - 5} more")
    else:
        print(f"\n✅ NO EXACT CONFLICTS FOUND!")
        print("All compressed images can be uploaded without name conflicts.")
    
    if potential_conflicts:
        print(f"\n⚠️  {len(potential_conflicts)} potential conflicts found (similar names)")
        print("Review these manually to ensure they're different images.")
    
    print(f"\nDetailed report saved to: {conflicts_file}")

if __name__ == "__main__":
    main()

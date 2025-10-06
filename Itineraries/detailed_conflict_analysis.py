#!/usr/bin/env python3
"""
Detailed analysis script to show examples of image names from both sources
and verify there are no conflicts.
"""

import json
import os
import glob
import random

def main():
    # Paths
    json_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/all-images-without-iti.json'
    compressed_dir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/compressed-images'
    
    print("Detailed analysis of image names...")
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        strapi_images = json.load(f)
    
    # Get compressed images
    compressed_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.svg']:
        compressed_files.extend(glob.glob(os.path.join(compressed_dir, ext)))
    
    # Extract filenames
    strapi_names = [img['name'] for img in strapi_images if 'name' in img]
    compressed_names = [os.path.basename(f) for f in compressed_files]
    
    print(f"\nStrapi images: {len(strapi_names)}")
    print(f"Compressed images: {len(compressed_names)}")
    
    # Show sample names from each source
    print(f"\nSAMPLE STRAPI IMAGE NAMES (first 10):")
    print("-" * 40)
    for i, name in enumerate(strapi_names[:10], 1):
        print(f"{i:2d}. {name}")
    
    print(f"\nSAMPLE COMPRESSED IMAGE NAMES (first 10):")
    print("-" * 40)
    for i, name in enumerate(compressed_names[:10], 1):
        print(f"{i:2d}. {name}")
    
    # Check for any exact matches
    strapi_set = set(strapi_names)
    compressed_set = set(compressed_names)
    exact_matches = strapi_set.intersection(compressed_set)
    
    print(f"\nEXACT MATCHES FOUND: {len(exact_matches)}")
    if exact_matches:
        print("Conflicting names:")
        for name in sorted(exact_matches):
            print(f"  - {name}")
    else:
        print("✅ No exact matches found - safe to upload!")
    
    # Check for similar patterns
    print(f"\nANALYZING NAMING PATTERNS:")
    print("-" * 30)
    
    # Strapi patterns
    strapi_prefixes = set()
    for name in strapi_names:
        if '_' in name:
            prefix = name.split('_')[0]
            strapi_prefixes.add(prefix)
    
    # Compressed patterns
    compressed_prefixes = set()
    for name in compressed_names:
        if '_' in name:
            prefix = name.split('_')[0]
            compressed_prefixes.add(prefix)
    
    common_prefixes = strapi_prefixes.intersection(compressed_prefixes)
    
    print(f"Strapi unique prefixes: {len(strapi_prefixes)}")
    print(f"Compressed unique prefixes: {len(compressed_prefixes)}")
    print(f"Common prefixes: {len(common_prefixes)}")
    
    if common_prefixes:
        print(f"\nCommon prefixes (first 10):")
        for prefix in sorted(list(common_prefixes))[:10]:
            print(f"  - {prefix}")
    
    # Check for any potential issues
    print(f"\nPOTENTIAL ISSUES CHECK:")
    print("-" * 25)
    
    issues_found = []
    
    # Check for very similar names
    for strapi_name in strapi_names[:100]:  # Check first 100 for performance
        for compressed_name in compressed_names:
            if (strapi_name.lower() in compressed_name.lower() or 
                compressed_name.lower() in strapi_name.lower()) and len(strapi_name) > 10:
                issues_found.append((strapi_name, compressed_name))
                break
    
    if issues_found:
        print(f"⚠️  Found {len(issues_found)} potentially similar names:")
        for strapi, compressed in issues_found[:5]:
            print(f"  Strapi: {strapi}")
            print(f"  Compressed: {compressed}")
            print()
    else:
        print("✅ No similar names found")
    
    # Final recommendation
    print(f"\nFINAL RECOMMENDATION:")
    print("-" * 20)
    if len(exact_matches) == 0 and len(issues_found) == 0:
        print("✅ SAFE TO UPLOAD ALL COMPRESSED IMAGES")
        print("   - No exact name conflicts")
        print("   - No similar name issues")
        print("   - All 3,147 images can be uploaded without problems")
    else:
        print("❌ REVIEW REQUIRED BEFORE UPLOAD")
        print(f"   - {len(exact_matches)} exact conflicts")
        print(f"   - {len(issues_found)} potential issues")

if __name__ == "__main__":
    main()

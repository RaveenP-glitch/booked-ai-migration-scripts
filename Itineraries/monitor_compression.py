#!/usr/bin/env python3
"""
Script to monitor the compression progress.
"""

import os
import time

def main():
    source_dir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/assets'
    output_dir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/compressed-images'
    
    # Count source images
    source_files = []
    for ext in ['*.jpeg', '*.jpg']:
        source_files.extend([f for f in os.listdir(source_dir) if f.lower().endswith(ext.replace('*', ''))])
    
    total_source = len(source_files)
    
    print(f"Monitoring compression progress...")
    print(f"Total source images: {total_source}")
    print(f"Source directory: {source_dir}")
    print(f"Output directory: {output_dir}")
    print(f"")
    
    while True:
        try:
            # Count processed images
            if os.path.exists(output_dir):
                processed_files = []
                for ext in ['*.jpeg', '*.jpg']:
                    processed_files.extend([f for f in os.listdir(output_dir) if f.lower().endswith(ext.replace('*', ''))])
                
                processed_count = len(processed_files)
                progress = (processed_count / total_source) * 100
                
                print(f"\rProgress: {processed_count}/{total_source} ({progress:.1f}%)", end="", flush=True)
                
                if processed_count >= total_source:
                    print(f"\n\nCompression completed! All {total_source} images processed.")
                    break
            else:
                print(f"\rWaiting for output directory to be created...", end="", flush=True)
        
        except KeyboardInterrupt:
            print(f"\n\nMonitoring stopped by user.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break
        
        time.sleep(2)  # Check every 2 seconds

if __name__ == "__main__":
    main()


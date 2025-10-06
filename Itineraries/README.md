# Itineraries Image Download

This directory contains scripts to extract and download images from the Itineraries CSV file for Strapi migration.

## Files Created

1. **`all_image_urls.txt`** - Contains all 3,147 unique image URLs extracted from the CSV
2. **`extract_image_urls.py`** - Script to extract image URLs from the CSV file
3. **`download_images.py`** - Main script to download all images
4. **`test_download.py`** - Test script to download first 5 images only
5. **`assets/`** - Directory where downloaded images are stored

## Usage

### Step 1: Extract Image URLs (Already Done)
```bash
python3 extract_image_urls.py
```
This creates `all_image_urls.txt` with all unique image URLs found in the CSV.

### Step 2: Test Download (Optional)
```bash
python3 test_download.py
```
Downloads the first 5 images to verify the process works correctly.

### Step 3: Download All Images
```bash
python3 download_images.py
```
Downloads all 3,147 images to the `assets/` directory.

## Features

- **Duplicate Detection**: Uses set to avoid downloading duplicate URLs
- **Error Handling**: Gracefully handles network errors and invalid URLs
- **Progress Tracking**: Shows progress every 50 downloads
- **File Validation**: Checks content-type to ensure files are actually images
- **Filename Sanitization**: Cleans filenames to be filesystem-safe
- **Resume Support**: Skips already downloaded files
- **Statistics**: Provides detailed download statistics

## Image Sources

All images are hosted on `cdn.prod.website-files.com` (Webflow CDN) and are primarily:
- Thumbnail images
- Main images  
- Itinerary images
- Images embedded in HTML content

## Download Statistics

- **Total URLs Found**: 3,147
- **All from Webflow CDN**: 3,147 URLs
- **Test Download**: 5/5 successful (100% success rate)
- **Average File Size**: ~2MB per image

## Notes

- The script includes a small delay (0.1s) between downloads to be respectful to the server
- Failed downloads can be retried by running the script again (it will skip already downloaded files)
- All images maintain their original filenames from the CDN
- The script uses a proper User-Agent header to avoid blocking


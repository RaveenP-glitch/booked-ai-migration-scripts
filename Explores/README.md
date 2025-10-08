# Explores Image Migration

This directory contains scripts and files for migrating explore entries and their associated images.

## Files

- `Booked (Live) - Explores-all.csv` - The main CSV file containing 1334 explore entries
- `all_image_urls.txt` - Extracted list of 1334 unique image URLs from the CSV
- `extract_image_urls.py` - Script to extract image URLs from the CSV file
- `download_images.py` - Script to download all images to the assets folder
- `assets/` - Directory where downloaded images will be stored

## Usage

### 1. Extract Image URLs
```bash
python3 extract_image_urls.py
```
This will read the CSV file and extract all image URLs from the 'Image' and 'Author Pic' columns, saving them to `all_image_urls.txt`.

### 2. Download Images
```bash
python3 download_images.py
```
This will download all images from the URLs list to the `assets/` folder. The script includes:
- Progress tracking
- Error handling
- Duplicate filename resolution
- File size reporting
- Respectful rate limiting

## CSV Analysis

- **Total entries**: 1334 (confirmed)
- **Total lines**: 1335 (including header)
- **Image URLs found**: 1334 unique URLs
- **Columns with images**: 
  - `Image` - Main explore image
  - `Author Pic` - Author profile picture

## Features

- **Duplicate handling**: Automatically handles duplicate filenames
- **Error resilience**: Continues downloading even if some images fail
- **Progress tracking**: Shows download progress and ETA
- **File validation**: Checks content types and validates URLs
- **Organized output**: All images saved to `assets/` directory


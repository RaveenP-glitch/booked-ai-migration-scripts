# Attractions Missing Images Summary

## Overview
This document summarizes the process of identifying and organizing missing images from the Attractions migration that were not uploaded to Strapi.

## Process Completed

### 1. Fetched Current Strapi Media Library
- **Script Used**: `Graphql-asset-manager/fetch-media-rest.js`
- **Total Media Assets in Strapi**: 36,577 files
- **Unique Media Names**: 34,866 files
- **Updated File**: `Graphql-asset-manager/media-ids-and-names.json`

### 2. Scanned Local Attractions Assets
- **Location**: `Attractions/assets/batch_1` through `batch_12`
- **Total Local Images**: 14,998 images across 12 batch folders

### 3. Identified Missing Images
- **Total Missing**: 2,431 images
- **Missing from**:
  - `batch_5`: 985 images (78.8% of batch)
  - `batch_6`: 1,105 images (88.4% of batch)
  - `batch_7`: 127 images (10.2% of batch)
  - `batch_8`: 213 images (17.0% of batch)
  - `batch_10`: 1 image (0.08% of batch)

### 4. Organized Missing Images
- **New Directory Created**: `Attractions/assets/missing_images/`
- **Structure**: Organized into subdirectories by batch (batch_5, batch_6, batch_7, batch_8, batch_10)
- **Report Generated**: `Attractions/assets/missing_images_report.json`

## Missing Images Breakdown

| Batch | Missing Images | Percentage of Batch |
|-------|---------------|---------------------|
| batch_1 | 0 | 0% ✓ |
| batch_2 | 0 | 0% ✓ |
| batch_3 | 0 | 0% ✓ |
| batch_4 | 0 | 0% ✓ |
| batch_5 | 985 | 78.8% ⚠️ |
| batch_6 | 1,105 | 88.4% ⚠️ |
| batch_7 | 127 | 10.2% ⚠️ |
| batch_8 | 213 | 17.0% ⚠️ |
| batch_9 | 0 | 0% ✓ |
| batch_10 | 1 | 0.08% ⚠️ |
| batch_11 | 0 | 0% ✓ |
| batch_12 | 0 | 0% ✓ |
| **Total** | **2,431** | **16.2%** |

## Next Steps

### To Upload Missing Images:

1. **Upload batch_5 images** (985 images)
   - Location: `Attractions/assets/missing_images/batch_5/`
   - Priority: HIGH (most missing images)

2. **Upload batch_6 images** (1,105 images)
   - Location: `Attractions/assets/missing_images/batch_6/`
   - Priority: HIGH (most missing images)

3. **Upload batch_8 images** (213 images)
   - Location: `Attractions/assets/missing_images/batch_8/`
   - Priority: MEDIUM

4. **Upload batch_7 images** (127 images)
   - Location: `Attractions/assets/missing_images/batch_7/`
   - Priority: MEDIUM

5. **Upload batch_10 image** (1 image)
   - Location: `Attractions/assets/missing_images/batch_10/`
   - Priority: LOW
   - Note: Only 1 image with a very long URL-encoded filename

### Verification After Upload:
Run the following command to verify all images have been uploaded:
```bash
cd /Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Attractions
python3 find_missing_images.py
```

If successful, it should report: "✓ All images have been uploaded to Strapi!"

## Files Generated

1. **find_missing_images.py** - Python script to identify missing images
2. **missing_images_report.json** - Detailed JSON report of all missing images
3. **missing_images/** - Directory containing all missing images organized by batch
4. **MISSING_IMAGES_SUMMARY.md** - This summary document

## Analysis

### Upload Success Rate
- **Successfully Uploaded**: 12,567 images (83.8%)
- **Not Uploaded**: 2,431 images (16.2%)

### Batches with Issues
The following batches had significant upload failures:
- **batch_5** and **batch_6**: Nearly 80-88% of images missing, suggesting the upload may have failed partway through
- **batch_7** and **batch_8**: Partial failures (10-17% missing)
- **batch_10**: Only 1 image missing (likely a filename encoding issue)

### Recommendation
Upload the missing images in the following order:
1. batch_6 (1,105 images) - highest count
2. batch_5 (985 images) - second highest
3. batch_8 (213 images)
4. batch_7 (127 images)
5. batch_10 (1 image - may need special handling due to URL-encoded filename)

---
*Generated: October 15, 2025*
*Script: find_missing_images.py*


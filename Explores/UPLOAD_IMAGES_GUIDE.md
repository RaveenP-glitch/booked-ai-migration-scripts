# Explores Images Upload Guide

This guide explains how to upload the Explores images to Strapi and map them for the Postman collection.

## Problem

The Explores entries reference images that are not yet in Strapi. These images are located in the `compressed-images/` folder but haven't been uploaded yet. Without uploading them first, the Postman collection won't be able to attach the images to the entries.

## Solution Overview

1. Upload all images from `compressed-images/` to Strapi
2. Fetch the media IDs from Strapi
3. Create a local media mapping file
4. Regenerate the Postman collection with correct media IDs

## Step-by-Step Instructions

### Step 1: Upload Images to Strapi

You have two options:

#### Option A: Using Strapi Admin Panel (Manual)
1. Log into your Strapi admin panel
2. Go to **Media Library**
3. Click **Add new assets**
4. Upload all images from `compressed-images/` folder
   - You can select multiple files at once
   - There are ~1335 images total

⚠️ **Note**: This method works but is time-consuming for large batches.

#### Option B: Using Bulk Upload Script (Recommended)

Create a bulk upload script:

```bash
# Create upload script
touch upload_images_to_strapi.js
```

```javascript
// upload_images_to_strapi.js
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

const STRAPI_URL = 'http://localhost:1337';
const API_TOKEN = 'YOUR_API_TOKEN_HERE';
const IMAGES_DIR = path.join(__dirname, 'compressed-images');

async function uploadImage(filePath) {
    const form = new FormData();
    form.append('files', fs.createReadStream(filePath));
    
    try {
        const response = await fetch(`${STRAPI_URL}/api/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_TOKEN}`,
                ...form.getHeaders()
            },
            body: form
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data[0];
    } catch (error) {
        console.error(`Failed to upload ${path.basename(filePath)}:`, error.message);
        return null;
    }
}

async function uploadAllImages() {
    const files = fs.readdirSync(IMAGES_DIR)
        .filter(file => file.endsWith('.jpeg') || file.endsWith('.jpg') || file.endsWith('.png'));
    
    console.log(`Found ${files.length} images to upload`);
    
    let uploaded = 0;
    let failed = 0;
    
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const filePath = path.join(IMAGES_DIR, file);
        
        console.log(`Uploading ${i + 1}/${files.length}: ${file}`);
        const result = await uploadImage(filePath);
        
        if (result) {
            uploaded++;
        } else {
            failed++;
        }
        
        // Rate limiting - wait 100ms between uploads
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    console.log(`\n✅ Uploaded: ${uploaded}`);
    console.log(`❌ Failed: ${failed}`);
}

uploadAllImages().catch(console.error);
```

To use this script:
```bash
npm install form-data
node upload_images_to_strapi.js
```

### Step 2: Fetch Media IDs from Strapi

Once images are uploaded, fetch their IDs:

```bash
node fetch-strapi-media.js YOUR_API_TOKEN_HERE
```

This will:
- Fetch all media from Strapi
- Create `media-ids-and-names.json` in the Explores folder
- Show which local images were found/missing in Strapi

**Example output:**
```
🚀 Starting Strapi Media Fetcher...

🔍 Fetching media from Strapi...
   Page 1: 100 media items fetched so far...
   Page 2: 200 media items fetched so far...
   ...
✅ Total media items fetched: 1500

✅ Mapping file created: media-ids-and-names.json
   Contains 1500 media items

📊 Local images in compressed-images: 1335
✅ Found 1335 images in Strapi
❌ Missing 0 images in Strapi
```

### Step 3: Regenerate Postman Collection

With the media mapping file in place, regenerate the collection:

```bash
node generate_postman_collection.js
```

This will now use the local `media-ids-and-names.json` file and properly map all images.

**Expected output:**
```
🚀 Starting Explores Postman Collection Generator...

Loading schema...
Loading media mapping...
   Using: /path/to/Explores/media-ids-and-names.json
Loading CSV data...
Loaded 1334 entries from CSV
Media map has 1335 entries
City blogs map has 4039 entries

✅ Mapping Success Rates:
   Images: 1334/1334 (100.0%)
   Author Pics: 1334/1334 (100.0%)
   City Blogs: 1200/1334 (89.9%)
```

### Step 4: Import Updated Collections to Postman

1. In Postman, delete the old Explores collections
2. Import the newly generated collections:
   - `Strapi_Explores_Test_5_Collection.postman_collection.json`
   - `Strapi_Explores_Complete_Collection.postman_collection.json`
3. Test with the 5-entry collection first
4. Run the complete collection once verified

## Verification

To verify images are properly attached:

1. Run the test collection (5 entries)
2. In Strapi admin, check one of the created Explores entries
3. Verify that the **Image** and **Author_Pic** fields are populated
4. If they are, proceed with the full collection

## Troubleshooting

### Issue: No images found in Strapi

**Cause**: Images haven't been uploaded yet

**Solution**: Complete Step 1 first

### Issue: Some images still missing after upload

**Cause**: Upload may have failed for some images

**Solution**: 
1. Check the upload script output for errors
2. Re-run the upload script (it will skip existing images)
3. Re-run the fetch script to update the mapping

### Issue: Images uploaded but still not mapped

**Cause**: Filename mismatch between local and Strapi

**Solution**:
1. Check `media-ids-and-names.json` for actual filenames in Strapi
2. Compare with filenames in CSV
3. The generator will try multiple matching strategies:
   - Exact filename match
   - Match without extension
   - Match by ID part (before first underscore)
   - Partial/fuzzy match

### Issue: Rate limiting errors during upload

**Cause**: Uploading too fast

**Solution**: Increase the delay in the upload script (change from 100ms to 500ms)

## Current Status

Based on the initial generation:

- ❌ **0/1334 images mapped** - Images need to be uploaded to Strapi first
- ✅ **City Blogs mapped** - ~90% success rate
- ✅ **All other fields** - Working correctly

## Next Steps

1. ⏳ Upload images to Strapi (Step 1)
2. ⏳ Fetch media IDs (Step 2)
3. ⏳ Regenerate collections (Step 3)
4. ⏳ Test and upload to Strapi (Step 4)

## Alternative: Manual Image Upload

If you prefer to map images after creating the entries:

1. Create entries without images first
2. Upload images to Strapi
3. Manually attach images to each entry in Strapi admin

⚠️ **Not recommended** - This is very time-consuming for 1334 entries.

## Files Generated

- `media-ids-and-names.json` - Media mapping file (created after Step 2)
- `Strapi_Explores_Test_5_Collection.postman_collection.json` - Test collection
- `Strapi_Explores_Complete_Collection.postman_collection.json` - Full collection

## Support

If you encounter issues:
1. Check Strapi server logs
2. Verify API token permissions (needs upload access)
3. Check available disk space in Strapi
4. Review the fetch-strapi-media.js output for errors



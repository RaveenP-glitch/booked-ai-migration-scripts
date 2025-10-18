# Explores Migration - Quick Start

## The Issue

Your Explores entries reference **1,335 images** that aren't in Strapi yet. These images are in the `compressed-images/` folder and need to be uploaded first before the Postman collection can properly attach them to the entries.

## The Solution (3 Simple Steps)

### Step 1: Upload Images to Strapi

```bash
cd /Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Explores
node upload_images_to_strapi.js YOUR_API_TOKEN
```

⏱️ Takes ~15-20 minutes

✅ Uploads all 1,335 images to Strapi  
✅ Skips already uploaded images  
✅ Shows progress and reports errors

### Step 2: Fetch Media IDs

```bash
node fetch-strapi-media.js YOUR_API_TOKEN
```

⏱️ Takes ~1 minute

✅ Creates `media-ids-and-names.json` mapping file  
✅ Shows which images were found/missing

### Step 3: Regenerate Collections

```bash
node generate_postman_collection.js
```

⏱️ Takes <1 minute

✅ Generates collections with proper image IDs  
✅ Maps all fields correctly  
✅ Creates test (5 entries) and full (1,334 entries) collections

### Step 4: Import and Run in Postman

1. Import `collection/Strapi_Explores_Test_5_Collection.postman_collection.json`
2. Import `collection/Strapi_Explores_Environment.postman_environment.json`
3. Set your `apiToken` in the environment
4. Run the test collection (5 entries)
5. Verify in Strapi admin
6. Run the complete collection (1,334 entries)

## Files You'll Need

### Input Files (Already Have)
- ✅ `Booked (Live) - Explores-all.csv` - Source data
- ✅ `compressed-images/` - All images ready
- ✅ `collection/schema.json` - Strapi schema

### Scripts (Already Created)
- ✅ `upload_images_to_strapi.js` - Bulk image uploader
- ✅ `fetch-strapi-media.js` - Media ID fetcher
- ✅ `generate_postman_collection.js` - Collection generator

### Output Files (Will Be Created)
- ⏳ `media-ids-and-names.json` - After Step 2
- ⏳ `Strapi_Explores_Test_5_Collection.postman_collection.json` - After Step 3
- ⏳ `Strapi_Explores_Complete_Collection.postman_collection.json` - After Step 3

## What Gets Mapped

### ✅ Fully Mapped
- All string fields (Title, Location, Author, etc.)
- Number_of_Spots (extracted from text)
- Sitemap_Indexing (boolean)
- City_blogs (oneToOne relationship, ~90% mapped)

### ⏳ After Following Steps Above
- Image (media field)
- Author_Pic (media field)

### ⏳ Not Mapped Yet
- Hotels (will be mapped later)
- Restaurants (will be mapped later)
- Attractions (will be mapped later)
- Itineraries (will be mapped later)

## Common Issues

### "No media ID found for image"
**Cause**: Images not uploaded yet  
**Fix**: Run Step 1 first

### "ValidationError: Invalid key"
**Cause**: Was sending null relationships  
**Status**: ✅ Already fixed in the generator

### Upload fails with rate limit error
**Fix**: The script already includes rate limiting (300ms delay). If still failing, edit `upload_images_to_strapi.js` and increase the delay.

## Time Estimate

| Step | Time |
|------|------|
| Step 1: Upload images | ~15-20 minutes |
| Step 2: Fetch IDs | ~1 minute |
| Step 3: Generate collections | <1 minute |
| Step 4: Test collection | ~1 minute |
| Step 5: Full upload | ~10-15 minutes |
| **Total** | **~30-40 minutes** |

## Ready to Start?

```bash
cd /Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Explores

# Step 1: Upload images
node upload_images_to_strapi.js YOUR_API_TOKEN

# Step 2: Fetch IDs  
node fetch-strapi-media.js YOUR_API_TOKEN

# Step 3: Generate collections
node generate_postman_collection.js

# Done! Import to Postman and run.
```

## Need Help?

- **Detailed guides**: See `README.md` and `UPLOAD_IMAGES_GUIDE.md`
- **Postman help**: See `POSTMAN_COLLECTION_README.md`
- **Strapi logs**: Check your Strapi server logs for errors
- **Script output**: All scripts provide detailed progress and error messages

---

**Replace `YOUR_API_TOKEN`** with your actual Strapi API token!



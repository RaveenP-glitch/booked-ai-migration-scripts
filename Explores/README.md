# Explores Content Migration to Strapi

Complete solution for migrating Explores content entries to Strapi, including image uploads and relationship mapping.

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `generate_postman_collection.js` | Main script to generate Postman collections from CSV |
| `upload_images_to_strapi.js` | Bulk upload all images to Strapi |
| `fetch-strapi-media.js` | Fetch media IDs from Strapi and create mapping |
| `POSTMAN_COLLECTION_README.md` | Guide for using Postman collections |
| `UPLOAD_IMAGES_GUIDE.md` | Detailed image upload instructions |
| `Booked (Live) - Explores-all.csv` | Source data (1334 entries) |
| `collection/schema.json` | Strapi schema definition |
| `compressed-images/` | All images ready for upload (~1335 files) |

## 🚀 Quick Start

### Prerequisites

- Node.js installed
- Strapi instance running
- API token with upload and create permissions
- All images in `compressed-images/` folder

### Complete Workflow

```bash
# 1. Upload all images to Strapi
node upload_images_to_strapi.js YOUR_API_TOKEN

# 2. Fetch media IDs and create mapping
node fetch-strapi-media.js YOUR_API_TOKEN

# 3. Generate Postman collections
node generate_postman_collection.js

# 4. Import collections to Postman and run
```

## 📊 Data Mapping

### Fields Mapped from CSV

| CSV Column | Strapi Field | Type | Notes |
|------------|--------------|------|-------|
| Title | Title | string | Required, unique |
| Slug | Slug | uid | Auto-generated from Title |
| Overview | Overview | text | - |
| Location | Location | string | - |
| # of spots | Number_of_Spots | integer | Extracted from text |
| Image | Image | media | Mapped via media IDs |
| Style | Style | string | e.g., "Adventure", "Foodie's Love" |
| Duration | Duration | string | e.g., "5 days" |
| Author | Author | string | - |
| Author Pic | Author_Pic | media | Mapped via media IDs |
| Min read | Min_Read | string | e.g., "3 min read" |
| Cost | Cost | string | e.g., "$", "$$", "$$$" |
| City Name | City_Name | string | - |
| Main Title | Main_Title | string | - |
| - | Sitemap_Indexing | boolean | Default: true |
| City Blogs | City_blogs | relation (oneToOne) | Mapped by slug |
| Hotels | Hotels | relation (oneToMany) | Not mapped yet (null) |
| Restaurants | Restaurants | relation (oneToMany) | Not mapped yet (null) |
| Attractions | Attractions | relation (oneToMany) | Not mapped yet (null) |
| Itineraries | Itineraries | relation (oneToMany) | Not mapped yet (null) |

## 🔧 Script Details

### generate_postman_collection.js

**Purpose**: Converts CSV data to Postman collections

**Features**:
- Parses CSV with proper quote handling
- Maps images via media-ids-and-names.json
- Maps City Blogs by slug
- Generates test collection (5 entries) and full collection (1334 entries)
- Provides detailed statistics and warnings

**Usage**:
```bash
node generate_postman_collection.js
```

**Output**:
- `collection/Strapi_Explores_Test_5_Collection.postman_collection.json`
- `collection/Strapi_Explores_Complete_Collection.postman_collection.json`
- `collection/Strapi_Explores_Environment.postman_environment.json`

### upload_images_to_strapi.js

**Purpose**: Bulk upload images to Strapi

**Features**:
- Uploads all images from compressed-images/
- Skips already uploaded images
- Rate limiting to avoid overwhelming server
- Progress tracking and estimated time
- Retry failed uploads
- Detailed error reporting

**Usage**:
```bash
node upload_images_to_strapi.js YOUR_API_TOKEN [BASE_URL]
```

**Example**:
```bash
node upload_images_to_strapi.js abc123token http://localhost:1337
```

### fetch-strapi-media.js

**Purpose**: Fetch all media from Strapi and create mapping

**Features**:
- Paginates through all media in Strapi
- Creates media-ids-and-names.json mapping file
- Checks which local images are in Strapi
- Reports missing images

**Usage**:
```bash
node fetch-strapi-media.js YOUR_API_TOKEN [BASE_URL]
```

**Output**:
- `media-ids-and-names.json` - Complete media mapping

## 📝 Step-by-Step Migration

### Step 1: Prepare Images ✅

Images are already compressed and ready in `compressed-images/` folder.

**Status**: ✅ Complete (1335 images ready)

### Step 2: Upload Images to Strapi ✅

~~Run the bulk upload script:~~

```bash
node upload_images_to_strapi.js YOUR_API_TOKEN
```

**Expected time**: ~15-20 minutes for 1335 images

**What it does**:
- Uploads each image to Strapi
- Skips images that already exist
- Shows progress every 50 images
- Reports failures at the end

**Status**: ✅ **COMPLETE** - All images uploaded to Strapi

### Step 3: Fetch Media IDs ✅

~~After upload, fetch the media IDs:~~

```bash
node fetch-strapi-media.js YOUR_API_TOKEN
```

**What it does**:
- Fetches all media from Strapi API
- Creates `media-ids-and-names.json` mapping
- Verifies all local images are in Strapi
- Reports success rate

**Status**: ✅ **COMPLETE** - Using Graphql-asset-manager/media-ids-and-names.json

### Step 4: Generate Collections ✅

Generate Postman collections with proper media mapping:

```bash
node generate_postman_collection.js
```

**What it does**:
- Loads CSV data (1334 entries)
- Maps images using media-ids-and-names.json
- Maps City Blogs using all-city-blogs.json
- Generates test collection (5 entries)
- Generates complete collection (1334 entries)
- Shows mapping statistics

**Status**: ✅ **COMPLETE** - Collections generated with 99.4% image mapping success!

### Step 5: Test with 5 Entries ⏳

1. Import `Strapi_Explores_Test_5_Collection.postman_collection.json` to Postman
2. Import `Strapi_Explores_Environment.postman_environment.json`
3. Set your API token in the environment
4. Run the collection
5. Verify entries in Strapi admin panel

**Status**: ⏳ Pending

### Step 6: Upload All Entries ⏳

Once testing is successful:

1. Import `Strapi_Explores_Complete_Collection.postman_collection.json`
2. Run the collection
3. Monitor progress
4. Verify in Strapi admin panel

**Status**: ⏳ Pending

## 🎯 Current Status

### Completed ✅
- [x] CSV parsing and data extraction
- [x] Postman collection generation structure
- [x] City Blogs relationship mapping (99.2% success)
- [x] Image compression and preparation
- [x] Bulk upload script created
- [x] Media fetching script created
- [x] Documentation and guides
- [x] **Upload images to Strapi (ALL DONE!)**
- [x] **Fetch media IDs from Strapi (USING GRAPHQL-ASSET-MANAGER)**
- [x] **Regenerate collections with image mapping (99.4% SUCCESS!)**

### Ready for Upload! 🚀
- [ ] Test with 5 entries
- [ ] Upload all 1334 entries
- [ ] Map Hotels, Restaurants, Attractions, Itineraries relationships (future)

### Issues Fixed ✅
- [x] ValidationError for null relationship fields (fixed by omitting them)
- [x] CSV parsing with quoted fields
- [x] Media mapping strategy (multiple matching methods)

## 📈 Statistics

| Metric | Value |
|--------|-------|
| Total entries | 1,334 |
| Images to upload | ~1,335 |
| City Blogs mapped | ~90% |
| Fields per entry | 19 |
| Collection size | ~41,000 lines (complete) |

## 🔍 Troubleshooting

### Issue: Images not showing in entries

**Solution**: 
1. Verify images were uploaded (check Step 2)
2. Verify media mapping exists (check Step 3)
3. Regenerate collections (run Step 4 again)

### Issue: ValidationError on upload

**Solution**:
- Check API token permissions
- Verify Title is unique
- Review Strapi logs for detailed error

### Issue: Upload script fails

**Solution**:
- Check network connection
- Verify API token has upload permission
- Reduce rate limit (increase delay in script)
- Check Strapi disk space

## 📚 Additional Resources

- [POSTMAN_COLLECTION_README.md](./POSTMAN_COLLECTION_README.md) - Detailed Postman usage
- [UPLOAD_IMAGES_GUIDE.md](./UPLOAD_IMAGES_GUIDE.md) - Image upload instructions
- [collection/schema.json](./collection/schema.json) - Strapi schema definition

## 🆘 Support

If you encounter issues:

1. **Check the logs**: All scripts provide detailed output
2. **Review Strapi logs**: Check your Strapi server logs for errors
3. **Verify permissions**: Ensure API token has necessary permissions
4. **Check the guides**: Detailed guides are available for each step

## 🎉 Next Actions

Run these commands in order:

```bash
# 1. Upload images (required for image mapping)
node upload_images_to_strapi.js YOUR_API_TOKEN

# 2. Fetch media IDs (creates mapping file)
node fetch-strapi-media.js YOUR_API_TOKEN

# 3. Regenerate collections (with proper image mapping)
node generate_postman_collection.js

# 4. Import to Postman and test!
```

---

**Note**: Replace `YOUR_API_TOKEN` with your actual Strapi API token in all commands above.

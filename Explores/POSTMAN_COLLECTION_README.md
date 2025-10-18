# Explores Postman Collection for Strapi Migration

This document explains how to use the generated Postman collections to upload Explores content to Strapi.

## Overview

Two Postman collections have been generated:
1. **Strapi_Explores_Test_5_Collection.postman_collection.json** - Contains 5 test entries for validation
2. **Strapi_Explores_Complete_Collection.postman_collection.json** - Contains all 1334 entries from the CSV

## Files Generated

```
Explores/
├── collection/
│   ├── Strapi_Explores_Test_5_Collection.postman_collection.json
│   ├── Strapi_Explores_Complete_Collection.postman_collection.json
│   └── Strapi_Explores_Environment.postman_environment.json
├── generate_postman_collection.js
└── POSTMAN_COLLECTION_README.md (this file)
```

## Schema Mapping

The following fields are mapped from the CSV to Strapi according to the schema:

### String Fields
- **Title** - Unique required field
- **Slug** - Auto-generated from Title (UID field)
- **Overview** - Text description
- **Location** - Location string
- **Style** - Content style (e.g., "Adventure", "Foodie's Love")
- **Duration** - Duration string (e.g., "5 days")
- **Author** - Author name
- **Min_Read** - Reading time (e.g., "3 min read")
- **Cost** - Cost indicator (e.g., "$", "$$", "$$$")
- **City_Name** - City name
- **Main_Title** - Main title field

### Integer Field
- **Number_of_Spots** - Extracted from "# of spots" column (default: 0)

### Boolean Field
- **Sitemap_Indexing** - Always set to `true` (default per schema)

### Media Fields
- **Image** - Main image (mapped via media-ids-and-names.json)
- **Author_Pic** - Author picture (mapped via media-ids-and-names.json)

### Relationship Fields
- **Hotels** - Currently set to `null` (to be mapped later)
- **Restaurants** - Currently set to `null` (to be mapped later)
- **Attractions** - Currently set to `null` (to be mapped later)
- **Itineraries** - Currently set to `null` (to be mapped later)
- **City_blogs** - Mapped using all-city-blogs.json (oneToOne relationship)

## Data Mapping Statistics

Based on the generation run:

- **Total Entries**: 1334
- **CSV Source**: Booked (Live) - Explores-all.csv
- **Media Mappings**: Many images could not be found in media-ids-and-names.json
- **City Blogs Mappings**: Successfully mapped where slugs matched

⚠️ **Note**: Many Image and Author_Pic fields may be missing IDs because the images were not found in the media mapping file. You may need to:
1. Upload missing images to Strapi first
2. Update the media-ids-and-names.json file
3. Re-run the generation script

## How to Use

### Step 1: Import the Environment

1. Open Postman
2. Click on "Environments" (left sidebar)
3. Click "Import"
4. Select `Strapi_Explores_Environment.postman_environment.json`
5. Update the variables:
   - `baseUrl`: Your Strapi instance URL (e.g., `http://localhost:1337`)
   - `apiToken`: Your Strapi API token with permission to create Explores entries

### Step 2: Import the Test Collection

1. Click on "Collections" (left sidebar)
2. Click "Import"
3. Select `Strapi_Explores_Test_5_Collection.postman_collection.json`
4. Make sure the environment is selected (top-right dropdown)

### Step 3: Test with 5 Entries

1. Open the test collection
2. Run the collection using the "Run collection" button
3. Verify that all 5 entries are created successfully
4. Check your Strapi admin panel to ensure data is correct

### Step 4: Upload All Entries

Once you've verified the test collection works:

1. Import `Strapi_Explores_Complete_Collection.postman_collection.json`
2. Run the complete collection
3. Monitor for any errors
4. Verify entries in Strapi admin panel

## Expected Response

Successful POST requests should return:

```json
{
  "data": {
    "id": 123,
    "documentId": "abc123xyz",
    "Title": "Trip to Bangkok",
    "Slug": "trip-to-bangkok",
    ...
    "createdAt": "2025-10-17T...",
    "updatedAt": "2025-10-17T...",
    "publishedAt": null
  }
}
```

## Troubleshooting

### Issue: 401 Unauthorized
**Solution**: Check that your API token is correct and has proper permissions

### Issue: 400 Bad Request - Duplicate Title
**Solution**: The Title field is unique. You may need to delete existing entries or modify the data

### Issue: 400 Bad Request - Missing Required Fields
**Solution**: Verify that all required fields (Title) are present in the request body

### Issue: 500 Internal Server Error
**Solution**: Check Strapi logs for detailed error messages

### Issue: Images Not Showing
**Solution**: 
1. Check if the media IDs in the request match existing media in Strapi
2. Upload missing images to Strapi
3. Update media-ids-and-names.json
4. Re-run the generation script

## Re-generating Collections

If you need to regenerate the collections (e.g., after updating media mappings):

```bash
cd /Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Explores
node generate_postman_collection.js
```

The script will:
1. Load the CSV data
2. Load media mappings from `../Hotels/collection/media-ids-and-names.json`
3. Load City Blogs mappings from `../City-Blogs-manager/all-city-blogs.json`
4. Generate both test and complete collections
5. Display statistics and warnings

## Next Steps

1. ✅ Test with the 5-entry collection
2. ⏳ Upload all entries using the complete collection
3. ⏳ Map Hotels, Restaurants, Attractions, and Itineraries relationships
4. ⏳ Upload missing images and update media mappings
5. ⏳ Verify all data in Strapi admin panel

## Notes

- The script automatically handles CSV parsing with proper quote handling
- Media URL filenames are extracted and matched against the media mapping
- City Blogs are mapped by slug matching
- All text fields are properly escaped for JSON
- The generation script provides detailed warnings for missing mappings

## Support

If you encounter issues:
1. Check Strapi server logs
2. Verify your API token permissions
3. Review the schema in Strapi admin panel
4. Check the console output when running the generation script



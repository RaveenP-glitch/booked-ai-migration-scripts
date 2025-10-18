# Hotels Migration to Strapi - Postman Collections

This directory contains the generated Postman collections and supporting files for migrating hotel entries from the CSV export to Strapi.

## 📋 Overview

- **Total Hotels**: 3,971 entries
- **Source**: `Booked (Live) - Hotels-3971.csv`
- **Schema**: Defined in `schema.json`

## 📁 Files

### Postman Collections

1. **`Strapi_Hotels_Test_5.postman_collection.json`**
   - Test collection with the first 5 hotel entries
   - Use this to verify the migration process before running the complete collection

2. **`Strapi_Hotels_Complete.postman_collection.json`**
   - Complete collection with all 3,971 hotel entries
   - Ready for bulk import into Strapi

### Environment File

3. **`Strapi_Hotels_Environment.postman_environment.json`**
   - Contains environment variables:
     - `BASE_URL`: Your Strapi instance URL (default: `http://localhost:1337`)
     - `API_TOKEN`: Your Strapi API authentication token

### Data Files

4. **`Strapi_Hotels_Test_5_data.json`**
   - Processed data for the test collection (first 5 hotels)
   - Useful for reviewing the data transformation

5. **`Strapi_Hotels_Complete_data.json`**
   - Processed data for all 3,971 hotels
   - Complete dataset in JSON format

### Scripts

6. **`generate_postman_collection.js`**
   - Node.js script that generates the Postman collections
   - Handles CSV parsing, image matching, attraction linking, and block content conversion

7. **`package.json`**
   - NPM package configuration with dependencies and scripts

## 🚀 Quick Start

### Prerequisites

1. Node.js installed on your system
2. Postman installed
3. Strapi instance running with the Hotels content type configured

### Setup

1. **Install dependencies:**
   ```bash
   cd Hotels/collection
   npm install
   ```

2. **Generate collections (if needed):**
   ```bash
   # Generate test collection (first 5 hotels)
   npm run test
   
   # Generate complete collection (all hotels)
   npm run generate
   ```

3. **Import into Postman:**
   - Open Postman
   - Click "Import" button
   - Select `Strapi_Hotels_Test_5.postman_collection.json` (for testing)
   - Select `Strapi_Hotels_Environment.postman_environment.json`

4. **Configure Environment:**
   - In Postman, select "Strapi Hotels Environment" from the environment dropdown
   - Edit the environment variables:
     - Set `BASE_URL` to your Strapi instance URL
     - Set `API_TOKEN` to your Strapi API token

5. **Run the Collection:**
   - Start with the test collection to verify everything works
   - Use Postman's Collection Runner to execute requests
   - Monitor for errors and adjust as needed
   - Once verified, run the complete collection

## 🔧 Data Processing

The generation script performs the following transformations:

### 1. Image Matching

Images are matched using multiple strategies:
- Exact filename match
- Hash-based matching (extracts 24-character MongoDB-style hashes)
- Partial hash matching
- URL parsing and cleanup

**Image Fields:**
- `Image`: Main hotel image
- `Photo1`, `Photo2`, `Photo3`: Individual photos
- `Photos`: Array of multiple photos

### 2. Block Content Conversion

HTML content is converted to Strapi's block format:

**Block Fields:**
- `Inner_Page`: Rich text content
- `Amenities`: List of amenities
- `Pros`: List of positive aspects
- `Cons`: List of negative aspects

**Conversion:**
- `<ul>/<li>` tags → List blocks with list-item children
- `<br>` tags → Multiple paragraph blocks
- HTML entities decoded (e.g., `&apos;` → `'`)

### 3. Nearby Attractions Linking

Hotels are linked to nearby attractions using:
- City-based matching (primary)
- Country-based matching (secondary)
- Maximum of 5 nearby attractions per hotel

**Source:** `Attractions-manager/all-attractions.json` (4,335 attractions)

### 4. Field Mapping

All schema fields are properly mapped:

**String Fields:**
- Name, Slug, Description, Formatted_Address
- Tag1, Tag2, Tag3
- City, Country
- Overview, Intro, Short_Summary
- Website, Phone_Number, Price
- Check_in, Check_out
- Review_Text, Review_Rating
- FAQ1-FAQ5
- Policies, Sustainability, Accessibility

**Numeric Fields:**
- Ratings (decimal)
- Review_Count (integer)

**Boolean Fields:**
- Sitemap_Indexing (default: true)

**Media Fields:**
- Image (single)
- Photo1, Photo2, Photo3 (single)
- Photos (multiple)

**Relation Fields:**
- Nearby_Attractions (oneToMany with attractions)

## 📊 Statistics

### Image Matching Results

The script successfully matched images from the `media-ids-and-names.json` file containing 156,022 media entries.

### Nearby Attractions

- **Source**: 4,335 attractions from `all-attractions.json`
- **Matching Strategy**: City-first, then country
- **Max per Hotel**: 5 attractions

### Data Quality

Review the generated `*_data.json` files to verify:
- Image IDs are correctly mapped
- Block content is properly formatted
- Nearby attractions are relevant
- All required fields are populated

## 🧪 Testing Workflow

1. **Test Collection First:**
   ```bash
   npm run test
   ```
   This generates a collection with only 5 hotels for quick verification.

2. **Import and Run Test Collection:**
   - Import `Strapi_Hotels_Test_5.postman_collection.json`
   - Configure environment
   - Run the collection
   - Verify results in Strapi

3. **Check Test Results:**
   - Verify images are correctly linked
   - Check block content renders properly
   - Confirm nearby attractions are linked
   - Validate all field data

4. **Run Complete Collection:**
   - Once test is successful, import `Strapi_Hotels_Complete.postman_collection.json`
   - Use Collection Runner with appropriate delays between requests
   - Monitor progress and handle any errors

## 🛠️ Troubleshooting

### Missing Images

If images are not matching:
1. Check the image URL format in the CSV
2. Verify the media IDs in `media-ids-and-names.json`
3. Review the `findImageId` function in the script
4. Check Strapi media library

### Block Content Issues

If block content doesn't render:
1. Verify HTML structure in source CSV
2. Check the `parseHtmlToBlocks` function
3. Test with simple content first
4. Review Strapi block editor requirements

### Nearby Attractions Not Linking

If attractions aren't linking:
1. Verify attraction documentIds in `all-attractions.json`
2. Check city/country matching logic
3. Ensure attractions are already created in Strapi
4. Review the `findNearbyAttractions` function

### API Errors

If you get API errors:
1. Verify Strapi is running
2. Check API token permissions
3. Confirm Hotels content type exists
4. Review Strapi logs for details

## 📝 Schema Reference

The Hotels content type schema includes:

```
Hotels Collection Type
├── Basic Info
│   ├── Name (string, required)
│   ├── Slug (uid, auto-generated from Name)
│   ├── Description (text)
│   └── Formatted_Address (text)
├── Rating & Tags
│   ├── Ratings (decimal)
│   ├── Tag1, Tag2, Tag3 (string)
│   └── Review_Count (integer)
├── Content Blocks
│   ├── Inner_Page (blocks)
│   ├── Amenities (blocks)
│   ├── Pros (blocks)
│   └── Cons (blocks)
├── Media
│   ├── Image (media, single)
│   ├── Photo1, Photo2, Photo3 (media, single)
│   └── Photos (media, multiple)
├── Details
│   ├── Overview, Intro, Short_Summary (text)
│   ├── Website, Phone_Number, Price (string)
│   ├── Check_in, Check_out (string)
│   ├── Review_Text, Review_Rating (text/string)
│   └── FAQ1-FAQ5 (text)
├── Policies & Info
│   ├── Policies (text)
│   ├── Sustainability (text)
│   └── Accessibility (text)
├── Relations
│   ├── Explore (oneToOne with explores)
│   └── Nearby_Attractions (oneToMany with attractions)
├── Location
│   ├── City (string)
│   └── Country (string)
└── SEO
    └── Sitemap_Indexing (boolean, default: true)
```

## 🔄 Regenerating Collections

If you need to regenerate the collections after modifying the script:

```bash
# Regenerate test collection
npm run test

# Regenerate complete collection
npm run generate
```

**Note:** This will overwrite existing collection files.

## 📈 Performance Tips

### Postman Collection Runner

1. **Add Delays**: Set a delay between requests (e.g., 100-500ms) to avoid overwhelming Strapi
2. **Batch Processing**: Consider splitting the complete collection into smaller batches
3. **Monitor Progress**: Watch for failed requests and retry them
4. **Check Strapi**: Monitor Strapi server resources during bulk import

### Optimization

For large-scale imports:
- Consider using Strapi's bulk import API if available
- Implement retry logic for failed requests
- Use parallel processing with rate limiting
- Monitor database performance

## 🎯 Next Steps

After successful import:

1. **Verify Data**: Check a sample of hotels in Strapi admin
2. **Test Relations**: Ensure nearby attractions are correctly linked
3. **Review Media**: Verify all images are properly displayed
4. **Check SEO**: Confirm slugs are unique and properly formatted
5. **Test API**: Query the hotels API endpoint to verify data structure

## 📞 Support

If you encounter issues:
1. Review the generated `*_data.json` files
2. Check the console output for errors
3. Test with the 5-entry test collection first
4. Verify all dependencies are installed
5. Ensure Strapi schema matches the expected structure

## 🏁 Summary

- ✅ Test collection created with 5 entries
- ✅ Complete collection created with 3,971 entries
- ✅ Environment file configured
- ✅ Images matched from media library (156,022 entries)
- ✅ Nearby attractions linked (from 4,335 attractions)
- ✅ Block content properly formatted
- ✅ All schema fields mapped

Ready to import into Strapi! Start with the test collection to verify everything works correctly.


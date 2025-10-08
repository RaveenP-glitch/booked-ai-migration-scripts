# City Blogs Migration to Strapi

This directory contains scripts and resources for migrating City Blog entries from CSV format to Strapi CMS using Postman collections.

## Files Overview

### Generated Files
- `Strapi_City_Blogs_Sample_5_Collection.json` - Sample collection with the last 5 entries for testing (proper HTML to blocks conversion)
- `collection/Strapi_City_Blogs_Complete_Collection.postman_collection.json` - Complete collection for all 4,058 entries (58 MB)
- `collection-part-by-part/` - Complete collection split into 4 manageable parts:
  - `Strapi_City_Blogs_Part_1_of_4.postman_collection.json` - Entries 1-1,015 (17 MB)
  - `Strapi_City_Blogs_Part_2_of_4.postman_collection.json` - Entries 1,016-2,030 (15 MB)
  - `Strapi_City_Blogs_Part_3_of_4.postman_collection.json` - Entries 2,031-3,045 (15 MB)
  - `Strapi_City_Blogs_Part_4_of_4.postman_collection.json` - Entries 3,046-4,058 (11 MB)

### Source Files
- `Booked (Live) - City Blogs all.csv` - Source CSV data with all City Blog entries
- `collection/all-images-id-name.json` - Image mapping file with Strapi media IDs
- `collection/schema.json` - Strapi schema definition for City Blogs

### Scripts
- `generate_full_collection.js` - Script to generate the complete Postman collection

## Schema Mapping

The following CSV headers are mapped to Strapi schema fields:

| CSV Header | Strapi Field | Type | Description |
|------------|--------------|------|-------------|
| Name | Name | string | Blog entry name |
| Slug | Slug | uid | Auto-generated from Name if not provided |
| short description | Short_Description | text | Brief description |
| Thumbnail Image | Thumbnail_Image | media | Image ID from mapping |
| Main Image | Main_Image | media | Image ID from mapping |
| Blog Title | Blog_Title | text | Blog title |
| Blog Intro | Blog_Intro | text | Introduction text |
| Blog Part X Image | Blog_Part_X_Image | media | Part image ID |
| Blog part X | Blog_Part_X | blocks | HTML content converted to blocks |
| FAQ Title | FAQ_Title | text | FAQ section title |
| FAQ X | FAQX | text | FAQ question |
| FAQ X Detail | FAQ_X_Detail | blocks | FAQ answer as blocks |
| Published On | publishedAt | datetime | Publication date |
| - | Sitemap_Indexing | boolean | Always set to true |

## Image Matching Strategy

Images are matched using the following strategy:

1. Extract filename from the image URL in CSV
2. Find matching entry in `all-images-id-name.json` by filename
3. Use the corresponding `id` field as the Strapi media reference
4. If no match is found, the field is set to `null`

## Content Conversion

HTML content from CSV fields is converted to Strapi blocks format:

- **Headings**: `<h1>` to `<h6>` become heading blocks with appropriate levels (1-6)
- **Paragraphs**: `<p>` become paragraph blocks
- **Quotes**: `<blockquote>` become quote blocks
- **Lists**: `<ul>` and `<ol>` become list blocks with proper formatting
- **List Items**: `<li>` become list-item blocks
- **Text Content**: HTML tags are stripped from text content
- **Empty Content**: Results in empty arrays

The conversion properly handles nested HTML structures and maintains the correct block hierarchy.

## Usage

### Testing with Sample Collection

1. Import `Strapi_City_Blogs_Sample_5_Collection.json` into Postman
2. Set up environment variables:
   - `baseUrl`: Your Strapi API base URL
   - `apiToken`: Your Strapi API token
3. Test the 5 sample requests to verify the structure works
4. Check that entries are created successfully in Strapi

### Generating Full Collection

```bash
node generate_full_collection.js
```

This will:
- Parse all valid entries from the CSV
- Match images to Strapi media IDs
- Convert HTML content to blocks format
- Generate the complete Postman collection
- Provide summary statistics

### Uploading All Entries

**Option 1: Using Split Collections (Recommended)**
1. Import parts from `collection-part-by-part/` directory into Postman
2. Set up environment variables (`baseUrl`, `apiToken`)
3. Run each part sequentially:
   - Part 1: Entries 1-1,015
   - Part 2: Entries 1,016-2,030
   - Part 3: Entries 2,031-3,045
   - Part 4: Entries 3,046-4,058
4. Use Collection Runner with 200-500ms delay between requests
5. Monitor progress and check for any errors

**Option 2: Using Complete Collection**
1. Import `collection/Strapi_City_Blogs_Complete_Collection.postman_collection.json`
2. Set up environment variables
3. Run the collection (note: this is a large file with 4,058 entries)
4. Consider running in batches using Collection Runner filters

## Notes

- The script filters out malformed CSV entries
- Image matching is based on exact filename matches
- HTML content is simplified during conversion to blocks
- All entries are set to published status
- Sitemap indexing is enabled for all entries

## Troubleshooting

### Common Issues

1. **Image not found**: Check if the image filename in CSV matches exactly with `all-images-id-name.json`
2. **HTML parsing errors**: The blocks conversion is basic - complex HTML may need manual adjustment
3. **CSV parsing issues**: Some entries may be skipped if they don't match the expected format

### Validation

Before running the full collection:
1. Test with the sample collection first
2. Verify a few entries are created correctly in Strapi
3. Check that images are properly linked
4. Ensure content formatting looks correct

## File Structure

```
City-Blogs/
├── README.md
├── Booked (Live) - City Blogs all.csv
├── Strapi_City_Blogs_Sample_5_Collection.json
├── Strapi_City_Blogs_Complete_Collection.postman_collection.json
├── generate_full_collection.js
└── collection/
    ├── schema.json
    └── all-images-id-name.json
```

# City Blogs Postman Collection - Split into 4 Parts

This directory contains the complete City Blogs Postman collection split into 4 manageable parts for easier processing and uploading to Strapi.

## Overview

**Total Entries**: 4,058 City Blog entries
**Split Strategy**: 4 approximately equal parts (~1,015 entries each)
**Purpose**: Easier management and separate execution in Postman

## Collection Parts

### Part 1 of 4
- **File**: `Strapi_City_Blogs_Part_1_of_4.postman_collection.json`
- **Entries**: 1-1,015 (1,015 entries)
- **File Size**: 17.0 MB
- **Content Coverage**: 87.0% of entries have Blog Part 1 content
- **Images**: 96.7% of entries have images
- **First Entry**: The Perfect Season for Exploring Bangkok: When to Plan Your Trip
- **Last Entry**: A Complete Travel Guide to Reine Norway Best Time to Visit Activities

### Part 2 of 4
- **File**: `Strapi_City_Blogs_Part_2_of_4.postman_collection.json`
- **Entries**: 1,016-2,030 (1,015 entries)
- **File Size**: 15.1 MB
- **Content Coverage**: 98.9% of entries have Blog Part 1 content
- **Images**: 94.5% of entries have images
- **First Entry**: Top 10 Must See Attractions in Visby Sweden
- **Last Entry**: A Complete Guide to Visiting Regensburg Best Hotels Restaurants

### Part 3 of 4
- **File**: `Strapi_City_Blogs_Part_3_of_4.postman_collection.json`
- **Entries**: 2,031-3,045 (1,015 entries)
- **File Size**: 15.2 MB
- **Content Coverage**: 99.2% of entries have Blog Part 1 content
- **Images**: 93.0% of entries have images
- **First Entry**: Exploring Regensburgs Historic Old Town Tips for First Time Visitors
- **Last Entry**: A Complete Travel Guide to Soroca Hotels Flights and Tips

### Part 4 of 4
- **File**: `Strapi_City_Blogs_Part_4_of_4.postman_collection.json`
- **Entries**: 3,046-4,058 (1,013 entries)
- **File Size**: 10.8 MB
- **Content Coverage**: 91.2% of entries have Blog Part 1 content
- **Images**: 97.3% of entries have images
- **First Entry**: Exploring Soroca Fortress History Tickets and Nearby Accommodations
- **Last Entry**: Where to Stay in Bingol Best Hotels and Accommodations

## Content Quality

### Blog Part 1 Content
- **Average blocks per entry**: ~28 blocks
- **Content includes**:
  - Multiple H2 sections (3-7 sections per entry)
  - Paragraphs with detailed information
  - Lists (unordered and ordered) with proper nesting
  - Quotes and other formatted content

### Images
- **Thumbnail Images**: Properly mapped to Strapi media IDs
- **Main Images**: Properly mapped to Strapi media IDs
- **Image Matching**: Based on filename from URLs matched with `all-images-id-name.json`

### FAQs
- **FAQ Questions**: 6 FAQ questions per entry (where available)
- **FAQ Details**: Converted to Strapi blocks format with proper structure

## Usage Instructions

### Setting Up Postman

1. **Import a Part**:
   - Open Postman
   - Click "Import" → Select one of the part files
   - The collection will appear in your workspace

2. **Configure Environment**:
   - Create or select an environment in Postman
   - Set the following variables:
     - `baseUrl`: Your Strapi API base URL (e.g., `http://localhost:1337` or `https://your-strapi-domain.com`)
     - `apiToken`: Your Strapi API authentication token

3. **Running a Part**:
   - Select the imported collection
   - Click "Run" to open the Collection Runner
   - Configure run settings:
     - Select the collection part
     - Choose the environment
     - Set delay between requests (recommended: 100-500ms to avoid overwhelming the server)
   - Click "Run" to start uploading

### Recommended Workflow

1. **Test with Sample First**:
   - Use `Strapi_City_Blogs_Sample_5_Collection.json` to test the structure
   - Verify a few entries are created correctly in Strapi
   - Check that images, content, and FAQs appear properly

2. **Run Parts Sequentially**:
   - Start with Part 1
   - Monitor for any errors
   - Once Part 1 completes successfully, proceed to Part 2
   - Continue with Parts 3 and 4

3. **Error Handling**:
   - If errors occur, note the entry number
   - You can re-run individual requests from the failed entry onwards
   - Check Strapi logs for detailed error messages

### Performance Tips

- **Batch Size**: Run 100-200 entries at a time for better monitoring
- **Delay**: Use 200-500ms delay between requests to avoid rate limiting
- **Server Resources**: Ensure your Strapi server has adequate resources
- **Database**: Monitor database connections and performance
- **Timeout**: Increase request timeout if needed for large content

## File Structure

```
collection-part-by-part/
├── README.md (this file)
├── README.json (summary metadata)
├── Strapi_City_Blogs_Part_1_of_4.postman_collection.json (1,015 entries)
├── Strapi_City_Blogs_Part_2_of_4.postman_collection.json (1,015 entries)
├── Strapi_City_Blogs_Part_3_of_4.postman_collection.json (1,015 entries)
└── Strapi_City_Blogs_Part_4_of_4.postman_collection.json (1,013 entries)
```

## Verification

All 4,058 entries have been verified:
- ✓ All entries from the CSV are present
- ✓ Blog Part 1 content extracted with complete sections
- ✓ Images properly mapped to Strapi media IDs
- ✓ FAQ content converted to blocks format
- ✓ Proper list structure with list items nested in list blocks
- ✓ All required fields populated

## Technical Details

### Content Extraction
- **Strategy**: Multi-line CSV parsing with regex pattern matching
- **Blog Parts**: Extracted complete HTML content from CSV
- **HTML to Blocks**: Proper conversion maintaining structure hierarchy

### Blocks Format
- **Headings**: `<h1>` to `<h6>` → heading blocks (levels 1-6)
- **Paragraphs**: `<p>` → paragraph blocks
- **Lists**: `<ul>/<ol>` → list blocks with nested list-item children
- **Quotes**: `<blockquote>` → quote blocks

### Data Mapping
- All CSV headers properly mapped to Strapi schema fields
- Image URLs matched to Strapi media IDs
- Slugs auto-generated from names where missing
- Published dates preserved from CSV

## Support

If you encounter issues:
1. Check the sample collection works first
2. Verify your Strapi API token is valid
3. Ensure the base URL is correct
4. Check Strapi server logs for detailed errors
5. Verify images were uploaded to Strapi media library

## Next Steps

After successfully uploading all parts:
1. Verify entries in Strapi admin panel
2. Check that content renders correctly
3. Verify images are properly linked
4. Test a few entries on the frontend
5. Enable published status if entries were created as drafts

---

**Generated**: October 8, 2025
**Total City Blogs**: 4,058 entries
**Parts**: 4 collections (1,015 + 1,015 + 1,015 + 1,013 entries)


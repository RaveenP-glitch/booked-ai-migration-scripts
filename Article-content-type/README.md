# Strapi Migration Script

This script migrates data from a CSV file to Strapi CMS using the REST API.

## Files

- `migrate-to-strapi.js` - Main migration script
- `config.js` - Configuration file for customizing the migration
- `package.json` - Node.js dependencies
- `Booked (Live) - Explores.csv` - Source CSV data

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure Strapi connection:**
   Edit `config.js` and update:
   - `strapi.url` - Your Strapi server URL
   - `strapi.adminEmail` - Your admin email
   - `strapi.adminPassword` - Your admin password
   - `contentType` - Your content type name (e.g., 'articles', 'explores')

3. **Configure content type mappings:**
   Update the field mappings in `config.js` to match your Strapi content type structure.

## Content Type Structure

Based on the image, your Article content type should have these fields:

### Basic Fields
- `title` (Text) - Maps from CSV "Title"
- `description` (Text) - Maps from CSV "Overview" 
- `slug` (UID) - Maps from CSV "Slug"
- `cover` (Media) - Maps from CSV "Image"

### Relations
- `author` (Relation to Author) - Maps from CSV "Author"
- `category` (Relation to Style) - Maps from CSV "Style"

### Rich Text
- `content` (Rich text - Blocks) - Maps from CSV "Overview"

### Dynamic Zone
- `blocks` (Dynamic zone) - Contains:
  - Media component
  - Quote component  
  - Rich text component
  - Slider component

## Usage

1. **Start your Strapi server:**
   ```bash
   npm run develop
   # or
   yarn develop
   ```

2. **Run the migration:**
   ```bash
   npm run migrate
   # or
   node migrate-to-strapi.js
   ```

## Configuration Options

### Field Mappings
Map CSV columns to Strapi fields in `config.js`:

```javascript
fieldMappings: {
  'Title': 'title',
  'Slug': 'slug',
  'Overview': 'description',
  'Image': 'cover',
  'Author': 'author',
  'Style': 'category',
  // Add more mappings as needed
}
```

### Processing Settings
- `batchSize` - Number of entries to process at once (default: 10)
- `delayBetweenBatches` - Delay between batches in milliseconds (default: 2000)

### Media Handling
- `downloadImages` - Whether to download and upload images (default: false)
- `defaultMimeType` - Default MIME type for images (default: 'image/jpeg')

### Relations
- `createMissingAuthors` - Create missing authors (default: true)
- `createMissingCategories` - Create missing categories (default: true)
- `authorContentType` - Author content type name (default: 'authors')
- `categoryContentType` - Category content type name (default: 'categories')

## CSV Data Structure

The script expects a CSV with these columns:
- Title
- Slug
- Overview
- Image (URL)
- Author
- Style
- Location
- Duration
- Cost
- Main Title
- Hotels
- Restaurants
- Attractions
- Itineraries
- City Blogs

## Error Handling

The script includes comprehensive error handling:
- Failed entries are logged but don't stop the migration
- Batch processing prevents overwhelming the server
- Detailed logging shows progress and errors

## Troubleshooting

### Common Issues

1. **Login Failed**
   - Check your admin email and password in `config.js`
   - Ensure Strapi server is running

2. **Content Type Not Found**
   - Verify the content type name in `config.js`
   - Ensure the content type exists in Strapi

3. **Field Mapping Errors**
   - Check that all mapped fields exist in your Strapi content type
   - Verify field types match (text, media, relation, etc.)

4. **Media Upload Issues**
   - Check your media provider configuration in Strapi
   - Verify image URLs are accessible

### Debug Mode

Add console logging by modifying the script or run with:
```bash
DEBUG=* node migrate-to-strapi.js
```

## Customization

### Adding New Field Mappings

1. Add the mapping to `config.js`:
   ```javascript
   fieldMappings: {
     'CSV Column': 'strapiField',
     // ... existing mappings
   }
   ```

2. The script will automatically map the fields during processing.

### Custom Rich Text Content

Modify the `processEntry` function to customize how rich text content is structured:

```javascript
// Handle rich text content
if (csvRow.Overview) {
  mappedData.content = [
    {
      type: 'paragraph',
      children: [
        {
          type: 'text',
          text: csvRow.Overview
        }
      ]
    }
  ];
}
```

### Custom Dynamic Zone Components

Modify the dynamic zone handling in `processEntry`:

```javascript
// Handle dynamic zone (blocks)
if (csvRow.Hotels) {
  mappedData.blocks.push({
    __component: 'blocks.rich-text',
    content: [
      // Your custom content structure
    ]
  });
}
```

## Support

For issues or questions:
1. Check the console output for error messages
2. Verify your Strapi content type structure
3. Test with a small batch first
4. Check Strapi logs for server-side errors




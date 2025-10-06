# Strapi Migration Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure your Strapi connection:**
   Edit `config.js` and update:
   - `strapi.url` - Your Strapi server URL (default: http://localhost:1337)
   - `strapi.adminEmail` - Your admin email
   - `strapi.adminPassword` - Your admin password

3. **Test the connection:**
   ```bash
   npm run test-connection
   ```

4. **Preview the migration:**
   ```bash
   npm run preview
   ```

5. **Run the migration:**
   ```bash
   npm run migrate
   ```

## What This Migration Does

### Content Type: `articles`

The script will create entries in your `articles` content type with the following field mappings:

| CSV Column | Strapi Field | Type | Notes |
|------------|--------------|------|-------|
| Title | title | Text | Article title |
| Slug | slug | UID | URL-friendly identifier |
| Overview | description | Text | Short description |
| Overview | content | Rich Text | Full content in rich text format |
| Image | cover | Media | Cover image (uses existing media by filename) |
| Location | location | Text | Location information |
| Duration | duration | Text | Duration information |
| Cost | cost | Text | Cost information |
| Main Title | mainTitle | Text | Main title |
| Hotels | blocks[0] | Dynamic Zone | Hotels info in rich text block |
| Restaurants | blocks[1] | Dynamic Zone | Restaurants info in rich text block |
| Attractions | blocks[2] | Dynamic Zone | Attractions info in rich text block |

### Media Handling

- **Uses existing media**: The script looks for existing media files by filename
- **No new uploads**: It doesn't download or upload new images
- **Filename matching**: Extracts filename from URL and searches for existing media

### Relations

- **Author relations**: Skipped (as requested)
- **Category relations**: Skipped (as requested)

### Dynamic Zone Structure

The `blocks` dynamic zone will contain rich text components with:
- Hotels information
- Restaurants information  
- Attractions information

Each block uses the `blocks.rich-text` component type.

## Configuration Options

### Batch Processing
- `batchSize`: Number of entries to process at once (default: 10)
- `delayBetweenBatches`: Delay between batches in milliseconds (default: 2000)

### Field Mappings
All field mappings are defined in `config.js` and can be customized as needed.

## Error Handling

- **Individual entry failures** don't stop the migration
- **Detailed logging** shows progress and errors
- **Batch processing** prevents overwhelming the server
- **Media lookup failures** are logged but don't stop processing

## Troubleshooting

### Common Issues

1. **"Login failed"**
   - Check your admin credentials in `config.js`
   - Ensure Strapi server is running

2. **"Content type not accessible"**
   - Verify the content type name is correct
   - Check that the content type exists in Strapi

3. **"Media not found"**
   - Ensure media files are uploaded to Strapi
   - Check that filenames match exactly

4. **"Field mapping errors"**
   - Verify all mapped fields exist in your Strapi content type
   - Check field types match (text, media, rich text, etc.)

### Debug Steps

1. **Test connection first:**
   ```bash
   npm run test-connection
   ```

2. **Preview the data:**
   ```bash
   npm run preview
   ```

3. **Check Strapi logs** for server-side errors

4. **Run with smaller batch size** if experiencing issues

## File Structure

```
Article-content-type/
├── migrate-to-strapi.js    # Main migration script
├── config.js              # Configuration file
├── test-connection.js     # Connection test script
├── preview-migration.js   # Data preview script
├── package.json           # Dependencies
├── README.md             # Detailed documentation
├── MIGRATION_GUIDE.md    # This quick start guide
└── Booked (Live) - Explores.csv  # Source data
```

## Next Steps

After running the migration:

1. **Verify entries** in Strapi admin panel
2. **Check media associations** are correct
3. **Test rich text content** displays properly
4. **Verify dynamic zone blocks** are structured correctly

## Support

If you encounter issues:
1. Check the console output for specific error messages
2. Verify your Strapi content type structure matches the expected fields
3. Test with a small batch first by reducing `batchSize` in config
4. Check Strapi server logs for additional error details






# City Blogs Postman Collection - Usage Guide

## Quick Start

### Files
- **Collection**: `collection/Strapi_City_Blogs_Complete_Collection_Fixed.postman_collection.json`
- **Size**: 110 MB
- **Entries**: 4,040 city blog posts

## Import to Postman

### Step 1: Import Collection
1. Open Postman application
2. Click **Import** button (top left)
3. Select **Upload Files**
4. Choose: `Strapi_City_Blogs_Complete_Collection_Fixed.postman_collection.json`
5. Click **Import**

### Step 2: Configure Environment Variables
You need to set up two environment variables:

1. Click **Environments** in left sidebar
2. Click **+** to create new environment
3. Add variables:

| Variable | Value | Example |
|----------|-------|---------|
| `baseUrl` | Your Strapi API URL | `http://localhost:1337` or `https://api.yourdomain.com` |
| `apiToken` | Your Strapi API token | `your_api_token_here` |

#### How to Get API Token:
1. Log into Strapi admin panel
2. Go to **Settings** → **API Tokens**
3. Click **Create new API Token**
4. Set permissions (needs `city-blogs` create/update access)
5. Copy the generated token

### Step 3: Test Single Request
Before running all 4,040 requests:

1. Open the collection in Postman
2. Select the first request: `1. The Perfect Season for Exploring Bangkok...`
3. Click **Send**
4. Verify response (should be 200 or 201 status)
5. Check Strapi admin to confirm entry was created

### Step 4: Bulk Import Using Collection Runner

#### Option A: Run All at Once (Fast)
1. Right-click on collection name
2. Select **Run collection**
3. Select all requests (or use filters)
4. Set **Delay** between requests: 100-500ms (to avoid overwhelming server)
5. Click **Run City Blogs Collection**
6. Monitor progress

#### Option B: Run in Batches (Recommended)
For better control and error handling:

1. Use Collection Runner
2. Select requests **1-500** first
3. Run and verify
4. Then run **501-1000**, etc.
5. This allows you to catch and fix any issues early

## Important Notes

### Before Running

✅ **Checklist:**
- [ ] Strapi is running and accessible
- [ ] Database is backed up
- [ ] API token has correct permissions
- [ ] All images exist in Strapi media library (IDs must match)
- [ ] Test request successful
- [ ] Server has adequate resources

### Image Requirements

⚠️ **Critical**: The collection references image IDs (1-9373). These images must already exist in your Strapi media library.

**To upload images first:**
1. Check `all_image_urls.txt` for image URLs
2. Download images using the provided scripts in `City-Blogs/` directory
3. Upload to Strapi media library before importing blog posts
4. Verify image IDs match the mapping in `all-images-id-name.json`

### Expected Behavior

**Successful Request:**
```json
{
  "data": {
    "id": 1,
    "attributes": {
      "Name": "...",
      "Slug": "...",
      "publishedAt": "2025-10-08T08:56:11.328Z",
      ...
    }
  }
}
```

**Error Handling:**
- **400 Bad Request**: Check field validation (required fields missing?)
- **401 Unauthorized**: API token is invalid or expired
- **404 Not Found**: Base URL is incorrect
- **500 Server Error**: Check Strapi logs for details

### Rate Limiting

If your Strapi server has rate limiting:
- Increase delay between requests (500-1000ms)
- Run in smaller batches
- Consider running overnight for large imports

## Verification After Import

### Check Entry Count
```bash
curl -X GET "http://localhost:1337/api/city-blogs?pagination[limit]=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Response should show total count near 4,040.

### Verify Sample Entry
1. Log into Strapi admin
2. Go to **Content Manager** → **City Blogs**
3. Open a few random entries
4. Check:
   - Images are displayed correctly
   - Blog content blocks render properly
   - FAQs are formatted correctly
   - All fields are populated

### Check for Duplicates
```sql
-- If using PostgreSQL
SELECT slug, COUNT(*) as count 
FROM city_blogs 
GROUP BY slug 
HAVING COUNT(*) > 1;
```

Should return 0 rows (no duplicates).

## Troubleshooting

### Issue: "Image ID not found"
**Solution**: Image doesn't exist in media library. Either:
- Upload the image first
- Remove the image reference (set to null)
- Run without images initially

### Issue: "Slug already exists"
**Solution**: Entry with that slug already exists. Either:
- Delete existing entry
- Skip that request
- Modify the slug in the collection

### Issue: "Request timeout"
**Solution**: Server is overloaded. Try:
- Reduce batch size
- Increase delay between requests
- Check server resources (CPU, memory, database)

### Issue: "Block validation error"
**Solution**: Block structure issue. Check:
- Strapi blocks plugin is installed
- Schema matches the collection structure
- No custom validation rules blocking import

## Performance Tips

### Fast Import (Testing/Development)
- Disable hooks/plugins temporarily
- Use localhost
- Import as drafts first (change `publishedAt` to null)
- Publish in bulk later

### Safe Import (Production)
- Run during low-traffic hours
- Monitor server resources
- Import in batches of 100-500
- Set delays of 500-1000ms
- Keep backups ready

## Post-Import Tasks

1. **Verify Count**: Check that 4,040 entries were created
2. **Spot Check**: Review 10-20 random entries for quality
3. **Test Frontend**: Ensure blog posts display correctly on website
4. **SEO Check**: Verify slugs and metadata
5. **Image Check**: Confirm all images load properly
6. **Search Index**: Rebuild search index if applicable

## Advanced: Filtering Requests

### Import Only Specific Cities
Use Postman's Collection Runner filters:

1. Open Collection Runner
2. Use **Search** to filter by city name
3. Example: Search "Bangkok" to import only Bangkok blogs
4. Run filtered selection

### Import by Date Range
Requests are numbered sequentially. Use request numbers to select ranges:
- First 1000 entries: Select requests 1-1000
- Middle section: Select requests 1001-2000
- etc.

## Rollback

If you need to undo the import:

```sql
-- CAUTION: This deletes all city blogs
DELETE FROM city_blogs WHERE id > 0;
```

Or use Strapi admin:
1. Go to Content Manager → City Blogs
2. Select all
3. Bulk delete

**Note**: Always test on a staging environment first!

## Support

For issues specific to:
- **Collection structure**: Check `COLLECTION_FIX_REPORT.md`
- **Script errors**: See `fix_postman_collection.py`
- **Strapi errors**: Check Strapi documentation and logs
- **Image mapping**: Review `all-images-id-name.json`

---

## Summary Statistics

- **Total Entries**: 4,040
- **Entries with Images**: 4,005 (99.1%)
- **Unique Images**: 3,999
- **Block Types**: heading, paragraph, quote, list
- **Average Blocks per Entry**: ~26
- **Total Blocks**: ~103,640
- **Collection Size**: 110 MB
- **Format**: Postman Collection v2.1.0

✅ Ready to import!

---

*Last updated: October 11, 2025*


# City Blogs Collection - Divided into 4 Parts

This folder contains the complete City Blogs collection divided into 4 equal parts for easier batch processing in Postman.

## Files

| File | Entries | Range | Size |
|------|---------|-------|------|
| `Strapi_City_Blogs_Part_1_of_4.postman_collection.json` | 1,010 | 1 - 1,010 | ~27 MB |
| `Strapi_City_Blogs_Part_2_of_4.postman_collection.json` | 1,010 | 1,011 - 2,020 | ~27 MB |
| `Strapi_City_Blogs_Part_3_of_4.postman_collection.json` | 1,010 | 2,021 - 3,030 | ~27 MB |
| `Strapi_City_Blogs_Part_4_of_4.postman_collection.json` | 1,010 | 3,031 - 4,040 | ~27 MB |

**Total: 4,040 entries** (same as the complete collection)

## Usage

### Import to Postman

Import each part as a separate collection:

1. Open Postman
2. Click **Import**
3. Select all 4 JSON files (or import one at a time)
4. Each will appear as a separate collection

### Running the Collections

#### Option 1: Run Parts Sequentially

Run each part one after another:

1. **Part 1**: Run Collection Runner on Part 1 (entries 1-1,010)
   - Wait for completion and verify
2. **Part 2**: Run Collection Runner on Part 2 (entries 1,011-2,020)
   - Wait for completion and verify
3. **Part 3**: Run Collection Runner on Part 3 (entries 2,021-3,030)
   - Wait for completion and verify
4. **Part 4**: Run Collection Runner on Part 4 (entries 3,031-4,040)
   - Wait for completion and verify

#### Option 2: Run Parts in Parallel (Advanced)

If your server can handle it, you can run multiple parts simultaneously using different Postman instances or Collection Runner tabs.

**Caution**: Only do this if:
- Your server has sufficient resources
- Database can handle concurrent writes
- No rate limiting issues

### Environment Variables

Set these variables in Postman for all collections:

| Variable | Example Value |
|----------|---------------|
| `baseUrl` | `http://localhost:1337` |
| `apiToken` | `your_strapi_api_token` |

### Recommended Settings

For each Collection Runner execution:

- **Delay between requests**: 200-500ms
- **Save responses**: Enabled (for debugging)
- **Keep variable values**: Enabled
- **Run order**: Linear (default)

### Progress Tracking

After each part completes:

1. ✅ Check Postman results summary
2. ✅ Verify in Strapi admin (Content Manager → City Blogs)
3. ✅ Note any failures for retry
4. ✅ Wait a moment before starting next part

Expected completion after all 4 parts:
- **Total entries in Strapi**: 4,040 city blogs
- **Total time**: ~1-4 hours (depending on server speed and delays)

### Handling Failures

If any requests fail in a part:

1. Note the failed request number/name
2. Check the error message in Postman
3. Fix the issue (e.g., missing image, validation error)
4. Re-run just that request individually
5. Or re-run the entire part after fixing

### Verification After Each Part

Quick verification query:

```bash
# Check entry count after each part
curl -X GET "{{baseUrl}}/api/city-blogs/count" \
  -H "Authorization: Bearer {{apiToken}}"
```

Expected counts:
- After Part 1: ~1,010 entries
- After Part 2: ~2,020 entries
- After Part 3: ~3,030 entries
- After Part 4: ~4,040 entries

## Benefits of Running in Parts

✅ **Better Progress Tracking**: See completion status for each quarter
✅ **Easier Error Handling**: Isolate and fix issues per part
✅ **Less Memory Usage**: Smaller collections use less memory in Postman
✅ **Can Pause**: Take breaks between parts if needed
✅ **Faster Recovery**: If something fails, only need to re-run one part

## File Details

Each part file contains:
- Complete Postman collection structure
- 1,010 properly formatted requests
- All image IDs mapped
- All content as rich text blocks
- Valid JSON ready to import

## Combined Results

When all 4 parts complete successfully:

| Metric | Total |
|--------|-------|
| Total Entries | 4,040 |
| Entries with Images | ~4,005 (99.1%) |
| Total Blocks | ~103,640 |
| Unique Images | ~3,999 |
| Cities Covered | Worldwide |

## Tips

### For Fast Import
- Run during off-peak hours
- Use minimal delay (100-200ms)
- Disable unnecessary Strapi plugins temporarily
- Import to localhost for speed

### For Safe Import
- Use 500-1000ms delay
- Run one part per day
- Monitor server resources
- Keep detailed logs

### For Testing
- Import Part 1 to staging first
- Verify everything works correctly
- Then proceed with remaining parts

## Troubleshooting

### "Cannot find module"
- You're importing the wrong file. Use the `.postman_collection.json` files

### "Duplicate slug"
- An entry from a previous part might have failed but is now succeeding
- Safe to ignore if it's from an earlier run
- Delete duplicates in Strapi if needed

### "Out of memory"
- Close other applications
- Restart Postman
- Parts are designed to be small enough to avoid this

## Summary

✅ Collection divided into 4 equal parts  
✅ Each part has 1,010 entries  
✅ All parts ready for import  
✅ Total: 4,040 city blog entries  

Import each part sequentially for best results!

---

*Generated: October 11, 2025*
*Source: Strapi City Blogs Complete Collection - Fixed*


# Import Order Guide - City Blogs Collection

## Quick Reference

Import and run these collections **in order**:

### ✅ Part 1 of 4
**File**: `Strapi_City_Blogs_Part_1_of_4.postman_collection.json`  
**Entries**: 1,010 (Entry #1 to #1,010)  
**Size**: ~26 MB  
**First Entry**: The Perfect Season for Exploring Bangkok  
**Last Entry**: A Complete Guide to Visiting Visby

**Estimated Time**: 15-45 minutes

---

### ✅ Part 2 of 4
**File**: `Strapi_City_Blogs_Part_2_of_4.postman_collection.json`  
**Entries**: 1,010 (Entry #1,011 to #2,020)  
**Size**: ~30 MB  
**First Entry**: Best Time to Visit Visby  
**Last Entry**: A Complete Guide to Visiting Regensburg

**Estimated Time**: 15-45 minutes

---

### ✅ Part 3 of 4
**File**: `Strapi_City_Blogs_Part_3_of_4.postman_collection.json`  
**Entries**: 1,010 (Entry #2,021 to #3,030)  
**Size**: ~30 MB  
**First Entry**: Exploring Regensburgs Historic Old Town  
**Last Entry**: Top 10 Attractions to Visit in Soroca

**Estimated Time**: 15-45 minutes

---

### ✅ Part 4 of 4
**File**: `Strapi_City_Blogs_Part_4_of_4.postman_collection.json`  
**Entries**: 1,010 (Entry #3,031 to #4,040)  
**Size**: ~23 MB  
**First Entry**: A Complete Travel Guide to Soroca  
**Last Entry**: Where to Stay in Bingol

**Estimated Time**: 15-45 minutes

---

## Import Instructions

### Step 1: Import All Parts to Postman

1. Open Postman
2. Click **Import** button
3. Select all 4 JSON files:
   - `Strapi_City_Blogs_Part_1_of_4.postman_collection.json`
   - `Strapi_City_Blogs_Part_2_of_4.postman_collection.json`
   - `Strapi_City_Blogs_Part_3_of_4.postman_collection.json`
   - `Strapi_City_Blogs_Part_4_of_4.postman_collection.json`
4. Click **Import**

All 4 collections will appear in your Collections sidebar.

### Step 2: Set Environment Variables

Create or select an environment with these variables:

```
baseUrl: http://localhost:1337
apiToken: your_strapi_api_token_here
```

### Step 3: Run Each Part Sequentially

#### Run Part 1

1. Select **Part 1 of 4** collection
2. Click **Run** (or right-click → Run collection)
3. In Collection Runner:
   - Select all 1,010 requests
   - Set delay: **300ms** (adjust based on your server)
   - Click **Run City Blogs Collection**
4. Monitor progress
5. **Wait for completion** before proceeding

**Verify Part 1**:
- Check Strapi admin: Should see ~1,010 entries
- Note any failures

#### Run Part 2

1. Once Part 1 completes successfully
2. Select **Part 2 of 4** collection
3. Run Collection Runner (same settings)
4. Monitor progress
5. **Wait for completion**

**Verify Part 2**:
- Check Strapi admin: Should see ~2,020 total entries
- Note any failures

#### Run Part 3

1. Once Part 2 completes successfully
2. Select **Part 3 of 4** collection
3. Run Collection Runner (same settings)
4. Monitor progress
5. **Wait for completion**

**Verify Part 3**:
- Check Strapi admin: Should see ~3,030 total entries
- Note any failures

#### Run Part 4

1. Once Part 3 completes successfully
2. Select **Part 4 of 4** collection
3. Run Collection Runner (same settings)
4. Monitor progress
5. **Wait for completion**

**Verify Part 4**:
- Check Strapi admin: Should see **4,040 total entries**
- All entries imported! 🎉

---

## Recommended Settings

### Collection Runner Configuration

For each part:

| Setting | Recommended Value | Notes |
|---------|------------------|-------|
| Delay | 300ms | Increase if server struggles |
| Save responses | ✅ Enabled | For debugging |
| Keep variables | ✅ Enabled | Maintain state |
| Stop on error | ❌ Disabled | Continue through errors |
| Run order | Linear | Default, keep as-is |

### Delay Recommendations

- **Fast server (localhost)**: 100-200ms
- **Normal server**: 300-500ms
- **Slow/remote server**: 500-1000ms
- **Rate-limited API**: 1000-2000ms

---

## Progress Tracking Checklist

Print this and check off as you go:

```
[ ] Part 1 imported to Postman
[ ] Part 2 imported to Postman
[ ] Part 3 imported to Postman
[ ] Part 4 imported to Postman

[ ] Environment variables configured
[ ] Test single request successful

[ ] Part 1 Runner started
[ ] Part 1 completed (1,010 entries)
[ ] Part 1 verified in Strapi

[ ] Part 2 Runner started
[ ] Part 2 completed (2,020 total)
[ ] Part 2 verified in Strapi

[ ] Part 3 Runner started
[ ] Part 3 completed (3,030 total)
[ ] Part 3 verified in Strapi

[ ] Part 4 Runner started
[ ] Part 4 completed (4,040 total)
[ ] Part 4 verified in Strapi

[ ] Final verification - all 4,040 entries present
[ ] Spot check random entries for quality
[ ] All images loading correctly
```

---

## Verification Queries

After each part, verify the count:

```bash
# Get total count
curl -X GET "http://localhost:1337/api/city-blogs/count" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

Expected counts:
- After Part 1: ~1,010
- After Part 2: ~2,020
- After Part 3: ~3,030
- After Part 4: ~4,040

---

## Troubleshooting

### If a Part Fails Midway

1. Note which request failed (request number/name)
2. Check the error in Postman response
3. Fix the issue in Strapi or data
4. You can either:
   - Re-run the entire part (duplicates will error but others will succeed)
   - Or manually run failed requests individually

### Common Issues

**"Slug already exists"**
- Entry already created (possibly from previous run)
- Safe to skip or delete old entry

**"Image not found"**
- Image ID doesn't exist in Strapi media library
- Upload images first or set image to null

**"Rate limit exceeded"**
- Increase delay between requests
- Wait a few minutes and retry

**"Request timeout"**
- Server is slow/overloaded
- Increase request timeout in Postman settings
- Reduce concurrent load

---

## Total Time Estimate

| Scenario | Time per Part | Total Time |
|----------|---------------|------------|
| Fast (100ms delay) | 2-3 minutes | 8-12 minutes |
| Normal (300ms delay) | 5-8 minutes | 20-32 minutes |
| Slow (500ms delay) | 8-12 minutes | 32-48 minutes |
| Very Slow (1000ms delay) | 17-20 minutes | 68-80 minutes |

*Plus verification time between parts*

---

## Final Verification

After all 4 parts complete:

1. **Check Count**:
   ```bash
   curl "http://localhost:1337/api/city-blogs/count" \
     -H "Authorization: Bearer TOKEN"
   ```
   Should return: **4040**

2. **Spot Check Entries**:
   - Open Strapi admin
   - Go to Content Manager → City Blogs
   - Check 5-10 random entries
   - Verify images, content blocks, and fields

3. **Check for Duplicates**:
   ```sql
   SELECT slug, COUNT(*) 
   FROM city_blogs 
   GROUP BY slug 
   HAVING COUNT(*) > 1;
   ```
   Should return 0 rows

4. **Test Frontend**:
   - View a few blog posts on your website
   - Ensure they display correctly

---

## Success Criteria

✅ All 4 parts imported  
✅ Total entries: 4,040  
✅ No duplicate slugs  
✅ Images loading correctly  
✅ Content blocks rendering properly  
✅ FAQs displaying correctly  

🎉 **Import Complete!**

---

*Run these imports during off-peak hours for best performance*  
*Keep Strapi logs open to monitor for any issues*


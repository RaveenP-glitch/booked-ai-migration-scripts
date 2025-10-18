# 📦 Attractions Collection - 4-Part Upload Guide

## Overview

The complete Attractions collection (4,340 entries) has been divided into 4 manageable parts for easier uploading and better control during the migration process.

---

## 📊 Collection Parts

| Part | Entries | Range | File Size | File Name |
|------|---------|-------|-----------|-----------|
| **Part 1** | 1,085 | 1-1,085 | 8.93 MB | `Strapi_Attractions_Part_1_of_4.postman_collection.json` |
| **Part 2** | 1,085 | 1,086-2,170 | 9.74 MB | `Strapi_Attractions_Part_2_of_4.postman_collection.json` |
| **Part 3** | 1,085 | 2,171-3,255 | 9.75 MB | `Strapi_Attractions_Part_3_of_4.postman_collection.json` |
| **Part 4** | 1,085 | 3,256-4,340 | 13.24 MB | `Strapi_Attractions_Part_4_of_4.postman_collection.json` |
| **Total** | **4,340** | 1-4,340 | 41.66 MB | All 4 parts combined |

---

## ⏱️ Estimated Upload Times

### Per Part (1,085 entries)
- With 200ms delay: ~3.6 minutes
- With 300ms delay: ~5.4 minutes
- Recommended: **8-12 minutes** (including processing time)

### Total Time (All 4 Parts)
- Minimum: ~14 minutes (200ms delay)
- Recommended: **35-50 minutes** (300ms delay + processing)
- Maximum: ~60 minutes (with server load)

---

## 🚀 Step-by-Step Upload Guide

### Step 1: Prepare Your Environment

1. **Open Postman**
2. **Import Environment**:
   - File: `collection/Strapi_Attractions_Environment.postman_environment.json`
3. **Configure Variables**:
   ```
   baseUrl: https://your-strapi-instance.com
   apiToken: your-api-token-here
   ```
4. **Activate Environment**: Select from dropdown (top right)

---

### Step 2: Test with Sample Collection (Optional but Recommended)

1. Import: `Strapi_Attractions_Test_5.postman_collection.json`
2. Run the test collection (5 entries)
3. Verify in Strapi admin panel
4. If successful, proceed to parts

---

### Step 3: Upload Part 1

1. **Import Collection**:
   - File: `Strapi_Attractions_Part_1_of_4.postman_collection.json`

2. **Open Collection Runner**:
   - Click on the collection
   - Click "Run" button

3. **Configure Runner**:
   ```
   Iterations: 1
   Delay: 300 ms (recommended)
   Save responses: Optional
   Keep variable values: Enabled
   ```

4. **Run Collection**:
   - Click "Run Strapi Attractions - Part 1 of 4"
   - Monitor progress (should take 8-12 minutes)

5. **Verify**:
   - Check Postman console for errors
   - Verify first ~100 entries in Strapi admin
   - Note any failures for retry

---

### Step 4: Upload Part 2

1. **Import**: `Strapi_Attractions_Part_2_of_4.postman_collection.json`
2. **Run Collection** (same settings as Part 1)
3. **Monitor**: Entries 1,086-2,170
4. **Break Time**: Take a 5-minute break if needed

---

### Step 5: Upload Part 3

1. **Import**: `Strapi_Attractions_Part_3_of_4.postman_collection.json`
2. **Run Collection** (same settings)
3. **Monitor**: Entries 2,171-3,255
4. **Check Server**: Ensure Strapi is performing well

---

### Step 6: Upload Part 4

1. **Import**: `Strapi_Attractions_Part_4_of_4.postman_collection.json`
2. **Run Collection** (same settings)
3. **Monitor**: Entries 3,256-4,340
4. **Final Verification**

---

## ✅ Verification Checklist

After each part:
- [ ] Check Collection Runner results (success/failure counts)
- [ ] Verify entries appear in Strapi admin
- [ ] Check Strapi server logs for errors
- [ ] Note any failed requests for retry

After all parts:
- [ ] Total count in Strapi: 4,340 entries
- [ ] Spot-check random entries for data quality
- [ ] Verify images are displaying
- [ ] Test Explore relationships
- [ ] Check block content rendering

---

## 🔧 Troubleshooting

### Issue: Rate Limiting (429 errors)
**Solution**: 
- Increase delay to 500ms or 1000ms
- Reduce batch size (split parts further if needed)
- Check Strapi rate limit settings

### Issue: Timeout Errors (504)
**Solution**:
- Server may be overloaded
- Wait 5-10 minutes between parts
- Check server resources (CPU, memory)
- Consider running during off-peak hours

### Issue: Validation Errors (400)
**Solution**:
- Check specific error message in response
- Verify schema matches collection structure
- Note failed entry name/number
- May need to fix and retry individually

### Issue: Authentication Errors (401)
**Solution**:
- Verify API token hasn't expired
- Check token permissions
- Regenerate token if needed
- Update environment variable

---

## 📈 Progress Tracking

Use this template to track your progress:

```
Part 1: [ ] Started [ ] Completed [ ] Verified
  - Start time: ____:____
  - End time: ____:____
  - Successes: ____
  - Failures: ____

Part 2: [ ] Started [ ] Completed [ ] Verified
  - Start time: ____:____
  - End time: ____:____
  - Successes: ____
  - Failures: ____

Part 3: [ ] Started [ ] Completed [ ] Verified
  - Start time: ____:____
  - End time: ____:____
  - Successes: ____
  - Failures: ____

Part 4: [ ] Started [ ] Completed [ ] Verified
  - Start time: ____:____
  - End time: ____:____
  - Successes: ____
  - Failures: ____

Total Duration: ______ minutes
```

---

## 💡 Best Practices

### 1. Sequential Upload
- Upload parts in order: 1 → 2 → 3 → 4
- Don't run multiple parts simultaneously
- Wait for each part to complete before starting next

### 2. Monitoring
- Keep Postman Collection Runner visible
- Monitor Strapi server logs in separate window
- Watch server resource usage (CPU, memory, disk)

### 3. Break Points
- After Part 2: Take a 5-minute break
- Check server health
- Verify data quality so far

### 4. Error Handling
- Note failed requests during each run
- Don't stop collection for individual failures
- Retry failed entries after all parts complete

### 5. Backup
- Backup Strapi database before starting
- This allows rollback if needed
- Test restore process beforehand

---

## 🎯 Success Metrics

After completing all 4 parts:

| Metric | Target | Status |
|--------|--------|--------|
| Total Entries Uploaded | 4,340 | [ ] |
| Success Rate | >99% | [ ] |
| Entries with Images | 4,323 (99.6%) | [ ] |
| Entries with Explores | 2,040 (47%) | [ ] |
| Failed Entries | <10 | [ ] |
| Total Upload Time | <60 minutes | [ ] |

---

## 🔄 Regenerating Parts

If you need to regenerate the parts:

```bash
cd /Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Attractions
node divide_collection.js
```

This will recreate all 4 part collections from the complete collection.

---

## 📁 File Locations

All collections are in: `Attractions/collection/`

```
collection/
├── Strapi_Attractions_Test_5.postman_collection.json (Test - 5 entries)
├── Strapi_Attractions_Part_1_of_4.postman_collection.json (1,085 entries)
├── Strapi_Attractions_Part_2_of_4.postman_collection.json (1,085 entries)
├── Strapi_Attractions_Part_3_of_4.postman_collection.json (1,085 entries)
├── Strapi_Attractions_Part_4_of_4.postman_collection.json (1,085 entries)
├── Strapi_Attractions_Complete.postman_collection.json (4,340 entries - backup)
└── Strapi_Attractions_Environment.postman_environment.json (Config)
```

---

## 🎉 Completion

Once all 4 parts are uploaded successfully:

1. ✅ Verify total entry count in Strapi: 4,340
2. ✅ Spot-check data quality
3. ✅ Test frontend display
4. ✅ Add Nearby_Attractions relationships (if needed)
5. ✅ Publish entries (if using draft/publish)
6. ✅ Celebrate! 🎊

---

## 📞 Support

If you encounter issues:

1. Check Postman console for detailed error messages
2. Review Strapi server logs
3. Consult `POSTMAN_COLLECTION_README.md` for troubleshooting
4. Check `FINAL_COMPLETION_REPORT.md` for technical details

---

**Created**: October 17, 2025  
**Collection Split**: 4 parts × 1,085 entries each  
**Status**: ✅ Ready for Sequential Upload



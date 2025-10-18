# Hotels Migration - Quick Start Guide

A fast-track guide to get your hotels imported into Strapi.

---

## 🎯 What You Have

- ✅ **3,971 Hotels** ready to import
- ✅ Test collection (5 hotels) for verification
- ✅ Complete collection (all 3,971 hotels)
- ✅ Images automatically matched
- ✅ Nearby attractions automatically linked

---

## ⚡ Quick Start (5 Minutes)

### 1. Prerequisites Check
```bash
# Verify files exist
cd Hotels/collection
ls -la *.postman_collection.json

# You should see:
# - Strapi_Hotels_Test_5.postman_collection.json
# - Strapi_Hotels_Complete.postman_collection.json
# - Strapi_Hotels_Environment.postman_environment.json
```

### 2. Postman Setup

**Import Files:**
1. Open Postman
2. Click **Import** button
3. Drag and drop these files:
   - `Strapi_Hotels_Test_5.postman_collection.json`
   - `Strapi_Hotels_Environment.postman_environment.json`

**Configure Environment:**
1. Select **"Strapi Hotels Environment"** from dropdown (top-right)
2. Click the eye icon 👁️ next to it
3. Click **Edit**
4. Update values:
   ```
   BASE_URL: http://localhost:1337
   API_TOKEN: YOUR_ACTUAL_TOKEN_HERE
   ```
5. Click **Save**

### 3. Get Your API Token

**In Strapi Admin:**
1. Go to **Settings** → **API Tokens**
2. Click **Create new API Token**
3. Set:
   - Name: `Hotels Import`
   - Token type: `Full access` (or custom with Hotels permissions)
   - Token duration: Unlimited
4. Click **Save**
5. Copy the token (you'll only see it once!)
6. Paste it into Postman environment as `API_TOKEN`

### 4. Test Run (IMPORTANT!)

**Run Test Collection First:**
1. In Postman, select **"Strapi Hotels Test Collection (5 entries)"**
2. Click **Runner** button (or **Run collection**)
3. Settings:
   - Iterations: `1`
   - Delay: `100` ms
   - Save responses: ✅ (optional)
4. Click **Run Strapi Hotels Test Collection**
5. Wait for completion (~1-2 seconds)

**Verify in Strapi:**
1. Go to **Content Manager** → **Hotels**
2. You should see **5 new hotels**
3. Open one and check:
   - ✅ Name and details present
   - ✅ Image displayed
   - ✅ Content blocks render correctly
   - ✅ Nearby attractions linked

### 5. Full Import

**If test succeeded:**
1. Import `Strapi_Hotels_Complete.postman_collection.json`
2. Select **"Strapi Hotels Complete Collection"**
3. Click **Runner**
4. Settings:
   - Iterations: `1`
   - Delay: `200-500` ms ⚠️ (important for server stability)
   - Save responses: ❌ (unnecessary, saves space)
5. Click **Run Strapi Hotels Complete Collection**
6. ☕ Grab coffee - this will take ~20-40 minutes at 200ms delay

---

## 🔍 Verify Import

After completion:

```bash
# Check count in Strapi
# Go to Content Manager → Hotels
# Should show: 3,971 entries (or 3,976 if you kept the test entries)
```

**Spot Check:**
- View 10-20 random hotels
- Verify images load
- Check block content renders
- Confirm attractions are linked

---

## ⚠️ Troubleshooting

### Problem: "Unauthorized" error
**Solution**: Check your API_TOKEN in Postman environment

### Problem: "Not Found" error
**Solution**: Verify BASE_URL is correct and Strapi is running

### Problem: Images not showing
**Solution**: 
1. Ensure media library has images uploaded
2. Check `media-ids-and-names.json` is up to date
3. Verify image IDs in `*_data.json` files

### Problem: Attractions not linked
**Solution**: 
1. Ensure attractions are already imported in Strapi
2. Check `all-attractions.json` has 4,335 entries
3. Verify the Hotels schema has `Nearby_Attractions` relation

### Problem: Requests failing
**Solution**:
1. Increase delay between requests (500ms or more)
2. Check Strapi server logs for errors
3. Verify database has enough resources
4. Try smaller batches

---

## 📊 Progress Monitoring

**During Import:**
- Postman shows progress: `123 / 3971 completed`
- Green = Success ✅
- Red = Failed ❌
- Orange = Warning ⚠️

**Failed Requests:**
1. Click on failed request to see error
2. Fix the issue
3. Export failed requests
4. Re-run just those requests

---

## 🎯 Success Checklist

- [ ] Test collection runs successfully (5/5 passed)
- [ ] 5 test hotels visible in Strapi
- [ ] Images are linked correctly
- [ ] Block content renders properly
- [ ] Nearby attractions are linked
- [ ] Environment configured correctly
- [ ] API token has proper permissions
- [ ] Ready for full import!

---

## 📈 Expected Results

| Metric | Expected Value |
|--------|----------------|
| Total Hotels | 3,971 |
| Hotels with Images | ~95%+ |
| Hotels with Gallery | ~60%+ |
| Hotels with Nearby Attractions | ~80%+ |
| Block Content Conversion | 100% |
| Import Success Rate | 99%+ |

---

## 🚀 Advanced Tips

### Batch Processing

If you want to split into batches:

```bash
# Regenerate in batches (modify script)
# Edit generate_postman_collection.js

# Example: First 1000
npm run generate -- --limit 1000 --offset 0

# Next 1000
npm run generate -- --limit 1000 --offset 1000
```

### Rate Limiting

For busy servers, increase delay:
- Local development: `100-200ms`
- Staging server: `300-500ms`
- Production server: `500-1000ms`

### Parallel Processing

Advanced users can use Postman CLI:

```bash
# Install Newman (Postman CLI)
npm install -g newman

# Run collection
newman run Strapi_Hotels_Complete.postman_collection.json \
  -e Strapi_Hotels_Environment.postman_environment.json \
  --delay-request 200 \
  --timeout-request 30000
```

---

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Review `MIGRATION_SUMMARY.md` for full details
3. Inspect `*_data.json` files to verify data
4. Check Strapi logs for server-side errors
5. Review Postman console for request details

---

## 🎉 You're Ready!

Everything is set up and ready to go:
1. Start with the **test collection** ✅
2. Verify results in Strapi ✅
3. Run the **complete collection** ✅
4. Enjoy your 3,971 hotels in Strapi! 🚀

**Time to start:** Run the test collection now!


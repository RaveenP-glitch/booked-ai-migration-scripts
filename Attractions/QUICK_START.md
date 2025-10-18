# 🚀 Quick Start - Attractions Migration

## What You Need

1. **Postman** installed on your computer
2. **Strapi instance** running with:
   - Attractions content type created (using schema.json)
   - Media files uploaded
   - Explores content type with entries
3. **API Token** from Strapi with create permissions

---

## 5-Minute Setup

### Step 1: Import Environment (30 seconds)

1. Open Postman
2. Click **Environments** (left sidebar)
3. Click **Import**
4. Select: `collection/Strapi_Attractions_Environment.postman_environment.json`
5. Click the imported environment
6. Edit these variables:
   - `baseUrl`: Your Strapi URL (e.g., `https://api.yoursite.com`)
   - `apiToken`: Your Strapi API token
7. Click **Save**
8. Select this environment from the dropdown (top right)

### Step 2: Import Test Collection (30 seconds)

1. Click **Import** in Postman
2. Select: `collection/Strapi_Attractions_Test_5.postman_collection.json`
3. Collection appears in **Collections** tab

### Step 3: Run Test (1 minute)

1. Click on the test collection
2. Click **Run** (or use Collection Runner)
3. Click **Run Strapi Attractions - Test (Last 5)**
4. Watch it complete (should see 5 successful requests)

### Step 4: Verify (1 minute)

1. Open your Strapi admin panel
2. Go to **Content Manager** → **Attractions**
3. You should see 5 new attractions
4. Check one entry:
   - Has main image? ✅
   - Has content? ✅
   - Has explore relation? ✅

### Step 5: Run Full Migration (30-45 minutes)

1. Import: `collection/Strapi_Attractions_Complete.postman_collection.json`
2. Open Collection Runner
3. Select the complete collection
4. Settings:
   - **Delay**: 200ms (or 0.2 seconds)
   - **Save responses**: Optional
5. Click **Run**
6. Get a coffee ☕ while it uploads 4,340 entries

---

## One-Command Alternative

If you prefer, regenerate collections anytime:

```bash
# Navigate to Attractions folder
cd /path/to/Attractions

# Install dependencies (first time only)
npm install

# Generate test collection
npm run test

# Generate full collection
npm run generate
```

---

## Expected Results

After full migration:

- ✅ **4,340** attraction entries in Strapi
- ✅ **4,323** with main images (99.6%)
- ✅ **2,486** with photo galleries (57.3%)
- ✅ **2,040** with explore relationships (47%)
- ✅ **4,340** with formatted block content (100%)

---

## Troubleshooting

### ❌ "Unauthorized" Error
→ Check your API token in the environment

### ❌ "Rate Limited" Error
→ Increase delay in Collection Runner (try 500ms)

### ❌ "Validation Failed" Error
→ Ensure Attractions content type matches schema.json

### ❌ Some Images Missing
→ Check `collection/missing_images_report.json` (only 3 images missing)

---

## Need More Help?

📖 **Detailed Guide**: Read `POSTMAN_COLLECTION_README.md`  
📊 **Full Report**: See `MIGRATION_SUMMARY.md`  
🐛 **Issues**: Check Strapi logs and Postman console

---

## Files Overview

```
Attractions/
├── collection/
│   ├── Strapi_Attractions_Test_5.postman_collection.json       ← Import this first
│   ├── Strapi_Attractions_Complete.postman_collection.json     ← Import this second
│   ├── Strapi_Attractions_Environment.postman_environment.json ← Configure this
│   ├── missing_images_report.json                              ← Review if needed
│   └── schema.json                                              ← Reference only
├── POSTMAN_COLLECTION_README.md  ← Detailed instructions
├── MIGRATION_SUMMARY.md          ← Complete report
└── QUICK_START.md                ← You are here! 👋
```

---

**Ready? Let's go! 🎉**

Import → Configure → Test → Deploy



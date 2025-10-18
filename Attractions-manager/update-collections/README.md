# Attractions Nearby_Attractions Update Collections

This directory contains Postman collections for updating the `Nearby_Attractions` field for all attractions in Strapi.

## 📁 Generated Files

- `Strapi_Attractions_Update_Part_1_of_4.postman_collection.json` (1,084 requests)
- `Strapi_Attractions_Update_Part_2_of_4.postman_collection.json` (1,084 requests)
- `Strapi_Attractions_Update_Part_3_of_4.postman_collection.json` (1,084 requests)
- `Strapi_Attractions_Update_Part_4_of_4.postman_collection.json` (1,083 requests)
- `Strapi_Attractions_Update_Environment.postman_environment.json`

**Total**: 4,335 PUT requests across 4 collections

## 📊 Statistics

- **Total attractions matched**: 4,335 / 4,340 from CSV
- **Attractions with Nearby_Attractions data**: 0
- **Nearby_Attractions that will be set**: 0
- **Nearby_Attractions that will be null**: 4,335

## ⚠️ Important Note

The source CSV file (`Booked (Live) - Attractions-4340.csv`) has a "Nearby Attractions" column (column 45), but **it is completely empty for all 4,340 entries**. 

As a result, all generated PUT requests will set the `Nearby_Attractions` field to `null`:

```json
{
  "data": {
    "Nearby_Attractions": null
  }
}
```

## 🔧 Request Format

Each PUT request updates a single attraction using its `documentId`:

**Method**: `PUT`  
**URL**: `{{baseUrl}}/api/attractions/{documentId}`  
**Headers**:
- `Content-Type: application/json`
- `Authorization: Bearer {{apiToken}}`

**Body**:
```json
{
  "data": {
    "Nearby_Attractions": null
  }
}
```

## 📝 Unmatched Attractions

5 attractions from the CSV could not be matched (likely deleted or renamed):
1. Stroll along the Mekong Riverfront
2. Krasnaya Street (Ulitsa Krasnaya)
3. Trek to Kudlu Theertha Falls
4. Hike in Røsnæs Peninsula and enjoy coastal views
5. Propylaea

## 🚀 How to Use

### Option 1: Import to Postman

1. Open Postman
2. Click "Import" in the top left
3. Import all 4 collection files
4. Import the environment file
5. Select "Strapi_Attractions_Update_Environment" as active environment
6. Run collections using Collection Runner

### Option 2: Use Postman CLI (newman)

```bash
# Install newman if not already installed
npm install -g newman

# Run each collection
newman run Strapi_Attractions_Update_Part_1_of_4.postman_collection.json \
  -e Strapi_Attractions_Update_Environment.postman_environment.json

newman run Strapi_Attractions_Update_Part_2_of_4.postman_collection.json \
  -e Strapi_Attractions_Update_Environment.postman_environment.json

newman run Strapi_Attractions_Update_Part_3_of_4.postman_collection.json \
  -e Strapi_Attractions_Update_Environment.postman_environment.json

newman run Strapi_Attractions_Update_Part_4_of_4.postman_collection.json \
  -e Strapi_Attractions_Update_Environment.postman_environment.json
```

## 🔄 To Populate Nearby_Attractions with Actual Data

If you have or can provide Nearby Attractions mapping data, you can:

1. **Create a mapping file** (e.g., `nearby-attractions-mapping.json`):
```json
{
  "Nang Thong Beach Private Yacht Charter": "Some Other Attraction Name",
  "Ushuaïa Ibiza Beach Hotel": "Another Attraction Name"
}
```

2. **Update the generation script** to use this mapping
3. **Regenerate the collections** with:
```bash
node generate-update-collections.js
```

## 📋 Environment Variables

The environment file contains:
- `baseUrl`: `http://127.0.0.1:1337`
- `apiToken`: Your Strapi API token (already configured)

Update these values if your Strapi instance is running on a different URL or if you need to use a different API token.

## ⚙️ Regenerating Collections

To regenerate the collections (e.g., after updating the CSV or mapping data):

```bash
cd /Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Attractions-manager
node generate-update-collections.js
```

The script will:
1. Read the CSV file
2. Match attraction names with documentIds from `all-attractions.json`
3. Look for Nearby Attractions data
4. Generate 4 Postman collections with PUT requests
5. Create an environment file

## 📦 Collection Structure

Each collection is split to handle approximately 1,084 attractions:
- **Part 1**: Attractions 1-1,084
- **Part 2**: Attractions 1,085-2,168
- **Part 3**: Attractions 2,169-3,252
- **Part 4**: Attractions 3,253-4,335

This division helps avoid timeout issues and allows for better progress tracking.



# Strapi Attractions Upload Instructions

## Files Generated:
1. all_attractions_request_bodies.json - Contains all 40 attraction request bodies
2. Strapi_Attractions_All_Collection.postman_collection.json - Postman collection ready for import

## How to Use:

### Option 1: Using Postman Collection
1. Open Postman
2. Import the collection: Strapi_Attractions_All_Collection.postman_collection.json
3. Import the environment: Strapi_Environment.postman_environment.json
4. Set your API token in the environment variables
5. Run the collection to upload all attractions

### Option 2: Using Individual Request Bodies
1. Use the all_attractions_request_bodies.json file
2. Each object contains:
   - attractionName: Name of the attraction
   - requestBody: Complete Strapi API request body

## Summary:
- Total attractions: 40
- All attractions have Main_Image assigned
- 19 attractions have Photos
- 19 attractions have Photo1
- 19 attractions have Photo2
- 19 attractions have Photo3

## API Endpoint:
POST {{baseUrl}}/api/attractions

## Required Headers:
- Content-Type: application/json
- Authorization: Bearer {{apiToken}}

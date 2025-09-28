# Strapi Blogs Upload Instructions

## Files Generated:
1. all_blogs_request_bodies.json - Contains all 100 blog request bodies
2. Strapi_Blogs_Collection.postman_collection.json - Postman collection ready for import
3. Strapi_Blogs_Environment.postman_environment.json - Environment variables

## How to Use:

### Option 1: Using Postman Collection
1. Open Postman
2. Import the collection: Strapi_Blogs_Collection.postman_collection.json
3. Import the environment: Strapi_Blogs_Environment.postman_environment.json
4. Set your API token and base URL in the environment variables
5. Run the collection to upload all blogs

### Option 2: Using Individual Request Bodies
1. Use the all_blogs_request_bodies.json file
2. Each object contains:
   - blogName: Name of the blog
   - requestBody: Complete Strapi API request body

## Summary:
- Total blogs: 100
- Images successfully mapped: 0
- Images with placeholder IDs: 210
- All blogs have Thumbnail_Image and Main_Image assigned (placeholders if no match found)
- Blog parts (1-15) have images and content assigned where available
- HTML content converted to simple text format (not blocks) to avoid validation errors

## API Endpoint:
POST {{baseUrl}}/api/blogs

## Required Headers:
- Content-Type: application/json
- Authorization: Bearer {{apiToken}}

## Notes:
- Image mapping uses partial matching when exact names don't match
- Placeholder IDs are assigned when no media match is found
- HTML content converted to simple text format to avoid Strapi blocks validation errors
- You may need to update placeholder image IDs with actual media IDs after upload
- If you need rich text formatting, you may need to manually convert the text back to proper Strapi blocks format

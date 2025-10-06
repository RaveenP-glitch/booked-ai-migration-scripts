# Strapi Attractions Migration

This directory contains all the necessary files to migrate attractions data from CSV to Strapi CMS using Postman.

## Files Overview

### 1. Postman Collection
- **`Strapi_Attractions_Collection.postman_collection.json`** - Complete Postman collection with all API endpoints
- **`Strapi_Environment.postman_environment.json`** - Environment variables for Postman

### 2. Data Files
- **`Attractions4301-4340.csv`** - Source CSV data with attractions information
- **`schema.json`** - Strapi content type schema for attractions
- **`sample_request_bodies.json`** - Sample request bodies for the first 3 attractions

### 3. Scripts
- **`csv_to_strapi_converter.js`** - Node.js script to convert CSV data to Strapi format

## CSV to Strapi Field Mapping

| CSV Column | Strapi Field | Type | Notes |
|------------|--------------|------|-------|
| Name | Name | string | Required field |
| Slug | Slug | uid | Auto-generated from Name |
| Rating | Rating | decimal | Converted to number |
| Main Image | Main_Image | media | Upload separately |
| Description | Description | text | |
| Tag 1 | Tag1 | string | |
| Tag 2 | Tag2 | string | |
| Tag 3 | Tag3 | string | |
| Formatted Address | Formatted_Address | text | |
| Inner Page | Inner_Page | blocks | Rich text content |
| Location | Location | text | |
| Explore | Explore | relation | One-to-many relation |
| Main Title | Main_Title | text | |
| City | City | text | |
| Country | Country | text | |
| Overview | Overview | text | |
| Intro | Intro | text | |
| Short Summary | Short_Summary | text | |
| Entry Fee | Entry_Fee | string | |
| Visitor Count | Visitor_Count | biginteger | Converted to number |
| Visitor Count Description | Visitor_Count_Description | text | |
| Opening Hours | Opening_Hours | blocks | Rich text content |
| Review Count | Review_Count | biginteger | Converted to number |
| Review Rating | Review_Rating | string | |
| Review Text | Review_Text | text | |
| Review Link | Review_Link | text | |
| Inner Content | Inner_Content | json | |
| Photos | Photos | media | Multiple files |
| Photo 1 | Photo1 | media | Single file |
| Photo 2 | Photo2 | media | Single file |
| Photo 3 | Photo3 | media | Single file |
| FAQ 1-5 | FAQ1-FAQ5 | text | |
| Nearby Attractions | Nearby_Attractions | relation | Self-referencing |
| Amenities | Amenities | blocks | Rich text content |
| Best Time to Visit | Best_Time_to_Visit | blocks | Rich text content |
| Photography Allowed | Photography_Allowed | blocks | Rich text content |
| Accessibility Notes | Accessibility_Notes | blocks | Rich text content |
| Cultural/Religious Notes | Cultural_or_Religous_Notes | blocks | Rich text content |
| Historical Significance | Historical_Significance | blocks | Rich text content |
| Famous Events or Dates | Famous_Events_or_Dates | blocks | Rich text content |
| Time Required to Explore | Time_Required_to_Explore | blocks | Rich text content |
| Kid/Family Friendly | Kid_or_Family_Friendly | blocks | Rich text content |
| Weather Sensitivity | Weather_Sensitivity | blocks | Rich text content |
| Transportation and Accessibility | Transportation_and_Accessibility | blocks | Rich text content |

## Setup Instructions

### 1. Import Postman Collection
1. Open Postman
2. Click "Import" button
3. Select `Strapi_Attractions_Collection.postman_collection.json`
4. Select `Strapi_Environment.postman_environment.json`

### 2. Configure Environment Variables
1. In Postman, go to Environments
2. Select "Strapi Attractions Environment"
3. Update the following variables:
   - `baseUrl`: Your Strapi server URL (e.g., `http://localhost:1337`)
   - `apiToken`: Your Strapi API token

### 3. Generate API Token
1. Go to your Strapi admin panel
2. Navigate to Settings > API Tokens
3. Create a new token with full access
4. Copy the token and paste it in the `apiToken` environment variable

## Usage Instructions

### Method 1: Using Postman Collection (Manual)

1. **Create Attraction**: Use the "Create Attraction" request
   - Set all required variables in the environment
   - Send the request
   - Copy the returned `id` to `attractionId` variable

2. **Upload Main Image**: Use the "Upload Main Image" request
   - Set `mainImagePath` to the local path of the image
   - Send the request

3. **Upload Photos**: Use the "Upload Photos" request
   - Set `photo1Path`, `photo2Path`, `photo3Path` to local image paths
   - Send the request

4. **Update with Blocks**: Use the "Update Attraction with Blocks" request
   - Set all block content variables
   - Send the request

### Method 2: Using the Converter Script (Automated)

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Run the Converter**:
   ```bash
   node csv_to_strapi_converter.js
   ```

3. **Generated Files**:
   - `strapi_attractions_data.json` - Complete Strapi data for all attractions
   - `postman_variables.json` - Postman variables for all attractions
   - `sample_request_bodies.json` - Sample request bodies

## API Endpoints

### Create Attraction
```
POST {{baseUrl}}/api/attractions
Content-Type: application/json
Authorization: Bearer {{apiToken}}
```

### Upload Media
```
POST {{baseUrl}}/api/upload
Authorization: Bearer {{apiToken}}
Content-Type: multipart/form-data
```

### Update Attraction
```
PUT {{baseUrl}}/api/attractions/{{attractionId}}
Content-Type: application/json
Authorization: Bearer {{apiToken}}
```

## Data Processing Notes

### Media Handling
- Images are referenced by URL in the CSV
- You'll need to download and upload them to Strapi
- Use the upload endpoints to attach media to attractions

### Block Content
- Fields marked as "blocks" in the schema contain rich text
- These are converted to Strapi's block format with paragraph blocks
- HTML content is preserved within the text blocks

### Relations
- `Explore` relation needs to be set up with existing explore records
- `Nearby_Attractions` is a self-referencing relation
- These need to be handled after all attractions are created

### Data Types
- `Rating`: Converted from string to decimal
- `Visitor_Count` and `Review_Count`: Converted from string to biginteger
- `publishedAt`: Converted from date string to ISO format

## Troubleshooting

### Common Issues
1. **Authentication Error**: Check your API token
2. **Media Upload Fails**: Ensure file paths are correct and files exist
3. **Validation Error**: Check required fields are not empty
4. **Relation Error**: Ensure referenced records exist before creating relations

### Required Fields
- `Name` (string) - Must be provided
- `Slug` (uid) - Auto-generated from Name if not provided

### Optional Fields
All other fields are optional and can be left empty if not available in the CSV.

## Next Steps

1. Test with a few attractions first
2. Set up proper media handling (download from URLs)
3. Create explore records if needed
4. Set up relations after all attractions are created
5. Consider batch processing for large datasets



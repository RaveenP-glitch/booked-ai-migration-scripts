# Explores Manager

This directory contains scripts to fetch and manage explores entries from Strapi.

## Setup

1. Install dependencies:
```bash
npm install
```

## Usage

### Fetch All Explores

To fetch all explores entries from Strapi:

```bash
npm run fetch
```

Or directly:
```bash
node fetch-all-explores-blogs.js
```

This script will:
- Connect to Strapi at `http://127.0.0.1:1337/api/explores`
- Fetch all explores entries with pagination
- Extract essential fields based on the explores schema
- Save the results to `all-explores.json`

## Output

The script generates `all-explores.json` containing an array of explores entries with the following structure:

```json
[
  {
    "id": 1,
    "documentId": "abc123",
    "Title": "Trip to Bangkok",
    "Slug": "trip-to-bangkok",
    "Overview": "Bangkok, a vibrant city...",
    "Location": "Bangkok, Thailand",
    "Number_of_Spots": 2,
    "Style": "Adventure",
    "Duration": "5 days",
    "Author": "John Doe",
    "Min_Read": "3 min read",
    "Cost": "$",
    "City_Name": "Bangkok",
    "Main_Title": "",
    "Sitemap_Indexing": true,
    "createdAt": "2023-01-01T00:00:00.000Z",
    "updatedAt": "2023-01-01T00:00:00.000Z",
    "publishedAt": "2023-01-01T00:00:00.000Z",
    "locale": "en"
  }
]
```

## Fields Fetched

Based on the explores schema, the following fields are retrieved:

### Content Fields
- `Title` - Unique required field
- `Slug` - URL slug
- `Overview` - Text description
- `Location` - Location string
- `Number_of_Spots` - Integer (number of spots)
- `Style` - Content style (e.g., "Adventure", "Foodie's Love")
- `Duration` - Duration string (e.g., "5 days")
- `Author` - Author name
- `Min_Read` - Reading time (e.g., "3 min read")
- `Cost` - Cost indicator (e.g., "$", "$$", "$$$")
- `City_Name` - City name
- `Main_Title` - Main title field
- `Sitemap_Indexing` - Boolean for sitemap inclusion

### Metadata Fields
- `id` - Entry ID
- `documentId` - Document ID
- `createdAt` - Creation timestamp
- `updatedAt` - Last update timestamp
- `publishedAt` - Publication timestamp
- `locale` - Localization

## Notes

- The script handles pagination automatically (100 entries per page)
- Essential fields are kept based on the explores schema
- Media relations and other complex data are excluded from this fetch
- Progress is logged to the console during fetching
- Total count and statistics are displayed at the end

## Configuration

To modify the configuration, edit these constants in `fetch-all-explores-blogs.js`:

```javascript
const BASE_URL = 'http://127.0.0.1:1337/api/explores';
const API_TOKEN = 'your-api-token-here';
const OUTPUT_FILE = 'all-explores.json';
const PAGE_SIZE = 100;
```



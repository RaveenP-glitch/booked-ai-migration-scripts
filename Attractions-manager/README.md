# Attractions Manager

This directory contains scripts to fetch and manage attractions entries from Strapi.

## Setup

1. Install dependencies:
```bash
npm install
```

## Usage

### Fetch All Attractions

To fetch all attractions entries from Strapi:

```bash
npm run fetch
```

Or directly:
```bash
node fetch-all-attractions.js
```

This script will:
- Connect to Strapi at `http://127.0.0.1:1337/api/attractions`
- Fetch all attractions entries with pagination
- Extract essential fields based on the attractions schema
- Save the results to `all-attractions.json`

## Output

The script generates `all-attractions.json` containing an array of attractions entries with the following structure:

```json
[
  {
    "id": 1,
    "documentId": "abc123",
    "Name": "Attraction Name",
    "Slug": "attraction-name",
    "Rating": 4.5,
    "Description": "Description text...",
    "Tag1": "Tag1",
    "Tag2": "Tag2",
    "Tag3": "Tag3",
    "Formatted_Address": "123 Main St, City, Country",
    "Location": "Location details",
    "Main_Title": "Main Title",
    "City": "City Name",
    "Country": "Country Name",
    "Overview": "Overview text...",
    "Intro": "Introduction text...",
    "Short_Summary": "Short summary...",
    "Entry_Fee": "$10",
    "Visitor_Count": 1000000,
    "Visitor_Count_Description": "Over 1 million visitors annually",
    "Review_Count": 5000,
    "Review_Rating": "4.5/5",
    "Review_Text": "Review text...",
    "Review_Link": "https://...",
    "FAQ1": "FAQ 1 text",
    "FAQ2": "FAQ 2 text",
    "FAQ3": "FAQ 3 text",
    "FAQ4": "FAQ 4 text",
    "FAQ5": "FAQ 5 text",
    "Sitemap_Indexing": true,
    "createdAt": "2023-01-01T00:00:00.000Z",
    "updatedAt": "2023-01-01T00:00:00.000Z",
    "publishedAt": "2023-01-01T00:00:00.000Z",
    "locale": "en"
  }
]
```

## Fields Fetched

Based on the attractions schema, the following fields are retrieved:

### Basic Information
- `Name` - Attraction name (required)
- `Slug` - URL slug
- `Rating` - Rating (decimal)
- `Description` - Description text
- `Tag1`, `Tag2`, `Tag3` - Tags for categorization

### Location Information
- `Formatted_Address` - Full address
- `Location` - Location details
- `City` - City name
- `Country` - Country name

### Content Fields
- `Main_Title` - Main title
- `Overview` - Overview text
- `Intro` - Introduction text
- `Short_Summary` - Short summary

### Visitor Information
- `Entry_Fee` - Entry fee information
- `Visitor_Count` - Visitor count (biginteger)
- `Visitor_Count_Description` - Description of visitor count

### Review Information
- `Review_Count` - Number of reviews
- `Review_Rating` - Rating string
- `Review_Text` - Review text
- `Review_Link` - Link to reviews

### FAQs
- `FAQ1` through `FAQ5` - Frequently asked questions

### Settings
- `Sitemap_Indexing` - Boolean for sitemap inclusion

### Metadata
- `id` - Entry ID
- `documentId` - Document ID
- `createdAt` - Creation timestamp
- `updatedAt` - Last update timestamp
- `publishedAt` - Publication timestamp
- `locale` - Localization

## Notes

- The script handles pagination automatically (100 entries per page)
- Essential fields are kept based on the attractions schema
- Complex blocks fields (Inner_Page, Opening_Hours, etc.) are excluded
- Media relations are excluded from this fetch
- Progress is logged to the console during fetching
- Total count and statistics are displayed at the end

## Configuration

To modify the configuration, edit these constants in `fetch-all-attractions.js`:

```javascript
const BASE_URL = 'http://127.0.0.1:1337/api/attractions';
const API_TOKEN = 'your-api-token-here';
const OUTPUT_FILE = 'all-attractions.json';
const PAGE_SIZE = 100;
```


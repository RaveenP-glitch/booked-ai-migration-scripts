# City Blogs Manager

This directory contains scripts to fetch and manage city-blogs entries from Strapi.

## Setup

1. Install dependencies:
```bash
npm install
```

## Usage

### Fetch All City Blogs

To fetch all city-blogs entries from Strapi:

```bash
npm run fetch
```

Or directly:
```bash
node fetch-all-city-blogs.js
```

This script will:
- Connect to Strapi at `http://127.0.0.1:1337/api/city-blogs`
- Fetch all 4040+ city-blogs entries with pagination
- Extract only essential fields (id, documentId, name, title, slug, timestamps)
- Save the results to `all-city-blogs.json`

## Output

The script generates `all-city-blogs.json` containing an array of city-blogs entries with the following structure:

```json
[
  {
    "id": 1,
    "documentId": "abc123",
    "name": "City Blog Name",
    "title": "City Blog Title",
    "slug": "city-blog-slug",
    "createdAt": "2023-01-01T00:00:00.000Z",
    "updatedAt": "2023-01-01T00:00:00.000Z",
    "publishedAt": "2023-01-01T00:00:00.000Z"
  }
]
```

## Notes

- The script handles pagination automatically (100 entries per page)
- Only essential fields are kept to reduce file size
- Media and blog content parts are excluded
- Progress is logged to the console during fetching


# GraphQL Asset Manager

This directory contains scripts to fetch media assets from Strapi using GraphQL API.

## Overview

The GraphQL Asset Manager provides tools to:
- Fetch all media assets (numeric IDs and names) from Strapi using REST API
- GraphQL introspection tools for schema exploration
- Alternative GraphQL fetcher (fetches documentId instead of numeric id)

## Files

- **`fetch-media-rest.js`** - **RECOMMENDED** REST API script to fetch numeric IDs and names
- **`fetch-media.js`** - GraphQL script (fetches documentId instead of numeric id)
- **`introspect-schema.js`** - Schema introspection tool to understand GraphQL structure
- **`media-ids-and-names.json`** - Output file with all media assets (23,908 items)
- **`schema-introspection.json`** - GraphQL schema details for UploadFile type

## Configuration

The scripts are configured with the following Strapi instance details:

```javascript
BASE_URL: http://127.0.0.1:1337
GRAPHQL_ENDPOINT: http://127.0.0.1:1337/graphql
REST_API_ENDPOINT: http://127.0.0.1:1337/api/upload/files
API_TOKEN: Bearer token for authentication
```

## Installation

```bash
npm install
```

Dependencies:
- `graphql-request` (^6.1.0) - GraphQL client
- `graphql` (^16.8.1) - GraphQL core
- `axios` (^1.6.2) - HTTP client for REST API

## Usage

### Fetch All Media with Numeric ID (REST API - Recommended)

```bash
npm run fetch
# or
node fetch-media-rest.js
```

This will:
1. Fetch all media assets from the REST API
2. Extract numeric `id` and `name` fields
3. Save results to `media-ids-and-names.json`
4. Display sample data and completion status

**Output format:**
```json
[
  {
    "id": 13544,
    "name": "68a5939b0ce6b2344e659fc5_photo.jpeg"
  },
  ...
]
```

### Fetch All Media with DocumentId (GraphQL Alternative)

```bash
node fetch-media.js
```

**Note:** GraphQL in Strapi v5 only exposes `documentId` (string UUID), not the numeric `id`. Use REST API if you need numeric IDs.

This will fetch assets in paginated batches and return:
```json
[
  {
    "documentId": "y3wjqh661jv6u86iu5i8t4l9",
    "name": "66da56fa331609f4953488ce_bookedai-flights-app-image.png"
  },
  ...
]
```

### Introspect GraphQL Schema

```bash
npm run introspect
# or
node introspect-schema.js
```

This will:
1. Query available upload/file-related queries
2. Inspect the UploadFile type structure
3. Save schema details to `schema-introspection.json`

### Available NPM Scripts

```bash
npm run fetch           # Fetch media using REST API (numeric IDs)
npm run fetch:graphql   # Fetch media using GraphQL (documentId)
npm run introspect      # Introspect GraphQL schema
```

## GraphQL Query Structure

The main query used to fetch media assets:

```graphql
query GetMedia($page: Int!, $pageSize: Int!) {
  uploadFiles(pagination: { page: $page, pageSize: $pageSize }) {
    documentId
    name
  }
}
```

Count query:
```graphql
query CountMedia {
  uploadFiles_connection {
    pageInfo {
      total
    }
  }
}
```

## Results

Successfully fetched **23,908 media assets** from the Strapi instance.

The output file `media-ids-and-names.json` contains:
- **id** - Numeric ID (e.g., 13544)
- **name** - Filename (e.g., "68a5939b0ce6b2344e659fc5_photo.jpeg")

File size: ~2.2MB

## Schema Details

The `UploadFile` type in Strapi's GraphQL schema includes these fields:
- documentId (ID)
- name (String)
- alternativeText (String)
- caption (String)
- width (Int)
- height (Int)
- formats (JSON)
- hash (String)
- ext (String)
- mime (String)
- size (Float)
- url (String)
- previewUrl (String)
- provider (String)
- provider_metadata (JSON)
- related (GenericMorph)
- createdAt (DateTime)
- updatedAt (DateTime)
- publishedAt (DateTime)

**Important Note:** The GraphQL API in Strapi v5 does **not** expose the numeric `id` field - only `documentId` (UUID string). To get numeric IDs, use the REST API endpoint (`fetch-media-rest.js`).

## Troubleshooting

### GraphQL Schema Errors

If you encounter schema validation errors, run the introspection script first:
```bash
node introspect-schema.js
```

This will help you understand the correct query structure.

### Authentication Errors

Ensure the API token has the correct permissions:
- Read access to Upload File collection
- GraphQL queries enabled in Strapi settings

### Pagination Issues

The script uses a page size of 100 items. You can adjust this in the script:
```javascript
const PAGE_SIZE = 100; // Increase or decrease as needed
```

## License

MIT


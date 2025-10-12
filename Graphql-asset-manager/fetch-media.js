const { GraphQLClient, gql } = require('graphql-request');
const fs = require('fs');

// Configuration
const GRAPHQL_ENDPOINT = 'http://127.0.0.1:1337/graphql';
const API_TOKEN = 'dae398eefb2012379e258f1a8a068ce684b4fd3e6a0fb37912d61c05149816f1585c455fa709b6c963cd16df09755fd2b0d2b8d4e0e2e648b2343ec55a7887d814724bc72694be35e99324f39d3686b3de73881f82cbbe7e1ea738f246ac462c460c75073453f4eaa796cdda1c1f190e407987fe30006121139fdfe1d29d0182';
const OUTPUT_FILE = 'media-ids-and-names.json';
const PAGE_SIZE = 100; // Adjust based on Strapi's limits

// Initialize GraphQL client
const client = new GraphQLClient(GRAPHQL_ENDPOINT, {
  headers: {
    authorization: `Bearer ${API_TOKEN}`,
  },
});

// GraphQL query to fetch media with pagination
const MEDIA_QUERY = gql`
  query GetMedia($page: Int!, $pageSize: Int!) {
    uploadFiles(pagination: { page: $page, pageSize: $pageSize }) {
      documentId
      name
    }
  }
`;

// Query to get total count
const COUNT_QUERY = gql`
  query CountMedia {
    uploadFiles_connection {
      pageInfo {
        total
      }
    }
  }
`;

async function fetchAllMedia() {
  console.log('Starting to fetch media assets from Strapi GraphQL...\n');
  
  let allMedia = [];
  let currentPage = 1;
  let hasMore = true;
  
  try {
    // Get total count first
    console.log('Getting total count...');
    const countData = await client.request(COUNT_QUERY);
    const totalCount = countData.uploadFiles_connection.pageInfo.total;
    console.log(`Total media assets available: ${totalCount}\n`);
    
    // Fetch all pages
    while (hasMore) {
      console.log(`Fetching page ${currentPage}...`);
      
      const data = await client.request(MEDIA_QUERY, {
        page: currentPage,
        pageSize: PAGE_SIZE,
      });
      
      const mediaItems = data.uploadFiles;
      
      if (mediaItems && mediaItems.length > 0) {
        // Map to use documentId as id (for consistency)
        const formattedItems = mediaItems.map(item => ({
          documentId: item.documentId,
          name: item.name
        }));
        
        allMedia = allMedia.concat(formattedItems);
        console.log(`  ✓ Fetched ${mediaItems.length} items (Total so far: ${allMedia.length}/${totalCount})`);
        
        // Check if there are more pages
        if (mediaItems.length < PAGE_SIZE || allMedia.length >= totalCount) {
          hasMore = false;
        } else {
          currentPage++;
        }
      } else {
        hasMore = false;
      }
    }
    
    console.log(`\n✓ Successfully fetched all ${allMedia.length} media assets!`);
    
    // Save to JSON file
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allMedia, null, 2));
    console.log(`✓ Saved results to ${OUTPUT_FILE}`);
    
    // Display sample of results
    console.log('\nSample of fetched data (first 5 items):');
    console.log(JSON.stringify(allMedia.slice(0, 5), null, 2));
    
    return allMedia;
    
  } catch (error) {
    console.error('Error fetching media:', error);
    if (error.response) {
      console.error('Response errors:', error.response.errors);
    }
    throw error;
  }
}

// Run the script
fetchAllMedia()
  .then(() => {
    console.log('\n✓ Script completed successfully!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\n✗ Script failed:', error.message);
    process.exit(1);
  });


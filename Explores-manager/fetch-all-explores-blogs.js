const axios = require('axios');
const fs = require('fs');

// Configuration
const BASE_URL = 'http://127.0.0.1:1337/api/explores';
const API_TOKEN = 'dae398eefb2012379e258f1a8a068ce684b4fd3e6a0fb37912d61c05149816f1585c455fa709b6c963cd16df09755fd2b0d2b8d4e0e2e648b2343ec55a7887d814724bc72694be35e99324f39d3686b3de73881f82cbbe7e1ea738f246ac462c460c75073453f4eaa796cdda1c1f190e407987fe30006121139fdfe1d29d0182';
const OUTPUT_FILE = 'all-explores.json';
const PAGE_SIZE = 100; // Fetch 100 items per page

async function fetchAllExplores() {
  console.log('Starting to fetch explores entries from Strapi...\n');
  
  let allExplores = [];
  let currentPage = 1;
  let hasMore = true;
  let totalEntries = 0;
  
  try {
    // First request to get total count
    console.log('Getting total count...');
    const initialResponse = await axios.get(BASE_URL, {
      headers: {
        'Authorization': `Bearer ${API_TOKEN}`,
      },
      params: {
        'pagination[page]': 1,
        'pagination[pageSize]': 1,
      }
    });
    
    totalEntries = initialResponse.data.meta.pagination.total;
    console.log(`Total explores entries available: ${totalEntries}\n`);
    
    // Fetch all pages
    while (hasMore) {
      console.log(`Fetching page ${currentPage}...`);
      
      const response = await axios.get(BASE_URL, {
        headers: {
          'Authorization': `Bearer ${API_TOKEN}`,
        },
        params: {
          'pagination[page]': currentPage,
          'pagination[pageSize]': PAGE_SIZE,
        }
      });
      
      const data = response.data;
      const explores = data.data;
      
      if (explores && explores.length > 0) {
        // Extract only essential fields based on explores schema
        const essentialData = explores.map(item => ({
          id: item.id,
          documentId: item.documentId,
          Title: item.Title,
          Slug: item.Slug,
          Overview: item.Overview,
          Location: item.Location,
          Number_of_Spots: item.Number_of_Spots,
          Style: item.Style,
          Duration: item.Duration,
          Author: item.Author,
          Min_Read: item.Min_Read,
          Cost: item.Cost,
          City_Name: item.City_Name,
          Main_Title: item.Main_Title,
          Sitemap_Indexing: item.Sitemap_Indexing,
          // Include metadata fields
          createdAt: item.createdAt,
          updatedAt: item.updatedAt,
          publishedAt: item.publishedAt,
          locale: item.locale,
        }));
        
        allExplores = allExplores.concat(essentialData);
        console.log(`  ✓ Fetched ${explores.length} items (Total so far: ${allExplores.length}/${totalEntries})`);
        
        // Check pagination info
        const pagination = data.meta.pagination;
        if (currentPage >= pagination.pageCount) {
          hasMore = false;
        } else {
          currentPage++;
        }
      } else {
        hasMore = false;
      }
      
      // Small delay to avoid overwhelming the server
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    console.log(`\n✓ Successfully fetched all ${allExplores.length} explores entries!`);
    
    // Save to JSON file
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allExplores, null, 2));
    console.log(`✓ Saved results to ${OUTPUT_FILE}`);
    
    // Display sample of results
    console.log('\nSample of fetched data (first 3 items):');
    console.log(JSON.stringify(allExplores.slice(0, 3), null, 2));
    
    // Display statistics
    console.log('\n=== Statistics ===');
    console.log(`Total entries fetched: ${allExplores.length}`);
    console.log(`Expected entries: ${totalEntries}`);
    console.log(`Match: ${allExplores.length === totalEntries ? '✓ Yes' : '✗ No'}`);
    
    return allExplores;
    
  } catch (error) {
    console.error('Error fetching explores:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', JSON.stringify(error.response.data, null, 2));
    }
    throw error;
  }
}

// Run the script
fetchAllExplores()
  .then(() => {
    console.log('\n✓ Script completed successfully!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\n✗ Script failed:', error.message);
    process.exit(1);
  });



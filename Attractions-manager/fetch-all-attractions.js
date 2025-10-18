const axios = require('axios');
const fs = require('fs');

// Configuration
const BASE_URL = 'http://127.0.0.1:1337/api/attractions';
const API_TOKEN = 'dae398eefb2012379e258f1a8a068ce684b4fd3e6a0fb37912d61c05149816f1585c455fa709b6c963cd16df09755fd2b0d2b8d4e0e2e648b2343ec55a7887d814724bc72694be35e99324f39d3686b3de73881f82cbbe7e1ea738f246ac462c460c75073453f4eaa796cdda1c1f190e407987fe30006121139fdfe1d29d0182';
const OUTPUT_FILE = 'all-attractions.json';
const PAGE_SIZE = 100; // Fetch 100 items per page

async function fetchAllAttractions() {
  console.log('Starting to fetch attractions entries from Strapi...\n');
  
  let allAttractions = [];
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
    console.log(`Total attractions entries available: ${totalEntries}\n`);
    
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
      const attractions = data.data;
      
      if (attractions && attractions.length > 0) {
        // Extract only essential fields based on attractions schema
        const essentialData = attractions.map(item => ({
          id: item.id,
          documentId: item.documentId,
          Name: item.Name,
          Slug: item.Slug,
          Rating: item.Rating,
          Description: item.Description,
          Tag1: item.Tag1,
          Tag2: item.Tag2,
          Tag3: item.Tag3,
          Formatted_Address: item.Formatted_Address,
          Location: item.Location,
          Main_Title: item.Main_Title,
          City: item.City,
          Country: item.Country,
          Overview: item.Overview,
          Intro: item.Intro,
          Short_Summary: item.Short_Summary,
          Entry_Fee: item.Entry_Fee,
          Visitor_Count: item.Visitor_Count,
          Visitor_Count_Description: item.Visitor_Count_Description,
          Review_Count: item.Review_Count,
          Review_Rating: item.Review_Rating,
          Review_Text: item.Review_Text,
          Review_Link: item.Review_Link,
          FAQ1: item.FAQ1,
          FAQ2: item.FAQ2,
          FAQ3: item.FAQ3,
          FAQ4: item.FAQ4,
          FAQ5: item.FAQ5,
          Sitemap_Indexing: item.Sitemap_Indexing,
          // Include metadata fields
          createdAt: item.createdAt,
          updatedAt: item.updatedAt,
          publishedAt: item.publishedAt,
          locale: item.locale,
        }));
        
        allAttractions = allAttractions.concat(essentialData);
        console.log(`  ✓ Fetched ${attractions.length} items (Total so far: ${allAttractions.length}/${totalEntries})`);
        
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
    
    console.log(`\n✓ Successfully fetched all ${allAttractions.length} attractions entries!`);
    
    // Save to JSON file
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allAttractions, null, 2));
    console.log(`✓ Saved results to ${OUTPUT_FILE}`);
    
    // Display sample of results
    console.log('\nSample of fetched data (first 2 items):');
    console.log(JSON.stringify(allAttractions.slice(0, 2), null, 2));
    
    // Display statistics
    console.log('\n=== Statistics ===');
    console.log(`Total entries fetched: ${allAttractions.length}`);
    console.log(`Expected entries: ${totalEntries}`);
    console.log(`Match: ${allAttractions.length === totalEntries ? '✓ Yes' : '✗ No'}`);
    
    return allAttractions;
    
  } catch (error) {
    console.error('Error fetching attractions:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', JSON.stringify(error.response.data, null, 2));
    }
    throw error;
  }
}

// Run the script
fetchAllAttractions()
  .then(() => {
    console.log('\n✓ Script completed successfully!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\n✗ Script failed:', error.message);
    process.exit(1);
  });



const axios = require('axios');
const fs = require('fs');

// Configuration
const BASE_URL = 'http://127.0.0.1:1337/api/upload/files';
const API_TOKEN = 'dae398eefb2012379e258f1a8a068ce684b4fd3e6a0fb37912d61c05149816f1585c455fa709b6c963cd16df09755fd2b0d2b8d4e0e2e648b2343ec55a7887d814724bc72694be35e99324f39d3686b3de73881f82cbbe7e1ea738f246ac462c460c75073453f4eaa796cdda1c1f190e407987fe30006121139fdfe1d29d0182';
const OUTPUT_FILE = 'media-ids-and-names.json';

async function fetchAllMedia() {
  console.log('Starting to fetch media assets from Strapi REST API...\n');
  
  try {
    const response = await axios.get(BASE_URL, {
      headers: {
        'Authorization': `Bearer ${API_TOKEN}`,
      },
    });
    
    const allMedia = response.data;
    console.log(`✓ Successfully fetched ${allMedia.length} media assets!`);
    
    // Extract only id and name (id is the numeric ID)
    const mediaIdsAndNames = allMedia.map(item => ({
      id: item.id,
      name: item.name
    }));
    
    // Save to JSON file
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(mediaIdsAndNames, null, 2));
    console.log(`✓ Saved results to ${OUTPUT_FILE}`);
    
    // Display sample of results
    console.log('\nSample of fetched data (first 5 items):');
    console.log(JSON.stringify(mediaIdsAndNames.slice(0, 5), null, 2));
    
    console.log(`\nTotal media assets: ${mediaIdsAndNames.length}`);
    
    return mediaIdsAndNames;
    
  } catch (error) {
    console.error('Error fetching media:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
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


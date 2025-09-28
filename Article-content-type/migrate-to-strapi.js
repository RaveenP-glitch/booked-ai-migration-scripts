// migrate-to-strapi.js
// Usage: node migrate-to-strapi.js
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');
const csv = require('csv-parser');
const config = require('./config');

const CONFIG = config;

async function login() {
  console.log('🔐 Logging in to Strapi...');
  const res = await fetch(`${CONFIG.strapi.url}/api/auth/local`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      identifier: CONFIG.strapi.adminEmail, 
      password: CONFIG.strapi.adminPassword 
    }),
  });
  
  const json = await res.json();
  if (!res.ok) {
    console.error('❌ Login failed:', json);
    throw new Error(`Login failed: ${JSON.stringify(json)}`);
  }
  
  console.log('✅ Successfully logged in');
  return json.jwt;
}

async function findExistingMedia(jwt, imageUrl) {
  if (!imageUrl || imageUrl.trim() === '') return null;
  
  try {
    // Extract filename from URL
    const filename = imageUrl.split('/').pop();
    if (!filename) return null;
    
    console.log(`🔍 Looking for existing media: ${filename}`);
    
    // Search for existing media by filename
    const res = await fetch(`${CONFIG.strapi.url}/api/upload/files?filters[name][$eq]=${encodeURIComponent(filename)}`, {
      headers: {
        'Authorization': `Bearer ${jwt}`,
      },
    });
    
    const result = await res.json();
    if (!res.ok) {
      console.warn(`⚠️ Failed to search for media ${filename}:`, result);
      return null;
    }
    
    if (result.data && result.data.length > 0) {
      console.log(`✅ Found existing media: ${filename} (ID: ${result.data[0].id})`);
      return result.data[0].id;
    }
    
    console.warn(`⚠️ Media not found: ${filename}`);
    return null;
  } catch (error) {
    console.warn(`⚠️ Error searching for media ${imageUrl}:`, error.message);
    return null;
  }
}

// Skipping author relations as per requirements

// Skipping category relations as per requirements

async function createEntry(jwt, data) {
  const res = await fetch(`${CONFIG.strapi.url}/api/${CONFIG.contentType}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${jwt}`,
    },
    body: JSON.stringify({ data }),
  });
  
  const json = await res.json();
  if (!res.ok) {
    throw new Error(`Failed to create entry: ${JSON.stringify(json)}`);
  }
  
  return json;
}

function parseCSVData(csvData) {
  return new Promise((resolve, reject) => {
    const results = [];
    
    const stream = require('stream');
    const readable = stream.Readable.from([csvData]);
    
    readable
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => resolve(results))
      .on('error', reject);
  });
}

function mapCSVToStrapi(csvRow) {
  const mappedData = {};
  
  // Map basic fields
  Object.entries(CONFIG.fieldMappings).forEach(([csvField, strapiField]) => {
    if (csvRow[csvField] !== undefined && csvRow[csvField] !== '') {
      mappedData[strapiField] = csvRow[csvField];
    }
  });
  
  // Handle additional fields that might exist
  if (csvRow['Location']) mappedData.location = csvRow['Location'];
  if (csvRow['Duration']) mappedData.duration = csvRow['Duration'];
  if (csvRow['Cost']) mappedData.cost = csvRow['Cost'];
  if (csvRow['Main Title']) mappedData.mainTitle = csvRow['Main Title'];
  
  return mappedData;
}

async function processEntry(jwt, csvRow, index) {
  try {
    console.log(`\n📝 Processing entry ${index + 1}: ${csvRow.Title}`);
    
    // Map CSV data to Strapi format
    const mappedData = mapCSVToStrapi(csvRow);
    
    // Handle media (cover image) - use existing media by name
    if (csvRow.Image) {
      const mediaId = await findExistingMedia(jwt, csvRow.Image);
      if (mediaId) {
        mappedData.cover = mediaId;
      }
    }
    
    // Skip author and category relations as per requirements
    
    // Handle rich text content - map Overview to content field
    if (csvRow.Overview) {
      // Create a rich text structure for the content field
      mappedData.content = [
        {
          type: 'paragraph',
          children: [
            {
              type: 'text',
              text: csvRow.Overview
            }
          ]
        }
      ];
    }
    
    // Handle dynamic zone (blocks) - create a simple structure
    if (csvRow.Hotels || csvRow.Restaurants || csvRow.Attractions) {
      mappedData.blocks = [];
      
      // Add hotels as a text block
      if (csvRow.Hotels) {
        mappedData.blocks.push({
          __component: 'blocks.rich-text',
          content: [
            {
              type: 'heading',
              level: 3,
              children: [{ type: 'text', text: 'Hotels' }]
            },
            {
              type: 'paragraph',
              children: [{ type: 'text', text: csvRow.Hotels }]
            }
          ]
        });
      }
      
      // Add restaurants as a text block
      if (csvRow.Restaurants) {
        mappedData.blocks.push({
          __component: 'blocks.rich-text',
          content: [
            {
              type: 'heading',
              level: 3,
              children: [{ type: 'text', text: 'Restaurants' }]
            },
            {
              type: 'paragraph',
              children: [{ type: 'text', text: csvRow.Restaurants }]
            }
          ]
        });
      }
      
      // Add attractions as a text block
      if (csvRow.Attractions) {
        mappedData.blocks.push({
          __component: 'blocks.rich-text',
          content: [
            {
              type: 'heading',
              level: 3,
              children: [{ type: 'text', text: 'Attractions' }]
            },
            {
              type: 'paragraph',
              children: [{ type: 'text', text: csvRow.Attractions }]
            }
          ]
        });
      }
    }
    
    // Create the entry
    const result = await createEntry(jwt, mappedData);
    console.log(`✅ Successfully created: ${csvRow.Title}`);
    return result;
    
  } catch (error) {
    console.error(`❌ Failed to process ${csvRow.Title}:`, error.message);
    throw error;
  }
}

async function main() {
  try {
    console.log('🚀 Starting Strapi migration...');
    
    // Read CSV file
    const csvPath = path.join(__dirname, 'Booked (Live) - Explores.csv');
    const csvData = fs.readFileSync(csvPath, 'utf8');
    
    // Parse CSV data
    console.log('📊 Parsing CSV data...');
    const csvRows = await parseCSVData(csvData);
    console.log(`📈 Found ${csvRows.length} entries to process`);
    
    // Login to Strapi
    const jwt = await login();
    
    // Process entries in batches
    let successCount = 0;
    let errorCount = 0;
    
    for (let i = 0; i < csvRows.length; i += CONFIG.batchSize) {
      const batch = csvRows.slice(i, i + CONFIG.batchSize);
      console.log(`\n📦 Processing batch ${Math.floor(i / CONFIG.batchSize) + 1}/${Math.ceil(csvRows.length / CONFIG.batchSize)}`);
      
      const batchPromises = batch.map((row, batchIndex) => 
        processEntry(jwt, row, i + batchIndex).catch(error => {
          console.error(`❌ Error in batch item ${i + batchIndex + 1}:`, error.message);
          return null;
        })
      );
      
      const results = await Promise.all(batchPromises);
      
      const batchSuccess = results.filter(result => result !== null).length;
      const batchErrors = results.length - batchSuccess;
      
      successCount += batchSuccess;
      errorCount += batchErrors;
      
      console.log(`📊 Batch completed: ${batchSuccess} success, ${batchErrors} errors`);
      
      // Add a small delay between batches to avoid overwhelming the server
      if (i + CONFIG.batchSize < csvRows.length) {
        console.log(`⏳ Waiting ${CONFIG.delayBetweenBatches / 1000} seconds before next batch...`);
        await new Promise(resolve => setTimeout(resolve, CONFIG.delayBetweenBatches));
      }
    }
    
    console.log('\n🎉 Migration completed!');
    console.log(`✅ Successfully processed: ${successCount} entries`);
    console.log(`❌ Errors: ${errorCount} entries`);
    
  } catch (error) {
    console.error('💥 Migration failed:', error.message);
    process.exit(1);
  }
}

// Run the migration
if (require.main === module) {
  main();
}

module.exports = {
  login,
  createEntry,
  findExistingMedia,
  mapCSVToStrapi,
  processEntry
};

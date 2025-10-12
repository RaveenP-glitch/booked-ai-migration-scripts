// preview-migration.js
// Preview what the migration will create without actually running it
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const CONFIG = require('./config');

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

function createPreviewEntry(csvRow, index) {
  const mappedData = mapCSVToStrapi(csvRow);
  
  // Handle media (cover image) - just show the filename
  if (csvRow.Image) {
    const filename = csvRow.Image.split('/').pop();
    mappedData.cover = `[Will look for existing media: ${filename}]`;
  }
  
  // Handle rich text content
  if (csvRow.Overview) {
    mappedData.content = [
      {
        type: 'paragraph',
        children: [
          {
            type: 'text',
            text: csvRow.Overview.substring(0, 100) + '...' // Truncate for preview
          }
        ]
      }
    ];
  }
  
  // Handle dynamic zone (blocks)
  if (csvRow.Hotels || csvRow.Restaurants || csvRow.Attractions) {
    mappedData.blocks = [];
    
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
            children: [{ type: 'text', text: csvRow.Hotels.substring(0, 50) + '...' }]
          }
        ]
      });
    }
    
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
            children: [{ type: 'text', text: csvRow.Restaurants.substring(0, 50) + '...' }]
          }
        ]
      });
    }
    
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
            children: [{ type: 'text', text: csvRow.Attractions.substring(0, 50) + '...' }]
          }
        ]
      });
    }
  }
  
  return {
    index: index + 1,
    title: csvRow.Title,
    data: mappedData
  };
}

async function previewMigration() {
  try {
    console.log('🔍 Previewing migration data...\n');
    
    // Read CSV file
    const csvPath = path.join(__dirname, 'Booked (Live) - Explores.csv');
    const csvData = fs.readFileSync(csvPath, 'utf8');
    
    // Parse CSV data
    const csvRows = await parseCSVData(csvData);
    console.log(`📊 Found ${csvRows.length} entries to process\n`);
    
    // Show preview of first 3 entries
    const previewCount = Math.min(3, csvRows.length);
    
    for (let i = 0; i < previewCount; i++) {
      const preview = createPreviewEntry(csvRows[i], i);
      
      console.log(`📝 Entry ${preview.index}: ${preview.title}`);
      console.log('📋 Data structure:');
      console.log(JSON.stringify(preview.data, null, 2));
      console.log('\n' + '='.repeat(80) + '\n');
    }
    
    if (csvRows.length > previewCount) {
      console.log(`... and ${csvRows.length - previewCount} more entries\n`);
    }
    
    console.log('✅ Preview complete! Run the actual migration with: npm run migrate');
    
  } catch (error) {
    console.error('💥 Preview failed:', error.message);
  }
}

previewMigration();









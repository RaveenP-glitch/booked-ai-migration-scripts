const fs = require('fs');
const path = require('path');

// Load the complete data
const completeData = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'Strapi_Hotels_Complete_data.json'), 'utf8')
);

console.log(`Total hotels: ${completeData.length}`);

// Calculate items per part
const totalHotels = completeData.length;
const partsCount = 5;
const hotelsPerPart = Math.ceil(totalHotels / partsCount);

console.log(`Hotels per part: ${hotelsPerPart}`);
console.log('');

// Create collection_parts directory
const outputDir = path.join(__dirname, '../collection_parts');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Function to create a Postman request
function createPostmanRequest(hotel) {
  const body = {
    data: {}
  };
  
  // Add all fields to the body
  Object.keys(hotel).forEach(key => {
    if (hotel[key] !== null && hotel[key] !== undefined && hotel[key] !== '') {
      body.data[key] = hotel[key];
    }
  });
  
  return {
    name: `Create Hotel: ${hotel.Name}`,
    request: {
      method: 'POST',
      header: [
        {
          key: 'Content-Type',
          value: 'application/json'
        },
        {
          key: 'Authorization',
          value: 'Bearer {{API_TOKEN}}',
          type: 'text'
        }
      ],
      body: {
        mode: 'raw',
        raw: JSON.stringify(body, null, 2)
      },
      url: {
        raw: '{{BASE_URL}}/api/hotels',
        host: ['{{BASE_URL}}'],
        path: ['api', 'hotels']
      }
    },
    response: []
  };
}

// Divide into parts
for (let i = 0; i < partsCount; i++) {
  const startIdx = i * hotelsPerPart;
  const endIdx = Math.min(startIdx + hotelsPerPart, totalHotels);
  const partHotels = completeData.slice(startIdx, endIdx);
  
  const partNumber = i + 1;
  const partName = `Part_${partNumber}_of_${partsCount}`;
  
  console.log(`Creating ${partName}: Hotels ${startIdx + 1}-${endIdx} (${partHotels.length} entries)`);
  
  // Create Postman collection for this part
  const collection = {
    info: {
      name: `Strapi Hotels ${partName}`,
      description: `Postman collection for Hotels Part ${partNumber} of ${partsCount} (Hotels ${startIdx + 1}-${endIdx})`,
      schema: 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
    },
    item: partHotels.map(hotel => createPostmanRequest(hotel)),
    variable: []
  };
  
  // Save the Postman collection
  const collectionPath = path.join(outputDir, `Strapi_Hotels_${partName}.postman_collection.json`);
  fs.writeFileSync(collectionPath, JSON.stringify(collection, null, 2));
  console.log(`  ✅ Saved: ${collectionPath}`);
  
  // Save the data JSON for reference
  const dataPath = path.join(outputDir, `Strapi_Hotels_${partName}_data.json`);
  fs.writeFileSync(dataPath, JSON.stringify(partHotels, null, 2));
  console.log(`  ✅ Saved: ${dataPath}`);
  console.log('');
}

console.log('✅ All parts created successfully!');
console.log('');
console.log('Summary:');
console.log(`  Total Hotels: ${totalHotels}`);
console.log(`  Parts Created: ${partsCount}`);
console.log(`  Hotels per Part: ~${hotelsPerPart}`);
console.log(`  Output Directory: ${outputDir}`);


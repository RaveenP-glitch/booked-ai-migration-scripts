const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// Configuration
const CSV_FILE = '../Attractions/collection/Booked (Live) - Attractions-4340.csv';
const ATTRACTIONS_JSON = './all-attractions.json';
const OUTPUT_DIR = './update-collections';
const BASE_URL = 'http://127.0.0.1:1337';
const API_TOKEN = 'dae398eefb2012379e258f1a8a068ce684b4fd3e6a0fb37912d61c05149816f1585c455fa709b6c963cd16df09755fd2b0d2b8d4e0e2e648b2343ec55a7887d814724bc72694be35e99324f39d3686b3de73881f82cbbe7e1ea738f246ac462c460c75073453f4eaa796cdda1c1f190e407987fe30006121139fdfe1d29d0182';

console.log('Loading attractions data...\n');

// Load attractions JSON
const attractionsData = JSON.parse(fs.readFileSync(ATTRACTIONS_JSON, 'utf8'));

// Create a map of Name -> full attraction data for quick lookup
const attractionMap = new Map();
attractionsData.forEach(attraction => {
  if (attraction.Name && attraction.documentId) {
    // Store with exact name
    attractionMap.set(attraction.Name.trim(), attraction);
    // Also store lowercase for fuzzy matching
    attractionMap.set(attraction.Name.trim().toLowerCase(), attraction);
  }
});

console.log(`Loaded ${attractionsData.length} attractions into lookup map`);

// Find attraction by name
function findAttraction(name) {
  if (!name || typeof name !== 'string') return null;
  
  const cleanName = name.trim();
  
  // Try exact match first
  let attraction = attractionMap.get(cleanName);
  if (attraction) return attraction;
  
  // Try case-insensitive match
  attraction = attractionMap.get(cleanName.toLowerCase());
  if (attraction) return attraction;
  
  return null;
}

// Parse CSV and generate collections
async function generateCollections() {
  const csvData = [];
  
  return new Promise((resolve, reject) => {
    console.log('\nParsing CSV file...');
    
    fs.createReadStream(CSV_FILE)
      .pipe(csv())
      .on('data', (row) => {
        // Extract relevant fields
        const name = row['Name']?.trim();
        const nearbyAttractions = row['Nearby Attractions']?.trim();
        
        if (name) {
          csvData.push({
            name,
            nearbyAttractions: nearbyAttractions || null
          });
        }
      })
      .on('end', () => {
        console.log(`Parsed ${csvData.length} rows from CSV\n`);
        
        // Build update requests
        console.log('Building update requests...');
        const updateRequests = [];
        let matchedCount = 0;
        let withNearbyCount = 0;
        let nearbyMatchedCount = 0;
        const unmatchedAttractions = [];
        const unmatchedNearby = [];
        
        csvData.forEach((row) => {
          const attraction = findAttraction(row.name);
          
          if (!attraction) {
            if (unmatchedAttractions.length < 10) {
              unmatchedAttractions.push(row.name);
            }
            return;
          }
          
          matchedCount++;
          
          let nearbyDocumentId = null;
          if (row.nearbyAttractions) {
            withNearbyCount++;
            const nearbyAttraction = findAttraction(row.nearbyAttractions);
            if (nearbyAttraction) {
              nearbyDocumentId = nearbyAttraction.documentId;
              nearbyMatchedCount++;
            } else {
              if (unmatchedNearby.length < 10) {
                unmatchedNearby.push(`${row.name} -> "${row.nearbyAttractions}"`);
              }
            }
          }
          
          updateRequests.push({
            name: row.name,
            documentId: attraction.documentId,
            nearbyAttractions: nearbyDocumentId
          });
        });
        
        console.log(`\n=== Matching Statistics ===`);
        console.log(`Total CSV rows: ${csvData.length}`);
        console.log(`Matched attractions: ${matchedCount}`);
        console.log(`Attractions with Nearby Attractions field: ${withNearbyCount}`);
        console.log(`Successfully matched Nearby Attractions: ${nearbyMatchedCount}`);
        
        if (unmatchedAttractions.length > 0) {
          console.log(`\nSample unmatched attractions (first 10):`);
          unmatchedAttractions.forEach(name => console.log(`  - ${name}`));
        }
        
        if (unmatchedNearby.length > 0) {
          console.log(`\nSample unmatched Nearby Attractions (first 10):`);
          unmatchedNearby.forEach(item => console.log(`  - ${item}`));
        }
        
        // Split into 4 collections
        const collectionsCount = 4;
        const itemsPerCollection = Math.ceil(updateRequests.length / collectionsCount);
        
        console.log(`\n=== Generating ${collectionsCount} Postman Collections ===`);
        console.log(`Items per collection: ~${itemsPerCollection}\n`);
        
        for (let i = 0; i < collectionsCount; i++) {
          const start = i * itemsPerCollection;
          const end = Math.min(start + itemsPerCollection, updateRequests.length);
          const requests = updateRequests.slice(start, end);
          
          const collection = {
            info: {
              name: `Strapi_Attractions_Update_Part_${i + 1}_of_${collectionsCount}`,
              description: `Postman collection for updating Nearby_Attractions field for attractions ${start + 1}-${end} (${requests.length} entries)`,
              schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            item: []
          };
          
          // Generate PUT request for each attraction
          requests.forEach((req, idx) => {
            const requestNumber = start + idx + 1;
            const body = {
              data: {
                Nearby_Attractions: req.nearbyAttractions
              }
            };
            
            collection.item.push({
              name: `${requestNumber}. UPDATE: ${req.name}`,
              request: {
                method: "PUT",
                header: [
                  {
                    key: "Content-Type",
                    value: "application/json"
                  },
                  {
                    key: "Authorization",
                    value: "Bearer {{apiToken}}"
                  }
                ],
                body: {
                  mode: "raw",
                  raw: JSON.stringify(body, null, 2)
                },
                url: {
                  raw: `{{baseUrl}}/api/attractions/${req.documentId}`,
                  host: ["{{baseUrl}}"],
                  path: ["api", "attractions", req.documentId]
                }
              },
              response: []
            });
          });
          
          // Save collection
          const filename = path.join(OUTPUT_DIR, `Strapi_Attractions_Update_Part_${i + 1}_of_${collectionsCount}.postman_collection.json`);
          fs.writeFileSync(filename, JSON.stringify(collection, null, 2));
          console.log(`✓ Created: ${filename} (${requests.length} update requests)`);
        }
        
        // Create environment file
        const environment = {
          id: "attractions-update-env",
          name: "Strapi_Attractions_Update_Environment",
          values: [
            {
              key: "baseUrl",
              value: BASE_URL,
              enabled: true
            },
            {
              key: "apiToken",
              value: API_TOKEN,
              enabled: true
            }
          ]
        };
        
        const envFilename = path.join(OUTPUT_DIR, 'Strapi_Attractions_Update_Environment.postman_environment.json');
        fs.writeFileSync(envFilename, JSON.stringify(environment, null, 2));
        console.log(`✓ Created: ${envFilename}`);
        
        console.log('\n=== Summary ===');
        console.log(`Total update requests generated: ${updateRequests.length}`);
        console.log(`Collections created: ${collectionsCount}`);
        console.log(`Nearby Attractions that will be set: ${nearbyMatchedCount}`);
        console.log(`Nearby Attractions that will be null: ${updateRequests.length - nearbyMatchedCount}`);
        console.log('\n✓ All collections generated successfully!');
        
        resolve();
      })
      .on('error', (error) => {
        reject(error);
      });
  });
}

// Run the generator
generateCollections()
  .then(() => {
    console.log('\n✓ Script completed!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\n✗ Error:', error.message);
    process.exit(1);
  });

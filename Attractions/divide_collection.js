const fs = require('fs');
const path = require('path');

console.log('📦 Dividing Attractions Collection into 4 Parts...\n');

// Read the complete collection
const collectionPath = path.join(__dirname, 'collection', 'Strapi_Attractions_Complete.postman_collection.json');
const completeCollection = JSON.parse(fs.readFileSync(collectionPath, 'utf8'));

const totalItems = completeCollection.item.length;
console.log(`   Total entries: ${totalItems}`);

// Calculate items per part (approximately 1000 each)
const itemsPerPart = Math.ceil(totalItems / 4);
console.log(`   Items per part: ~${itemsPerPart}\n`);

// Divide into 4 parts
const parts = [
  { start: 0, end: itemsPerPart, name: 'Part 1 of 4' },
  { start: itemsPerPart, end: itemsPerPart * 2, name: 'Part 2 of 4' },
  { start: itemsPerPart * 2, end: itemsPerPart * 3, name: 'Part 3 of 4' },
  { start: itemsPerPart * 3, end: totalItems, name: 'Part 4 of 4' }
];

parts.forEach((part, index) => {
  const partNum = index + 1;
  const items = completeCollection.item.slice(part.start, part.end);
  const actualCount = items.length;
  
  // Add numbering to each request name
  const numberedItems = items.map((item, idx) => {
    const globalNumber = part.start + idx + 1;
    const originalName = item.name;
    
    // Update the name to include the number at the beginning
    const numberedItem = {
      ...item,
      name: `${globalNumber}. ${originalName}`
    };
    
    return numberedItem;
  });
  
  // Create part collection
  const partCollection = {
    info: {
      name: `Strapi Attractions - ${part.name} (${actualCount} entries)`,
      description: `Part ${partNum} of 4: Attractions ${part.start + 1} to ${part.end} (${actualCount} entries)`,
      schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    item: numberedItems,
    variable: completeCollection.variable
  };
  
  // Save part collection
  const outputPath = path.join(__dirname, 'collection', `Strapi_Attractions_Part_${partNum}_of_4.postman_collection.json`);
  fs.writeFileSync(outputPath, JSON.stringify(partCollection, null, 2));
  
  console.log(`✅ Part ${partNum}: Entries ${part.start + 1}-${part.end} (${actualCount} entries)`);
  console.log(`   File: collection/Strapi_Attractions_Part_${partNum}_of_4.postman_collection.json`);
  
  // Calculate approximate file size
  const stats = fs.statSync(outputPath);
  const fileSizeMB = (stats.size / (1024 * 1024)).toFixed(2);
  console.log(`   Size: ${fileSizeMB} MB\n`);
});

console.log('✨ Collection successfully divided into 4 parts!\n');

// Print summary
console.log('📊 Summary:');
console.log(`   Total entries: ${totalItems}`);
console.log(`   Part 1: ${parts[0].end - parts[0].start} entries`);
console.log(`   Part 2: ${parts[1].end - parts[1].start} entries`);
console.log(`   Part 3: ${parts[2].end - parts[2].start} entries`);
console.log(`   Part 4: ${parts[3].end - parts[3].start} entries`);

console.log('\n💡 Next steps:');
console.log('   1. Import each part collection into Postman');
console.log('   2. Run parts sequentially (Part 1 → Part 2 → Part 3 → Part 4)');
console.log('   3. Use 200-300ms delay between requests');
console.log('   4. Estimated time per part: 8-12 minutes');
console.log('   5. Total estimated time: 35-50 minutes');



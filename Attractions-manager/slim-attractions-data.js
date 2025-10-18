const fs = require('fs');

// Configuration
const INPUT_FILE = 'all-attractions.json';
const OUTPUT_FILE = 'all-attractions-slim.json';

// Fields to keep (essential fields only)
const FIELDS_TO_KEEP = [
  'id',
  'documentId',
  'Name',
  'Slug',
  'City',
  'Country',
  'Rating',
  'createdAt',
  'updatedAt',
  'publishedAt',
  'locale'
];

console.log('Reading attractions data...');
const attractionsData = JSON.parse(fs.readFileSync(INPUT_FILE, 'utf8'));

console.log(`Total entries: ${attractionsData.length}`);
console.log(`\nKeeping only these fields: ${FIELDS_TO_KEEP.join(', ')}`);

// Slim down the data
const slimData = attractionsData.map(item => {
  const slimItem = {};
  FIELDS_TO_KEEP.forEach(field => {
    if (item.hasOwnProperty(field)) {
      slimItem[field] = item[field];
    }
  });
  return slimItem;
});

// Save slim data
fs.writeFileSync(OUTPUT_FILE, JSON.stringify(slimData, null, 2));

console.log(`\n✓ Slim data saved to ${OUTPUT_FILE}`);

// Show file size comparison
const originalSize = fs.statSync(INPUT_FILE).size;
const newSize = fs.statSync(OUTPUT_FILE).size;
const reduction = ((originalSize - newSize) / originalSize * 100).toFixed(2);

console.log('\n=== File Size Comparison ===');
console.log(`Original: ${(originalSize / 1024 / 1024).toFixed(2)} MB`);
console.log(`Slim:     ${(newSize / 1024 / 1024).toFixed(2)} MB`);
console.log(`Reduction: ${reduction}%`);

// Show sample
console.log('\nSample of slim data (first 2 items):');
console.log(JSON.stringify(slimData.slice(0, 2), null, 2));


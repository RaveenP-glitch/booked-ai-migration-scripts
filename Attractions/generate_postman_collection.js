const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

console.log('📁 Loading reference data...');

// Load media IDs mapping
const mediaMapping = JSON.parse(
  fs.readFileSync(path.join(__dirname, '../Graphql-asset-manager/media-ids-and-names.json'), 'utf8')
);
console.log(`   ✓ Loaded ${mediaMapping.length} media entries`);

// Load explores data
const exploresData = JSON.parse(
  fs.readFileSync(path.join(__dirname, '../Explores-manager/all-explores.json'), 'utf8')
);
console.log(`   ✓ Loaded ${exploresData.length} explore entries`);

// Create lookup maps
const mediaMap = new Map();
mediaMapping.forEach(item => {
  const name = item.name.toLowerCase();
  mediaMap.set(name, item.id);
  // Also create entries without file extension for easier matching
  const nameWithoutExt = name.replace(/\.[^/.]+$/, '');
  if (nameWithoutExt !== name) {
    mediaMap.set(nameWithoutExt, item.id);
  }
});

const exploresMap = new Map();
exploresData.forEach(explore => {
  if (explore.Slug) {
    exploresMap.set(explore.Slug.toLowerCase(), explore.documentId);
  }
});

console.log('   ✓ Created lookup maps\n');

// Track missing images for reporting
const missingImages = new Set();

// Function to find media ID by URL or filename
function findMediaId(imageUrl) {
  if (!imageUrl || imageUrl.trim() === '') return null;
  
  // Extract filename from URL
  const filename = imageUrl.split('/').pop().toLowerCase();
  
  // Try exact match first
  if (mediaMap.has(filename)) {
    return mediaMap.get(filename);
  }
  
  // Try without file extension
  const filenameWithoutExt = filename.replace(/\.[^/.]+$/, '');
  if (mediaMap.has(filenameWithoutExt)) {
    return mediaMap.get(filenameWithoutExt);
  }
  
  // Try extracting the ID part (e.g., "68a54bc71f80760099af9dd7_photo.jpeg" -> "68a54bc71f80760099af9dd7")
  const idMatch = filename.match(/^([a-f0-9]{24,})/);
  if (idMatch) {
    const idPart = idMatch[1];
    for (let [name, id] of mediaMap) {
      if (name.startsWith(idPart)) {
        return id;
      }
    }
  }
  
  // Try fuzzy matching (check if any part of the filename matches)
  for (let [name, id] of mediaMap) {
    if (name.includes(filenameWithoutExt) || filenameWithoutExt.includes(name.split('.')[0])) {
      return id;
    }
  }
  
  // If no match found, add to missing images
  missingImages.add(filename);
  return null;
}

// Function to parse HTML to Strapi blocks
function htmlToBlocks(html) {
  if (!html || html.trim() === '') return [];
  
  const blocks = [];
  html = html.trim();
  
  // Handle special case: hours wrapper div
  if (html.includes('hours-wrapper') || (html.includes('day') && html.includes('time'))) {
    const dayMatches = html.match(/<div class="day">([^<]+)<\/div>/gi) || [];
    const timeMatches = html.match(/<div class="time">([^<]+)<\/div>/gi) || [];
    
    for (let i = 0; i < Math.min(dayMatches.length, timeMatches.length); i++) {
      const day = dayMatches[i].replace(/<[^>]+>/g, '').trim();
      const time = timeMatches[i].replace(/<[^>]+>/g, '').trim();
      blocks.push({
        type: 'paragraph',
        children: [{ type: 'text', text: `${day}: ${time}` }]
      });
    }
    return blocks;
  }
  
  // Handle lists
  if (html.match(/<ul|<ol/i)) {
    const listMatch = html.match(/<(ul|ol)(?:\s+[^>]*)?>(.+?)<\/\1>/is);
    if (listMatch) {
      const listType = listMatch[1].toLowerCase();
      const listContent = listMatch[2];
      const items = listContent.match(/<li(?:\s+[^>]*)?>(.+?)<\/li>/gis) || [];
      
      const listItems = [];
      items.forEach(item => {
        const itemText = item.replace(/<\/?li[^>]*>/gi, '').replace(/<[^>]+>/g, '').trim();
        if (itemText) {
          listItems.push({
            type: 'list-item',
            children: [{ type: 'text', text: itemText }]
          });
        }
      });
      
      if (listItems.length > 0) {
        blocks.push({
          type: 'list',
          format: listType === 'ul' ? 'unordered' : 'ordered',
          children: listItems
        });
      }
      return blocks;
    }
  }
  
  // Handle headings and paragraphs
  const elements = [];
  let currentPos = 0;
  const elementRegex = /<(h[1-6]|p|div)(?:\s+[^>]*)?>(.+?)<\/\1>/gis;
  let match;
  
  while ((match = elementRegex.exec(html)) !== null) {
    elements.push({
      tag: match[1].toLowerCase(),
      content: match[2],
      index: match.index
    });
  }
  
  if (elements.length === 0) {
    // No HTML tags, treat as plain text
    const text = html.replace(/<[^>]+>/g, '').trim();
    if (text) {
      blocks.push({
        type: 'paragraph',
        children: [{ type: 'text', text: text }]
      });
    }
    return blocks;
  }
  
  elements.forEach(element => {
    const tag = element.tag;
    const content = element.content.replace(/<[^>]+>/g, '').trim();
    
    if (!content) return;
    
    if (tag.match(/^h[1-6]$/)) {
      const level = parseInt(tag.charAt(1));
      blocks.push({
        type: 'heading',
        level: level,
        children: [{ type: 'text', text: content }]
      });
    } else if (tag === 'p' || tag === 'div') {
      blocks.push({
        type: 'paragraph',
        children: [{ type: 'text', text: content }]
      });
    }
  });
  
  return blocks;
}

// Function to generate slug from name
function generateSlug(name) {
  if (!name) return '';
  return name
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '') // Remove special characters
    .replace(/\s+/g, '-') // Replace spaces with hyphens
    .replace(/-+/g, '-') // Replace multiple hyphens with single hyphen
    .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
}

// Function to create Strapi request body
function createStrapiEntry(row) {
  const entry = {
    data: {}
  };
  
  // Basic string fields
  if (row.Name) {
    entry.data.Name = row.Name;
    // Auto-generate slug from Name if not provided
    entry.data.Slug = row.Slug || generateSlug(row.Name);
  }
  if (row['Main Title']) entry.data.Main_Title = row['Main Title'];
  if (row.City) entry.data.City = row.City;
  if (row.Country) entry.data.Country = row.Country;
  if (row.Location) entry.data.Location = row.Location;
  if (row['Formatted Address']) entry.data.Formatted_Address = row['Formatted Address'];
  if (row['Entry Fee']) entry.data.Entry_Fee = row['Entry Fee'];
  if (row['Review Rating']) entry.data.Review_Rating = row['Review Rating'];
  if (row['Review Link']) entry.data.Review_Link = row['Review Link'];
  
  // Text fields
  if (row.Description) entry.data.Description = row.Description;
  if (row.Overview) entry.data.Overview = row.Overview;
  if (row.Intro) entry.data.Intro = row.Intro;
  if (row['Short Summary']) entry.data.Short_Summary = row['Short Summary'];
  if (row['Visitor Count Description']) entry.data.Visitor_Count_Description = row['Visitor Count Description'];
  if (row['Review Text']) entry.data.Review_Text = row['Review Text'];
  
  // Tags
  if (row['Tag 1']) entry.data.Tag1 = row['Tag 1'];
  if (row['Tag 2']) entry.data.Tag2 = row['Tag 2'];
  if (row['Tag 3']) entry.data.Tag3 = row['Tag 3'];
  
  // Numeric fields
  if (row.Rating) {
    const rating = parseFloat(row.Rating);
    if (!isNaN(rating)) entry.data.Rating = rating;
  }
  
  if (row['Visitor Count']) {
    const visitorCount = row['Visitor Count'].replace(/,/g, '');
    const count = parseInt(visitorCount);
    if (!isNaN(count)) entry.data.Visitor_Count = count.toString();
  }
  
  if (row['Review Count']) {
    const reviewCount = row['Review Count'].replace(/k/i, '000').replace(/,/g, '').replace(' reviews', '');
    const count = parseInt(reviewCount);
    if (!isNaN(count)) entry.data.Review_Count = count.toString();
  }
  
  // Main Image
  if (row['Main Image']) {
    const mainImageId = findMediaId(row['Main Image']);
    if (mainImageId) {
      entry.data.Main_Image = mainImageId;
    }
  }
  
  // Photos (multiple images)
  if (row.Photos) {
    const photoUrls = row.Photos.split(';').map(url => url.trim()).filter(url => url);
    const photoIds = photoUrls.map(url => findMediaId(url)).filter(id => id !== null);
    if (photoIds.length > 0) {
      entry.data.Photos = photoIds;
    }
  }
  
  // Individual Photo fields
  if (row['Photo 1']) {
    const photo1Id = findMediaId(row['Photo 1']);
    if (photo1Id) entry.data.Photo1 = photo1Id;
  }
  if (row['Photo 2']) {
    const photo2Id = findMediaId(row['Photo 2']);
    if (photo2Id) entry.data.Photo2 = photo2Id;
  }
  if (row['Photo 3']) {
    const photo3Id = findMediaId(row['Photo 3']);
    if (photo3Id) entry.data.Photo3 = photo3Id;
  }
  
  // FAQ fields
  if (row['FAQ 1']) entry.data.FAQ1 = row['FAQ 1'];
  if (row['FAQ 2']) entry.data.FAQ2 = row['FAQ 2'];
  if (row['FAQ 3']) entry.data.FAQ3 = row['FAQ 3'];
  if (row['FAQ 4']) entry.data.FAQ4 = row['FAQ 4'];
  if (row['FAQ 5']) entry.data.FAQ5 = row['FAQ 5'];
  
  // Block type fields - only add if content exists and has blocks
  if (row['Inner Page'] && row['Inner Page'].trim()) {
    const blocks = htmlToBlocks(row['Inner Page']);
    if (blocks.length > 0) {
      entry.data.Inner_Page = blocks;
    }
  }
  
  if (row['Opening Hours'] && row['Opening Hours'].trim()) {
    const blocks = htmlToBlocks(row['Opening Hours']);
    if (blocks.length > 0) {
      entry.data.Opening_Hours = blocks;
    }
  }
  
  if (row['Inner Content'] && row['Inner Content'].trim()) {
    const blocks = htmlToBlocks(row['Inner Content']);
    if (blocks.length > 0) {
      entry.data.Inner_Content = blocks;
    }
  }
  
  if (row.Amenities && row.Amenities.trim()) {
    const blocks = htmlToBlocks(row.Amenities);
    if (blocks.length > 0) {
      entry.data.Amenities = blocks;
    }
  }
  
  if (row['Best Time to Visit'] && row['Best Time to Visit'].trim()) {
    const blocks = htmlToBlocks(row['Best Time to Visit']);
    if (blocks.length > 0) {
      entry.data.Best_Time_to_Visit = blocks;
    }
  }
  
  if (row['Photography Allowed'] && row['Photography Allowed'].trim()) {
    const blocks = htmlToBlocks(row['Photography Allowed']);
    if (blocks.length > 0) {
      entry.data.Photography_Allowed = blocks;
    }
  }
  
  if (row['Accessibility Notes'] && row['Accessibility Notes'].trim()) {
    const blocks = htmlToBlocks(row['Accessibility Notes']);
    if (blocks.length > 0) {
      entry.data.Accessibility_Notes = blocks;
    }
  }
  
  if (row['Cultural/Religious Notes'] && row['Cultural/Religious Notes'].trim()) {
    const blocks = htmlToBlocks(row['Cultural/Religious Notes']);
    if (blocks.length > 0) {
      entry.data.Cultural_or_Religous_Notes = blocks;
    }
  }
  
  if (row['Historical Significance'] && row['Historical Significance'].trim()) {
    const blocks = htmlToBlocks(row['Historical Significance']);
    if (blocks.length > 0) {
      entry.data.Historical_Significance = blocks;
    }
  }
  
  if (row['Famous Events or Dates'] && row['Famous Events or Dates'].trim()) {
    const blocks = htmlToBlocks(row['Famous Events or Dates']);
    if (blocks.length > 0) {
      entry.data.Famous_Events_or_Dates = blocks;
    }
  }
  
  if (row['Time Required to Explore'] && row['Time Required to Explore'].trim()) {
    const blocks = htmlToBlocks(row['Time Required to Explore']);
    if (blocks.length > 0) {
      entry.data.Time_Required_to_Explore = blocks;
    }
  }
  
  if (row['Kid/Family Friendly'] && row['Kid/Family Friendly'].trim()) {
    const blocks = htmlToBlocks(row['Kid/Family Friendly']);
    if (blocks.length > 0) {
      entry.data.Kid_or_Family_Friendly = blocks;
    }
  }
  
  if (row['Weather Sensitivity'] && row['Weather Sensitivity'].trim()) {
    const blocks = htmlToBlocks(row['Weather Sensitivity']);
    if (blocks.length > 0) {
      entry.data.Weather_Sensitivity = blocks;
    }
  }
  
  if (row['Transportation and Accessibility'] && row['Transportation and Accessibility'].trim()) {
    const blocks = htmlToBlocks(row['Transportation and Accessibility']);
    if (blocks.length > 0) {
      entry.data.Transportation_and_Accessibility = blocks;
    }
  }
  
  // Explore relationship
  if (row.Explore) {
    const exploreSlug = row.Explore.toLowerCase().trim();
    const exploreDocId = exploresMap.get(exploreSlug);
    if (exploreDocId) {
      entry.data.Explore = exploreDocId;
    }
  }
  
  // Sitemap indexing (default to true)
  entry.data.Sitemap_Indexing = true;
  
  return entry;
}

// Function to generate Postman collection
function generatePostmanCollection(entries, collectionName, outputFileName) {
  const collection = {
    info: {
      name: collectionName,
      description: `Collection for uploading ${entries.length} attraction entries to Strapi`,
      schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    item: [],
    variable: [
      {
        key: "baseUrl",
        value: "{{STRAPI_URL}}",
        type: "string"
      },
      {
        key: "apiToken",
        value: "{{STRAPI_API_TOKEN}}",
        type: "string"
      }
    ]
  };
  
  entries.forEach((entry, index) => {
    const attractionName = entry.data.Name || `Attraction ${index + 1}`;
    
    collection.item.push({
      name: `Create Attraction - ${attractionName}`,
      request: {
        method: "POST",
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
          raw: JSON.stringify(entry, null, 2)
        },
        url: {
          raw: "{{baseUrl}}/api/attractions",
          host: ["{{baseUrl}}"],
          path: ["api", "attractions"]
        }
      },
      response: []
    });
  });
  
  // Write collection to file
  const outputPath = path.join(__dirname, 'collection', outputFileName);
  fs.writeFileSync(outputPath, JSON.stringify(collection, null, 2));
  console.log(`✅ Generated ${outputFileName} with ${entries.length} entries`);
}

// Main processing function
async function processCSV(testMode = false) {
  const csvFilePath = path.join(__dirname, 'collection', 'Booked (Live) - Attractions-4340.csv');
  const allEntries = [];
  
  return new Promise((resolve, reject) => {
    fs.createReadStream(csvFilePath)
      .pipe(csv())
      .on('data', (row) => {
        try {
          const entry = createStrapiEntry(row);
          allEntries.push(entry);
        } catch (error) {
          console.error(`Error processing row: ${row.Name}`, error.message);
        }
      })
      .on('end', () => {
        console.log(`\n📊 Total entries processed: ${allEntries.length}`);
        
        if (testMode) {
          // Get last 5 entries for test collection
          const testEntries = allEntries.slice(-5);
          console.log(`\n🧪 Creating test collection with last 5 entries...`);
          generatePostmanCollection(
            testEntries,
            'Strapi Attractions - Test (Last 5)',
            'Strapi_Attractions_Test_5.postman_collection.json'
          );
        } else {
          // Generate full collection
          console.log(`\n📦 Creating full collection with all entries...`);
          generatePostmanCollection(
            allEntries,
            'Strapi Attractions - Complete Collection',
            'Strapi_Attractions_Complete.postman_collection.json'
          );
        }
        
        resolve(allEntries);
      })
      .on('error', reject);
  });
}

// Run the script
const testMode = process.argv.includes('--test');

console.log('🚀 Starting Attractions Postman Collection Generator...\n');

processCSV(testMode)
  .then(entries => {
    console.log('\n✨ Collection generation complete!');
    
    // Print summary
    console.log('\n📈 Summary:');
    console.log(`   Total entries processed: ${entries.length}`);
    
    const entriesWithImages = entries.filter(e => e.data.Main_Image).length;
    console.log(`   Entries with main images: ${entriesWithImages}`);
    
    const entriesWithPhotos = entries.filter(e => e.data.Photos && e.data.Photos.length > 0).length;
    console.log(`   Entries with photo galleries: ${entriesWithPhotos}`);
    
    const entriesWithExplores = entries.filter(e => e.data.Explore).length;
    console.log(`   Entries with Explore relations: ${entriesWithExplores}`);
    
    const entriesWithBlocks = entries.filter(e => 
      e.data.Inner_Page || e.data.Opening_Hours || e.data.Inner_Content
    ).length;
    console.log(`   Entries with block content: ${entriesWithBlocks}`);
    
    if (missingImages.size > 0) {
      console.log(`\n⚠️  Missing Images (${missingImages.size} unique):`);
      const missingArray = Array.from(missingImages).slice(0, 10);
      missingArray.forEach(img => console.log(`      - ${img}`));
      if (missingImages.size > 10) {
        console.log(`      ... and ${missingImages.size - 10} more`);
      }
      
      // Save missing images report
      const missingImagesReport = {
        count: missingImages.size,
        images: Array.from(missingImages)
      };
      fs.writeFileSync(
        path.join(__dirname, 'collection', 'missing_images_report.json'),
        JSON.stringify(missingImagesReport, null, 2)
      );
      console.log('\n   📝 Full missing images report saved to: collection/missing_images_report.json');
    }
    
    console.log('\n💡 Next steps:');
    console.log('   1. Review the generated collection file');
    if (testMode) {
      console.log('   2. Test with the 5-entry collection: collection/Strapi_Attractions_Test_5.postman_collection.json');
      console.log('   3. If successful, run full generation: npm run generate');
    } else {
      console.log('   2. Import collection/Strapi_Attractions_Complete.postman_collection.json into Postman');
    }
    console.log('   4. Set environment variables in Postman:');
    console.log('      - STRAPI_URL: Your Strapi instance URL');
    console.log('      - STRAPI_API_TOKEN: Your API token');
    console.log('   5. Run the collection to upload attractions to Strapi');
  })
  .catch(error => {
    console.error('❌ Error:', error);
    process.exit(1);
  });


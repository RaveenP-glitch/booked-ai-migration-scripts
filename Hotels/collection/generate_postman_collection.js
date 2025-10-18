const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// Load media IDs and names
const mediaData = JSON.parse(
  fs.readFileSync(
    path.join(__dirname, '../../Graphql-asset-manager/media-ids-and-names.json'),
    'utf8'
  )
);

// Load all attractions
const attractionsData = JSON.parse(
  fs.readFileSync(
    path.join(__dirname, '../../Attractions-manager/all-attractions.json'),
    'utf8'
  )
);

// Load all explores
const exploresData = JSON.parse(
  fs.readFileSync(
    path.join(__dirname, '../../Explores-manager/all-explores.json'),
    'utf8'
  )
);

// Create a mapping for quick image lookup
const imageMap = new Map();
mediaData.forEach(media => {
  const fileName = media.name.toLowerCase();
  imageMap.set(fileName, media.id);
  
  // Also map without extension and hash
  const nameWithoutExt = fileName.replace(/\.[^/.]+$/, '');
  const hashMatch = nameWithoutExt.match(/^([a-f0-9]+)_/);
  if (hashMatch) {
    const hashPart = hashMatch[1];
    imageMap.set(hashPart, media.id);
  }
});

// Create mapping for attractions by name
const attractionMap = new Map();
attractionsData.forEach(attraction => {
  if (attraction.Name) {
    const nameLower = attraction.Name.toLowerCase().trim();
    attractionMap.set(nameLower, attraction.documentId);
  }
});

// Create mapping for explores by slug
const exploreMap = new Map();
exploresData.forEach(explore => {
  if (explore.Slug) {
    const slugLower = explore.Slug.toLowerCase().trim();
    exploreMap.set(slugLower, explore.documentId);
  }
});

/**
 * Extract image ID from URL
 */
function findImageId(url) {
  if (!url || url.trim() === '') return null;
  
  try {
    const fileName = url.split('/').pop().toLowerCase();
    
    // Try exact match first
    if (imageMap.has(fileName)) {
      return imageMap.get(fileName);
    }
    
    // Try without extension
    const nameWithoutExt = fileName.replace(/\.[^/.]+$/, '');
    if (imageMap.has(nameWithoutExt)) {
      return imageMap.get(nameWithoutExt);
    }
    
    // Try extracting hash part
    const hashMatch = fileName.match(/([a-f0-9]{24})_/);
    if (hashMatch && imageMap.has(hashMatch[1])) {
      return imageMap.get(hashMatch[1]);
    }
    
    // Try partial match on hash
    const fullHashMatch = fileName.match(/([a-f0-9]{24})/);
    if (fullHashMatch) {
      const hash = fullHashMatch[1];
      for (const [key, id] of imageMap.entries()) {
        if (key.includes(hash)) {
          return id;
        }
      }
    }
  } catch (error) {
    console.error(`Error finding image ID for URL: ${url}`, error);
  }
  
  return null;
}

/**
 * Parse HTML list to block format
 */
function parseHtmlToBlocks(html) {
  if (!html || html.trim() === '') return [];
  
  const blocks = [];
  
  // Match list items
  const listItemRegex = /<li>(.*?)<\/li>/gs;
  const matches = [...html.matchAll(listItemRegex)];
  
  if (matches.length > 0) {
    const listItems = matches.map(match => {
      const text = match[1]
        .replace(/<[^>]*>/g, '')
        .replace(/&apos;/g, "'")
        .replace(/&quot;/g, '"')
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&nbsp;/g, ' ')
        .trim();
      
      return {
        type: 'list-item',
        children: [{ type: 'text', text }]
      };
    });
    
    blocks.push({
      type: 'list',
      format: 'unordered',
      children: listItems
    });
  } else {
    // Parse as paragraphs
    const cleanText = html
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]*>/g, '')
      .replace(/&apos;/g, "'")
      .replace(/&quot;/g, '"')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&nbsp;/g, ' ')
      .trim();
    
    const paragraphs = cleanText.split('\n').filter(p => p.trim());
    
    paragraphs.forEach(para => {
      blocks.push({
        type: 'paragraph',
        children: [{ type: 'text', text: para.trim() }]
      });
    });
  }
  
  return blocks;
}

/**
 * Find explore by slug
 */
function findExploreBySlug(exploreSlug) {
  if (!exploreSlug || exploreSlug.trim() === '') return null;
  
  const slugLower = exploreSlug.toLowerCase().trim();
  
  // Direct match
  if (exploreMap.has(slugLower)) {
    return exploreMap.get(slugLower);
  }
  
  // Try with 'trip-to-' prefix if not present
  if (!slugLower.startsWith('trip-to-')) {
    const withPrefix = 'trip-to-' + slugLower;
    if (exploreMap.has(withPrefix)) {
      return exploreMap.get(withPrefix);
    }
  }
  
  return null;
}

/**
 * Find nearby attractions
 */
function findNearbyAttractions(hotelName, city, country, maxResults = 5) {
  const results = [];
  
  if (!city && !country) return results;
  
  const cityLower = city ? city.toLowerCase().trim() : '';
  const countryLower = country ? country.toLowerCase().trim() : '';
  
  // Find attractions in the same city or country
  for (const attraction of attractionsData) {
    if (results.length >= maxResults) break;
    
    const attrCity = attraction.City ? attraction.City.toLowerCase().trim() : '';
    const attrCountry = attraction.Country ? attraction.Country.toLowerCase().trim() : '';
    
    // Match by city first
    if (cityLower && attrCity && attrCity === cityLower) {
      results.push(attraction.documentId);
    } else if (countryLower && attrCountry && attrCountry === countryLower && results.length < maxResults) {
      // Match by country if city doesn't match
      if (!results.includes(attraction.documentId)) {
        results.push(attraction.documentId);
      }
    }
  }
  
  return results;
}

/**
 * Parse review count with K notation support
 */
function parseReviewCount(reviewCountStr) {
  if (!reviewCountStr || reviewCountStr.trim() === '') return null;
  
  // Remove "reviews" text
  let cleaned = reviewCountStr.toLowerCase().replace('reviews', '').trim();
  
  // Check for K notation (e.g., "4.8k", "1.2k", "5.3k")
  const kMatch = cleaned.match(/^(\d+\.?\d*)\s*k$/i);
  if (kMatch) {
    const value = parseFloat(kMatch[1]);
    return Math.round(value * 1000);
  }
  
  // Try regular integer parsing
  const intValue = parseInt(cleaned);
  return isNaN(intValue) ? null : intValue;
}

/**
 * Process a hotel row
 */
function processHotelRow(row) {
  const hotel = {
    Name: row.Name || '',
    Slug: row.Slug || '',
    Description: row.Description || '',
    Formatted_Address: row['Formatted Address'] || '',
    Ratings: row.Ratings ? parseFloat(row.Ratings) : null,
    Tag1: row['Tag 1'] || '',
    Tag2: row['Tag 2'] || '',
    Tag3: row['Tag 3'] || '',
    City: row.City || '',
    Country: row.Country || '',
    Overview: row.Overview || '',
    Intro: row.Intro || '',
    Short_Summary: row['Short Summary'] || '',
    Website: row.Website || '',
    Phone_Number: row['Phone Number'] || '',
    Price: row.Price || '',
    Check_in: row['Check in'] || '',
    Check_out: row['Check out'] || '',
    Review_Count: parseReviewCount(row['Review Count']),
    Review_Text: row['Review Text'] || '',
    Review_Rating: row['Review Rating'] || '',
    FAQ1: row['FAQ 1'] || '',
    FAQ2: row['FAQ 2'] || '',
    FAQ3: row['FAQ 3'] || '',
    FAQ4: row['FAQ 4'] || '',
    FAQ5: row['FAQ 5'] || '',
    Policies: row.Policies || '',
    Sustainability: row.Sustainability || '',
    Accessibility: row.Accessibility || '',
    Sitemap_Indexing: true
  };
  
  // Process Image
  const imageId = findImageId(row.Image);
  if (imageId) {
    hotel.Image = imageId;
  }
  
  // Process Photo1, Photo2, Photo3
  const photo1Id = findImageId(row['Photo 1']);
  if (photo1Id) {
    hotel.Photo1 = photo1Id;
  }
  
  const photo2Id = findImageId(row['Photo 2']);
  if (photo2Id) {
    hotel.Photo2 = photo2Id;
  }
  
  const photo3Id = findImageId(row['Photo 3']);
  if (photo3Id) {
    hotel.Photo3 = photo3Id;
  }
  
  // Process Photos (multiple)
  if (row.Photos) {
    const photoUrls = row.Photos.split(';').map(url => url.trim()).filter(url => url);
    const photoIds = photoUrls.map(url => findImageId(url)).filter(id => id !== null);
    if (photoIds.length > 0) {
      hotel.Photos = photoIds;
    }
  }
  
  // Process block fields
  if (row['Inner Page']) {
    hotel.Inner_Page = parseHtmlToBlocks(row['Inner Page']);
  }
  
  if (row.Amenities) {
    hotel.Amenities = parseHtmlToBlocks(row.Amenities);
  }
  
  if (row.Pros) {
    hotel.Pros = parseHtmlToBlocks(row.Pros);
  }
  
  if (row.Cons) {
    hotel.Cons = parseHtmlToBlocks(row.Cons);
  }
  
  // Find nearby attractions
  const nearbyAttractions = findNearbyAttractions(hotel.Name, hotel.City, hotel.Country);
  if (nearbyAttractions.length > 0) {
    hotel.Nearby_Attractions = nearbyAttractions;
  }
  
  // Find and map Explore
  if (row.Explore) {
    const exploreDocId = findExploreBySlug(row.Explore);
    if (exploreDocId) {
      hotel.Explore = exploreDocId;
    }
  }
  
  return hotel;
}

/**
 * Create Postman request for a hotel
 */
function createPostmanRequest(hotel, index) {
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

/**
 * Generate Postman collection
 */
async function generateCollection(limit = null, outputFileName = 'Strapi_Hotels_Collection.postman_collection.json') {
  return new Promise((resolve, reject) => {
    const hotels = [];
    const csvPath = path.join(__dirname, '../Booked (Live) - Hotels-3971.csv');
    
    fs.createReadStream(csvPath)
      .pipe(csv())
      .on('data', (row) => {
        if (limit === null || hotels.length < limit) {
          try {
            const hotel = processHotelRow(row);
            hotels.push(hotel);
          } catch (error) {
            console.error(`Error processing hotel: ${row.Name}`, error);
          }
        }
      })
      .on('end', () => {
        console.log(`Processed ${hotels.length} hotels`);
        
        // Create Postman collection
        const collection = {
          info: {
            name: limit ? `Strapi Hotels Test Collection (${limit} entries)` : 'Strapi Hotels Complete Collection',
            description: `Postman collection to upload ${limit ? limit : 'all'} hotel entries to Strapi`,
            schema: 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
          },
          item: hotels.map((hotel, index) => createPostmanRequest(hotel, index)),
          variable: []
        };
        
        // Save collection
        const outputPath = path.join(__dirname, outputFileName);
        fs.writeFileSync(outputPath, JSON.stringify(collection, null, 2));
        console.log(`Collection saved to: ${outputPath}`);
        
        // Save processed data for review
        const dataOutputPath = path.join(__dirname, outputFileName.replace('.postman_collection.json', '_data.json'));
        fs.writeFileSync(dataOutputPath, JSON.stringify(hotels, null, 2));
        console.log(`Processed data saved to: ${dataOutputPath}`);
        
        resolve(hotels);
      })
      .on('error', reject);
  });
}

// Main execution
async function main() {
  const args = process.argv.slice(2);
  const isTest = args.includes('--test');
  
  if (isTest) {
    console.log('Generating test collection for first 5 hotels...');
    await generateCollection(5, 'Strapi_Hotels_Test_5.postman_collection.json');
  } else {
    console.log('Generating complete collection for all hotels...');
    await generateCollection(null, 'Strapi_Hotels_Complete.postman_collection.json');
  }
  
  console.log('Done!');
}

main().catch(console.error);


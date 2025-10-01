const fs = require('fs');
const path = require('path');

const csvFilePath = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/Booked (Live) - Blogs (2).csv';
const allImagesJsonPath = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/all-images.json';

// Load all images data
const allImagesData = JSON.parse(fs.readFileSync(allImagesJsonPath, 'utf8'));

// Create a map for quick image lookup
const imageIdMap = {};
const imageNameById = {};
allImagesData.forEach(image => {
    const hash8 = image.name.substring(0, 8);
    if (!imageIdMap[hash8]) {
        imageIdMap[hash8] = [];
    }
    imageIdMap[hash8].push({
        id: image.id,
        name: image.name
    });
    imageNameById[image.id] = image.name;
});

// Function to parse CSV line
function parseCSVLine(line) {
    const result = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        const nextChar = line[i + 1];
        
        if (char === '"') {
            if (inQuotes && nextChar === '"') {
                current += '"';
                i++;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (char === ',' && !inQuotes) {
            result.push(current);
            current = '';
        } else {
            current += char;
        }
    }
    result.push(current);
    return result;
}

// Function to extract filename from URL
function extractFilename(url) {
    if (!url) return null;
    try {
        const urlObj = new URL(url);
        const pathname = decodeURIComponent(urlObj.pathname);
        return path.basename(pathname);
    } catch (error) {
        return null;
    }
}

// Function to find image ID by URL
function findImageIdByURL(imageUrl) {
    if (!imageUrl) return null;
    
    const filename = extractFilename(imageUrl);
    if (!filename) return null;
    
    const match = filename.match(/^([0-9a-f]{24})_/i);
    if (!match) return null;
    
    const fullHash = match[1];
    const hash8 = fullHash.substring(0, 8);
    
    if (imageIdMap[hash8]) {
        for (const img of imageIdMap[hash8]) {
            if (img.name.startsWith(fullHash)) {
                return img.id;
            }
        }
        return imageIdMap[hash8][0].id;
    }
    
    return null;
}

// Function to clean HTML
function cleanHtmlContent(html) {
    if (!html) return '';
    return html
        .replace(/<[^>]*>/g, '')
        .replace(/&nbsp;/g, ' ')
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/\s+/g, ' ')
        .trim();
}

// Function to parse and verify image mapping
function verifyImageMapping(blogDetailHTML, blogNumber, blogName) {
    if (!blogDetailHTML) return;
    
    console.log('='.repeat(80));
    console.log(`BLOG ${blogNumber}: ${blogName}`);
    console.log('='.repeat(80));
    
    // Split by h2 tags and track images
    const h2Regex = /<h2[^>]*>(.*?)<\/h2>/gi;
    const h2Matches = [];
    let h2Match;
    
    while ((h2Match = h2Regex.exec(blogDetailHTML)) !== null) {
        h2Matches.push({
            fullMatch: h2Match[0],
            heading: cleanHtmlContent(h2Match[1]),
            index: h2Match.index
        });
    }
    
    if (h2Matches.length === 0) {
        console.log('No h2 sections found in this blog\n');
        return;
    }
    
    // Extract content and images for each section
    for (let i = 0; i < h2Matches.length; i++) {
        const currentH2 = h2Matches[i];
        const nextH2 = h2Matches[i + 1];
        
        const startIndex = currentH2.index + currentH2.fullMatch.length;
        const endIndex = nextH2 ? nextH2.index : blogDetailHTML.length;
        
        const sectionHTML = blogDetailHTML.substring(startIndex, endIndex);
        
        // Extract all images from this section
        const imgRegex = /<img[^>]+src=["']([^"']+)["']/gi;
        const sectionImages = [];
        let imgMatch;
        
        while ((imgMatch = imgRegex.exec(sectionHTML)) !== null) {
            const imageUrl = imgMatch[1];
            const imageId = findImageIdByURL(imageUrl);
            const filename = extractFilename(imageUrl);
            sectionImages.push({
                url: imageUrl,
                filename: filename,
                imageId: imageId,
                imageName: imageId ? imageNameById[imageId] : null
            });
        }
        
        console.log(`\nSection ${i + 1}: "${currentH2.heading}"`);
        console.log('-'.repeat(80));
        
        if (sectionImages.length > 0) {
            console.log(`  Images found: ${sectionImages.length}`);
            sectionImages.forEach((img, idx) => {
                console.log(`  ${idx + 1}. URL: ${img.url.substring(0, 80)}...`);
                console.log(`     Filename: ${img.filename}`);
                console.log(`     Matched ID: ${img.imageId || 'NOT FOUND ❌'}`);
                if (img.imageName) {
                    console.log(`     Strapi Name: ${img.imageName}`);
                }
                console.log();
            });
            
            // Show which image would be used (first one)
            console.log(`  ✅ Blog_Part_${i + 1}_Image would be: ${sectionImages[0].imageId || 'null'}`);
        } else {
            console.log('  No images in this section');
            console.log(`  ✅ Blog_Part_${i + 1}_Image would be: null`);
        }
    }
    
    console.log();
}

// Read CSV
const csvContent = fs.readFileSync(csvFilePath, 'utf8');
const lines = csvContent.split('\n');
const headers = parseCSVLine(lines[0]);

const nameIdx = headers.indexOf('Name');
const blogDetailIdx = headers.indexOf('Blog Detail (OLD STUFF, DONT TOUCH)');

console.log('\n🔍 VERIFYING IMAGE-TO-SECTION MAPPING FOR FIRST 3 BLOGS\n');

// Verify first 3 blogs
for (let i = 2; i <= 4; i++) { // Blogs 2, 3, 4 (skip blog 1 as it has fewer images)
    const line = lines[i];
    if (!line.trim()) continue;
    
    const columns = parseCSVLine(line);
    const name = columns[nameIdx];
    const blogDetailHTML = columns[blogDetailIdx];
    
    verifyImageMapping(blogDetailHTML, i, name);
}

console.log('\n' + '='.repeat(80));
console.log('✅ VERIFICATION COMPLETE');
console.log('='.repeat(80));
console.log('\nThis shows exactly which images are in each section and how they map');
console.log('to the Blog_Part_X_Image fields in the generated request bodies.');
console.log();

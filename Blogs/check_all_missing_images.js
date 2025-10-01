const fs = require('fs');
const path = require('path');

const csvFilePath = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/Booked (Live) - Blogs (2).csv';
const allImagesJsonPath = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/all-images.json';

// Load all images data
const allImagesData = JSON.parse(fs.readFileSync(allImagesJsonPath, 'utf8'));

// Create a lookup map
const imageNameMap = {};
allImagesData.forEach(img => {
    imageNameMap[img.name] = img.id;
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

// Extract filename from URL
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

// Find image ID with better matching
function findImageId(url) {
    if (!url) return null;
    
    const filename = extractFilename(url);
    if (!filename) return null;
    
    // Try exact match first
    if (imageNameMap[filename]) {
        return imageNameMap[filename];
    }
    
    // Try with shortened hash (8 chars)
    const fullHash = filename.match(/^([0-9a-f]{24})_/i);
    if (fullHash) {
        const hash24 = fullHash[1];
        const hash8 = hash24.substring(0, 8);
        
        // Look for images starting with this hash
        for (const imageName in imageNameMap) {
            if (imageName.startsWith(hash8)) {
                return imageNameMap[imageName];
            }
        }
    }
    
    return null;
}

// Read CSV
const csvContent = fs.readFileSync(csvFilePath, 'utf8');
const lines = csvContent.split('\n');
const headers = parseCSVLine(lines[0]);

const nameIdx = headers.indexOf('Name');
const thumbnailIdx = headers.indexOf('Thumbnail Image');
const mainImageIdx = headers.indexOf('Main Image');

console.log('=== Checking First 5 Blogs for Missing Images ===\n');

const missingImages = [];

for (let i = 1; i <= 5 && i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    
    const columns = parseCSVLine(line);
    const name = columns[nameIdx];
    const thumbnailUrl = columns[thumbnailIdx];
    const mainImageUrl = columns[mainImageIdx];
    
    const thumbnailId = findImageId(thumbnailUrl);
    const mainImageId = findImageId(mainImageUrl);
    
    console.log(`Blog ${i}: ${name}`);
    console.log(`  Thumbnail: ${thumbnailId ? '✅ ID: ' + thumbnailId : '❌ Missing'}`);
    if (!thumbnailId && thumbnailUrl) {
        const filename = extractFilename(thumbnailUrl);
        console.log(`    URL: ${thumbnailUrl}`);
        console.log(`    Filename: ${filename}`);
        missingImages.push({ blog: i, type: 'thumbnail', filename, url: thumbnailUrl });
    }
    
    console.log(`  Main Image: ${mainImageId ? '✅ ID: ' + mainImageId : '❌ Missing'}`);
    if (!mainImageId && mainImageUrl) {
        const filename = extractFilename(mainImageUrl);
        console.log(`    URL: ${mainImageUrl}`);
        console.log(`    Filename: ${filename}`);
        missingImages.push({ blog: i, type: 'main', filename, url: mainImageUrl });
    }
    console.log();
}

console.log('\n=== Summary ===');
console.log(`Total missing images: ${missingImages.length}`);
console.log('\nMissing Images List:');
missingImages.forEach((img, idx) => {
    console.log(`${idx + 1}. Blog ${img.blog} - ${img.type}: ${img.filename}`);
});

// Save missing images report
fs.writeFileSync(
    '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/first_5_blogs/missing_images_report.json',
    JSON.stringify(missingImages, null, 2)
);

console.log('\n📄 Report saved to: missing_images_report.json');

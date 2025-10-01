const fs = require('fs');
const path = require('path');

const csvFilePath = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/Booked (Live) - Blogs (2).csv';
const allImagesJsonPath = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/all-images.json';

// Load all images data
const allImagesData = JSON.parse(fs.readFileSync(allImagesJsonPath, 'utf8'));

console.log('Total images in all-images.json:', allImagesData.length);

// Check what image names look like
console.log('\nSample image names:');
allImagesData.slice(0, 10).forEach(img => {
    console.log(`  ID: ${img.id}, Name: ${img.name}`);
});

// Function to parse CSV line handling quoted fields
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

// Read CSV
const csvContent = fs.readFileSync(csvFilePath, 'utf8');
const lines = csvContent.split('\n');
const headers = parseCSVLine(lines[0]);

const thumbnailIdx = headers.indexOf('Thumbnail Image');
const mainImageIdx = headers.indexOf('Main Image');
const blogDetailIdx = headers.indexOf('Blog Detail (OLD STUFF, DONT TOUCH)');

console.log('\n=== Checking Blog 2 (10 Best Vacation Spots) ===');
const line2 = lines[2];
const columns2 = parseCSVLine(line2);

const thumbnailUrl = columns2[thumbnailIdx];
const mainImageUrl = columns2[mainImageIdx];
const blogDetail = columns2[blogDetailIdx];

console.log('\nThumbnail URL:', thumbnailUrl);
console.log('Main Image URL:', mainImageUrl);

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

const thumbFilename = extractFilename(thumbnailUrl);
const mainFilename = extractFilename(mainImageUrl);

console.log('\nExtracted filenames:');
console.log('  Thumbnail:', thumbFilename);
console.log('  Main:', mainFilename);

// Check if these images exist in all-images.json
if (thumbFilename) {
    const thumbHash = thumbFilename.substring(0, 8);
    console.log('\nLooking for thumbnail with hash:', thumbHash);
    const matches = allImagesData.filter(img => img.name.includes(thumbHash));
    console.log('Matches found:', matches.length);
    if (matches.length > 0) {
        console.log('Sample matches:');
        matches.slice(0, 3).forEach(img => {
            console.log(`  ID: ${img.id}, Name: ${img.name}`);
        });
    } else {
        console.log('❌ No matches found! This image is not in the system.');
    }
}

// Check Blog_Detail content
console.log('\n=== Checking Blog_Detail Content ===');
console.log('Blog_Detail length:', blogDetail.length, 'characters');

// Count h2 tags
const h2Count = (blogDetail.match(/<h2[^>]*>/gi) || []).length;
console.log('Number of <h2> tags:', h2Count);

// Check if there's content before first h2
const firstH2Match = blogDetail.match(/<h2[^>]*>/i);
if (firstH2Match) {
    const introContent = blogDetail.substring(0, firstH2Match.index);
    const introText = introContent.replace(/<[^>]*>/g, '').trim();
    console.log('Intro content before first h2:', introText.length, 'chars');
    console.log('Intro preview:', introText.substring(0, 100) + '...');
} else {
    console.log('No h2 tags found in Blog_Detail');
}

// Extract all h2 titles
const h2Regex = /<h2[^>]*>(.*?)<\/h2>/gi;
const h2Titles = [];
let h2Match;
while ((h2Match = h2Regex.exec(blogDetail)) !== null) {
    const cleanTitle = h2Match[1].replace(/<[^>]*>/g, '').trim();
    h2Titles.push(cleanTitle);
}

console.log('\nExtracted h2 titles:');
h2Titles.forEach((title, i) => {
    console.log(`  ${i + 1}. ${title}`);
});

// Calculate total content length
const totalTextLength = blogDetail.replace(/<[^>]*>/g, '').trim().length;
console.log('\nTotal text content (no HTML):', totalTextLength, 'chars');

// Now check generated file to see what was captured
const generatedFilePath = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/first_5_blogs/blog_2_10-best-vacation-spots-for-couples-in-2024.json';
if (fs.existsSync(generatedFilePath)) {
    const generated = JSON.parse(fs.readFileSync(generatedFilePath, 'utf8'));
    
    console.log('\n=== Checking Generated File ===');
    console.log('Thumbnail_Image ID:', generated.data.Thumbnail_Image);
    console.log('Main_Image ID:', generated.data.Main_Image);
    console.log('Blog_Intro length:', generated.data.Blog_Intro.length);
    
    // Count non-null sections
    let sectionsWithContent = 0;
    let totalGeneratedText = generated.data.Blog_Intro.length;
    
    for (let i = 1; i <= 15; i++) {
        const section = generated.data[`Blog_Part_${i}`];
        if (section && section.length > 0) {
            sectionsWithContent++;
            // Calculate text length in this section
            section.forEach(block => {
                if (block.children) {
                    block.children.forEach(child => {
                        if (child.text) {
                            totalGeneratedText += child.text.length;
                        }
                    });
                }
            });
        }
    }
    
    console.log('Sections with content:', sectionsWithContent);
    console.log('Total text in generated file:', totalGeneratedText, 'chars');
    console.log('\n📊 Content Coverage:');
    const coverage = (totalGeneratedText / totalTextLength * 100).toFixed(2);
    console.log(`  Original: ${totalTextLength} chars`);
    console.log(`  Generated: ${totalGeneratedText} chars`);
    console.log(`  Coverage: ${coverage}%`);
    
    if (coverage < 95) {
        console.log('\n⚠️  WARNING: Some content may be missing!');
    } else {
        console.log('\n✅ Good coverage! All content appears to be included.');
    }
}

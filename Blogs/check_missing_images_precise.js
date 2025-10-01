const fs = require('fs');
const path = require('path');

const jsonFilePath = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/all-images.json';
const downloadedImagesDir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/downloaded_images';

function checkMissingImagesPrecise() {
    try {
        console.log('Reading all-images.json file...');
        const jsonData = fs.readFileSync(jsonFilePath, 'utf8');
        const allImages = JSON.parse(jsonData);
        
        console.log(`Found ${allImages.length} images in JSON file`);
        
        // Get all downloaded image filenames
        const downloadedFiles = fs.readdirSync(downloadedImagesDir);
        console.log(`Found ${downloadedFiles.length} downloaded images`);
        
        console.log('Checking for missing images with precise matching...');
        
        const missingImages = [];
        const foundImages = [];
        const usedJsonImages = new Set(); // Track which JSON images have been matched
        
        downloadedFiles.forEach(filename => {
            let found = false;
            let bestMatch = null;
            
            // Extract the 8-char hash from the downloaded filename
            const hashPart = filename.split('_')[0];
            
            // Look for exact matches first
            for (const image of allImages) {
                if (image.name.startsWith(hashPart) && !usedJsonImages.has(image.id)) {
                    // This is a potential match
                    if (!bestMatch) {
                        bestMatch = image;
                    }
                }
            }
            
            if (bestMatch) {
                foundImages.push({
                    downloaded: filename,
                    original: bestMatch.name,
                    id: bestMatch.id
                });
                usedJsonImages.add(bestMatch.id);
                found = true;
            }
            
            if (!found) {
                missingImages.push(filename);
            }
        });
        
        console.log('\n=== RESULTS ===');
        console.log(`Total downloaded images: ${downloadedFiles.length}`);
        console.log(`Found matches: ${foundImages.length}`);
        console.log(`Missing images: ${missingImages.length}`);
        console.log(`Unique JSON images used: ${usedJsonImages.size}`);
        
        if (missingImages.length > 0) {
            console.log('\n=== MISSING IMAGES ===');
            missingImages.forEach((filename, index) => {
                console.log(`${index + 1}. ${filename}`);
            });
        }
        
        // Check for duplicates in found images
        const duplicateCheck = {};
        foundImages.forEach(mapping => {
            if (duplicateCheck[mapping.original]) {
                duplicateCheck[mapping.original].push(mapping.downloaded);
            } else {
                duplicateCheck[mapping.original] = [mapping.downloaded];
            }
        });
        
        const duplicates = Object.entries(duplicateCheck).filter(([original, downloaded]) => downloaded.length > 1);
        
        if (duplicates.length > 0) {
            console.log('\n=== DUPLICATE MAPPINGS ===');
            duplicates.forEach(([original, downloaded]) => {
                console.log(`${original} -> ${downloaded.join(', ')}`);
            });
        }
        
        // Save results to files
        fs.writeFileSync('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/missing_images_precise.json', JSON.stringify(missingImages, null, 2));
        fs.writeFileSync('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/found_images_mapping_precise.json', JSON.stringify(foundImages, null, 2));
        
        console.log('\n=== FILES CREATED ===');
        console.log('missing_images_precise.json - List of missing image filenames');
        console.log('found_images_mapping_precise.json - Mapping of downloaded to original names');
        
        // Show some sample mappings
        console.log('\n=== SAMPLE MAPPINGS ===');
        foundImages.slice(0, 10).forEach(mapping => {
            console.log(`${mapping.downloaded} -> ${mapping.original} (ID: ${mapping.id})`);
        });
        
    } catch (error) {
        console.error('Error checking missing images:', error);
    }
}

checkMissingImagesPrecise();

const fs = require('fs');
const path = require('path');

const jsonFilePath = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/all-images.json';
const downloadedImagesDir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/downloaded_images';

function checkMissingImages() {
    try {
        console.log('Reading all-images.json file...');
        const jsonData = fs.readFileSync(jsonFilePath, 'utf8');
        const allImages = JSON.parse(jsonData);
        
        console.log(`Found ${allImages.length} images in JSON file`);
        
        // Get all downloaded image filenames
        const downloadedFiles = fs.readdirSync(downloadedImagesDir);
        console.log(`Found ${downloadedFiles.length} downloaded images`);
        
        // Create a set of all image names from JSON for faster lookup
        const jsonImageNames = new Set();
        allImages.forEach(image => {
            jsonImageNames.add(image.name);
        });
        
        console.log('Checking for missing images...');
        
        const missingImages = [];
        const foundImages = [];
        
        downloadedFiles.forEach(filename => {
            // Extract the original filename from the shortened name
            // The shortened format is: {8-char-hash}_{AD_12-char-part}.{extension}
            // We need to find the corresponding original name in the JSON
            
            let found = false;
            
            // Try to find a match by looking for images that contain the 8-char hash
            const hashPart = filename.split('_')[0]; // Get the 8-char hash part
            
            for (const image of allImages) {
                if (image.name.startsWith(hashPart)) {
                    foundImages.push({
                        downloaded: filename,
                        original: image.name,
                        id: image.id
                    });
                    found = true;
                    break;
                }
            }
            
            if (!found) {
                missingImages.push(filename);
            }
        });
        
        console.log('\n=== RESULTS ===');
        console.log(`Total downloaded images: ${downloadedFiles.length}`);
        console.log(`Found matches: ${foundImages.length}`);
        console.log(`Missing images: ${missingImages.length}`);
        
        if (missingImages.length > 0) {
            console.log('\n=== MISSING IMAGES ===');
            missingImages.forEach((filename, index) => {
                console.log(`${index + 1}. ${filename}`);
            });
        }
        
        // Save results to files
        fs.writeFileSync('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/missing_images.json', JSON.stringify(missingImages, null, 2));
        fs.writeFileSync('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/found_images_mapping.json', JSON.stringify(foundImages, null, 2));
        
        console.log('\n=== FILES CREATED ===');
        console.log('missing_images.json - List of missing image filenames');
        console.log('found_images_mapping.json - Mapping of downloaded to original names');
        
        // Show some sample mappings
        console.log('\n=== SAMPLE MAPPINGS ===');
        foundImages.slice(0, 5).forEach(mapping => {
            console.log(`${mapping.downloaded} -> ${mapping.original} (ID: ${mapping.id})`);
        });
        
    } catch (error) {
        console.error('Error checking missing images:', error);
    }
}

checkMissingImages();

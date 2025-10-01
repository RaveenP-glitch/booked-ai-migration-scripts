const fs = require('fs');
const path = require('path');

const sourceDir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/downloaded_images';
const mappingFile = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/image_name_mapping.json';

function revertImageNames() {
    try {
        // Read the mapping file
        const mappingData = fs.readFileSync(mappingFile, 'utf8');
        const mappings = JSON.parse(mappingData);
        
        console.log(`Found ${mappings.length} mappings to revert`);
        
        let revertedCount = 0;
        let errorCount = 0;
        
        // Process each mapping in reverse order to avoid conflicts
        for (let i = mappings.length - 1; i >= 0; i--) {
            const mapping = mappings[i];
            const oldName = mapping.old;
            const newName = mapping.new;
            
            const oldPath = path.join(sourceDir, oldName);
            const newPath = path.join(sourceDir, newName);
            
            try {
                // Check if the new (shortened) file exists
                if (fs.existsSync(newPath)) {
                    // Rename back to original name
                    fs.renameSync(newPath, oldPath);
                    revertedCount++;
                    console.log(`${revertedCount}. ${newName} -> ${oldName}`);
                } else {
                    console.log(`Warning: File not found: ${newName}`);
                    errorCount++;
                }
            } catch (error) {
                console.error(`Error reverting ${newName}: ${error.message}`);
                errorCount++;
            }
        }
        
        console.log(`\nReverting completed:`);
        console.log(`- Successfully reverted: ${revertedCount} files`);
        console.log(`- Errors: ${errorCount} files`);
        
        // Remove the mapping file after successful reversion
        if (revertedCount > 0) {
            fs.unlinkSync(mappingFile);
            console.log(`\nMapping file removed: ${mappingFile}`);
        }
        
    } catch (error) {
        console.error('Error reverting image names:', error);
    }
}

revertImageNames();

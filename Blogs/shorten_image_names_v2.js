const fs = require('fs');
const path = require('path');

const sourceDir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/downloaded_images';

function shortenImageNamesV2() {
    try {
        // Read all files in the directory
        const files = fs.readdirSync(sourceDir);
        
        console.log(`Found ${files.length} files to rename`);
        
        let renamedCount = 0;
        let errorCount = 0;
        
        files.forEach((filename, index) => {
            const oldPath = path.join(sourceDir, filename);
            const fileStats = fs.statSync(oldPath);
            
            // Skip if it's not a file
            if (!fileStats.isFile()) {
                return;
            }
            
            // Extract file extension
            const ext = path.extname(filename);
            
            // Remove the initial hash part (24 characters) and leading underscores
            // Pattern: {24-char-hash}_AD_... -> AD_...
            let newName = filename;
            
            // Check if filename starts with a 24-character hash followed by underscore
            const hashPattern = /^[0-9a-f]{24}_/;
            if (hashPattern.test(filename)) {
                // Remove the first 25 characters (24-char hash + underscore)
                newName = filename.substring(25);
            }
            
            // If the new name is different, rename the file
            if (newName !== filename) {
                const newPath = path.join(sourceDir, newName);
                
                try {
                    fs.renameSync(oldPath, newPath);
                    renamedCount++;
                    console.log(`${renamedCount}. ${filename} -> ${newName}`);
                } catch (error) {
                    console.error(`Error renaming ${filename}: ${error.message}`);
                    errorCount++;
                }
            }
        });
        
        console.log(`\nShortening completed:`);
        console.log(`- Successfully renamed: ${renamedCount} files`);
        console.log(`- Errors: ${errorCount} files`);
        
    } catch (error) {
        console.error('Error shortening image names:', error);
    }
}

shortenImageNamesV2();

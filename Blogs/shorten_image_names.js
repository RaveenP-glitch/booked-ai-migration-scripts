const fs = require('fs');
const path = require('path');

const sourceDir = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Blogs/all-assets/downloaded_images';

function shortenImageNames() {
    try {
        // Read all files in the directory
        const files = fs.readdirSync(sourceDir);
        
        console.log(`Found ${files.length} files to rename`);
        
        const renamedFiles = [];
        
        files.forEach((filename, index) => {
            const oldPath = path.join(sourceDir, filename);
            const fileStats = fs.statSync(oldPath);
            
            // Skip if it's not a file
            if (!fileStats.isFile()) {
                return;
            }
            
            // Extract file extension
            const ext = path.extname(filename);
            
            // Create a shorter unique name
            // Use first 8 chars of hash + last 12 chars of the AD part + extension
            const parts = filename.split('_');
            if (parts.length >= 2) {
                const hashPart = parts[0].substring(0, 8);
                const adPart = parts[1].substring(0, 12);
                const newName = `${hashPart}_${adPart}${ext}`;
                
                const newPath = path.join(sourceDir, newName);
                
                // Check if new name already exists
                if (fs.existsSync(newPath)) {
                    // Add index to make it unique
                    const nameWithoutExt = newName.replace(ext, '');
                    const uniqueName = `${nameWithoutExt}_${index}${ext}`;
                    const uniquePath = path.join(sourceDir, uniqueName);
                    
                    fs.renameSync(oldPath, uniquePath);
                    renamedFiles.push({ old: filename, new: uniqueName });
                    console.log(`${index + 1}. ${filename} -> ${uniqueName}`);
                } else {
                    fs.renameSync(oldPath, newPath);
                    renamedFiles.push({ old: filename, new: newName });
                    console.log(`${index + 1}. ${filename} -> ${newName}`);
                }
            } else {
                console.log(`Skipping file with unexpected format: ${filename}`);
            }
        });
        
        console.log(`\nSuccessfully renamed ${renamedFiles.length} files`);
        
        // Save the mapping for reference
        const mappingFile = path.join(sourceDir, '..', 'image_name_mapping.json');
        fs.writeFileSync(mappingFile, JSON.stringify(renamedFiles, null, 2));
        console.log(`\nName mapping saved to: ${mappingFile}`);
        
    } catch (error) {
        console.error('Error shortening image names:', error);
    }
}

shortenImageNames();

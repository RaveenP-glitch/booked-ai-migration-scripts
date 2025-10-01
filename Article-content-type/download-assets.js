const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

// Read the asset URLs from the file
const assetUrlsFile = path.join(__dirname, 'assets', 'AssetURLs.txt');
const downloadsDir = path.join(__dirname, 'downloads');

// Ensure downloads directory exists
if (!fs.existsSync(downloadsDir)) {
    fs.mkdirSync(downloadsDir, { recursive: true });
}

// Read URLs from file
const assetUrls = fs.readFileSync(assetUrlsFile, 'utf8')
    .split('\n')
    .map(url => url.trim())
    .filter(url => url.length > 0);

console.log(`Found ${assetUrls.length} asset URLs to download`);

// Function to extract filename from URL
function getFilenameFromUrl(url) {
    try {
        const urlObj = new URL(url);
        const pathname = urlObj.pathname;
        const filename = path.basename(pathname);
        
        // Decode URL-encoded characters
        return decodeURIComponent(filename);
    } catch (error) {
        console.error(`Error parsing URL: ${url}`, error.message);
        return null;
    }
}

// Function to download a single asset
async function downloadAsset(url, index, total) {
    try {
        const filename = getFilenameFromUrl(url);
        if (!filename) {
            console.log(`[${index + 1}/${total}] Skipping invalid URL: ${url}`);
            return;
        }

        const filePath = path.join(downloadsDir, filename);
        
        // Skip if file already exists
        if (fs.existsSync(filePath)) {
            console.log(`[${index + 1}/${total}] File already exists, skipping: ${filename}`);
            return;
        }

        console.log(`[${index + 1}/${total}] Downloading: ${filename}`);
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const buffer = await response.buffer();
        fs.writeFileSync(filePath, buffer);
        
        console.log(`[${index + 1}/${total}] ✓ Downloaded: ${filename} (${buffer.length} bytes)`);
        
    } catch (error) {
        console.error(`[${index + 1}/${total}] ✗ Failed to download ${url}:`, error.message);
    }
}

// Function to download all assets with concurrency control
async function downloadAllAssets() {
    const concurrency = 5; // Download 5 files at a time
    const total = assetUrls.length;
    
    console.log(`Starting download of ${total} assets with concurrency of ${concurrency}...`);
    console.log(`Downloading to: ${downloadsDir}`);
    console.log('---');
    
    for (let i = 0; i < assetUrls.length; i += concurrency) {
        const batch = assetUrls.slice(i, i + concurrency);
        const promises = batch.map((url, batchIndex) => 
            downloadAsset(url, i + batchIndex, total)
        );
        
        await Promise.all(promises);
        
        // Small delay between batches to be respectful to the server
        if (i + concurrency < assetUrls.length) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }
    
    console.log('---');
    console.log('Download completed!');
    
    // Show summary
    const downloadedFiles = fs.readdirSync(downloadsDir);
    console.log(`Files in downloads directory: ${downloadedFiles.length}`);
}

// Run the download process
downloadAllAssets().catch(error => {
    console.error('Download process failed:', error);
    process.exit(1);
});



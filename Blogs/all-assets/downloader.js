const fs = require('fs');
const https = require('https');
const http = require('http');
const path = require('path');

// Read the URLs from the text file
const urls = fs.readFileSync('all_blog_image_urls.txt', 'utf8').split('\n').filter(Boolean);

const downloadDir = 'downloaded_images';
if (!fs.existsSync(downloadDir)){
    fs.mkdirSync(downloadDir);
}

function download(url, dest, cb) {
    const mod = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(dest);
    mod.get(url, (res) => {
        if (res.statusCode === 200) {
            res.pipe(file);
            file.on('finish', () => file.close(cb));
        } else {
            fs.unlink(dest, () => {});
            cb(new Error(`Failed to get '${url}' (${res.statusCode})`));
        }
    }).on('error', (err) => {
        fs.unlink(dest, () => {});
        cb(err);
    });
}

let idx = 0;
function next() {
    if (idx >= urls.length) {
        console.log('All downloads completed!');
        return;
    }
    const url = urls[idx];
    const filename = path.basename(url.split('?')[0]);
    
    download(url, path.join(downloadDir, filename), (err) => {
        if (err) console.error(`Error downloading ${url}: ${err.message}`);
        else console.log(`Downloaded ${filename}`);
        idx += 1;
        setTimeout(next, 250); // Small delay between downloads
    });
}
next();
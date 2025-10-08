const fs = require('fs');
const path = require('path');

// Read the image mapping file
const imageMapping = JSON.parse(fs.readFileSync('collection/all-images-id-name.json', 'utf8'));

// Function to extract image ID from URL
function getImageIdFromUrl(imageUrl) {
    if (!imageUrl) return null;
    
    // Extract the filename from the URL
    const filename = imageUrl.split('/').pop();
    
    // Find matching image in the mapping
    const image = imageMapping.find(img => img.name === filename);
    return image ? image.id : null;
}

// Function to generate slug from name
function generateSlug(name) {
    return name.toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim();
}

// Improved HTML to blocks converter
function convertHtmlToBlocks(htmlContent) {
    if (!htmlContent) return [];
    
    const blocks = [];
    
    // Remove any leading/trailing whitespace
    htmlContent = htmlContent.trim();
    
    // If content doesn't contain HTML tags, treat as plain text
    if (!htmlContent.includes('<')) {
        if (htmlContent) {
            blocks.push({
                type: "paragraph",
                children: [{
                    type: "text",
                    text: htmlContent
                }]
            });
        }
        return blocks;
    }
    
    // Split content by HTML tags while preserving the tags
    const parts = htmlContent.split(/(<[^>]+>)/);
    
    let currentBlock = null;
    let currentText = '';
    
    for (let i = 0; i < parts.length; i++) {
        const part = parts[i];
        
        if (part.startsWith('<')) {
            // This is an HTML tag
            const tagMatch = part.match(/<(\/?)([a-zA-Z0-9]+)([^>]*)>/);
            if (tagMatch) {
                const isClosing = tagMatch[1] === '/';
                const tagName = tagMatch[2].toLowerCase();
                
                if (isClosing) {
                    // Closing tag - finalize current block
                    if (currentBlock && currentText.trim()) {
                        currentBlock.children = [{
                            type: "text",
                            text: currentText.trim()
                        }];
                        blocks.push(currentBlock);
                    }
                    currentBlock = null;
                    currentText = '';
                } else {
                    // Opening tag - start new block
                    if (currentBlock && currentText.trim()) {
                        currentBlock.children = [{
                            type: "text",
                            text: currentText.trim()
                        }];
                        blocks.push(currentBlock);
                    }
                    
                    switch (tagName) {
                        case 'h1':
                            currentBlock = { type: "heading", level: 1, children: [] };
                            break;
                        case 'h2':
                            currentBlock = { type: "heading", level: 2, children: [] };
                            break;
                        case 'h3':
                            currentBlock = { type: "heading", level: 3, children: [] };
                            break;
                        case 'h4':
                            currentBlock = { type: "heading", level: 4, children: [] };
                            break;
                        case 'h5':
                            currentBlock = { type: "heading", level: 5, children: [] };
                            break;
                        case 'h6':
                            currentBlock = { type: "heading", level: 6, children: [] };
                            break;
                        case 'p':
                            currentBlock = { type: "paragraph", children: [] };
                            break;
                        case 'blockquote':
                            currentBlock = { type: "quote", children: [] };
                            break;
                        case 'ul':
                        case 'ol':
                            currentBlock = { type: "list", format: tagName === 'ul' ? 'unordered' : 'ordered', children: [] };
                            break;
                        case 'li':
                            currentBlock = { type: "list-item", children: [] };
                            break;
                        default:
                            currentBlock = { type: "paragraph", children: [] };
                            break;
                    }
                    currentText = '';
                }
            }
        } else {
            // This is text content
            currentText += part;
        }
    }
    
    // Handle any remaining content
    if (currentBlock && currentText.trim()) {
        currentBlock.children = [{
            type: "text",
            text: currentText.trim()
        }];
        blocks.push(currentBlock);
    } else if (!currentBlock && currentText.trim()) {
        // No block was created, treat as paragraph
        blocks.push({
            type: "paragraph",
            children: [{
                type: "text",
                text: currentText.trim()
            }]
        });
    }
    
    return blocks.length > 0 ? blocks : [];
}

// Function to parse CSV and extract valid entries
function parseCSVEntries() {
    const csvContent = fs.readFileSync('Booked (Live) - City Blogs all.csv', 'utf8');
    const lines = csvContent.split('\n');
    const headers = lines[0].split(',');
    
    const entries = [];
    
    for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;
        
        // Skip lines that don't look like proper CSV entries
        if (line.startsWith('<') || line.includes('</ul>') || line.includes('<li>')) {
            continue;
        }
        
        const values = line.split(',');
        if (values.length < 10) continue;
        
        const entry = {};
        headers.forEach((header, index) => {
            entry[header] = values[index] || '';
        });
        
        // Only include entries with proper names
        if (entry.Name && entry.Name.trim() && !entry.Name.startsWith('<')) {
            entries.push(entry);
        }
    }
    
    return entries;
}

// Function to create request body for a single entry
function createRequestBody(entry, index) {
    const thumbnailImageId = getImageIdFromUrl(entry['Thumbnail Image']);
    const mainImageId = getImageIdFromUrl(entry['Main Image']);
    
    // Generate slug if not available
    const slug = entry.Slug || generateSlug(entry.Name);
    
    return {
        name: `${index + 1}. ${entry.Name}`,
        request: {
            method: "POST",
            header: [
                {
                    key: "Content-Type",
                    value: "application/json",
                    type: "text"
                },
                {
                    key: "Authorization",
                    value: "Bearer {{apiToken}}",
                    type: "text"
                }
            ],
            body: {
                mode: "raw",
                raw: JSON.stringify({
                    data: {
                        Name: entry.Name,
                        Slug: slug,
                        publishedAt: entry['Published On'] || new Date().toISOString(),
                        Short_Description: entry['short description'] || '',
                        Thumbnail_Image: thumbnailImageId,
                        Main_Image: mainImageId,
                        Blog_Title: entry['Blog Title'] || entry.Name,
                        Blog_Intro: entry['Blog Intro'] || '',
                        Blog_Part_1_Image: getImageIdFromUrl(entry['Blog Part 1 Image']),
                        Blog_Part_1: convertHtmlToBlocks(entry['Blog part 1']),
                        Blog_Part_2_Image: getImageIdFromUrl(entry['Blog Part 2 Image']),
                        Blog_Part_2: convertHtmlToBlocks(entry['Blog part 2']),
                        Blog_Part_3_Image: getImageIdFromUrl(entry['Blog Part 3 Image']),
                        Blog_Part_3: convertHtmlToBlocks(entry['Blog part 3']),
                        Blog_Part_4_Image: getImageIdFromUrl(entry['Blog Part 4 Image']),
                        Blog_Part_4: convertHtmlToBlocks(entry['Blog part 4']),
                        Blog_Part_5_Image: getImageIdFromUrl(entry['Blog Part 5 Image']),
                        Blog_Part_5: convertHtmlToBlocks(entry['Blog part 5']),
                        Blog_Part_6_Image: getImageIdFromUrl(entry['Blog Part 6 Image']),
                        Blog_Part_6: convertHtmlToBlocks(entry['Blog part 6']),
                        FAQ_Title: entry['FAQ Title'] || 'Frequently Asked Questions',
                        FAQ1: entry['FAQ 1'] || '',
                        FAQ2: entry['FAQ 2'] || '',
                        FAQ3: entry['FAQ 3'] || '',
                        FAQ4: entry['FAQ 4'] || '',
                        FAQ5: entry['FAQ 5'] || '',
                        FAQ6: entry['FAQ 6'] || '',
                        FAQ_1_Detail: convertHtmlToBlocks(entry['FAQ 1 Detail']),
                        FAQ_2_Detail: convertHtmlToBlocks(entry['FAQ 2 Detail']),
                        FAQ_3_Detail: convertHtmlToBlocks(entry['FAQ 3 Detail']),
                        FAQ_4_Detail: convertHtmlToBlocks(entry['FAQ 4 Detail']),
                        FAQ_5_Detail: convertHtmlToBlocks(entry['FAQ 5 Detail']),
                        FAQ_6_Detail: convertHtmlToBlocks(entry['FAQ 6 Detail']),
                        Sitemap_Indexing: true
                    }
                }, null, 2)
            },
            url: {
                raw: "{{baseUrl}}/api/city-blogs",
                host: ["{{baseUrl}}"],
                path: ["api", "city-blogs"]
            },
            description: `Create city blog: ${entry.Name}`
        },
        response: []
    };
}

// Main function to generate the full collection
function generateFullCollection() {
    console.log('Parsing CSV entries...');
    const entries = parseCSVEntries();
    console.log(`Found ${entries.length} valid entries`);
    
    console.log('Generating request bodies...');
    const requestBodies = entries.map((entry, index) => {
        if (index % 100 === 0) {
            console.log(`Processed ${index} entries...`);
        }
        return createRequestBody(entry, index);
    });
    
    // Create the Postman collection structure
    const postmanCollection = {
        info: {
            name: "Strapi City Blogs Complete Collection",
            description: `Complete collection for uploading all ${entries.length} City Blog entries to Strapi`,
            schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        item: requestBodies
    };
    
    // Write the collection to a file
    const filename = 'Strapi_City_Blogs_Complete_Collection.postman_collection.json';
    fs.writeFileSync(filename, JSON.stringify(postmanCollection, null, 2));
    
    console.log(`\nComplete Postman collection generated successfully!`);
    console.log(`File: ${filename}`);
    console.log(`Generated ${requestBodies.length} request bodies`);
    
    // Generate summary statistics
    const withImages = requestBodies.filter(item => {
        const data = JSON.parse(item.request.body.raw);
        return data.data.Thumbnail_Image || data.data.Main_Image;
    }).length;
    
    console.log(`\nSummary:`);
    console.log(`- Total entries: ${entries.length}`);
    console.log(`- Entries with images: ${withImages}`);
    console.log(`- Entries without images: ${entries.length - withImages}`);
    
    return filename;
}

// Run the generator
if (require.main === module) {
    try {
        generateFullCollection();
    } catch (error) {
        console.error('Error generating collection:', error);
        process.exit(1);
    }
}

module.exports = { generateFullCollection, parseCSVEntries, createRequestBody };

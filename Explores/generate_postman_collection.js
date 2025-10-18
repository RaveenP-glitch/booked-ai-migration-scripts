const fs = require('fs');
const path = require('path');

/**
 * Explores Content to Strapi Postman Collection Generator
 * This script converts CSV data to Postman collection format for Strapi upload
 */

class ExploresCollectionGenerator {
    constructor() {
        this.csvPath = path.join(__dirname, 'Booked (Live) - Explores-all.csv');
        this.schemaPath = path.join(__dirname, 'collection', 'schema.json');
        // Try local media mapping first, then Graphql-asset-manager, fallback to Hotels folder
        const localMediaPath = path.join(__dirname, 'media-ids-and-names.json');
        const graphqlMediaPath = path.join(__dirname, '..', 'Graphql-asset-manager', 'media-ids-and-names.json');
        const hotelsMediaPath = path.join(__dirname, '..', 'Hotels', 'collection', 'media-ids-and-names.json');
        
        if (fs.existsSync(localMediaPath)) {
            this.mediaMapPath = localMediaPath;
        } else if (fs.existsSync(graphqlMediaPath)) {
            this.mediaMapPath = graphqlMediaPath;
        } else {
            this.mediaMapPath = hotelsMediaPath;
        }
        
        this.cityBlogsPath = path.join(__dirname, '..', 'City-Blogs-manager', 'all-city-blogs.json');
        
        this.schema = null;
        this.mediaMap = new Map();
        this.cityBlogsMap = new Map();
        this.csvData = [];
    }

    /**
     * Load all required data files
     */
    loadData() {
        console.log('Loading schema...');
        this.schema = JSON.parse(fs.readFileSync(this.schemaPath, 'utf8'));
        
        console.log('Loading media mapping...');
        console.log(`   Using: ${this.mediaMapPath}`);
        const mediaArray = JSON.parse(fs.readFileSync(this.mediaMapPath, 'utf8'));
        mediaArray.forEach(item => {
            // Store full name
            this.mediaMap.set(item.name, item.id);
            
            // Also store without extension
            const nameWithoutExt = item.name.replace(/\.[^/.]+$/, '');
            this.mediaMap.set(nameWithoutExt, item.id);
            
            // Store by the ID part (first part before underscore)
            const idPart = item.name.split('_')[0];
            if (idPart && idPart.length > 10) {
                this.mediaMap.set(idPart, item.id);
            }
        });
        
        console.log('Loading city blogs mapping...');
        const cityBlogsArray = JSON.parse(fs.readFileSync(this.cityBlogsPath, 'utf8'));
        cityBlogsArray.forEach(blog => {
            this.cityBlogsMap.set(blog.Slug, blog.documentId);
        });
        
        console.log('Loading CSV data...');
        this.csvData = this.parseCSV();
        
        console.log(`Loaded ${this.csvData.length} entries from CSV`);
        console.log(`Media map has ${this.mediaMap.size} entries`);
        console.log(`City blogs map has ${this.cityBlogsMap.size} entries`);
    }

    /**
     * Parse CSV file with proper handling of quoted fields
     */
    parseCSV() {
        const csvContent = fs.readFileSync(this.csvPath, 'utf8');
        const lines = csvContent.split('\n');
        const headers = this.parseCSVLine(lines[0]);
        
        const data = [];
        for (let i = 1; i < lines.length; i++) {
            if (lines[i].trim()) {
                const values = this.parseCSVLine(lines[i]);
                const row = {};
                headers.forEach((header, index) => {
                    row[header.trim()] = values[index] ? values[index].trim() : '';
                });
                data.push(row);
            }
        }
        return data;
    }

    /**
     * Parse a single CSV line with proper quote handling
     */
    parseCSVLine(line) {
        const result = [];
        let current = '';
        let inQuotes = false;
        
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            
            if (char === '"') {
                inQuotes = !inQuotes;
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

    /**
     * Extract filename from URL
     */
    getFilenameFromURL(url) {
        if (!url) return null;
        try {
            const urlParts = url.split('/');
            return urlParts[urlParts.length - 1];
        } catch (error) {
            return null;
        }
    }

    /**
     * Get media ID from URL
     */
    getMediaIdFromURL(url) {
        if (!url) return null;
        
        const filename = this.getFilenameFromURL(url);
        if (!filename) return null;
        
        // Try exact match first
        if (this.mediaMap.has(filename)) {
            return this.mediaMap.get(filename);
        }
        
        // Try without extension
        const nameWithoutExt = filename.replace(/\.[^/.]+$/, '');
        if (this.mediaMap.has(nameWithoutExt)) {
            return this.mediaMap.get(nameWithoutExt);
        }
        
        // Try matching by the ID part (first part before underscore)
        const idPart = filename.split('_')[0];
        if (idPart && this.mediaMap.has(idPart)) {
            return this.mediaMap.get(idPart);
        }
        
        // Try partial match (case insensitive)
        const lowerFilename = nameWithoutExt.toLowerCase();
        for (const [key, value] of this.mediaMap.entries()) {
            const lowerKey = key.toLowerCase();
            if (lowerKey.includes(lowerFilename) || lowerFilename.includes(lowerKey)) {
                return value;
            }
        }
        
        console.warn(`⚠️  No media ID found for: ${filename}`);
        return null;
    }

    /**
     * Parse relationship string (semicolon-separated slugs)
     */
    parseRelationshipField(fieldValue) {
        if (!fieldValue || fieldValue.trim() === '') {
            return [];
        }
        return fieldValue.split(';').map(slug => slug.trim()).filter(slug => slug !== '');
    }

    /**
     * Map City Blogs slugs to document IDs
     */
    mapCityBlogs(slugs) {
        const documentIds = [];
        slugs.forEach(slug => {
            const documentId = this.cityBlogsMap.get(slug);
            if (documentId) {
                documentIds.push(documentId);
            } else {
                console.warn(`⚠️  No City Blog found for slug: ${slug}`);
            }
        });
        return documentIds;
    }

    /**
     * Convert CSV row to Strapi request body
     */
    convertToStrapiFormat(row) {
        const data = {};
        
        // String fields
        data.Title = row.Title || '';
        data.Slug = row.Slug || '';
        data.Overview = row.Overview || '';
        data.Location = row.Location || '';
        data.Style = row.Style || '';
        data.Duration = row.Duration || '';
        data.Author = row.Author || '';
        data.Min_Read = row['Min read'] || '';
        data.Cost = row.Cost || '';
        data.City_Name = row['City Name'] || '';
        data.Main_Title = row['Main Title'] || '';
        
        // Integer field
        const numberOfSpots = row['# of spots'];
        if (numberOfSpots && numberOfSpots.trim() !== '') {
            // Extract number from strings like "Top 2 AI Travel Recommendations"
            const match = numberOfSpots.match(/\d+/);
            data.Number_of_Spots = match ? parseInt(match[0]) : 0;
        } else {
            data.Number_of_Spots = 0;
        }
        
        // Boolean field (default to true per schema)
        data.Sitemap_Indexing = true;
        
        // Media fields
        const imageUrl = row.Image;
        if (imageUrl) {
            const imageId = this.getMediaIdFromURL(imageUrl);
            if (imageId) {
                data.Image = imageId;
            }
        }
        
        const authorPicUrl = row['Author Pic'];
        if (authorPicUrl) {
            const authorPicId = this.getMediaIdFromURL(authorPicUrl);
            if (authorPicId) {
                data.Author_Pic = authorPicId;
            }
        }
        
        // Relationship fields
        // For oneToMany relationships, use empty arrays instead of null
        // For unmapped fields, we'll omit them entirely from the request
        
        // Map City_blogs (oneToOne relationship)
        const cityBlogSlugs = this.parseRelationshipField(row['City Blogs']);
        if (cityBlogSlugs.length > 0) {
            const mappedIds = this.mapCityBlogs(cityBlogSlugs);
            if (mappedIds.length > 0) {
                // For oneToOne relationship, use the first match
                data.City_blogs = mappedIds[0];
            }
        }
        
        // Note: Hotels, Restaurants, Attractions, and Itineraries are not included
        // in the request body until they are properly mapped. Including them as null
        // or empty arrays can cause validation errors in Strapi.
        
        return { data };
    }

    /**
     * Generate Postman collection structure
     */
    generatePostmanCollection(entries, collectionName) {
        const collection = {
            info: {
                name: collectionName,
                description: `Postman collection for uploading ${entries.length} Explores entries to Strapi`,
                schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            item: [],
            variable: [
                {
                    key: "baseUrl",
                    value: "http://localhost:1337",
                    type: "string"
                },
                {
                    key: "apiToken",
                    value: "YOUR_API_TOKEN_HERE",
                    type: "string"
                }
            ]
        };

        entries.forEach((entry, index) => {
            const requestBody = this.convertToStrapiFormat(entry);
            
            const request = {
                name: `${index + 1}. ${entry.Title || 'Untitled'}`,
                request: {
                    method: "POST",
                    header: [
                        {
                            key: "Content-Type",
                            value: "application/json"
                        },
                        {
                            key: "Authorization",
                            value: "Bearer {{apiToken}}"
                        }
                    ],
                    body: {
                        mode: "raw",
                        raw: JSON.stringify(requestBody, null, 2)
                    },
                    url: {
                        raw: "{{baseUrl}}/api/explores",
                        host: ["{{baseUrl}}"],
                        path: ["api", "explores"]
                    }
                },
                response: []
            };
            
            collection.item.push(request);
        });

        return collection;
    }

    /**
     * Generate test collection with first 5 entries
     */
    generateTestCollection() {
        console.log('\n📝 Generating test collection with 5 entries...');
        const testEntries = this.csvData.slice(0, 5);
        const collection = this.generatePostmanCollection(testEntries, 'Strapi_Explores_Test_5_Collection');
        
        const outputPath = path.join(__dirname, 'collection', 'Strapi_Explores_Test_5_Collection.postman_collection.json');
        fs.writeFileSync(outputPath, JSON.stringify(collection, null, 2));
        
        console.log(`✅ Test collection saved to: ${outputPath}`);
        console.log(`   Contains ${testEntries.length} entries`);
        
        return testEntries;
    }

    /**
     * Generate full collection with all entries
     */
    generateFullCollection() {
        console.log('\n📝 Generating full collection with all entries...');
        const collection = this.generatePostmanCollection(this.csvData, 'Strapi_Explores_Complete_Collection');
        
        const outputPath = path.join(__dirname, 'collection', 'Strapi_Explores_Complete_Collection.postman_collection.json');
        fs.writeFileSync(outputPath, JSON.stringify(collection, null, 2));
        
        console.log(`✅ Full collection saved to: ${outputPath}`);
        console.log(`   Contains ${this.csvData.length} entries`);
    }

    /**
     * Generate summary report
     */
    generateReport(testEntries) {
        console.log('\n' + '='.repeat(60));
        console.log('GENERATION SUMMARY');
        console.log('='.repeat(60));
        
        console.log('\n📊 Test Collection Sample (First 5 entries):');
        testEntries.forEach((entry, index) => {
            console.log(`   ${index + 1}. ${entry.Title}`);
            console.log(`      Location: ${entry.Location}`);
            console.log(`      Style: ${entry.Style}`);
            console.log(`      Duration: ${entry.Duration}`);
            console.log(`      Author: ${entry.Author}`);
            console.log('');
        });
        
        console.log('📈 Statistics:');
        console.log(`   Total entries in CSV: ${this.csvData.length}`);
        console.log(`   Media mappings available: ${this.mediaMap.size}`);
        console.log(`   City Blogs mappings available: ${this.cityBlogsMap.size}`);
        
        // Count successful mappings
        let imagesFound = 0;
        let authorPicsFound = 0;
        let cityBlogsFound = 0;
        
        this.csvData.forEach(row => {
            if (row.Image) {
                const imageId = this.getMediaIdFromURL(row.Image);
                if (imageId) imagesFound++;
            }
            
            if (row['Author Pic']) {
                const authorPicId = this.getMediaIdFromURL(row['Author Pic']);
                if (authorPicId) authorPicsFound++;
            }
            
            const cityBlogSlugs = this.parseRelationshipField(row['City Blogs']);
            if (cityBlogSlugs.length > 0) {
                const mappedIds = this.mapCityBlogs(cityBlogSlugs);
                if (mappedIds.length > 0) cityBlogsFound++;
            }
        });
        
        console.log(`\n✅ Mapping Success Rates:`);
        console.log(`   Images: ${imagesFound}/${this.csvData.length} (${(imagesFound/this.csvData.length*100).toFixed(1)}%)`);
        console.log(`   Author Pics: ${authorPicsFound}/${this.csvData.length} (${(authorPicsFound/this.csvData.length*100).toFixed(1)}%)`);
        console.log(`   City Blogs: ${cityBlogsFound}/${this.csvData.length} (${(cityBlogsFound/this.csvData.length*100).toFixed(1)}%)`);
        
        console.log('\n' + '='.repeat(60));
    }

    /**
     * Main execution method
     */
    run() {
        try {
            console.log('🚀 Starting Explores Postman Collection Generator...\n');
            
            this.loadData();
            const testEntries = this.generateTestCollection();
            this.generateFullCollection();
            this.generateReport(testEntries);
            
            console.log('\n✅ Generation complete!');
            console.log('\n📝 Next steps:');
            console.log('   1. Import the test collection into Postman');
            console.log('   2. Set the apiToken variable with your Strapi API token');
            console.log('   3. Test with the 5-entry collection first');
            console.log('   4. Once verified, use the complete collection');
            
        } catch (error) {
            console.error('❌ Error:', error);
            throw error;
        }
    }
}

// Run the generator
if (require.main === module) {
    const generator = new ExploresCollectionGenerator();
    generator.run();
}

module.exports = ExploresCollectionGenerator;


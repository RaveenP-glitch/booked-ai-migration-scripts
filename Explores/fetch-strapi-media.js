const fs = require('fs');
const path = require('path');

/**
 * Fetch all media from Strapi and create a mapping file
 * This script fetches media items from Strapi and creates a media-ids-and-names.json file
 */

class StrapiMediaFetcher {
    constructor(baseUrl, apiToken) {
        this.baseUrl = baseUrl || 'http://localhost:1337';
        this.apiToken = apiToken;
        this.allMedia = [];
    }

    /**
     * Fetch all media from Strapi with pagination
     */
    async fetchAllMedia() {
        let page = 1;
        const pageSize = 100;
        let hasMore = true;

        console.log('🔍 Fetching media from Strapi...');

        while (hasMore) {
            try {
                const url = `${this.baseUrl}/api/upload/files?pagination[page]=${page}&pagination[pageSize]=${pageSize}`;
                
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${this.apiToken}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                if (data && Array.isArray(data)) {
                    // Direct array response
                    this.allMedia.push(...data);
                    hasMore = data.length === pageSize;
                } else if (data && data.data) {
                    // Wrapped in data property
                    this.allMedia.push(...data.data);
                    hasMore = data.data.length === pageSize;
                } else {
                    hasMore = false;
                }

                console.log(`   Page ${page}: ${this.allMedia.length} media items fetched so far...`);
                page++;

            } catch (error) {
                console.error(`Error fetching page ${page}:`, error.message);
                hasMore = false;
            }
        }

        console.log(`✅ Total media items fetched: ${this.allMedia.length}`);
        return this.allMedia;
    }

    /**
     * Create mapping file with media IDs and names
     */
    createMappingFile(outputPath) {
        const mapping = this.allMedia.map(media => ({
            id: media.id,
            name: media.name,
            url: media.url || null,
            ext: media.ext || null
        }));

        fs.writeFileSync(outputPath, JSON.stringify(mapping, null, 2));
        console.log(`✅ Mapping file created: ${outputPath}`);
        console.log(`   Contains ${mapping.length} media items`);

        return mapping;
    }

    /**
     * Filter media relevant to Explores (images in compressed-images folder)
     */
    filterExploresMedia() {
        const compressedImagesPath = path.join(__dirname, 'compressed-images');
        let localImages = [];

        try {
            localImages = fs.readdirSync(compressedImagesPath)
                .filter(file => file.endsWith('.jpeg') || file.endsWith('.jpg') || file.endsWith('.png'));
        } catch (error) {
            console.warn('⚠️  Could not read compressed-images folder');
        }

        console.log(`\n📊 Local images in compressed-images: ${localImages.length}`);

        // Find matches in Strapi media
        const matches = [];
        const missing = [];

        localImages.forEach(localImage => {
            const found = this.allMedia.find(media => 
                media.name === localImage || 
                media.name.includes(localImage.split('.')[0])
            );

            if (found) {
                matches.push({
                    localName: localImage,
                    strapiId: found.id,
                    strapiName: found.name
                });
            } else {
                missing.push(localImage);
            }
        });

        console.log(`✅ Found ${matches.length} images in Strapi`);
        console.log(`❌ Missing ${missing.length} images in Strapi`);

        if (missing.length > 0) {
            console.log('\n⚠️  Images not found in Strapi (first 10):');
            missing.slice(0, 10).forEach(img => console.log(`   - ${img}`));
            if (missing.length > 10) {
                console.log(`   ... and ${missing.length - 10} more`);
            }
        }

        return { matches, missing };
    }

    /**
     * Main execution method
     */
    async run() {
        try {
            if (!this.apiToken) {
                console.error('❌ Error: API token is required');
                console.log('\nUsage:');
                console.log('  node fetch-strapi-media.js <API_TOKEN> [BASE_URL]');
                console.log('\nExample:');
                console.log('  node fetch-strapi-media.js your-api-token-here');
                console.log('  node fetch-strapi-media.js your-api-token-here http://localhost:1337');
                process.exit(1);
            }

            console.log('🚀 Starting Strapi Media Fetcher...\n');
            console.log(`   Base URL: ${this.baseUrl}`);
            console.log(`   API Token: ${this.apiToken.substring(0, 10)}...`);
            console.log('');

            await this.fetchAllMedia();

            const outputPath = path.join(__dirname, 'media-ids-and-names.json');
            this.createMappingFile(outputPath);

            this.filterExploresMedia();

            console.log('\n✅ Done!');
            console.log('\n📝 Next steps:');
            console.log('   1. Check media-ids-and-names.json for the mapping');
            console.log('   2. If images are missing, upload them to Strapi first');
            console.log('   3. Re-run this script after uploading');
            console.log('   4. Regenerate the Postman collection with: node generate_postman_collection.js');

        } catch (error) {
            console.error('❌ Error:', error);
            throw error;
        }
    }
}

// Run the fetcher
if (require.main === module) {
    const apiToken = process.argv[2];
    const baseUrl = process.argv[3] || 'http://localhost:1337';

    const fetcher = new StrapiMediaFetcher(baseUrl, apiToken);
    fetcher.run().catch(console.error);
}

module.exports = StrapiMediaFetcher;



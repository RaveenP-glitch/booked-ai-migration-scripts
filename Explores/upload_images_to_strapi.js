const fs = require('fs');
const path = require('path');

/**
 * Bulk Image Upload to Strapi
 * This script uploads all images from compressed-images folder to Strapi
 */

class ImageUploader {
    constructor(baseUrl, apiToken) {
        this.baseUrl = baseUrl || 'http://localhost:1337';
        this.apiToken = apiToken;
        this.imagesDir = path.join(__dirname, 'compressed-images');
        this.uploaded = 0;
        this.failed = 0;
        this.skipped = 0;
        this.failedFiles = [];
    }

    /**
     * Upload a single image to Strapi
     */
    async uploadImage(filePath, fileName) {
        try {
            // Read file as buffer
            const fileBuffer = fs.readFileSync(filePath);
            const blob = new Blob([fileBuffer], { type: 'image/jpeg' });
            
            // Create FormData
            const formData = new FormData();
            formData.append('files', blob, fileName);

            const response = await fetch(`${this.baseUrl}/api/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiToken}`
                },
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            const data = await response.json();
            return data[0];

        } catch (error) {
            throw error;
        }
    }

    /**
     * Check if image already exists in Strapi
     */
    async checkImageExists(fileName) {
        try {
            const response = await fetch(
                `${this.baseUrl}/api/upload/files?filters[name][$eq]=${encodeURIComponent(fileName)}`,
                {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${this.apiToken}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            if (!response.ok) {
                return false;
            }

            const data = await response.json();
            return (Array.isArray(data) && data.length > 0) || 
                   (data.data && Array.isArray(data.data) && data.data.length > 0);

        } catch (error) {
            return false;
        }
    }

    /**
     * Upload all images with progress tracking
     */
    async uploadAllImages(skipExisting = true) {
        if (!fs.existsSync(this.imagesDir)) {
            console.error(`❌ Error: Directory not found: ${this.imagesDir}`);
            return;
        }

        const files = fs.readdirSync(this.imagesDir)
            .filter(file => /\.(jpeg|jpg|png|webp)$/i.test(file))
            .sort();

        console.log(`📁 Found ${files.length} images in compressed-images/`);
        console.log(`⏱️  Estimated time: ~${Math.ceil(files.length * 0.5 / 60)} minutes\n`);

        const startTime = Date.now();

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const filePath = path.join(this.imagesDir, file);
            const progress = `[${i + 1}/${files.length}]`;

            try {
                // Check if already exists
                if (skipExisting) {
                    const exists = await this.checkImageExists(file);
                    if (exists) {
                        console.log(`${progress} ⏭️  Skipped (exists): ${file}`);
                        this.skipped++;
                        continue;
                    }
                }

                // Upload image
                console.log(`${progress} ⬆️  Uploading: ${file}`);
                const result = await this.uploadImage(filePath, file);

                if (result && result.id) {
                    console.log(`${progress} ✅ Uploaded (ID: ${result.id}): ${file}`);
                    this.uploaded++;
                } else {
                    throw new Error('No ID in response');
                }

                // Rate limiting - wait between uploads
                await this.delay(300);

            } catch (error) {
                console.error(`${progress} ❌ Failed: ${file}`);
                console.error(`            Error: ${error.message}`);
                this.failed++;
                this.failedFiles.push({ file, error: error.message });

                // Wait longer after error
                await this.delay(1000);
            }

            // Progress report every 50 images
            if ((i + 1) % 50 === 0) {
                const elapsed = (Date.now() - startTime) / 1000;
                const rate = (i + 1) / elapsed;
                const remaining = (files.length - i - 1) / rate;
                console.log(`\n📊 Progress: ${i + 1}/${files.length} (${((i + 1) / files.length * 100).toFixed(1)}%)`);
                console.log(`   Uploaded: ${this.uploaded} | Skipped: ${this.skipped} | Failed: ${this.failed}`);
                console.log(`   Time remaining: ~${Math.ceil(remaining / 60)} minutes\n`);
            }
        }

        const totalTime = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
        this.printSummary(totalTime);
    }

    /**
     * Delay helper
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Print upload summary
     */
    printSummary(totalTime) {
        console.log('\n' + '='.repeat(60));
        console.log('UPLOAD SUMMARY');
        console.log('='.repeat(60));
        console.log(`✅ Successfully uploaded: ${this.uploaded}`);
        console.log(`⏭️  Skipped (existing):   ${this.skipped}`);
        console.log(`❌ Failed:               ${this.failed}`);
        console.log(`⏱️  Total time:           ${totalTime} minutes`);

        if (this.failedFiles.length > 0) {
            console.log('\n❌ Failed files:');
            this.failedFiles.forEach(({ file, error }) => {
                console.log(`   - ${file}`);
                console.log(`     ${error}`);
            });
            console.log(`\n💡 Tip: You can re-run this script to retry failed uploads`);
        }

        console.log('\n📝 Next steps:');
        console.log('   1. Run: node fetch-strapi-media.js YOUR_API_TOKEN');
        console.log('   2. Run: node generate_postman_collection.js');
        console.log('   3. Import updated Postman collections');
        console.log('='.repeat(60));
    }

    /**
     * Retry failed uploads
     */
    async retryFailed() {
        if (this.failedFiles.length === 0) {
            console.log('✅ No failed uploads to retry');
            return;
        }

        console.log(`\n🔄 Retrying ${this.failedFiles.length} failed uploads...\n`);
        
        const toRetry = [...this.failedFiles];
        this.failedFiles = [];
        const previousFailed = this.failed;
        this.failed = 0;

        for (let i = 0; i < toRetry.length; i++) {
            const { file } = toRetry[i];
            const filePath = path.join(this.imagesDir, file);
            const progress = `[${i + 1}/${toRetry.length}]`;

            try {
                console.log(`${progress} ⬆️  Retrying: ${file}`);
                const result = await this.uploadImage(filePath, file);

                if (result && result.id) {
                    console.log(`${progress} ✅ Uploaded (ID: ${result.id}): ${file}`);
                    this.uploaded++;
                } else {
                    throw new Error('No ID in response');
                }

                await this.delay(300);

            } catch (error) {
                console.error(`${progress} ❌ Failed again: ${file}`);
                console.error(`            Error: ${error.message}`);
                this.failed++;
                this.failedFiles.push({ file, error: error.message });
                await this.delay(1000);
            }
        }

        console.log(`\n✅ Retry complete: ${this.uploaded} succeeded, ${this.failed} still failed`);
    }

    /**
     * Main execution method
     */
    async run(retry = false) {
        try {
            if (!this.apiToken) {
                console.error('❌ Error: API token is required\n');
                console.log('Usage:');
                console.log('  node upload_images_to_strapi.js <API_TOKEN> [BASE_URL]\n');
                console.log('Example:');
                console.log('  node upload_images_to_strapi.js your-api-token-here');
                console.log('  node upload_images_to_strapi.js your-api-token-here http://localhost:1337\n');
                process.exit(1);
            }

            console.log('🚀 Starting Bulk Image Upload to Strapi...\n');
            console.log(`   Base URL: ${this.baseUrl}`);
            console.log(`   API Token: ${this.apiToken.substring(0, 10)}...`);
            console.log(`   Images Dir: ${this.imagesDir}`);
            console.log('');

            await this.uploadAllImages(true);

            // Ask if user wants to retry failed uploads
            if (this.failedFiles.length > 0 && !retry) {
                console.log('\n💡 To retry failed uploads, run this script again');
            }

        } catch (error) {
            console.error('❌ Fatal error:', error);
            process.exit(1);
        }
    }
}

// Run the uploader
if (require.main === module) {
    const apiToken = process.argv[2];
    const baseUrl = process.argv[3] || 'http://localhost:1337';

    const uploader = new ImageUploader(baseUrl, apiToken);
    uploader.run().catch(console.error);
}

module.exports = ImageUploader;



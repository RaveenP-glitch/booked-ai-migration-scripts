const fs = require('fs');
const path = require('path');

// CSV to Strapi Data Converter
// This script converts CSV data to Strapi-compatible JSON format

class CSVToStrapiConverter {
    constructor(csvFilePath) {
        this.csvFilePath = csvFilePath;
        this.csvData = this.readCSV();
    }

    readCSV() {
        try {
            const csvContent = fs.readFileSync(this.csvFilePath, 'utf8');
            const lines = csvContent.split('\n');
            const headers = lines[0].split(',');
            
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
        } catch (error) {
            console.error('Error reading CSV file:', error);
            return [];
        }
    }

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

    convertToStrapiFormat(row) {
        // Helper function to clean and format text
        const cleanText = (text) => {
            if (!text) return '';
            return text.replace(/"/g, '\\"').replace(/\n/g, '\\n');
        };

        // Helper function to convert string to number
        const toNumber = (str) => {
            if (!str) return null;
            const cleaned = str.replace(/[^\d.-]/g, '');
            return cleaned ? parseFloat(cleaned) : null;
        };

        // Helper function to convert visitor count string to number
        const parseVisitorCount = (str) => {
            if (!str) return null;
            const cleaned = str.replace(/[^\d]/g, '');
            return cleaned ? parseInt(cleaned) : null;
        };

        // Helper function to format date
        const formatDate = (dateStr) => {
            if (!dateStr) return null;
            try {
                const date = new Date(dateStr);
                return date.toISOString();
            } catch (error) {
                return null;
            }
        };

        return {
            data: {
                Name: cleanText(row.Name),
                Slug: cleanText(row.Slug),
                Rating: toNumber(row.Rating),
                Description: cleanText(row.Description),
                Tag1: cleanText(row['Tag 1']),
                Tag2: cleanText(row['Tag 2']),
                Tag3: cleanText(row['Tag 3']),
                Formatted_Address: cleanText(row['Formatted Address']),
                Location: cleanText(row.Location),
                Main_Title: cleanText(row['Main Title']),
                City: cleanText(row.City),
                Country: cleanText(row.Country),
                Overview: cleanText(row.Overview),
                Intro: cleanText(row.Intro),
                Short_Summary: cleanText(row['Short Summary']),
                Entry_Fee: cleanText(row['Entry Fee']),
                Visitor_Count: parseVisitorCount(row['Visitor Count']),
                Visitor_Count_Description: cleanText(row['Visitor Count Description']),
                Review_Count: parseVisitorCount(row['Review Count']),
                Review_Rating: cleanText(row['Review Rating']),
                Review_Text: cleanText(row['Review Text']),
                Review_Link: cleanText(row['Review Link']),
                FAQ1: cleanText(row['FAQ 1']),
                FAQ2: cleanText(row['FAQ 2']),
                FAQ3: cleanText(row['FAQ 3']),
                FAQ4: cleanText(row['FAQ 4']),
                FAQ5: cleanText(row['FAQ 5']),
                publishedAt: formatDate(row['Published On'])
            }
        };
    }

    generatePostmanVariables(row) {
        const cleanText = (text) => {
            if (!text) return '';
            return text.replace(/"/g, '\\"').replace(/\n/g, '\\n');
        };

        const toNumber = (str) => {
            if (!str) return '';
            const cleaned = str.replace(/[^\d.-]/g, '');
            return cleaned ? cleaned : '';
        };

        const parseVisitorCount = (str) => {
            if (!str) return '';
            const cleaned = str.replace(/[^\d]/g, '');
            return cleaned ? cleaned : '';
        };

        const formatDate = (dateStr) => {
            if (!dateStr) return '';
            try {
                const date = new Date(dateStr);
                return date.toISOString();
            } catch (error) {
                return '';
            }
        };

        return {
            attractionName: cleanText(row.Name),
            attractionSlug: cleanText(row.Slug),
            rating: toNumber(row.Rating),
            description: cleanText(row.Description),
            tag1: cleanText(row['Tag 1']),
            tag2: cleanText(row['Tag 2']),
            tag3: cleanText(row['Tag 3']),
            formattedAddress: cleanText(row['Formatted Address']),
            location: cleanText(row.Location),
            mainTitle: cleanText(row['Main Title']),
            city: cleanText(row.City),
            country: cleanText(row.Country),
            overview: cleanText(row.Overview),
            intro: cleanText(row.Intro),
            shortSummary: cleanText(row['Short Summary']),
            entryFee: cleanText(row['Entry Fee']),
            visitorCount: parseVisitorCount(row['Visitor Count']),
            visitorCountDescription: cleanText(row['Visitor Count Description']),
            reviewCount: parseVisitorCount(row['Review Count']),
            reviewRating: cleanText(row['Review Rating']),
            reviewText: cleanText(row['Review Text']),
            reviewLink: cleanText(row['Review Link']),
            faq1: cleanText(row['FAQ 1']),
            faq2: cleanText(row['FAQ 2']),
            faq3: cleanText(row['FAQ 3']),
            faq4: cleanText(row['FAQ 4']),
            faq5: cleanText(row['FAQ 5']),
            publishedAt: formatDate(row['Published On']),
            // Block content fields
            innerPageContent: cleanText(row['Inner Page']),
            openingHours: cleanText(row['Opening Hours']),
            amenities: cleanText(row.Amenities),
            bestTimeToVisit: cleanText(row['Best Time to Visit']),
            photographyAllowed: cleanText(row['Photography Allowed']),
            accessibilityNotes: cleanText(row['Accessibility Notes']),
            culturalNotes: cleanText(row['Cultural/Religious Notes']),
            historicalSignificance: cleanText(row['Historical Significance']),
            famousEvents: cleanText(row['Famous Events or Dates']),
            timeRequired: cleanText(row['Time Required to Explore']),
            familyFriendly: cleanText(row['Kid/Family Friendly']),
            weatherSensitivity: cleanText(row['Weather Sensitivity']),
            transportation: cleanText(row['Transportation and Accessibility']),
            // Image URLs
            mainImageUrl: row['Main Image'],
            photo1Url: row['Photo 1'],
            photo2Url: row['Photo 2'],
            photo3Url: row['Photo 3'],
            photosUrl: row.Photos
        };
    }

    generateAllStrapiData() {
        return this.csvData.map(row => this.convertToStrapiFormat(row));
    }

    generateAllPostmanVariables() {
        return this.csvData.map(row => this.generatePostmanVariables(row));
    }

    saveStrapiData(outputPath) {
        const strapiData = this.generateAllStrapiData();
        fs.writeFileSync(outputPath, JSON.stringify(strapiData, null, 2));
        console.log(`Strapi data saved to ${outputPath}`);
    }

    savePostmanVariables(outputPath) {
        const postmanData = this.generateAllPostmanVariables();
        fs.writeFileSync(outputPath, JSON.stringify(postmanData, null, 2));
        console.log(`Postman variables saved to ${outputPath}`);
    }

    generateSampleRequestBodies() {
        const samples = [];
        for (let i = 0; i < Math.min(3, this.csvData.length); i++) {
            const row = this.csvData[i];
            const variables = this.generatePostmanVariables(row);
            
            samples.push({
                attractionName: row.Name,
                requestBody: {
                    data: {
                        Name: variables.attractionName,
                        Slug: variables.attractionSlug,
                        Rating: variables.rating ? parseFloat(variables.rating) : null,
                        Description: variables.description,
                        Tag1: variables.tag1,
                        Tag2: variables.tag2,
                        Tag3: variables.tag3,
                        Formatted_Address: variables.formattedAddress,
                        Location: variables.location,
                        Main_Title: variables.mainTitle,
                        City: variables.city,
                        Country: variables.country,
                        Overview: variables.overview,
                        Intro: variables.intro,
                        Short_Summary: variables.shortSummary,
                        Entry_Fee: variables.entryFee,
                        Visitor_Count: variables.visitorCount ? parseInt(variables.visitorCount) : null,
                        Visitor_Count_Description: variables.visitorCountDescription,
                        Review_Count: variables.reviewCount ? parseInt(variables.reviewCount) : null,
                        Review_Rating: variables.reviewRating,
                        Review_Text: variables.reviewText,
                        Review_Link: variables.reviewLink,
                        FAQ1: variables.faq1,
                        FAQ2: variables.faq2,
                        FAQ3: variables.faq3,
                        FAQ4: variables.faq4,
                        FAQ5: variables.faq5,
                        publishedAt: variables.publishedAt || new Date().toISOString()
                    }
                }
            });
        }
        return samples;
    }
}

// Usage example
const converter = new CSVToStrapiConverter('./Attractions4301-4340.csv');

// Generate and save all data
converter.saveStrapiData('./strapi_attractions_data.json');
converter.savePostmanVariables('./postman_variables.json');

// Generate sample request bodies
const samples = converter.generateSampleRequestBodies();
fs.writeFileSync('./sample_request_bodies.json', JSON.stringify(samples, null, 2));

console.log('Conversion complete!');
console.log('Generated files:');
console.log('- strapi_attractions_data.json: Complete Strapi data for all attractions');
console.log('- postman_variables.json: Postman variables for all attractions');
console.log('- sample_request_bodies.json: Sample request bodies for first 3 attractions');


// config.js - Configuration for Strapi migration
module.exports = {
  // Strapi connection settings
  strapi: {
    url: 'http://localhost:1337',
    adminEmail: 'admin@example.com', // Update with your admin email
    adminPassword: 'yourpassword', // Update with your admin password
  },
  
  // Content type settings
  contentType: 'articles', // Content type name in Strapi
  
  // Processing settings
  batchSize: 10, // Number of entries to process at once
  delayBetweenBatches: 2000, // Delay in milliseconds between batches
  
  // Field mappings from CSV to Strapi
  fieldMappings: {
    'Title': 'title',
    'Slug': 'slug',
    'Overview': 'description',
    'Image': 'cover',
    'Location': 'location',
    'Duration': 'duration',
    'Cost': 'cost',
    'Main Title': 'mainTitle'
  },
  
  // Rich text content settings
  richTextFields: {
    'Overview': 'content' // Map Overview to content rich text field
  },
  
  // Dynamic zone settings
  dynamicZoneFields: {
    'blocks': {
      // Component mappings for dynamic zone
      hotels: 'blocks.rich-text',
      restaurants: 'blocks.rich-text',
      attractions: 'blocks.rich-text'
    }
  },
  
  // Media settings
  media: {
    // Whether to download and upload images or just store URLs
    downloadImages: false, // Set to false to use existing media by name
    useExistingMedia: true, // Use existing media assets by name
    defaultMimeType: 'image/jpeg',
    provider: 'local' // or 'cloudinary', 'aws-s3', etc.
  },
  
  // Relation settings
  relations: {
    // Whether to create missing authors and categories
    createMissingAuthors: false, // Skip author relations
    createMissingCategories: false, // Skip category relations
    
    // Author content type name
    authorContentType: 'authors',
    
    // Category content type name  
    categoryContentType: 'categories'
  }
};

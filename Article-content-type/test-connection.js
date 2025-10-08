// test-connection.js
// Test script to verify Strapi connection and content type
const fetch = require('node-fetch');
const config = require('./config');

async function testConnection() {
  try {
    console.log('🔐 Testing Strapi connection...');
    
    // Test login
    const loginRes = await fetch(`${config.strapi.url}/api/auth/local`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        identifier: config.strapi.adminEmail, 
        password: config.strapi.adminPassword 
      }),
    });
    
    if (!loginRes.ok) {
      const error = await loginRes.json();
      console.error('❌ Login failed:', error);
      return;
    }
    
    const loginData = await loginRes.json();
    console.log('✅ Login successful');
    
    // Test content type access
    const jwt = loginData.jwt;
    const contentTypeRes = await fetch(`${config.strapi.url}/api/${config.contentType}`, {
      headers: {
        'Authorization': `Bearer ${jwt}`,
      },
    });
    
    if (!contentTypeRes.ok) {
      const error = await contentTypeRes.json();
      console.error(`❌ Content type '${config.contentType}' not accessible:`, error);
      return;
    }
    
    const contentTypeData = await contentTypeRes.json();
    console.log(`✅ Content type '${config.contentType}' accessible`);
    console.log(`📊 Found ${contentTypeData.data ? contentTypeData.data.length : 0} existing entries`);
    
    // Test media files access
    const mediaRes = await fetch(`${config.strapi.url}/api/upload/files`, {
      headers: {
        'Authorization': `Bearer ${jwt}`,
      },
    });
    
    if (!mediaRes.ok) {
      const error = await mediaRes.json();
      console.error('❌ Media files not accessible:', error);
      return;
    }
    
    const mediaData = await mediaRes.json();
    console.log(`✅ Media files accessible`);
    console.log(`📷 Found ${mediaData.data ? mediaData.data.length : 0} existing media files`);
    
    if (mediaData.data && mediaData.data.length > 0) {
      console.log('📋 Sample media files:');
      mediaData.data.slice(0, 3).forEach(file => {
        console.log(`  - ${file.name} (ID: ${file.id})`);
      });
    }
    
    console.log('\n🎉 All tests passed! Ready to run migration.');
    
  } catch (error) {
    console.error('💥 Test failed:', error.message);
  }
}

testConnection();







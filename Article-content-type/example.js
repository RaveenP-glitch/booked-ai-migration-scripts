// bulk-upload-rest.js
// Usage: node bulk-upload-rest.js data.json
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const STRAPI_URL = 'http://localhost:1337';
const ADMIN_EMAIL = 'admin@example.com'; // or use an API token (preferred)
const ADMIN_PASSWORD = 'yourpassword';
const BATCH_SIZE = 100;

async function login() {
  const res = await fetch(`${STRAPI_URL}/api/auth/local`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ identifier: ADMIN_EMAIL, password: ADMIN_PASSWORD }),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(json));
  return json.jwt;
}

async function createEntry(jwt, contentType, data) {
  const res = await fetch(`${STRAPI_URL}/api/${contentType}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${jwt}`,
    },
    body: JSON.stringify({ data }),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(json));
  return json;
}

(async () => {
  const file = process.argv[2] || path.join(__dirname, 'data.json');
  const items = JSON.parse(fs.readFileSync(file, 'utf8'));
  const jwt = await login();

  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE);
    const promises = batch.map(item => createEntry(jwt, 'articles', item)); // change 'articles'
    try {
      const results = await Promise.all(promises);
      console.log(`Uploaded batch ${i/BATCH_SIZE + 1}: ${results.length} items`);
    } catch (err) {
      console.error('Batch upload error:', err);
      // choose to continue or exit
      // process.exit(1);
    }
  }
})();
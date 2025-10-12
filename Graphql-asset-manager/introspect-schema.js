const { GraphQLClient, gql } = require('graphql-request');
const fs = require('fs');

// Configuration
const GRAPHQL_ENDPOINT = 'http://127.0.0.1:1337/graphql';
const API_TOKEN = 'dae398eefb2012379e258f1a8a068ce684b4fd3e6a0fb37912d61c05149816f1585c455fa709b6c963cd16df09755fd2b0d2b8d4e0e2e648b2343ec55a7887d814724bc72694be35e99324f39d3686b3de73881f82cbbe7e1ea738f246ac462c460c75073453f4eaa796cdda1c1f190e407987fe30006121139fdfe1d29d0182';

// Initialize GraphQL client
const client = new GraphQLClient(GRAPHQL_ENDPOINT, {
  headers: {
    authorization: `Bearer ${API_TOKEN}`,
  },
});

// Introspection query to get UploadFile type structure
const INTROSPECTION_QUERY = gql`
  query IntrospectUploadFile {
    __type(name: "UploadFile") {
      name
      kind
      fields {
        name
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
    }
  }
`;

// Query to list all available queries
const ROOT_QUERIES = gql`
  query GetRootQueries {
    __schema {
      queryType {
        fields {
          name
          type {
            name
            kind
          }
          args {
            name
            type {
              name
              kind
            }
          }
        }
      }
    }
  }
`;

async function introspectSchema() {
  console.log('Introspecting GraphQL schema...\n');
  
  try {
    console.log('1. Checking available root queries:');
    const rootData = await client.request(ROOT_QUERIES);
    const uploadRelatedQueries = rootData.__schema.queryType.fields.filter(
      field => field.name.toLowerCase().includes('upload') || field.name.toLowerCase().includes('file')
    );
    
    console.log('\nUpload/File related queries:');
    uploadRelatedQueries.forEach(query => {
      console.log(`  - ${query.name} (returns ${query.type.name || query.type.kind})`);
      if (query.args.length > 0) {
        console.log(`    Args: ${query.args.map(a => `${a.name}: ${a.type.name || a.type.kind}`).join(', ')}`);
      }
    });
    
    console.log('\n2. Checking UploadFile type structure:');
    const typeData = await client.request(INTROSPECTION_QUERY);
    
    if (typeData.__type) {
      console.log(`\nUploadFile fields:`);
      typeData.__type.fields.forEach(field => {
        const typeName = field.type.name || field.type.ofType?.name || field.type.kind;
        console.log(`  - ${field.name}: ${typeName}`);
      });
    }
    
    // Save introspection results
    const results = {
      rootQueries: uploadRelatedQueries,
      uploadFileType: typeData.__type
    };
    
    fs.writeFileSync('schema-introspection.json', JSON.stringify(results, null, 2));
    console.log('\n✓ Schema introspection saved to schema-introspection.json');
    
  } catch (error) {
    console.error('Error during introspection:', error.message);
    if (error.response) {
      console.error('Response errors:', JSON.stringify(error.response.errors, null, 2));
    }
    throw error;
  }
}

// Run the script
introspectSchema()
  .then(() => {
    console.log('\n✓ Introspection completed successfully!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\n✗ Introspection failed:', error.message);
    process.exit(1);
  });



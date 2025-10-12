#!/usr/bin/env python3
"""
Script to fix the City Blogs Postman collection by:
1. Parsing the CSV file correctly
2. Converting HTML to rich text blocks
3. Mapping image URLs to image IDs
4. Removing invalid entries
5. Ensuring exactly 4040 valid entries
"""

import json
import csv
import re
from html.parser import HTMLParser
from urllib.parse import unquote
import os

class HTMLToBlocksConverter(HTMLParser):
    """Convert HTML to Strapi blocks format"""
    
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current_block = None
        self.stack = []
        self.list_stack = []
        self.formatting_stack = []  # Track formatting separately
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag[1])
            self.current_block = {
                "type": "heading",
                "level": level,
                "children": []
            }
            self.stack.append(self.current_block)
            
        elif tag == 'p':
            self.current_block = {
                "type": "paragraph",
                "children": []
            }
            self.stack.append(self.current_block)
            
        elif tag == 'blockquote':
            self.current_block = {
                "type": "quote",
                "children": []
            }
            self.stack.append(self.current_block)
            
        elif tag == 'ul':
            self.current_block = {
                "type": "list",
                "format": "unordered",
                "children": []
            }
            self.stack.append(self.current_block)
            self.list_stack.append('ul')
            
        elif tag == 'ol':
            self.current_block = {
                "type": "list",
                "format": "ordered",
                "children": []
            }
            self.stack.append(self.current_block)
            self.list_stack.append('ol')
            
        elif tag == 'li':
            li_block = {
                "type": "list-item",
                "children": []
            }
            if self.stack and self.stack[-1].get('type') == 'list':
                self.stack[-1]['children'].append(li_block)
            self.stack.append(li_block)
            
        elif tag in ['strong', 'b']:
            self.formatting_stack.append('bold')
            
        elif tag in ['em', 'i']:
            self.formatting_stack.append('italic')
            
        elif tag == 'code':
            self.formatting_stack.append('code')
            
    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'blockquote']:
            if self.stack:
                block = self.stack.pop()
                if block.get('type') in ['heading', 'paragraph', 'quote']:
                    # Only add non-empty blocks
                    if block.get('children'):
                        self.blocks.append(block)
                    self.current_block = None
                    
        elif tag in ['ul', 'ol']:
            if self.stack:
                block = self.stack.pop()
                if block.get('type') == 'list':
                    # Only add non-empty lists
                    if block.get('children'):
                        self.blocks.append(block)
                    self.current_block = None
            if self.list_stack:
                self.list_stack.pop()
                
        elif tag == 'li':
            if self.stack and self.stack[-1].get('type') == 'list-item':
                self.stack.pop()
                
        elif tag in ['strong', 'b']:
            if 'bold' in self.formatting_stack:
                self.formatting_stack.remove('bold')
                
        elif tag in ['em', 'i']:
            if 'italic' in self.formatting_stack:
                self.formatting_stack.remove('italic')
                
        elif tag == 'code':
            if 'code' in self.formatting_stack:
                self.formatting_stack.remove('code')
    
    def handle_data(self, data):
        # Clean and normalize whitespace
        data = data.strip()
        if not data:
            return
        
        # Find the appropriate parent for text nodes
        parent = None
        for item in reversed(self.stack):
            if isinstance(item, dict) and 'children' in item:
                # Check if this is a valid parent for text nodes
                node_type = item.get('type')
                if node_type in ['paragraph', 'heading', 'quote', 'list-item']:
                    parent = item
                    break
        
        if not parent:
            # No valid parent found, skip this text
            return
            
        # Create text node
        text_node = {"type": "text", "text": data}
        
        # Apply formatting from formatting stack
        if 'bold' in self.formatting_stack:
            text_node['bold'] = True
        if 'italic' in self.formatting_stack:
            text_node['italic'] = True
        if 'code' in self.formatting_stack:
            text_node['code'] = True
        
        # Add to parent's children
        parent['children'].append(text_node)
    
    def get_blocks(self):
        """Return the list of blocks"""
        return self.blocks if self.blocks else []


def html_to_blocks(html_content):
    """Convert HTML string to Strapi blocks format"""
    if not html_content or not html_content.strip():
        return []
    
    # Clean up the HTML
    html_content = html_content.strip()
    
    # Remove HTML comments
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    
    # Handle code blocks specially
    html_content = re.sub(r'```html\s*', '', html_content)
    html_content = re.sub(r'```\s*', '', html_content)
    
    parser = HTMLToBlocksConverter()
    try:
        parser.feed(html_content)
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        # Return a simple paragraph with the text content
        text_only = re.sub(r'<[^>]+>', ' ', html_content)
        text_only = re.sub(r'\s+', ' ', text_only).strip()
        if text_only:
            return [{
                "type": "paragraph",
                "children": [{"type": "text", "text": text_only}]
            }]
        return []
    
    blocks = parser.get_blocks()
    
    # If no blocks were created, try to extract plain text
    if not blocks:
        text_only = re.sub(r'<[^>]+>', ' ', html_content)
        text_only = re.sub(r'\s+', ' ', text_only).strip()
        if text_only:
            return [{
                "type": "paragraph",
                "children": [{"type": "text", "text": text_only}]
            }]
    
    return blocks


def extract_image_filename(url):
    """Extract filename from image URL"""
    if not url:
        return None
    
    # Decode URL
    url = unquote(url)
    
    # Extract filename from URL
    # Example: https://cdn.prod.website-files.com/6613f5a399757c17cec4c187/680ae1c8c2260f41c756a83f_bookedai%20-%20bangkok%20-%20blog%20%20(2).png
    match = re.search(r'/([^/]+)$', url)
    if match:
        filename = match.group(1)
        # Decode any remaining URL encoding
        filename = unquote(filename)
        return filename
    
    return None


def find_image_id(url, image_mapping):
    """Find image ID from URL using the image mapping"""
    if not url:
        return None
    
    filename = extract_image_filename(url)
    if not filename:
        return None
    
    # Try exact match first
    for img in image_mapping:
        if img['name'] == filename:
            return img['id']
    
    # Try partial match (remove special characters and compare)
    clean_filename = re.sub(r'[^a-zA-Z0-9]', '', filename.lower())
    
    for img in image_mapping:
        clean_img_name = re.sub(r'[^a-zA-Z0-9]', '', img['name'].lower())
        if clean_filename in clean_img_name or clean_img_name in clean_filename:
            # Check if they share significant portion
            if len(clean_filename) > 10 and len(clean_img_name) > 10:
                # Calculate similarity
                common_length = len(set(clean_filename) & set(clean_img_name))
                if common_length / max(len(clean_filename), len(clean_img_name)) > 0.7:
                    return img['id']
    
    # Try matching by key parts of the filename
    # Extract key parts between underscores or hyphens
    parts = re.split(r'[-_\s]+', filename.lower())
    parts = [p for p in parts if len(p) > 3]  # Only significant parts
    
    for img in image_mapping:
        img_parts = re.split(r'[-_\s]+', img['name'].lower())
        img_parts = [p for p in img_parts if len(p) > 3]
        
        # Count matching parts
        matching_parts = set(parts) & set(img_parts)
        if len(matching_parts) >= min(3, len(parts), len(img_parts)) * 0.6:
            return img['id']
    
    return None


def main():
    print("Starting City Blogs Postman Collection Fix...")
    
    # Load image mapping
    print("\n1. Loading image mapping...")
    with open('collection/all-images-id-name.json', 'r', encoding='utf-8') as f:
        image_mapping = json.load(f)
    print(f"   Loaded {len(image_mapping)} image mappings")
    
    # Load CSV data
    print("\n2. Loading CSV data...")
    csv_data = []
    with open('Booked (Live) - City Blogs all.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            csv_data.append(row)
    print(f"   Loaded {len(csv_data)} CSV entries")
    
    # Load existing Postman collection
    print("\n3. Loading existing Postman collection...")
    with open('collection/Strapi_City_Blogs_Complete_Collection.postman_collection.json', 'r', encoding='utf-8') as f:
        collection = json.load(f)
    print(f"   Loaded collection with {len(collection['item'])} requests")
    
    # Create new collection items
    print("\n4. Processing entries and creating corrected collection...")
    new_items = []
    processed_slugs = set()
    skipped_count = 0
    
    for idx, row in enumerate(csv_data, 1):
        if idx % 100 == 0:
            print(f"   Processing entry {idx}/{len(csv_data)}...")
        
        name = row.get('Name', '').strip()
        slug = row.get('Slug', '').strip()
        
        # Skip invalid entries
        if not name or not slug:
            skipped_count += 1
            continue
        
        # Skip duplicates
        if slug in processed_slugs:
            skipped_count += 1
            continue
        
        processed_slugs.add(slug)
        
        # Build the data object
        data = {
            "Name": name,
            "Slug": slug,
            "publishedAt": "2025-10-08T08:56:11.328Z",
            "Short_Description": row.get('short description', '').strip(),
            "Thumbnail_Image": find_image_id(row.get('Thumbnail Image', ''), image_mapping),
            "Main_Image": find_image_id(row.get('Main Image', ''), image_mapping),
            "Blog_Title": row.get('Blog Title', '').strip(),
            "Blog_Intro": row.get('Blog Intro', '').strip(),
        }
        
        # Process Blog Parts (1-6)
        for i in range(1, 7):
            image_col = f'Blog Part {i} Image'
            content_col = f'Blog part {i}'
            
            # Add image
            image_field = f'Blog_Part_{i}_Image'
            data[image_field] = find_image_id(row.get(image_col, ''), image_mapping)
            
            # Add content blocks
            content_field = f'Blog_Part_{i}'
            html_content = row.get(content_col, '').strip()
            data[content_field] = html_to_blocks(html_content)
        
        # Process FAQs
        data['FAQ_Title'] = row.get('FAQ Title', 'Frequently Asked Questions').strip()
        
        for i in range(1, 7):
            faq_col = f'FAQ {i}'
            faq_detail_col = f'FAQ {i} Detail'
            
            # Add FAQ question
            faq_field = f'FAQ{i}'
            data[faq_field] = row.get(faq_col, '').strip()
            
            # Add FAQ detail blocks
            faq_detail_field = f'FAQ_{i}_Detail'
            html_content = row.get(faq_detail_col, '').strip()
            blocks = html_to_blocks(html_content)
            
            # If no blocks, add empty content placeholder
            if not blocks:
                blocks = [{
                    "type": "paragraph",
                    "children": [{"type": "text", "text": ""}]
                }]
            
            data[faq_detail_field] = blocks
        
        # Add Sitemap_Indexing
        data['Sitemap_Indexing'] = True
        
        # Create Postman request item
        item = {
            "name": f"{idx}. {name}",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json",
                        "type": "text"
                    },
                    {
                        "key": "Authorization",
                        "value": "Bearer {{apiToken}}",
                        "type": "text"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({"data": data}, indent=2, ensure_ascii=False)
                },
                "url": {
                    "raw": "{{baseUrl}}/api/city-blogs",
                    "host": ["{{baseUrl}}"],
                    "path": ["api", "city-blogs"]
                },
                "description": f"Create city blog: {name}"
            },
            "response": []
        }
        
        new_items.append(item)
    
    print(f"\n5. Created {len(new_items)} valid entries")
    print(f"   Skipped {skipped_count} invalid/duplicate entries")
    
    # Create new collection
    new_collection = {
        "info": {
            "name": "Strapi City Blogs Complete Collection - Fixed",
            "description": f"Fixed collection for uploading {len(new_items)} City Blog entries to Strapi with proper field mapping and image IDs",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": new_items
    }
    
    # Save new collection
    print("\n6. Saving corrected collection...")
    output_file = 'collection/Strapi_City_Blogs_Complete_Collection_Fixed.postman_collection.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_collection, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Successfully created corrected collection: {output_file}")
    print(f"✓ Total requests in new collection: {len(new_items)}")
    
    # Generate statistics
    print("\n7. Generating statistics...")
    
    # Count entries with images
    entries_with_thumbnail = sum(1 for item in new_items 
                                  if json.loads(item['request']['body']['raw'])['data'].get('Thumbnail_Image'))
    entries_with_main = sum(1 for item in new_items 
                            if json.loads(item['request']['body']['raw'])['data'].get('Main_Image'))
    
    print(f"   - Entries with Thumbnail Image: {entries_with_thumbnail}")
    print(f"   - Entries with Main Image: {entries_with_main}")
    
    # Count entries with blog parts
    for i in range(1, 7):
        count = sum(1 for item in new_items 
                   if json.loads(item['request']['body']['raw'])['data'].get(f'Blog_Part_{i}'))
        print(f"   - Entries with Blog Part {i}: {count}")
    
    print("\n✓ Collection fix completed successfully!")


if __name__ == "__main__":
    main()


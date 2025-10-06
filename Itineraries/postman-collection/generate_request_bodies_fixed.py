#!/usr/bin/env python3
"""
Script to generate request bodies for Itineraries posts from CSV data.
Creates both sample requests (first 2) and full collection.
Fixed to handle rich text fields as blocks and correct slug format.
"""

import json
import csv
import re
from datetime import datetime
import os
from bs4 import BeautifulSoup

def html_to_blocks(html_content):
    """Convert HTML content to Strapi block format."""
    if not html_content or html_content.strip() == '':
        return []
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    blocks = []
    
    # Process each element
    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'div']):
        if element.name in ['p', 'div']:
            # Paragraph block
            text_content = element.get_text().strip()
            if text_content:
                blocks.append({
                    "type": "paragraph",
                    "children": [
                        {
                            "type": "text",
                            "text": text_content
                        }
                    ]
                })
        elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            # Heading block
            text_content = element.get_text().strip()
            if text_content:
                blocks.append({
                    "type": "heading",
                    "level": int(element.name[1]),  # Extract level from h1, h2, etc.
                    "children": [
                        {
                            "type": "text",
                            "text": text_content
                        }
                    ]
                })
        elif element.name in ['ul', 'ol']:
            # List block
            list_items = []
            for li in element.find_all('li'):
                li_text = li.get_text().strip()
                if li_text:
                    list_items.append({
                        "type": "list-item",
                        "children": [
                            {
                                "type": "text",
                                "text": li_text
                            }
                        ]
                    })
            
            if list_items:
                blocks.append({
                    "type": "list",
                    "format": "unordered" if element.name == 'ul' else "ordered",
                    "children": list_items
                })
        elif element.name == 'blockquote':
            # Quote block
            text_content = element.get_text().strip()
            if text_content:
                blocks.append({
                    "type": "quote",
                    "children": [
                        {
                            "type": "text",
                            "text": text_content
                        }
                    ]
                })
    
    # If no blocks were created, create a simple paragraph
    if not blocks:
        text_content = soup.get_text().strip()
        if text_content:
            blocks.append({
                "type": "paragraph",
                "children": [
                    {
                        "type": "text",
                        "text": text_content
                    }
                ]
            })
    
    return blocks

def clean_html_content(html_content):
    """Clean and format HTML content for Strapi rich text fields."""
    if not html_content or html_content.strip() == '':
        return []
    
    # Convert HTML to blocks
    return html_to_blocks(html_content)

def create_slug(name):
    """Create a URL-friendly slug from the name."""
    if not name:
        return ""
    
    # Convert to lowercase and replace spaces with hyphens
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remove special characters
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with hyphens
    slug = re.sub(r'-+', '-', slug)  # Replace multiple hyphens with single
    slug = slug.strip('-')  # Remove leading/trailing hyphens
    
    return slug

def format_date(date_str):
    """Format date string for Strapi."""
    if not date_str or date_str.strip() == '':
        return datetime.now().isoformat() + 'Z'
    
    try:
        # Parse the date and format it
        # Handle various date formats that might be in the CSV
        if 'GMT' in date_str:
            # Parse GMT date format
            dt = datetime.strptime(date_str, '%a %b %d %Y %H:%M:%S GMT%z (%Z)')
        else:
            # Try other common formats
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                # If no format matches, use current time
                dt = datetime.now()
        
        return dt.isoformat() + 'Z'
    except Exception:
        # If parsing fails, use current time
        return datetime.now().isoformat() + 'Z'

def create_itinerary_request_body(row, image_mapping, row_number):
    """Create a request body for a single itinerary entry."""
    
    # Get image IDs from mapping
    mapping = image_mapping.get(str(row_number), {})
    thumbnail_id = mapping.get('thumbnail_id')
    main_image_id = mapping.get('main_image_id')
    itinerary_image_id = mapping.get('itinerary_image_id')
    
    # Create the request body
    request_body = {
        "data": {
            "Name": row.get('Name', '').strip(),
            "Slug": create_slug(row.get('Name', '')),
            "publishedAt": format_date(row.get('Published On', '')),
            "Short_Description": row.get('short description', '').strip(),
            "Thumbnail_Image": thumbnail_id,
            "Main_Image": main_image_id,
            "Itineraray_Title": row.get('Itinerary Title', '').strip(),  # Note: typo in schema
            "Itinerary_Image": itinerary_image_id,
            "Itinerary1": clean_html_content(row.get('Itinerary 1', '')),
            "Itinerary2": clean_html_content(row.get('Itinerary 2', '')),
            "Itinerary3": clean_html_content(row.get('Itinerary 3', '')),
            "Itinerary4": clean_html_content(row.get('Itinerary 4', '')),
            "Itinerary5": clean_html_content(row.get('Itinerary 5', '')),
            "Itinerary6": clean_html_content(row.get('Itinerary 6', '')),
            "Itinerary7": clean_html_content(row.get('Itinerary 7', '')),
            "Tag1": row.get('Tag 1', '').strip(),
            "Tag2": row.get('Tag 2', '').strip(),
            "Tag3": row.get('Tag 3', '').strip(),
            "FAQ1": row.get('FAQ 1', '').strip(),
            "FAQ2": row.get('FAQ 2', '').strip(),
            "FAQ3": row.get('FAQ 3', '').strip(),
            "FAQ4": row.get('FAQ 4', '').strip(),
            "FAQ5": row.get('FAQ 5', '').strip(),
            "FAQ6": row.get('FAQ 6', '').strip(),
            "FAQ_1_Detail": clean_html_content(row.get('FAQ 1 Detail', '')),
            "FAQ_2_Detail": clean_html_content(row.get('FAQ 2 Detail', '')),
            "FAQ_3_Detail": clean_html_content(row.get('FAQ 3 Detail', '')),
            "FAQ_4_Detail": clean_html_content(row.get('FAQ 4 Detail', '')),
            "FAQ_5_Detail": clean_html_content(row.get('FAQ 5 Detail', '')),
            "FAQ_6_Detail": clean_html_content(row.get('FAQ 6 Detail', '')),
            "Sitemap_Indexing": True
        }
    }
    
    return request_body

def create_postman_request(name, request_body, row_number):
    """Create a Postman request item."""
    return {
        "name": f"{row_number}. {name}",
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
                "raw": json.dumps(request_body, indent=2, ensure_ascii=False)
            },
            "url": {
                "raw": "{{baseUrl}}/api/itineraries",
                "host": [
                    "{{baseUrl}}"
                ],
                "path": [
                    "api",
                    "itineraries"
                ]
            },
            "description": f"Create itinerary: {name}"
        },
        "response": []
    }

def main():
    # Load image mapping
    with open('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/postman-collection/image_mapping.json', 'r', encoding='utf-8') as f:
        image_mapping = json.load(f)
    
    # Read CSV file
    csv_file = '/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/Booked (Live) - Itineraries.csv'
    
    all_requests = []
    sample_requests = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row_number, row in enumerate(reader, 1):
            # Create request body
            request_body = create_itinerary_request_body(row, image_mapping, row_number)
            
            # Create Postman request
            name = row.get('Name', f'Itinerary {row_number}').strip()
            postman_request = create_postman_request(name, request_body, row_number)
            
            # Add to collections
            all_requests.append(postman_request)
            
            # Add first 2 to sample
            if row_number <= 2:
                sample_requests.append({
                    "row_number": row_number,
                    "name": name,
                    "request_body": request_body
                })
    
    # Create sample request bodies file
    with open('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/postman-collection/sample_request_bodies_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(sample_requests, f, indent=2, ensure_ascii=False)
    
    # Create full request bodies file
    with open('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/postman-collection/full_request_bodies_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(all_requests, f, indent=2, ensure_ascii=False)
    
    # Create Postman collection
    postman_collection = {
        "info": {
            "name": "Strapi Itineraries Collection - Fixed Format",
            "description": "Complete collection for uploading all itineraries to Strapi with correct block format",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": all_requests
    }
    
    with open('/Users/raveen/Documents/GitHub/booked-ai-migration-scripts/Itineraries/postman-collection/Strapi_Itineraries_Collection_Fixed.postman_collection.json', 'w', encoding='utf-8') as f:
        json.dump(postman_collection, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(all_requests)} itinerary requests")
    print(f"Sample requests: {len(sample_requests)}")
    print("Files created:")
    print("- sample_request_bodies_fixed.json")
    print("- full_request_bodies_fixed.json") 
    print("- Strapi_Itineraries_Collection_Fixed.postman_collection.json")

if __name__ == "__main__":
    main()

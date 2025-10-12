#!/usr/bin/env python3
"""
Script to divide the fixed Postman collection into 4 parts for batch processing
"""

import json
import math

def divide_collection_into_parts(input_file, output_folder, num_parts=4):
    """Divide a Postman collection into multiple parts"""
    
    print(f"Loading collection from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        collection = json.load(f)
    
    total_items = len(collection['item'])
    items_per_part = math.ceil(total_items / num_parts)
    
    print(f"Total entries: {total_items}")
    print(f"Dividing into {num_parts} parts (~{items_per_part} entries each)\n")
    
    # Create parts
    for part_num in range(num_parts):
        start_idx = part_num * items_per_part
        end_idx = min((part_num + 1) * items_per_part, total_items)
        
        # Extract items for this part
        part_items = collection['item'][start_idx:end_idx]
        
        # Create new collection for this part
        part_collection = {
            "info": {
                "name": f"{collection['info']['name']} - Part {part_num + 1} of {num_parts}",
                "description": f"Part {part_num + 1} of {num_parts}: Entries {start_idx + 1} to {end_idx} ({len(part_items)} entries)",
                "schema": collection['info']['schema']
            },
            "item": part_items
        }
        
        # Save part
        output_file = f"{output_folder}/Strapi_City_Blogs_Part_{part_num + 1}_of_{num_parts}.postman_collection.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(part_collection, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Part {part_num + 1}: Entries {start_idx + 1:4d}-{end_idx:4d} ({len(part_items):4d} entries) → {output_file}")
    
    print(f"\n✅ Successfully created {num_parts} collection parts in {output_folder}/")
    
    # Create summary file
    summary = {
        "total_entries": total_items,
        "num_parts": num_parts,
        "entries_per_part": items_per_part,
        "parts": []
    }
    
    for part_num in range(num_parts):
        start_idx = part_num * items_per_part
        end_idx = min((part_num + 1) * items_per_part, total_items)
        summary["parts"].append({
            "part_number": part_num + 1,
            "file": f"Strapi_City_Blogs_Part_{part_num + 1}_of_{num_parts}.postman_collection.json",
            "start_entry": start_idx + 1,
            "end_entry": end_idx,
            "total_entries": end_idx - start_idx
        })
    
    summary_file = f"{output_folder}/README.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Summary saved to {summary_file}")


def main():
    input_file = "collection/Strapi_City_Blogs_Complete_Collection_Fixed.postman_collection.json"
    output_folder = "collection-fixed-parts"
    
    print("=" * 80)
    print("DIVIDING COLLECTION INTO PARTS")
    print("=" * 80)
    print()
    
    divide_collection_into_parts(input_file, output_folder, num_parts=4)
    
    print("\n" + "=" * 80)
    print("DIVISION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Script to read all award names from Airtable

This script connects to an Airtable base to extract award names from a specified
table and field. It handles authentication through an API key stored in the .env file
or passed as a command-line argument.
"""

import os
import sys
import argparse
import json
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for the Airtable reader
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Read award names and categories from Airtable base and save to JSON"
    )
    
    parser.add_argument(
        '--api-key', '-k',
        type=str,
        help='Airtable API key (will use AIRTABLE_API_KEY from .env file if not provided)'
    )
    
    parser.add_argument(
        '--base-id', '-b',
        type=str,
        default='appNLda8uMnN5ZJPb',  # Base ID extracted from Airtable URL
        help='Airtable base ID (default: appNLda8uMnN5ZJPb)'
    )
    
    parser.add_argument(
        '--table-name', '-t',
        type=str,
        default='Awards Overview',
        help='Airtable table name (default: Awards Overview)'
    )
    
    parser.add_argument(
        '--field-name', '-f',
        type=str,
        default='Award Name',
        help='Field name for award names (default: Award Name)'
    )
    
    parser.add_argument(
        '--category-field', '-c',
        type=str,
        default='Categories',
        help='Field name for award categories (default: Categories)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='airtable_awards.json',
        help='Output file path for the JSON file (default: airtable_awards.json)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress verbose output'
    )
    
    return parser.parse_args()


def get_api_key(args: argparse.Namespace) -> str:
    """Get API key from args or environment variables
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        str: The Airtable API key
        
    Raises:
        ValueError: If no API key is found
    """
    # First priority: command line argument
    if args.api_key:
        return args.api_key
    
    # Second priority: .env file
    load_dotenv()
    env_key = os.getenv('AIRTABLE_API_KEY')
    if env_key:
        return env_key
    
    # If no key found, raise error
    raise ValueError("No Airtable API key provided. Please set AIRTABLE_API_KEY in .env file or use --api-key")


def read_airtable_award_names(api_key: str, base_id: str, table_name: str, field_name: str, category_field: str, verbose: bool = True) -> Dict[str, Dict[str, Any]]:
    """
Read award names from Airtable, handling pagination to get all records
    
    Args:
        api_key: Airtable API key
        base_id: Airtable base ID
        table_name: Name of the table to read from
        field_name: Name of the field containing award names
        verbose: Whether to print status messages
        
    Returns:
        List[str]: List of award names
    """
    base_url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    all_records = []
    offset = None
    page_count = 0
    
    try:
        # Implement pagination to retrieve all records
        while True:
            page_count += 1
            if verbose:
                print(f"Fetching page {page_count} of records...")
            
            # Add offset parameter if we have one
            params = {}
            if offset:
                params['offset'] = offset
            
            # Make the API request
            response = requests.get(base_url, headers=headers, params=params, timeout=15)
            
            if response.status_code != 200:
                if verbose:
                    print(f"Error: HTTP {response.status_code}")
                    print(response.text)
                return {}
            
            data = response.json()
            page_records = data.get('records', [])
            all_records.extend(page_records)
            
            # Check if there are more records to fetch
            offset = data.get('offset')
            if not offset:
                break
        
        # Extract award names and categories from all records
        awards_data = {}
        for record in all_records:
            if 'fields' in record and field_name in record['fields']:
                award_name = record['fields'][field_name]
                
                # Get categories if available
                categories = []
                if category_field in record['fields']:
                    # Categories might be a string or a list in Airtable
                    cat_data = record['fields'][category_field]
                    if isinstance(cat_data, list):
                        categories = cat_data
                    elif isinstance(cat_data, str):
                        categories = [cat.strip() for cat in cat_data.split(',')]
                    
                awards_data[award_name] = {
                    "name": award_name,
                    "categories": categories,
                    "record_id": record.get('id', '')
                }
        
        if verbose:
            print(f"Successfully read {len(awards_data)} awards from Airtable (from {len(all_records)} total records)")
        return awards_data
    
    except requests.exceptions.Timeout:
        if verbose:
            print("Error: Connection to Airtable timed out")
        return {}
    except requests.exceptions.ConnectionError:
        if verbose:
            print("Error: Failed to connect to Airtable")
        return {}
    except Exception as e:
        if verbose:
            print(f"Error reading from Airtable: {str(e)}")
        return {}


def save_to_json(data: Dict[str, Dict[str, Any]], output_file: str, verbose: bool = True) -> bool:
    """Save data to JSON file
    
    Args:
        data: Award data dictionary to save
        output_file: Path to output file
        verbose: Whether to print status messages
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        if verbose:
            print(f"Successfully saved data to {output_file}")
        return True
    except Exception as e:
        if verbose:
            print(f"Error saving to JSON: {str(e)}")
        return False


def list_available_bases(api_key: str, verbose: bool = True) -> List[Dict[str, str]]:
    """List available bases to verify API connection
    
    Args:
        api_key: Airtable API key
        verbose: Whether to print status messages
        
    Returns:
        List[Dict[str, str]]: List of bases with name and ID
    """
    url = "https://api.airtable.com/v0/meta/bases"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            bases = []
            for base in data.get('bases', []):
                bases.append({
                    'name': base.get('name', 'Unknown'),
                    'id': base.get('id', 'Unknown')
                })
            
            if verbose:
                print("\nSuccessfully connected to Airtable API")
                print(f"Bases available: {len(bases)}")
                for base in bases:
                    print(f"  - Base: {base['name']} (ID: {base['id']})")
            return bases
        else:
            if verbose:
                print(f"\nError accessing Airtable metadata: {response.status_code}")
                print(response.text)
            return []
    except Exception as e:
        if verbose:
            print(f"Error accessing Airtable metadata: {str(e)}")
        return []

def main():
    """Main entry point for the script"""
    # Parse arguments
    args = parse_arguments()
    verbose = not args.quiet
    
    # Use the API key from args or env file
    try:
        api_key = get_api_key(args)
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Please provide an API key using --api-key or by setting AIRTABLE_API_KEY in .env")
        sys.exit(1)
    
    if verbose:
        print(f"Using Airtable API key: {api_key[:5]}...{api_key[-5:]}")
        print(f"Using Airtable base ID: {args.base_id}")
        print(f"Table name: {args.table_name}")
        print(f"Award field name: {args.field_name}")
        print(f"Category field name: {args.category_field}")
        print(f"Output file: {args.output}")
    
    # Try to read from the base ID
    if verbose:
        print(f"\nAttempting to read from base: {args.base_id}")
    
    awards_data = read_airtable_award_names(
        api_key=api_key,
        base_id=args.base_id,
        table_name=args.table_name,
        field_name=args.field_name,
        category_field=args.category_field,
        verbose=verbose
    )
    
    # If failed, provide a simple error message without interactive troubleshooting
    if not awards_data and verbose:
        print("\nFailed to read award data. This could be due to:")
        print("  1. The API key doesn't have access to this base")
        print("  2. The table name might be different than expected")
        print("  3. The field name or category field name might be different than expected")
        print("\nTry running the script with different options:")
        print("  python read_airtable_awards.py --table-name \"TABLE_NAME\" --field-name \"FIELD_NAME\" --category-field \"CATEGORY_FIELD\"")
    
    # Save results if we have any
    if awards_data:
        success = save_to_json(awards_data, args.output, verbose=verbose)
        if not success:
            sys.exit(1)
            
        if verbose:
            print(f"Total awards found: {len(awards_data)}")
            # Print all award names with their categories
            if awards_data:
                print("\nAll awards with categories:")
                for i, (award_name, award_info) in enumerate(awards_data.items()):
                    categories = award_info.get('categories', [])
                    if categories:
                        category_text = ", ".join(categories)
                        print(f"  {i+1}. {award_name} - Categories: {category_text}")
                    else:
                        print(f"  {i+1}. {award_name} - No categories found")
    elif verbose:
        print("\nNo award data was retrieved. Please check your Airtable credentials and base information.")
        sys.exit(1)
    



if __name__ == "__main__":
    main()

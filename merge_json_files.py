import json
from typing import List, Dict

def load_json_file(file_path: str) -> List[Dict]:
    """Load JSON file and return its contents."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: {file_path} contains invalid JSON")
        return []

def convert_name_to_award_dict(name: str) -> Dict:
    """Convert a simple award name to award dictionary format."""
    return {
        'award_name': name.strip(),
        'registration_url': '',
        'categories': [],
        'organization': ''
    }

def merge_awards(detailed_awards: List[Dict], award_names: List[str]) -> List[Dict]:
    """Merge detailed awards with award names list."""
    merged = {}
    
    # First, add all detailed awards
    for award in detailed_awards:
        name = award['award_name'].strip()
        merged[name] = award
    
    # Then, add any missing awards from the names list
    for name in award_names:
        name = name.strip()
        if name and name not in merged:
            merged[name] = convert_name_to_award_dict(name)

    # Convert back to list and sort by award name
    return sorted(merged.values(), key=lambda x: x['award_name'])

def save_json_file(data: List[Dict], output_file: str):
    """Save data to a JSON file with proper formatting."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved merged data to {output_file}")
    except Exception as e:
        print(f"Error saving to JSON: {str(e)}")

def main():
    # Input files
    file1 = 'bookawards.json'
    file2 = 'bookawards_airtable_manual.json'
    output_file = 'bookawards_merged.json'

    # Load both JSON files
    awards1 = load_json_file(file1)
    awards2 = load_json_file(file2)

    if not awards1 or not awards2:
        print("Error: Could not proceed with merge due to missing or invalid input files")
        return

    # Merge the awards
    merged_awards = merge_awards(awards1, awards2)

    # Save the merged result
    save_json_file(merged_awards, output_file)
    
    # Print some statistics
    print(f"\nMerge Statistics:")
    print(f"Original file 1 ({file1}): {len(awards1)} awards")
    print(f"Original file 2 ({file2}): {len(awards2)} awards")
    print(f"Merged result: {len(merged_awards)} awards")

if __name__ == "__main__":
    main()

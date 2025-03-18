import os
from pyairtable import Api
import json
from typing import List, Dict
from datetime import datetime

class AirtableToJson:
    def __init__(self, api_key: str, base_id: str, table_id: str):
        self.api = Api(api_key)
        self.base_id = base_id
        self.table_id = table_id
        self.table = self.api.table(base_id, table_id)

    def fetch_records(self) -> List[Dict]:
        """Fetch all records from the Airtable table."""
        try:
            records = self.table.all()
            return [record['fields'] for record in records]
        except Exception as e:
            print(f"Error fetching records: {str(e)}")
            return []

    def transform_records(self, records: List[Dict]) -> List[Dict]:
        """Transform Airtable records into the desired JSON format."""
        transformed_records = []
        for record in records:
            award_entry = {
                "award_name": record.get("Award Name", ""),
                "registration_url": record.get("Registration URL", ""),
                "categories": record.get("Categories", []),
                "organization": record.get("Organization", "")
            }
            transformed_records.append(award_entry)
        return transformed_records

    def save_to_json(self, data: List[Dict], output_file: str = "bookawards.json"):
        """Save the transformed records to a JSON file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Successfully saved data to {output_file}")
        except Exception as e:
            print(f"Error saving to JSON: {str(e)}")

def main():
    # These should be set as environment variables
    API_KEY = os.getenv("AIRTABLE_API_KEY")
    BASE_ID = "appoxpcNACeB8MxxF"  # From your Airtable URL
    TABLE_ID = "tblNCMCfFZ3LnakRj"  # From your Airtable URL

    if not API_KEY:
        print("Error: AIRTABLE_API_KEY environment variable not set")
        return

    converter = AirtableToJson(API_KEY, BASE_ID, TABLE_ID)
    
    # Fetch records from Airtable
    records = converter.fetch_records()
    if not records:
        print("No records found or error occurred")
        return

    # Transform records to desired format
    transformed_data = converter.transform_records(records)

    # Save to JSON file
    output_file = "bookawards.json"
    converter.save_to_json(transformed_data, output_file)

if __name__ == "__main__":
    main()

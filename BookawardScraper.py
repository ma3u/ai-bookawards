import json
import os
import requests
import argparse
from typing import List, Dict
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables
load_dotenv()

class BookawardScraper:
    def __init__(self, json_file: str = 'bookawards_merged.json'):
        self.json_file = json_file
        self.awards = []
        self.console = Console()
        self.perplexity_url = "https://api.perplexity.ai/chat/completions"
        self.api_key = os.environ.get('PERPLEXITY_API_KEY')

    def load_awards(self) -> List[Dict]:
        """Load and parse the bookawards JSON file."""
        try:
            with open(self.json_file, 'r') as f:
                self.awards = json.load(f)
            return self.awards
        except FileNotFoundError:
            print(f"Error: {self.json_file} not found")
            return []
        except json.JSONDecodeError:
            print(f"Error: {self.json_file} contains invalid JSON")
            return []

        """
        Enrich the bookawards data with additional information from Perplexity.
        
        Returns a new list of enriched award dictionaries.
        """
    def get_award_info_from_perplexity(self, award: Dict) -> Dict:
        """Get additional information about an award using Perplexity API."""
        if not self.api_key:
            print("Error: PERPLEXITY_API_KEY not set in environment variables")
            return award

        prompt = (
            f"Create a structured JSON object for the {award['award_name']} literary award, including the following details:\n"
            "Registration URL: The web address where participants can register for the award.\n"
            "Categories: A list of categories under which books can compete.\n"
            "Organization: The organization responsible for hosting the award.\n"
            "Last Winning Books for the {award['award_name']} literary award: An array of the winning books the last years, with each entry containing:\n"
            "  - Author\n"
            "  - Title\n"
            "  - Publishing Year\n"
            "  - Publisher\n"
            "  - ISBN\n"
            "  - Link to the book\n"
            "Latest Date of Submission: The deadline for submitting entries for this year's award.\n"
            "Possible Strongest Competition This Year: A list of books or authors likely to be strong contenders in this year's competition.\n\n"
            "Ensure that the JSON is formatted as follows:\n"
            "{\n"
            "  \"bookAward\": {\n"
            "    \"registrationUrl\": \"https://example.com/register\",\n"
            "    \"categories\": [\"Fiction\", \"Non-Fiction\", \"Poetry\", \"Young Adult\"],\n"
            "    \"organization\": \"National Book Foundation\",\n"
            "    \"lastWinningBooks\": [\n"
            "      {\n"
            "        \"author\": \"John Doe\",\n"
            "        \"title\": \"The Great Novel\",\n"
            "        \"publishingYear\": 2024,\n"
            "        \"publisher\": \"Fictional Press\",\n"
            "        \"isbn\": \"123-4567890123\",\n"
            "        \"link\": \"https://example.com/the-great-novel\"\n"
            "      },\n"
            "      {\n"
            "        \"author\": \"Jane Smith\",\n"
            "        \"title\": \"Poems of the Heart\",\n"
            "        \"publishingYear\": 2024,\n"
            "        \"publisher\": \"Poetry House\",\n"
            "        \"isbn\": \"987-6543210987\",\n"
            "        \"link\": \"https://example.com/poems-of-the-heart\"\n"
            "      }\n"
            "    ],\n"
            "    \"latestDateOfSubmission\": \"2025-04-30\",\n"
            "    \"possibleStrongestCompetitionThisYear\": [\n"
            "      {\n"
            "        \"author\": \"Alice Johnson\",\n"
            "        \"title\": \"A New Dawn\"\n"
            "      },\n"
            "      {\n"
            "        \"author\": \"Bob Brown\",\n"
            "        \"title\": \"The Last Frontier\"\n"
            "      }\n"
            "    ]\n"
            "  }\n"
            "}\n"
            # "Use \"Not available\" for information that cannot be found, but make reasonable predictions based on past winners and trends for the competition section.\n"
            "Please ensure to find finding the last winning books of the last year for this aw.\n"
            "Response should be ONLY the valid JSON without any other text."
        )

        payload = {
            "temperature": 0.1,  # Lower temperature for more consistent output
            "top_p": 0.9,
            "model": "sonar",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.perplexity_url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    content = data['choices'][0]['message']['content']
                    
                    # Try to extract JSON from the response if it's embedded in text
                    try:
                        # Find JSON-like structure in the content
                        json_start = content.find('{')
                        json_end = content.rfind('}') + 1
                        if json_start >= 0 and json_end > json_start:
                            json_str = content[json_start:json_end]
                            parsed_json = json.loads(json_str)
                            
                            # Extract the bookAward object
                            if 'bookAward' in parsed_json:
                                book_award = parsed_json['bookAward']
                                # Store the enriched data in the award object
                                award['enriched_data'] = book_award
                                print(f"Successfully enriched data for {award['award_name']}")
                            else:
                                print(f"Warning: No 'bookAward' field in response for {award['award_name']}")
                        else:
                            print(f"Warning: No JSON structure found in response for {award['award_name']}")
                    except json.JSONDecodeError:
                        print(f"Error: Could not parse JSON response for {award['award_name']}")
                else:
                    print(f"Error: No choices in response for {award['award_name']}")
            else:
                print(f"Error: API request failed with status {response.status_code} for {award['award_name']}")
        except requests.exceptions.Timeout:
            print(f"Error: Request timed out for {award['award_name']}")
        except Exception as e:
            print(f"Error making API request for {award['award_name']}: {str(e)}")

        return award

    def enrich_awards_with_perplexity(self, limit: int = None) -> List[Dict]:
        """Enrich awards with additional information from Perplexity.
        
        Args:
            limit: Maximum number of awards to process (None for all)
        """
        enriched_awards = []
        
        # Limit to the specified number or use all awards
        awards_to_process = self.awards[:limit] if limit else self.awards
        total_awards = len(awards_to_process)
        
        print(f"Processing {total_awards} awards out of {len(self.awards)} total")

        for i, award in enumerate(awards_to_process, 1):
            print(f"Processing award {i}/{total_awards}: {award['award_name']}")
            try:
                enriched_award = self.get_award_info_from_perplexity(award.copy())
                enriched_awards.append(enriched_award)
                # Save progress after each successful enrichment
                with open('bookawards_result_partial.json', 'w', encoding='utf-8') as f:
                    json.dump(enriched_awards, f, indent=2, ensure_ascii=False)
                print(f"Progress saved for {award['award_name']}")
            except KeyboardInterrupt:
                print("\nProcess interrupted by user. Saving current progress...")
                if enriched_awards:
                    with open('bookawards_result_partial.json', 'w', encoding='utf-8') as f:
                        json.dump(enriched_awards, f, indent=2, ensure_ascii=False)
                    print(f"Progress saved with {len(enriched_awards)} processed awards")
                raise
            except Exception as e:
                print(f"Error processing {award['award_name']}: {str(e)}")
                continue

        # Add remaining awards without enrichment if we limited the processing
        if limit and limit < len(self.awards):
            for award in self.awards[limit:]:
                award_copy = award.copy()
                award_copy['enriched_data'] = {"note": "Data not enriched due to processing limit"}
                enriched_awards.append(award_copy)

        return enriched_awards

    def save_enriched_awards(self, output_file: str = 'bookawards_result.json', limit: int = None):
        """Save enriched awards data to a new JSON file.
        
        Args:
            output_file: Path to the output JSON file
            limit: Maximum number of awards to enrich (None for all)
        """
        enriched_awards = self.enrich_awards_with_perplexity(limit=limit)
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(enriched_awards, f, indent=2, ensure_ascii=False)
            print(f"Successfully saved enriched awards data to {output_file}")
        except Exception as e:
            print(f"Error saving enriched awards: {str(e)}")

    def get_award_by_name(self, name: str) -> Dict:
        """Get a specific award entry by name."""
        for award in self.awards:
            if award.get('award_name', '').lower() == name.lower():
                return award
        return {}

    def get_awards_by_category(self, category: str) -> List[Dict]:
        """Get all awards that include a specific category."""
        matching_awards = []
        for award in self.awards:
            if category in award.get('categories', []):
                matching_awards.append(award)
        return matching_awards

    def get_all_categories(self) -> List[str]:
        """Get a list of all unique categories across all awards."""
        categories = set()
        for award in self.awards:
            categories.update(award.get('categories', []))
        return sorted(list(categories))

    def get_awards_by_organization(self, organization: str) -> List[Dict]:
        """Get all awards associated with a specific organization."""
        return [award for award in self.awards 
                if award.get('organization', '').lower() == organization.lower()]

# Command line argument handling and documentation
def parse_arguments():
    """
    Parse command line arguments for the book award scraper.
    
    Returns:
        Parsed arguments object with the following attributes:
        - limit: Maximum number of awards to enrich with Perplexity (None for all)
        - output: Path to the output JSON file
        - help: Display help documentation
    """
    parser = argparse.ArgumentParser(
        description='''
        BookawardScraper: A tool to enrich book award data using the Perplexity API
        
        This script reads book award data from a JSON file and enriches it with additional
        information fetched from the Perplexity API. The enriched data is then saved to a
        new JSON file.
        
        The script requires a Perplexity API key to be set in the .env file as PERPLEXITY_API_KEY.
        ''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=None,
        help='Maximum number of awards to enrich with Perplexity API (default: unlimited)\n'
             'Example: --limit 5 will process only the first 5 awards'
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        default='bookawards_merged.json',
        help='Path to the input JSON file with award data (default: bookawards_merged.json)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='bookawards_result.json',
        help='Path to the output JSON file (default: bookawards_result.json)'
    )
    
    return parser.parse_args()

# Example usage
if __name__ == '__main__':
    # Parse command line arguments
    args = parse_arguments()
    
    # Initialize scraper with input file and load awards
    scraper = BookawardScraper(json_file=args.input)
    awards = scraper.load_awards()
    
    print(f"Total number of awards: {len(awards)}")
    
    # Handle different limit scenarios
    if args.limit is None:
        process_limit = None
        print("Processing all awards (this may take a while and incur significant Perplexity API costs)")
    elif args.limit == 0:
        process_limit = None
        print("Processing all awards (this may take a while and incur significant Perplexity API costs)")
    else:
        process_limit = args.limit
        print(f"Limiting Perplexity API requests to the first {args.limit} awards")
    
    # Enrich awards with Perplexity API data and save to specified output file
    scraper.save_enriched_awards(output_file=args.output, limit=process_limit)

    print("\nExample - First 3 enriched book awards:")
    for i, award in enumerate(scraper.awards[:3], 1):
        print(f"\n{i}. {award['award_name']}")
        print(f"   Organization: {award.get('organization', 'Not specified')}")
        print(f"   Categories: {', '.join(award.get('categories', ['None']))}")
        
        # Show enriched data if available
        if 'enriched_data' in award and isinstance(award['enriched_data'], dict):
            print(f"   Latest submission date: {award['enriched_data'].get('latestDateOfSubmission', 'Not available')}")
            
            # Show potential competition if available
            competition = award['enriched_data'].get('possibleStrongestCompetitionThisYear', [])
            if competition and len(competition) > 0:
                print(f"   Top competitor: {competition[0].get('author', 'Unknown')}: {competition[0].get('title', 'Unknown')}")

    print("\nAll unique award categories:")
    categories = scraper.get_all_categories()
    print(f"Total unique categories: {len(categories)}")
    print("First 10 categories:")
    print(', '.join(sorted(categories)[:10]))
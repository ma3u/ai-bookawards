import json
from typing import List, Dict

class BookawardScraper:
    def __init__(self, json_file: str = 'bookawards.json'):
        self.json_file = json_file
        self.awards = []

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

# Example usage
if __name__ == '__main__':
    scraper = BookawardScraper()
    awards = scraper.load_awards()
    
    print(f"Total number of awards: {len(awards)}")
    print("\nExample - Getting award by name:")
    pulitzer = scraper.get_award_by_name('Pulitzer Prize')
    print(json.dumps(pulitzer, indent=2))
    
    print("\nExample - Getting awards for Fiction category:")
    fiction_awards = scraper.get_awards_by_category('Fiction')
    print(f"Number of awards with Fiction category: {len(fiction_awards)}")
    
    print("\nUnique categories:")
    categories = scraper.get_all_categories()
    print(f"Total unique categories: {len(categories)}")
    print("First 5 categories:")
    print(json.dumps(categories[:5], indent=2))
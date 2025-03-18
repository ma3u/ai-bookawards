# Book Award AI Scraper

A tool to enrich book award data using the Perplexity API. This script reads award data from a JSON file and enriches it with additional information fetched from the Perplexity API, then saves the results to a new JSON file.

## Setup

1. Setup file `.env` with your Perplexity API key:

```
PERPLEXITY_API_KEY=<YOUR_API_KEY>
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the environment:
```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

4. Install required packages:
```bash
pip install requests rich python-dotenv
```

## Usage

Run the script with command line arguments to control the number of Perplexity API requests and output file:

```bash
python BookawardScraper.py [options]
```

### Command Line Options

- `--limit` or `-l`: Maximum number of awards to enrich with Perplexity API (default: unlimited)
  - Example: `--limit 5` will process only the first 5 awards, reducing API costs
  - Warning: Processing all awards will incur significant Perplexity API costs

- `--input` or `-i`: Path to the input JSON file with award data (default: bookawards_merged.json)
  - Example: `--input custom_awards.json`

- `--output` or `-o`: Path to the output JSON file (default: bookawards_result.json)
  - Example: `--output enriched_awards.json`

### Examples

1. Process only the first 10 awards to reduce API costs:
```bash
python BookawardScraper.py --limit 10
```

2. Process all awards and save to a custom file:
```bash
python BookawardScraper.py --output my_enriched_awards.json
```

3. Process a small subset for testing and save to a different file:
```bash
python BookawardScraper.py --limit 3 --output test_awards.json
```

4. Display help and available options:
```bash
python BookawardScraper.py --help
```

## Output

The script will create two JSON files:
1. `bookawards_result.json` (or your specified output file): Contains all awards with enriched data for the processed awards
2. `bookawards_result_partial.json`: Progressive backup saved after each successful API call (useful if the process is interrupted)
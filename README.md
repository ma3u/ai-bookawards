# Book Award AI Tools

A collection of tools to process book award data through a complete workflow:

1. [**Merge JSON**](#1-merge-json-files): Combine Perplexity deep research data with existing list of awards
2. [**Bookaward Scraper**](#2-bookaward-scraper): Enrich award data using the Perplexity API
3. [**Transform to Excel**](#3-json-to-excel-transformation): Convert JSON data to Excel format for analysis
4. [**Import to Airtable**](#4-airtable-integration): Upload and maintain the data in Airtable for collaboration
5. [**Read from Airtable**](#5-read-from-airtable): Extract award names from Airtable database

This project provides scripts that work together to process and enrich book award data, resulting in a well-structured Excel file ready for analysis and import.

## Table of Contents

- [Setup](#setup)
- [Complete Workflow](#complete-workflow)
  - [Workflow Diagram](#workflow-diagram)
- [1. Merge JSON Files](#1-merge-json-files)
- [2. Bookaward Scraper](#2-bookaward-scraper)
- [3. JSON to Excel Transformation](#3-json-to-excel-transformation)
- [4. Airtable Integration](#4-airtable-integration)
- [5. Read from Airtable](#5-read-from-airtable)

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

## Complete Workflow

The complete workflow for processing book awards data involves five main steps:

1. [**Merge JSON files**](#1-merge-json-files) to combine your Perplexity research data with existing award listings
2. [**Enrich data**](#2-bookaward-scraper) with the BookawardScraper using the Perplexity API
3. [**Transform to Excel**](#3-json-to-excel-transformation) format for easy viewing and analysis
4. [**Import to Airtable**](#4-airtable-integration) to maintain the data in a collaborative database
5. [**Read from Airtable**](#5-read-from-airtable) to extract award names from your Airtable database

### Workflow Diagram

```mermaid
flowchart TD
    C[Perplexity Research JSON] -->|merge_json_files.py| D[Merged JSON]
    D -->|BookawardScraper.py| E[Enriched JSON]
    E -->|transformJSON2excel.py| F[Excel Workbook]
    F -->|Manual Review| G[Verified Data]
    G -->|Upload to Airtable| A[Airtable Database]
    A -->|read_airtable_awards.py| B[Award Names JSON]
    
    style A fill:#b7dbff,stroke:#007bff
    style F fill:#ffdfb7,stroke:#ff8c00
    style G fill:#c9e6ca,stroke:#28a745
```

```bash
# Step 1: Merge JSON files
python merge_json_files.py

# Step 2: Enrich the award data (optionally with a limit to reduce API costs)
python BookawardScraper.py --limit 10

# Step 3: Transform the enriched data to Excel
python transformJSON2excel.py

# Step 4: Import back to Airtable (manual step via Excel import)

# Step 5: Read award names from Airtable
python read_airtable_awards.py
```

## 1. Merge JSON Files

The `merge_json_files.py` script combines two JSON files containing book award data.

### Merge Script Usage

Simply run the script with no arguments:

```bash
python merge_json_files.py
```

The script will:

- Merge data from `bookawards.json` and `bookawards_airtable_manual.json`
- Output the combined data to `bookawards_merged.json`
- Print statistics about the merge process

## 2. Bookaward Scraper

The `BookawardScraper.py` script enriches book award data using the Perplexity API.

### Scraper Usage

Run the script with command line arguments to control the number of Perplexity API requests and output file:

```bash
python BookawardScraper.py [options]
```

### Scraper Command Line Options

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

### Output

The script will create two JSON files:
1. `bookawards_result.json` (or your specified output file): Contains all awards with enriched data for the processed awards
2. `bookawards_result_partial.json`: Progressive backup saved after each successful API call (useful if the process is interrupted)

## 3. JSON to Excel Transformation

After enriching the book award data, you can transform the JSON data into a well-structured Excel file using the `transformJSON2excel.py` script.

### Transform Script Usage

Run the script with command line arguments to specify input and output files:

```bash
python transformJSON2excel.py [options]
```

### Transform Script Options

- `--input` or `-i`: Path to the input JSON file with enriched award data (default: bookawards_result.json)
  - Example: `--input custom_enriched_awards.json`

- `--output` or `-o`: Path to the output Excel file (default: bookawards.xlsx)
  - Example: `--output my_bookawards.xlsx`

### Transform Script Examples

1. Transform the default enriched data file to Excel:

```bash
python transformJSON2excel.py
```

2. Use a custom input JSON file and output Excel file:

```bash
python transformJSON2excel.py --input custom_enriched_awards.json --output custom_bookawards.xlsx
```

3. Display help and available options:

```bash
python transformJSON2excel.py --help
```

### Excel Output Structure

The generated Excel file contains the following sheets:

1. **Awards Overview**: Contains basic information about each award, including award name, organization, registration URL, and enriched data
2. **Winning Books**: Lists the winning books for each award, including author, title, publishing year, publisher, ISBN, and link
3. **Competition**: Contains information about potential competitors for each award
4. **Categories**: Lists all categories for each award

![alt text](image-1.png)

## 4. Airtable Integration

### Importing Excel Data to Airtable

Once you've generated the Excel file, you can import the data into Airtable:

1. **Sign in to Airtable** and open your base (or create a new one)
2. **Add a new table** for each sheet you want to import
3. **Import data** using Airtable's import feature:
   - Click "Add or import" → "Import data" → "From file"
   - Select your Excel file (e.g., `bookawards.xlsx`)
   - Choose the sheet to import
   - Airtable will auto-detect field types, but review and adjust as needed
   - Click "Import" to complete the process

![alt text](image.png)

### Field Type Recommendations

For optimal data structure in Airtable:

- **Text fields**: Award names, descriptions, websites
- **URL fields**: Links to award sites, registration pages
- **Number fields**: Years, counts
- **Date fields**: Award dates, submission deadlines
- **Long text fields**: Extended descriptions, eligibility details

## 5. Read from Airtable

The `read_airtable_awards.py` script extracts award names from your Airtable database and saves them to a JSON file.

### Script Features

- Connects to Airtable using your API key
- Extracts award names from a specified table and field
- Saves the data as a structured JSON file
- Shows all award entries in the output
- Supports quiet mode for use in automated workflows

### Airtable Script Usage

```bash
python read_airtable_awards.py [options]
```

### Airtable Command Line Options

| Option | Description |
|--------|-------------|
| `-k`, `--api-key` | Airtable API key (will use AIRTABLE_API_KEY from .env file if not provided) |
| `-b`, `--base-id` | Airtable base ID (default: appNLda8uMnN5ZJPb) |
| `-t`, `--table-name` | Table name to read from (default: Awards Overview) |
| `-f`, `--field-name` | Field name to extract (default: Award Name) |
| `-o`, `--output` | Output JSON file path (default: airtable_awards.json) |
| `-q`, `--quiet` | Suppress verbose output |

### Airtable Script Examples

```bash
# Use default settings
python read_airtable_awards.py

# Specify custom table and field
python read_airtable_awards.py --table-name "My Table" --field-name "Award Title"

# Use in automated workflows
python read_airtable_awards.py --quiet
```

The script will output a JSON file containing the award names, which can be used in subsequent steps of the workflow. The script now displays all award entries in the console output, making it easier to verify the data.

#### Troubleshooting

If the script fails to retrieve data:

1. Verify your API key is correct
2. Confirm the base ID matches your Airtable base
3. Check that the table name and field name exactly match what's in your Airtable base
4. Try running with different options as suggested in the error message

### Read Airtable Awards Script Details

The `read_airtable_awards.py` script is a powerful tool for extracting award data from your Airtable base. It implements full pagination support to retrieve all records, regardless of how many there are (Airtable's API limits each page to 100 records).

#### How It Works

The script connects to the Airtable API and retrieves all records from a specified table, extracting the award names from a specified field. The script handles pagination automatically, making multiple API requests as needed to retrieve all records.

- Airtable API key
- Airtable base ID

The `read_airtable_awards.py` script supports a complete bidirectional workflow:

1. **Extract data** from Airtable using `read_airtable_awards.py`
2. **Process and enrich** the data with the Perplexity API
3. **Transform to Excel** for review and modifications
4. **Import back to Airtable** for data persistence

This creates a powerful cycle where data can flow between systems while maintaining data integrity.

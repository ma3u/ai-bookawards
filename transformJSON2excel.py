import json
import pandas as pd

# Load JSON data
# Option 1: From a JSON string
json_str = '''[
  {
    "award_name": "National Book Award",
    "registration_url": "https://www.nationalbook.org/national-book-awards/submissions/",
    "categories": ["Fiction", "Nonfiction", "Poetry", "Translated Literature"],
    "organization": "National Book Foundation"
  },
  {
    "award_name": "Pulitzer Prize",
    "registration_url": "https://www.pulitzer.org/entry-information",
    "categories": ["Fiction", "Drama", "History", "Biography"],
    "organization": "Columbia University"
  }
]'''
data = json.loads(json_str)

# Option 2: From a JSON file
# with open('your_file.json', 'r') as file:
#    data = json.load(file)

# Convert to DataFrame
df = pd.DataFrame(data)

# Export to Excel
excel_filename = 'output.xlsx'
df.to_excel(excel_filename, index=False)

print(f"Excel file '{excel_filename}' has been created successfully.")

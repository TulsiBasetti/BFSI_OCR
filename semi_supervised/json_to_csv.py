"""
JSON to DataFrame Conversion & CSV Saving

- Load JSON: Loads the JSON data from a file into a Python dictionary.
- Extract Transactions: Retrieves the list of transactions from the nested JSON structure.
- DataFrame Creation: Converts the list of transactions into a pandas DataFrame.
- Save CSV: Saves the DataFrame as a CSV file at a specified location.
"""

import json
import pandas as pd

with open(r"C:\BFSI_OCR\data\statement.json") as file:
    data_dictionary = json.load(file)# Parse JSON string into a Python dictionary

#Extract transactions list from JSON
transactions = data_dictionary["AccountStatementOverAPIResponse"]["Data"]["AccountStatementReportResponseBody"]["data"]

#Convert list of transactions into a Pandas DataFrame
df = pd.DataFrame(transactions)

#Save DataFrame to a CSV file
csv_filepath = r"C:\BFSI_OCR\data\api_data.csv"
df.to_csv(csv_filepath, index=False)
print(f"CSV file '{csv_filepath}' has been created successfully!")

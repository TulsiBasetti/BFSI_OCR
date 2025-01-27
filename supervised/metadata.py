"""
MCC Extraction & Matching with BERT

- Extracts MCC codes and descriptions from a PDF.
- Generates BERT embeddings for descriptions.
- Searches for best match using cosine similarity.
- User Input: Finds the closest MCC code or description.
"""

import os
import re
import torch
import pdfplumber
import pandas as pd
from dotenv import load_dotenv
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables (remove database credentials)
load_dotenv()

# Initialize a list to store MCC data
mcc_data = []

# Extract MCC codes and descriptions from PDF
pdf_path = r"C:\BFSI_OCR\data\Merchant-Category-Codes.pdf"
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            for row in table:
                if row and row[0] and row[1]:  # Ensure valid MCC and Description
                    if row[0].isdigit():  # Ensure it's an MCC code
                        mcc_data.append([row[0].strip(), row[1].strip()])
        else:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    match = re.match(r"^(\d{4})\s+(.+)", line)  # Find MCC codes and description
                    if match:
                        mcc_data.append([match.group(1), match.group(2)])

# Convert extracted data to DataFrame and save as CSV
df = pd.DataFrame(mcc_data, columns=["MCC", "Description"])
df.to_csv(r"C:\BFSI_OCR\data\mcc_codes.csv", index=False)
print("CSV file created successfully!")

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Convert MCC descriptions into BERT embeddings
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

# Add a new column for embeddings
df["embedding"] = df["Description"].apply(lambda x: get_embedding(x).tolist())

# Search for MCC Code or Description using BERT-based similarity
def find_best_match(query):
    if query.isdigit():  # If the user enters an MCC code
        match = df[df["MCC"] == query]
        return match["Description"].values[0] if not match.empty else "MCC code not found."
    else:  # If the user enters a description and needs to find the closest MCC code
        query_embedding = get_embedding(query)
        similarities = df["embedding"].apply(lambda x: cosine_similarity([query_embedding], [x])[0][0])
        best_match_index = similarities.idxmax()
        return df.iloc[best_match_index]["MCC"]

# Prompt user for input and return best match
while True:
    user_input = input("Enter MCC code or category (or type 'exit'): ").strip()
    if user_input.lower() == "exit":
        break
    print("Best Match MCC Code:", find_best_match(user_input))

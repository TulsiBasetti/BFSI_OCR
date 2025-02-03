"""
Bank Statement Processing & Visualization

- Extracts tables from PDFs and saves as CSV.
- Cleans and categorizes transaction descriptions.
- Analyzes spending per category.
- Generates pie, bar, and scatter charts for visualization.
- Integrates with Streamlit for web display.
"""

import pdfplumber
import pandas as pd
import re
import matplotlib.pyplot as plt
import streamlit as st

# Function to extract data from the PDF and save it to a CSV
def extract_data_from_pdf(pdf_path, csv_path):
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()  # Extract tables from each page
            for table in tables:
                for row in table:  # Extract row from each table
                    transactions.append(row)  # Append each extracted row in the list

    # Convert extracted data into a DataFrame
    df = pd.DataFrame(transactions)

    # Remove all rows and columns having all values NaN
    df = df.dropna(how='all').dropna(axis=1, how='all')

    # Save DataFrame as CSV
    df.to_csv(csv_path, index=False, header=False)
    return df

# Function to clean and standardize transaction descriptions
def clean_description(description):
    if pd.isna(description):  # If there are missing values
        return ""
    description = str(description).lower()  # Convert to lowercase
    description = re.sub(r"[^a-zAZ0-9\s@]", "", description)  # Remove special characters except '@'
    description = re.sub(r"\s+", " ", description).strip()  # Remove extra spaces
    return description

# Function to categorize the transaction descriptions
def categorize_transaction(description):
    category_mapping = {
        "Food": ["swiggy", "zomato", "faasos", "ovenstory", "restaurant", "pizza", "mcdonald"],
        "Transport": ["metro", "uber", "ola", "fuel", "petrol", "bus", "train", "olacabs"],
        "Shopping": ["amazon", "flipkart", "myntra", "ebay", "paytm", "snapdeal"],
        "Utilities": ["electricity", "water bill", "internet", "phone recharge", "vodafone", "jio", "billdesk"],
        "Entertainment": ["netflix", "prime", "spotify", "hotstar", "movie"],
        "Salary": ["salary", "payout", "income", "credit interest"],
        "Health": ["pharmacy", "medical", "hospital", "larimedicals", "medicine", "doctor"],
        "ATM Withdrawals": ["atm wdl", "cash withdrawal", "atm"],
        "Bank_fees": ["sms charges", "account charges", "service fee", "penalty"],
        "Peer To Peer": ["upi", "imps", "transfer", "to", "by", "neft", "rtgs"],
        "Loan Payments": ["emi", "loan", "repayment"]
    }

    for category, keywords in category_mapping.items():
        if any(keyword in description for keyword in keywords):
            return category  # Assign the matched category
    return "other"  # If no match is found

# Function to clean data and categorize transactions
def process_bank_statement(pdf_path, output_csv_path=r"C:\BFSI_OCR\data\Bank_transactions_categories.csv"):
    # Extract data from PDF
    df = extract_data_from_pdf(pdf_path, r"C:\BFSI_OCR\data\bank_transactions.csv")

    # Load CSV file
    df = pd.read_csv(r"C:\BFSI_OCR\data\bank_transactions.csv")

    # Apply cleaning function to descriptions
    df["Cleaned_Description"] = df["Description"].apply(clean_description)

    # Apply categorization function
    df["Category"] = df["Cleaned_Description"].apply(categorize_transaction)

    # Save the corrected CSV
    df.to_csv(output_csv_path, index=False)

    return df

# Function to visualize spending distribution by category
def plot_category_spending(df):

    colors = [
        '#2E5A4E',  # Deep Forest Green
        '#437C6F',  # Medium Sea Green
        '#598C75',  # Sage Green
        '#6B4423',  # Deep Brown
        '#8B6B4F',  # Medium Brown
        '#A47551',  # Light Brown
        '#C49A6C'   # Pale Brown
    ]
    # Clean the 'DR' and 'CR' columns by filling NaN with 0 and converting to numeric
    df["DR"] = pd.to_numeric(df["DR"], errors='coerce')
    df["CR"] = pd.to_numeric(df["CR"], errors='coerce')

    # Calculate the amount spent (DR is outflow, CR is inflow, DR-CR)
    df["Amount"] = df["DR"].fillna(0) - df["CR"].fillna(0)

    # Remove rows with the category "other"
    df = df[df["Category"] != "other"]

    # Group by Category and sum the total amount for each category
    category_totals = df.groupby("Category")["Amount"].sum()

    # Remove categories with zero or negative spending 
    category_totals = category_totals[category_totals > 0]

   
    # Plot the Pie Chart
    plt.figure(figsize=(8, 8))
    category_totals.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title("Spending Distribution Per Category (Pie Chart)",fontsize=16)
    plt.ylabel("")  # To remove the y-axis label (default text)
    plt.tight_layout()
    
    # Use Streamlit to display the pie chart
    st.pyplot(plt)

    # Plot the Bar Graph
    plt.figure(figsize=(12, 6)) 
    category_totals.plot(kind='bar', color=colors, edgecolor='black')
    plt.title("Total Spending by Category (Bar Graph)",fontsize=16)
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")
    plt.xticks(rotation=0)  # Set x-axis labels to be straight
    plt.tight_layout()
    
    # Use Streamlit to display the bar chart
    st.pyplot(plt)

    # Plot the Scatter Plot for Spending by Category
    plt.figure(figsize=(10, 6))
    plt.scatter(category_totals.index, category_totals, color='#6B4423', s=100)  # 's' defines the size of the points
    plt.title("Total Spending by Category (Scatter Plot)",fontsize=16)
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Use Streamlit to display the scatter plot
    st.pyplot(plt)

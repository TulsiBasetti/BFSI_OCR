"""
Invoice Data Extraction & Visualization

Features:
- Extracts invoice details (Description, Qty, Price, Total) using OCR.
- Cleans and structures extracted data into a DataFrame.
- Generates visualizations:
  - Bar Chart: Displays total price per item.
  - Line Chart: Shows price trends.
  - Pie Chart: Illustrates item-wise cost distribution.
"""

import pandas as pd
import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

pytesseract.pytesseract.tesseract_cmd = r"C:\\Tesseract-OCR\\tesseract.exe"

def extract_invoice_data(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_string(gray)
    # Extract relevant lines 
    lines = [line.strip() for line in data.split('\n') if line.strip()]
    
    # Parse invoice details
    extracted_data = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 4:  # Ensure line has required columns
            description = " ".join(parts[:-3])  # Merge words for description
            if description.strip().upper() == "GRAND":  # Check if description is "GRAND"
                 continue  # Skip this row
            qty = parts[-3]
            price = parts[-2]
            total = parts[-1]
            extracted_data.append([description, qty, price, total])
    
    # Convert to DataFrame
    df = pd.DataFrame(extracted_data, columns=["Description", "Qty", "Price", "Total"])
    return df

def generate_visualizations(df):
    # Convert columns to numeric, forcing errors to NaN
    df["Qty"] = pd.to_numeric(df["Qty"], errors='coerce')
    df["Total"] = pd.to_numeric(df["Total"], errors='coerce')
    df = df.dropna()

    if df.empty:
        print("No valid data to visualize.")
        return None, None, None  

    # Bar Chart
    fig_bar, ax_bar = plt.subplots(figsize=(8, 5))
    ax_bar.bar(df["Description"], df["Total"], color='#ffeb3b') 
    plt.xticks(rotation=0, ha='right')
    plt.ylabel("Total Price")
    plt.title("Invoice (Bar Chart)",fontsize=16)
    plt.tight_layout()
    
    # Line Chart
    fig_line, ax_line = plt.subplots(figsize=(8, 5))
    ax_line.plot(df["Description"], df["Total"], marker='o', linestyle='-', color='red')
    plt.xticks(rotation=0, ha='right')
    plt.ylabel("Total Price")
    plt.title("Invoice (Line Chart)",fontsize=16)
    plt.tight_layout()
    
    # Pie Chart
    fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
    if df["Total"].sum() > 0:
        ax_pie.pie(df["Total"], labels=df["Description"], autopct='%1.1f%%',
                   colors=['#ff9800', '#f44336', '#ffeb3b', '#9c27b0', '#673ab7'])
        plt.title("Invoice (Pie Chart)",fontsize=16)
        plt.tight_layout()
    else:
        fig_pie = None
    
    return fig_bar, fig_line, fig_pie


def process_invoice(image_path):
    # Extract data from invoice
    df = extract_invoice_data(image_path)
    # Save extracted data as CSV
    df.to_csv(r'C:\BFSI_OCR\data\invoice_data.csv', index=False)
    # Generate visualizations
    bar_chart, line_chart, pie_chart = generate_visualizations(df)
    
    return df, bar_chart, line_chart, pie_chart

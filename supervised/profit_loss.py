"""
Business Expense Extraction & Visualization

- Extracts text from expense images using OCR.
- Identifies and cleans expense categories and amounts.
- Generates pie and bar charts for expense distribution.
- Stores visualizations in memory for easy integration.
"""


import pytesseract
import cv2
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from io import BytesIO  
from PIL import Image
from typing import Dict, Tuple  
import os
import platform

# pytesseract.pytesseract.tesseract_cmd = r'C:\\Tesseract-OCR\\tesseract.exe'
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Tesseract-OCR\\tesseract.exe'
else:
    # For Linux/Streamlit Cloud environment
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Process the image
def process_image(image_file) -> Tuple[Dict[str, float], BytesIO, BytesIO]:
    # Read the uploaded image directly from the UploadedFile object
    image = Image.open(image_file)  
    ocr_text = perform_ocr(image)
    data = extract_expenses(ocr_text)
    # Create visualizations (return the chart to frontend)
    pie_chart, bar_chart = create_visualizations(data)
    return data, pie_chart, bar_chart

# Perform OCR on the image
def perform_ocr(image: Image.Image) -> str:
    image = np.array(image)  # Convert the PIL image to a numpy array for OpenCV
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    custom_config = r'--oem 3 --psm 6'
    ocr_text = pytesseract.image_to_string(thresh, config=custom_config)
    return ocr_text

# Extract expenses from OCR text
def extract_expenses(ocr_text: str) -> pd.DataFrame:
    lines = ocr_text.split("\n")
    data = []
    flag = False

    for line in lines:
        line = line.strip()
        if "Allowable Business Expenses" in line:
            flag = True
            continue
        if "TOTAL BUSINESS EXPENSES" in line:
            flag = False
            continue

        if flag and line:
            match = re.match(r"(.+?)\s+\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", line)  # Extract expense name and amount
            if match:
                category = match.group(1).strip()
                amount = match.group(2).replace(",", "")  # Remove commas for numeric values
                data.append([category, amount])  # Both are added to the list
    
    df = pd.DataFrame(data, columns=["Allowable Business Expenses", "Amount"])
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")  # Convert 'Amount' column to numeric
    df = df.dropna()
    
     # Save DataFrame to a CSV file in a folder
    folder_path = r"C:\BFSI_OCR\data"  
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create folder if it doesn't exist
    
    csv_file_path = os.path.join(folder_path, "profit_loss_data.csv")  
    df.to_csv(csv_file_path, index=False)  


    return df

# Create pie and bar charts and return them as image buffers
def create_visualizations(df: pd.DataFrame) -> Tuple[BytesIO, BytesIO]:
    
    colors = [
        '#2E5A4E',  # Deep Forest Green
        '#437C6F',  # Medium Sea Green
        '#598C75',  # Sage Green
        '#6B4423',  # Deep Brown
        '#8B6B4F',  # Medium Brown
        '#A47551',  # Light Brown
        '#C49A6C'   # Pale Brown
    ]
    # Plot Pie Chart
    pie_buf = BytesIO()
    plt.figure(figsize=(8, 8))
    plt.pie(df["Amount"], labels=df["Allowable Business Expenses"], autopct="%1.1f%%", startangle=140,colors=colors)
    plt.title("Allowable Business Expenses",fontsize=16)
    plt.savefig(pie_buf, format='png')
    pie_buf.seek(0)# Reset buffer position to the beginning
    plt.close()

    # Plot Bar Chart
    bar_buf = BytesIO()
    plt.figure(figsize=(8, 6)) 
    plt.bar(df["Allowable Business Expenses"], df["Amount"], color=colors[:len(df)])
    plt.xticks(rotation=45, ha='right', rotation_mode='anchor')  
    plt.tight_layout(pad=4.0)  
    plt.xlabel("Expense Categories", labelpad=15) 
    plt.ylabel("Amount ($)", labelpad=15)  
    plt.title("Allowable Business Expenses",fontsize=16)
    plt.savefig(bar_buf, format='png')
    bar_buf.seek(0)  # Reset buffer position to the beginning

    plt.close()  

    return pie_buf, bar_buf

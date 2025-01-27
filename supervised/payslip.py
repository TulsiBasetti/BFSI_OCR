"""
Payslip Earnings Extraction & Visualization

- Preprocesses image (grayscale, thresholding) for OCR.
- Extracts earnings categories and amounts using Tesseract OCR.
- Cleans and structures extracted data.
- Generates bar and pie charts for earnings distribution.
- Stores visualizations in memory buffers for easy integration.
"""

import os
import pytesseract
import cv2
import numpy as np
import re
import matplotlib.pyplot as plt
from typing import Dict
from io import BytesIO
import pandas as pd

# Preprocess image for OCR
def preprocess_image(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshold

# Clean category text
def clean_category(category: str) -> str:
    category = re.sub(r'[|]', '', category)
    category = re.sub(r'\s+', ' ', category)#Replace multiple spaces with a single space
    return category.strip()

#Extract earnings data from payslip image
def extract_earnings(image_path: str) -> Dict[str, float]:
    processed_img = preprocess_image(image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_img, config=custom_config)
    lines = text.split('\n')
    earnings = {}
    flag = False
    earnings_keywords = {
        'Basic Salary',
        'House Rent Allowances',
        'Medical Allowances',
        'Conveyance Allowances',
        'Special Allowances',
        'Other Allowances'
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if 'Earnings' in line:
            flag = True
            continue
        elif 'Deductions' in line:
            flag = False
            continue

        if flag:
            amount_match = re.search(r'\b(\d+(?:\.\d{2})?)\b', line)
            if amount_match:
                amount = float(amount_match.group(1))
                category = line.split(amount_match.group(1))[0]
                category = clean_category(category)
                if any(keyword in category for keyword in earnings_keywords):
                    earnings[category] = amount

    return earnings

# Save earnings data to CSV
def save_earnings_to_csv(earnings: Dict[str, float], folder_path: str = r"C:\BFSI_OCR\data"):
    # Convert earnings dictionary to DataFrame
    df = pd.DataFrame(list(earnings.items()), columns=["Category", "Amount"])
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define CSV file path
    csv_file_path = os.path.join(folder_path, "payslip_data.csv")
    
    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

#Visualize
def visualize_earnings(earnings: Dict[str, float]) -> BytesIO:
    # Custom order for specific categories
    custom_order = ['Basic Salary','Special Allowance','House Rent Allowances', 'Conveyance Allowances', 'Medical Allowances']
    # Ensure the custom order categories appear first in the pie chart
    categories = [category for category in custom_order if category in earnings] + [category for category in earnings.keys() if category not in custom_order]
    amounts = [earnings.get(category, 0.0) for category in categories]
    
    colors = ['#FF9999', '#66B3FF', 'purple', '#FFCC99', '#FF6347', '#32CD32', '#FFD700', '#8A2BE2', '#FF4500', '#ADFF2F']

    # Bar Chart
    plt.figure(figsize=(10, 6))
    plt.bar(earnings.keys(), [earnings[key] for key in earnings], color='#ff9800')
    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.title('Earnings Distribution',fontsize=16)
    plt.tight_layout()
    # Save Bar Chart to a buffer
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    
    # Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', colors=colors, labeldistance=1.1, startangle=90)
    plt.title('Earnings Distribution', loc='center',fontsize=16)
    plt.tight_layout() 
    # Save Pie Chart to the same buffer
    img_buf_pie = BytesIO()
    plt.savefig(img_buf_pie, format='png')
    img_buf_pie.seek(0)
    plt.close()

    return img_buf, img_buf_pie

# Process the payslip
def process_payslip(image_path: str):
    earnings = extract_earnings(image_path)
    save_earnings_to_csv(earnings)
    bar_chart, pie_chart = visualize_earnings(earnings)
    return earnings, bar_chart, pie_chart

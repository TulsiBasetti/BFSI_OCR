"""
Payment Mode Distribution Visualization

- Load CSV: Loads transaction data from a CSV file.
- Data Preprocessing: Converts Transaction Date to datetime format.
- Grouping: Calculates the sum of amounts for each payment mode.
- Visualization: Generates a pie chart showing payment mode distribution by amount.
- Image Encoding: Saves the plot as a PNG image and encodes it in base64 for Streamlit display.
"""


import os
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def plot_payment_mode_distribution():
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    csv_file_path = os.path.join(current_dir, r"C:\BFSI_OCR\data\api_data.csv")  

    try:
        df = pd.read_csv(csv_file_path)  # Load the CSV file
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise  # Re-raise the error if the file is not found

    # Convert 'transactionDate' to datetime format 
    df["transactionDate"] = pd.to_datetime(df["transactionDate"], format="%d-%m-%Y")

     # Sum of amount for each payment mode
    payment_amounts = df.groupby("paymentMode")["amount"].sum() 

    # Pie chart for Payment Mode Distribution by Amount
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(payment_amounts, labels=payment_amounts.index, autopct="%1.1f%%", colors=["#FFC107", "#28A745", "#007BFF"])
    ax.set_title("Payment Mode Distribution by Amount",fontsize=16)
    # Save to a BytesIO object
    img_stream = io.BytesIO()
    fig.savefig(img_stream, format='png')
    img_stream.seek(0)
    # Encode to base64 for Streamlit display
    img_base64 = base64.b64encode(img_stream.getvalue()).decode()
    return img_base64

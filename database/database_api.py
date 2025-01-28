import os
from dotenv import load_dotenv
import pymysql
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Get database credentials
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
try:
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    print("Connected to MySQL successfully!")
except pymysql.MySQLError as e:
    print(f"Error: {e}")

# Read CSV
df = pd.read_csv(r"C:\BFSI_OCR\data\api_data.csv", dtype=str)
df = df.where(pd.notna(df), None)  

# Convert dates to proper datetime format
df['transactionDate'] = pd.to_datetime(df['transactionDate'], format='%d/%m/%Y', errors='coerce')
df['pstdDate'] = pd.to_datetime(df['pstdDate'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df['valueDate'] = pd.to_datetime(df['valueDate'], format='%d/%m/%Y', errors='coerce')
df['timeStamp'] = pd.to_datetime(df['timeStamp'], format='%H:%M:%S', errors='coerce')
df['entryDate'] = pd.to_datetime(df['entryDate'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

# SQL Insert Query (with 28 placeholders now)
sql = """INSERT INTO transactions (serialNumber, transactionDate, pstdDate, transactionParticulars, chqNumber, 
    valueDate, amount, drcr, balance, paymentMode, utrNumber, internalReferenceNumber,remittingBranch, remittingBankName, remittingAccountNumber, remittingAccountName, 
    remittingIFSC, benficiaryBranch, benficiaryName, benficiaryAccountNumber, benficiaryIFSC, 
    channel, timeStamp, remarks, transactionCurrencyCode, entryDate, referenceId, transactionIdentificationCode) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

# Inserting data
try:
    cursor = connection.cursor()
    cursor.executemany(sql, df.itertuples(index=False, name=None))  
    connection.commit()
    print("Data stored successfully!")
except pymysql.IntegrityError as e:
    print(f"Error: {e}")  # Handle duplicate entries
except pymysql.MySQLError as e:
    print(f"MySQL Error: {e}")  # Handle other MySQL errors

# Close the connection
cursor.close()
connection.close()

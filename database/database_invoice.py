import os
from dotenv import load_dotenv
import pymysql
import pandas as pd

# Load environment variables
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
    exit()

# Load CSV
df = pd.read_csv(r"C:\BFSI_OCR\data\invoice_data.csv", dtype=str)

# Check column names before stripping
print("Columns in CSV before stripping spaces:", df.columns)
df.columns = df.columns.str.strip().str.replace(" ", "_")  
print("Columns after stripping spaces:", df.columns)

# Replace empty strings with NaN and strip spaces from values
df.replace(r'^\s*$', None, regex=True, inplace=True)
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Handle NaN values
df.fillna(0, inplace=True)

# Convert to correct data types
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
df['Unit_Price'] = pd.to_numeric(df['Unit_Price'], errors='coerce').fillna(0)
df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0)

# Verify cleaned data
print("Final DataFrame before inserting:")
print(df)

# Prepare SQL query
sql = """INSERT INTO invoice (Description, Quantity, Unit_Price, Total) 
         VALUES (%s, %s, %s, %s)"""

# Insert data into MySQL
try:
    cursor = connection.cursor()
    cursor.executemany(sql, df[['Description', 'Quantity', 'Unit_Price', 'Total']].values.tolist())
    connection.commit()
    print("Data stored successfully!")
except pymysql.MySQLError as e:
    print(f"MySQL Error: {e}")
finally:
    cursor.close()
    connection.close()

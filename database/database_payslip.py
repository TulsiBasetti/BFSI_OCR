import os
from dotenv import load_dotenv
import pymysql

# Load environment variables from .env file
load_dotenv()

# Get database credentials
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
try:
    connection = pymysql.connect(host=DB_HOST,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)
    print("Connected to MySQL successfully!")
except pymysql.MySQLError as e:
    print(f"Error: {e}")


import pandas as pd 

cursor=connection.cursor()
df=pd.read_csv(r"C:\BFSI_OCR\data\payslip_data.csv" , dtype=str)
sql = """INSERT INTO payslips (Payslip_ID, Basic_Salary, Conveyance_Allowances, House_Rent_Allowances, Medical_Allowances, Special_Allowances) 
VALUES (%s, %s, %s, %s, %s, %s)"""

try:
    cursor.executemany(sql, df.itertuples(index=False, name=None))  
    connection.commit()
    print("Data stored successfully!")
except pymysql.IntegrityError as e:
    print(f"Error: {e}")
except pymysql.MySQLError as e:
    print(f"MySQL Error: {e}")

# Close the connection
cursor.close()
connection.close()

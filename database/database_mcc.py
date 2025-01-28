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
df=pd.read_csv(r"C:\BFSI_OCR\data\mcc_codes.csv" , dtype=str)

# Insert data into MySQL table
for index,row in df.iterrows():
    sql="INSERT INTO mcc_codes (MCC , Description) VALUES (%s,%s)"
    values=(row["MCC"], row["Description"])

    try:
        cursor.execute(sql,values)
    except pymysql.IntegrityError:
        print(f"Skipping duplicate MCC codes : {row["MCC"]}")

#Commit and Close the conection
connection.commit()
cursor.close()
connection.close()

print("Data store successfully")

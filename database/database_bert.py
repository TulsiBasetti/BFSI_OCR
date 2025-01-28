import os
import pymysql
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MySQL connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

try:
    connection = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    print("Connected to MySQL successfully!")
except pymysql.MySQLError as e:
    print(f" MySQL Connection Error: {e}")
    exit()

cursor = connection.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS unsupervised (
    Transaction_ID INT PRIMARY KEY,
    Description VARCHAR(255),
    Amount DECIMAL(10,2),
    Cluster_KMeans INT,
    Cluster_KMeans_Mapped INT
);
"""
cursor.execute(create_table_query)
connection.commit()

# Read CSV
csv_path = r"C:\BFSI_OCR\data\clustered_transactions.csv"
df = pd.read_csv(csv_path, dtype=str)

# Rename columns to match MySQL
df.columns = ["Transaction_ID", "Description", "Amount", "Cluster_KMeans", "Cluster_KMeans_Mapped"]

# Strip spaces and fill NaN values with "0"
df = df.map(lambda x: x.strip() if isinstance(x, str) else x).fillna("0")

# Convert data types
df["Transaction_ID"] = df["Transaction_ID"].astype(int)
df["Amount"] = df["Amount"].astype(float)
df["Cluster_KMeans"] = df["Cluster_KMeans"].astype(int)
df["Cluster_KMeans_Mapped"] = df["Cluster_KMeans_Mapped"].astype(int)

# SQL Query to insert data
sql = """
INSERT INTO unsupervised (Transaction_ID, Description, Amount, Cluster_KMeans, Cluster_KMeans_Mapped) 
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    Description=VALUES(Description), 
    Amount=VALUES(Amount), 
    Cluster_KMeans=VALUES(Cluster_KMeans), 
    Cluster_KMeans_Mapped=VALUES(Cluster_KMeans_Mapped);
"""

# Insert data into MySQL
try:
    cursor.executemany(sql, df.itertuples(index=False, name=None))
    connection.commit()
    print("Data stored successfully in MySQL!")
except pymysql.MySQLError as e:
    print(f" MySQL Error: {e}")

# Close connections
cursor.close()
connection.close()

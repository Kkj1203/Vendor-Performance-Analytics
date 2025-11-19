import sqlite3
import pandas as pd

# Connect to DB
conn = sqlite3.connect("inventory.db")

#LIST ALL TABLES
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)
print("Tables in DB:")
print(tables)
print("\nRow Count Per Table:")
for table in tables["name"]:
    count_df = pd.read_sql_query(f"SELECT COUNT(*) AS count FROM {table}", conn)
    print(f"{table}: {count_df['count'][0]} rows")

#CHECK vendor_sales_summary SHAPE
try:
    df = pd.read_sql_query("SELECT * FROM vendor_sales_summary LIMIT 5;", conn)
    print("\nFirst 5 rows of vendor_sales_summary:")
    print(df)
    
    full_df = pd.read_sql_query("SELECT * FROM vendor_sales_summary;", conn)
    print("\nRows:", full_df.shape[0])
    print("Columns:", full_df.shape[1])
except Exception as e:
    print("\nvendor_sales_summary does not exist yet.")
    print(e)

#checking for any inconsistensies
#Load summary table
df = pd.read_sql_query("SELECT * FROM vendor_sales_summary", conn)

#Check data types
print("\n--- DATA TYPES ---")
print(df.dtypes)

#Count missing values (NA)
print("\n--- MISSING VALUES ---")
print(df.isna().sum())
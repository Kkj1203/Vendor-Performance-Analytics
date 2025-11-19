import sqlite3
import pandas as pd

#Load summary table
conn = sqlite3.connect("inventory.db")
df = pd.read_sql_query("SELECT * FROM vendor_sales_summary", conn)

#Fill NA with 0 for numeric columns
numeric_cols = [
    "TotalPurchaseQuantity",
    "TotalPurchaseDollars",
    "TotalSalesQuantity",
    "TotalSalesDollars",
    "TotalSalesPrice",
    "TotalExciseTax",
    "FreightCost",
    "ActualPrice",
    "Volume",
    "PurchasePrice"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

#Convert Volume to float64
if "Volume" in df.columns:
    df["Volume"] = df["Volume"].astype("float64")

#Clean categorical columns using str.strip()
categorical_cols = ["VendorName", "Description"]
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

#Create additional columns
df["TotalGrossProfit"] = df["TotalSalesDollars"] - df["TotalPurchaseDollars"]
df["ProfitMargin"] = df.apply(
    lambda row: (row["TotalGrossProfit"] / row["TotalSalesDollars"] * 100)
    if row["TotalSalesDollars"] > 0 else 0,
    axis=1
)
df["StockTurnover"] = df.apply(
    lambda row: (row["TotalSalesQuantity"] / row["TotalPurchaseQuantity"])
    if row["TotalPurchaseQuantity"] > 0 else 0,
    axis=1
)
df["SalesToPurchaseRatio"] = df.apply(
    lambda row: (row["TotalSalesDollars"] / row["TotalPurchaseDollars"])
    if row["TotalPurchaseDollars"] > 0 else 0,
    axis=1
)

#Save cleaned and preprocessed table back to inventory.db
df.to_sql("vendor_sales_summary_cleaned", conn, if_exists="replace", index=False)
print("\nNew cleaned table saved as: vendor_sales_summary_cleaned")

#printing all the inventory.db contents
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'",conn)
print(tables)
print("_"*70)

#display the vendor_sales_summary_cleaned table upto 20 rows
df = pd.read_sql_query("SELECT * FROM vendor_sales_summary_cleaned LIMIT 20", conn)
print(df)
print("_"*70)

#display the vendor_sales_summary_cleaned table total count of ros and columns
df = pd.read_sql_query("SELECT * FROM vendor_sales_summary_cleaned", conn)
print("\nRows:", df.shape[0])
print("Columns:", df.shape[1])

conn.close()
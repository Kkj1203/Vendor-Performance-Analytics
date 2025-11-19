import pandas as pd
import os
from sqlalchemy import create_engine
import logging

# LOGGING SETUP (simple, clean)
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# DELETE OLD DB
'''this block deletes the inventory.db if it exists before so that a new one can be created'''
if os.path.exists("inventory.db"):
    os.remove("inventory.db")
    logging.info("Old inventory.db deleted.")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "csv_files")
#DATA_DIR = r"C:\Users\kkj\Desktop\data\csv_files" within my pc

engine = create_engine("sqlite:///inventory.db")

# INGEST FUNCTION
'''this function is used to ingest the csv files by combining them into a single inventory.db by ngesting row by row'''

def ingest_chunked(csv_file, table_name, chunksize=20000):
    logging.info(f"Starting ingestion for {csv_file} → {table_name}")
    print(f"\nLoading {csv_file} into table {table_name}")

    first_chunk = True
    for chunk in pd.read_csv(
        csv_file,
        chunksize=chunksize,
        sep=",",
        quotechar='"',
        engine="python"
    ):
        chunk.to_sql(
            table_name,
            con=engine,
            if_exists="replace" if first_chunk else "append",
            index=False
        )
        first_chunk = False
        logging.info(f"Inserted {len(chunk)} rows into {table_name}")
        print(f"Inserted {len(chunk)} rows...")

    logging.info(f"Completed ingestion for {table_name}")
    print(f"Completed table: {table_name}")

# MAIN
def main():
    logging.info("----- Starting Full Ingestion -----")

    files = {
        "begin_inventory.csv": "begin_inventory",
        "end_inventory.csv": "end_inventory",
        "purchase_prices.csv": "purchase_prices",
        "purchases.csv": "purchases",
        "sales.csv": "sales",
        "vendor_invoice.csv": "vendor_invoice"
    }

    for file, table in files.items():
        full_path = os.path.join(DATA_DIR, file)
        ingest_chunked(full_path, table)

    logging.info("----- Ingestion Complete -----")

if __name__ == "__main__":
    main()
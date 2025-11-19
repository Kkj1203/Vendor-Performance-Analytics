'''EDA helps us in understanding the dataset to explore how the data is present in the databse created 
and if there is some need of creating an aggregated tables that can help with : 
-Vendor selection for profitability
-Product Pricing Optimization'''

import sqlite3
import pandas as pd

DB_PATH = "inventory.db"

def show_table_info(cursor, table_name):
    print("\n\n" + "="*80)
    print(f"TABLE: {table_name}")
    print("="*80)

    # Column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cursor.fetchall()]
    print(f"Columns: {cols}")

    # Total rows and columns count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cursor.fetchone()[0]
    print(f"Total Rows: {total_rows}")
    print(f"Total Columns: {len(cols)}")

    # First 5 rows
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
    print("\nFirst 5 Rows:")
    print(df)

    print("="*80)


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]

    print("Tables found:", tables)

    for table in tables:
        show_table_info(cursor, table)

    conn.close()

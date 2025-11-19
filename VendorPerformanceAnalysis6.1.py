import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD DATA
conn = sqlite3.connect("inventory.db")
df = pd.read_sql_query("SELECT * FROM vendor_sales_summary_cleaned", conn)
conn.close()
print("Loaded. Shape:", df.shape)
print(df.head())

# 2. SUMMARY STATISTICS
print("\n--- Data Types ---")
print(df.dtypes)
print("\n--- Summary Statistics ---")
print(df.describe(include="all"))

# 3. NUMERICAL COLUMNS
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
print("\nNumerical columns:", num_cols)
n = len(num_cols)
rows = (n // 3) + 1

# 4. HISTOGRAMS OF ALL NUMERIC COLUMNS
sns.set(style="whitegrid")
fig, axes = plt.subplots(rows, 3, figsize=(18, rows * 4))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    sns.histplot(df[col], kde=True, ax=axes[i])
    axes[i].set_title(col)
plt.tight_layout()
plt.show()

# 5. BOXPLOTS FOR OUTLIERS
fig, axes = plt.subplots(rows, 3, figsize=(18, rows * 4))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    sns.boxplot(x=df[col], ax=axes[i])
    axes[i].set_title(col)
plt.tight_layout()
plt.show()

# 6. FILTERING PROFITABLE & RELEVANT VENDORS
df_filtered = df[
    (df["TotalGrossProfit"] > 0) &
    (df["ProfitMargin"] > 0) &
    (df["TotalSalesQuantity"] > 0)
]
print("\nFiltered shape:", df_filtered.shape)

# 7. FILTERED HISTOGRAMS
fig, axes = plt.subplots(rows, 3, figsize=(18, rows * 4))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    sns.histplot(df_filtered[col], kde=True, ax=axes[i])
    axes[i].set_title(col)
plt.tight_layout()
plt.show()

# 8. FILTERED BOXPLOTS
fig, axes = plt.subplots(rows, 3, figsize=(18, rows * 4))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    sns.boxplot(x=df_filtered[col], ax=axes[i])
    axes[i].set_title(col)
plt.tight_layout()
plt.show()

# 9. TOP 10 VENDORS (COUNT PLOT)
print("Top 10 vendors...")
top_vendors = df["VendorName"].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_vendors.values, y=top_vendors.index)
plt.title("Top 10 Vendors by Frequency")
plt.xlabel("Count")
plt.ylabel("Vendor Name")
plt.show()

# 10. TOP 10 PRODUCTS
print("Top 10 products...")
top_products = df["Description"].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_products.values, y=top_products.index)
plt.title("Top 10 Products by Frequency")
plt.xlabel("Count")
plt.ylabel("Description")
plt.show()

# 11. CORRELATION HEATMAP
plt.figure(figsize=(12, 8))
sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
print("\nAnalysis completed.")
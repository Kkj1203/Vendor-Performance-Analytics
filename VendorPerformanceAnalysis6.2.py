import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, sem, t
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
DB = "inventory.db"

# LOAD TABLE
def load_table():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM vendor_sales_summary_cleaned", conn)
    conn.close()
    # Numeric cleaning
    num_cols = [
        "TotalPurchaseQuantity", "TotalPurchaseDollars", "TotalSalesQuantity",
        "TotalSalesDollars", "TotalSalesPrice", "TotalExciseTax",
        "FreightCost", "ActualPrice", "Volume", "PurchasePrice",
        "TotalGrossProfit", "ProfitMargin", "StockTurnover", "SalesToPurchaseRatio"
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    if "VendorName" in df.columns:
        df["VendorName"] = df["VendorName"].astype(str).str.strip()
    return df

# BUSINESS ANALYSIS FUNCTIONS
def brands_need_promo(df):
    sales_median = df["TotalSalesDollars"].median()
    margin_median = df["ProfitMargin"].median()
    candidates = df[(df["TotalSalesDollars"] < sales_median) &(df["ProfitMargin"] > margin_median)]
    print("\n--- Brands Needing Promo (low sales, high margin) ---")
    print(candidates[["VendorName", "Brand", "Description","TotalSalesDollars", "ProfitMargin"]].head(20))
    return candidates

def top10_brands_by_sales_plot(df):
    top10 = (df.groupby(["Brand", "Description"], as_index=False)
             ["TotalSalesDollars"].sum()
             .sort_values("TotalSalesDollars", ascending=False)
             .head(10))
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="TotalSalesDollars", y="Description", data=top10, ax=ax)
    for p in ax.patches:
        val = p.get_width()
        ax.text(val + 1e-6, p.get_y() + p.get_height()/2,
                f"{val/1e6:.2f}M", va="center")
    plt.tight_layout()
    plt.show()
    return top10

def vendor_top10_purchase_contrib(df):
    vendor_sum = df.groupby("VendorName", as_index=False)["TotalPurchaseDollars"].sum()
    vendor_sum.sort_values("TotalPurchaseDollars", ascending=False, inplace=True)
    vendor_sum["Pct"] = 100 * vendor_sum["TotalPurchaseDollars"] / vendor_sum["TotalPurchaseDollars"].sum()
    top10 = vendor_sum.head(10).copy()
    top10["CumPct"] = top10["Pct"].cumsum()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Pct", y="VendorName", data=top10, ax=ax)
    for p in ax.patches:
        ax.text(p.get_width() + 0.2,
                p.get_y() + p.get_height()/2,
                f"{p.get_width():.2f}%", va="center")
    ax2 = ax.twiny()
    ax2.plot(top10["CumPct"], np.arange(len(top10)) + 0.5,
             marker="o", color="C1")
    plt.tight_layout()
    plt.show()
    print(f"\nTop vendor contributes {top10.iloc[0]['Pct']:.2f}%")
    return top10

def donut_top10_vendor_share(df):
    vendor_sum = df.groupby("VendorName", as_index=False)["TotalPurchaseDollars"].sum()
    vendor_sum.sort_values("TotalPurchaseDollars", ascending=False, inplace=True)
    top10 = vendor_sum.head(10)
    others = vendor_sum["TotalPurchaseDollars"].sum() - top10["TotalPurchaseDollars"].sum()
    labels = top10["VendorName"].tolist() + ["Others"]
    sizes = top10["TotalPurchaseDollars"].tolist() + [others]
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, _, autotexts = ax.pie(
        sizes, labels=labels, autopct=lambda p: f"{p:.1f}%", startangle=90)
    centre_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig.gca().add_artist(centre_circle)
    plt.tight_layout()
    plt.show()


def bulk_purchase_effect(df):
    df_q = df.copy()
    df_q["QtyQuantile"] = pd.qcut(df_q["TotalPurchaseQuantity"].rank(method="first"),q=3, labels=["Small", "Medium", "Large"])
    print("\nMean purchase price by quantile:")
    print(df_q.groupby("QtyQuantile")["PurchasePrice"].mean())
    sns.boxplot(x="QtyQuantile", y="PurchasePrice", data=df_q)
    plt.tight_layout()
    plt.show()

def low_inventory_turnover(df):
    low_turn = df.sort_values("StockTurnover").head(10)
    print("\n--- Low Inventory Turnover (Top 10) ---")
    print(low_turn[["VendorName", "Brand", "Description","StockTurnover", "TotalPurchaseQuantity", "TotalSalesQuantity"]])
    return low_turn

def unsold_inventory_value(df):
    df2 = df.copy()
    df2["UnsoldQty"] = (df2["TotalPurchaseQuantity"] - df2["TotalSalesQuantity"]).clip(lower=0)
    df2["UnitCost"] = np.where(df2["PurchasePrice"] > 0,df2["PurchasePrice"], df2["ActualPrice"])
    df2["UnsoldValue"] = df2["UnsoldQty"] * df2["UnitCost"]
    vendor_unsold = df2.groupby("VendorName", as_index=False)["UnsoldValue"].sum()
    vendor_unsold.sort_values("UnsoldValue", ascending=False, inplace=True)
    print("\nTop vendors by unsold inventory:")
    print(vendor_unsold.head(10))
    return vendor_unsold

# 95% CI HISTOGRAMS
def ci_and_histograms(df):
    q75 = np.percentile(df["ProfitMargin"], 75)
    q25 = np.percentile(df["ProfitMargin"], 25)
    top_group = df[df["ProfitMargin"] >= q75]["ProfitMargin"]
    low_group = df[df["ProfitMargin"] <= q25]["ProfitMargin"]
    def ci95(x):
        n = len(x)
        m = np.mean(x)
        s = sem(x)
        tval = t.ppf(0.975, n - 1)
        return (m - tval*s, m + tval*s, m)
    top_ci = ci95(top_group)
    low_ci = ci95(low_group)
    print("\nTop group CI:", top_ci)
    print("Low group CI:", low_ci)
    plt.figure(figsize=(10, 6))
    sns.histplot(top_group, color="C0", label="Top", stat="density")
    sns.histplot(low_group, color="C1", label="Low", stat="density")
    plt.legend()
    plt.tight_layout()
    plt.show()
    return top_group, low_group

# FIXED: PROPER HYPOTHESIS TEST FUNCTION
def hypothesis_test(df):
    top_threshold = df["TotalSalesDollars"].quantile(0.75)
    low_threshold = df["TotalSalesDollars"].quantile(0.25)
    top_vendors = df[df["TotalSalesDollars"] >= top_threshold]["ProfitMargin"]
    low_vendors = df[df["TotalSalesDollars"] <= low_threshold]["ProfitMargin"]
    t_stat, p_value = ttest_ind(top_vendors, low_vendors, equal_var=False)
    print(f"\nT-stat: {t_stat:.4f}, p-val: {p_value:.4f}")
    if p_value < 0.05:
        print("Reject H0: Significant difference in profit margins.")
    else:
        print("Fail to reject H0.")
    return t_stat, p_value

# MAIN
def main():
    df = load_table()

    brands_need_promo(df)
    top10_brands_by_sales_plot(df)
    vendor_top10_purchase_contrib(df)
    donut_top10_vendor_share(df)
    bulk_purchase_effect(df)
    low_inventory_turnover(df)
    unsold_inventory_value(df)
    top_group, low_group = ci_and_histograms(df)
    hypothesis_test(df)
    print("\nAll analysis complete.")

if __name__ == "__main__":
    main()
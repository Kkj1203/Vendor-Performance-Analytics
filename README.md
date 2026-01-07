Vendor Performance & Sales Analytics Pipeline
📌 Project Overview
This project implements a complete end-to-end data analytics pipeline for vendor-level sales, purchase, and profitability analysis.
It starts from raw CSV ingestion, builds a relational SQLite database, creates a consolidated analytical summary table, performs extensive EDA and statistical analysis in Python, and finally prepares the data for Power BI visualisation and business decision-making.
The project is designed to simulate a real-world data engineering + analytics workflow, emphasizing scalability, data quality, and business relevance.

🧩 Business Objectives
The analysis aims to answer key business questions such as:
Which vendors and brands generate the highest sales and profitability?
Which products require promotional or pricing adjustments?
How dependent is procurement on top vendors?
Does bulk purchasing reduce unit costs, and what is the optimal purchase volume?
Which vendors have low inventory turnover indicating excess stock?
How much capital is locked in unsold inventory?
Is there a statistically significant difference in profit margins between top- and low-performing vendors?

📂 Project Structure
.
├── IngestionScript1.py              # Chunk-based CSV ingestion with logging
├── ExploratoryDataAnalysis2.py      # Table-level EDA on SQLite DB
├── CleaningPreprocessing5.py        # Cleaning, type casting, feature engineering
├── SummaryTable3.py                 # SQL-based vendor sales summary creation
├── VendorPerformanceAnalysis6.1.py  # Initial vendor analytics & plots
├── VendorPerformanceAnalysis6.2.py  # Advanced analytics, CI & hypothesis testing
│
├── inventory.db                     # SQLite database (generated)
├── logs/                            # Ingestion logs
├── PowerBI/                         # Power BI dashboards & assets
├── plots.6.1/                       # Saved plots (version 6.1)
├── plots.6.2/                       # Saved plots (version 6.2)
└── notes/                           # Project notes & references

🗃️ Data Sources
Raw CSV files ingested into the database:
begin_inventory.csv
end_inventory.csv
purchase_prices.csv
purchases.csv
sales.csv
vendor_invoice.csv

These datasets together represent inventory levels, purchase transactions, sales transactions, pricing, and freight costs.

🛠️ Technology Stack
Python 3.13
SQLite (local analytical database)
Pandas, NumPy – data manipulation
SQLAlchemy – database interaction
Matplotlib, Seaborn – visualisation
SciPy – statistical analysis
Power BI – business dashboards

🚀 Execution Flow (Recommended Order)
Step 1 — Data Ingestion
python IngestionScript1.py

Ingests CSVs in chunks
Creates inventory.db
Logs ingestion progress

Step 2 — Exploratory Data Analysis
python ExploratoryDataAnalysis2.py

Lists tables
Displays schema, row counts, and sample records

Step 3 — Data Cleaning & Feature Engineering
python CleaningPreprocessing5.py

Actions performed:
Handle missing values
Convert numeric & categorical data types
Trim unwanted spaces
Create derived metrics:
TotalGrossProfit
ProfitMargin
StockTurnover
SalesToPurchaseRatio

Output:
vendor_sales_summary_cleaned table

Step 4 — Summary Table Creation
python SummaryTable3.py

Creates a consolidated vendor_sales_summary table using SQL CTEs combining:
Purchase data
Sales data
Freight costs
Actual product prices

Step 5 — Vendor Performance Analytics
python VendorPerformanceAnalysis6.2.py

Includes:
Summary statistics
Histograms & boxplots (subplots for multiple metrics)
Vendor & brand ranking
Cumulative contribution analysis
Donut charts
Inventory turnover analysis
Unsold inventory valuation
95% confidence intervals
Two-sample Welch’s t-test on profit margins

📊 Power BI Integration

Data Source Options
Load vendor_sales_summary_cleaned.csv (exported)
Or connect directly to inventory.db via SQLite ODBC

Pre-Applied Filters
TotalSalesQuantity > 0
TotalGrossProfit > 0
ProfitMargin > 0

Dashboards include:
Top vendors & brands
Procurement dependency
Profitability vs sales analysis
Inventory risk indicators

📈 Key Analytical Outputs
Top 10 vendors by sales and purchase value
Cumulative contribution analysis
Bulk purchase cost optimization insights
Inventory turnover risk detection
Statistical validation of vendor performance differences

🧪 Statistical Testing
Hypothesis Tested
H₀: No significant difference in profit margins between top and low-performing vendors
H₁: Significant difference exists

Method:
Welch’s Two-Sample t-test
Significance level: α = 0.05
Result interpretation printed directly in the console.

✅ Project Highlights
Realistic data volume handling (chunked ingestion)
SQL + Python hybrid analytics
End-to-end reproducibility
Business-oriented insights
Production-style logging & modular scripts

📌 Future Enhancements
Automated ETL scheduling
Migration to PostgreSQL / cloud warehouse
Advanced forecasting models
Power BI incremental refresh
Vendor risk scoring model

👤 Author
Keerthikrishna Jog
Computer Science Engineering
Data Analytics & Machine Learning Enthusiast

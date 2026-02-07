# 🏗️ Olist E-commerce ETL Pipeline (Data Engineering Project)

## 📌 Project Overview

This project demonstrates a **Data Engineering ETL pipeline** built on top of the
**Olist Brazilian E-commerce Dataset**.

The main objective is to design and implement an end-to-end pipeline that:
- Extracts raw CSV data
- Cleans and validates data
- Loads structured data into a relational database
- Produces analytics-ready tables for downstream analysis

The project emphasizes **data pipeline design, schema consistency, and reproducibility**
rather than purely exploratory analysis.

---

## 🎯 Project Goals

- Build a reusable and idempotent ETL pipeline
- Separate concerns between extract, transform, and load stages
- Enforce basic data quality checks and schema validation
- Prepare fact tables suitable for analytical SQL queries

---

## 📊 Dataset

**Olist Brazilian E-commerce Dataset**

Source tables used:
- `olist_customers_dataset`
- `olist_orders_dataset`
- `olist_order_items_dataset`
- `olist_order_payments_dataset`
- `olist_order_reviews_dataset`
- `olist_products_dataset`
- `olist_sellers_dataset`
- `product_category_name_translation`

The dataset represents real-world transactional data from a Brazilian online marketplace
and contains multiple relational dependencies (primary and foreign keys).

---

## 🧱 Project Architecture

```
Raw CSV files
     ↓
Extract (pandas)
     ↓
Transform (cleaning, validation, enrichment)
     ↓
Load (SQLite)
     ↓
Analytics-ready tables
```

---

## 📁 Project Structure

```text
olist-etl-pipeline/
├── data/
│   ├── raw/                    # Original CSV datasets
│   └── processed/              # Generated SQLite database
├── etl/
│   ├── extract.py              # Data ingestion from CSV
│   ├── transform.py            # Data cleaning and feature engineering
│   ├── load.py                 # Load cleaned data into database
│   ├── validate.py             # Data quality checks
│   └── logger.py               # Centralized logging
├── db/
│   ├── schema.sql              # Database schema definitions
│   └── init_db.py              # Database initialization
├── config/
│   └── config.yaml             # Paths and table configuration
├── logs/
│   └── etl.log                 # ETL execution logs
├── main.py                     # Pipeline entry point
├── requirements.txt
└── README.md
```

---

## 🔄 ETL Pipeline Details

### 1. Extract
- Reads raw CSV files using pandas
- Performs no mutation at this stage
- Fails fast if any required file is missing

### 2. Transform
- Removes duplicate records
- Converts timestamps into a standardized ISO format
- Sanitizes numeric fields
- Enforces basic data validation rules
- Builds an analytics-ready fact table:
  - `fact_order_item_sales`

### 3. Load
- Initializes database schema using SQL
- Loads cleaned data into SQLite
- Supports repeatable execution (pipeline can be rerun safely)

---

## 📈 Fact Table Example

**fact_order_item_sales**
- order_id
- order_item_id
- seller_id
- product_id
- product_category_name_english
- order_purchase_timestamp
- price
- freight_value
- revenue

This table is designed specifically for analytical queries such as:
- Revenue by category
- Revenue trends over time
- Seller and product performance

---

## ▶ How to Run

### 1. Create environment
```bash
conda create -n olist-etl python=3.11 -y
conda activate olist-etl
pip install -r requirements.txt
```

### 2. Place raw data
Copy all dataset CSV files into:
```
data/raw/
```

### 3. Run ETL pipeline
```bash
python main.py
```

After execution, the SQLite database will be available at:
```
data/processed/olist.db
```

---

## 🧪 Example SQL Query

```sql
SELECT
  product_category_name_english,
  ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_order_item_sales
GROUP BY 1
ORDER BY total_revenue DESC
LIMIT 10;
```

---

## 🤖 Use of AI Assistance

AI tools (including large language models) were used as a **development aid** for:
- Structuring the ETL workflow
- Reviewing schema design
- Improving code organization and readability
- Debugging and refining pipeline logic

All architectural decisions, validation logic, and final implementations were
**reviewed, understood, and manually integrated** by the author.

AI was used as a productivity and learning tool, not as a replacement for
data engineering decision-making.

---

## 🚀 Future Improvements

- Incremental loading strategy
- Migration to PostgreSQL
- Orchestration using Airflow
- Advanced data quality checks
- CI/CD integration for pipeline testing

---

## 👤 Author

Bright  
Computer Engineering Student  

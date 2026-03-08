# Olist E-commerce ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green)
![SQL](https://img.shields.io/badge/SQL-SQLite-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![ETL](https://img.shields.io/badge/Data%20Engineering-ETL-blueviolet)

## Project Overview

This project implements an end-to-end **ETL (Extract, Transform, Load) pipeline** on top of the **Olist Brazilian E-commerce dataset**.

The pipeline reads raw CSV files, cleans and standardizes selected fields, creates a fact table for analytics, and loads the processed data into a **SQLite** database. The project is designed to demonstrate core **data engineering practices** such as modular pipeline design, reproducible execution, schema-driven loading, and basic data quality validation.

---

## Objectives

- Extract multiple relational CSV files from the Olist dataset
- Clean and standardize raw transactional data
- Load structured tables into SQLite using a predefined schema
- Build an analytics-ready fact table for SQL analysis
- Apply basic validation checks for data consistency

---

## Dataset

This repository uses **8 raw CSV files** stored in `data/raw/`:

- `olist_customers_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

These files represent a relational e-commerce dataset containing customers, orders, products, sellers, payments, reviews, and category translation data.

---

## Architecture

```text
           Raw CSV files
                │
                ▼
        +----------------+
        |    Extract     |
        | read_csv()     |
        +----------------+
                │
                ▼
        +----------------+
        |   Transform    |
        | deduplicate    |
        | type cleaning  |
        | datetime clean |
        +----------------+
                │
                ▼
        +----------------+
        |   Validate     |
        | PK null checks |
        | FK checks      |
        | non-negative   |
        +----------------+
                │
                ▼
        +----------------+
        |     Load       |
        | SQLite schema  |
        | append tables  |
        +----------------+
                │
                ▼
        Analytics-ready database
```

---

## Tech Stack

- **Python 3.11**
- **Pandas**
- **NumPy**
- **PyYAML**
- **SQLite**
- **SQLAlchemy** (listed in dependencies)

---

## Repository Structure

```text
olist-etl-pipeline-main/
├── config/
│   └── config.yaml              # Paths and source file mapping
├── data/
│   └── raw/                     # Raw Olist CSV files
├── db/
│   ├── init_db.py               # Initializes SQLite database from schema
│   └── schema.sql               # Table definitions
├── etl/
│   ├── extract.py               # Reads CSV files into pandas DataFrames
│   ├── transform.py             # Cleans data and builds fact table
│   ├── load.py                  # Loads cleaned tables into SQLite
│   ├── validate.py              # Basic validation checks
│   └── logger.py                # File + console logging
├── logs/
│   └── etl.log                  # Generated at runtime
├── main.py                      # Pipeline entry point
├── requirements.txt
└── README.md
```

---

## ETL Workflow

### 1. Extract
The pipeline reads all required CSV files defined in `config/config.yaml`.

Source-to-key mapping used by the pipeline:

- `customers` → `olist_customers_dataset.csv`
- `orders` → `olist_orders_dataset.csv`
- `order_items` → `olist_order_items_dataset.csv`
- `order_payments` → `olist_order_payments_dataset.csv`
- `order_reviews` → `olist_order_reviews_dataset.csv`
- `products` → `olist_products_dataset.csv`
- `sellers` → `olist_sellers_dataset.csv`
- `category_translation` → `product_category_name_translation.csv`

If any required file is missing, the pipeline raises a `FileNotFoundError`.

### 2. Transform
The transformation step performs the following operations:

- Removes duplicates from source tables using table-specific keys
- Converts datetime columns to `YYYY-MM-DD HH:MM:SS`
- Converts numeric columns such as `price`, `freight_value`, and `payment_value`
- Preserves cleaned versions of source tables
- Builds an analytics-ready fact table named `fact_order_item_sales`

### 3. Validate
The validation step checks:

- `customer_id` in `customers` is not null
- `order_id` in `orders` is not null
- all `orders.customer_id` values exist in `customers`
- `price` and `freight_value` in `order_items` are not negative

### 4. Load
The pipeline:

- initializes the SQLite database from `db/schema.sql`
- clears existing table contents in a dependency-safe order
- inserts cleaned tables into SQLite
- writes the output database to `data/processed/olist.db`

---

## Output Tables

The database schema includes cleaned relational tables:

- `customers`
- `orders`
- `order_items`
- `order_payments`
- `order_reviews`
- `products`
- `sellers`
- `category_translation`

It also includes one analytics table:

- `fact_order_item_sales`

### fact_order_item_sales columns

- `order_id`
- `order_item_id`
- `seller_id`
- `product_id`
- `product_category_name_english`
- `order_purchase_timestamp`
- `price`
- `freight_value`
- `revenue`

`revenue` is computed as:

```text
price + freight_value
```

This fact table is created by joining:

- `order_items`
- `orders`
- `products`
- `category_translation`

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Make sure raw files exist in:

```text
data/raw/
```

### 3. Run the pipeline

```bash
python main.py
```

### 4. Output
After a successful run:

- database file: `data/processed/olist.db`
- log file: `logs/etl.log`

---

## Example SQL Query

```sql
SELECT
    product_category_name_english,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_order_item_sales
GROUP BY product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;
```

---

## Skills Demonstrated

- ETL pipeline design
- Relational data handling
- Data cleaning with pandas
- Schema-based loading into SQLite
- Basic data quality validation
- Fact table construction for analytics
- Project organization for maintainability

---

## Notes

- The pipeline is **rerunnable** because tables are cleared before each load.
- Logging is written to both the console and `logs/etl.log`.
- Validation currently covers a small set of core checks and can be extended further.

---

## Future Improvements

- Add unit tests for each ETL stage
- Add stronger schema and null validation
- Add incremental loading support
- Migrate storage from SQLite to PostgreSQL
- Add orchestration with Airflow or Prefect

---

## Author

**Bright**  
Computer Engineering Student

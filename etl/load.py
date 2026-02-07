from __future__ import annotations
import sqlite3
import pandas as pd
from typing import Dict

def load_to_sqlite(db_path: str, cleaned: Dict[str, pd.DataFrame]) -> None:
    con = sqlite3.connect(db_path)
    try:
        con.execute("PRAGMA foreign_keys = ON;")
        cur = con.cursor()

        # delete order matters because of FK
        delete_order = [
            "order_items",
            "order_payments",
            "order_reviews",
            "orders",
            "customers",
            "products",
            "sellers",
            "category_translation",
            "fact_order_item_sales",
        ]
        for t in delete_order:
            cur.execute(f"DELETE FROM {t};")
        con.commit()

        # insert order: parents first
        insert_order = [
            "customers",
            "products",
            "sellers",
            "category_translation",
            "orders",
            "order_items",
            "order_payments",
            "order_reviews",
            "fact_order_item_sales",
        ]

        for t in insert_order:
            cleaned[t].to_sql(t, con, if_exists="append", index=False)

        con.commit()
    finally:
        con.close()

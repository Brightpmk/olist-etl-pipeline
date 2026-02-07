from __future__ import annotations
import pandas as pd


def _to_iso_datetime(series: pd.Series) -> pd.Series:
    dt = pd.to_datetime(series, errors="coerce")
    return dt.dt.strftime("%Y-%m-%d %H:%M:%S")


def build_fact_order_item_sales(cleaned: dict):
    oi = cleaned["order_items"][
        [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "price",
            "freight_value",
        ]
    ]

    o = cleaned["orders"][
        ["order_id", "order_purchase_timestamp"]
    ]

    p = cleaned["products"][
        ["product_id", "product_category_name"]
    ]

    ct = cleaned["category_translation"]

    df = (
        oi.merge(o, on="order_id", how="left")
          .merge(p, on="product_id", how="left")
          .merge(ct, on="product_category_name", how="left")
    )

    df = df.rename(
        columns={"product_category_name_english": "product_category_name_english"}
    )

    df["revenue"] = df["price"] + df["freight_value"]

    # 🔑 เลือก column ให้ตรง schema
    df = df[
        [
            "order_id",
            "order_item_id",
            "seller_id",
            "product_id",
            "product_category_name_english",
            "order_purchase_timestamp",
            "price",
            "freight_value",
            "revenue",
        ]
    ]

    return df



def transform(dfs: dict) -> dict:
    out = {}

    # customers
    c = dfs["customers"].copy().drop_duplicates(subset=["customer_id"])
    out["customers"] = c

    # orders
    o = dfs["orders"].copy().drop_duplicates(subset=["order_id"])
    for col in [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]:
        if col in o.columns:
            o[col] = _to_iso_datetime(o[col])
    out["orders"] = o

    # products
    p = dfs["products"].copy().drop_duplicates(subset=["product_id"])
    out["products"] = p

    # sellers
    s = dfs["sellers"].copy().drop_duplicates(subset=["seller_id"])
    out["sellers"] = s

    # order_items
    oi = dfs["order_items"].copy().drop_duplicates(
        subset=["order_id", "order_item_id"]
    )
    for col in ["price", "freight_value"]:
        if col in oi.columns:
            oi[col] = pd.to_numeric(oi[col], errors="coerce")
    if "shipping_limit_date" in oi.columns:
        oi["shipping_limit_date"] = _to_iso_datetime(oi["shipping_limit_date"])
    out["order_items"] = oi

    # order_payments
    pay = dfs["order_payments"].copy().drop_duplicates(
        subset=["order_id", "payment_sequential"]
    )
    if "payment_value" in pay.columns:
        pay["payment_value"] = pd.to_numeric(pay["payment_value"], errors="coerce")
    out["order_payments"] = pay

    # order_reviews
    rv = dfs["order_reviews"].copy().drop_duplicates(subset=["review_id"])
    for col in ["review_creation_date", "review_answer_timestamp"]:
        if col in rv.columns:
            rv[col] = _to_iso_datetime(rv[col])
    out["order_reviews"] = rv

    # category_translation
    ct = dfs["category_translation"].copy().drop_duplicates(
        subset=["product_category_name"]
    )
    out["category_translation"] = ct

    # fact table
    out["fact_order_item_sales"] = build_fact_order_item_sales(out)

    return out

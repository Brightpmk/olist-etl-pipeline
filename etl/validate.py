def validate(cleaned: dict) -> None:
    # 1. PK not null
    assert cleaned["customers"]["customer_id"].isna().sum() == 0
    assert cleaned["orders"]["order_id"].isna().sum() == 0

    # 2. FK consistency
    order_customers = set(cleaned["orders"]["customer_id"])
    customers = set(cleaned["customers"]["customer_id"])
    missing = order_customers - customers
    assert len(missing) == 0, f"Missing customers for orders: {len(missing)}"

    # 3. No negative values
    assert (cleaned["order_items"]["price"] < 0).sum() == 0
    assert (cleaned["order_items"]["freight_value"] < 0).sum() == 0

"""
Modular Data Ingestion, Quality Validation, and Cleaning Pipeline
Project 1: E-commerce Delivery & Logistics Performance Analysis
Week 1 Implementation
"""

import os
import sqlite3
import pandas as pd
import numpy as np


def run_pipeline(project_dir: str):
    raw_dir = os.path.join(project_dir, "data", "raw")
    interim_dir = os.path.join(project_dir, "data", "interim")
    os.makedirs(interim_dir, exist_ok=True)
    db_path = os.path.join(interim_dir, "logistics.db")

    print("[1/5] Ingesting raw CSV files into SQLite database...")
    conn = sqlite3.connect(db_path)

    # Ingest tables
    tables = {
        "raw_orders": "olist_orders_dataset.csv",
        "raw_order_items": "olist_order_items_dataset.csv",
        "raw_order_reviews": "olist_order_reviews_dataset.csv",
        "raw_customers": "olist_customers_dataset.csv",
        "raw_sellers": "olist_sellers_dataset.csv",
        "raw_products": "olist_products_dataset.csv",
        "raw_payments": "olist_order_payments_dataset.csv",
        "raw_category_translation": "product_category_name_translation.csv"
    }

    loaded_dfs = {}
    for table_name, file_name in tables.items():
        file_path = os.path.join(raw_dir, file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            loaded_dfs[table_name] = df
            print(f"  ✓ Loaded {table_name}: {len(df):,} rows")
        else:
            print(f"  ✗ Warning: {file_path} not found")

    print("\n[2/5] Parsing datetime columns and executing data-quality checks...")
    orders = loaded_dfs["raw_orders"].copy()
    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col])

    # Quality Flags
    carrier_before_purchase = orders["order_delivered_carrier_date"] < orders["order_purchase_timestamp"]
    customer_before_carrier = orders["order_delivered_customer_date"] < orders["order_delivered_carrier_date"]
    
    orders["has_invalid_timestamps"] = (carrier_before_purchase | customer_before_carrier).fillna(False)
    orders["is_delivered"] = (orders["order_status"] == "delivered")
    orders["is_canceled"] = orders["order_status"].isin(["canceled", "unavailable"])
    
    orders["is_valid_delivered"] = (
        orders["is_delivered"] & 
        orders["order_delivered_customer_date"].notnull() & 
        orders["order_delivered_carrier_date"].notnull()
    )
    
    orders["is_eligible_otd"] = orders["is_valid_delivered"] & (~orders["has_invalid_timestamps"])

    # Duration metrics (in fractional days)
    orders["order_processing_time_days"] = np.where(
        ~orders["has_invalid_timestamps"] & orders["order_delivered_carrier_date"].notnull(),
        (orders["order_delivered_carrier_date"] - orders["order_purchase_timestamp"]).dt.total_seconds() / 86400.0,
        np.nan
    )

    orders["carrier_transit_time_days"] = np.where(
        ~orders["has_invalid_timestamps"] & orders["is_valid_delivered"],
        (orders["order_delivered_customer_date"] - orders["order_delivered_carrier_date"]).dt.total_seconds() / 86400.0,
        np.nan
    )

    orders["total_delivery_duration_days"] = np.where(
        orders["is_valid_delivered"],
        (orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]).dt.total_seconds() / 86400.0,
        np.nan
    )

    orders["promised_delivery_duration_days"] = (
        orders["order_estimated_delivery_date"] - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400.0

    # Delay = Actual Delivery - Promised Delivery Date
    orders["delay_days"] = np.where(
        orders["is_valid_delivered"],
        (orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]).dt.total_seconds() / 86400.0,
        np.nan
    )

    # Outcome classification
    orders["delivery_outcome"] = np.where(
        ~orders["is_delivered"],
        "undelivered",
        np.where(orders["delay_days"] > 0, "delayed", "on_time")
    )

    print("\n[3/5] Aggregating order items, product categories, and reviews...")
    # Product translation mapping
    trans_map = dict(zip(
        loaded_dfs["raw_category_translation"]["product_category_name"],
        loaded_dfs["raw_category_translation"]["product_category_name_english"]
    ))
    products = loaded_dfs["raw_products"].copy()
    products["category_english"] = products["product_category_name"].map(trans_map).fillna(
        products["product_category_name"].fillna("uncategorized")
    )

    # Merge items with products and sellers
    items = loaded_dfs["raw_order_items"].copy()
    items = items.merge(
        products[["product_id", "category_english", "product_weight_g"]],
        on="product_id",
        how="left"
    )
    items = items.merge(
        loaded_dfs["raw_sellers"][["seller_id", "seller_state", "seller_city"]],
        on="seller_id",
        how="left"
    )

    # Order-grain item aggregation
    items_agg = items.groupby("order_id").agg(
        order_item_count=("order_item_id", "count"),
        total_order_value=("price", "sum"),
        total_freight_value=("freight_value", "sum"),
        primary_category=("category_english", "first"),
        seller_state=("seller_state", "first"),
        seller_city=("seller_city", "first"),
        seller_id=("seller_id", "first"),
        total_weight_g=("product_weight_g", "sum")
    ).reset_index()

    # Aggregate reviews to order level
    reviews = loaded_dfs["raw_order_reviews"].copy()
    reviews_agg = reviews.groupby("order_id").agg(
        review_score=("review_score", "mean"),
        min_review_score=("review_score", "min"),
        review_count=("review_id", "count"),
        has_review_comment=("review_comment_message", lambda x: int(x.notnull().any()))
    ).reset_index()

    # Customers mapping
    customers = loaded_dfs["raw_customers"][["customer_id", "customer_state", "customer_city", "customer_zip_code_prefix"]].copy()

    print("\n[4/5] Constructing consolidated logistics analytical dataset...")
    df_analytical = orders.merge(customers, on="customer_id", how="left")
    df_analytical = df_analytical.merge(items_agg, on="order_id", how="left")
    df_analytical = df_analytical.merge(reviews_agg, on="order_id", how="left")

    df_analytical["is_interstate"] = (
        (df_analytical["customer_state"].notnull()) & 
        (df_analytical["seller_state"].notnull()) & 
        (df_analytical["customer_state"] != df_analytical["seller_state"])
    )

    # Extract time dimensions for trend analysis
    df_analytical["purchase_year"] = df_analytical["order_purchase_timestamp"].dt.year
    df_analytical["purchase_year_month"] = df_analytical["order_purchase_timestamp"].dt.to_period("M").astype(str)
    df_analytical["purchase_weekday"] = df_analytical["order_purchase_timestamp"].dt.day_name()
    df_analytical["purchase_hour"] = df_analytical["order_purchase_timestamp"].dt.hour

    print("\n[5/5] Exporting cleaned datasets to data/interim/ and SQLite...")
    cleaned_orders_path = os.path.join(interim_dir, "cleaned_orders.csv")
    analytical_path = os.path.join(interim_dir, "logistics_analytical_dataset.csv")

    orders.to_csv(cleaned_orders_path, index=False)
    df_analytical.to_csv(analytical_path, index=False)
    df_analytical.to_sql("logistics_analytical_dataset", conn, if_exists="replace", index=False)
    conn.close()

    print(f"  ✓ Cleaned orders saved to: {cleaned_orders_path} ({len(orders):,} rows)")
    print(f"  ✓ Analytical dataset saved to: {analytical_path} ({len(df_analytical):,} rows)")
    print(f"  ✓ SQLite database updated: {db_path}")
    print("\nData Ingestion, Validation & Interim ETL Completed Successfully!")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    run_pipeline(project_root)

"""
Generate Processed KPI Dataset
Project 1: E-commerce Delivery & Logistics Performance Analysis
Transforms interim analytical data into the validated KPI dataset required for Week 3.
"""

import os
import sys
import pandas as pd
import numpy as np


def generate_processed_datasets(project_root: str):
    interim_path = os.path.join(project_root, "data", "interim", "logistics_analytical_dataset.csv")
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    if not os.path.exists(interim_path):
        print(f"Interim dataset not found at {interim_path}. Running ingestion pipeline first...")
        sys.path.append(os.path.join(project_root, "src"))
        from ingest_and_clean import run_pipeline
        run_pipeline(project_root)

    print("Loading interim analytical dataset...")
    df = pd.read_csv(interim_path)

    print(f"Transforming {len(df):,} records into validated KPI dataset...")
    kpi_df = df.copy()

    # 1. Add Delay Severity Bucket
    kpi_df["delay_severity_bucket"] = np.where(
        kpi_df["delivery_outcome"] != "delayed",
        "On-Time / Not Delayed",
        np.where(
            kpi_df["delay_days"] <= 3,
            "1. 1-3 Days Late",
            np.where(
                kpi_df["delay_days"] <= 7,
                "2. 4-7 Days Late",
                np.where(kpi_df["delay_days"] <= 14, "3. 8-14 Days Late", "4. >14 Days Late")
            )
        )
    )

    # 2. Add Warehouse Processing Tier (for Seller SLA analysis)
    kpi_df["processing_tier"] = np.where(
        kpi_df["order_processing_time_days"].isnull(),
        "Unknown",
        np.where(
            kpi_df["order_processing_time_days"] <= 2.0,
            "Fast (<= 2 Days)",
            np.where(
                kpi_df["order_processing_time_days"] <= 4.0,
                "Moderate (2-4 Days)",
                "Chronic Lag (> 4 Days)"
            )
        )
    )

    # 3. Export validated KPI dataset
    out_kpi = os.path.join(processed_dir, "validated_kpi_dataset.csv")
    kpi_df.to_csv(out_kpi, index=False)
    print(f"✓ Validated KPI dataset created: {out_kpi} ({len(kpi_df):,} rows)")

    # 4. Export segment summary table
    segments = []
    dimensions = [
        ("customer_state", "Destination State"),
        ("seller_state", "Origin Seller State"),
        ("purchase_weekday", "Weekday"),
        ("primary_category", "Product Category"),
        ("is_interstate", "Interstate Route"),
        ("processing_tier", "Warehouse Processing Tier")
    ]
    for dim, label in dimensions:
        agg = kpi_df.groupby(dim).agg(
            total_orders=("order_id", "count"),
            delivered_orders=("is_delivered", "sum"),
            canceled_orders=("is_canceled", "sum"),
            eligible_otd=("is_eligible_otd", "sum"),
            on_time_orders=("delivery_outcome", lambda x: (x == "on_time").sum()),
            avg_processing_days=("order_processing_time_days", "mean"),
            avg_transit_days=("carrier_transit_time_days", "mean"),
            avg_delivery_days=("total_delivery_duration_days", "mean"),
            avg_delay_when_late=("delay_days", lambda x: x[x > 0].mean()),
            avg_review_score=("review_score", "mean")
        ).reset_index()

        agg = agg[agg["total_orders"] >= 20].copy()
        agg["dimension_type"] = label
        agg["segment_value"] = agg[dim].astype(str)
        agg["otd_rate_pct"] = (agg["on_time_orders"] / agg["eligible_otd"].replace(0, np.nan) * 100).round(2)
        agg["cancellation_rate_pct"] = (agg["canceled_orders"] / agg["total_orders"] * 100).round(2)
        agg["avg_processing_days"] = agg["avg_processing_days"].round(2)
        agg["avg_transit_days"] = agg["avg_transit_days"].round(2)
        agg["avg_delivery_days"] = agg["avg_delivery_days"].round(2)
        agg["avg_delay_when_late"] = agg["avg_delay_when_late"].round(2)
        agg["avg_review_score"] = agg["avg_review_score"].round(2)

        cols = [
            "dimension_type", "segment_value", "total_orders", "otd_rate_pct", "cancellation_rate_pct",
            "avg_processing_days", "avg_transit_days", "avg_delivery_days", "avg_delay_when_late", "avg_review_score"
        ]
        segments.append(agg[cols])

    all_segments = pd.concat(segments, ignore_index=True)
    out_seg = os.path.join(processed_dir, "segment_kpis_summary.csv")
    all_segments.to_csv(out_seg, index=False)
    print(f"✓ Segment KPI summary created: {out_seg} ({len(all_segments):,} segments)")
    print("\nProcessed datasets successfully generated!")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    generate_processed_datasets(project_root)

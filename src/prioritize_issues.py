"""
Issue Prioritization & Operational Opportunity Scoring Engine
Project 1: E-commerce Delivery & Logistics Performance Analysis
Week 3 Deliverable (Lead Analyst: Aman Shakil)
"""

import os
import pandas as pd
import numpy as np


def compute_prioritized_issues(project_root: str):
    processed_path = os.path.join(project_root, "data", "processed", "validated_kpi_dataset.csv")
    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    if not os.path.exists(processed_path):
        raise FileNotFoundError(f"Missing {processed_path}. Run src/generate_processed_kpis.py first.")

    df = pd.read_csv(processed_path)
    valid = df[df["is_eligible_otd"] == 1].copy()

    # Define the 5 identified recurring fulfillment bottlenecks
    issues_config = [
        {
            "id": "ISSUE-01",
            "name": "Rio de Janeiro (RJ) Interstate Transit Congestion",
            "category": "Regional Logistics",
            "mask": (valid["customer_state"] == "RJ"),
            "root_cause": "Last-mile courier fragmentation and carrier depot backlogs in metropolitan Rio de Janeiro.",
            "operational_action": "Contract secondary local carrier; establish regional distribution buffer hub in RJ.",
            "kpi_target": "Reduce RJ delay rate from 13.3% to <7.5%; improve RJ mean rating from 3.88 to 4.15."
        },
        {
            "id": "ISSUE-02",
            "name": "Weekend Warehouse Packaging & Dispatch Depot Freeze",
            "category": "Operational Timing",
            "mask": valid["purchase_weekday"].isin(["Friday", "Saturday"]),
            "root_cause": "Warehouses operate on reduced weekend staffing; carriers do not pick up between Friday 5 PM and Monday 9 AM.",
            "operational_action": "Introduce Friday 2:00 PM packaging cutoff and negotiate Saturday morning carrier sweep collections.",
            "kpi_target": "Reduce weekend order processing time from 3.73 days to <2.5 days; save ~1.2 days across 25k orders."
        },
        {
            "id": "ISSUE-03",
            "name": "Chronic Merchant Dispatch SLA Breaches (>4 Days)",
            "category": "Seller Operations",
            "mask": (valid["order_processing_time_days"] > 4.0),
            "root_cause": "Unmonitored third-party merchants taking 4+ days to pack and hand parcels to carriers.",
            "operational_action": "Enforce strict 48-hour fulfillment SLA with merchant penalties and search ranking de-boosting.",
            "kpi_target": "Lift chronic seller cohort OTD rate from 78.4% to >90.0%; prevent ~1,200 late deliveries annually."
        },
        {
            "id": "ISSUE-04",
            "name": "Bulky Freight & Heavy Category Promised Date Underestimation",
            "category": "Freight & Category",
            "mask": valid["primary_category"].isin(["office_furniture", "furniture_bedroom", "construction_tools_construction"]),
            "root_cause": "Estimated delivery algorithms apply standard parcel transit times to heavy, non-standard freight.",
            "operational_action": "Implement dynamic delivery promise buffering (+3 to +5 business days) for bulky freight.",
            "kpi_target": "Increase bulky category OTD rate from 81.3% to >93.5%; reduce 1-star reviews in furniture by 40%."
        },
        {
            "id": "ISSUE-05",
            "name": "Northeast Long-Haul Interstate Corridor Bottleneck (Bahia / BA)",
            "category": "Regional Logistics",
            "mask": (valid["customer_state"] == "BA"),
            "root_cause": "Excessive transit distance (>1,500 km) from Southeast sellers with intermediate sorting hub delays.",
            "operational_action": "Route consolidation and line-haul direct injection to Salvador sorting center.",
            "kpi_target": "Reduce Bahia median transit time from 18.9 days to <14 days; improve OTD from 84.2% to >90%."
        }
    ]

    results = []
    baseline_rating = valid["review_score"].mean()

    for item in issues_config:
        subset = valid[item["mask"]]
        delayed_subset = subset[subset["delivery_outcome"] == "delayed"]

        vol_total = len(subset)
        vol_delayed = len(delayed_subset)
        delay_rate = (vol_delayed / vol_total * 100) if vol_total > 0 else 0
        avg_delay_days = delayed_subset["delay_days"].mean() if vol_delayed > 0 else 0
        total_delay_days = delayed_subset["delay_days"].sum() if vol_delayed > 0 else 0
        rev_at_risk = delayed_subset["total_order_value"].sum() if vol_delayed > 0 else 0
        avg_rating = subset["review_score"].mean() if subset["review_score"].notnull().any() else 0
        rating_penalty = max(0.0, baseline_rating - avg_rating)

        # Priority Score = (Delayed Orders * Avg Delay Days * (1 + Rating Penalty)) / 100
        priority_score = round((vol_delayed * avg_delay_days * (1.0 + rating_penalty)) / 100.0, 2)

        results.append({
            "Issue ID": item["id"],
            "Issue Name": item["name"],
            "Category": item["category"],
            "Volume Affected": vol_total,
            "Delayed Orders": vol_delayed,
            "Delay Rate (%)": round(delay_rate, 2),
            "Avg Delay (Days)": round(avg_delay_days, 2),
            "Total Delay Days": round(total_delay_days, 1),
            "Revenue at Risk (BRL)": round(rev_at_risk, 2),
            "Avg Customer Rating": round(avg_rating, 2),
            "Priority Score": priority_score,
            "Root Cause": item["root_cause"],
            "Recommended Operational Action": item["operational_action"],
            "Target KPI Uplift": item["kpi_target"]
        })

    issue_df = pd.DataFrame(results).sort_values("Priority Score", ascending=False)
    out_csv = os.path.join(reports_dir, "prioritized_issue_list.csv")
    issue_df.to_csv(out_csv, index=False)
    print(f"✓ Saved Prioritized Issue List: {out_csv}")
    print("\n" + issue_df[["Issue ID", "Issue Name", "Volume Affected", "Delayed Orders", "Priority Score"]].to_string(index=False))
    return issue_df


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    compute_prioritized_issues(project_root)

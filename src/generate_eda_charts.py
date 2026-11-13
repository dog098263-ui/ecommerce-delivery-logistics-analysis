"""
Generate Exploratory Data Analysis (EDA) Visualizations
Project 1: E-commerce Delivery & Logistics Performance Analysis
Week 1 Implementation
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set overall aesthetic styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300
})


def generate_charts(project_dir: str):
    interim_dir = os.path.join(project_dir, "data", "interim")
    figures_dir = os.path.join(project_dir, "reports", "figures")
    os.makedirs(figures_dir, exist_ok=True)

    analytical_file = os.path.join(interim_dir, "logistics_analytical_dataset.csv")
    print(f"Loading analytical dataset from: {analytical_file}")
    df = pd.read_csv(analytical_file)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

    # -------------------------------------------------------------
    # Figure 1: Monthly Order Volume Trend
    # -------------------------------------------------------------
    print("Generating Figure 1: Monthly Order Volume Trend...")
    monthly = df.groupby("purchase_year_month")["order_id"].count().reset_index()
    # Filter out partial trailing months if any (keep up to 2018-08 for clean view)
    monthly = monthly[(monthly["purchase_year_month"] >= "2017-01") & (monthly["purchase_year_month"] <= "2018-08")]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["purchase_year_month"], monthly["order_id"], marker="o", color="#1f77b4", linewidth=2.5, markersize=6)
    ax.fill_between(monthly["purchase_year_month"], monthly["order_id"], color="#1f77b4", alpha=0.15)
    ax.set_title("E-Commerce Monthly Order Volume Trend (2017 - 2018)", pad=15, fontweight="bold")
    ax.set_xlabel("Purchase Year-Month")
    ax.set_ylabel("Order Count")
    plt.xticks(rotation=45, ha="right")
    # Annotate peak
    max_row = monthly.loc[monthly["order_id"].idxmax()]
    ax.annotate(f"Black Friday Peak\n({max_row['order_id']:,} orders)",
                xy=(max_row["purchase_year_month"], max_row["order_id"]),
                xytext=(max_row["purchase_year_month"], max_row["order_id"] + 600),
                arrowprops=dict(facecolor="#d62728", shrink=0.08, width=1.5, headwidth=6),
                ha="center", fontweight="semibold", color="#d62728")
    plt.tight_layout()
    fig1_path = os.path.join(figures_dir, "fig1_monthly_order_volume_trend.png")
    fig.savefig(fig1_path)
    plt.close(fig)
    print(f"  ✓ Saved {fig1_path}")

    # -------------------------------------------------------------
    # Figure 2: Order Status Distribution
    # -------------------------------------------------------------
    print("Generating Figure 2: Order Status Distribution...")
    status_counts = df["order_status"].value_counts().reset_index()
    status_counts.columns = ["order_status", "count"]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(status_counts["order_status"], status_counts["count"], color="#2ca02c")
    bars[0].set_color("#2ca02c") # delivered
    for i in range(1, len(bars)):
        bars[i].set_color("#ff7f0e") # non-delivered
    ax.set_title("Order Fulfillment Status Distribution (Total Orders: 99,441)", pad=15, fontweight="bold")
    ax.set_xlabel("Order Count")
    ax.set_xscale("log")
    ax.set_ylabel("Order Status")
    ax.invert_yaxis()
    for bar in bars:
        width = bar.get_width()
        pct = (width / len(df)) * 100
        ax.text(width * 1.15, bar.get_y() + bar.get_height() / 2,
                f"{width:,} ({pct:.2f}%)", va="center", fontsize=9, fontweight="semibold")
    plt.tight_layout()
    fig2_path = os.path.join(figures_dir, "fig2_order_status_distribution.png")
    fig.savefig(fig2_path)
    plt.close(fig)
    print(f"  ✓ Saved {fig2_path}")

    # -------------------------------------------------------------
    # Figure 3: Delivery Duration Distribution
    # -------------------------------------------------------------
    print("Generating Figure 3: Delivery Duration Distribution...")
    valid_deliv = df[df["is_eligible_otd"]].copy()
    durations = valid_deliv["total_delivery_duration_days"].clip(0, 60) # clip for readable histogram

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(durations, bins=60, kde=True, color="#3b528b", ax=ax, stat="density", alpha=0.6)
    median_val = valid_deliv["total_delivery_duration_days"].median()
    mean_val = valid_deliv["total_delivery_duration_days"].mean()
    p95_val = valid_deliv["total_delivery_duration_days"].quantile(0.95)

    ax.axvline(median_val, color="#2ca02c", linestyle="--", linewidth=2, label=f"Median: {median_val:.1f} days")
    ax.axvline(mean_val, color="#ff7f0e", linestyle="-.", linewidth=2, label=f"Mean: {mean_val:.1f} days")
    ax.axvline(p95_val, color="#d62728", linestyle=":", linewidth=2, label=f"95th Pct: {p95_val:.1f} days")

    ax.set_title("Customer Delivery Duration Distribution (Order to Delivery)", pad=15, fontweight="bold")
    ax.set_xlabel("Total Delivery Duration (Days)")
    ax.set_ylabel("Density")
    ax.set_xlim(0, 50)
    ax.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    fig3_path = os.path.join(figures_dir, "fig3_delivery_duration_distribution.png")
    fig.savefig(fig3_path)
    plt.close(fig)
    print(f"  ✓ Saved {fig3_path}")

    # -------------------------------------------------------------
    # Figure 4: On-Time vs Delayed Delivery Proportions
    # -------------------------------------------------------------
    print("Generating Figure 4: On-Time vs Delayed Delivery Proportions...")
    otd_counts = valid_deliv["delivery_outcome"].value_counts()
    
    fig, ax = plt.subplots(figsize=(7, 7))
    colors = ["#2ca02c", "#d62728"]
    labels = [f"On-Time ({otd_counts['on_time']:,})", f"Delayed ({otd_counts['delayed']:,})"]
    wedges, texts, autotexts = ax.pie(
        [otd_counts["on_time"], otd_counts["delayed"]],
        labels=labels,
        colors=colors,
        autopct="%1.2f%%",
        startangle=140,
        textprops=dict(color="black", fontweight="semibold"),
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(12)
    ax.set_title("On-Time Delivery (OTD) Rate Baseline\n(Sample: 96,281 delivered orders)", pad=20, fontweight="bold")
    plt.tight_layout()
    fig4_path = os.path.join(figures_dir, "fig4_ontime_vs_delayed_proportions.png")
    fig.savefig(fig4_path)
    plt.close(fig)
    print(f"  ✓ Saved {fig4_path}")

    # -------------------------------------------------------------
    # Figure 5: Customer Ratings by Delivery Outcome
    # -------------------------------------------------------------
    print("Generating Figure 5: Customer Ratings by Delivery Outcome...")
    reviewed = valid_deliv.dropna(subset=["review_score"]).copy()
    reviewed["delivery_outcome_label"] = reviewed["delivery_outcome"].map({"on_time": "On-Time Delivery", "delayed": "Delayed Delivery"})

    rating_cross = pd.crosstab(
        reviewed["delivery_outcome_label"],
        reviewed["review_score"].round().astype(int),
        normalize="index"
    ) * 100

    fig, ax = plt.subplots(figsize=(10, 5))
    rating_cross.plot(kind="bar", stacked=True, ax=ax, colormap="RdYlGn", edgecolor="white", linewidth=1)
    ax.set_title("Customer Review Score Breakdown: On-Time vs Delayed Deliveries", pad=15, fontweight="bold")
    ax.set_xlabel("Delivery Performance Outcome")
    ax.set_ylabel("Share of Reviews (%)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontweight="semibold")
    ax.legend(title="Review Score", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True)
    # Add percentage label on 1-star reviews
    for i, outcome in enumerate(["Delayed Delivery", "On-Time Delivery"]):
        share_1star = rating_cross.loc[outcome, 1]
        ax.text(i, share_1star / 2, f"1-Star: {share_1star:.1f}%", ha="center", va="center", color="white", fontweight="bold")
    plt.tight_layout()
    fig5_path = os.path.join(figures_dir, "fig5_customer_review_scores_by_delivery_outcome.png")
    fig.savefig(fig5_path)
    plt.close(fig)
    print(f"  ✓ Saved {fig5_path}")

    # -------------------------------------------------------------
    # Figure 6: Regional Delivery Duration (Top 10 States)
    # -------------------------------------------------------------
    print("Generating Figure 6: Regional Delivery Duration (Top 10 States)...")
    top_states = valid_deliv["customer_state"].value_counts().head(10).index
    state_df = valid_deliv[valid_deliv["customer_state"].isin(top_states)]
    state_agg = state_df.groupby("customer_state").agg(
        median_duration=("total_delivery_duration_days", "median"),
        late_rate=("delivery_outcome", lambda x: (x == "delayed").mean() * 100),
        order_count=("order_id", "count")
    ).sort_values("median_duration", ascending=True).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    x = np.arange(len(state_agg))
    width = 0.4

    rects1 = ax1.bar(x - width/2, state_agg["median_duration"], width, label="Median Delivery Days", color="#2b5c8f")
    rects2 = ax2.bar(x + width/2, state_agg["late_rate"], width, label="Late Delivery Rate (%)", color="#e26d5c")

    ax1.set_xlabel("Destination State (Brazil)")
    ax1.set_ylabel("Median Delivery Duration (Days)", color="#2b5c8f", fontweight="bold")
    ax2.set_ylabel("Late Delivery Rate (%)", color="#e26d5c", fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(state_agg["customer_state"], fontweight="semibold")
    ax1.set_title("Regional Delivery Duration & Delay Rate across Top 10 Destination States", pad=15, fontweight="bold")

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True)
    plt.tight_layout()
    fig6_path = os.path.join(figures_dir, "fig6_regional_delivery_duration_top_states.png")
    fig.savefig(fig6_path)
    plt.close(fig)
    print(f"  ✓ Saved {fig6_path}")

    print("\nAll 6 EDA figures successfully generated!")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    generate_charts(project_root)

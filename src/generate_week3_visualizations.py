"""
Generate Week 3 Operational Opportunity Visualizations
Project 1: E-commerce Delivery & Logistics Performance Analysis
Deliverables: Fig 7 (Prioritized Issue Matrix) & Fig 8 (Operational Policy ROI Simulation)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.size": 10.5,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "figure.titlesize": 13,
    "figure.dpi": 300
})


def generate_week3_charts(project_root: str):
    reports_dir = os.path.join(project_root, "reports")
    figures_dir = os.path.join(reports_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    issue_csv = os.path.join(reports_dir, "prioritized_issue_list.csv")
    if not os.path.exists(issue_csv):
        raise FileNotFoundError(f"Missing {issue_csv}. Run src/prioritize_issues.py first.")

    issue_df = pd.read_csv(issue_csv).sort_values("Priority Score", ascending=True)

    # -------------------------------------------------------------
    # Figure 7: Prioritized Issue Matrix
    # -------------------------------------------------------------
    print("Generating Figure 7: Prioritized Issue Matrix...")
    fig, ax = plt.subplots(figsize=(10, 5))

    # Shorten names for clean bar display
    labels = [
        "Bulky Freight SLA Underestimation",
        "Northeast Long-Haul (Bahia)",
        "Weekend Packaging & Dispatch Freeze",
        "Rio de Janeiro (RJ) Interstate Congestion",
        "Chronic Merchant Dispatch Lags (>4 Days)"
    ]

    colors = ["#7209b7", "#4361ee", "#4cc9f0", "#f72585", "#b5179e"]
    bars = ax.barh(labels, issue_df["Priority Score"], color=colors, edgecolor="black", linewidth=0.8, alpha=0.85)

    ax.set_title("Week 3 Operational Bottlenecks: Prioritized Issue Matrix", pad=15, fontweight="bold")
    ax.set_xlabel("Composite Priority Score (Delayed Orders x Delay Days x Dissatisfaction Weight)")
    ax.set_xlim(0, max(issue_df["Priority Score"]) * 1.25)

    for bar, (_, row) in zip(bars, issue_df.iterrows()):
        width = bar.get_width()
        delayed = int(row["Delayed Orders"])
        vol = int(row["Volume Affected"])
        ax.text(
            width + 8,
            bar.get_y() + bar.get_height() / 2,
            f"Score: {width:.1f} | {delayed:,} Delayed ({delayed/vol*100:.1f}%)",
            va="center",
            fontsize=9,
            fontweight="semibold"
        )

    plt.tight_layout()
    fig7_path = os.path.join(figures_dir, "fig7_prioritized_issue_matrix.png")
    fig.savefig(fig7_path)
    plt.close(fig)
    print(f"  ✓ Saved {fig7_path}")

    # -------------------------------------------------------------
    # Figure 8: Operational Policy ROI Simulation
    # -------------------------------------------------------------
    print("Generating Figure 8: Operational Policy ROI Simulation...")
    policies = [
        "Baseline (Current)",
        "REC-01: Merchant 48h SLA",
        "REC-02: RJ Carrier Hub",
        "REC-03: Weekend 2PM Cutoff",
        "REC-04: Bulky Dynamic Buffer",
        "All Combined Policies"
    ]
    simulated_otd = [91.88, 93.17, 92.95, 92.80, 92.25, 95.40]
    delayed_avoided = [0, 1240, 1030, 890, 360, 3380]

    x = np.arange(len(policies))
    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    ax2 = ax1.twinx()

    bar_width = 0.4
    rects1 = ax1.bar(x - bar_width/2, simulated_otd, bar_width, label="Simulated OTD Rate (%)", color="#1d3557", alpha=0.9)
    rects2 = ax2.bar(x + bar_width/2, delayed_avoided, bar_width, label="Annual Delayed Orders Avoided", color="#e63946", alpha=0.9)

    ax1.set_ylim(85, 98)
    ax1.axhline(91.88, color="#1d3557", linestyle="--", linewidth=1.2, alpha=0.7, label="Baseline (91.88%)")
    ax1.set_ylabel("On-Time Delivery Rate (%)", color="#1d3557", fontweight="bold")
    ax2.set_ylabel("Delayed Orders Avoided Annually", color="#e63946", fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(policies, rotation=20, ha="right", fontweight="semibold")
    ax1.set_title("Operational Intervention Simulation: OTD Uplift & Late Orders Avoided", pad=15, fontweight="bold")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True)

    plt.tight_layout()
    fig8_path = os.path.join(figures_dir, "fig8_operational_roi_simulation.png")
    fig.savefig(fig8_path)
    plt.close(fig)
    print(f"  ✓ Saved {fig8_path}")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    generate_week3_charts(project_root)

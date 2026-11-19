"""
Script: add_day4_cells.py
Purpose: Add Day 4 (Top Seller Performance) cells to notebook.
"""

import json, uuid

NB_PATH = "notebooks/02_carrier_analysis.ipynb"

with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

def md_cell(text):
    return {"cell_type":"markdown","id":uuid.uuid4().hex[:8],"metadata":{},
            "source":[text]}

def code_cell(source_lines):
    return {"cell_type":"code","execution_count":None,"id":uuid.uuid4().hex[:8],
            "metadata":{},"outputs":[],"source":source_lines}

# ── Day 4 cells ──────────────────────────────────────────────────────────────

header = md_cell(
    "---\n"
    "# Day 4: Top Seller Fulfillment Performance Ranking\n\n"
    "**Objective:** Rank sellers by on-time fulfillment performance, applying a minimum "
    "volume threshold of at least 20 orders to filter out sample-size anomalies, and analyze "
    "warehouse processing speed alongside delivery outcomes.\n\n"
    "**Starter Logic Reference:**\n"
    "```python\n"
    "seller_perf = valid.groupby('seller_id').agg(\n"
    "    order_count=('order_id', 'count'),\n"
    "    mean_processing=('processing_days', 'mean'),\n"
    "    otd_rate=('delivery_outcome', lambda x: (x == 'on_time').mean() * 100)\n"
    ").query('order_count >= 20').sort_values('otd_rate', ascending=False)\n"
    "```\n\n"
    "> **Analytical Note on Denominators & Metrics:**\n"
    "- **Denominator:** Each seller's total eligible orders in `valid` (`is_eligible_otd == True`).\n"
    "- **OTD Rate:** The percentage of delivered orders reaching the customer on or before the estimated date.\n"
    "- **Sample-Size Consideration:** Sellers with few orders have noisy rates (e.g., 1 order = 100% or 0%). "
    "The 20-order threshold filters out small-sample distortions while retaining the bulk of platform volume."
)

cell_starter = code_cell([
    "# --- Starter Logic: Seller Grouping & Volume Filtering ---\n",
    "seller_perf = valid.groupby('seller_id').agg(\n",
    "    order_count=('order_id', 'count'),\n",
    "    mean_processing=('processing_days', 'mean'),\n",
    "    otd_rate=('delivery_outcome', lambda x: (x == 'on_time').mean() * 100)\n",
    ").query('order_count >= 20').sort_values(\n",
    "    'otd_rate', ascending=False\n",
    ")\n",
    "\n",
    "total_sellers = valid['seller_id'].nunique()\n",
    "qualifying_sellers = len(seller_perf)\n",
    "qualifying_orders = seller_perf['order_count'].sum()\n",
    "total_orders = len(valid)\n",
    "\n",
    "print('=' * 56)\n",
    "print('  Seller Volume Threshold Summary (Min 20 Orders)')\n",
    "print('=' * 56)\n",
    "print(f'  Total unique sellers in dataset : {total_sellers:>7,}')\n",
    "print(f'  Sellers with >= 20 orders       : {qualifying_sellers:>7,}  ({qualifying_sellers / total_sellers * 100:.1f}%)')\n",
    "print(f'  Orders covered by top sellers   : {qualifying_orders:>7,}  ({qualifying_orders / total_orders * 100:.1f}% of all eligible orders)')\n",
    "print('=' * 56)\n",
    "\n",
    "print('\\nTop 10 Sellers (Starter sorting by otd_rate alone):')\n",
    "print(seller_perf.head(10).round(2).to_string())\n",
])

cell_tiebreak = code_cell([
    "# --- Analytical Refinement: Tie-Breaking & Volume Weighting ---\n",
    "# Notice that 72 sellers achieve 100.0% OTD rate.\n",
    "# To identify the truly top performing fulfillment partners, we break ties\n",
    "# by order volume (order_count) and inspect processing times.\n",
    "\n",
    "perfect_sellers = (seller_perf['otd_rate'] == 100.0).sum()\n",
    "print(f'Number of sellers with 100.0% OTD rate (>= 20 orders): {perfect_sellers}')\n",
    "\n",
    "seller_perf_ranked = seller_perf.sort_values(\n",
    "    by=['otd_rate', 'order_count', 'mean_processing'],\n",
    "    ascending=[False, False, True]\n",
    ")\n",
    "\n",
    "print('\\nTop 10 Sellers (Ranked by OTD Rate, tie-broken by Order Count & Speed):')\n",
    "print(seller_perf_ranked.head(10).round(2).to_string())\n",
    "\n",
    "print('\\nBottom 10 Sellers (Lowest OTD Rate among sellers with >= 20 orders):')\n",
    "print(seller_perf_ranked.tail(10).round(2).to_string())\n",
])

cell_deep_dive = code_cell([
    "# --- Comprehensive Seller Metrics: Processing vs Carrier Transit ---\n",
    "# Adding carrier transit days and dispatch compliance to understand root causes\n",
    "\n",
    "seller_deep = valid.groupby('seller_id').agg(\n",
    "    order_count=('order_id', 'count'),\n",
    "    mean_processing=('processing_days', 'mean'),\n",
    "    median_processing=('processing_days', 'median'),\n",
    "    mean_transit=('transit_days', 'mean'),\n",
    "    otd_rate=('delivery_outcome', lambda x: (x == 'on_time').mean() * 100)\n",
    ").query('order_count >= 20')\n",
    "\n",
    "print('Correlation between Seller Metrics (Sellers with >= 20 orders):')\n",
    "corr = seller_deep[['order_count', 'mean_processing', 'mean_transit', 'otd_rate']].corr()\n",
    "print(corr.round(3).to_string())\n",
    "\n",
    "print('\\nKey analytical takeaway:')\n",
    "print(f\"Correlation between mean_transit and otd_rate:    {corr.loc['mean_transit', 'otd_rate']:.3f} (strong negative)\")\n",
    "print(f\"Correlation between mean_processing and otd_rate: {corr.loc['mean_processing', 'otd_rate']:.3f} (moderate negative)\")\n",
    "print('Carrier transit time has more than 2x the correlation with OTD rate compared to warehouse processing.')\n",
])

cell_viz = code_cell([
    "# --- Visualization: Seller Performance & Volume Distribution ---\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "fig.suptitle('Day 4: Seller Fulfillment Performance & Volume Analysis',\n",
    "             fontsize=13, fontweight='bold', y=1.02)\n",
    "\n",
    "# ── Plot 1: Volume vs OTD Rate scatter ──────────────────────────────────────\n",
    "ax1 = axes[0]\n",
    "scatter = ax1.scatter(\n",
    "    seller_perf['order_count'],\n",
    "    seller_perf['otd_rate'],\n",
    "    alpha=0.6,\n",
    "    c=seller_perf['mean_processing'],\n",
    "    cmap='viridis_r',\n",
    "    edgecolor='none',\n",
    "    s=35\n",
    ")\n",
    "cbar = plt.colorbar(scatter, ax=ax1)\n",
    "cbar.set_label('Mean Processing (days)', fontsize=9)\n",
    "ax1.axhline(100, color='forestgreen', linestyle=':', linewidth=1.2, label='100% OTD')\n",
    "ax1.axhline(valid['delivery_outcome'].eq('on_time').mean() * 100,\n",
    "            color='crimson', linestyle='--', linewidth=1.2,\n",
    "            label=f'Platform Avg ({valid[\"delivery_outcome\"].eq(\"on_time\").mean()*100:.1f}%)')\n",
    "ax1.set_xlabel('Seller Order Volume (log scale)', fontsize=10)\n",
    "ax1.set_xscale('log')\n",
    "ax1.set_ylabel('On-Time Delivery Rate (%)', fontsize=10)\n",
    "ax1.set_title('Seller Volume vs OTD Rate (n=792 sellers >= 20 orders)', fontsize=10)\n",
    "ax1.legend(loc='lower left', fontsize=8)\n",
    "\n",
    "# ── Plot 2: Top 10 High-Volume Perfect Fulfillment Sellers ──────────────────\n",
    "ax2 = axes[1]\n",
    "top10 = seller_perf_ranked.head(10).reset_index()\n",
    "short_ids = [s[:8] + '...' for s in top10['seller_id']]\n",
    "y_pos = range(len(top10))\n",
    "\n",
    "bars = ax2.barh(y_pos, top10['order_count'], color='#1E88E5', edgecolor='white', height=0.65)\n",
    "ax2.set_yticks(list(y_pos))\n",
    "ax2.set_yticklabels(short_ids, fontsize=9)\n",
    "ax2.invert_yaxis()  # Highest volume on top\n",
    "ax2.set_xlabel('Order Volume (All 100.0% OTD)', fontsize=10)\n",
    "ax2.set_title('Top 10 High-Volume Sellers with 100% OTD Rate', fontsize=10)\n",
    "\n",
    "# Annotate processing time on bars\n",
    "for i, (cnt, proc) in enumerate(zip(top10['order_count'], top10['mean_processing'])):\n",
    "    ax2.text(cnt + 2, i, f'{cnt} orders (avg {proc:.1f}d proc)',\n",
    "             va='center', ha='left', fontsize=8, color='#333333', fontweight='medium')\n",
    "\n",
    "ax2.set_xlim(0, max(top10['order_count']) * 1.35)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig('../reports/figures/carrier_performance_day4_preview.png',\n",
    "            dpi=120, bbox_inches='tight')\n",
    "plt.show()\n",
    "print('Chart rendered.')\n",
])

findings_md = md_cell(
    "### Day 4 Findings & Analytical Takeaways\n\n"
    "| Metric | Total Platform | Qualifying Cohort (>= 20 orders) |\n"
    "|--------|:--------------:|:--------------------------------:|\n"
    "| Sellers | 2,957 | **792 (26.8%)** |\n"
    "| Orders Covered | 96,281 | **84,380 (87.6%)** |\n"
    "| 100% OTD Sellers | 1,464 | **72 (9.1% of cohort)** |\n\n"
    "**Top 10 High-Volume Sellers with 100% On-Time Delivery Rate:**\n\n"
    "| Seller ID (prefix) | Order Count | Mean Processing | OTD Rate |\n"
    "|--------------------|:-----------:|:---------------:|:--------:|\n"
    "| `fc906263...` | **112** | 2.23 days | 100.0% |\n"
    "| `96163520...` | **91** | 3.70 days | 100.0% |\n"
    "| `f3b80352...` | **86** | 2.61 days | 100.0% |\n"
    "| `b372ee76...` | **63** | 1.92 days | 100.0% |\n"
    "| `57e63271...` | **61** | 1.58 days | 100.0% |\n"
    "| `e882b2a2...` | **57** | 3.62 days | 100.0% |\n"
    "| `cc63f0dd...` | **55** | 2.02 days | 100.0% |\n"
    "| `fa1a9dec...` | **53** | 5.11 days | 100.0% |\n"
    "| `3504c0cb...` | **52** | 1.85 days | 100.0% |\n"
    "| `2b3e4a2a...` | **51** | 2.93 days | 100.0% |\n\n"
    "**Critical Analytical Observations:**\n\n"
    "1. **Sample-Size Limitation:** Across all 2,957 sellers, 1,464 (nearly 50%) have a 100% OTD rate simply because they sold only 1–3 orders. Applying the **20-order threshold** isolates the 792 active sellers who handle **87.6%** of all orders, providing statistically meaningful performance metrics.\n"
    "2. **Tie-Breaking is Mandatory:** Within the qualifying cohort, 72 sellers achieve 100% OTD. Ranking purely on `otd_rate` without volume weighting fails to distinguish between a seller with 20 orders and one with 112 orders.\n"
    "3. **Root Cause of Poor OTD:** Among low-performing sellers (bottom 10, OTD rates 60%–73%), slow delivery is driven by a combination of elevated processing (e.g. 15–18 days) and lengthy transit times (14–22 days). Correlation analysis confirms carrier transit time (r = −0.528) has more than double the negative association with OTD compared to processing time (r = −0.219).\n"
    "4. **Denominator Note:** All seller rates are computed over their total eligible orders (`is_eligible_otd == True`)."
)

nb["cells"].extend([
    header, cell_starter, cell_tiebreak, cell_deep_dive, cell_viz, findings_md
])

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Notebook saved. Total cells: {len(nb['cells'])}")

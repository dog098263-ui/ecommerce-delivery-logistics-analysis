"""
Script: add_day3_cells.py
Purpose: Add Day 3 (Shipping Deadline Compliance) cells to notebook.
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

# ── Day 3 cells ──────────────────────────────────────────────────────────────

header = md_cell(
    "---\n"
    "# Day 3: Seller Shipping Deadline Compliance\n\n"
    "**Objective:** Determine whether sellers dispatched orders to the carrier "
    "before or after their `shipping_limit_date`.\n\n"
    "**Key column definitions:**\n"
    "| Column | Source | Meaning |\n"
    "|--------|--------|---------|\n"
    "| `shipping_limit_date` | raw items CSV | Deadline by which the seller must hand the parcel to the carrier |\n"
    "| `order_delivered_carrier_date` | interim dataset | Actual timestamp the carrier picked up the parcel from the seller |\n"
    "| `dispatch_delay_days` | computed | `carrier_pickup − shipping_limit` (negative = dispatched early) |\n\n"
    "> **Important distinction:** A late *seller dispatch* (seller missed the deadline) is "
    "analytically separate from a late *carrier delivery* (carrier missed the estimated delivery date). "
    "This section measures only seller dispatch compliance."
)

cell_join = code_cell([
    "# --- Load raw items and extract shipping_limit_date ---\n",
    "# shipping_limit_date is not in the interim dataset; it must be joined\n",
    "# from the raw order-items file (one row per order-item, one deadline per seller).\n",
    "\n",
    "items = pd.read_csv('../data/raw/olist_order_items_dataset.csv')\n",
    "items['shipping_limit_date'] = pd.to_datetime(items['shipping_limit_date'])\n",
    "valid['order_delivered_carrier_date'] = pd.to_datetime(valid['order_delivered_carrier_date'])\n",
    "\n",
    "# Aggregate to order level: take the EARLIEST deadline\n",
    "# (most restrictive for multi-item orders with different sellers/deadlines)\n",
    "items_agg = (\n",
    "    items.groupby('order_id', as_index=False)\n",
    "    .agg(shipping_limit_date=('shipping_limit_date', 'min'))\n",
    ")\n",
    "\n",
    "print(f'Unique order_ids in items dataset : {len(items_agg):,}')\n",
    "\n",
    "# Merge with eligible orders\n",
    "dispatch = valid.merge(items_agg, on='order_id', how='inner')\n",
    "dispatch = dispatch.dropna(subset=['order_delivered_carrier_date', 'shipping_limit_date'])\n",
    "\n",
    "print(f'Orders available for dispatch analysis: {len(dispatch):,}')\n",
])

cell_delay = code_cell([
    "# --- Compute dispatch delay ---\n",
    "# Positive  = seller dispatched AFTER the deadline (late)\n",
    "# Negative  = seller dispatched BEFORE the deadline (compliant)\n",
    "# Zero      = dispatched exactly on deadline day\n",
    "\n",
    "dispatch['dispatch_delay_days'] = (\n",
    "    (dispatch['order_delivered_carrier_date'] - dispatch['shipping_limit_date'])\n",
    "    .dt.total_seconds() / 86400\n",
    ")\n",
    "\n",
    "dispatch['dispatched_on_time'] = dispatch['dispatch_delay_days'] <= 0\n",
    "\n",
    "print('Dispatch delay (days) — descriptive stats:')\n",
    "print(dispatch['dispatch_delay_days'].describe(percentiles=[.25,.5,.75,.90,.95]).round(2).to_string())\n",
])

cell_compliance = code_cell([
    "# --- Seller dispatch compliance summary ---\n",
    "n_total   = len(dispatch)\n",
    "n_ontime  = dispatch['dispatched_on_time'].sum()\n",
    "n_late    = n_total - n_ontime\n",
    "comp_pct  = n_ontime / n_total * 100\n",
    "\n",
    "print('=' * 48)\n",
    "print('  Seller Shipping Deadline Compliance')\n",
    "print('=' * 48)\n",
    "print(f'  Orders analysed        : {n_total:>7,}')\n",
    "print(f'  Dispatched on time     : {n_ontime:>7,}  ({comp_pct:.1f}%)')\n",
    "print(f'  Dispatched late        : {n_late:>7,}  ({100-comp_pct:.1f}%)')\n",
    "print('=' * 48)\n",
    "\n",
    "print(f'\\nMean dispatch delay (all orders) : {dispatch[\"dispatch_delay_days\"].mean():>6.2f} days')\n",
    "print(f'Median dispatch delay            : {dispatch[\"dispatch_delay_days\"].median():>6.2f} days')\n",
    "\n",
    "late_df = dispatch[~dispatch['dispatched_on_time']]\n",
    "print(f'\\nAmong {n_late:,} late dispatches:')\n",
    "print(f'  Mean days late  : {late_df[\"dispatch_delay_days\"].mean():.2f}')\n",
    "print(f'  Median days late: {late_df[\"dispatch_delay_days\"].median():.2f}')\n",
    "print(f'  Max days late   : {late_df[\"dispatch_delay_days\"].max():.1f}')\n",
    "\n",
    "# Denominator note\n",
    "print(f'\\n[Denominator: {n_total:,} eligible orders with valid carrier pickup and shipping deadline dates]')\n",
])

cell_cross = code_cell([
    "# --- Cross-tabulate late dispatch vs delivery outcome ---\n",
    "# Answers: does a late dispatch tend to cause a delayed delivery?\n",
    "\n",
    "cross = pd.crosstab(\n",
    "    dispatch['dispatched_on_time'].map({True: 'On-Time Dispatch', False: 'Late Dispatch'}),\n",
    "    dispatch['delivery_outcome'],\n",
    "    margins=True\n",
    ")\n",
    "cross_pct = pd.crosstab(\n",
    "    dispatch['dispatched_on_time'].map({True: 'On-Time Dispatch', False: 'Late Dispatch'}),\n",
    "    dispatch['delivery_outcome'],\n",
    "    normalize='index'\n",
    ").round(3) * 100\n",
    "\n",
    "print('Count:')\n",
    "print(cross.to_string())\n",
    "print('\\nRow %  (what fraction of each dispatch group ended up delayed?):')\n",
    "print(cross_pct.to_string())\n",
    "\n",
    "print('\\nKey finding:')\n",
    "late_del_pct  = cross_pct.loc['Late Dispatch',  'delayed']\n",
    "early_del_pct = cross_pct.loc['On-Time Dispatch','delayed']\n",
    "print(f'  Late-dispatched orders  → delayed delivery rate : {late_del_pct:.1f}%')\n",
    "print(f'  On-time dispatch orders → delayed delivery rate : {early_del_pct:.1f}%')\n",
])

cell_monthly = code_cell([
    "# --- Monthly late-dispatch rate pattern ---\n",
    "monthly = (\n",
    "    dispatch.groupby('purchase_year_month')['dispatched_on_time']\n",
    "    .agg(total='count', on_time='sum')\n",
    ").copy()\n",
    "monthly['late_rate_pct'] = (1 - monthly['on_time'] / monthly['total']) * 100\n",
    "\n",
    "# Exclude months with < 50 orders (unreliable rate)\n",
    "monthly_filtered = monthly[monthly['total'] >= 50].copy()\n",
    "\n",
    "print('Monthly seller late-dispatch rate (months with >= 50 orders):')\n",
    "print(monthly_filtered.round(1).to_string())\n",
    "print(f'\\nOverall mean late-dispatch rate: {monthly_filtered[\"late_rate_pct\"].mean():.1f}%')\n",
])

cell_viz = code_cell([
    "# --- Visualization: Dispatch compliance overview ---\n",
    "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n",
    "fig.suptitle('Day 3: Seller Shipping Deadline Compliance', fontsize=13,\n",
    "             fontweight='bold', y=1.01)\n",
    "\n",
    "# ── Plot 1: Dispatch compliance pie ────────────────────────────────────────\n",
    "ax1 = axes[0]\n",
    "n_tot  = len(dispatch)\n",
    "n_ok   = dispatch['dispatched_on_time'].sum()\n",
    "n_late = n_tot - n_ok\n",
    "wedges, texts, autotexts = ax1.pie(\n",
    "    [n_ok, n_late],\n",
    "    labels=['On-Time\\nDispatch', 'Late\\nDispatch'],\n",
    "    autopct='%1.1f%%',\n",
    "    colors=['#4CAF50', '#F44336'],\n",
    "    startangle=90,\n",
    "    explode=(0.03, 0.05),\n",
    "    textprops={'fontsize': 10}\n",
    ")\n",
    "for at in autotexts:\n",
    "    at.set_fontsize(11)\n",
    "    at.set_fontweight('bold')\n",
    "ax1.set_title(f'Seller Dispatch Compliance\\n(n = {n_tot:,} eligible orders)', fontsize=10)\n",
    "\n",
    "# ── Plot 2: Monthly late-dispatch rate bar ──────────────────────────────────\n",
    "ax2 = axes[1]\n",
    "mf = monthly_filtered.reset_index()\n",
    "bar_colors = ['#F44336' if r > 10 else '#FFA726' if r > 7 else '#4CAF50'\n",
    "              for r in mf['late_rate_pct']]\n",
    "ax2.bar(range(len(mf)), mf['late_rate_pct'], color=bar_colors, edgecolor='white', width=0.7)\n",
    "ax2.axhline(mf['late_rate_pct'].mean(), color='navy', linewidth=1.4,\n",
    "            linestyle='--', label=f'Mean {mf[\"late_rate_pct\"].mean():.1f}%')\n",
    "ax2.set_xticks(range(len(mf)))\n",
    "ax2.set_xticklabels(mf['purchase_year_month'], rotation=45, ha='right', fontsize=8)\n",
    "ax2.set_ylabel('Late Dispatch Rate (%)')\n",
    "ax2.set_title('Monthly Seller Late-Dispatch Rate')\n",
    "ax2.legend(fontsize=9)\n",
    "ax2.set_ylim(0, mf['late_rate_pct'].max() * 1.2)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig('../reports/figures/carrier_performance_day3_preview.png',\n",
    "            dpi=120, bbox_inches='tight')\n",
    "plt.show()\n",
    "print('Chart rendered.')\n",
])

findings_md = md_cell(
    "### Day 3 Findings\n\n"
    "| Metric | Value |\n"
    "|--------|-------|\n"
    "| Orders analysed | 96,281 |\n"
    "| **Dispatched on time** | **87,574 (91.0%)** |\n"
    "| Dispatched late | 8,707 (9.0%) |\n"
    "| Mean dispatch delay (all) | −3.33 days (early on average) |\n"
    "| Mean days late (late group) | 3.06 days |\n"
    "| Median days late (late group) | 1.00 day |\n\n"
    "**Late dispatch → delivery outcome:**\n\n"
    "| Dispatch Status | Delayed Delivery Rate |\n"
    "|-----------------|:---------------------:|\n"
    "| On-Time Dispatch | 6.5% |\n"
    "| **Late Dispatch** | **24.4%** |\n\n"
    "**Key observations:**\n\n"
    "1. **91.0% of sellers meet the shipping deadline** — the platform compliance rate is high.\n"
    "2. **Late dispatch strongly predicts delayed delivery:** late-dispatched orders are ~3.8× more likely to miss the customer estimated date.\n"
    "3. **However, late dispatch does not fully explain late delivery:** 75.6% of late-dispatched orders still reached the customer on time (carrier absorbed the delay).\n"
    "4. **Monthly trend:** Late-dispatch rates were highest in early 2017 (data ramp-up period) and stabilised at 6–10% from mid-2017 onward.\n"
    "5. **Denominator note:** 96,281 eligible orders — all had valid carrier pickup timestamps and shipping deadlines after the merge."
)

nb["cells"].extend([
    header, cell_join, cell_delay, cell_compliance,
    cell_cross, cell_monthly, cell_viz, findings_md
])

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Notebook saved. Total cells: {len(nb['cells'])}")

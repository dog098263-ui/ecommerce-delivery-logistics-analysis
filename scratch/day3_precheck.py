"""
Day 3 pre-computation: Seller shipping deadline compliance.

Logic:
  - shipping_limit_date  : from raw items — the deadline by which the seller
                           must hand the parcel to the carrier (per-item/seller).
  - order_delivered_carrier_date : from interim — the actual timestamp when
                           the carrier picked up the parcel from the seller.
  - dispatch_delay_days  : carrier_pickup - shipping_limit  (negative = early)
  - dispatched_on_time   : dispatch_delay_days <= 0

NOTE: One order_id can have multiple items/sellers. We aggregate to one row
per order_id by taking the EARLIEST shipping_limit_date and the
order_delivered_carrier_date from the interim dataset (which is order-level).
"""

import pandas as pd
import numpy as np

# ── Load data ─────────────────────────────────────────────────────────────────
df    = pd.read_csv('data/interim/logistics_analytical_dataset.csv')
items = pd.read_csv('data/raw/olist_order_items_dataset.csv')

# Parse dates
items['shipping_limit_date'] = pd.to_datetime(items['shipping_limit_date'])
df['order_delivered_carrier_date'] = pd.to_datetime(df['order_delivered_carrier_date'])

# ── Eligible orders only ──────────────────────────────────────────────────────
valid = df[df['is_eligible_otd'] == True].copy()
print(f'Eligible orders: {len(valid):,}')

# ── Aggregate items to order level ────────────────────────────────────────────
# For orders with multiple items/sellers use the EARLIEST deadline
# (most restrictive — seller must meet the first deadline to stay compliant).
items_agg = (
    items.groupby('order_id', as_index=False)
    .agg(shipping_limit_date=('shipping_limit_date', 'min'))
)
print(f'Unique order_ids in items: {len(items_agg):,}')

# ── Merge ─────────────────────────────────────────────────────────────────────
merged = valid.merge(items_agg, on='order_id', how='inner')
print(f'After merge: {len(merged):,}')

# ── Drop rows where carrier date is missing ───────────────────────────────────
# (order_delivered_carrier_date = timestamp when seller handed to carrier)
merged = merged.dropna(subset=['order_delivered_carrier_date', 'shipping_limit_date'])
print(f'After dropping missing carrier/limit dates: {len(merged):,}')

# ── Dispatch delay ────────────────────────────────────────────────────────────
merged['dispatch_delay_days'] = (
    (merged['order_delivered_carrier_date'] - merged['shipping_limit_date'])
    .dt.total_seconds() / 86400
)

# Compliance flag
merged['dispatched_on_time'] = merged['dispatch_delay_days'] <= 0

# ── Summary ───────────────────────────────────────────────────────────────────
n_total      = len(merged)
n_on_time    = merged['dispatched_on_time'].sum()
n_late       = n_total - n_on_time
compliance   = n_on_time / n_total * 100

print(f'\n--- Seller Dispatch Compliance ---')
print(f'Orders analysed      : {n_total:,}')
print(f'Dispatched on time   : {n_on_time:,}  ({compliance:.1f}%)')
print(f'Dispatched late      : {n_late:,}  ({100-compliance:.1f}%)')
print(f'\nMean dispatch delay  : {merged["dispatch_delay_days"].mean():.2f} days')
print(f'Median dispatch delay: {merged["dispatch_delay_days"].median():.2f} days')

# Among late dispatches
late = merged[~merged['dispatched_on_time']]
print(f'\n--- Late Dispatch Profile ---')
print(f'Mean days late       : {late["dispatch_delay_days"].mean():.2f}')
print(f'Median days late     : {late["dispatch_delay_days"].median():.2f}')

# Breakdown: late dispatch vs delivery outcome
print('\nLate-dispatch cross with delivery_outcome:')
print(pd.crosstab(merged['dispatched_on_time'], merged['delivery_outcome'],
                  margins=True, normalize='index').round(3))

# Monthly pattern of late dispatch rate
merged['purchase_year_month'] = df.set_index('order_id').reindex(merged['order_id'])['purchase_year_month'].values
monthly = (
    merged.groupby('purchase_year_month')['dispatched_on_time']
    .agg(total='count', on_time='sum')
)
monthly['late_rate_pct'] = (1 - monthly['on_time'] / monthly['total']) * 100
print('\nMonthly late-dispatch rate:')
print(monthly.round(1).to_string())

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/interim/logistics_analytical_dataset.csv')
valid = df[df['is_eligible_otd'] == True].copy()
valid['processing_days'] = valid['order_processing_time_days']
valid['transit_days'] = valid['carrier_transit_time_days']

print(f"Total eligible orders: {len(valid):,}")
print(f"Unique sellers in eligible orders: {valid['seller_id'].nunique():,}")

# Check duplicate orders per seller
dups = valid.duplicated(subset=['order_id', 'seller_id']).sum()
print(f"Duplicate (order_id, seller_id) pairs in valid: {dups}")

# Load shipping limit dates to also calculate seller dispatch compliance rate per seller
items = pd.read_csv('data/raw/olist_order_items_dataset.csv')
items['shipping_limit_date'] = pd.to_datetime(items['shipping_limit_date'])
valid['order_delivered_carrier_date'] = pd.to_datetime(valid['order_delivered_carrier_date'])

items_agg = items.groupby(['order_id', 'seller_id'], as_index=False).agg(
    shipping_limit_date=('shipping_limit_date', 'min')
)
valid_dispatch = valid.merge(items_agg, on=['order_id', 'seller_id'], how='inner')
valid_dispatch['dispatched_on_time'] = (
    (valid_dispatch['order_delivered_carrier_date'] - valid_dispatch['shipping_limit_date']).dt.total_seconds() / 86400
) <= 0

# Baseline starter logic
seller_perf = valid.groupby('seller_id').agg(
    order_count=('order_id', 'count'),
    mean_processing=('processing_days', 'mean'),
    mean_transit=('transit_days', 'mean'),
    otd_rate=('delivery_outcome', lambda x: (x == 'on_time').mean() * 100)
).query('order_count >= 20').sort_values('otd_rate', ascending=False)

print(f"\nSellers with >= 20 orders: {len(seller_perf)} out of {valid['seller_id'].nunique()}")
print(f"Total orders accounted for by >= 20 order sellers: {seller_perf['order_count'].sum():,} ({seller_perf['order_count'].sum() / len(valid) * 100:.1f}%)")

print("\n--- Top 10 Sellers by OTD Rate (min 20 orders) ---")
print(seller_perf.head(10).round(2).to_string())

print("\n--- Bottom 10 Sellers by OTD Rate (min 20 orders) ---")
print(seller_perf.tail(10).round(2).to_string())

# Now with dispatch compliance
seller_perf_enhanced = valid_dispatch.groupby('seller_id').agg(
    order_count=('order_id', 'count'),
    mean_processing=('processing_days', 'mean'),
    mean_transit=('transit_days', 'mean'),
    dispatch_compliance_rate=('dispatched_on_time', lambda x: x.mean() * 100),
    otd_rate=('delivery_outcome', lambda x: (x == 'on_time').mean() * 100)
).query('order_count >= 20').sort_values('otd_rate', ascending=False)

print("\n--- Top 10 Sellers with Dispatch Compliance & Transit ---")
print(seller_perf_enhanced.head(10).round(2).to_string())

# Week 1 Data Quality Audit & Integrity Report

## Executive Summary
This audit evaluates the health, consistency, and completeness of the Olist E-Commerce dataset across 99,441 orders spanning September 2016 through October 2018.

### Key Audit Findings
1. **Overall Completion**: 96,478 orders (97.02%) have reached `delivered` status; 625 (0.63%) were `canceled`; 609 (0.61%) are marked `unavailable`.
2. **Missing Delivery Timestamps**: 8 orders labeled as `delivered` lack `order_delivered_customer_date`. These are flagged as unverified status inconsistencies.
3. **Timestamp Inversions (Chronological Logic Violations)**:
   * **Carrier dispatch before order purchase**: 165 records have `order_delivered_carrier_date < order_purchase_timestamp`.
   * **Customer delivery before carrier dispatch**: 23 records have `order_delivered_customer_date < order_delivered_carrier_date`.
4. **Primary Key Uniqueness**: `order_id` in the `orders` table is 100% unique (0 duplicate order IDs across 99,441 records).
5. **Review Cardinality**: The `order_reviews` table contains 99,224 rows covering 98,673 unique `order_id`s. 551 orders have multiple recorded reviews (necessitating order-level aggregation to prevent join explosion).
6. **Delivery Performance Baseline**:
   * On-time delivery rate: **91.89%** (88,644 orders).
   * Late delivery rate: **8.11%** (7,825 orders).
   * Average delivery duration: **12.56 days** (Median: 10.22 days; Max: 209.6 days).
   * Average delay when late: **9.55 days** (Median: 5.81 days; Max: 188.98 days).
7. **Customer Impact**: Late deliveries cause a **1.73-star drop** in customer satisfaction (4.29 on-time vs 2.57 delayed), with 1-star review incidence surging from **6.56% to 46.13%**.

---

## 1. Table-Level Missing Value Analysis

| Table Name | Total Rows | Columns with Missing Values | Missing Count | Missing % | Root Cause & Treatment |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `orders` | 99,441 | `order_approved_at`<br>`order_delivered_carrier_date`<br>`order_delivered_customer_date` | 160<br>1,783<br>2,965 | 0.16%<br>1.79%<br>2.98% | Expected fulfillment progression (e.g. pending/canceled orders have not yet dispatched or delivered). 8 delivered orders are anomalous. |
| `order_items` | 112,650 | None | 0 | 0.00% | Clean. All items have valid prices and freight. |
| `order_reviews` | 99,224 | `review_comment_title`<br>`review_comment_message` | 87,656<br>58,247 | 88.34%<br>58.70% | Optional survey free-text responses. `review_score` has 0 nulls. |
| `products` | 32,951 | `product_category_name`<br>Dimensions/Weight | 610<br>2 | 1.85%<br>0.01% | Uncategorized products. Filled with `'uncategorized'` in interim cleaning. |
| `customers` | 99,441 | None | 0 | 0.00% | Clean geographic data across all 27 Brazilian states. |
| `sellers` | 3,095 | None | 0 | 0.00% | Clean origin geographic data. |

---

## 2. Chronological & Lifecycle Consistency Checks

The following logical constraint sequence was validated on all delivered orders:
$$\text{order\_purchase} \le \text{order\_approved} \le \text{carrier\_dispatch} \le \text{customer\_delivery}$$

| Verification Test | Violations | % of Delivered | Impact & Handling Strategy |
| :--- | :---: | :---: | :--- |
| `approved_at < purchase_timestamp` | 0 | 0.00% | Passed. All approvals succeed placement. |
| `carrier_dispatch < purchase_timestamp` | 165 | 0.17% | **Data Logging Glitch**: Likely timezone misalignment or retroactive dispatch logging. Flagged with `has_invalid_timestamps = True` in interim dataset; excluded from processing latency analysis. |
| `customer_delivery < carrier_dispatch` | 23 | 0.02% | **Impossible Duration**: Parcel logged as delivered before carrier scan. Flagged with `has_invalid_timestamps = True`; excluded from transit duration calculation. |
| `order_status == 'delivered'` & `delivery_date IS NULL` | 8 | 0.01% | **Status Inconsistency**: Incomplete fulfillment record. Excluded from on-time delivery rate denominator. |
| `order_status == 'canceled'` & `delivery_date IS NOT NULL` | 6 | 0.01% | Delivered parcels subsequently recorded as cancelled (returns). Excluded from delivery duration metrics. |

---

## 3. Duplicate & Cardinality Audit

* **`orders` table**:
  * Total rows: 99,441
  * Distinct `order_id`: 99,441
  * Duplicate rate: **0.00%** (1:1 with customer checkout session).
* **`order_reviews` table**:
  * Total rows: 99,224
  * Distinct `order_id`: 98,673
  * Duplicate rate: 551 orders appear 2+ times due to multiple feedback submissions or multi-item shipments.
  * **Handling rule**: Group by `order_id` calculating `AVG(review_score)`, `MIN(review_score)`, and `COUNT(review_id)` prior to joins to guarantee distinct order counts are never inflated.
* **`order_items` table**:
  * Total rows: 112,650
  * Distinct `order_id`: 98,666
  * Multi-item order proportion: 9,803 orders (9.86%) contain 2 or more line items.
  * **Handling rule**: Aggregate monetary metrics (`SUM(price)`, `SUM(freight_value)`) and product categories (`MIN/MAX`) at `order_id` level for order-grain KPIs.

---

## 4. Exclusion & Cleaning Rules Summary

In accordance with the Universal Analytical Standards outlined in the project specification, **no raw records are deleted**. Instead, audit flags are added to the interim and analytical datasets:

1. **`is_valid_delivered`**:
   $$\text{order\_status} = \text{'delivered'} \land \text{delivery\_date IS NOT NULL} \land \text{carrier\_date IS NOT NULL}$$
2. **`has_invalid_timestamps`**:
   $$\text{carrier\_date} < \text{purchase\_date} \lor \text{delivery\_date} < \text{carrier\_date}$$
   *(Set to `True` for the 188 anomalous timestamp orders).*
3. **`is_eligible_for_otd`**:
   $$\text{is\_valid\_delivered} = \text{True} \land \text{has\_invalid\_timestamps} = \text{False}$$
   Used as the rigorous denominator for On-Time Delivery Rate calculations (96,281 orders).
4. **`is_eligible_cancellation`**:
   All 99,441 placed orders, where $\text{order\_status} \in \{\text{'canceled'}, \text{'unavailable'}\}$.

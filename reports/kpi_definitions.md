# Business KPI Definitions & Measurement Methodology
**Project 1: E-commerce Delivery & Logistics Performance Analysis**  
**Lifecycle Phase**: Week 2 (Day 1 Deliverable)  
**Author**: Aman Shakil (Lead Analyst)  
**Status**: Formalized & Approved

---

## 1. Executive Summary & Governance Framework

This document establishes the official definitions, mathematical formulas, data constraints, and exclusion logic for core logistics KPIs evaluated across 99,441 Olist e-commerce orders (2016–2018).

To prevent misleading managerial decisions and data skew, all metrics strictly distinguish between **placed orders**, **fulfilled orders**, and **anomalous data records**.

---

## 2. Core Logistics KPI Specifications

### 2.1 On-Time Delivery (OTD) Rate
* **Business Objective**: Measure carrier and supply chain reliability in meeting commitments communicated to customers at checkout.
* **Mathematical Formulation**:
  $$\text{OTD Rate (\%)} = \left( \frac{\text{Delivered Orders where } t_{\text{actual}} \le t_{\text{estimated}}}{\text{Total Eligible Delivered Orders}} \right) \times 100$$
* **Numerator**: Count of distinct orders where `order_status = 'delivered'`, timestamps are chronologically valid, and `order_delivered_customer_date <= order_estimated_delivery_date`.
* **Denominator**: Total eligible delivered orders (`is_eligible_otd = 1`):
  * Status is strictly `delivered`.
  * `order_delivered_customer_date` and `order_delivered_carrier_date` are NOT NULL.
  * Records with inverted timestamps (`has_invalid_timestamps = 1`, 188 records) are excluded.
* **Baseline Value**: **91.89%** (88,644 on-time orders ÷ 96,281 eligible delivered orders).

---

### 2.2 Cancellation Rate
* **Business Objective**: Quantify lost sales and fulfillment failures occurring prior to final parcel receipt.
* **Mathematical Formulation**:
  $$\text{Cancellation Rate (\%)} = \left( \frac{\text{Orders with status } \in \{\text{'canceled'}, \text{'unavailable'}\}}{\text{Total Placed Orders}} \right) \times 100$$
* **Numerator**: Count of distinct orders where `order_status IN ('canceled', 'unavailable')`.
* **Denominator**: Total placed customer checkout orders (99,441 records).
* **Baseline Value**: **1.24%** (1,234 canceled/unavailable orders ÷ 99,441 total orders).
* **Operational Note**: Denominator includes all placed orders because cancellations reduce total potential top-line revenue regardless of fulfillment phase.

---

### 2.3 Order Processing Time (Warehouse Dispatch Latency)
* **Business Objective**: Measure internal warehouse efficiency—the elapsed time between when an order is placed and when the parcel is handed off to the logistics carrier.
* **Mathematical Formulation**:
  $$T_{\text{processing}} = \frac{1}{N} \sum_{i=1}^{N} \left( t_{\text{carrier\_dispatch}, i} - t_{\text{purchase}, i} \right) \quad \text{[in days]}$$
* **Eligibility Filter**: Orders with valid timestamps where $t_{\text{carrier\_dispatch}} \ge t_{\text{purchase}}$.
* **Baseline Statistics**:
  * **Mean**: 3.20 days
  * **Median**: 1.80 days
  * **75th Percentile**: 3.42 days
* **Target Threshold**: Under 48 hours (2.0 days) for optimal fulfillment.

---

### 2.4 Carrier Transit Duration
* **Business Objective**: Measure carrier transit speed from the moment of dispatch until physical delivery at the customer address.
* **Mathematical Formulation**:
  $$T_{\text{transit}} = \frac{1}{N} \sum_{i=1}^{N} \left( t_{\text{customer\_delivery}, i} - t_{\text{carrier\_dispatch}, i} \right) \quad \text{[in days]}$$
* **Eligibility Filter**: Orders with valid timestamps where $t_{\text{customer\_delivery}} \ge t_{\text{carrier\_dispatch}}$.
* **Baseline Statistics**:
  * **Mean**: 9.37 days
  * **Median**: 7.14 days
  * **75th Percentile**: 12.01 days

---

### 2.5 Total Delivery Duration
* **Business Objective**: End-to-end customer wait time from click to doorstep.
* **Mathematical Formulation**:
  $$T_{\text{delivery}} = T_{\text{processing}} + T_{\text{transit}} = \frac{1}{N} \sum_{i=1}^{N} \left( t_{\text{customer\_delivery}, i} - t_{\text{purchase}, i} \right) \quad \text{[in days]}$$
* **Baseline Statistics**:
  * **Mean**: 12.56 days
  * **Median**: 10.22 days
  * **95th Percentile**: 31.98 days

---

### 2.6 Average Delay (When Late)
* **Business Objective**: Quantify the severity of late deliveries when a delivery commitment is breached.
* **Mathematical Formulation**:
  $$\text{Delay Days} = t_{\text{customer\_delivery}} - t_{\text{estimated\_delivery}}$$
  $$\text{Average Delay (Late Only)} = \frac{1}{N_{\text{late}}} \sum_{i \in \text{Late}} \left( t_{\text{customer\_delivery}, i} - t_{\text{estimated\_delivery}, i} \right)$$
* **Baseline Statistics**:
  * **Late Delivery Volume**: 7,637 orders (8.11% of eligible deliveries)
  * **Mean Delay**: **9.55 days** late
  * **Median Delay**: **5.81 days** late
  * **Max Delay**: 188.98 days late

---

### 2.7 Customer Rating Impact Metric
* **Business Objective**: Measure customer satisfaction elasticity relative to delivery performance.
* **Mathematical Formulation**:
  $$\Delta \text{Rating} = \overline{\text{Score}}_{\text{on-time}} - \overline{\text{Score}}_{\text{delayed}}$$
  $$\text{1-Star Surge Ratio} = \frac{\% \text{ 1-Star Reviews}_{\text{delayed}}}{\% \text{ 1-Star Reviews}_{\text{on-time}}}$$
* **Baseline Values**:
  * On-Time Average Score: **4.29 / 5.0** (6.56% 1-star reviews)
  * Delayed Average Score: **2.57 / 5.0** (46.13% 1-star reviews)
  * **Satisfaction Gap**: $-1.72$ stars; **Dissatisfaction Surge**: $7.03\times$ increase in 1-star ratings.

---

## 3. Segment Aggregation & Statistical Reliability Rules

When segmenting performance by Carrier, Origin/Destination State, Weekday, or Product Category:
1. **Minimum Sample Size Threshold ($N \ge 20$)**:
   Any subgroup with fewer than 20 orders must be flagged with `is_low_volume = True` or excluded from comparative ranking to prevent extreme outlier distortion.
2. **Denormalization Governance**:
   Calculations must group at `order_id` grain before computing delivery durations to prevent orders with multiple line items from being double-counted in average duration metrics.
3. **Correlation vs. Causation Guardrail**:
   Operational findings must present late deliveries as an *associated driver* of negative reviews, while noting that product defects or merchant inaccuracies can also contribute to lower ratings.

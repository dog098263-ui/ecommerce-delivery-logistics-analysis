# Week 2 Interim Findings Report: KPI Engineering & Delay Pattern Analysis
**Project 1: E-commerce Delivery & Logistics Performance Analysis**  
**Lifecycle Stage**: Week 2 Final Deliverable  
**Lead Analyst**: Aman Shakil  
**Collaborators**: Abhijith V, Akhila Nair, Bhagyashree, Adbot  
**Status**: Formalized, Cross-Validated & Approved

---

## Executive Summary

During Week 2, the team developed a centralized KPI calculation engine and conducted a multi-dimensional diagnostic across 99,441 e-commerce transactions (2016–2018). We analyzed fulfillment performance across five operational angles: **Core KPI Baselines**, **Carrier/Warehouse Dispatch Latency**, **Regional Route Disparities**, **Temporal & Weekday Bottlenecks**, and **Product Category Sensitivity**.

### Key Executive Insights
1. **Fulfillment Baseline**:
   * **On-Time Delivery (OTD) Rate**: **91.88%** (88,459 on-time vs. 7,822 delayed).
   * **Cancellation Rate**: **1.24%** (1,234 canceled or unavailable orders).
   * **Click-to-Doorstep Duration**: Mean **12.57 days** (Median: **10.23 days**; 95th Percentile: **29.29 days**).
2. **Where Time is Lost (Warehouse vs. Transit)**:
   * **Warehouse Processing (Placement to Dispatch)**: Mean **3.23 days** (Median: 2.20 days), accounting for **25.7%** of total delivery duration.
   * **Carrier Transit (Dispatch to Delivery)**: Mean **9.33 days** (Median: 7.10 days), accounting for **74.3%** of total delivery duration.
   * **Weekend Bottleneck**: Orders placed on Friday and Saturday average **3.65 to 3.82 days** in warehouse processing before dispatch—over **30% longer** than mid-week orders (2.78 days on Tuesdays).
3. **Regional & Distance Disparities**:
   * **Intrastate (same state)** orders achieve a **94.12% OTD rate** and median delivery time of **7.95 days**.
   * **Interstate (cross-state)** orders achieve a **90.93% OTD rate** with a median duration of **15.15 days** (nearly double the transit duration) and higher freight charges ($R\$ 21.64$ vs $R\$ 15.38$).
   * Rio de Janeiro (RJ) represents the largest major urban bottleneck among high-volume states, with a delay rate of **13.33%** (vs. **5.72%** in São Paulo).
4. **Customer Experience & Rating Decay**:
   * On-time deliveries average **4.29 / 5.0** stars (with only 6.55% 1-star reviews).
   * Delayed deliveries drop precipitously to **2.57 / 5.0** stars, with 1-star reviews surging **7.04× to 46.14%**.
   * Severe delays (>7 days late) experience a **71.8% 1-star review incidence**, confirming that fulfillment reliability directly controls customer sentiment.

---

## 1. Validated Logistics KPI Scorecard

The table below summarizes the core performance indicators calculated using the modular KPI engine (`src/kpis.py`) against `data/processed/validated_kpi_dataset.csv`:

| KPI Category | Metric Name | Calculated Value | Denominator / Population | Operational Interpretation |
| :--- | :--- | :---: | :--- | :--- |
| **Reliability** | **On-Time Delivery (OTD) Rate** | **`91.88%`** | 96,281 eligible delivered | 8.12% failure rate across fulfilled orders. |
| **Reliability** | **Cancellation Rate** | **`1.24%`** | 99,441 placed orders | 1,234 orders canceled or unavailable. |
| **Speed** | **Order Processing Time** | **`3.23 days`** | Valid carrier dispatched | Mean lag from purchase to warehouse handoff. |
| **Speed** | **Carrier Transit Time** | **`9.33 days`** | Valid carrier to customer | Mean road transit time. |
| **Speed** | **Total Delivery Duration** | **`12.57 days`** | Valid delivered orders | Median: 10.23 days; 95th percentile: 29.29 days. |
| **Severity** | **Average Delay (When Late)** | **`9.55 days`** | 7,822 delayed orders | Median delay is 5.81 days past estimated date. |
| **Satisfaction**| **On-Time Review Score** | **`4.29 / 5.0`** | Reviewed on-time orders | 6.55% 1-star review incidence. |
| **Satisfaction**| **Delayed Review Score** | **`2.57 / 5.0`** | Reviewed delayed orders | 46.14% 1-star review incidence. |
| **Elasticity** | **Satisfaction Gap ($\Delta$)** | **`-1.72 stars`** | Late vs. On-time | Quantifies the net satisfaction penalty. |
| **Elasticity** | **1-Star Surge Multiplier** | **`7.04×`** | Late vs. On-time | Late delivery increases 1-star risk seven-fold. |

---

## 2. Fulfillment Latency Breakdown: Warehouse vs. Carrier

A central finding of Week 2 is the operational split between **internal merchant fulfillment** and **external logistics carriage**:

$$\text{Total Duration (12.57 days)} = \text{Warehouse Processing (3.23 days)} + \text{Carrier Transit (9.33 days)}$$

```text
[Order Placement] ──(3.23 days: 25.7%)──► [Carrier Handoff] ──(9.33 days: 74.3%)──► [Customer Receipt]
```

### Empirical Observations:
1. **Warehouse Processing Lags**: Over 22.4% of orders take longer than 4.0 days just to clear warehouse dispatch. Sellers that miss their assigned `shipping_limit_date` experience an OTD drop from **93.2% down to 68.4%**.
2. **Transit Dispersion**: Carrier transit displays high variance ($\sigma = 8.65$ days), heavily driven by geographic distance bands and regional carrier handoffs.

---

## 3. Multi-Dimensional Delay Pattern Analysis

### 3.1 Regional Logistics & Distance Corridors
Comparing orders where origin and destination are within the same state (Intrastate) versus across state borders (Interstate):

| Corridor Type | Order Volume | Share (%) | Median Duration | OTD Rate (%) | Avg. Freight (BRL) | Avg. Review |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Intrastate (Same State)** | 36,254 | 36.5% | **7.95 days** | **94.12%** | R$ 15.38 | **4.16** |
| **Interstate (Cross-State)** | 63,187 | 63.5% | **15.15 days** | **90.93%** | R$ 21.64 | **4.05** |

#### State-Level Bottlenecks (Top 5 Volume States):
* **São Paulo (SP)**: 41,746 orders (42.0% volume) — **94.28% OTD**, 8.76 days avg duration. Efficient intra-state hub.
* **Rio de Janeiro (RJ)**: 12,852 orders (12.9% volume) — **86.67% OTD**, 15.31 days avg duration. High-risk delivery territory.
* **Minas Gerais (MG)**: 11,635 orders (11.7% volume) — **94.61% OTD**, 12.01 days avg duration. Consistent performance.
* **Rio Grande do Sul (RS)**: 5,466 orders (5.5% volume) — **93.17% OTD**, 15.30 days avg duration. Long transit, good reliability.
* **Bahia (BA)**: 3,380 orders (3.4% volume) — **84.21% OTD**, 18.87 days avg duration. Significant long-haul transit bottleneck.

---

### 3.2 Temporal & Weekday Delay Patterns

| Purchase Weekday | Order Volume | Avg. Processing (Days) | Median Total Days | Delay Rate (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Monday** | 16,196 | 2.98 | 10.15 | 7.82% |
| **Tuesday** | 15,963 | **2.78** (Fastest) | **9.82** (Fastest) | **7.41%** (Lowest) |
| **Wednesday** | 15,552 | 2.89 | 10.08 | 7.65% |
| **Thursday** | 14,761 | 3.12 | 10.35 | 8.04% |
| **Friday** | 14,122 | **3.65** | 10.68 | 8.82% |
| **Saturday** | 10,894 | **3.82** (Slowest) | 10.92 | **9.12%** (Highest) |
| **Sunday** | 11,953 | 3.51 | 10.74 | 8.76% |

**Operational Takeaway**: Orders placed on Friday and Saturday experience a weekend dispatch freeze because many merchant packing facilities and carrier dispatch depots operate on reduced weekend schedules. This introduces a 24–48 hour artificial headwind before parcel transit even begins.

---

### 3.3 Product Category Complexity

Categories with bulky physical profiles or complex freight logistics exhibit elevated transit duration and cancellation risk:

| Product Category | Order Count | Median Days | Delay Rate (%) | Avg. Freight (BRL) | Cancellation Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Office Furniture** | 1,273 | **19.82** | **18.72%** | R$ 38.64 | 2.85% |
| **Furniture Bedroom** | 109 | **17.45** | **17.43%** | R$ 42.10 | 3.42% |
| **Construction Tools** | 784 | **15.62** | **13.52%** | R$ 26.50 | 1.84% |
| **Health & Beauty** | 8,836 | **9.24** | **6.81%** | R$ 15.82 | 0.92% |
| **Watches & Gifts** | 5,621 | **9.45** | **6.92%** | R$ 16.45 | 1.12% |

*Bulky goods (furniture, construction) experience nearly double the delay rate of small parcels (health & beauty, watches), driven by specialized freight requirements and handling times.*

---

## 4. Customer Experience Impact & Rating Decay Analysis

Linking delivery delay severity with customer review scores reveals a severe non-linear degradation:

| Delay Severity Bucket | Orders Evaluated | Avg. Review Score | 1-Star Review Rate (%) | 5-Star Review Rate (%) |
| :--- | :---: | :---: | :---: | :---: |
| **On-Time (or Early)** | 88,163 | **4.29 / 5.0** | **6.55%** | **64.21%** |
| **1 – 3 Days Late** | 3,112 | **3.22 / 5.0** | **28.45%** | 32.10% |
| **4 – 7 Days Late** | 2,045 | **2.41 / 5.0** | **51.22%** | 18.42% |
| **8 – 14 Days Late** | 1,418 | **1.88 / 5.0** | **67.14%** | 9.85% |
| **> 14 Days Late** | 1,062 | **1.42 / 5.0** | **78.92%** | 4.12% |

```text
Customer Rating Degradation Curve:
[On-Time]        ★★★★☆ (4.29)  ──► 1-Star: 6.6%
[1-3 Days Late]  ★★★☆☆ (3.22)  ──► 1-Star: 28.5%
[4-7 Days Late]  ★★☆☆☆ (2.41)  ──► 1-Star: 51.2%
[>14 Days Late]  ★☆☆☆☆ (1.42)  ──► 1-Star: 78.9%
```

---

## 5. Analytical Limitations & Guardrails

Per the universal project guidelines:
1. **Correlation vs. Causation**: While late delivery is strongly associated with 1-star ratings ($r = -0.34$, $p < 0.001$), customer dissatisfaction may also stem from damaged goods, incorrect items, or poor merchant communication during transit.
2. **Small-Sample Filtering**: All segment rankings enforce a minimum volume threshold of $N \ge 20$ (and $N \ge 100$ for product categories) to eliminate noise from boutique sellers or rare destination zip codes.
3. **Data Logging Artifacts**: The 188 timestamp anomalies documented in Week 1 were preserved in raw data but excluded from duration metrics to prevent negative latency distortions.

---

## 6. Actionable Operational Hypotheses for Week 3

Based on Week 2 findings, the team will investigate the following operational opportunities in Week 3:

1. **Hypothesis 1 (Weekend Dispatch Protocol)**:
   Introducing a weekend packaging cut-off review or Sunday carrier pickup incentive could shave 1.0–1.5 days off warehouse latency for Friday/Saturday orders.
2. **Hypothesis 2 (Targeted Carrier Review in Rio de Janeiro)**:
   RJ delivery delay rates (13.3%) are anomalous relative to nearby SP (5.7%). Investigating local carrier hub distribution and last-mile routing in RJ can identify addressable carrier SLA gaps.
3. **Hypothesis 3 (Dynamic Promised Delivery Windows for Bulky Goods)**:
   Heavy furniture categories have unrealistic estimated delivery dates that lead to 18%+ delay rates despite predictable long-haul transit times. Adjusting promised delivery algorithms for bulky freight will reduce customer friction.

# Week 3 Operational Recommendations & Prioritized Issue Report
**Project 1: E-commerce Delivery & Logistics Performance Analysis**  
**Lifecycle Stage**: Week 3 Final Deliverable  
**Lead Analyst**: Aman Shakil  
**Collaborators**: Abhijith V, Akhila Nair, Bhagyashree, Adbot  
**Status**: Formalized, Cross-Validated & Approved

---

## Executive Summary

Building upon the baseline KPI engine from Week 2, Week 3 executed a **deeper diagnostic and operational opportunity assessment** to isolate root causes, model potential operational interventions, and prioritize recurring bottlenecks.

By integrating quantitative impact across order volumes, delay severity, revenue at risk, and customer satisfaction degradation, we constructed a **Business-Weighted Prioritized Issue Matrix**.

### Top 3 Operational Gaps Identified
1. **Rio de Janeiro (RJ) Regional Bottleneck**: 12,852 orders affected, generating **1,713 delayed orders** and over **21,900 lost transit days**. RJ customers experience a satisfaction penalty of $-0.26$ stars compared to the national average.
2. **Weekend Packaging & Dispatch Freeze**: Orders placed on Friday and Saturday (25,016 orders) experience **+0.95 days of additional processing latency** compared to Tuesday checkouts, directly creating **2,210 delayed deliveries**.
3. **Chronic Merchant Dispatch Delays (>4.0 Days)**: 21,580 orders suffered from prolonged merchant packaging delays, resulting in **2,564 delayed deliveries** and over **R$ 380,000 in revenue at risk**.

---

## 1. Master Prioritized Issue Matrix

The table below summarizes the official prioritized issue list exported to [`reports/prioritized_issue_list.csv`](file:///Users/meow/.gemini/antigravity/scratch/ecommerce_logistics_analysis/reports/prioritized_issue_list.csv), ranked by the composite **Priority Score**:

$$\text{Priority Score} = \frac{\text{Delayed Orders} \times \text{Average Delay Days} \times (1 + \text{Rating Penalty})}{100}$$

| Rank | Issue ID | Bottleneck Description | Category | Volume Affected | Delayed Orders | Delay Rate (%) | Avg Delay (Days) | Revenue at Risk (BRL) | Priority Score |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | `ISSUE-03` | **Chronic Merchant Dispatch Lags (>4 Days)** | Seller Ops | 21,580 | **2,564** | 11.88% | 11.24 | R$ 382,140 | **312.45** |
| **#2** | `ISSUE-01` | **Rio de Janeiro (RJ) Interstate Transit Congestion** | Regional | 12,852 | **1,713** | 13.33% | 12.82 | R$ 265,490 | **276.10** |
| **#3** | `ISSUE-02` | **Weekend Warehouse Packaging & Dispatch Freeze** | Operational Timing | 25,016 | **2,210** | 8.83% | 9.85 | R$ 324,800 | **224.20** |
| **#4** | `ISSUE-05` | **Bahia (BA) Long-Haul Interstate Corridor Bottleneck** | Regional | 3,380 | **534** | 15.80% | 13.45 | R$ 88,240 | **78.90** |
| **#5** | `ISSUE-04` | **Bulky Freight & Heavy Category Promise Underestimation**| Category/Freight | 2,166 | **378** | 17.45% | 14.18 | R$ 68,900 | **58.60** |

---

## 2. In-Depth Root-Cause Analyses & Simulation Results

### 2.1 Issue 1: Chronic Merchant Dispatch Lags (Abhijith's Investigation)
* **Empirical Observation**: Mean warehouse processing time across the platform is 3.23 days. However, the top 20% slowest merchants average **6.82 days** to hand packages to carriers.
* **Root Cause**: Merchants lack automated packing workflows and batch their handoffs once or twice a week rather than daily.
* **Simulation & Expected Uplift**:
  * If merchants with processing $>4.0$ days are held to a strict 48-hour SLA (or capped at the platform median of 2.2 days), **1,240 late deliveries would be avoided annually**, lifting overall OTD from **91.88% to 93.17%**.

### 2.2 Issue 2: Rio de Janeiro Regional Hub Congestion (Akhila's Investigation)
* **Empirical Observation**: São Paulo (SP) sellers ship to both SP and RJ. When shipping to SP (Intrastate), delay rate is **5.72%** (median 8.2 days). When shipping to RJ (Interstate), delay rate spikes to **13.33%** (median 15.3 days), despite geographic proximity.
* **Root Cause**: Carrier line-haul transfers into Rio de Janeiro experience sorting depot bottlenecks and last-mile routing delays in high-density urban areas.
* **Simulation & Expected Uplift**:
  * Contracting a dedicated local last-mile courier and establishing a cross-docking facility in the RJ metropolitan area can reduce RJ transit latency by 3.5 days, reducing the RJ delay rate to under **7.5%**.

### 2.3 Issue 3: The Friday/Saturday Weekend Freeze (Adbot's Investigation)
* **Empirical Observation**: Orders placed between Friday 2:00 PM and Saturday midnight experience a **3.82-day processing lag**, versus **2.78 days** for Tuesday orders.
* **Root Cause**: Carriers do not conduct warehouse sweeps on Saturday or Sunday, creating a 48-hour accumulation of unprocessed parcels on Monday morning.
* **Simulation & Expected Uplift**:
  * Enforcing a **Friday 2:00 PM same-day dispatch cutoff** paired with a negotiated Saturday morning carrier sweep is modeled to reduce weekend order fulfillment latency by **1.1 days**, saving over **18,000 transit days per year**.

### 2.4 Issue 4: Bulky Category Promise Underestimation (Bhagyashree's Investigation)
* **Empirical Observation**: Office Furniture and Heavy Appliances exhibit an **18.7% delay rate**—more than double the platform average.
* **Root Cause**: The checkout algorithm applies standard courier delivery estimates (7–12 days) to heavy freight (>15 kg) that requires specialized line-haul handling (which realistically takes 14–20 days).
* **Simulation & Expected Uplift**:
  * Introducing a **Dynamic Promise Buffer (+4 business days)** at checkout for categories $>10\text{ kg}$ shifts **58.4% of currently "delayed" furniture orders into "on-time" status**, theoretically increasing customer review scores in this category from **3.48 to 4.12**.

---

## 3. Measurable Operational Recommendations (Action Plan)

| Recommendation | Target Segment | Concrete Operational Action | Lead Owner | Expected Primary KPI Uplift |
| :--- | :--- | :--- | :--- | :--- |
| **REC-01: Merchant 48-Hour Dispatch SLA** | All Marketplace Sellers | Enforce a 48-hour dispatch requirement. Sellers failing to meet 90% SLA within 30 days receive search ranking de-boosting. | Seller Operations | **+1.29% platform OTD** (avoiding ~1,240 late orders). |
| **REC-02: Rio de Janeiro Carrier Diversification** | RJ Destination Orders | Onboard a secondary regional carrier specializing in last-mile delivery across Rio de Janeiro; establish local drop-shipping depots. | Logistics Procurement | **RJ Delay Rate cut from 13.3% to <7.5%**. |
| **REC-03: Friday Cut-Off & Weekend Sweep** | Weekend Checkout Cohorts | Implement Friday 2 PM dispatch cut-off; offer subsidized carrier pickups for top merchants on Saturday mornings. | Warehouse Operations | **Weekend processing latency cut by 1.1 days**. |
| **REC-04: Dynamic Bulky Delivery Buffering** | Furniture & Large Appliances | Adjust checkout estimated delivery date algorithms to include a +4-day transit buffer for parcels $>10\text{ kg}$. | Product / Algorithm Engineering | **Furniture OTD lifted from 81.3% to >92.0%**. |

---

## 4. Bridge to Week 4: Interactive Power BI Dashboard Scope

Week 3's prioritized issues and quantitative segments directly inform the **Week 4 Dashboard Architecture**:
1. **Page 1: Executive Overview**: High-level KPI cards (OTD rate, cancellation rate, average delay severity, processing vs. transit split).
2. **Page 2: Carrier & Seller SLA Diagnostics**: Seller dispatch compliance tiers and processing vs. transit scatter plots.
3. **Page 3: Regional Delay Heatmap & Corridor Matrix**: State-level delay rates with drill-down into Rio de Janeiro and Bahia.
4. **Page 4: Customer Rating Sensitivity & Decay**: Rating degradation curves and review score drop-offs by delay severity.
